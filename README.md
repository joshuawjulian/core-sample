# Core Sample

> **An inch wide and a mile deep.** A series of standalone data-science monographs,
> authored in Quarto and rendered to PDF. Each article answers *one* tightly-scoped
> question and follows it all the way to the bottom — for a coder with a CS background and
> rusty math, with **nothing assumed above a Calculus-I floor** and **every derivation step
> on the page**.

The full authoring standard lives in **[`CLAUDE.md`](CLAUDE.md)**. The cross-reference
scheme, file conventions, and authoring syntax live in **[`REGISTRY.md`](REGISTRY.md)**.

## How it's organized

- **Tracks** are ordered sequences where each article builds on the last (e.g. Regression:
  simple OLS → projection → multiple regression → … → nonparametric). Each track's roadmap
  is a file in **[`tracks/`](tracks/)**.
- **Articles** live at `articles/<track-slug>/<ID>-<slug>.qmd`. Global IDs use four-letter
  track prefixes: `REGR-`, `INFR-`, `PROB-`, `GEOM-`, `OPTM-`, `CLAS-`, `UNSP-`, `CAUS-`.
- **Dual output, one source:** every article renders **standalone** to its own PDF, and the
  whole library renders as **one bound book** (Parts = tracks, chapters = articles).

## Building the PDFs

The host stays lean — no Quarto/LaTeX installed locally. Two supported paths:

- **GitHub Actions** (source of truth): `.github/workflows/render.yml` renders the book on
  every push to `main` and uploads the PDF as the `core-sample-pdf` artifact.
- **Devcontainer** (local preview): `.devcontainer/` provides Quarto + TinyTeX + Python.
  Then `quarto render` (book) or `quarto render articles/regression/REGR-1-*.qmd` (one).

## Status — tracks designed, scaffold built, pilots written

**8 tracks designed (~170 articles mapped), 2 articles written.**

| Track | Prefix | Articles | Roadmap |
|---|---|---:|---|
| Regression | `REGR` | 27 | [tracks/regression.md](tracks/regression.md) |
| Statistical Inference | `INFR` | 18 | [tracks/statistical-inference.md](tracks/statistical-inference.md) |
| Probability Foundations | `PROB` | 24 | [tracks/probability-foundations.md](tracks/probability-foundations.md) |
| Geometry of Data | `GEOM` | 28 | [tracks/geometry-of-data.md](tracks/geometry-of-data.md) |
| Optimization | `OPTM` | 18 | [tracks/optimization.md](tracks/optimization.md) |
| Classification | `CLAS` | 21 | [tracks/classification.md](tracks/classification.md) |
| Unsupervised Learning | `UNSP` | 16 | [tracks/unsupervised-learning.md](tracks/unsupervised-learning.md) |
| Causal Inference | `CAUS` | 18 | [tracks/causal-inference.md](tracks/causal-inference.md) |

**Written so far:**
- `REGR-0 — Why a Line?` (motivational opener; history of least squares + regression to the mean)
- `REGR-1 — OLS, One Predictor` (flagship pilot: the full step-by-step derivation, Old
  Faithful worked example, the Anscombe quartet)

### ⚠️ One thing to check first
The Quarto/LaTeX pipeline has **not been rendered yet** — it couldn't be built on this host.
All config and article front matter pass YAML/JSON validation, but the *real* test is the
first **GitHub Actions run** (Actions tab → "Render PDFs"). If it errors, the fix is a
next-session task. **Please skim REGR-1 and REGR-0 for depth/format/voice** before we mass-
produce — they are the template every future article will follow.

### Suggested next steps
1. Confirm the first CI render produces a clean PDF (or report the error to fix).
2. React to the pilots — adjust the article template/voice if needed.
3. Then scale: write the rest of the Regression trunk (REGR-2 … REGR-13), and/or the
   prerequisite-free entry articles of the foundational tracks (PROB-0, GEOM-0, OPTM-0).
