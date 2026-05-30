#!/usr/bin/env python3
"""Execute every ```{python} figure chunk in the given .qmd files the way Quarto's
Jupyter kernel does (one namespace per file, chunks in document order) and report any
runtime errors — so we catch figure breakage locally instead of in a slow CI render.

Usage:  MPLBACKEND=Agg python3 tools/check_figures.py <file.qmd> [...]
Exit code 0 = all clean, 1 = at least one file errored.
"""
import os, re, sys, io, contextlib, pathlib, traceback
os.environ.setdefault('MPLBACKEND', 'Agg')

def check(path: pathlib.Path):
    chunks = re.findall(r"```\{python\}\n(.*?)```", path.read_text(), re.S)
    if not chunks:
        return None
    code = "\n".join(chunks)
    g = {"__name__": "__main__"}
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            exec(compile(code, path.name, "exec"), g)
        try:
            import matplotlib.pyplot as plt; plt.close('all')
        except Exception:
            pass
        return None
    except Exception:
        return traceback.format_exc().strip().splitlines()[-1]

if __name__ == '__main__':
    fails = []
    for arg in sys.argv[1:]:
        err = check(pathlib.Path(arg))
        if err:
            fails.append((arg, err))
    n = len(sys.argv) - 1
    print(f"checked {n} file(s), {len(fails)} with errors")
    for name, err in fails:
        print(f"FAIL {name}\n     {err}")
    sys.exit(1 if fails else 0)
