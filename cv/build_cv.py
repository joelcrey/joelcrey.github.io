"""Build the CV web page data and the PDF from cv/cv.xlsx.

    python3 cv/build_cv.py          # writes _data/cv.json and cv/sections.tex
    python3 cv/build_cv.py --pdf    # also compiles cv/acadcv.tex and copies it to acadcv.pdf

In cv.xlsx, the "Sections" sheet lists the sections in order. A section of type "list" takes its
rows from the sheet with the same name, listed oldest first (the CV shows them newest first); one of
type "events" takes the rows of the "Events" sheet with its contribution (invited talk, talk, poster
or attended); one of type "text" uses the text column. Text cells may use
*italics* and **bold**. Only the Python standard library is needed.
"""
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

CV_DIR = Path(__file__).resolve().parent
ROOT = CV_DIR.parent
XLSX = CV_DIR / "cv.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}


# --- Reading the spreadsheet ------------------------------------------------

def read_xlsx(path):
    """Return {sheet name: list of rows}, each row a list of cell strings."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
        rels = {r.get("Id"): r.get("Target")
                for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("pr:Relationship", NS)}
        sheets = {}
        for sheet in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS):
            target = rels[sheet.get(f"{{{NS['r']}}}id")].lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            sheets[sheet.get("name")] = read_sheet(ET.fromstring(z.read(target)), shared)
        return sheets


def read_sheet(root, shared):
    rows = []
    for row in root.iter(f"{{{NS['m']}}}row"):
        cells = {}
        for c in row.findall("m:c", NS):
            col = column_index(c.get("r"))
            kind, v = c.get("t"), c.find("m:v", NS)
            if kind == "s":
                value = shared[int(v.text)]
            elif kind == "inlineStr":
                value = "".join(t.text or "" for t in c.iter(f"{{{NS['m']}}}t"))
            elif v is not None:
                value = v.text or ""
            else:
                value = ""
            cells[col] = value.strip()
        rows.append([cells.get(i, "") for i in range(max(cells, default=-1) + 1)])
    return rows


def column_index(ref):
    letters = re.match(r"[A-Z]+", ref).group()
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def as_records(rows):
    """Turn rows into dicts keyed by the header row, skipping empty rows."""
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0]]
    records = []
    for row in rows[1:]:
        if not any(row):
            continue
        records.append({h: (row[i] if i < len(row) else "") for i, h in enumerate(header) if h})
    return records


def excel_date(value):
    """Excel stores typed dates as day numbers; show those as e.g. 'Nov 2025'."""
    if re.fullmatch(r"\d{5}(\.\d+)?", value):
        return (date(1899, 12, 30) + timedelta(days=float(value))).strftime("%b %Y")
    return value


def yes(value, default=True):
    value = value.strip().lower()
    return default if not value else value in ("yes", "y", "true", "1", "x")


# --- Formatting --------------------------------------------------------------

def inline(text, bold, italic, escape):
    """Apply **bold** and *italics* markers, escaping everything else."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*|\*.+?\*)", text):
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append(bold(escape(part[2:-2])))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append(italic(escape(part[1:-1])))
        else:
            out.append(escape(part))
    return "".join(out)


TEX_SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
               "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def tex_escape(text):
    return "".join(TEX_SPECIAL.get(ch, ch) for ch in text)


def tex(text, link=""):
    out = inline(text, lambda s: r"\textbf{%s}" % s, lambda s: r"\emph{%s}" % s, tex_escape)
    return r"\href{%s}{%s}" % (link.replace("%", r"\%").replace("#", r"\#"), out) if link and out else out


def web(text, link=""):
    out = inline(text, lambda s: f"<strong>{s}</strong>", lambda s: f"<em>{s}</em>", html.escape)
    return f'<a href="{html.escape(link)}">{out}</a>' if link and out else out


def web_entry(e):
    """One line of the web CV: **title**, institution, place. date. details"""
    head = ", ".join(x for x in [f"<strong>{web(e['title'], e.get('title_link', ''))}</strong>" if e["title"] else "",
                                 web(e.get("institution", ""), e.get("institution_link", "")),
                                 web(e.get("place", ""))] if x)
    parts = [head, web(e.get("date", ""))]
    line = ". ".join(p.rstrip(".") for p in parts if p) + "."
    details = web(e.get("details", ""), e.get("details_link", ""))
    return f"{line} {details}" if details else line


def tex_entry(e, details):
    args = [tex(e.get("date", "")), tex(e["title"], e.get("title_link", "")),
            tex(e.get("institution", ""), e.get("institution_link", "")), tex(e.get("place", "")), "",
            tex(e.get("details", ""), e.get("details_link", "")) if details else ""]
    return r"\cventry" + "".join("{%s}" % a for a in args)


def event_entry(e):
    """Turn a row of the Events sheet into an entry, laid out as each section of the CV expects.

    invited talk:  **host**, *event*, place. Talk title in the details.
    talk:          ***talk title***, event, host, place.
    poster:        **event**, *host*, place. Poster title in the details.
    attended:      **event**, *host*, place.
    """
    kind = e.get("contribution", "").strip().lower() or "attended"
    entry = {k: e.get(k, "") for k in ("date", "place", "web", "pdf")}
    event, link, host = e.get("event", ""), e.get("event_link", ""), e.get("host", "")
    if kind == "invited talk" and host:
        entry.update(title=host, institution=event, institution_link=link)
    elif kind == "talk":
        entry.update(title=e.get("title", ""), title_link=e.get("title_link", ""),
                     institution=", ".join(x for x in (event, host) if x))
        return entry
    else:
        entry.update(title=event, title_link=link, institution=host)
    entry.update(details=e.get("title", ""), details_link=e.get("title_link", ""))
    return entry


# --- Build -------------------------------------------------------------------

def build():
    sheets = read_xlsx(XLSX)
    web_sections, tex_lines = [], ["% Generated by cv/build_cv.py from cv/cv.xlsx. Do not edit by hand.", ""]
    for s in as_records(sheets.get("Sections", [])):
        name, kind = s.get("section", ""), s.get("type", "").strip().lower()
        if not name or kind not in ("list", "text", "events"):
            continue
        show_web, show_pdf = yes(s.get("web", "")), yes(s.get("pdf", ""))
        if kind == "text":
            if show_web:
                web_sections.append({"title": name, "text": web(s.get("text", ""))})
            if show_pdf:
                tex_lines += [r"\section{%s}" % tex_escape(name), tex(s.get("text", "")), ""]
            continue
        if kind == "events":
            wanted = s.get("contribution", "").strip().lower() or "attended"
            rows = [event_entry(e) for e in as_records(sheets.get("Events", []))
                    if (e.get("contribution", "").strip().lower() or "attended") == wanted]
        elif name in sheets:
            rows = as_records(sheets[name])
        else:
            sys.exit(f'cv.xlsx: section "{name}" has no sheet with that name')
        # The sheets list entries oldest first; the CV shows them newest first
        rows = [e for e in rows if e.get("title") or e.get("institution")][::-1]
        for e in rows:
            e["date"] = excel_date(e.get("date", ""))
        web_rows = [web_entry(e) for e in rows if yes(e.get("web", ""))]
        pdf_rows = [e for e in rows if yes(e.get("pdf", ""))]
        if show_web and web_rows:
            web_sections.append({"title": name, "items": web_rows})
        if show_pdf and pdf_rows:
            tex_lines.append(r"\section{%s}" % tex_escape(name))
            details = yes(s.get("details_in_pdf", ""))
            tex_lines += [tex_entry(e, details) for e in pdf_rows] + [""]

    (ROOT / "_data").mkdir(exist_ok=True)
    (ROOT / "_data" / "cv.json").write_text(json.dumps(web_sections, ensure_ascii=False, indent=1) + "\n")
    (CV_DIR / "sections.tex").write_text("\n".join(tex_lines))
    print("wrote _data/cv.json and cv/sections.tex")


def build_pdf():
    subprocess.run(["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error", "acadcv.tex"],
                   cwd=CV_DIR, check=True, stdout=subprocess.DEVNULL)
    shutil.copy(CV_DIR / "acadcv.pdf", ROOT / "acadcv.pdf")
    print("wrote acadcv.pdf")


if __name__ == "__main__":
    build()
    if "--pdf" in sys.argv:
        build_pdf()
