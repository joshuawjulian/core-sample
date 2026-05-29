# Core Sample — Authoring Constitution

**Core Sample** is a series of standalone monographs on data-science topics, authored
as Quarto `.qmd` and rendered to PDF. Each article is **an inch wide and a mile deep**:
it answers *one* tightly-scoped question and follows it all the way to the bottom.

This file is the binding standard for every article. The clauses in
**§1 Non-Negotiables** are not stylistic preferences — they are requirements. If an
article cannot satisfy them, the *scope* is wrong (see §2), not the standard.

---

## The Reader

The reader is a **"coder"** — a computer-science undergrad background, now a **graduate
student in data science** — fluent in code and rigorous reasoning, who **understands
mathematics but is rusty**. They have seen this math before and can absolutely follow it
again — but only if **nothing is assumed**. Definitions, identities, and steps they once
knew but have not used in years must all be on the page.

This is **not** "code-first." In the articles, **the math is the primary subject and
implementation is secondary.** The reader is a coder by training, not because code leads
the content — code is in service of the math, never the other way around.

The depth of this series comes from the reader being able to *follow every move* despite
the rust, not from terse or compressed rigor.

Write for someone who says: *"I have a CS degree and I get this stuff, but it's been
years — don't assume I remember the trick, and don't skip a step."*

---

## The Goal — Graduate-Level Mastery

The outcome standard of every article is that, after reading it, the reader has a
**graduate-level understanding** of the topic — the command expected of someone who has
*graduated from a data-science master's program*. Concretely, an article should leave the
reader able to:

- **Pass a graduate course** covering the topic — handle the exam questions and the
  problem sets, not just recognize the term.
- **Pass a technical / coding interview** on it, answering at the level interviewers
  expect from a grad-program graduate: state it precisely, derive it, reason about its
  assumptions and trade-offs, and connect it to neighboring ideas.
- **Know when to actually use it — and when not to.** Real practitioner judgment: the
  problem shapes where this technique is the right tool, the conditions under which it
  shines, the conditions under which it fails or is the *wrong* choice, and what you reach
  for instead. The reader should finish able to make a sound applicability call on a
  problem they have never seen.

This is the bar. **Buildup is allowed and expected** to reach it — if achieving a
graduate understanding of topic X requires first establishing Y and Z, build them up
(inline or via track prerequisites in §1.3). Never short-change the destination to save
space; that is what tracks and the split protocol (§2) are for.

A calibration note: **not every subject is intrinsically graduate-level**, and an article
should not inflate a simple idea into false complexity. Match the *treatment* to the
topic — but always bring the reader to graduate-level **command** of whatever that topic
is. The depth target is the reader's mastery, not an artificial difficulty quota.

---

## Creative Freedom — fixed ends, free means

Read everything below in this light. **What each article must *achieve* is fixed; how it
gets there is wide open.** The non-negotiables (§1) and the goal define the *ends* — the
*why* kept in view, honest examples and visuals, narrative build, fully explicit
derivations with nothing implicit above Calc 1, anticipated interview questions, and
graduate-level mastery with real applicability judgment. Those are non-negotiable.

The *form* is not. Article **order, length, shape, structure, and decomposition are free**
— articles may be long or short, a track may branch or merge, the section skeleton (§3)
may be reordered, sections added or dropped, an idea split or combined — **whenever a
different shape is the best way to get the information across.** Pick the structure the
material wants, not the one a template prescribes.

The single test of any formal choice: *does it do the job (§1 + the goal), and is it the
best way to convey this particular idea?* If yes, the form is correct. The rules below
constrain **outcomes**, not creativity.

## §1 — Non-Negotiables

Every article MUST satisfy all five of these. No exceptions. (They are *ends* to achieve,
not a prescribed shape — see "Creative Freedom" above.)

**Priority when they compete — the math is primary.** The *why* (§1.1) and visuals (§1.2)
are essential and required, never optional. But when space, ordering, or emphasis force a
trade-off, **the math leads and everything else serves it.** Required does not mean
co-equal: the *why* motivates the math, visuals illuminate the math, examples ground the
math, interview-prompts stress-test the math — none of them displaces the mathematical
core. If a cut must be made, cut toward more math, not less.

### 1.1 Keep the "why" in mind — the whole way through
Every article MUST establish, and then **keep in view**, *why this idea exists*: the
problem it was invented to solve, what came before and why that was inadequate, and the
tension that forced it into existence. History is the **vehicle** for this, not the point
— we tell the origin story because it carries the *why*, and the *why* is what we hold
onto for the rest of the article.

The *why* is **not** a one-time opening paragraph you then leave behind. It threads
through everything: it explains **why the method is built the way it is** and **why it's
implemented the way it is.** Every choice in the formalism (§1.4) and every implementation
note should trace back to the original *why* — when a step appears, the reader should be
able to see which part of the motivating problem it answers. When the *why* is kept in
mind, the *how* and the *why-this-way* stop feeling arbitrary and start feeling inevitable.

### 1.2 Multiple real-world examples, with visuals
Every article MUST contain **multiple concrete, real-world worked examples** — not one,
not a toy. Each must be carried through end-to-end.

**Examples must be honest, never contrived.** Do not engineer an example that flatters the
technique — one rigged so the method looks more broadly usable (or less) than it really
is. Use the kinds of problems and data where the technique genuinely belongs, with their
real messiness. Include at least one example near the **edge of applicability** — a case
where it strains, breaks, or is the wrong tool — so the reader sees the honest boundary,
not a highlight reel. Every article MUST make explicit **when this technique applies and
when it does not**, and what one reaches for instead when it does not.

Every article MUST include **visuals generated in the `.qmd`**: plots, charts, diagrams,
connected/relationship graphs — whatever the concept actually needs to be *seen*. A
derivation without a picture of what it does is incomplete. Use real data or realistic
data where possible. Figures are first-class content, not garnish.

### 1.3 Articles build on each other — flow within tracks
The series is organized into **tracks**: ordered sequences where each article builds on
the last. *Inch wide, mile deep* applies across a track as much as within one article.

> Example track — **Regression**: simple linear regression → multiple regression →
> regularization → generalized linear models → ... → nonparametric regression → ...

Every article MUST state where it sits in its track — what it assumes the reader has
already read (with links), and what it sets up next. There must be a **narrative flow**:
an article is a chapter in a story, not an isolated entry. A reader moving through a
track in order should feel a continuous build, never a cold start.

**Tracks are not the same length, and that's expected.** One track may be 4–5 articles;
another may be 30. Let the subject dictate the count — never pad a short track or starve a
deep one to hit some uniform size. When a track threatens to balloon (e.g. Bayesian
methods, which sprawl), we have three legitimate moves, chosen per case: **(a)** let it be
a large track; **(b)** split it into several smaller sibling tracks; or **(c)** sprinkle
its pieces into the tracks that need them, where each piece is most motivated. Decide this
the same way as the split/prerequisite protocols — propose the options and discuss before
committing.

### 1.4 Full derivations — every step, zero assumptions
Every derivation MUST show **every step**. This is the heart of the series.

- **No skipped steps.** No "it follows that," "clearly," "it can be shown,"
  "after some algebra," or "left to the reader." If algebra happens, the algebra is on
  the page.
- **No assumed prior results inside a derivation.** If a step relies on a result, either
  derive it inline or link to the Core Sample that derives it — never assume the reader
  already carries it.
- **No notational leaps.** Define every symbol the first time it appears. When notation
  changes form, say why.
- Advanced is fine; **opaque is not.** We will happily do graduate-level derivations —
  but the reader must be able to follow each line without filling in a gap themselves.

**The knowledge floor.** Exactly one thing may be assumed: mathematical maturity up to
roughly **precalculus / Calculus I** (algebra, functions, limits, basic
differentiation/integration at the Calc-1 level). **Everything above that floor is
explicit** — linear algebra, probability, statistics, multivariable/vector calculus,
optimization, measure-theoretic notions, every named theorem, every identity. If a step
uses it and it lives above the floor, it is either derived inline or carried by a
prerequisite article (below). **Nothing implicit. Nothing.** Length is irrelevant — if
explicitness makes an article long, we split it (§2); we do not compress.

**Prerequisite protocol.** If writing an article would require leaning on knowledge above
the floor that is too large to build inline without burying the main idea, **do not
assume it and do not hand-wave it.** Instead, stop and **propose one or more prerequisite
articles to prepend** to the current one — titled, scoped, in track order — and explain
what each one establishes and why it must come first. We discuss and confirm the
prerequisite chain before writing the dependent article. (This is the same spirit as the
split protocol in §2, applied *backward* in a track.)

The test: a coder with a CS degree and rusty math — who remembers Calc 1 and nothing
above it reliably — can read the derivation top-to-bottom and never get stuck on a move
they can't reconstruct.

### 1.5 Anticipate the interview — answer the question before it's asked
Every article MUST **get in front of the questions a sharp examiner or interviewer would
ask** about the topic, and answer them explicitly. We do not wait for the reader to wonder
— we voice the question for them and resolve it on the spot.

As each section develops, surface the natural question that a reader (or an interviewer)
would raise at that moment and answer it immediately, in flow:
- *"Why would we do this here?"* (motivation / justification)
- *"Where would this actually be used — and where wouldn't it?"* (applicability, ties to §1.2)
- *"How would you implement this?"* (the practical move, kept secondary to the math per §4)
- *"What's the catch — what would an interviewer push back on?"* (assumptions, trade-offs, gotchas)

These are written so they read as a **natural part of the article's narrative** — an aside
that voices what the reader is already thinking — while systematically covering the
**interview and exam surface** of the topic. They may be set off as a recurring callout
(working name: a *"You might be asked / Interview lens"* box — final styling in §5) or woven
into the prose, but they MUST be present and explicit, never left implicit. By the end of
an article, the common interview/exam questions on its topic should each have been raised
and answered somewhere in it.

This operationalizes the "pass the interview" half of **The Goal** — and, like everything
else, it serves the math rather than competing with it.

---

## §2 — Scope Discipline ("inch wide")

If §4 (the formal development) cannot reach the bottom of the idea within **~30 pages**,
the article is **secretly two or more articles** — split it and add them to the track.
The "inch wide" constraint *forces* decomposition. We would rather have three razor-
focused Core Samples than one sprawling survey.

Hard ceiling: **30 pages per article.** Target the depth, let the page count fall out,
but if it exceeds 30, split.

**Split protocol.** When an article runs long (or is trending past ~30 pages), do not
silently truncate or compress — instead **stop and propose a split**:
- Name the **natural seam(s)** — the exact section/derivation boundary where the article
  should be cut (e.g. "split after §4.3, where the ELBO is introduced").
- Propose the resulting articles as **titled, scoped pieces** with a one-line abstract
  each, in their intended **track order**.
- Explain *why* the seam is the right cut (each side must stand as its own inch-wide,
  mile-deep idea).
- Wait for confirmation on the split before continuing to write.

---

## §3 — Article Skeleton (default, not a cage)

A sensible **default** spine — a starting point, not a requirement. Reorder it, drop
sections, add sections, or restructure entirely whenever the material is better served
another way (see "Creative Freedom"). The skeleton exists so you never start from a blank
page, not to force every article into one mold.

0. **Abstract** — 3–4 lines: the one concept + the single claim the article defends.
1. **The Core** — the one-sentence idea, boxed; everything orbits this.
2. **History / why we're here** — §1.1.
3. **Intuition first** — the geometric/probabilistic picture before any symbols.
4. **Formal development** — definitions → results → **full derivations** (§1.4).
5. **Worked examples** — multiple, real-world, with visuals (§1.2).
6. **Failure modes** — assumptions that break it, edge cases, common misuses.
7. **Connections** — links to neighboring Core Samples; place in the track (§1.3).
8. **Going deeper** — primary sources, the rabbit hole, open threads.

---

## §4 — Locked Decisions

- **Name:** Core Sample. Standalone titles (no issue numbers).
- **Format:** Quarto `.qmd` → PDF.
- **Dual output — both targets, same source files:**
  1. **Per-article PDF.** Every article `.qmd` renders on its own to a self-contained PDF
     — grab one, print it, move on. This is the everyday workflow.
  2. **The bound book.** The entire library renders to a single continuous PDF that reads
     like a book — hit "print the book" and get one ordered volume, however many thousands
     of pages it is. Structure: **Parts = tracks (§1.3), chapters = articles**, in track
     order. Front matter (title page, full table of contents), cross-references, and
     continuous numbering all resolve in this mode.

  Neither target is second-class. The scaffold must make an article work *both* as a
  standalone document and as a chapter in the book without per-article rework. (Leading
  approach: a Quarto `book` project for the bound volume + per-file standalone render;
  exact mechanism finalized in §5.)
- **Build:** GitHub Actions (source-of-truth) **and** a devcontainer (local preview).
  Host (WSL) stays lean — no host-level LaTeX/Quarto install.
- **Math depth:** graduate-level, **full proofs/derivations**, every step shown (§1.4).
- **Math is primary, implementation is secondary.** The math leads every article. Code
  is language-agnostic and appears only in service of the math: to clarify something you
  cannot see by hand (e.g. convergence behavior, numerical instability) and to generate
  the figures. Code is never the main event.

---

## §5 — Open Decisions (still being designed)

- Repo layout & file-naming convention for tracks + articles — must support **both**
  output targets in §4 (standalone per-article PDF *and* the single bound book) from one
  set of source files.
- Cross-reference registry (how forward-links to not-yet-written articles stay valid).
- Visual design: typeset callout boxes (Core / Definition / Theorem / Proof ∎ / Pitfall),
  LaTeX template, title page, typography.
- Master topic taxonomy across all tracks (see §6 for tracks designed so far).
- Authoring + review workflow at scale.

---

## §6 — Tracks

Each track is its own file in **`tracks/`** — that folder is the source of truth for what
tracks exist and what's in them. **Do NOT enumerate or inline tracks here** (CLAUDE.md is
auto-loaded every session; keeping the list out of it keeps context lean and means this
file never needs editing when a track is added). To work on a track, list `tracks/` and
have an agent read the relevant file on demand.
