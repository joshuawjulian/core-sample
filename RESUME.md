# Resume Playbook — Core Sample mass production

The library is being filled in by an automated, **resumable** pipeline. If a run pauses
(token limits, manual stop, or session end), use this to restart cleanly. **Nothing is
lost:** every completed track is committed, and the `.qmd` files on disk are the ground
truth for what's done.

## Wave status (update as tracks complete)

| Wave | Track | slug | Articles | Status |
|---|---|---|---:|---|
| — | Pilots | regression | 2 (REGR-00,1) | ✅ committed |
| 1 | Probability Foundations | probability-foundations | 24 | ✅ committed |
| 2 | Geometry of Data | geometry-of-data | 28 | ✅ committed |
| 3 | Optimization | optimization | 18 | 🔄 in progress |
| 4 | Statistical Inference | statistical-inference | 18 | ⬜ pending |
| 5 | Regression (REGR-02…26) | regression | 25 | ⬜ pending |
| 6 | Classification | classification | 21 | ⬜ pending |
| 7 | Unsupervised Learning | unsupervised-learning | 16 | ⬜ pending |
| 8 | Causal Inference | causal-inference | 18 | ⬜ pending |

**Ground truth for any track:** `ls articles/<slug>/*.qmd` — files present = articles done.

## The pipeline

A reusable workflow drafts + quality-gates every article in one track:

- **Script (persists on disk):**
  `~/.claude/projects/-home-julian-dev-core-sample/<session>/workflows/scripts/write-track-articles-wf_eb3a3c23-06c.js`
- Per article: a **write** agent (reads `CLAUDE.md`, `REGISTRY.md`, the track roadmap in
  `tracks/<slug>.md`, and the `REGR-01` exemplar) + a **verify** agent (hunts dangling
  claims / skipped steps and fixes them in place).

## To resume

1. **Same session, interrupted mid-track:** re-invoke `Workflow` with that `scriptPath`
   plus `resumeFromRunId` — completed agents return cached, only unfinished ones re-run.
2. **Fresh session (after limits refresh):** for each not-yet-complete track, build the
   `args` from the article list in `tracks/<slug>.md` (the `### <ID> — <title>` headings),
   and run the workflow with `{ track: {slug,name,file}, articles: [{id,slug,title}…] }`.
   **Pass only articles whose `.qmd` is not already on disk** (skip finished ones).
3. **After a track's files exist:** figure-gate them (`tools/check_figures.py`), zero-fill
   IDs if needed (`tools/zfill_ids.py`), then just `git commit` + `git push`. No `_quarto.yml`
   editing — CI runs `tools/make_track_books.py` (scans `articles/<slug>/`) and renders a
   **per-track book PDF** plus **per-article PDFs** to the `latest` release. There is no
   single combined book (dropped: too large).

## Pause policy

Stop at the next article/track boundary, commit completed work, and update the Status
table above. Because writes are one-file-per-article and the workflow caches completed
agents, resuming never repeats finished work.
