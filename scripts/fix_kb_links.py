#!/usr/bin/env python3
"""Fix cross-section links in knowledgebase nodes.
related links should be: ../<section>/<slug>.md for cross-section,
or just <slug>.md for same-section."""
from pathlib import Path
import re

DST = Path(r"C:\Users\Henry\Documents\tennis-wiki\docs\tennisplayer")

# Build slug -> section map
slug_to_section = {}
for section_dir in DST.iterdir():
    if not section_dir.is_dir():
        continue
    for md in section_dir.glob("*.md"):
        if md.name == 'index.md':
            continue
        slug = md.stem
        slug_to_section[slug] = section_dir.name

print(f"Built map: {len(slug_to_section)} slugs across sections")

# Pattern: - [Title](slug.md)
LINK_PATTERN = re.compile(r'^- \[([^\]]+)\]\(([^/)]+)\.md\)$', re.MULTILINE)

fixed = 0
for md_file in DST.rglob("*.md"):
    if md_file.name == 'index.md':
        continue
    text = md_file.read_text(encoding='utf-8', errors='replace')
    current_section = md_file.parent.name

    def fix_link(m):
        global fixed
        title = m.group(1)
        slug = m.group(2)
        target_section = slug_to_section.get(slug)
        if not target_section:
            return m.group(0)  # Not found, leave as is
        if target_section == current_section:
            return f'- [{title}]({slug}.md)'
        else:
            return f'- [{title}](../{target_section}/{slug}.md)'

    new_text = LINK_PATTERN.sub(fix_link, text)
    if new_text != text:
        # Count changes
        fixed += len(LINK_PATTERN.findall(text))
        md_file.write_text(new_text, encoding='utf-8')

print(f"Fixed {fixed} cross-section links")
