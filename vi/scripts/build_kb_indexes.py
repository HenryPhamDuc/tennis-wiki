#!/usr/bin/env python3
"""Generate tennisplayer/index.md (hub) and per-section index pages."""
from pathlib import Path
import re
from collections import defaultdict, OrderedDict

DST = Path(r"C:\Users\Henry\Documents\tennis-wiki\docs\tennisplayer")
import sys
sys.path.insert(0, str(Path(r"C:\Users\Henry\Documents\tennis-wiki\scripts")))
from build_knowledgebase import CONCEPTS


# Group by sub-library
by_sub = OrderedDict()
sub_titles = {
    "ultimate-fundamentals": "Ultimate Fundamentals",
    "ultimate-drill-games": "Ultimate Drill Games",
    "teaching-systems": "Teaching Systems",
    "famous-coaches": "Famous Coaches",
    "classic-lessons": "Classic Lessons",
    "footwork": "Footwork",
    "strategy-and-statistics": "Strategy and Statistics",
    "mental-game": "Mental Game",
    "advanced-tennis": "Advanced Tennis",
    "science-of-biomechanics": "Science of Biomechanics",
    "mysteries-of-the-heavy-ball": "Mysteries of the Heavy Ball",
    "tour-strokes": "Tour Strokes",
    "tennis-science": "Tennis Science",
    "high-performance": "High Performance",
}
for c in CONCEPTS:
    by_sub.setdefault(c['sub_library'], []).append(c)


# ============================================================
# HUB INDEX
# ============================================================

hub = ['---']
hub.append('title: "Tennis Knowledgebase Hub"')
hub.append('subtitle: "Concept nodes from the tennisplayer.net teaching library"')
hub.append('language: en')
hub.append('vault: tennis-knowledgebase')
hub.append('created: 2026-06-22')
hub.append('updated: 2026-06-22')
hub.append('source_inspiration: "tennisplayer.net (John Yandell, 2002-2022)"')
hub.append('content_type: "Original synthesis - no verbatim content"')
hub.append('---')
hub.append('')
hub.append('# Tennis Knowledgebase Hub')
hub.append('')
hub.append('> **A network of tennis concept nodes** inspired by the legendary tennisplayer.net teaching library. Each node is a single tennis concept with an original summary, cross-linked to related concepts. **No verbatim text is used**—all content is original synthesis.')
hub.append('')
hub.append('## What is a Knowledgebase Hub?')
hub.append('')
hub.append('Unlike a traditional article-based wiki, this knowledgebase organizes tennis knowledge as a **graph of concept nodes**. Each node represents one concept (e.g., "Split Step", "Kinetic Chain", "Percentage Tennis"), with:')
hub.append('')
hub.append('- A short **original summary** (200-400 words)')
hub.append('- **Cross-links** to 3-7 related concept nodes')
hub.append('- **Source inspiration** (the original tennisplayer.net article that inspired the node)')
hub.append('')
hub.append('This structure helps you:')
hub.append('')
hub.append('- **Explore** a concept and its relationships')
hub.append('- **Compare** related concepts side by side')
hub.append('- **Learn** through contextual cross-references')
hub.append('- **Avoid copyright issues** by reading original synthesis, not source articles')
hub.append('')

# Group by category (top-level)
categories = OrderedDict([
    ("Fundamentals", ["ultimate-fundamentals", "ultimate-drill-games", "teaching-systems", "famous-coaches", "classic-lessons"]),
    ("Footwork & Strategy", ["footwork", "strategy-and-statistics"]),
    ("Mental Game & Performance", ["mental-game", "high-performance"]),
    ("Stroke Mastery", ["advanced-tennis"]),
    ("Biomechanics & Science", ["science-of-biomechanics", "mysteries-of-the-heavy-ball", "tour-strokes", "tennis-science"]),
])

hub.append(f'## Knowledgebase Structure ({len(CONCEPTS)} nodes across {len(by_sub)} sub-libraries)')
hub.append('')

for cat, subs in categories.items():
    valid_subs = [s for s in subs if s in by_sub]
    if not valid_subs:
        continue
    cat_total = sum(len(by_sub[s]) for s in valid_subs)
    hub.append(f'### {cat} ({cat_total} nodes)')
    hub.append('')
    for s in valid_subs:
        sub_title = sub_titles.get(s, s)
        hub.append(f'- **[{sub_title}]({s}/index.md)** — {len(by_sub[s])} concept nodes')
    hub.append('')

hub.append('## How to Use This Knowledgebase')
hub.append('')
hub.append('1. **Start with the Fundamentals** — concepts like "Kinetic Chain" and "Split Step" are foundational to everything else')
hub.append('2. **Follow cross-links** — each node links to 3-7 related concepts to build a deeper understanding')
hub.append('3. **Browse by category** — the structure above groups concepts by domain (biomechanics, tactics, mental game)')
hub.append('4. **Use for reference** — when you encounter a tennis term, search for it here')
hub.append('')

hub.append('## Source & Attribution')
hub.append('')
hub.append('**Source inspiration:** The concept organization and topic selection draws from the tennisplayer.net teaching library (2002-2022, founded by John Yandell). All content in this knowledgebase is **original synthesis**, not verbatim reproduction.')
hub.append('')
hub.append('For the original tennisplayer.net content, visit [tennisplayer.net](https://www.tennisplayer.net/).')
hub.append('')

hub_path = DST / 'index.md'
hub_path.write_text('\n'.join(hub), encoding='utf-8')
print(f"Wrote {hub_path}")


# ============================================================
# PER-SECTION INDEX PAGES
# ============================================================

for sub, nodes in by_sub.items():
    sub_title = sub_titles.get(sub, sub)
    sec = ['---']
    sec.append(f'title: "{sub_title} - Knowledgebase"')
    sec.append(f'sub_library: "{sub}"')
    sec.append('language: en')
    sec.append('vault: tennis-knowledgebase')
    sec.append('created: 2026-06-22')
    sec.append('updated: 2026-06-22')
    sec.append('---')
    sec.append('')
    sec.append(f'# {sub_title}')
    sec.append('')
    sec.append(f'**Concept nodes:** {len(nodes)}')
    sec.append(f'**Parent hub:** [Tennis Knowledgebase Hub](../index.md)')
    sec.append('')
    sec.append('## Concepts in this Sub-Library')
    sec.append('')
    for c in nodes:
        sec.append(f'### [{c["title"]}]({c["slug"]}.md)')
        sec.append('')
        sec.append(c['summary'][:200] + ('...' if len(c['summary']) > 200 else ''))
        sec.append('')
    sec.append('---')
    sec.append('')
    sec.append('**Source inspiration:** tennisplayer.net teaching library — *all content is original synthesis*')
    sec.append('')

    out = DST / sub / 'index.md'
    out.write_text('\n'.join(sec), encoding='utf-8')
    print(f"Wrote {out}")
