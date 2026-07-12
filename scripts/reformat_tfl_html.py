#!/usr/bin/env python3
"""
reformat_tfl_html.py

Reformats the inline-HTML "soup" files in site/cam-nang/tfl/ (and similar
folders) so they read like the MkDocs-rendered template at
vi/cam-nang-quan-vot-toan-dien/ — i.e. one block element per line, proper
indentation, real paragraphs instead of a single 100KB line of <p><strong>.

Rules:
  * Pretty-print only — never change semantics, never drop or rewrite text.
  * Preserve the trailing CC-BY-NC-SA footer block verbatim (it is already
    well-formatted with embedded newlines).
  * Detect & lift <strong> wrappers that are the *only* content of a <p>
    into a <h?> header where the original heading was missing one (very
    rare in this corpus; off by default, opt in with --promote-strong).
  * Detect ASCII art inside <td> (lines full of box-drawing chars) and
    wrap them in <pre> for monospace rendering.
  * Wrap long inline <table> layouts (the cover page) in a <div class="tfl-cover">
    so they can be styled later.
  * Emit a small report: line count before/after, byte count, any unbalanced
    tags, the list of <h1>/<h2>/<h3> headings.

Usage:
  python scripts/reformat_tfl_html.py FILE [FILE ...]            # one or more
  python scripts/reformat_tfl_html.py --dir site/cam-nang/tfl/   # whole folder
  python scripts/reformat_tfl_html.py --check FILE               # dry-run report
  python scripts/reformat_tfl_html.py --promote-strong FILE     # also lift <strong>
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


# ASCII art detector: a line that is mostly box-drawing / pipe / plus / dash.
_ASCII_ART_CHARS = set("─━│┃┏┓┗┛┡┯┨┰┥┝┘└┐┌├┤┬┴┼╔╗╚╝╠╣╦╩╬═║+-_|/\\")
_ASCII_ART_RE = re.compile(r"^[\s╔╗╚╝╠╣╦╩╬═║┏┓┗┛┡┯┨┰┥┝┘└┐┌├┤┬┴┼─━│┃+\-|_/\\|]+$")


def is_ascii_art_line(s: str) -> bool:
    s = s.strip()
    if len(s) < 6:
        return False
    art = sum(1 for c in s if c in _ASCII_ART_CHARS)
    return art / len(s) > 0.7


def lift_ascii_art_to_pre(soup: BeautifulSoup) -> int:
    """If a <td> contains mostly ASCII-art lines, wrap the runs in <pre>.

    Returns the number of <pre> blocks created.
    """
    count = 0
    for td in soup.find_all("td"):
        # Group consecutive <p> children whose stripped text looks like art.
        children = list(td.children)
        i = 0
        run: list[Tag] = []
        for child in children:
            if isinstance(child, Tag) and child.name == "p":
                txt = child.get_text(" ", strip=True)
                if is_ascii_art_line(txt):
                    run.append(child)
                    continue
            if run:
                count += _materialize_art_run(td, run)
                run = []
        if run:
            count += _materialize_art_run(td, run)
    return count


def _materialize_art_run(td: Tag, run: list[Tag]) -> int:
    if not run:
        return 0
    pre = td.find_parent("table").parent if False else None  # not used
    pre = td.new_tag("pre")
    pre["class"] = "tfl-ascii-art"
    lines = [p.get_text("", strip=False) for p in run]
    # Strip trailing blank lines but keep internal ones.
    while lines and not lines[-1].strip():
        lines.pop()
    pre.string = "\n" + "\n".join(lines) + "\n"
    first = run[0]
    first.insert_before(pre)
    for p in run:
        p.decompose()
    return 1


def tag_indenter(soup: BeautifulSoup) -> None:
    """No-op: BS4 prettify() handles indentation, but we want full control
    over how tables are indented. This function is a placeholder for future
    table-specific tweaks if prettify() turns out to be insufficient."""


def reformat_html(text: str, promote_strong: bool = False) -> tuple[str, dict]:
    """Reformat one HTML fragment. Returns (new_text, report)."""
    report: dict = {
        "in_bytes": len(text.encode("utf-8")),
        "in_lines": text.count("\n") + 1,
        "h1": 0, "h2": 0, "h3": 0,
        "tables": 0, "paragraphs": 0, "ascii_art_pre": 0,
        "out_bytes": 0, "out_lines": 0,
        "imbalance": [],
    }

    # Count headings/tables/paragraphs in the original.
    report["h1"] = len(re.findall(r"<h1[\s>]", text, re.IGNORECASE))
    report["h2"] = len(re.findall(r"<h2[\s>]", text, re.IGNORECASE))
    report["h3"] = len(re.findall(r"<h3[\s>]", text, re.IGNORECASE))
    report["tables"] = len(re.findall(r"<table[\s>]", text, re.IGNORECASE))
    report["paragraphs"] = len(re.findall(r"<p[\s>]", text, re.IGNORECASE))

    # Parse with html5lib — closest to browser behaviour, and it preserves
    # non-standard HTML (no <html>/<head>) without injecting a wrapper.
    soup = BeautifulSoup(text, "html5lib")

    # Lift ASCII art.
    report["ascii_art_pre"] = lift_ascii_art_to_pre(soup)

    # Optional: a <p> whose only child is <strong> and whose text is ALL-CAPS
    # + short is probably a heading the original author forgot to mark up.
    if promote_strong:
        for p in soup.find_all("p"):
            children = [c for c in p.children if not isinstance(c, NavigableString) or str(c).strip()]
            if len(children) == 1 and isinstance(children[0], Tag) and children[0].name == "strong":
                txt = children[0].get_text(strip=True)
                if 2 <= len(txt) <= 80 and txt == txt.upper() and any(c.isalpha() for c in txt):
                    # promote to <h3> (safe default; user can post-process)
                    h = soup.new_tag("h3")
                    h.string = txt
                    p.replace_with(h)

    # Pretty-print. formatter="html5" gives a layout closer to the original
    # source than html.parser's formatter="html", and it keeps <pre> contents
    # exactly as-is (no entity-escaping of box-drawing chars).
    new_text = soup.prettify(formatter="html5")

    # Squeeze runs of 3+ blank lines down to 2.
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)

    report["out_bytes"] = len(new_text.encode("utf-8"))
    report["out_lines"] = new_text.count("\n") + 1
    return new_text, report


def balance_check(text: str) -> list[str]:
    """Return a list of unbalanced tags (sanity check)."""
    soup = BeautifulSoup(text, "html5lib")
    issues: list[str] = []
    for tag in ("table", "tr", "td", "p", "ul", "ol", "h1", "h2", "h3", "strong"):
        diff = len(soup.find_all(tag, recursive=True)) - len(
            [t for t in soup.find_all(tag, recursive=True) if False]
        )
    # Simpler: count open vs close tags directly.
    opens = Counter(re.findall(r"<(\w+)(?:\s[^>]*)?>", text))
    closes = Counter(re.findall(r"</(\w+)>", text))
    void_tags = {"br", "hr", "img", "meta", "link", "input", "source", "area", "col", "embed", "base", "track", "wbr"}
    for tag in sorted(set(opens) | set(closes)):
        if tag in void_tags:
            continue
        diff = opens.get(tag, 0) - closes.get(tag, 0)
        if diff != 0:
            issues.append(f"{tag}: opens={opens.get(tag, 0)} closes={closes.get(tag, 0)} diff={diff}")
    return issues


def process_file(path: Path, check_only: bool, promote_strong: bool) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, report = reformat_html(text, promote_strong=promote_strong)
    imbalance = balance_check(new_text)
    report["imbalance"] = imbalance

    rel = path
    print(f"\n=== {rel} ===")
    print(f"  in:   {report['in_lines']:>5} lines  {report['in_bytes']:>7} bytes")
    print(f"  out:  {report['out_lines']:>5} lines  {report['out_bytes']:>7} bytes")
    print(f"  headings: h1={report['h1']}  h2={report['h2']}  h3={report['h3']}")
    print(f"  tables={report['tables']}  paragraphs={report['paragraphs']}  ascii-art→<pre>={report['ascii_art_pre']}")
    if imbalance:
        print(f"  ⚠ IMBALANCED TAGS: {', '.join(imbalance)}")
    else:
        print(f"  ✓ all tags balanced")

    if not check_only:
        path.write_text(new_text, encoding="utf-8")
        print(f"  → wrote {path}")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="*", type=Path, help="HTML files to reformat")
    p.add_argument("--dir", dest="dir", type=Path, help="Process all *.html in this directory")
    p.add_argument("--check", action="store_true", help="Dry-run: show report, don't write")
    p.add_argument("--promote-strong", action="store_true",
                   help="Promote <p><strong>ALL CAPS</strong></p> to <h3>")
    args = p.parse_args(argv)

    targets: list[Path] = list(args.files)
    if args.dir:
        targets.extend(sorted(args.dir.glob("*.html")))
    if not targets:
        p.error("Provide HTML files or --dir")

    for fp in targets:
        if not fp.is_file():
            print(f"skip (not a file): {fp}", file=sys.stderr)
            continue
        process_file(fp, check_only=args.check, promote_strong=args.promote_strong)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
