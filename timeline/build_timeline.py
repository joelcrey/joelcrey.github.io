"""Build the timeline page data from the Obsidian canvas.

    python3 timeline/build_timeline.py

Reads the canvas named in timeline/timeline.toml and writes _data/timeline.json. Only cards with a
year that do not look like private notes are written, so nothing else from the canvas reaches the
site; the script lists everything it left out. Only the Python standard library is needed.
"""
import json
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parent
CONFIG = DIR / "timeline.toml"
OUT = ROOT / "_data" / "timeline.json"

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
YEAR = re.compile(r"\b(1[89]\d\d|20\d\d)\b")
SPANISH = re.compile(r"\b(lo llamaba|los define|pero no es|como los|hoy día|según)\b", re.I)


def inside(n, g):
    return (g["x"] <= n["x"] and g["y"] <= n["y"]
            and n["x"] + n["width"] <= g["x"] + g["width"]
            and n["y"] + n["height"] <= g["y"] + g["height"])


def starts(text, prefixes):
    return next((p for p in prefixes if text.startswith(p)), None)


def private_reasons(text):
    """Why a card looks like a note to self rather than an entry for the page."""
    reasons = []
    if "?" in text:
        reasons.append("question mark")
    if text.startswith("*") and not text.startswith("**"):
        reasons.append("side comment")
    if SPANISH.search(text):
        reasons.append("in Spanish")
    if len(text) > 220:
        reasons.append("long comment")
    return reasons


def split_title(text, year, links, missing):
    """Title and note of a card, with the year taken out and canvas links made public or plain."""
    def link(m):
        target, label = m.group(1).strip(), (m.group(2) or "").strip()
        label = label or re.sub(r"\.(pdf|md)$", "", target)
        if target in links:
            return f"[{label}]({links[target]})"
        missing.add(target)
        return label
    text = LINK.sub(link, text)
    first, *rest = [line.strip() for line in text.split("\n") if line.strip()]
    first = re.sub(r"^\s*\d{4}\.\s*", "", first)
    first = re.sub(r",?\s*\b%d\b(-\d{4}|/\d{4})?\??\??" % year, "", first)
    first = re.sub(r"\s*\(\s*\)", "", first).strip(" ,.-")
    note = " ".join(rest)
    # A long first line is usually "title: explanation" or "title (explanation)".
    if len(first) > 80:
        m = re.search(r"(?<=.{20})(: |\. | \()", first)
        if m:
            cut = m.start()
            extra = first[cut:].lstrip(":. ")
            first, note = first[:cut].strip(), (extra + " " + note).strip()
    return first, note


def main():
    config = tomllib.loads(CONFIG.read_text())
    canvas_path = (DIR / config["canvas"]).resolve()
    canvas = json.loads(canvas_path.read_text())
    include, exclude = config.get("include", []), config.get("exclude", [])
    place, links = config.get("place", {}), config.get("links", {})
    fields = config["fields"]
    field_of = {g: i for i, f in enumerate(fields) for g in f["groups"]}

    groups = [n for n in canvas["nodes"] if n["type"] == "group"]
    cards = [n for n in canvas["nodes"] if n["type"] == "text"]
    held, undated, unplaced, missing, used = [], 0, [], set(), set()
    entries = []
    for n in cards:
        text = n["text"].strip()
        if re.fullmatch(r"\d{4}", text):  # the year markers on the canvas
            continue
        years = YEAR.findall(LINK.sub(lambda m: m.group(2) or "", text))
        forced_in, forced_out = starts(text, include), starts(text, exclude)
        used.update(p for p in (forced_in, forced_out) if p)
        if forced_out:
            held.append((text, ["excluded in timeline.toml"]))
            continue
        if not years:
            undated += 1
            continue
        reasons = private_reasons(text)
        if reasons and not forced_in:
            held.append((text, reasons))
            continue
        containing = [g for g in groups if inside(n, g)]
        group = min(containing, key=lambda g: g["width"] * g["height"])["label"] if containing else None
        p = starts(text, place)
        if p:
            group = place[p]
            used.add(p)
        if group not in field_of:
            unplaced.append((text, group))
            continue
        year = int(years[0])
        title, note = split_title(text, year, links, missing)
        entries.append({"id": n["id"], "year": year, "title": title, "note": note,
                        "group": group, "field": field_of[group]})

    ids = {e["id"] for e in entries}
    for e in entries:
        e["leads_to"] = sorted({x["toNode"] for x in canvas.get("edges", [])
                                if x["fromNode"] == e["id"] and x["toNode"] in ids})
    entries.sort(key=lambda e: (e["year"], e["field"], e["title"]))

    fields_out = [{"name": f["name"], "color": f["color"]} for f in fields]
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    unchanged = old.get("entries") == entries and old.get("fields") == fields_out
    data = {"updated": old["updated"] if unchanged else date.today().isoformat(),
            "fields": fields_out, "entries": entries}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

    def short(t):
        t = re.sub(r"\s+", " ", LINK.sub(lambda m: m.group(2) or m.group(1), t))
        return t if len(t) <= 90 else t[:87] + "..."
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(entries)} entries"
          f"{' (no changes)' if unchanged else ''}. Left out {undated} cards without a year.")
    if held:
        print("\nHeld back (add the start of the card to `include` in timeline.toml to publish it):")
        for t, why in held:
            print(f"  - {short(t)}  [{', '.join(why)}]")
    if unplaced:
        print("\nLeft out, in no field (add the group to a field, or the card to [place]):")
        for t, g in unplaced:
            print(f"  - {short(t)}  [group: {g or 'none'}]")
    if missing:
        print("\nLinked files with no public link (shown as plain text; add them to [links]):")
        for f in sorted(missing):
            print(f"  - {f}")
    stale = [p for p in [*include, *exclude, *place] if p not in used]
    if stale:
        print("\nIn timeline.toml but matching no card (perhaps the card was edited):")
        for p in stale:
            print(f"  - {p}")


if __name__ == "__main__":
    sys.exit(main())
