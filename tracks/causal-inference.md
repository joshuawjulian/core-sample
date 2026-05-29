# Core Sample — Track Roadmap: **Causal Inference**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

## PART 0 — Aim, and the Boundary with Regression and Inference

### Charter (one paragraph)

> **Causal Inference** is the track that earns the word *because*. Every other track in this
> series answers questions of *association* — what tends to occur with what, how to predict one
> thing from another, how sure we are about a number. This track asks the categorically harder
> question: **if we intervene and change `X`, what happens to `Y`** — not "what `Y` do we *observe*
> alongside this `X`," but "what `Y` would we *cause*." It builds the language for that question
> (potential outcomes and causal graphs), confronts the **fundamental problem** that the
> counterfactual we want is never observed, names the precise conditions (ignorability, the backdoor
> criterion, SUTVA) under which observed data can stand in for an experiment, and then develops the
> estimators — matching, weighting, regression adjustment, instruments, diff-in-diff, discontinuities
> — that recover a causal effect from data, each with the assumptions it lives or dies by. The reader
> finishes able to *state a causal estimand precisely, draw the DAG that encodes their assumptions,
> decide whether the effect is even identifiable, choose the estimator the design calls for, and say
> honestly how badly an unmeasured confounder could be hiding in the answer.*

### The boundary with Regression and Inference (explicit contract)

This track sits **downstream** of Regression and Statistical Inference and consumes both. The
single most important contract: **Causal Inference owns the *target* (the causal estimand and the
assumptions that identify it); Regression and Inference own the *machinery* (fitting models,
sampling distributions, standard errors).** A causal estimator is almost always "fit some
familiar model, but at a quantity chosen so its coefficient *means* a causal effect." We never
re-derive OLS, the GLM, the MLE, or a confidence interval here — we link back and spend our pages
on *why this particular regression identifies a cause*.

| Concern | Owned by **Causal Inference** (this track) | Owned elsewhere |
|---|---|---|
| The **potential-outcomes** notation `Y(1), Y(0)` and the counterfactual estimand (ATE, ATT) | ✅ owns | — |
| **Identification** assumptions (ignorability, SUTVA, positivity, backdoor, exclusion) | ✅ owns | — |
| **Causal DAGs**, d-separation, colliders, the do-operator | ✅ owns | — |
| Fitting OLS / GLM, the normal equations, IRLS | links | ✅ **Regression** |
| The **sampling distribution / standard error** of an estimator, the bootstrap, CIs | links | ✅ **Inference** |
| **Propensity score** as a *fitted probability model* | shares (owns its causal *role*) | logistic fit is **Regression** |
| **Logistic / linear regression coefficients** as numbers | links | ✅ **Regression** |
| Whether a coefficient estimates a **cause** vs. an association | ✅ owns | — |

The rule of thumb: **if the deliverable is "a causal claim and the assumptions licensing it,"
it's this track's job; if the deliverable is "a fitted model or a quantified uncertainty about a
number," it belongs to Regression or Inference and we link rather than re-derive.**

---

## The flow diagram

```
                 [CAUS-0] Correlation Is Not Causation (and why that sentence is useless alone)
                                        │
                                        ▼
                 [CAUS-1] The Fundamental Problem of Causal Inference (the missing counterfactual)
                                        │
                                        ▼
                 [CAUS-2] Potential Outcomes: the Rubin Causal Model (Y(1), Y(0), ATE, ATT)
                                        │
                                        ▼
                 [CAUS-3] SUTVA and Positivity (the fine print that makes "an effect" well-defined)
                                        │
                  ┌─────────────────────┼─────────────────────────┐
                  ▼                                                ▼
   GRAPH LANGUAGE  [CAUS-4] Causal DAGs & the do-Operator     [CAUS-7] Randomization: the Gold Standard
                  │                                        (why an RCT identifies the ATE for free)
                  ▼                                                │
   [CAUS-5] d-Separation: Reading Independence off a Graph            │
                  │                                                │
                  ▼                                                │
   [CAUS-6] Confounders, Colliders & the Backdoor Criterion ◄─────────┘
   (+ selection bias, M-bias, "don't condition on a collider")
                  │
        ┌─────────┴───────────────── ADJUSTMENT UNDER IGNORABILITY ──────────────────┐
        ▼                                                                             ▼
   [CAUS-8] Regression Adjustment        [CAUS-9] The Propensity Score        [CAUS-10] Matching on Covariates
   (the backdoor formula via a       (collapsing confounders to       (and on the propensity score)
    model — links to Regression)      one number)                                    │
        │                                   │                                         │
        │                                   ▼                                         │
        │                          [CAUS-11] Inverse-Probability Weighting ◄──────────────┘
        │                          (reweighting to a pseudo-population)
        │                                   │
        └───────────────┬───────────────────┘
                        ▼
              [CAUS-12] Doubly-Robust Estimation (AIPW: two chances to be right)
                        │
        ┌───────────────┴──────────── WHEN IGNORABILITY FAILS ────────────────────┐
        ▼                          ▼                          ▼                    ▼
  [CAUS-13] Instrumental        [CAUS-14] Difference-in-      [CAUS-15] Regression      (designs that
  Variables                 Differences              Discontinuity          break confounding
  (a back door you can't    (parallel trends as      (local randomization   WITHOUT measuring it)
   close → find a valve)     the identifying bet)     at a threshold)
        └──────────────────────────┬────────────────────────────┘
                                    ▼
              [CAUS-16] Sensitivity Analysis (how wrong could an unmeasured confounder make us?)
                                    │
                                    ▼
              [CAUS-17] Putting It Together: Choosing a Design (the decision tree)
```

Linear reading order: **CAUS-0 → CAUS-1 → CAUS-2 → CAUS-3 → CAUS-4 → CAUS-5 → CAUS-6 → CAUS-7 → CAUS-8 → CAUS-9 → CAUS-10 → CAUS-11 → CAUS-12 →
CAUS-13 → CAUS-14 → CAUS-15 → CAUS-16 → CAUS-17.** The graph language (CAUS-4–CAUS-6) and the potential-outcomes language
(CAUS-1–CAUS-3) are two dialects for the same ideas; CAUS-6 is where they fuse (backdoor = ignorability).

---

## A. The Question and the Language

### CAUS-0 — Correlation Is Not Causation (and Why That Sentence Is Useless Alone)
1. **The one question:** Everyone knows correlation isn't causation — so what *is* causation, and why can't statistics-as-usual ever get at it?
2. **Scope / inside:**
   - The three sources of an observed association — a true cause, a common cause (confounding), and a selection/collider artifact — previewed with one honest example of each (the classic ice-cream/drowning confound; the hospitalized-patients collider).
   - Why prediction and causation are *different goals*: a model can predict `Y` from `X` beautifully and be useless for "should we change `X`." Simpson's paradox as the sharpest demonstration that the same data supports opposite causal stories.
   - Historical *why*: from Hume's problem of causation through Fisher's randomization, Wright's path analysis, to Rubin and Pearl — the long road to a *formal* definition of cause.
3. **Assumes:** *(this track)* none — entry point. *(cross-track)* the idea of correlation/association [Probability foundations; Regression REGR-0].
4. **Sets up:** CAUS-1 (formalizing the missing piece), CAUS-2 (the notation), CAUS-6 (each association source gets a graph).
5. **Depth:** short–medium (~10–14). Motivational; the one article that may lean on stories over derivation.

### CAUS-1 — The Fundamental Problem of Causal Inference
1. **The one question:** Why is a causal effect, for any single unit, *fundamentally unobservable* — and what does that force us to do?
2. **Scope / inside:**
   - The counterfactual framing: each unit has an outcome-if-treated and an outcome-if-untreated; the effect is their difference; we **only ever see one** of the two. Stated as Holland's "fundamental problem."
   - Why this makes causal inference a **missing-data problem**, not a measurement problem — no instrument, no sample size, fixes it for an individual.
   - The escape hatch: we abandon individual effects and target *averages over a population*, which *are* recoverable under assumptions — the whole rest of the track lives in this move.
3. **Assumes:** *(this track)* CAUS-0. *(cross-track)* expectation as a population average [Probability foundations].
4. **Sets up:** CAUS-2 (defines the averages precisely), the entire identification program.
5. **Depth:** short–medium (~10–14).

### CAUS-2 — Potential Outcomes: the Rubin Causal Model (ATE, ATT)
1. **The one question:** How do we write a causal effect as a mathematical object, and what *exactly* are the average effects we can hope to estimate?
2. **Scope / inside:**
   - Potential outcomes `Y_i(1), Y_i(0)`; the observed outcome `Y_i = T_i·Y_i(1) + (1−T_i)·Y_i(0)` (the "consistency" / observation equation) derived.
   - The estimands defined precisely: **ATE** `E[Y(1)−Y(0)]`, **ATT** `E[Y(1)−Y(0) | T=1]`, ATC, CATE — and why they can genuinely differ (effect heterogeneity).
   - **Ignorability / unconfoundedness** `(Y(1), Y(0)) ⊥ T | X` stated as *the* assumption that turns a comparison of observed groups into a causal contrast — derived to show how it collapses the missing-data problem.
   - The naive difference-in-means decomposed into **causal effect + selection bias**, in full, so the reader sees exactly what confounding adds.
3. **Assumes:** *(this track)* CAUS-1. *(cross-track)* conditional expectation `E[Y|X]`, conditional independence [Probability foundations].
4. **Sets up:** CAUS-3 (the assumptions that make `Y(t)` well-defined), CAUS-6 (backdoor = ignorability), CAUS-8–CAUS-12 (all adjustment estimators target these estimands).
5. **Depth:** deep (~18–24). **Split seam:** cut after the estimand definitions into *CAUS-2a "Potential Outcomes and the Estimands"* and *CAUS-2b "Ignorability and the Selection-Bias Decomposition,"* at the boundary where the assumption enters.

### CAUS-3 — SUTVA and Positivity: the Fine Print That Makes "an Effect" Well-Defined
1. **The one question:** What hidden assumptions does writing `Y_i(1)` already smuggle in, and when do they break?
2. **Scope / inside:**
   - **SUTVA** unpacked into its two halves: *no interference* (one unit's treatment doesn't change another's outcome — derived counterexamples: vaccines/herd immunity, market equilibrium, network spillover) and *consistency / no hidden versions of treatment* ("which dose? which surgeon?").
   - **Positivity / overlap** `0 < P(T=1|X) < 1`: why a covariate stratum with no treated (or no control) units makes the effect *unidentifiable there*, not just imprecise — derived from CAUS-2's conditioning.
   - Honest edge cases: interference under network/marketplace data (the boundary where the whole potential-outcomes setup needs extending), and positivity violations from high-dimensional `X`.
3. **Assumes:** *(this track)* CAUS-2. *(cross-track)* none new.
4. **Sets up:** CAUS-9/CAUS-11 (positivity is exactly what extreme propensity scores violate), CAUS-7 (RCTs guarantee positivity by design).
5. **Depth:** medium (~12–16).

---

## B. The Graph Language

### CAUS-4 — Causal DAGs and the do-Operator
1. **The one question:** How do we draw a set of causal assumptions as a picture, and what does "intervening" mean on that picture?
2. **Scope / inside:**
   - Directed acyclic graphs as encodings of causal structure: nodes = variables, arrows = direct causes; the **causal Markov condition** (a variable is independent of its non-descendants given its parents) stated and motivated.
   - The **do-operator** `P(Y | do(X=x))` defined as graph surgery — delete the arrows *into* `X`, then read off — contrasted line by line with conditioning `P(Y | X=x)`. This is the formal "set vs. see" distinction CAUS-0 promised.
   - Structural causal models (the equations behind the graph) sketched as the generator of both the graph and the potential outcomes — the bridge that makes CAUS-2 and this article the same theory.
3. **Assumes:** *(this track)* CAUS-2 (so the do-operator can be tied to potential outcomes). *(cross-track)* joint distributions and factorization, conditional independence [Probability foundations]; directed graphs / DAG basics (built inline — it's above no floor, just unfamiliar).
4. **Sets up:** CAUS-5 (reading independences), CAUS-6 (the backdoor criterion is a do-operator theorem).
5. **Depth:** deep (~18–24). **Split seam:** cut after the Markov condition into *CAUS-4a "Causal DAGs and Structural Equations"* and *CAUS-4b "The do-Operator and Intervention,"* at the see-vs-set boundary.

### CAUS-5 — d-Separation: Reading Independence off a Graph
1. **The one question:** Given a DAG, how do we *mechanically* decide whether two variables are independent — possibly after conditioning on others?
2. **Scope / inside:**
   - The three building blocks of every path — **chain** (`A→B→C`), **fork** (`A←B→C`), **collider** (`A→B←C`) — and what flows or blocks through each, derived from the factorization in CAUS-4.
   - The **d-separation** rule assembled from the three blocks: a path is blocked if it contains a non-collider you condition on, or a collider you *don't* condition on (and whose descendants you don't condition on either). Worked on multi-path graphs.
   - The payoff: d-separation in the graph ⇒ conditional independence in the distribution — the engine that lets a drawing make testable and identifying claims.
3. **Assumes:** *(this track)* CAUS-4. *(cross-track)* conditional independence [Probability foundations].
4. **Sets up:** CAUS-6 (backdoor and collider bias are both d-separation read-offs); gives the reader the tool to *check their own DAG*.
5. **Depth:** deep (~18–22). **Split seam:** the three path-types can spin out as *CAUS-5a "Chains, Forks, and Colliders"* if the full d-separation assembly crowds the worked graphs.

### CAUS-6 — Confounders, Colliders, and the Backdoor Criterion (with Selection Bias)
1. **The one question:** Which variables *must* we adjust for to identify a causal effect — and which ones will *create* bias if we adjust for them?
2. **Scope / inside:**
   - **Confounding** as an open backdoor path (a fork `T ← Z → Y`); the **backdoor criterion** stated and shown to license the **adjustment formula** `P(Y|do(T)) = Σ_z P(Y|T,z)P(z)` — derived from the do-operator (CAUS-4) plus d-separation (CAUS-5). This is the graph-side twin of CAUS-2's ignorability: **backdoor adjustment ⇔ conditioning on `X` makes treatment ignorable.**
   - **Colliders and the danger of over-conditioning**: why controlling for a collider (or its descendant) *opens* a spurious path — the formal account of **selection bias**, M-bias, and "controlling for everything is wrong." Honest examples: collider bias in case-control/hospital data, the "birth-weight paradox," sample-selection artifacts.
   - The mediator trap: why you must *not* adjust for a variable on the causal pathway if you want the total effect (preview of direct/indirect effects, kept brief).
3. **Assumes:** *(this track)* CAUS-2 (ignorability), CAUS-4 (do-operator), CAUS-5 (d-separation). *(cross-track)* none new.
4. **Sets up:** CAUS-8–CAUS-12 (the entire adjustment family *is* backdoor adjustment, executed by different machinery); CAUS-13 (IV is what you reach for when you *can't* close the back door).
5. **Depth:** deep (~22–28). **Split seam:** cut after the backdoor criterion into *CAUS-6a "Confounding and the Backdoor Criterion"* and *CAUS-6b "Colliders, Selection Bias, and Over-Adjustment,"* at the confounder/collider boundary — they are the two opposite mistakes and each deserves room.

---

## C. The Gold Standard

### CAUS-7 — Randomized Experiments: Why an RCT Identifies the ATE for Free
1. **The one question:** Why does physically randomizing the treatment dissolve confounding, and what *exactly* do we get to assume that observational data never lets us?
2. **Scope / inside:**
   - Randomization makes `T ⊥ (Y(1), Y(0))` *by construction* (no `X` needed) — derived — so the naive difference in means is unbiased for the ATE; the selection-bias term from CAUS-2 is forced to zero. Guarantees positivity (CAUS-3) too.
   - Inference for the experimental effect: Neyman's repeated-sampling variance and Fisher's randomization/permutation test — *linked* to the Inference track (permutation INFR-E3, CIs INFR-C1), not re-derived; covariate adjustment in an RCT for *precision* (links to Regression) vs. for bias.
   - The honest boundary: noncompliance, attrition, blinding failures, external validity, and ethics/feasibility — the reasons we ever leave the gold standard for the observational methods that fill the rest of the track. ITT vs. per-protocol previewed (sets up IV).
3. **Assumes:** *(this track)* CAUS-2, CAUS-3. *(cross-track)* hypothesis-test logic and the permutation test [Statistical Inference INFR-D1, INFR-E3]; sampling-distribution/standard-error machinery [Statistical Inference INFR-A1]; randomized assignment as i.i.d./Bernoulli draws [Probability foundations].
4. **Sets up:** the benchmark every later method is measured against ("does this recover the number a randomized experiment would have gotten?"); CAUS-13 (noncompliance → IV).
5. **Depth:** deep (~18–24). **Split seam:** cut into *CAUS-7a "Why Randomization Identifies the ATE"* and *CAUS-7b "Analyzing an Experiment: Neyman, Fisher, and Covariate Adjustment,"* at the identification/estimation boundary.

---

## D. Adjustment Under Ignorability

*All four estimators in this section target the same backdoor-adjusted estimand (CAUS-6) under the same
ignorability assumption (CAUS-2); they differ only in **how** they implement the adjustment. CAUS-12 fuses
the two main families.*

### CAUS-8 — Regression Adjustment: the Backdoor Formula via a Model
1. **The one question:** How does "just put the confounders in the regression" actually implement backdoor adjustment, and when does the coefficient on treatment *mean* the causal effect?
2. **Scope / inside:**
   - The adjustment formula (CAUS-6) realized by modeling `E[Y | T, X]` and averaging over the covariate distribution — the **g-formula / standardization**; why the treatment coefficient in `Y ~ T + X` estimates the ATE *only* under correct functional form + ignorability + no effect modification (or with interactions, by averaging). Derived, not asserted.
   - The functional-form trap: bias from a mis-specified outcome model even when the backdoor set is right; why "controlling for `X`" is not magic. Honest contrast with the design-based methods that follow.
   - **Reliance on the Regression track:** OLS/GLM fitting, coefficient interpretation, and standard errors are *consumed* (links to REGR-5, REGR-9, REGR-17); the new content is purely the causal *reading* of the fitted model.
3. **Assumes:** *(this track)* CAUS-2, CAUS-6. *(cross-track)* multiple regression and coefficient interpretation [Regression REGR-5, REGR-8]; GLM for non-continuous outcomes [Regression REGR-17–REGR-18]; standard errors / CIs [Statistical Inference INFR-C3].
4. **Sets up:** CAUS-12 (regression adjustment is the "outcome model" half of doubly-robust); contrast class for CAUS-9–CAUS-11.
5. **Depth:** medium–deep (~16–20).

### CAUS-9 — The Propensity Score: Collapsing Confounders to One Number
1. **The one question:** Can we summarize *all* the confounders in a single number, and why does adjusting for that one number suffice?
2. **Scope / inside:**
   - The propensity score `e(X) = P(T=1 | X)` defined; **Rosenbaum–Rubin's balancing theorem** proved: `T ⊥ X | e(X)`, so the score is a balancing score and conditioning on it suffices for ignorability — the full derivation, the central result of the article.
   - Estimating `e(X)` (usually logistic regression — *linked* to Regression REGR-17, not re-derived); checking **balance** and **overlap/common support** (positivity from CAUS-3 made operational); the difference between the *true* and *estimated* score.
   - Honest boundary: the score is only as good as the covariates in it (no help against unmeasured confounding); model dependence; why a high-dimensional or near-deterministic score signals a positivity problem.
3. **Assumes:** *(this track)* CAUS-2, CAUS-3, CAUS-6. *(cross-track)* logistic regression as the fitted probability model [Regression REGR-17]; conditional independence [Probability foundations].
4. **Sets up:** CAUS-10 (matching on `e(X)`), CAUS-11 (weighting by `e(X)`), CAUS-12 (the score is the "treatment model" half of doubly-robust).
5. **Depth:** deep (~18–22). **Split seam:** cut after the balancing theorem into *CAUS-9a "The Propensity Score and the Balancing Theorem"* and *CAUS-9b "Estimating, Checking, and the Limits of the Score,"* at the theory/practice boundary.

### CAUS-10 — Matching: Building the Counterfactual by Comparison
1. **The one question:** How do we estimate an effect by *pairing* each treated unit with a comparable untreated one, and what does "comparable" cost us?
2. **Scope / inside:**
   - Matching as a direct attack on CAUS-1's missing counterfactual: impute the unseen `Y(0)` for a treated unit from its match. Exact matching → the curse of dimensionality → **distance matching** (Mahalanobis) → **propensity-score matching** (payoff from CAUS-9).
   - Design choices and their bias/variance consequences: nearest-neighbor vs. caliper, with/without replacement, k:1 ratios, trimming off-support units; why matching most naturally targets the **ATT** (CAUS-2). Assessing balance *after* matching.
   - Honest edge: matching discards data, the bias from inexact matches, and the well-documented pathologies of naive propensity-score matching (the "PSM increases imbalance" critique) — when to prefer weighting or a coarsened/optimal match instead.
3. **Assumes:** *(this track)* CAUS-2 (ATT), CAUS-3 (overlap), CAUS-9 (the score). *(cross-track)* distance metrics / Mahalanobis distance [Geometry of Data]; standard errors via the bootstrap [Statistical Inference INFR-E1].
4. **Sets up:** CAUS-11 (weighting as "soft matching"); CAUS-16 (Rosenbaum's sensitivity analysis was built for matched designs).
5. **Depth:** deep (~18–22).

### CAUS-11 — Inverse-Probability Weighting: Reweighting to a Pseudo-Population
1. **The one question:** Instead of matching units, can we *reweight* them so the treated and control groups look like the same population — and why does weighting by `1/e(X)` work?
2. **Scope / inside:**
   - The **IPW (Horvitz–Thompson) estimator** derived: weighting treated units by `1/e(X)` and controls by `1/(1−e(X))` recreates a population where treatment is independent of `X`; the proof that `E[ T·Y / e(X) ] = E[Y(1)]` — every step. The **stabilized** weights and why they tame variance.
   - The direct, visible link to positivity (CAUS-3): a propensity near 0 or 1 produces an exploding weight — *the* failure mode, made concrete; trimming and stabilization as the honest, imperfect fixes.
   - Why IPW is the bridge to causal effects of *time-varying* treatments (marginal structural models, named and motivated as the place this method becomes indispensable — left to a future extension, not built).
3. **Assumes:** *(this track)* CAUS-2, CAUS-3 (positivity is central here), CAUS-9 (the score). *(cross-track)* expectation of a transformed random variable, the law of total expectation [Probability foundations]; sandwich/bootstrap standard errors [Statistical Inference INFR-E1; Regression REGR-11].
4. **Sets up:** CAUS-12 (IPW is the "treatment model" half of AIPW).
5. **Depth:** deep (~18–24). **Split seam:** cut after the unbiasedness proof into *CAUS-11a "Inverse-Probability Weighting and Why It Works"* and *CAUS-11b "Extreme Weights, Stabilization, and Trimming,"* at the estimator/diagnostics boundary.

### CAUS-12 — Doubly-Robust Estimation: Two Chances to Be Right
1. **The one question:** Regression adjustment needs a correct *outcome* model; IPW needs a correct *treatment* model — can we combine them so that getting **either one** right is enough?
2. **Scope / inside:**
   - The **augmented IPW (AIPW)** estimator built explicitly from CAUS-8's outcome model and CAUS-11's weights; the **double-robustness** property proved: the estimator is consistent if *either* the propensity model *or* the outcome model is correct (work the two cases separately so the reader sees each rescue).
   - The bias-cancellation intuition and the connection to influence functions / semiparametric efficiency (introduced gently, to the floor); why DR is the modern default and the gateway to ML-based estimation (TMLE, double/debiased ML — named, motivated, deferred).
   - Honest boundary: double robustness is not *free* — both models wrong, or near-positivity-violations, still sink it; finite-sample behavior can be worse than a single good model.
3. **Assumes:** *(this track)* CAUS-8, CAUS-9, CAUS-11. *(cross-track)* the outcome model is consumed from [Regression REGR-5/REGR-17]; the weighting and SEs link to [Statistical Inference INFR-E1].
4. **Sets up:** the terminal node of the ignorability branch; the modern hand-off to ML-for-causal-inference (future track).
5. **Depth:** deep (~20–26). **Split seam:** cut after the double-robustness proof into *CAUS-12a "The AIPW Estimator and Double Robustness"* and *CAUS-12b "Efficiency and the Road to ML-Based Causal Estimation."*

---

## E. When Ignorability Fails — Designs Without Measured Confounding

*The previous section assumed we measured enough to close every back door. This section is for when
we **cannot** — when an unmeasured confounder is present and no amount of adjustment fixes it. Each
method finds a different structural feature that breaks confounding without measuring it.*

### CAUS-13 — Instrumental Variables: a Back Door You Can't Close, So Find a Valve
1. **The one question:** If an unmeasured confounder makes treatment endogenous, how can a *third* variable that nudges treatment — but affects the outcome only through it — still recover a causal effect?
2. **Scope / inside:**
   - The IV conditions stated on the DAG (CAUS-4): **relevance** (`Z→T`), **exclusion** (`Z` affects `Y` only via `T`), **independence/ignorable instrument**; why these together identify an effect despite an open `T↔Y` confounding path. The **Wald estimator** `ATE = Cov(Z,Y)/Cov(Z,T)` derived; **two-stage least squares** as its regression realization (links to Regression REGR-5, not re-derived).
   - The **LATE** theorem (Imbens–Angrist): with a binary instrument, IV estimates the effect *on compliers only* — derived via the principal-strata (always-takers / never-takers / compliers / defiers) decomposition under monotonicity. Why LATE ≠ ATE, and who the compliers are.
   - Honest failure modes: **weak instruments** (small `Cov(Z,T)` → exploded variance and bias toward OLS), violations of exclusion (the assumption you can *never* test), and the strong external-validity caveat of a complier-only effect. Real instruments — draft lottery, distance-to-hospital, judge leniency — and why each is defensible or not.
3. **Assumes:** *(this track)* CAUS-2, CAUS-6 (the open back door it routes around), CAUS-7 (noncompliance/ITT motivates it). *(cross-track)* covariance and its algebra [Probability foundations]; OLS/2SLS as the fitting engine [Regression REGR-5]; weak-instrument inference links to [Statistical Inference].
4. **Sets up:** the "natural experiment" mindset shared with CAUS-14–CAUS-15; CAUS-16 (exclusion is exactly what sensitivity analysis probes).
5. **Depth:** deep (~22–28). **Split seam:** cut after the Wald/2SLS identification into *CAUS-13a "Instrumental Variables and the Wald Estimator"* and *CAUS-13b "LATE, Compliers, and Weak Instruments,"* at the homogeneous-effect/heterogeneous-effect boundary.

### CAUS-14 — Difference-in-Differences: Parallel Trends as the Identifying Bet
1. **The one question:** When a treatment hits one group at a known time, how does comparing *changes* over time — rather than levels — cancel out fixed unmeasured confounders?
2. **Scope / inside:**
   - The 2×2 DiD estimator derived as a double difference (treated-vs-control × after-vs-before); the proof that it differences away any *time-invariant* group confounder — the precise sense in which it beats a cross-sectional comparison. The **parallel-trends** assumption stated as the *untestable* identifying bet, and what the counterfactual trend means in potential-outcomes terms (CAUS-2).
   - The two-way fixed-effects regression realization (links to Regression REGR-8's categorical/interaction machinery); checking pre-treatment trends as supporting (not proving) evidence; the event-study generalization sketched.
   - Honest boundary: when parallel trends is implausible (differential shocks, **Ashenfelter's dip**, treatment timing that varies across units → the recently-documented two-way-FE bias with staggered adoption); placebo tests as the practitioner's discipline.
3. **Assumes:** *(this track)* CAUS-2, CAUS-6. *(cross-track)* fixed-effects / interaction terms in regression [Regression REGR-8]; panel-data standard errors / clustering links to [Regression REGR-11; Statistical Inference].
4. **Sets up:** the panel/natural-experiment toolkit; CAUS-17 (where DiD sits in the design decision tree).
5. **Depth:** deep (~18–24).

### CAUS-15 — Regression Discontinuity: Local Randomization at a Threshold
1. **The one question:** When treatment is assigned by a sharp cutoff on a running variable, why are units *just* above and *just* below the cutoff effectively randomized — and what effect does that identify?
2. **Scope / inside:**
   - **Sharp RD**: treatment is a deterministic step at the cutoff `c`; the effect is identified as the *jump in `E[Y | running variable]`* at `c`, under the continuity assumption that all confounders vary smoothly through `c` — derived, with the potential-outcomes reading (a **local** effect right at the cutoff). **Fuzzy RD** as RD-meets-IV (the jump in treatment *probability* as the first stage → links to CAUS-13).
   - Estimation as **local polynomial regression** at the boundary — an explicit, deliberate payoff from the Regression track's local-regression articles (REGR-23–REGR-24), with bandwidth selection (REGR-25) as the bias-variance dial; the boundary-bias problem from REGR-23 reappearing exactly here.
   - Honest boundary: manipulation of the running variable (the McCrary density test), bandwidth sensitivity, the *local*-effect external-validity limit, and why RD is high-credibility but low-generality.
3. **Assumes:** *(this track)* CAUS-2, CAUS-13 (for the fuzzy case). *(cross-track)* local/kernel regression and bandwidth selection [Regression REGR-23–REGR-25]; continuity/limits of a function [Calc-1 floor].
4. **Sets up:** CAUS-17; rounds out the "exploit a structural feature" trio (IV/DiD/RD).
5. **Depth:** deep (~18–24). **Split seam:** cut into *CAUS-15a "Sharp Regression Discontinuity"* and *CAUS-15b "Fuzzy RD and Local-Polynomial Estimation,"* at the sharp/fuzzy boundary.

---

## F. Honesty and Judgment

### CAUS-16 — Sensitivity Analysis: How Wrong Could an Unmeasured Confounder Make Us?
1. **The one question:** Every observational method rests on an *untestable* assumption — so how do we quantify how badly a hidden confounder (or a violated exclusion) could be distorting our answer?
2. **Scope / inside:**
   - The premise: ignorability (CAUS-2) and exclusion (CAUS-13) can never be verified from data, so the honest deliverable is not a point estimate but **how fragile that estimate is**. Reframes the whole observational program as "assume, then stress-test."
   - The core tools, derived to the floor: **Rosenbaum bounds** for matched designs (how large a hidden bias `Γ` would overturn significance), the **E-value** (the minimum confounder–exposure and confounder–outcome association needed to explain away the effect), and the simpler omitted-variable-bias / confounding-function reasoning. Worked on a real observational estimate from an earlier article.
   - The interview-grade framing: how to *report* a causal estimate responsibly — "this effect is robust unless an unmeasured confounder at least this strong exists, which we judge (im)plausible because …".
3. **Assumes:** *(this track)* CAUS-2, CAUS-6, CAUS-9/CAUS-10/CAUS-11 (the estimates being stressed), CAUS-13 (exclusion). *(cross-track)* p-values / significance [Statistical Inference INFR-D1]; odds/risk ratios [Regression REGR-17].
4. **Sets up:** CAUS-17 (sensitivity is part of every design's honest write-up).
5. **Depth:** deep (~18–22). **Split seam:** cut into *CAUS-16a "Sensitivity Analysis: Rosenbaum Bounds"* and *CAUS-16b "The E-Value and Reporting a Causal Estimate Honestly."*

### CAUS-17 — Putting It Together: Choosing a Causal Design
1. **The one question:** Faced with a real "does `X` cause `Y`?" question and a real dataset, how do we decide *which* method is even applicable — and what to do when none cleanly is?
2. **Scope / inside:**
   - The decision tree, assembled from the whole track: Can you randomize? (→ CAUS-7). If not, can you measure and close all back doors? (→ CAUS-8–CAUS-12, choosing among regression/PS/matching/IPW/DR by overlap, dimensionality, and estimand). If not, is there an instrument / a policy threshold / a natural before-after with a control group? (→ CAUS-13/CAUS-15/CAUS-14). If none, what's the *honest* conclusion (→ CAUS-16: bound it, don't pretend).
   - Three end-to-end case studies carried across multiple methods on the *same* question, showing the answers converge or diverge and *why* — the capstone honest-comparison the constitution demands.
   - The estimand-first discipline: name the population and the contrast (ATE vs ATT vs LATE vs local-at-cutoff) *before* choosing a method, because the method silently chooses the estimand.
3. **Assumes:** *(this track)* all of CAUS-0–CAUS-16.
4. **Sets up:** Terminal node. Hands off to future tracks: **ML for causal inference** (double ML, causal forests, TMLE — seeded at CAUS-12), **mediation / direct & indirect effects** (seeded at CAUS-6), **time-varying treatments / marginal structural models** (seeded at CAUS-11), and **synthetic control** (seeded at CAUS-14).
5. **Depth:** medium–deep (~16–20). Synthesis and judgment; light on new derivation, heavy on applicability calls.

---

## CROSS-TRACK PREREQUISITE Articles (owned by OTHER tracks)

Pulled in at the points noted. Causal Inference does **not** build these; they are named so the
prerequisite chain (§1.4) is explicit.

**From Probability foundations:**
- **Conditional expectation `E[Y|X]` and conditional independence** — needed at **CAUS-2** (and pervasively; this is the language of ignorability).
- **Joint distributions, factorization, the law of total expectation** — needed at **CAUS-4, CAUS-11**.
- **Expectation of a transformed random variable** — needed at **CAUS-11** (the IPW unbiasedness proof).
- **Covariance and its algebra** — needed at **CAUS-13** (the Wald estimator).
- **Bernoulli/binomial assignment, i.i.d. sampling** — needed at **CAUS-7**.

**From the Regression track:**
- **Multiple regression, coefficient interpretation ("holding others fixed"), categorical & interaction terms** — needed at **CAUS-8, CAUS-14**.
- **Logistic regression as a fitted probability model** — needed at **CAUS-9** (propensity score), **CAUS-16** (odds ratios).
- **GLMs** for non-continuous outcomes — needed at **CAUS-8**.
- **OLS / two-stage least squares as a fitting engine** — needed at **CAUS-13**.
- **Robust / clustered standard errors (sandwich)** — needed at **CAUS-11, CAUS-14**.
- **Local / kernel regression and bandwidth selection (REGR-23–REGR-25)** — needed at **CAUS-15** (RD is local polynomial regression at a boundary). *This is the track's deepest reuse of Regression and a deliberate payoff.*

**From the Statistical Inference track:**
- **Sampling distribution / standard error of an estimator (INFR-A1)** — needed wherever an estimate gets a CI (**CAUS-7 onward**).
- **Hypothesis-test logic and p-values (INFR-D1)** — needed at **CAUS-7, CAUS-16**.
- **The permutation/randomization test (INFR-E3)** — needed at **CAUS-7** (Fisher's exact test of the sharp null).
- **The bootstrap (INFR-E1)** — needed at **CAUS-10, CAUS-11, CAUS-12** (standard errors with no closed form).
- **Confidence-interval construction (INFR-C1, INFR-C3)** — needed at **CAUS-8 onward**.

**From the Geometry of Data track:**
- **Distance metrics / Mahalanobis distance** — needed at **CAUS-10** (matching).

---

## Overlaps with other tracks — ownership calls

Recommendation: **Causal Inference owns the *causal question and its identifying assumptions*;
every other track owns the *machinery* and is *linked*, never re-derived here.**

| Shared topic | **Owner** | Rationale |
|---|---|---|
| **Potential outcomes, do-operator, DAGs, d-separation, identification assumptions** | **Causal Inference** | The defining content of the track; exists nowhere else in the series. |
| **OLS / GLM / 2SLS fitting and coefficient mechanics** | **Regression** | This track *reads* a fitted coefficient causally (CAUS-8, CAUS-13); it never re-derives the fit. |
| **Local-polynomial / kernel regression + bandwidth** | **Regression (REGR-23–REGR-25)** | RD (CAUS-15) *applies* it at a boundary; Regression owns the estimator and its bias-variance theory. |
| **Logistic regression (the propensity model itself)** | **Regression (REGR-17)** | Causal Inference owns the propensity score's *causal role and balancing theorem* (CAUS-9); the logistic fit is Regression's. |
| **Sampling distributions, standard errors, bootstrap, permutation, p-values, CIs** | **Statistical Inference** | All uncertainty quantification for causal estimates links back; this track adds the causal *target*, not new inference theory. |
| **MAP / regularization** (if a propensity or outcome model is regularized) | **Regression / Inference** | Consumed as-is; relevant only as the ML-causal hand-off at CAUS-12. |
| **Distance metrics for matching** | **Geometry of Data** | Mahalanobis distance is owned there; CAUS-10 uses it. |
| **Simpson's paradox / confounding *intuition*** | **shared with Probability & Regression, owned here for the *causal* resolution** | Other tracks may show the arithmetic; this track owns *why* it resolves one way or the other (it's a causal, not statistical, question — CAUS-0). |

**Versus the tracks being designed concurrently:**
- **Probability Foundations** — supplies conditional independence, joint factorization, expectation algebra (the language CAUS-2–CAUS-5 are written *in*). Pure consumer relationship; no overlap, only dependency.
- **Geometry of Data** — supplies Mahalanobis distance for matching (CAUS-10). Minor, clean dependency.
- **Optimization** — no direct dependency in the core track; surfaces only if the CAUS-12 ML-causal hand-off (double ML) is later built, where it would consume Optimization for the nuisance-model fitting.
- **Classification** — overlaps **only** at the propensity score: a propensity model *is* a probabilistic classifier. Recommendation: **Classification owns the classifier; Causal Inference owns its use as a balancing score (CAUS-9).** The two should cross-link, not duplicate. Classification's calibration content is directly relevant to good propensity estimates and should be referenced from CAUS-9.
- **Unsupervised Learning** — no core overlap. (Coarsened-exact matching's binning and any clustering-for-balance ideas would link out to it if pursued, but they are not in this roadmap.)

**One-line ownership rule:** *the cause and the assumptions that license claiming it are this
track's; the fitting, the distance, and the uncertainty are borrowed and linked.*

---

### Summary of decisions
- **Name:** **Causal Inference** — moving from correlation to causation.
- **Aim:** state a causal estimand, draw the DAG that encodes the assumptions, decide whether the
  effect is identifiable, choose the estimator the design supports, and report honestly how fragile
  the answer is to unmeasured confounding.
- **Boundary:** this track owns the causal *target and its identifying assumptions*; Regression,
  Inference, Geometry, and Classification own the *machinery* and are linked, never re-derived.
- **18 articles** in six movements (A Question & Language → B Graphs → C Gold Standard →
  D Adjustment under ignorability → E Designs when ignorability fails → F Honesty & judgment),
  with **13 named split seams**, each inch-wide and building on the last.
