#!/usr/bin/env python3
"""Generate one standalone Quarto *book* project per track, so each track renders to its
own PDF (e.g. "Probability Foundations.pdf") in addition to the full bound book and the
per-article PDFs.

No content is duplicated: each generated project under build/books/<slug>/ is a symlink
farm pointing back at articles/<slug>/*.qmd, plus a generated _quarto.yml (book config with
the same PDF preamble as the main book) and a tiny index.qmd title page.

Zero-filled numeric IDs (PROB-00..) and movement IDs (INFR-A1..) both sort correctly with a
plain lexicographic sort, so chapter order = sorted(filenames).

Usage:  python3 tools/make_track_books.py     (regenerates build/books/ from articles/)
"""
import os, pathlib, shutil

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

def quarto_yaml(name, chapter_files):
    chapters = "\n".join(f"        - {f}" for f in chapter_files)
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
            (proj / f.name).symlink_to(os.path.relpath(f, proj))
        (proj / "index.qmd").write_text(
            f"# {name} {{.unnumbered}}\n\n"
            f"A *Core Sample* track — {len(files)} articles, each an inch wide and a mile deep.\n"
        )
        (proj / "_quarto.yml").write_text(quarto_yaml(name, [f.name for f in files]))
        built.append((slug, name, len(files)))
    for slug, name, n in built:
        print(f"  {slug}: {n} chapters -> build/books/{slug}")
    print(f"generated {len(built)} track book project(s)")

if __name__ == "__main__":
    main()
