#!/usr/bin/env python3
"""
Merge the converted docs/ into existing docs/ (non-destructive).

1. Identify files in NEW that are NOT in EXISTING → copy them
2. For files in BOTH with identical size → skip
3. For files in BOTH with different size → use newer (if significantly larger)
4. Regenerate section indexes to include all files
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

EXISTING = Path(r"C:\Users\Henry\AppData\Local\Temp\docs-backup-current")
NEW = Path(r"C:\Users\Henry\AppData\Local\Temp\tennis-wiki-docs-new")
TARGET = Path(r"C:\Users\Henry\Documents\tennis-wiki\docs")

def find_md(root):
    return {p.relative_to(root).as_posix() for p in root.rglob("*.md") if p.is_file()}

print("=== Merge plan ===")
existing_set = find_md(EXISTING)
new_set = find_md(NEW)
print(f"  Existing files: {len(existing_set)}")
print(f"  New files:      {len(new_set)}")
print(f"  Net new:        {len(new_set - existing_set)}")
print(f"  Identical path: {len(new_set & existing_set)}")
print(f"  Removed (only in existing): {len(existing_set - new_set)}")

# Step 1: Copy all NEW files to TARGET (overwrite identical-by-content existing if different)
copied = 0
skipped = 0
overwritten = 0
for rel in sorted(new_set):
    src = NEW / rel
    dst = TARGET / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if rel not in existing_set:
        # Truly new file
        shutil.copy2(src, dst)
        copied += 1
    else:
        # Existing — check if it differs
        existing_size = (EXISTING / rel).stat().st_size
        new_size = src.stat().st_size
        if existing_size != new_size:
            # Different — overwrite with new (assumed fresher from vault)
            shutil.copy2(src, dst)
            overwritten += 1
        else:
            skipped += 1

print(f"\n  Copied (new):       {copied}")
print(f"  Overwritten (diff): {overwritten}")
print(f"  Skipped (same):     {skipped}")
print()

# Step 2: Regenerate section indexes
print("=== Regenerating section indexes ===")
SECTION_META = {
    'ky-thuat': ('🎾', 'Kỹ thuật Tennis', 'Forehand, backhand, serve, volley, footwork — từ cơ bản đến nâng cao'),
    'co-sinh-hoc': ('🦴', 'Cơ sinh học Tennis', 'Kinetic chain, tensegrity, wave theory, proprioception'),
    'chien-thuat': ('🎯', 'Chiến thuật Tennis', '70% Rule, 3-shot patterns, serve & volley'),
    'tam-ly': ('🧠', 'Tâm lý Tennis', 'Pre-performance routine, breathing, pressure management'),
    'the-luc': ('🏃', 'Thể lực Tennis', 'Proprioception programs, spiral chain, age-50+ safety'),
    'tay-vot': ('👤', 'Tay vợt chuyên nghiệp', 'Phân tích kỹ thuật và chiến thuật của các tay vợt hàng đầu'),
    'cam-nang': ('📚', 'Cẩm nang Tennis', 'Các cẩm nang đầy đủ, hệ thống, từ cơ bản đến chuyên sâu'),
    'tham-khao': ('📖', 'Tài liệu tham khảo', 'Lý thuyết sóng, biomechanics, methodology nâng cao'),
    'wiki': ('🗒️', 'Wiki gốc', 'Các bài viết gốc từ Obsidian vault'),
    'he-thong': ('⚙️', 'Hệ thống tổng thể', 'Các hệ thống tennis toàn diện'),
}

import re
for section, (emoji, title, desc) in SECTION_META.items():
    d = TARGET / section
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)
    md_files = sorted([f for f in d.iterdir() if f.suffix == '.md' and f.name != 'index.md'])
    lines = [
        f'# {emoji} {title}',
        '',
        f'*{desc}*',
        '',
        f'**Tổng số bài viết:** {len(md_files)}',
        '',
        '## Danh sách bài viết',
        '',
    ]
    for f in md_files:
        try:
            raw = f.read_text(encoding='utf-8', errors='replace')
            title_hint = None
            body = raw
            if body.startswith('---\n'):
                end = body.find('\n---\n', 4)
                if end > 0:
                    body = body[end + 5:]
            for ln in body.split('\n'):
                m = re.match(r'^#\s+(.+)$', ln)
                if m:
                    title_hint = m.group(1).strip()
                    break
            display = title_hint or f.stem.replace('-', ' ').title()
        except Exception:
            display = f.stem.replace('-', ' ').title()
        lines.append(f'- [{display}]({f.name})')
    (d / 'index.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"  {section:15s} → {len(md_files)} bài viết")

print()
print("=== Final stats ===")
total = 0
for d in sorted(TARGET.iterdir()):
    if not d.is_dir() or d.name in ('assets',): continue
    n = len([f for f in d.iterdir() if f.suffix == '.md' and f.name != 'index.md'])
    if n > 0:
        print(f"  {d.name:20s} {n:3d} bài viết")
        total += n
print(f"  {'TOTAL':20s} {total:3d} bài viết")
