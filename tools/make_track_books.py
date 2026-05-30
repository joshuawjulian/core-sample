#!/usr/bin/env python3
"""Generate one standalone Quarto *book* project per track, so each track renders to its
own PDF (e.g. "Optimization.pdf").

Each article becomes exactly ONE chapter: we prepend a chapter heading "# <ID> — <title>"
and DEMOTE the article's own headings by one level (# -> ##, ## -> ###, ...), skipping
'#' comment lines inside ```{python}``` code blocks. Without this, every article's
section-level '#' headings would each become a top-level book chapter, dissolving the
article boundaries into one long flat run of chapters.

Result: clear per-article breaks (new page + "Chapter N · <ID> — <title>"), and the book
TOC maps each <ID> to its page range for per-article printing. Source articles are not
modified — transformed copies are written under build/books/<slug>/.

Usage:  python3 tools/make_track_books.py
"""
import os, re, shutil, pathlib

try:
    import yaml
except ImportError:
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
ART = ROOT / "articles"
BUILD = ROOT / "build" / "books"

TRACKS = {
    "probability-foundations": "Probability Foundations",
    "geometry-of-data": "Geometry of Data",
    "optimization": "Optimization",
    "statistical-inference": "Statistical Inference",
    "regression": "Regression",
    "classification": "Classification",
    "unsupervised-learning": "Unsupervised Learning",
    "causal-inference": "Causal Inference",
}

HEADING = re.compile(r'^(#{1,6})(\s)')
FENCE = re.compile(r'^\s*```')

def article_id(name):           # "OPTM-01-one-...qmd" -> "OPTM-01"; "INFR-A1-...qmd" -> "INFR-A1"
    return "-".join(name.split("-")[:2])

def front_matter_title(text, fallback):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if m and yaml:
        try:
            d = yaml.safe_load(m.group(1)) or {}
            if d.get("title"):
                return str(d["title"])
        except Exception:
            pass
    return fallback

def to_chapter(text, aid, title):
    m = re.match(r'^---\n.*?\n---\n', text, re.S)
    body = text[m.end():] if m else text
    out, in_fence = [], False
    for line in body.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            hm = HEADING.match(line)
            if hm:
                line = '#' * min(len(hm.group(1)) + 1, 6) + line[len(hm.group(1)):]
        out.append(line)
    head = f"# {aid} — {title}\n\n"
    return head + "\n".join(out).lstrip("\n") + "\n"

def quarto_yaml(name, chapter_files):
    chapters = "\n".join(f"    - {f}" for f in chapter_files)
    return f'''project:
  type: book
  output-dir: _out

book:
  title: "{name}"
  subtitle: "Core Sample"
  author: "Joshua Julian"
  chapters:
    - index.qmd
{chapters}

execute:
  freeze: auto
  echo: false
  warning: false

jupyter: python3

crossref:
  thm-title: "Theorem"
  lem-title: "Lemma"
  def-title: "Definition"
  cor-title: "Corollary"
  prp-title: "Proposition"

format:
  pdf:
    documentclass: scrbook
    classoption:
      - oneside
      - open=any
    number-sections: true
    toc: true
    colorlinks: true
    fig-pos: "H"
    geometry:
      - top=1in
      - bottom=1in
      - left=1.25in
      - right=1.25in
    include-in-header:
      text: |
        \\usepackage{{mathtools}}
        \\raggedbottom
'''

def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    built = []
    for slug, name in TRACKS.items():
        src = ART / slug
        files = sorted(src.glob("*.qmd"))
        if not files:
            continue
        proj = BUILD / slug
        proj.mkdir(parents=True)
        for f in files:
            aid = article_id(f.name)
            text = f.read_text()
            title = front_matter_title(text, aid)
            (proj / f.name).write_text(to_chapter(text, aid, title))
        (proj / "index.qmd").write_text(
            f"# {name} {{.unnumbered}}\n\n"
            f"A *Core Sample* track — {len(files)} articles, each an inch wide and a mile deep. "
            f"Each chapter is one article, labelled with its ID (e.g. {article_id(files[0].name)}); "
            f"use the table of contents to find an article's pages.\n"
        )
        (proj / "_quarto.yml").write_text(quarto_yaml(name, [f.name for f in files]))
        built.append((slug, len(files)))
    for slug, n in built:
        print(f"  {slug}: {n} chapters")
    print(f"generated {len(built)} track book project(s)")

if __name__ == "__main__":
    main()
