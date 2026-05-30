#!/usr/bin/env python3
r"""Convert double-quoted Quarto cell options (#| fig-cap: "...") to SINGLE-quoted YAML,
which is the safe home for literal LaTeX (single quotes do no escape processing).

The tricky part is recovering the author's intended literal from the double-quoted source:
  - "\\{"  (escaped backslash) means a literal  \{   -> collapse \\ to \
  - "\""   (escaped quote)      means a literal   "
  - "\ge"  (a lone backslash, an *invalid* double-quote escape that the author meant
            literally) stays  \ge
So: protect "\\" -> sentinel, turn "\"" -> ", restore sentinel -> "\", then single-quote
(doubling any internal single quote). Lines without a backslash, and already single-quoted
or non-#| lines, are left untouched.

Usage:  python3 tools/fix_caption_quotes.py <file.qmd> [...]
"""
import re, sys, pathlib

OPT_DQ = re.compile(r'^(\s*#\|\s*[\w.-]+:\s*)"(.*)"\s*$')

def fix_line(line):
    # Convert double-quoted cell options to single-quoted, recovering the intended literal
    # (\\ -> \, \" -> "). Single-quoted options are left ALONE — their backslashes are
    # already literal (e.g. \\ is a real LaTeX line break and must NOT be collapsed).
    m = OPT_DQ.match(line)
    if not m:
        return line, 0
    prefix, val = m.group(1), m.group(2)
    if '\\' not in val:
        return line, 0
    literal = val.replace('\\\\', '\x00')   # protect escaped backslashes
    literal = literal.replace('\\"', '"')    # escaped double-quote -> literal "
    literal = literal.replace('\x00', '\\')  # escaped backslash -> a single backslash
    return f"{prefix}'{literal.replace(chr(39), chr(39)*2)}'\n", 1

def fix_file(p):
    lines = p.read_text().splitlines(keepends=True)
    n = 0
    for i, ln in enumerate(lines):
        new, k = fix_line(ln)
        if k:
            lines[i] = new; n += k
    if n:
        p.write_text("".join(lines))
    return n

if __name__ == '__main__':
    total = sum(fix_file(pathlib.Path(a)) for a in sys.argv[1:])
    print(f"converted {total} cell-option line(s) to single-quoted")
