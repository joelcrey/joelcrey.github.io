import os
import re

SOURCE_FILE = "index.html"

HEADER_PATTERN = re.compile(
    r"<!-- Header -->(.*?)</header>",
    re.DOTALL
)

SIDEBAR_PATTERN = re.compile(
    r"<!-- Sidebar -->(.*?)<!-- Scripts -->",
    re.DOTALL
)

def extract_section(pattern, text, name):
    match = pattern.search(text)
    if not match:
        raise ValueError(f"No se encontró la sección {name}")
    return match.group(0)

# Leer index.html
with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    source_html = f.read()

print("¿Existe '<!-- Header -->'?", "<!-- Header -->" in source_html)
print("¿Existe '</header>'?", "</header>" in source_html)

header = extract_section(HEADER_PATTERN, source_html, "HEADER")
menu = extract_section(SIDEBAR_PATTERN, source_html, "SIDEBAR")

# Procesar el resto de archivos
for filename in os.listdir("."):
    if not filename.endswith(".html"):
        continue
    if filename == SOURCE_FILE:
        continue

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    html = HEADER_PATTERN.sub(header, html)
    html = SIDEBAR_PATTERN.sub(menu, html)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Actualizado: {filename}")