"""Insert two new top-level tabs into the hand-rolled mkdocs-material nav."""
import os
import re
import sys
import time

SITE_ROOT = 'site'
ANCHOR = '<a href="https://henryphamduc.github.io/tennis-wiki/en/" class="md-tabs__link">'
EN_LI_PATTERN = re.compile(
    r'(\s*<li class="md-tabs__item">\s*<a href="https://henryphamduc\.github\.io/tennis-wiki/en/" class="md-tabs__link">)',
    re.MULTILINE
)
NEW_TAB_1_TARGET = 'vi/cam-nang-quan-vot-toan-dien/'
NEW_TAB_2_TARGET = 'en/manual/absolute-tennis/'
NEW_TAB_1_LABEL = '🇻🇳 Cẩm nang QVTD'
NEW_TAB_2_LABEL = '📘 Absolute Tennis'

def relpath_to_site_root(html_path):
    rel = os.path.relpath(html_path, SITE_ROOT)
    depth = rel.count(os.sep)
    return '' if depth == 0 else '../' * depth

def make_new_tab_li(label, target_rel_from_site_root, file_depth_prefix):
    href = file_depth_prefix + target_rel_from_site_root
    return (
        f'\n        \n  \n  \n  \n  \n    <li class="md-tabs__item">\n'
        f'      <a href="{href}" class="md-tabs__link">\n'
        f'        \n  \n  \n    \n  \n  {label}\n\n'
        f'      </a>\n    </li>\n  \n'
    )

t0 = time.time()
html_files = []
for root, dirs, files in os.walk(SITE_ROOT):
    if 'assets' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))
print(f"Found {len(html_files)} HTML files in {time.time()-t0:.1f}s", flush=True)

modified, skipped, errors = 0, 0, 0
t1 = time.time()
for i, path in enumerate(html_files):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        if 'md-tabs__link' not in content or ANCHOR not in content:
            skipped += 1
            continue
        if 'Cẩm nang QVTD' in content:
            skipped += 1
            continue
        prefix = relpath_to_site_root(path)
        new_tab_1 = make_new_tab_li(NEW_TAB_1_LABEL, NEW_TAB_1_TARGET, prefix)
        new_tab_2 = make_new_tab_li(NEW_TAB_2_LABEL, NEW_TAB_2_TARGET, prefix)
        new_content, n_subs = EN_LI_PATTERN.subn(
            new_tab_1 + new_tab_2 + r'\1',
            content
        )
        if n_subs == 0:
            skipped += 1
            continue
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        modified += 1
        if modified % 200 == 0:
            print(f"  {modified} modified, {skipped} skipped, {i+1}/{len(html_files)} done in {time.time()-t1:.1f}s", flush=True)
    except Exception as e:
        errors += 1
        print(f"ERR {path}: {e}", file=sys.stderr)

print(f"Done. Modified {modified}, skipped {skipped}, errors {errors} in {time.time()-t1:.1f}s", flush=True)
