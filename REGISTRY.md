# Core Sample — Registry

The cross-reference and conventions source of truth. Every article must follow the IDs,
file paths, and syntax conventions defined here. When a forward-link points at an article
that does not yet exist, the ID is still reserved here so the link stays valid.

---

## Article-ID prefixes

Every article has a global ID: a four-letter track prefix plus a number. Within a track,
numbers run in track order (`REGR-00`, `REGR-01`, ...). A letter-prefixed number (`INFR-B4`)
denotes a side-branch / sub-sequence within a track.

| Prefix | Track                   |
| ------ | ----------------------- |
| REGR   | Regression              |
| INFR   | Statistical Inference   |
| PROB   | Probability Foundations |
| GEOM   | Geometry of Data        |
| OPTM   | Optimization            |
| CLAS   | Classification          |
| UNSP   | Unsupervised Learning   |
| CAUS   | Causal Inference        |

Example IDs: `REGR-04`, `INFR-B4`.

---

## File-path convention

Each article lives at:

```
articles/<track-slug>/<ID>-<kebab-slug>.qmd
```

- `<track-slug>` is the track's directory slug (table below).
- `<ID>` is the global article ID (e.g. `REGR-01`).
- `<kebab-slug>` is a short kebab-case description of the article.

Example: `articles/regression/REGR-01-ols-one-predictor.qmd`.

| Prefix | Track slug                |
| ------ | ------------------------- |
| REGR   | `regression`              |
| INFR   | `statistical-inference`   |
| PROB   | `probability-foundations` |
| GEOM   | `geometry-of-data`        |
| OPTM   | `optimization`            |
| CLAS   | `classification`          |
| UNSP   | `unsupervised-learning`   |
| CAUS   | `causal-inference`        |

---

## Authoring syntax conventions

All of the following are Quarto-native and render correctly in PDF. Every article MUST use
these forms so that numbering, cross-references, and callout styling stay consistent across
standalone and book builds.

### Theorem-like environments

Use Quarto's cross-referenceable div syntax. The `#`-prefix encodes the environment type:

```markdown
::: {#thm-slug}
Statement of the theorem.
:::

::: {#lem-slug}
Statement of the lemma.
:::

::: {#def-slug}
The definition.
:::
```

- Theorems: `::: {#thm-...}`
- Lemmas: `::: {#lem-...}`
- Definitions: `::: {#def-...}`

Reference them inline with `@thm-slug`, `@lem-slug`, `@def-slug`.

Proofs use the proof class (closes with the ∎ tombstone automatically):

```markdown
::: {.proof}
The argument, every step shown.
:::
```

### Callout boxes

| Purpose                | Syntax                                                       |
| ---------------------- | ----------------------------------------------------------- |
| **The Core** (§3.1)    | `::: {.callout-important title="The Core"}`                 |
| **Pitfall** (§6)       | `::: {.callout-warning title="Pitfall"}`                    |
| **Interview prompt**   | `::: {.callout-tip title="You might be asked"}`             |

Each opens with the fenced div and closes with `:::`.

### Figures

Figures are generated in Python code blocks and must carry a label and a caption so they
are cross-referenceable:

````markdown
```{python}
#| label: fig-residuals
#| fig-cap: "Residuals of the one-predictor OLS fit."

import matplotlib.pyplot as plt
# ... plotting code ...
```
````

Reference figures inline with `@fig-residuals`. Labels must start with `fig-`.

---

## Resolved ownership decisions

To avoid two tracks deriving the same machinery, the following topics have a single owning
article; every other track links to it rather than re-deriving.

- **EM algorithm** — owned by **Unsupervised Learning** (`UNSP-05`). Other tracks (e.g.
  mixture models, missing-data treatments) link to `UNSP-05`.
- **The kernel trick** — owned by **Classification** (`CLAS`), introduced alongside SVMs.
  Other tracks link to the SVM article rather than re-introducing kernels.
- **Cross-method evaluation** — a future **Model-Evaluation** track is planned to absorb
  evaluation material that spans methods. Until it exists, `CLAS-18..20` carry this content
  as interim home; expect those to migrate when the track is created.
