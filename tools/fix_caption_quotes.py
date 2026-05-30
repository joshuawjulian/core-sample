#!/usr/bin/env python3
"""Make Quarto cell options (#| fig-cap: "...", etc.) safe for LaTeX.

A double-quoted YAML scalar processes backslash escapes: '\g' (\\ge) is an *invalid*
escape -> hard render failure; '\b'/'\f'/'\t' are *valid* escapes -> the caption is
silently corrupted. LaTeX in a caption needs literal backslashes, so the right
representation is a SINGLE-quoted YAML scalar (no escape processing).

This rewrites any '#| key: "<value containing a backslash>"' to single-quoted form,
un-escaping \\" -> " and doubling internal single quotes per YAML rules. Lines without a
backslash, and non-#| lines, are left untouched.

Usage:  python3 tools/fix_caption_quotes.py <file.qmd> [...]
"""
import re, sys, pathlib

OPT = re.compile(r'^(\s*#\|\s*[\w.-]+:\s*)"(.*)"\s*$')

def fix_line(line):
    m = OPT.match(line)
    if not m:
        return line, 0
    prefix, val = m.group(1), m.group(2)
    if '\\' not in val:
        return line, 0                       # nothing risky
    inner = val.replace('\\"', '"')          # a literal " had to be escaped in dquotes
    single = inner.replace("'", "''")        # YAML single-quote escaping
    return f"{prefix}'{single}'\n", 1

def fix_file(p):
    lines = p.read_text().splitlines(keepends=True)
    n = 0
    for i, ln in enumerate(lines):
        new, k = fix_line(ln)
        if k:
            lines[i] = new
            n += k
    if n:
        p.write_text("".join(lines))
    return n

if __name__ == '__main__':
    total = 0
    for a in sys.argv[1:]:
        total += fix_file(pathlib.Path(a))
    print(f"converted {total} cell-option line(s) to single-quoted")
