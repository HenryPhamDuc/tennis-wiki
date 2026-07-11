#!/usr/bin/env python3
"""
Convert 'Hệ  thong' (Hệ thống) folder → tennis-wiki docs/he-thong/

Source: C:/Users/Henry/Documents/MY VAULT/Documents/Obsidian Vault/tennis-vault/Hệ  thong
Target: C:/Users/Henry/Documents/tennis-wiki/docs/he-thong/

5 sub-folders × ~10-40 files = 104 MD files total.
"""
import os
import re
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import yaml

SRC = Path(r"C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\Hệ  thong")
DOCS = Path(r"C:\Users\Henry\Documents\tennis-wiki\docs\he-thong")
DOCS.mkdir(parents=True, exist_ok=True)


def slugify(text):
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-').lower()


def parse_existing_yaml(text):
    """Parse existing simple YAML frontmatter (no --- close in some files)."""
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---', 4)
    if end < 0:
        # Maybe single --- at start only, no closing — try to find end-of-block heuristic
        lines = text.split('\n')
        end = 0
        for i, ln in enumerate(lines[1:], 1):
            if ln.strip() and not ln.startswith(('  ', '\t', '-', '[')) and ':' not in ln:
                end = i
                break
        if end == 0:
            end = len(lines)
        fm_text = '\n'.join(lines[1:end])
        body = '\n'.join(lines[end:])
        try:
            fm = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            return None, text
        return fm, body
    fm_text = text[4:end]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None, text
    body = text[end + 4:].lstrip('\n')
    return fm, body


def build_yaml(title, fm, slug, source_path, sub):
    """Build standard English-keyed YAML frontmatter."""
    lines = ['---']
    lines.append(f'title: "{title}"')
    lines.append('language: vi')
    lines.append('vault: Hệ thống Tennis')
    lines.append(f'created: {datetime.now().strftime("%Y-%m-%d")}')

    # Preserve original tags
    if fm.get('tags'):
        if isinstance(fm['tags'], list):
            tag_str = ', '.join(json.dumps(str(t), ensure_ascii=False) for t in fm['tags'])
        else:
            tag_str = json.dumps(str(fm['tags']), ensure_ascii=False)
        lines.append(f'tags: [{tag_str}]')

    lines.append(f'sub_system: "{sub}"')
    lines.append(f'vault_path: "{source_path}"')
    lines.append('---')
    return '\n'.join(lines)


def main():
    files = sorted(SRC.rglob("*.md"))
    print(f"Source files: {len(files)}")

    # Compute hashes of existing tennis-wiki docs (for dedup)
    print("Loading existing docs for dedup...")
    existing_hashes = set()
    existing_slugs = set()
    for f in DOCS.parent.rglob("*.md"):
        if f.name == 'index.md':
            continue
        try:
            text = f.read_text(encoding='utf-8', errors='replace')
            norm = re.sub(r'\s+', ' ', text).strip()
            h = hashlib.md5(norm.encode('utf-8', errors='ignore')).hexdigest()
            existing_hashes.add(h)
            existing_slugs.add(f.stem.lower())
        except Exception:
            pass
    print(f"  Existing: {len(existing_hashes)} articles")

    # Build page index for wiki-link resolution (search ALL existing docs)
    page_index = {}
    # 1. Add all existing docs FIRST (so they take priority)
    for f in DOCS.parent.rglob("*.md"):
        if f.name == 'index.md':
            continue
        s = slugify(f.stem)
        cat = f.parent.name
        page_index[s] = {'source': f, 'cat': cat}
    # 2. Add current source files (will overwrite if same slug — same file)
    for f in files:
        slug = slugify(f.stem)
        # If we already have this slug from existing docs, don't overwrite
        # (existing docs in other categories take priority for cross-category linking)
        if slug not in page_index:
            page_index[slug] = {'source': f, 'cat': 'he-thong'}
    print(f"  Page index: {len(page_index)}")

    print("\nProcessing files...")
    written = []
    skipped = []
    for f in files:
        slug = slugify(f.stem)

        # Slug dedup
        if slug in existing_slugs:
            skipped.append({'file': str(f), 'reason': f'slug exists: {slug}'})
            continue

        # Read content
        try:
            text = f.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"  err reading {f.name}: {e}")
            continue

        # Content hash dedup
        norm = re.sub(r'\s+', ' ', text).strip()
        h = hashlib.md5(norm.encode('utf-8', errors='ignore')).hexdigest()
        if h in existing_hashes:
            skipped.append({'file': str(f), 'reason': 'content hash exists'})
            continue

        # Parse existing YAML
        fm, body = parse_existing_yaml(text)
        if not fm:
            fm = {}

        # Extract title from H1
        title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Remove the H1 from body (we'll let H1 stay — it's the title)
        else:
            title = f.stem.replace('_', ' ').title()

        # Determine sub-system from parent dir
        rel = f.relative_to(SRC)
        sub = rel.parts[0] if len(rel.parts) > 1 else 'root'

        # Rewrite wiki-links [[Page Name]] → MkDocs link
        def repl(m):
            inner = m.group(1)
            if '|' in inner:
                target, alias = inner.split('|', 1)
            else:
                target, alias = inner, None
            target_name = os.path.basename(target).replace('.md', '')
            target_slug = slugify(target_name)
            if target_slug in page_index:
                target_cat = page_index[target_slug].get('cat', 'he-thong')
                if target_cat == 'he-thong':
                    link = f"{target_slug}.md"
                else:
                    link = f"../{target_cat}/{target_slug}.md"
                display = alias if alias else target_name
                return f'[{display}]({link})'
            return f'_{target_name}_'
        body = re.sub(r'\[\[([^\]]+)\]\]', repl, body)

        # Build new YAML
        new_fm = build_yaml(title, fm, slug, str(f.relative_to(SRC.parent)), sub)
        full_doc = new_fm + '\n\n' + body

        # Save
        out = DOCS / f'{slug}.md'
        out.write_text(full_doc, encoding='utf-8')
        existing_hashes.add(h)
        existing_slugs.add(slug)
        written.append({'src': str(f), 'out': str(out), 'sub': sub, 'slug': slug})

    # Stats
    sub_count = defaultdict(int)
    for w in written:
        sub_count[w['sub']] += 1
    print(f"\n=== Results ===")
    print(f"  Written: {len(written)}")
    print(f"  Skipped: {len(skipped)}")
    for s, n in sorted(sub_count.items(), key=lambda x: -x[1]):
        print(f"    {n:3d}  {s}")

    if skipped:
        from collections import Counter
        reasons = Counter(s['reason'] for s in skipped)
        print(f"\n  Skip reasons:")
        for r, n in reasons.most_common():
            print(f"    {n:3d}: {r}")

    # Save manifest
    with open(r"C:\Users\Henry\Documents\tennis-wiki\scripts\hethong_manifest.json", 'w', encoding='utf-8') as f:
        json.dump({'written': written, 'skipped': skipped}, f, ensure_ascii=False, indent=2)
    print(f"\nManifest saved")


if __name__ == "__main__":
    main()
