# Core Sample — Track Roadmap: **Statistical Inference**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

## PART 0 — Naming, Aim, and the Boundary with Regression

### Decision: name it **Statistical Inference** (not "Statistical Modeling").

**Why this name, not "Statistical Modeling."** The two aims are genuinely different. *Modeling* is the act of **writing down a probabilistic story for the data** — picking a likelihood, a model family, latent structure, and then choosing among such stories. *Inference* is the act of **reasoning backward from observed data to claims about unknowns, with a calibrated statement of uncertainty.** This track's charter question — *"what can we conclude from data, and how sure are we"* — is the inference question, word for word. Estimators, sampling distributions, confidence intervals, hypothesis tests, and the bootstrap are all *machinery for quantifying and reasoning about uncertainty in a conclusion* — they are not machinery for *specifying* a model.

There is a second, decisive reason: **the Regression track already owns most of the modeling surface.** Linear models, GLMs, regularization, and nonparametric regression are precisely "specifying probabilistic models of data and selecting among them." Naming this track *Inference* draws a clean line: **Regression specifies and fits models; Inference says how sure we are about what comes out, and tests claims against data.**

### Charter (one paragraph)

> **Statistical Inference** is the track that turns data into *defensible conclusions with honest uncertainty*. It assumes someone has already chosen a probabilistic description of the data (often in the Regression track, or built here for the canonical one-and-two-sample cases) and asks: given a finite, noisy sample, what can we say about the unknown quantity that generated it, and how confident are we entitled to be? It builds the estimator as the central object — its sampling distribution, its bias and variance, the information it extracts — and from that foundation erects the three pillars of frequentist uncertainty (point estimation, interval estimation, hypothesis testing), the computational engine that frees them from analytic tractability (the bootstrap and permutation), and the Bayesian alternative that answers the same questions with a different definition of probability. The reader finishes able to *choose an estimator, state its uncertainty correctly, test a claim, know exactly what a p-value and a confidence interval do and do not mean, and judge when each tool is the right one.*

### The boundary with the Regression track (explicit contract)

| Concern | Owned by **Inference** (this track) | Owned by **Regression** |
|---|---|---|
| The likelihood as an *object* and **MLE as a general estimation principle** | ✅ owns the general theory | consumes it for fitting |
| Specifying a particular **model family** (linear, GLM, splines) | — | ✅ |
| **Sampling distribution of an estimator** in general | ✅ | consumes for β̂ |
| **Bias / variance / consistency / efficiency** of estimators in general | ✅ | consumes |
| **Confidence intervals & hypothesis tests as concepts** + the t/F/χ² test machinery | ✅ | consumes (e.g. CI on a coefficient) |
| **Regularization as estimation / model selection** (ridge, lasso, AIC/BIC *for choosing predictors*) | — | ✅ |
| **The bootstrap** as a general uncertainty engine | ✅ | consumes for CI on predictions |
| Goodness-of-fit / **model criticism for a fitted regression** | shares (test theory here, residual diagnostics there) | residual diagnostics there |

The rule of thumb: **if the deliverable is "an estimate or a model," it's Regression's job to produce it; if the deliverable is "a quantified statement of how sure we are, or a test of a claim," it's Inference's job."** The MLE and the sampling distribution are the shared spine, and **Inference owns them** so Regression can link rather than re-derive.

---

## The Roadmap

The track has five movements:

- **A. Foundations of estimation** (what an estimator is; sampling distributions; the two big theorems)
- **B. The likelihood spine** (likelihood, MLE, Fisher information, asymptotics) — the engine room
- **C. Interval estimation** (confidence intervals, done right and done honestly)
- **D. Hypothesis testing** (the whole apparatus, including what p-values do not mean)
- **E. Computational & alternative inference** (bootstrap, permutation, and the Bayesian fork)

---

### A. Foundations of Estimation

#### INFR-A1. **The Estimator as a Random Variable**
1. **Question it answers:** What exactly *is* an estimator, and why is the number it produces itself a draw from a distribution?
2. **Scope / inside:**
   - The population-parameter vs. sample-statistic distinction; estimator as a *function of the sample*, hence a random variable.
   - The **sampling distribution** defined from first principles; standard error as its standard deviation.
   - Worked construction of the sampling distribution of the sample mean and sample proportion by simulation *and* by exact argument.
   - Bias, variance, and **mean squared error** decomposition `MSE = bias² + variance` derived in full.
3. **Assumes:** *(this track)* none — entry point. *(cross-track)* random variables, expectation & variance, independence [Probability foundations]; i.i.d. sampling [Probability foundations].
4. **Sets up:** INFR-A2 (the two limit theorems), INFR-B1 (likelihood), INFR-C1 (CIs need a sampling distribution).
5. **Depth:** medium (~12–16).

#### INFR-A2. **Two Theorems That Make Statistics Possible: LLN and the CLT**
1. **Question it answers:** Why does averaging more data home in on the truth, and why is the bell curve the universal shape of estimation error?
2. **Scope / inside:**
   - **Law of Large Numbers** (weak form) stated and proved via Chebyshev; what "converges in probability" means, built from scratch.
   - **Central Limit Theorem** stated precisely; intuition via convolution/MGF sketch; the `√n` scaling derived.
   - Why the CLT is what makes the standard error usable; finite-sample caveats (skew, heavy tails, the "n≥30" myth dismantled honestly).
   - **Edge-of-applicability example:** a heavy-tailed (e.g. Cauchy-like / Pareto) sample where the CLT bites slowly or the mean is the wrong target.
3. **Assumes:** *(this track)* INFR-A1. *(cross-track)* expectation/variance, Chebyshev's inequality, moment generating functions or characteristic-function sketch [Probability foundations]; convergence concepts [Probability foundations].
4. **Sets up:** INFR-C1/INFR-C2 (CLT-based intervals), INFR-B4 (asymptotic normality of the MLE reuses CLT machinery), INFR-D2 (test statistics' null distributions).
5. **Depth:** deep (~20–26). **Split seam if needed:** cut after the LLN into *INFR-A2a "The Law of Large Numbers"* and *INFR-A2b "The Central Limit Theorem,"* at the boundary between the two convergence modes.

### B. The Likelihood Spine

#### INFR-B1. **The Likelihood: Reading Probability Backwards**
1. **Question it answers:** Once we have a model, how do we measure how well a particular parameter value explains the data we actually saw?
2. **Scope / inside:**
   - The flip from "probability of data given parameter" to **likelihood as a function of the parameter given fixed data**; why it is *not* a probability density over the parameter.
   - The **log-likelihood** and why we always work in logs (products → sums, numerical stability) — derived, not asserted.
   - Likelihoods for the canonical cases: Bernoulli/binomial, Normal (known and unknown variance), Poisson.
   - The score function `∂_θ log L` introduced as the slope whose root we will chase.
3. **Assumes:** *(this track)* INFR-A1. *(cross-track)* pmf/pdf, joint density of i.i.d. data, log/derivative rules [Probability foundations; Calc-1 floor].
4. **Sets up:** INFR-B2 (MLE maximizes this), INFR-B3 (Fisher information is its curvature), INFR-E4 (Bayesian posterior = likelihood × prior).
5. **Depth:** medium (~12–16).

#### INFR-B2. **Maximum Likelihood: The Parameter That Best Explains the Data**
1. **Question it answers:** How do we turn "this parameter explains the data well" into a single best estimate, and how do we actually compute it?
2. **Scope / inside:**
   - The **MLE** defined as the argmax of the log-likelihood; first-order condition (score = 0); checking the second-order condition.
   - Closed-form MLEs derived end-to-end: Normal `(μ̂, σ̂²)`, Bernoulli `p̂`, Poisson `λ̂`.
   - **Invariance** of the MLE under reparameterization, proved.
   - When there's no closed form: the link to numerical optimization (Newton / gradient ascent) — kept secondary, pointing to the Optimization track.
   - **Edge case:** a likelihood with no maximum / on a boundary / non-identifiable (e.g. the uniform `[0,θ]` where the score approach fails) to show the method's limits.
3. **Assumes:** *(this track)* INFR-B1. *(cross-track)* finding maxima via derivatives, multivariable critical points [Calc-1 floor + gradients from Geometry of Data / Optimization]; Newton's method / gradient ascent [Optimization].
4. **Sets up:** INFR-B3 & INFR-B4 (properties and uncertainty of the MLE), INFR-C3 (likelihood-based intervals), INFR-D3 (likelihood-ratio test), and is consumed by all of Regression.
5. **Depth:** deep (~18–24). **Split seam:** if numerical optimization grows, cut after the closed-form section into *INFR-B2a "Maximum Likelihood (closed-form)"* and *INFR-B2b "Computing the MLE When There's No Formula,"* at the score-equation/no-closed-form boundary.

#### INFR-B3. **Fisher Information: How Much a Sample Can Tell You**
1. **Question it answers:** How much information about a parameter does a single observation carry, and what is the best precision any estimator could hope for?
2. **Scope / inside:**
   - **Fisher information** defined two equivalent ways (variance of the score; negative expected curvature of the log-likelihood) — equivalence proved.
   - The **Cramér–Rao lower bound** derived; the meaning of an *efficient* estimator.
   - Information adds over i.i.d. data (`Iₙ = nI₁`), derived — the precise sense in which "more data = more information."
   - Worked information calculations for Normal, Bernoulli, Poisson.
3. **Assumes:** *(this track)* INFR-B1, INFR-B2. *(cross-track)* expectation, variance, differentiating under the integral (stated and motivated, not assumed) [Probability foundations]; second derivatives/curvature [Calc-1 floor].
4. **Sets up:** INFR-B4 (the asymptotic variance of the MLE *is* `1/I`), INFR-C3 (Wald intervals use it), INFR-D3 (the score test uses it).
5. **Depth:** medium–deep (~16–20).

#### INFR-B4. **Why Maximum Likelihood Works: Consistency, Efficiency, and Asymptotic Normality**
1. **Question it answers:** In what precise sense is the MLE a *good* estimator as the sample grows, and what is its sampling distribution?
2. **Scope / inside:**
   - **Consistency** of the MLE (the estimate converges to the truth) — argued via the LLN applied to the log-likelihood.
   - **Asymptotic normality:** `√n(θ̂−θ₀) → N(0, I₁⁻¹)` derived via Taylor-expanding the score and applying the CLT — every step shown.
   - **Asymptotic efficiency:** the MLE attains the Cramér–Rao bound in the limit.
   - The **delta method** for the distribution of a function of an estimator, derived.
   - **Edge of applicability:** where these guarantees fail — small `n`, boundary parameters, misspecified models — stated honestly.
3. **Assumes:** *(this track)* INFR-A2 (CLT), INFR-B2 (MLE), INFR-B3 (Fisher info). *(cross-track)* Taylor expansion [Calc-1 floor], convergence in distribution [Probability foundations].
4. **Sets up:** INFR-C3 (Wald CI), INFR-D3 (the trinity of asymptotic tests), and the asymptotic inference all of Regression relies on.
5. **Depth:** deep (~22–28). **Split seam:** cut after asymptotic normality into *INFR-B4a "Consistency & Asymptotic Normality of the MLE"* and *INFR-B4b "Efficiency and the Delta Method,"* at the point where the limiting distribution is established.

### C. Interval Estimation

#### INFR-C1. **Confidence Intervals: What "95% Confident" Actually Means**
1. **Question it answers:** What does a confidence interval really claim — and what does it emphatically *not* claim?
2. **Scope / inside:**
   - The **coverage** definition built carefully: the interval is random, the parameter is fixed; "95%" is a property of the *procedure*, not of one interval.
   - The **pivotal-quantity** method for constructing intervals, derived.
   - The canonical CLT-based interval for a mean (known variance) end-to-end.
   - The classic misinterpretations stated and corrected (interview-grade).
3. **Assumes:** *(this track)* INFR-A1, INFR-A2. *(cross-track)* Normal quantiles [Probability foundations].
4. **Sets up:** INFR-C2 (t-interval), INFR-C3 (likelihood/Wald intervals), INFR-E2 (bootstrap CI), and contrasts with INFR-E4 (Bayesian credible interval).
5. **Depth:** medium (~12–16).

#### INFR-C2. **When You Don't Know σ: the t-Distribution and Small-Sample Intervals**
1. **Question it answers:** How do we build an honest interval for a mean when the variance is unknown and the sample is small?
2. **Scope / inside:**
   - Why plugging in `σ̂` inflates uncertainty; the **t-statistic** and the **Student's t-distribution** derived (as a Normal over a scaled chi-square root).
   - **Chi-square distribution** of the sample variance built from scratch (it's needed here and in D).
   - Degrees of freedom explained mechanically; t → Normal as `n→∞` shown.
   - Two-sample intervals; the **Welch** correction for unequal variances.
   - **Edge case:** non-normal small samples where the t-interval's coverage degrades — pointing forward to the bootstrap (INFR-E2).
3. **Assumes:** *(this track)* INFR-C1, INFR-A2. *(cross-track)* the Normal and chi-square as distributions, sums of squared normals [Probability foundations].
4. **Sets up:** INFR-D2 (the t-test is the same machinery), INFR-E2 (bootstrap as the assumption-free alternative).
5. **Depth:** deep (~18–22). **Split seam:** the chi-square/sample-variance derivation can spin out as *INFR-C2a "The Distribution of the Sample Variance (Chi-Square)"* if it crowds the t-interval.

#### INFR-C3. **Intervals From the Likelihood: Wald, Score, and Profile Intervals**
1. **Question it answers:** How do we build a confidence interval for *any* MLE-estimated parameter, not just a mean?
2. **Scope / inside:**
   - **Wald interval** `θ̂ ± z·√(I(θ̂)⁻¹)` derived from INFR-B4's asymptotic normality.
   - **Profile-likelihood** and **score (Rao)** intervals; why they can beat Wald for skewed likelihoods.
   - When Wald fails badly (the binomial-near-0/1 disaster) and what to use instead (Wilson, Agresti–Coull) — honest failure mode.
3. **Assumes:** *(this track)* INFR-B3, INFR-B4, INFR-C1. *(cross-track)* none new.
4. **Sets up:** INFR-D3 (these intervals are dual to the asymptotic tests); consumed directly by Regression for coefficient CIs.
5. **Depth:** medium–deep (~16–20).

### D. Hypothesis Testing

#### INFR-D1. **The Logic of Hypothesis Testing: Null, Alternative, and the Two Ways to Be Wrong**
1. **Question it answers:** What is the actual decision-theoretic structure of a hypothesis test, and what is a p-value *really*?
2. **Scope / inside:**
   - Null vs. alternative; **Type I / Type II error**; significance level `α` and **power** `1−β`, all defined precisely.
   - The **p-value** defined as a tail probability under the null — and the long list of what it is *not* (not P(null true), not effect size, not replication probability). Interview-grade, with the misinterpretations named.
   - The duality of tests and confidence intervals, proved in one direction.
   - The base-rate / multiple-comparisons trap previewed.
3. **Assumes:** *(this track)* INFR-A1, INFR-A2, INFR-C1. *(cross-track)* conditional probability [Probability foundations].
4. **Sets up:** INFR-D2, INFR-D3, INFR-D4 — every concrete test instantiates this logic.
5. **Depth:** medium (~12–16).

#### INFR-D2. **The Workhorse Tests: z, t, χ², and F**
1. **Question it answers:** For the everyday one- and two-sample questions, which test statistic do we use, what's its null distribution, and why?
2. **Scope / inside:**
   - One- and two-sample **z- and t-tests** (the INFR-C2 machinery turned into a decision).
   - **Chi-square test** for goodness-of-fit and independence, statistic derived.
   - **F-test** for comparing variances / nested models, statistic derived as a ratio of chi-squares.
   - **Edge cases:** assumption violations (non-normality, unequal variance, dependence) and which test is robust to what.
3. **Assumes:** *(this track)* INFR-C2 (t & chi-square distributions), INFR-D1. *(cross-track)* none new.
4. **Sets up:** INFR-D5 (multiple testing across many such tests), consumed by Regression (the F-test for nested models).
5. **Depth:** deep (~18–24). **Split seam:** cut into *INFR-D2a "z- and t-tests"* and *INFR-D2b "χ² and F tests,"* at the one-parameter/variance-and-counts boundary.

#### INFR-D3. **The Asymptotic Trinity: Likelihood-Ratio, Wald, and Score Tests**
1. **Question it answers:** How do we test *any* hypothesis about an MLE-fit model, and how do the three general-purpose tests relate?
2. **Scope / inside:**
   - **Likelihood-ratio test**; **Wilks' theorem** (`2 log Λ → χ²`) motivated and the degrees of freedom explained.
   - **Wald** and **score** tests as the other two corners; the geometric picture of all three on the log-likelihood curve.
   - **Neyman–Pearson lemma** for the most-powerful test of simple-vs-simple, proved — the theoretical justification for why likelihood ratios are optimal.
   - When the three disagree and which to trust.
3. **Assumes:** *(this track)* INFR-B2, INFR-B3, INFR-B4, INFR-D1, INFR-D2 (chi-square). *(cross-track)* none new.
4. **Sets up:** consumed pervasively by Regression (deviance, nested-model tests); pairs with INFR-C3 (interval duals).
5. **Depth:** deep (~22–28). **Split seam:** cut after Neyman–Pearson into *INFR-D3a "Neyman–Pearson and the Most Powerful Test"* and *INFR-D3b "The LR, Wald, and Score Trinity."*

#### INFR-D4. **Power and Sample Size: Designing a Test That Can Actually Find Something**
1. **Question it answers:** Before collecting data, how big a sample do we need to detect an effect of a given size?
2. **Scope / inside:**
   - Power as a function of effect size, `n`, `α`, and variance — the power curve derived for the z/t case.
   - **Effect size** vs. statistical significance; why a significant result can be trivial and a null result can be uninformative.
   - Sample-size formulas derived; minimum detectable effect.
   - **Honest boundary:** the difference between "underpowered" and "no effect," and the file-drawer/p-hacking consequences.
3. **Assumes:** *(this track)* INFR-D1, INFR-D2. *(cross-track)* none new.
4. **Sets up:** INFR-D5 (power under multiplicity); informs all experimental practice.
5. **Depth:** medium (~12–16).

#### INFR-D5. **When You Run Many Tests: the Multiple-Comparisons Problem**
1. **Question it answers:** Why does testing many hypotheses inflate false discoveries, and how do we control the damage?
2. **Scope / inside:**
   - Family-wise error rate; the math of why `α` compounds; **Bonferroni** and **Holm** derived.
   - **False discovery rate** and the **Benjamini–Hochberg** procedure, derived and contrasted with FWER control.
   - When to use which; the genomics / A-B-testing reality where this is unavoidable.
3. **Assumes:** *(this track)* INFR-D1, INFR-D4. *(cross-track)* order statistics / uniform p-values under the null [Probability foundations].
4. **Sets up:** closes the testing arc; feeds practitioner judgment used in E and in Regression model selection.
5. **Depth:** medium (~12–16).

### E. Computational & Alternative Inference

#### INFR-E1. **The Bootstrap: Inference When You Can't Do the Math**
1. **Question it answers:** How do we get a sampling distribution for *any* statistic when no formula exists?
2. **Scope / inside:**
   - The **plug-in principle**: the empirical distribution as a stand-in for the population; resampling with replacement as simulating new samples.
   - Bootstrap **standard errors** and the logic of why it works (the bootstrap world mirrors the real world).
   - Worked on a statistic with no closed-form SE (e.g. the median, a correlation, a ratio).
   - **Edge of applicability:** where the bootstrap *fails* — heavy tails, the maximum, very small `n`, dependent data — stated honestly.
3. **Assumes:** *(this track)* INFR-A1, INFR-A2. *(cross-track)* empirical CDF, sampling with replacement [Probability foundations].
4. **Sets up:** INFR-E2 (bootstrap intervals), INFR-E3 (permutation is its testing cousin).
5. **Depth:** deep (~18–24). **Split seam:** cut after standard errors into *INFR-E1a "The Bootstrap Principle & Standard Errors"* and *INFR-E1b "When the Bootstrap Fails."*

#### INFR-E2. **Bootstrap Confidence Intervals: Percentile, Pivotal, and BCa**
1. **Question it answers:** How do we turn bootstrap resamples into a trustworthy confidence interval?
2. **Scope / inside:**
   - **Percentile**, **basic/pivotal**, and **bias-corrected-and-accelerated (BCa)** intervals derived; why naive percentile can be biased.
   - Coverage comparison against the t-interval (INFR-C2) on the same data.
   - How many resamples you actually need; Monte Carlo error.
3. **Assumes:** *(this track)* INFR-C1, INFR-E1. *(cross-track)* none new.
4. **Sets up:** the assumption-light alternative referenced throughout Regression for prediction intervals.
5. **Depth:** medium–deep (~16–20).

#### INFR-E3. **Permutation Tests: Testing Without a Model**
1. **Question it answers:** How do we test for an effect using only the symmetry of the null hypothesis, assuming almost nothing about the distribution?
2. **Scope / inside:**
   - The **exchangeability** argument; building the null distribution by relabeling/permuting.
   - Exact vs. Monte-Carlo permutation p-values, derived.
   - Relationship to the t-test (same answer under normality, more robust otherwise).
   - **Boundary:** what exchangeability requires and when it's violated (dependence, unequal nuisance parameters).
3. **Assumes:** *(this track)* INFR-D1, INFR-E1. *(cross-track)* combinatorics of permutations [Probability foundations].
4. **Sets up:** completes the computational-inference arc; pairs with INFR-D5 (permutation-based FWER control).
5. **Depth:** medium (~12–16).

#### INFR-E4. **The Bayesian Turn: Probability as Degree of Belief**
1. **Question it answers:** What changes when we treat the *parameter* as random, and how does that re-answer the same "how sure are we" question?
2. **Scope / inside:**
   - **Bayes' theorem for parameters**: posterior ∝ likelihood × prior, derived; the prior, the role of the marginal likelihood.
   - **Conjugate** examples worked end-to-end (Beta-Binomial, Normal-Normal) so the reader sees a full posterior by hand.
   - **Credible interval** vs. confidence interval — the philosophical and numerical difference, made concrete (this is the payoff of the whole track's framing).
   - **MAP** estimate and its relationship to the MLE (and to regularization, linking to Regression).
   - **Honest boundary:** prior sensitivity, when Bayesian and frequentist answers agree/diverge, what computation Bayes demands (pointing to MCMC as a separate future track, not built here).
3. **Assumes:** *(this track)* INFR-B1 (likelihood), INFR-C1 (to contrast intervals), INFR-D1 (to contrast testing). *(cross-track)* conditional probability & Bayes' rule for events [Probability foundations]; the Beta/Gamma distributions [Probability foundations].
4. **Sets up:** a future **Bayesian Computation / MCMC** track; closes this track by showing the alternative paradigm to the same charter question. Connects MAP ↔ regularization back to Regression.
5. **Depth:** deep (~22–28). **Split seam:** cut into *INFR-E4a "Bayes' Theorem for Parameters & Conjugate Inference"* and *INFR-E4b "Credible Intervals, MAP, and Bayesian vs. Frequentist,"* at the prior/posterior-mechanics vs. interpretation boundary.

---

## Flow Diagram

```
A. FOUNDATIONS
  INFR-A1 Estimator as a Random Variable
        │
        ▼
  INFR-A2 LLN & CLT ───────────────────────────────┐
        │                                       │
        ▼                                       │
B. LIKELIHOOD SPINE                             │
  INFR-B1 The Likelihood                             │
        │                                       │
        ▼                                       │
  INFR-B2 Maximum Likelihood (MLE)                   │
        │                                       │
        ▼                                       │
  INFR-B3 Fisher Information ──────────┐             │
        │                         │             │
        ▼                         │             │
  INFR-B4 MLE Asymptotics ◄────────────┘◄────────────┘   (uses CLT + Fisher info)
        │
        ├───────────────────────────────┐
        ▼                                ▼
C. INTERVALS                        D. TESTING
  INFR-C1 Confidence Intervals  ──┐       INFR-D1 Logic of Testing / p-values
        │                    │             │
        ▼                    │             ▼
  INFR-C2 t & χ² / small sample   │       INFR-D2 z, t, χ², F  ◄── (needs INFR-C2's distributions)
        │                    │             │
        ▼                    │             ├──► INFR-D4 Power & Sample Size
  INFR-C3 Wald/Score/Profile CI ◄─┘             │         │
        │ (INFR-B3,INFR-B4)                          ▼         ▼
        │                            INFR-D3 LR/Wald/Score Trinity   INFR-D5 Multiple Comparisons
        │  (INFR-C3 ⇄ INFR-D3 are interval/test duals)  (INFR-B2,INFR-B3,INFR-B4)
        │
        ▼
E. COMPUTATIONAL & ALTERNATIVE
  INFR-E1 The Bootstrap ──► INFR-E2 Bootstrap CIs   (INFR-C1)
        │
        └────► INFR-E3 Permutation Tests   (INFR-D1)

  INFR-E4 The Bayesian Turn   (INFR-B1, INFR-C1, INFR-D1)  ── closes the track, forks to a future MCMC track
```

Linear reading order: **INFR-A1 → INFR-A2 → INFR-B1 → INFR-B2 → INFR-B3 → INFR-B4 → INFR-C1 → INFR-C2 → INFR-C3 → INFR-D1 → INFR-D2 → INFR-D3 → INFR-D4 → INFR-D5 → INFR-E1 → INFR-E2 → INFR-E3 → INFR-E4.**

---

## CROSS-TRACK PREREQUISITE Articles (owned by OTHER tracks)

**From Probability foundations:**
- **Random variables, expectation & variance** — needed at **INFR-A1**.
- **Independence & i.i.d. samples** — needed at **INFR-A1**.
- **Chebyshev's inequality + modes of convergence (in probability, in distribution)** — needed at **INFR-A2**.
- **Moment generating / characteristic functions** — needed at **INFR-A2** (CLT machinery).
- **Common distributions I: Bernoulli/Binomial, Poisson, Normal (pmf/pdf, joint density)** — needed at **INFR-B1**.
- **Common distributions II: Chi-square, Student's t, F** — needed at **INFR-C2**.
- **Common distributions III: Beta, Gamma** — needed at **INFR-E4**.
- **Conditional probability & Bayes' rule for events** — needed at **INFR-D1** and **INFR-E4**.
- **The empirical CDF / sampling with replacement** — needed at **INFR-E1**.
- **Order statistics & the uniform distribution of null p-values** — needed at **INFR-D5**.
- **Combinatorics of permutations** — needed at **INFR-E3**.

**From Geometry of Data / Linear Algebra:**
- **Gradients and the multivariable critical-point condition** — needed at **INFR-B2** (multi-parameter MLE).
- *(Light)* **Quadratic forms / the Hessian** — needed at **INFR-B3–INFR-B4** for the multi-parameter Fisher information matrix.

**From Optimization:**
- **Newton's method / gradient ascent** — needed at **INFR-B2** (when the MLE has no closed form) and **INFR-B4**.

**From Regression:** *(this track feeds Regression more than it consumes it)* — no hard prerequisite. The only inbound link is **MAP ↔ regularization** at **INFR-E4**, which is a *connection*, not a dependency.

---

## Shared Prerequisites OVERLAPPING with the Regression Track — ownership calls

Recommendation: **Inference owns the general theory; Regression links to it and applies it.**

| Shared topic | **Owner** | Rationale |
|---|---|---|
| **MLE as a general estimation principle** (INFR-B1–INFR-B2) | **Inference** | It's the general engine; Regression instantiates it for β̂. |
| **Sampling distribution of an estimator** (INFR-A1) | **Inference** | The general concept; Regression specializes to β̂. |
| **Fisher information & Cramér–Rao** (INFR-B3) | **Inference** | General; Regression uses it for coefficient standard errors. |
| **MLE asymptotics / asymptotic normality** (INFR-B4) | **Inference** | Underwrites all of Regression's inference. |
| **Confidence intervals (concept + construction)** (INFR-C1, INFR-C3) | **Inference** | Regression produces intervals by applying INFR-C1/INFR-C3. |
| **Hypothesis-test logic + the F-test for nested models** (INFR-D1, INFR-D2, INFR-D3) | **Inference owns theory; Regression owns the application** | The F-test statistic/null distribution live here; Regression's "F-test for nested regression models" links back. |
| **The bootstrap** (INFR-E1–INFR-E2) | **Inference** | General method; Regression uses it for prediction/coefficient intervals. |
| **MAP ↔ ridge/lasso regularization** (INFR-E4) | **Shared, written twice on purpose at different altitudes** | Inference derives MAP-as-penalized-likelihood in general; Regression derives the specific ridge/lasso penalties. |
| **Residual diagnostics / goodness-of-fit for a fitted model** | **Regression** | Model criticism of a specific fit. Inference supplies only the test theory. |

**One-line ownership rule:** *the general estimator/uncertainty machinery is Inference's; any instance bolted onto a specific model family is Regression's, and links back rather than re-deriving.*

---

### Summary of decisions
- **Name:** Statistical **Inference** (not Modeling).
- **Aim:** turn data into defensible conclusions with calibrated uncertainty; estimator → likelihood → intervals → tests → computational/Bayesian alternatives.
- **Boundary:** Inference owns *uncertainty and testing machinery in general*; Regression owns *model specification and any model-specific instance*, linking back.
- **18 articles** in 5 movements (with 8 named split seams), each inch-wide and building on the last.
