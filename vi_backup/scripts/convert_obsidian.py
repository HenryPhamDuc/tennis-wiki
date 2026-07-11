#!/usr/bin/env python3
"""
Tennis WIKI - Obsidian to MkDocs Markdown Converter
====================================================

Converts Henry's tennis knowledge corpus (Obsidian-flavored Markdown)
into MkDocs-compatible Markdown files for static site generation.

Usage:
    python convert_obsidian.py <source_dir> <output_dir> [--source-label LABEL]

The converter:
- Strips YAML frontmatter (or converts tags → MkDocs frontmatter)
- Converts Obsidian wikilinks [[Page]] → MkDocs-style .md links
- Handles ![[image.png]] image embeds (preserves reference for manual upload)
- Auto-categorizes into output folders
- Preserves all standard markdown (headings, tables, code, etc.)
"""

import sys
import os
import re
import shutil
import argparse
import unicodedata
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ---------------------------------------------------------------------------
# Frontmatter parser (minimal)
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Strip and parse simple YAML frontmatter. Returns (meta_dict, body_text)."""
    meta = {}
    if not text.startswith('---\n'):
        return meta, text
    end = text.find('\n---\n', 4)
    if end < 0:
        return meta, text
    fm_block = text[4:end]
    body = text[end + 5:]
    current_list_key = None
    for raw_line in fm_block.split('\n'):
        if not raw_line.strip() or raw_line.lstrip().startswith('#'):
            continue
        m = re.match(r'^\s*-\s+(.+)$', raw_line)
        if m and current_list_key:
            meta.setdefault(current_list_key, []).append(
                m.group(1).strip().strip('"').strip("'")
            )
            continue
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)$', raw_line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == '' or val is None:
                current_list_key = key
                meta[key] = []
            elif val.startswith('[') and val.endswith(']'):
                inner = val[1:-1]
                items = [x.strip().strip('"').strip("'") for x in inner.split(',') if x.strip()]
                meta[key] = items
                current_list_key = None
            else:
                meta[key] = val.strip('"').strip("'")
                current_list_key = None
    return meta, body


# ---------------------------------------------------------------------------
# Slug helper — convert title to filesystem-safe name
# ---------------------------------------------------------------------------

def slugify(text):
    """Make a URL/filesystem-safe slug. Preserves Vietnamese diacritics as-is
    (MkDocs handles UTF-8 URLs natively). Removes only forbidden chars."""
    # Replace forbidden filename chars
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    # Replace spaces and underscores (MkDocs prefers -)
    text = re.sub(r'[\s_]+', '-', text.strip())
    # Remove leading/trailing dashes
    text = text.strip('-')
    # Lowercase for consistency
    return text.lower()


# ---------------------------------------------------------------------------
# MkDocs frontmatter generation
# ---------------------------------------------------------------------------

def make_mkdocs_meta(tags, title, source_path):
    """Generate YAML frontmatter for the output Markdown file."""
    lines = ['---']
    lines.append(f'title: {yaml_quote(title)}')
    if tags:
        if isinstance(tags, list):
            lines.append('tags:')
            for t in tags:
                lines.append(f'  - {yaml_quote(str(t))}')
        else:
            lines.append(f'tags: [{yaml_quote(str(tags))}]')
    if source_path:
        lines.append(f'source: {yaml_quote(source_path)}')
    lines.append(f'updated: {datetime.now().strftime("%Y-%m-%d")}')
    lines.append('---')
    return '\n'.join(lines) + '\n\n'


def yaml_quote(s):
    """Quote a YAML string if needed."""
    s = str(s)
    if not s:
        return '""'
    if re.match(r'^[a-zA-Z0-9_\-\.\sÀ-ỹ]+$', s):
        return s
    # needs quoting
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---------------------------------------------------------------------------
# Obsidian → MkDocs conversions
# ---------------------------------------------------------------------------

def rewrite_wikilinks(text, all_pages_by_slug, current_dir_relpath=''):
    """
    Convert Obsidian [[Page Name]] or [[Page Name|Alias]] to MkDocs-compatible
    markdown links with RELATIVE paths.

    current_dir_relpath: the current file's directory relative to docs root.
        e.g. 'tay-vot/alcaraz' for a file in tay-vot/alcaraz/foo.md
    """
    def repl(m):
        inner = m.group(1)
        if '|' in inner:
            target, alias = inner.split('|', 1)
        else:
            target, alias = inner, None
        page = os.path.basename(target)
        page = re.sub(r'\.(md|markdown)$', '', page, flags=re.IGNORECASE)
        page_slug = slugify(page)
        if page_slug in all_pages_by_slug:
            target_path = all_pages_by_slug[page_slug]['output_relpath']
            display = alias if alias else page
            rel = _relative_link(current_dir_relpath, target_path)
            return f'[{display}]({rel})'
        else:
            display = alias if alias else page
            return f'_{display}_'
    text = re.sub(r'\[\[([^\]]+)\]\]', repl, text)
    return text


def rewrite_image_embeds(text, image_index):
    """
    Convert Obsidian ![[image.png]] to MkDocs image syntax.
    Images are kept as references; if they exist in the image_index (relative
    path from docs root), they get proper relative path. Otherwise left as
    a placeholder note for manual upload.
    """
    def repl(m):
        inner = m.group(1)
        if '|' in inner:
            target, alt = inner.split('|', 1)
        else:
            target, alt = inner, ''
        fname = os.path.basename(target)
        if fname in image_index:
            img_path = image_index[fname]
            return f'![{alt or fname}]({img_path})'
        else:
            # Leave a TODO for manual upload
            return f'![{alt or fname}](images/{fname}){{ .missing-image }}'
    text = re.sub(r'!\[\[([^\]]+)\]\]', repl, text)
    return text


def enhance_admonitions(text):
    """Convert Obsidian > [!note] style callouts to MkDocs admonitions."""
    # Pattern: blockquote starting with > [!type] Title
    # e.g. > [!info] Important note
    #       > body line
    pattern = re.compile(
        r'^>\s*\[!(\w+)\][+-]?\s*(.*?)\n((?:^>.*\n?)*)',
        re.MULTILINE,
    )
    def repl(m):
        atype = m.group(1).lower()
        title = m.group(2).strip()
        body = m.group(3)
        # convert body lines from "> foo" to "foo"
        body_lines = []
        for line in body.split('\n'):
            line = re.sub(r'^>\s?', '', line)
            body_lines.append(line)
        body_text = '\n'.join(body_lines).strip()
        # MkDocs admonition syntax:
        # !!! type "Optional Title"
        #     body
        if title:
            return f'!!! {atype} "{title}"\n    {body_text}\n\n'
        else:
            return f'!!! {atype}\n    {body_text}\n\n'
    return pattern.sub(repl, text)


def md_passes_for_mkdocs(text):
    """Other small conversions MkDocs-friendly."""
    # Convert Obsidian ==highlight== (already a markdown extension but make sure)
    # (mkdocs pymdownx.mark handles this natively)
    # Strip Windows line endings if present
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text


# ---------------------------------------------------------------------------
# Categorization
# ---------------------------------------------------------------------------

CATEGORY_MAP = {
    'Tennis Wiki-Vietnamese': 'wiki',
    'VN_Tennis_Vault_v3_Final': 'tham-khao',
    'VN_Tennis_Vault_V2': 'tham-khao',
    'Obsidian_Tennis_Vault_Vietnamese': 'cam-nang',
    'Wave theory': 'co-sinh-hoc',
    'TFL Tennis 3.0 — Framework RPM': 'cam-nang',
    'Hệ thống Tennis Toàn diện': 'he-thong',
    'Kỹ Thuật Vợt Nâng Cao': 'ky-thuat',
}

TOPIC_KEYWORDS = {
    'forehand': 'ky-thuat',
    'backhand': 'ky-thuat',
    'serve': 'ky-thuat',
    'volley': 'ky-thuat',
    'footwork': 'ky-thuat',
    'splitstep': 'ky-thuat',
    'split step': 'ky-thuat',
    'biomechanic': 'co-sinh-hoc',
    'kinetic': 'co-sinh-hoc',
    'wave': 'co-sinh-hoc',
    'tensegrity': 'co-sinh-hoc',
    'mental': 'tam-ly',
    'psycholog': 'tam-ly',
    'breath': 'tam-ly',
    'tactic': 'chien-thuat',
    'strategy': 'chien-thuat',
    'fitness': 'the-luc',
    'proprioception': 'the-luc',
    'federer': 'tay-vot',
    'nadal': 'tay-vot',
    'djokovic': 'tay-vot',
    'alcaraz': 'tay-vot',
    'sinner': 'tay-vot',
    'rublev': 'tay-vot',
    'shelton': 'tay-vot',
    'sampras': 'tay-vot',
}

PLAYER_PAGES = {
    'Roger Federer': 'tay-vot/federer',
    'Rafael Nadal': 'tay-vot/nadal',
    'Novak Djokovic': 'tay-vot/djokovic',
    'Carlos Alcaraz': 'tay-vot/alcaraz',
    'Jannik Sinner': 'tay-vot/sinner',
    'Andrey Rublev': 'tay-vot/rublev',
    'Ben Shelton': 'tay-vot/shelton',
    'Pete Sampras': 'tay-vot/sampras',
}


def categorize(source_relpath, body):
    """Determine the output folder for an article based on source + content."""
    parts = Path(source_relpath).parts
    if not parts:
        return 'wiki'
    folder = parts[0]
    fname = parts[-1].lower()
    title_hint = None
    for ln in body.split('\n'):
        m = re.match(r'^#\s+(.+)$', ln)
        if m:
            title_hint = m.group(1).strip()
            break
    title_lower = (title_hint or '').lower()
    body_lower = body.lower()
    # Player detection (highest priority: must be explicit)
    for player_name in PLAYER_PAGES:
        player_lower = player_name.lower()
        last_name = player_lower.split()[-1]
        # Title contains full or last name → strong signal
        if last_name in title_lower or player_lower in title_lower:
            return PLAYER_PAGES[player_name]
        # Filename contains last name AND it's the dominant topic
        if last_name in fname:
            if re.match(rf'^{last_name}', fname) or fname.startswith('0'):
                return PLAYER_PAGES[player_name]
        # First 200 chars (after title) prominently feature the player
        first_chunk = body_lower[:500]
        if first_chunk.count(last_name) >= 1:
            # AND title is about that player (not just mentioning them)
            if last_name in title_lower.split() or player_lower in title_lower:
                return PLAYER_PAGES[player_name]
    if folder in CATEGORY_MAP:
        return CATEGORY_MAP[folder]
    # Topic-based fallback (only first 2000 chars)
    for kw, cat in TOPIC_KEYWORDS.items():
        if kw in body_lower[:2000]:
            return cat
    return 'wiki'


# ---------------------------------------------------------------------------
# Scan & convert
# ---------------------------------------------------------------------------

DEFAULT_SOURCES = [
    {
        'path': r'C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\Tennis Wiki-Vietnamese',
        'label': 'Tennis Wiki-Vietnamese',
    },
    {
        'path': r'C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\Wave theory',
        'label': 'Wave theory',
    },
    {
        'path': r'C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\TFL Tennis 3.0 — Framework RPM',
        'label': 'TFL Tennis 3.0 — Framework RPM',
    },
    {
        'path': r'C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\Hệ thống Tennis Toàn diện',
        'label': 'Hệ thống Tennis Toàn diện',
    },
    {
        'path': r'C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\Kỹ Thuật Vợt Nâng Cao',
        'label': 'Kỹ Thuật Vợt Nâng Cao',
    },
    {
        'path': r'C:\Users\Henry\Documents\MY VAULT\Documents\Obsidian Vault\tennis-vault\Obsidian_Tennis_Vault_Vietnamese',
        'label': 'Obsidian_Tennis_Vault_Vietnamese',
    },
]


def find_files(root, exts=('.md', '.markdown')):
    root_path = Path(root)
    for p in root_path.rglob('*'):
        if p.is_file() and p.suffix.lower() in exts:
            try:
                rel = p.relative_to(root_path)
            except ValueError:
                rel = Path(p.name)
            if '.obsidian' in rel.parts:
                continue
            yield p, rel


def build_page_index(sources):
    """First pass: scan all sources, build a slug → file path index for
    wikilink resolution."""
    index = {}
    for src in sources:
        src_path = Path(src['path'])
        if not src_path.exists():
            continue
        for abs_path, rel_path in find_files(src_path):
            slug = slugify(rel_path.stem)
            # First match wins; later sources can override if slug collides
            if slug not in index:
                # Peek at file to find first heading as canonical title
                try:
                    raw = abs_path.read_text(encoding='utf-8', errors='replace')
                except Exception:
                    raw = ''
                _, body = parse_frontmatter(raw)
                title_hint = None
                for ln in body.split('\n'):
                    m = re.match(r'^#\s+(.+)$', ln)
                    if m:
                        title_hint = m.group(1).strip()
                        break
                title = title_hint or rel_path.stem.replace('_', ' ').replace('-', ' ')
                cat = categorize(str(rel_path), body)
                output_relpath = f'{cat}/{slug}.md'
                index[slug] = {
                    'title': title,
                    'source_relpath': str(rel_path),
                    'abs_source_path': str(abs_path),
                    'category': cat,
                    'output_relpath': output_relpath,
                }
    return index


def convert_file(abs_path, rel_path, page_index, current_dir_relpath):
    """Convert one Obsidian MD file to MkDocs Markdown string.

    current_dir_relpath: e.g. 'tay-vot/alcaraz' (relative to docs root)
    """
    try:
        raw = abs_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        raw = abs_path.read_text(encoding='utf-8-sig', errors='replace')
    meta, body = parse_frontmatter(raw)
    title_hint = None
    for ln in body.split('\n'):
        m = re.match(r'^#\s+(.+)$', ln)
        if m:
            title_hint = m.group(1).strip()
            break
    title = title_hint or rel_path.stem.replace('_', ' ').replace('-', ' ')
    slug = slugify(rel_path.stem)
    text = body
    text = enhance_admonitions(text)
    text = rewrite_wikilinks(text, page_index, current_dir_relpath)
    text = re.sub(
        r'!\[\[([^\]]+)\]\]',
        lambda m: f'![{os.path.basename(m.group(1).split("|")[0])}](images/{os.path.basename(m.group(1).split("|")[0])}){{ .missing-image }}',
        text,
    )
    text = md_passes_for_mkdocs(text)
    fm = make_mkdocs_meta(meta.get('tags', []), title, str(rel_path))
    return f'{fm}{text}'


def _relative_link(from_dir, to_path):
    """Compute relative path from one directory to another."""
    from_parts = from_dir.split('/') if from_dir else []
    to_parts = to_path.split('/')
    # Find common prefix
    common = 0
    while common < len(from_parts) and common < len(to_parts) - 1 and \
          from_parts[common] == to_parts[common]:
        common += 1
    ups = ['..'] * (len(from_parts) - common)
    downs = to_parts[common:]
    return '/'.join(ups + downs)


def write_pages(sources, output_root):
    """Convert all source files and write to output_root/<category>/<slug>.md."""
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    # First pass: build page index for wikilink resolution
    print('Pass 1: Building page index...', file=sys.stderr)
    page_index = build_page_index(sources)
    print(f'  Indexed {len(page_index)} pages', file=sys.stderr)
    # Second pass: convert & write
    print('Pass 2: Converting files...', file=sys.stderr)
    stats = defaultdict(int)
    seen_slugs = set()
    for src in sources:
        src_path = Path(src['path'])
        if not src_path.exists():
            print(f'WARNING: source not found: {src_path}', file=sys.stderr)
            continue
        for abs_path, rel_path in find_files(src_path):
            slug = slugify(rel_path.stem)
            if slug in seen_slugs:
                # Duplicate — append source folder suffix
                folder_slug = slugify(src['label'])[:8]
                slug = f'{slug}-{folder_slug}'
            seen_slugs.add(slug)
            info = page_index.get(slugify(rel_path.stem))
            category = info['category'] if info else categorize(str(rel_path), '')
            out_dir = output_root / category
            out_dir.mkdir(parents=True, exist_ok=True)
            md_text = convert_file(abs_path, rel_path, page_index, current_dir_relpath=category)
            out_file = out_dir / f'{slug}.md'
            out_file.write_text(md_text, encoding='utf-8')
            stats[category] += 1
            stats['total'] += 1
    return stats


# ---------------------------------------------------------------------------
# Index page generator
# ---------------------------------------------------------------------------

INDEX_TEMPLATE = """# 🎾 Tennis WIKI

> **Bách khoa toàn thư mở về quần vợt hiện đại — tiếng Việt**
>
> Tổng hợp từ hệ thống nghiên cứu của [Henry Phạm](https://github.com/henryPhamDuc)

## Bắt đầu nhanh

<div class="grid cards" markdown>

-   :material-tennis:{ .lg .middle } **Kỹ thuật**

    ---

    Forehand, backhand, serve, volley, footwork — từ cơ bản đến nâng cao

    [:octicons-arrow-right-24: Xem tất cả](ky-thuat/index.md)

-   :material-bone:{ .lg .middle } **Cơ sinh học**

    ---

    Kinetic chain, tensegrity, wave theory, proprioception

    [:octicons-arrow-right-24: Khám phá](co-sinh-hoc/index.md)

-   :material-strategy:{ .lg .middle } **Chiến thuật**

    ---

    70% Rule, 3-shot patterns, serve & volley

    [:octicons-arrow-right-24: Đọc thêm](chien-thuat/index.md)

-   :material-meditation:{ .lg .middle } **Tâm lý**

    ---

    Pre-performance routine, breathing, pressure management

    [:octicons-arrow-right-24: Tìm hiểu](tam-ly/index.md)

-   :material-run-fast:{ .lg .middle } **Thể lực**

    ---

    Proprioception programs, spiral chain, age-50+ safety

    [:octicons-arrow-right-24: Bắt đầu](the-luc/index.md)

-   :material-account-group:{ .lg .middle } **Tay vợt**

    ---

    Federer, Nadal, Djokovic, Alcaraz, Sinner, Rublev, Shelton

    [:octicons-arrow-right-24: Xem](tay-vot/index.md)

-   :material-book-open-page-variant:{ .lg .middle } **Cẩm nang**

    ---

    Cẩm nang 3.5, Giáo trình 5 năm, TFL 3.0 Framework

    [:octicons-arrow-right-24: Đọc](cam-nang/index.md)

-   :material-bookshelf:{ .lg .middle } **Tham khảo**

    ---

    Wave theory, biomechanics, advanced methodology

    [:octicons-arrow-right-24: Đọc](tham-khao/index.md)

</div>

## Về dự án

Tennis WIKI là wiki tổng hợp từ hệ thống nghiên cứu cá nhân của **Henry Phạm** — huấn luyện viên quần vợt và nhà nghiên cứu cơ sinh học thể thao tại Việt Nam.

Nội dung bao gồm:

- **~350 bài viết** chuyên sâu, được biên soạn từ ghi chép cá nhân, cẩm nang và tài liệu nghiên cứu
- **Kỹ thuật, cơ sinh học, chiến thuật, tâm lý, thể lực** — đầy đủ các khía cạnh
- **Phân tích chuyên sâu** các tay vợt hàng đầu thế giới
- **Framework độc đáo**: TFL 3.0 (Rhythm-Position-Movement), Dynamic Energy Transfer, Wave Theory, Tennis Control System
- **Tích hợp triết lý Đông Á**: Thái Cực Quyền, Dantian, Mingmen, Chan Si Gong (Silk Reeling)

## Đóng góp

Wiki này là mã nguồn mở. Bạn có thể:

- :material-github:{ .lg } **[GitHub Repository](https://github.com/henryPhamDuc/tennis-wiki)** — xem mã nguồn, đề xuất chỉnh sửa
- :fontawesome-brands-youtube:{ .lg } **[Tennis for Everyone Blog](https://tennis-for-everyone.blogspot.com/)** — bài viết bằng song ngữ Anh-Việt
- :fontawesome-brands-facebook:{ .lg } **[Facebook Page](https://www.facebook.com/share/1BmokPQjf2/)** — cộng đồng

## Giấy phép

Nội dung được phát hành theo [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0).

!!! quote "Ghi công"
    Khi sử dụng lại nội dung, vui lòng ghi: *"Tennis WIKI by Henry Phạm, [https://tennis-wiki.example.com](https://github.com/henryPhamDuc/tennis-wiki)"*
"""


def write_index(output_root):
    """Write the main index.md page."""
    (Path(output_root) / 'index.md').write_text(INDEX_TEMPLATE, encoding='utf-8')


# ---------------------------------------------------------------------------
# Section index generators
# ---------------------------------------------------------------------------

SECTION_INDEXES = {
    'ky-thuat': """# 🎾 Kỹ thuật Tennis

Tất cả về forehand, backhand, serve, volley và footwork.

## Tổng quan

- **Forehand** — cú đánh thuận tay, kỹ thuật quan trọng nhất
- **Backhand** — cú đánh trái tay (một tay hoặc hai tay)
- **Serve** — giao bóng, cú duy nhất bạn hoàn toàn kiểm soát
- **Volley** — đánh ở lưới
- **Footwork** — di chuyển, split step, crossover
""",
    'co-sinh-hoc': """# 🦴 Cơ sinh học Tennis

Khoa học về chuyển động cơ thể trong tennis: kinetic chain, tensegrity, wave theory.

## Chủ đề chính

- **Lý thuyết sóng** — truyền năng lượng qua cơ thể như sóng
- **Kinetic chain** — chuỗi truyền lực từ chân → hông → tay
- **Tensegrity** — cấu trúc căng-nén trong cơ thể
- **Proprioception** — nhận thức vị trí cơ thể trong không gian
""",
    'chien-thuat': """# 🎯 Chiến thuật Tennis

Các chiến thuật và mẫu thi đấu đã được chứng minh hiệu quả.

## Khái niệm chính

- **70% Rule** — chỉ cần thắng 70% số điểm để giành chiến thắng
- **First Strike Tennis** — tấn công chủ động
- **3-Shot Pattern** — chuỗi 3 cú đánh có chủ đích
- **Serve & Volley** — giao bóng lên lưới
""",
    'tam-ly': """# 🧠 Tâm lý Tennis

Mindset, pre-performance routine, quản lý áp lực.

## Phương pháp

- **15-Second Reset** — giao thức giữa các điểm
- **Pre-Performance Routine** — chuẩn bị trước khi giao bóng
- **Thở 4-2-6** — kỹ thuật thở giảm stress
- **Quản lý áp lực** — chiến thắng trong những điểm quan trọng
""",
    'the-luc': """# 🏃 Thể lực Tennis

Sức mạnh, linh hoạt, sức bền — dành cho mọi lứa tuổi.

## Chương trình

- **Proprioception 4 tuần** — cải thiện cảm giác cơ thể
- **Spiral Chain** — xoắn ốc trong cơ thể
- **An toàn tuổi 50+** — tập luyện không chấn thương
""",
    'tay-vot': """# 👤 Tay vợt chuyên nghiệp

Phân tích kỹ thuật và chiến thuật của các tay vợt hàng đầu.

## Tay vợt được phân tích

- [Roger Federer](federer.md) — Pre-stretch cổ tay, volley đẳng cấp
- [Rafael Nadal](nadal.md) — Topspin heavy, chiến đấu bền bỉ
- [Novak Djokovic](djokovic.md) — Return vị trí, sliding
- [Carlos Alcaraz](alcaraz.md) — Dây thun dài / Whip
- [Jannik Sinner](sinner.md) — Roi da, racket flip
- [Andrey Rublev](rublev.md) — Máy ép thủy lực
- [Ben Shelton](shelton.md) — Giao bóng mạnh, forehand tốc độ
- [Pete Sampras](sampras.md) — Serve & volley thuần túy
""",
    'cam-nang': """# 📚 Cẩm nang Tennis

Các cẩm nang đầy đủ, hệ thống, từ cơ bản đến chuyên sâu.

## Cẩm nang tiêu biểu

- **Cẩm nang 3.5** — cho người chơi trung cấp
- **Giáo trình 5 năm** — lộ trình dài hạn
- **TFL Tennis 3.0** — framework RPM (Rhythm-Position-Movement)
- **Tennis Control System** — hệ thống điều khiển
""",
    'tham-khao': """# 📖 Tài liệu tham khảo

Các tài liệu nền tảng: lý thuyết sóng, biomechanics, methodology nâng cao.

## Tài liệu

- **Wave theory** — lý thuyết sóng trong tennis
- **TFL Framework** — chi tiết framework TFL 3.0
- **Biomechanics** — cơ sinh học ứng dụng
""",
}


def write_section_indexes(output_root):
    """Write per-section index.md files based on actual folder contents."""
    out = Path(output_root)
    section_meta = {
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
    for section, (emoji, title, desc) in section_meta.items():
        d = out / section
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
        # List files in this section
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
            # Read first heading or use filename
            try:
                raw = f.read_text(encoding='utf-8', errors='replace')
                title_hint = None
                # Skip frontmatter
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


# ---------------------------------------------------------------------------
# Assets (theme CSS + JS)
# ---------------------------------------------------------------------------

EXTRA_CSS = """/* Tennis WIKI - Custom theme additions on top of Material */

:root {
    --md-primary-fg-color:        #2e7d32;
    --md-primary-fg-color--light: #43a047;
    --md-primary-fg-color--dark:  #1b5e20;
    --md-accent-fg-color:         #d4e157;
}

/* Brand */
.md-header__button.md-logo {
    color: var(--md-accent-fg-color);
}

/* Bigger hero on landing */
.md-typeset .grid.cards > ul > li {
    border-radius: 8px;
    transition: transform 0.2s;
}
.md-typeset .grid.cards > ul > li:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(46, 125, 50, 0.2);
}

/* Code blocks with tennis theme */
.md-typeset code {
    background: #f1f8e9;
    color: #2e7d32;
}
.md-typeset pre > code {
    background: #1a472a;
    color: #e8f5e9;
}

/* Custom admonition colors */
.md-typeset .admonition.note,
.md-typeset details.note {
    border-color: #2e7d32;
}
.md-typeset .admonition.tip,
.md-typeset details.tip {
    border-color: #d4e157;
}

/* Missing image placeholder */
img.missing-image {
    border: 2px dashed #ff9800;
    padding: 4px;
    background: #fff3e0;
}

/* Broken link styling */
.broken-link {
    color: #c62828;
    text-decoration: line-through;
}

/* Wiki navigation: highlight current page */
.md-nav__link--active {
    color: #2e7d32 !important;
    font-weight: 600;
}
"""

EXTRA_JS = """// Tennis WIKI - Client-side enhancements
// Add copy buttons to all preformatted code blocks
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('pre code').forEach((block) => {
        const btn = document.createElement('button');
        btn.className = 'copy-button';
        btn.textContent = '📋';
        btn.title = 'Copy to clipboard';
        btn.onclick = () => {
            navigator.clipboard.writeText(block.textContent);
            btn.textContent = '✓';
            setTimeout(() => btn.textContent = '📋', 1500);
        };
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(btn);
    });
});
"""


def write_assets(output_root):
    """Write theme CSS and JS to docs/assets/."""
    assets = Path(output_root) / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    (assets / 'tennis-extra.css').write_text(EXTRA_CSS, encoding='utf-8')
    (assets / 'tennis-extra.js').write_text(EXTRA_JS, encoding='utf-8')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Tennis WIKI: Obsidian → MkDocs converter')
    parser.add_argument('--source', action='append', help='Source dir (repeatable)')
    parser.add_argument('--out', default='docs', help='Output directory (default: docs/)')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    sources = []
    if args.source:
        for s in args.source:
            sources.append({'path': s, 'label': Path(s).name})
    else:
        sources = DEFAULT_SOURCES
    if args.verbose:
        print(f'Sources: {len(sources)}', file=sys.stderr)
        for s in sources:
            print(f'  - {s["path"]}', file=sys.stderr)
    # Clear output dir if --clean
    out_root = Path(args.out)
    if out_root.exists() and (out_root / 'index.md').exists():
        if args.verbose:
            print(f'Cleaning {out_root}...', file=sys.stderr)
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    # Generate content
    stats = write_pages(sources, out_root)
    write_index(out_root)
    write_section_indexes(out_root)
    write_assets(out_root)
    # Report
    print(f'\n=== Build complete ===')
    print(f'  Total pages:     {stats["total"]}')
    for cat in sorted(stats.keys()):
        if cat != 'total':
            print(f'  {cat:20} {stats[cat]:>4}')
    print(f'\n  Output: {out_root}/')


if __name__ == '__main__':
    main()