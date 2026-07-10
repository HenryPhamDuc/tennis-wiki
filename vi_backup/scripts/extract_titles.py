#!/usr/bin/env python3
"""Extract just titles from tennisplayer.net .docx files (no body content)."""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path(r"H:\Play Tennis\tennisplayer.net")

SECTIONS = [
    ("Fundamentals/Ultimate Fundamentals", "ultimate-fundamentals"),
    ("Fundamentals/Ultimate Drill Games", "ultimate-drill-games"),
    ("Fundamentals/Teaching Systems", "teaching-systems"),
    ("Fundamentals/Famous Coaches", "famous-coaches"),
    ("Fundamentals/Classic Lessons", "classic-lessons"),
    ("Fundamentals/Footwork", "footwork"),
    ("Fundamentals/Strategy", "strategy-and-statistics"),
    ("Fundamentals/Mental game", "mental-game"),
    ("Fundamentals/Physical Training", "physical-training"),
    ("Fundamentals/High Performance", "high-performance"),
    ("Stroke Analysis/Advanced Tennis", "advanced-tennis"),
    ("Stroke Analysis/Biomechanics", "science-of-biomechanics"),
    ("Stroke Analysis/The Heavy Ball", "mysteries-of-the-heavy-ball"),
    ("Stroke Analysis/Tour strokes", "tour-strokes"),
    ("More/Tennis Science", "tennis-science"),
]


def read_docx_title(path):
    try:
        z = zipfile.ZipFile(path)
        doc_xml = z.read('word/document.xml').decode('utf-8')
    except:
        return None
    root = ET.fromstring(doc_xml)
    NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    for para in root.iter(NS + 'p'):
        text_parts = []
        for child in para.iter():
            tag = child.tag.split('}')[-1]
            if tag == 't':
                text_parts.append(child.text or '')
        text = ''.join(text_parts).strip()
        if text and len(text) > 5 and len(text) < 200:
            return text
    return None


all_titles = []
for src_rel, slug in SECTIONS:
    src_folder = SRC / src_rel
    if not src_folder.exists():
        continue
    docx_files = sorted([f for f in src_folder.iterdir()
                        if f.suffix == '.docx' and not f.name.startswith('~$')])
    print(f"\n=== {src_rel} ({len(docx_files)} files) ===")
    for docx in docx_files:
        title = read_docx_title(docx)
        if title:
            print(f"  {title[:100]}")
            all_titles.append((slug, docx.stem, title))
        else:
            print(f"  (no title): {docx.stem}")
            all_titles.append((slug, docx.stem, docx.stem))

print(f"\n=== Total: {len(all_titles)} titles ===")

# Save to file for next step
import json
out = Path(r"C:\Users\Henry\Documents\tennis-wiki\scripts\tp_titles.json")
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(all_titles, f, ensure_ascii=False, indent=2)
print(f"Saved to {out}")
