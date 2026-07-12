#!/usr/bin/env python3
"""
Reformat Modern_Tennis_Handbook.html to match the Vietnamese template style
(Co_Sinh_Hoc_Tennis_Hien_Dai.html):
  - Add DOCTYPE, html lang, head, title, viewport, style block
  - Lift single-cell "card" tables (cover, CHAPTER banners, side-notes, CLOSING)
    into styled <div class="card"> / <div class="card chapter"> blocks
  - Keep multi-cell data tables intact (but tag numbered step tables so they
    get a styled "1"/"2" badge column on the left)
  - Preserve all ASCII art <pre> blocks
  - Preserve the existing <footer class="cc-license">
"""
from bs4 import BeautifulSoup, NavigableString
import re
import os
import html as ihtml

SRC = r"C:\Users\Henry\GITHUB\tennis-wiki\site\cam-nang\tfl\Modern_Tennis_Handbook.html"
DST = SRC
BAK = SRC + ".bak"

VI_CSS = r"""
body {
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  max-width: 900px;
  margin: 32px auto;
  padding: 24px 28px;
  color: #1f2937;
  line-height: 1.7;
}
h1, h2, h3, h4 {
  color: #14285a;
  margin-top: 1.4em;
  margin-bottom: 0.6em;
}
h1 { font-size: 1.8em; border-bottom: 3px solid #b41e1e; padding-bottom: 8px; }
h2 { font-size: 1.4em; }
h3 { font-size: 1.15em; }
p { margin-bottom: 0.9em; }
img { max-width: 100%; height: auto; display: block; margin: 16px auto; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}
th, td {
  border: 1px solid #e5e7eb;
  padding: 8px 12px;
  text-align: left;
  vertical-align: top;
}
th {
  color: #14285a;
  font-weight: 700;
}
ul, ol { margin-bottom: 0.9em; padding-left: 1.6em; }
li { margin-bottom: 0.25em; }
pre.tfl-ascii-art {
  font-family: 'Consolas', 'Menlo', 'Courier New', monospace;
  border: 1px solid #e5e7eb;
  border-left: 3px solid #b41e1e;
  padding: 10px 14px;
  margin: 12px 0;
  white-space: pre;
  overflow-x: auto;
  font-size: 0.9em;
  line-height: 1.25;
}
.card {
  border: 1px solid #e5e7eb;
  border-left: 4px solid #14285a;
  padding: 16px 20px;
  border-radius: 6px;
  margin: 18px 0;
}
.card.chapter {
  border: 1px solid #14285a;
  border-left: 6px solid #14285a;
  padding: 18px 22px;
}
.card.chapter p { margin-bottom: 0.4em; }
.card.chapter p strong { font-size: 1.1em; letter-spacing: 0.02em; color: #14285a; }
.card.chapter p em { color: #b41e1e; font-style: normal; font-weight: 600; }
.card.cover {
  text-align: center;
  border: 2px solid #14285a;
  border-top: 4px solid #b41e1e;
  border-bottom: 4px solid #b41e1e;
  padding: 32px 24px;
}
.card.cover p { margin-bottom: 0.5em; }
.card.cover p.title { font-size: 1.6em; font-weight: 800; letter-spacing: 0.04em; line-height: 1.2; color: #14285a; }
.card.cover p.subtitle { color: #b41e1e; font-weight: 600; }
.card.cover p.tagline { color: #6b7280; font-size: 0.95em; }
.card.closing {
  text-align: center;
  border: 1px solid #14285a;
  border-left: 6px solid #b41e1e;
  padding: 22px 24px;
}
.card.closing p { margin-bottom: 0.4em; }
.card.closing p strong { color: #b41e1e; }
.card.ascii {
  border: 1px solid #e5e7eb;
  border-left: 3px solid #b41e1e;
  padding: 12px 16px;
  margin: 14px 0;
  font-family: 'Consolas', 'Menlo', 'Courier New', monospace;
  font-size: 0.88em;
  line-height: 1.2;
  white-space: pre;
  overflow-x: auto;
}
.nav {
  border: 1px solid #e5e7eb;
  border-left: 4px solid #b41e1e;
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 24px;
  font-size: 0.92em;
}
.nav a {
  color: #14285a;
  font-weight: 600;
  text-decoration: none;
}
.nav a:hover { text-decoration: underline; }
.meta {
  color: #6b7280;
  font-size: 0.88em;
  border-top: 1px solid #e5e7eb;
  margin-top: 32px;
  padding-top: 16px;
}

/* Numbered step tables: 1-row 2-cell with a tiny "1"/"2" badge on the left */
td.step-num {
  width: 56px;
  text-align: center;
  border-right: 3px solid #b41e1e;
  color: #b41e1e;
  font-weight: 800;
  font-size: 1.6em;
  vertical-align: middle;
}
td.step-num p { margin: 0; }
td.step-num strong { color: #b41e1e; font-size: 1.4em; }
td.step-body strong { font-size: 1.1em; color: #14285a; display: block; margin-bottom: 4px; }
td.step-body p { margin-bottom: 0.6em; }

@media (max-width: 720px) {
  body { margin: 12px auto; padding: 14px 14px; }
  h1 { font-size: 1.5em; }
  h2 { font-size: 1.25em; }
  pre.tfl-ascii-art, .card.ascii { font-size: 0.78em; }
  td.step-num { width: 44px; font-size: 1.3em; }
}
"""

BOX_CHARS = set("\u2500\u2502\u250c\u2510\u2514\u2518\u251c\u2524\u252c\u2534\u253c\u2501\u2503\u250f\u2513\u2517\u251b\u2523\u252b\u2533\u253b\u254b\u2574\u2575\u2576\u2504\u2506\u2508\u250a\u256d\u256e\u256f\u2570\u2571\u2572\u2573")

def is_single_cell_table(tbl):
    rows = tbl.find_all("tr")
    if len(rows) != 1:
        return False
    cells = rows[0].find_all(["td", "th"])
    return len(cells) == 1

def has_box_chars(s, min_n=3):
    return sum(1 for ch in s if ch in BOX_CHARS) >= min_n

def classify_card(tbl):
    text = tbl.get_text(" ", strip=True)
    first_p = tbl.find("p")
    strong = (first_p.find("strong") if first_p else None)
    first_strong_text = strong.get_text(" ", strip=True) if strong else ""
    if text.startswith("THE COMPLETE") and "MODERN TENNIS" in text:
        return "cover"
    if text.startswith("CLOSING THOUGHTS"):
        return "closing"
    if re.match(r"^CHAPTER\s+\d+", first_strong_text, re.I) or re.match(r"^CHAPTER\s+\d+", text, re.I):
        return "chapter"
    if has_box_chars(text):
        return "ascii"
    return "note"

def build_card_html(tbl, css_class):
    td = tbl.find("td")
    inner_parts = []
    for child in list(td.children):
        if isinstance(child, NavigableString):
            s = str(child).strip()
            if not s:
                continue
            inner_parts.append("<p>" + ihtml.escape(s) + "</p>")
        else:
            inner_parts.append(str(child))
    inner = "".join(inner_parts)
    if css_class == "cover":
        return '<div class="card cover">' + inner + '</div>'
    if css_class == "chapter":
        return '<div class="card chapter">' + inner + '</div>'
    if css_class == "closing":
        return '<div class="card closing">' + inner + '</div>'
    if css_class == "ascii":
        raw_text = td.get_text("\n", strip=True)
        return '<pre class="card ascii">' + ihtml.escape(raw_text) + '</pre>'
    return '<div class="card">' + inner + '</div>'

def transform_single_cell_tables(soup):
    counts = {"cover": 0, "chapter": 0, "closing": 0, "ascii": 0, "note": 0}
    for tbl in list(soup.find_all("table")):
        if not is_single_cell_table(tbl):
            continue
        cls = classify_card(tbl)
        new_html = build_card_html(tbl, cls)
        new_tag = BeautifulSoup(new_html, "html5lib").find()
        tbl.replace_with(new_tag)
        counts[cls] += 1
    return counts

def is_step_table(tbl):
    """1-row 2-cell table where first cell is a single short number/letter."""
    rows = tbl.find_all("tr")
    if len(rows) != 1:
        return False
    cells = rows[0].find_all(["td", "th"])
    if len(cells) != 2:
        return False
    first_text = cells[0].get_text(" ", strip=True)
    # Match "1", "2", ..., "A", "B", "R1", "R5" (very short, alphanumeric, no spaces)
    return bool(re.fullmatch(r"[A-Z]?\d{1,2}", first_text))

def tag_step_tables(soup):
    n = 0
    for tbl in list(soup.find_all("table")):
        if is_step_table(tbl):
            cells = tbl.find_all("tr")[0].find_all(["td", "th"])
            cells[0]["class"] = cells[0].get("class", []) + ["step-num"]
            cells[1]["class"] = cells[1].get("class", []) + ["step-body"]
            n += 1
    return n

def main():
    print("Reading " + SRC)
    with open(SRC, "r", encoding="utf-8") as f:
        original = f.read()

    if not os.path.exists(BAK):
        with open(BAK, "w", encoding="utf-8") as f:
            f.write(original)
        print("Backup saved to " + BAK)

    soup = BeautifulSoup(original, "html5lib")

    before_h1 = len(soup.find_all("h1"))
    before_h2 = len(soup.find_all("h2"))
    before_h3 = len(soup.find_all("h3"))
    before_p = len(soup.find_all("p"))
    before_pre = len(soup.find_all("pre"))
    before_li = len(soup.find_all("li"))
    before_table = len(soup.find_all("table"))
    visible_before = soup.get_text(" ", strip=True)

    counts = transform_single_cell_tables(soup)
    step_count = tag_step_tables(soup)
    print("Card transformations: " + str(counts))
    print("Step tables tagged:  " + str(step_count))

    if soup.html:
        soup.html.unwrap()
    if soup.head:
        soup.head.decompose()
    if soup.body:
        soup.body.unwrap()

    doctype = "<!DOCTYPE html>\n"
    html_open = '<html lang="en">\n'
    head = (
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>The Complete Modern Tennis Handbook</title>\n'
        "<style>\n" + VI_CSS + "</style>\n"
        "</head>\n"
    )
    body_open = "<body>\n"

    inner = "".join(str(c) for c in soup.contents)
    body_close = "\n</body>\n"
    html_close = "</html>\n"

    final = doctype + html_open + head + body_open + inner + body_close + html_close

    with open(DST, "w", encoding="utf-8") as f:
        f.write(final)

    soup2 = BeautifulSoup(final, "html5lib")
    after_h1 = len(soup2.find_all("h1"))
    after_h2 = len(soup2.find_all("h2"))
    after_h3 = len(soup2.find_all("h3"))
    after_p = len(soup2.find_all("p"))
    after_pre = len(soup2.find_all("pre"))
    after_li = len(soup2.find_all("li"))
    after_table = len(soup2.find_all("table"))
    after_card = len(soup2.find_all("div", class_="card"))
    after_step = len(soup2.find_all("td", class_="step-num"))
    visible_after = soup2.get_text(" ", strip=True)

    def normalize(s):
        s = ihtml.unescape(s)
        s = re.sub(r"\s+", " ", s).strip()
        return s
    nb = normalize(visible_before)
    na = normalize(visible_after)
    if nb == na:
        print("OK: visible text preserved exactly (entity-aware).")
    else:
        print("WARNING: visible text changed after reformat!")
        for i, (ca, cb) in enumerate(zip(nb, na)):
            if ca != cb:
                print("First diff at char " + str(i) + ": " + repr(nb[max(0,i-30):i+30]) + " vs " + repr(na[max(0,i-30):i+30]))
                break
        if len(na) != len(nb):
            print("Length delta: " + str(len(na) - len(nb)))

    print("---STATS---")
    print("  h1: " + str(before_h1) + " -> " + str(after_h1))
    print("  h2: " + str(before_h2) + " -> " + str(after_h2))
    print("  h3: " + str(before_h3) + " -> " + str(after_h3))
    print("  p:  " + str(before_p) + " -> " + str(after_p))
    print("  pre: " + str(before_pre) + " -> " + str(after_pre))
    print("  li:  " + str(before_li) + " -> " + str(after_li))
    print("  table: " + str(before_table) + " -> " + str(after_table) + "  (cards lifted: " + str(sum(counts.values())) + ")")
    print("  card div: " + str(after_card))
    print("  step-num td: " + str(after_step))
    print("  file size: " + str(len(original)) + " -> " + str(len(final)) + " bytes")

if __name__ == "__main__":
    main()
