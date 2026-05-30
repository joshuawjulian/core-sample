#!/usr/bin/env python3
"""Zero-fill numeric article IDs to 2 digits so PROB-2 sorts before PROB-14.

Idempotent: (PREFIX)-(N) -> (PREFIX)-(NN) for the numeric-prefix tracks. Already-2-digit
IDs and split sub-letters (PROB-9a -> PROB-09a) are handled. INFR uses movement-letter IDs
(A1..E4) which already sort fine, so it is left alone.

Usage:  python3 tools/zfill_ids.py <file> [...]   (rewrites file CONTENT in place)
File renames are done separately by the caller.
"""
import re, sys, pathlib

PAT = re.compile(r'(REGR|PROB|GEOM|OPTM|CLAS|UNSP|CAUS)-(\d+)')

def _repl(m):
    return f"{m.group(1)}-{int(m.group(2)):02d}"

def fix(p: pathlib.Path) -> bool:
    t = p.read_text()
    t2 = PAT.sub(_repl, t)
    if t2 != t:
        p.write_text(t2)
        return True
    return False

if __name__ == '__main__':
    n = 0
    for a in sys.argv[1:]:
        if fix(pathlib.Path(a)):
            n += 1
    print(f"{n} file(s) changed")
