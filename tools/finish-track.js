export const meta = {
  name: 'finish-track',
  description: 'Finish a partially-written track: write missing articles, verify the rest',
  phases: [
    { title: 'Write', detail: 'draft + verify the missing articles' },
    { title: 'Verify', detail: 'quality-gate the already-written-but-unverified articles' },
  ],
}

const A = (typeof args === 'string') ? JSON.parse(args) : args
const TRACK = A.track            // { slug, name, file }
const WRITE = A.write || []      // [{ id, slug, title }] -> write then verify
const VERIFY = A.verify || []    // [{ id, path }]        -> verify only

const EXEMPLAR = 'articles/regression/REGR-01-ols-one-predictor.qmd'

const writePrompt = (a) => `You are writing ONE complete Core Sample article as a Quarto .qmd file — a finished, graduate-level monograph, NOT an outline.

Article: ${a.id} — "${a.title}"
Track: ${TRACK.name}
Write it to EXACTLY: /home/julian/dev/core-sample/articles/${TRACK.slug}/${a.id}-${a.slug}.qmd

STEP 1 — Read and obey (Read tool):
- /home/julian/dev/core-sample/CLAUDE.md (constitution)
- /home/julian/dev/core-sample/REGISTRY.md (ID scheme, file paths, Quarto-native authoring syntax)
- /home/julian/dev/core-sample/${TRACK.file} (find the ${a.id} entry; honor its scope/Assumes/Sets up/depth)
- /home/julian/dev/core-sample/${EXEMPLAR} (the GOLD-STANDARD exemplar — match its depth, rigor, voice)
- A couple of sibling files in articles/${TRACK.slug}/ to match this track's established style.

STEP 2 — Constitution essentials: keep the WHY in view; MULTIPLE honest real-world examples WITH Python figures (\`\`\`{python} blocks, each '#| label: fig-...' + '#| fig-cap:'), at least one at the edge of applicability; FULL step-by-step derivations, nothing implicit above a Calc-1 floor; NO dangling claims (never "it can be shown"/"coincides"/"it follows that"/deferred-as-explanation — derive in place, only FLAG genuinely-imported prerequisites); anticipate interview questions ('::: {.callout-tip title="You might be asked"}'); graduate-level mastery + applicability; math primary, code secondary.

STEP 3 — Conventions: minimal YAML (title + 'subtitle: "Core Sample · ${TRACK.name}"', NO format block). Quarto-native: '::: {.callout-important title="The Core"}', '::: {.callout-warning title="Pitfall"}', '::: {.callout-tip title="You might be asked"}', theorems '::: {#thm-...}', proofs '::: {.proof}'. IMPORTANT for matplotlib labels: a render shim tolerates LaTeX, but prefer mathtext-safe forms ('\\leq' not '\\le', '\\frac{}{}' not '\\tfrac', brace '\\sqrt{}' and '\\mathcal{}'); never put literal LaTeX braces in an f-string (double them or avoid f-strings for labels). Use numpy 2.x APIs (np.trapezoid, not np.trapz). Cross-ref other articles by global ID.

STEP 4 — Re-read: valid YAML, balanced fences/divs, no skipped steps, no dangling claims. Return one line: '${a.id} written, ~N pages, M figures'.`

const verifyPrompt = (id, path) => `You are the QUALITY GATE for ONE Core Sample article. Read the constitution and the article, then FIX it in place (edit the file directly).

File: /home/julian/dev/core-sample/${path}
Read: /home/julian/dev/core-sample/CLAUDE.md and the ${id} entry in /home/julian/dev/core-sample/${TRACK.file}.

Check and FIX:
1. DANGLING CLAIMS (top priority): "it can be shown", "it turns out", "coincides", "it follows that", "one can show", "clearly", "obviously", "trivially", "by symmetry", or any result asserted-and-deferred AS its explanation. Replace with the actual derivation in place (only FLAG genuinely-imported prerequisites with a pointer).
2. Every derivation step explicit; nothing implicit above a Calc-1 floor; every symbol defined on first use.
3. Multiple honest real-world examples, at least one at the edge of applicability; "when NOT to use it" stated.
4. At least one Python figure block with '#| label: fig-...' and '#| fig-cap:'.
5. The why/history present; at least one answered "You might be asked" prompt.
6. Math primary; minimal YAML (title + subtitle, NO format block); Quarto-native callout/theorem syntax; balanced fences/divs; valid front matter.
7. matplotlib-label safety: prefer mathtext-safe LaTeX; no literal LaTeX braces inside f-strings; numpy 2.x APIs (np.trapezoid not np.trapz).

Deepen, don't trim. Return a SHORT report of concrete fixes, or "compliant — no changes".`

const out = { written: [], verified: [] }

phase('Write')
if (WRITE.length) {
  out.written = await pipeline(
    WRITE,
    (a) => agent(writePrompt(a), { label: `write:${a.id}`, phase: 'Write' }).then(() => a),
    (a) => agent(verifyPrompt(a.id, `articles/${TRACK.slug}/${a.id}-${a.slug}.qmd`), { label: `verify:${a.id}`, phase: 'Write' })
              .then(r => ({ id: a.id, report: String(r).slice(0, 200) })),
  )
}

phase('Verify')
out.verified = (await parallel(
  VERIFY.map(v => () =>
    agent(verifyPrompt(v.id, v.path), { label: `verify:${v.id}`, phase: 'Verify' })
      .then(r => ({ id: v.id, report: String(r).slice(0, 200) }))
  )
)).filter(Boolean)

return out
