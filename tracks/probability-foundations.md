# Core Sample — Track Roadmap: **Probability Foundations**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

*An inch wide, a mile deep. From "what is a random event" all the way down to random vectors, convergence, and the distributions every other track leans on.*

This is the **root track** of the series: almost everything downstream (Statistical Inference, Regression, Geometry of Data, Optimization, Classification, Unsupervised Learning, Causal Inference) draws a prerequisite from here. So it starts at the true entry point — the **Calc-1 floor** — and builds, with nothing assumed above algebra/functions/limits/single-variable differentiation and integration. Multivariable calculus, linear algebra, and the very idea of an estimator are *not* assumed; where a result needs the Calc-1 shadow of a higher tool (a double integral, a vector mean), it is built inline at the floor's level and flagged.

The charter question: **"How do we put numbers on uncertainty, manipulate them without contradiction, and describe the random quantities that data is made of?"** This track owns the *objects* of probability (sample spaces, random variables, distributions, expectation, convergence) — **not** estimation, not testing, not modeling. Those are downstream and link back.

The spine is: **build the sample space → put a random number on it (random variable) → summarize it (expectation/variance) → combine many of them (joint, independence, i.i.d.) → catalog the named distributions → go to vectors → control the tails and the limits (Chebyshev, convergence, MGFs) → the sampling-theory objects (empirical CDF, order statistics, combinatorics) that the data tracks consume.**

---

## The flow diagram

```
                 [PROB-0] What Is Probability? (sample spaces & the axioms)
                                     │
                                     ▼
                 [PROB-1] Conditional Probability, Independence & Bayes' Rule
                                     │
                                     ▼
                 [PROB-2] Random Variables: Turning Outcomes into Numbers
                                     │
                  ┌──────────────────┼───────────────────┐
                  ▼                                       ▼
   [PROB-3] Discrete RVs (pmf, CDF)                [PROB-4] Continuous RVs (pdf, CDF)
                  └──────────────────┬───────────────────┘
                                     ▼
                 [PROB-5] Expectation: The Long-Run Average
                                     │
                                     ▼
                 [PROB-6] Variance, Standard Deviation & Variance-as-Sum-of-Squares
                                     │
                                     ▼
                 [PROB-7] Joint Distributions, Covariance & Correlation
                                     │
                  ┌──────────────────┼───────────────────┐
                  ▼                                       ▼
   [PROB-8] Independence & the i.i.d. Sample       [PROB-9] Conditional Distributions
                  │                             & Conditional Expectation E[Y|X]
                  └──────────────────┬───────────────────┘
                                     ▼
            ┌──────────── THE DISTRIBUTION CATALOG ────────────┐
            │ [PROB-10] Counting: Permutations & Combinations        │
            │            │                                       │
            │            ▼                                       │
            │ [PROB-11] Bernoulli, Binomial & Negative-Binomial      │
            │            │                                       │
            │            ▼                                       │
            │ [PROB-12] The Poisson Distribution (& the limit)       │
            │            │                                       │
            │            ▼                                       │
            │ [PROB-13] The Normal (Gaussian) Distribution           │
            │            │                                       │
            │            ▼                                       │
            │ [PROB-14] Gamma, Exponential & Beta                    │
            │            │                                       │
            │            ▼                                       │
            │ [PROB-15] Chi-Square, Student's t & F                  │
            │            │                                       │
            │            ▼                                       │
            │ [PROB-16] The Exponential Family (the unifying form)   │
            └────────────────────────────────────────────────────┘
                                     │
                                     ▼
                 [PROB-17] Random Vectors, Mean Vectors & Covariance Matrices
                                     │
                                     ▼
                 [PROB-18] Linear Transforms of Random Vectors
                                     │
                  ┌──────────────────┼───────────────────┐
                  ▼                                       ▼
   [PROB-19] Chebyshev's Inequality              [PROB-20] Moment Generating &
   & the Markov/Concentration Idea           Characteristic Functions
                  └──────────────────┬───────────────────┘
                                     ▼
                 [PROB-21] Modes of Convergence (in Probability, in Distribution)
                                     │
                  ┌──────────────────┼───────────────────┐
                  ▼                                       ▼
   [PROB-22] The Empirical CDF &                  [PROB-23] Order Statistics & the
   Sampling With Replacement                  Uniform Distribution of Null p-Values
```

The catalog (PROB-10–PROB-16) hangs off the joint/conditional foundation (PROB-5–PROB-9) and can be read in parallel with the vector/limit spine (PROB-17–PROB-23) once expectation and variance exist. See the reading-order note at the end.

---

## Movement 1 — The ground floor: events, conditioning, random variables

### PROB-0 — What Is Probability? Sample Spaces and the Axioms
1. **The one question:** Before any formula, what is the object we are assigning probabilities *to*, and what rules keep those assignments from contradicting each other?
2. **Scope / inside:**
   - Sample space `Ω`, outcomes, and **events** as subsets; the event algebra (union, intersection, complement) in plain set language built from scratch.
   - **Kolmogorov's axioms** (non-negativity, `P(Ω)=1`, countable additivity) and the elementary consequences derived from them: `P(∅)=0`, complement rule, **inclusion–exclusion**, monotonicity.
   - The three honest interpretations (classical/equally-likely, frequentist long-run, subjective) and why the axioms hold for all three — set up before any track has to *choose* one.
   - Worked examples: dice/cards (finite), a dart on an interval (the leap to uncountable Ω and why we measure sets, gently).
3. **Assumes:** Only the floor (sets, functions, the idea of a fraction of outcomes). The countable-additivity / measure subtlety is flagged and built to the floor's level, not assumed.
4. **Sets up:** PROB-1 (conditioning), PROB-2 (a random variable is a function on Ω). The true entry point of the whole series.
5. **Depth:** medium (~12–16). Motivational and definitional.

### PROB-1 — Conditional Probability, Independence, and Bayes' Rule
1. **The one question:** How does learning that one event happened change the probability of another — and how do we invert that relationship?
2. **Scope / inside:**
   - Conditional probability `P(A|B)=P(A∩B)/P(B)` motivated as "restricting the sample space"; the **multiplication rule** and the chain rule.
   - **Independence** of events defined as `P(A∩B)=P(A)P(B)`; why "independent" ≠ "mutually exclusive" (the classic confusion, settled).
   - The **law of total probability** and **Bayes' rule** derived in full; the base-rate worked example (medical test) that every interview asks for.
   - Edge case: the prosecutor's fallacy / confusing `P(A|B)` with `P(B|A)` as the honest failure mode.
3. **Assumes:** PROB-0.
4. **Sets up:** PROB-8 (independence of random variables), PROB-9 (conditional distributions), PROB-12 (Poisson via independence). **Cross-track payoff:** Statistical Inference D1 & E4, Causal Inference, Classification (naive Bayes) all consume this.
5. **Depth:** medium (~12–16).

### PROB-2 — Random Variables: Turning Outcomes into Numbers
1. **The one question:** How do we attach a number to a random outcome so we can do arithmetic, and what is the one object (the CDF) that describes *any* such number?
2. **Scope / inside:**
   - A random variable as a **function `X: Ω → ℝ`**; why this is the move that lets calculus touch probability.
   - The **cumulative distribution function** `F(x)=P(X≤x)` as the universal descriptor (works for discrete, continuous, and mixed); its three defining properties (monotone, right-continuous, limits 0 and 1), derived from the axioms.
   - Discrete vs. continuous vs. mixed previewed via the CDF's jumps and flats — motivating the PROB-3/PROB-4 split.
3. **Assumes:** PROB-0, PROB-1.
4. **Sets up:** PROB-3, PROB-4 (the two concrete kinds), PROB-22 (the *empirical* CDF is this object estimated from data).
5. **Depth:** medium (~12–16).

### PROB-3 — Discrete Random Variables: The Probability Mass Function
1. **The one question:** When a random variable takes countably many values, how do we describe it and compute probabilities of events?
2. **Scope / inside:**
   - The **pmf** `p(x)=P(X=x)`; the normalization `Σ p(x)=1`; recovering the CDF as a running sum and vice versa.
   - The support; probabilities of compound events as sums over the mass.
   - Worked examples that *aren't* yet "named" distributions (a loaded die, a custom payout table) so the machinery is clear before the catalog names it.
3. **Assumes:** PROB-2.
4. **Sets up:** PROB-5 (expectation as a weighted sum), PROB-11/PROB-12 (the named discrete distributions).
5. **Depth:** short–medium (~10–14).

### PROB-4 — Continuous Random Variables: The Probability Density Function
1. **The one question:** When a random variable can take any value in a continuum, why is `P(X=x)=0`, and how does a *density* still let us compute probabilities?
2. **Scope / inside:**
   - The **pdf** `f(x)` as the derivative of the CDF; `P(a≤X≤b)=∫ₐᵇ f` built from the Calc-1 fundamental theorem of calculus (the one place we lean on the floor's integration directly).
   - Why density is *not* probability (it can exceed 1); the normalization `∫f=1`.
   - Change-of-variables for a monotone transform `Y=g(X)`, derived with the Jacobian-of-one-variable (Calc-1 substitution), flagged as the scalar shadow of the vector version (PROB-18).
   - Worked examples: uniform, a triangular density, and a first look at the exponential.
3. **Assumes:** PROB-2; floor-level integration and the chain rule (used explicitly, not assumed away).
4. **Sets up:** PROB-5, PROB-13/PROB-14 (the named continuous distributions), PROB-18 (vector change of variables).
5. **Depth:** medium (~12–16).

---

## Movement 2 — Summaries: expectation, spread, and how variables relate

### PROB-5 — Expectation: The Long-Run Average
1. **The one question:** What single number summarizes "where a random variable lands on average," and how do we compute and manipulate it?
2. **Scope / inside:**
   - `E[X]=Σ x p(x)` (discrete) and `E[X]=∫ x f(x) dx` (continuous), motivated as the limit of a sample average (foreshadowing the LLN, owned by Inference).
   - **The law of the unconscious statistician** `E[g(X)]` derived; **linearity of expectation** proved and stressed as the workhorse identity (holds even without independence).
   - Existence/divergence: an honest example where the expectation does not exist (heavy tail / Cauchy preview) — the boundary case.
3. **Assumes:** PROB-3, PROB-4.
4. **Sets up:** PROB-6 (variance is an expectation), PROB-7 (covariance is an expectation), every distribution's mean in the catalog, PROB-19 (Markov/Chebyshev).
5. **Depth:** medium (~12–16).

### PROB-6 — Variance, Standard Deviation, and Variance as a Sum of Squares
1. **The one question:** How do we quantify how *spread out* a random variable is, and why is that spread fundamentally a sum of squared deviations?
2. **Scope / inside:**
   - `Var(X)=E[(X−μ)²]`; the **computational identity** `Var(X)=E[X²]−(E[X])²`, derived; standard deviation as the back-to-scale measure.
   - **Variance as a sum of squares:** the deviation-squared structure, the population-vs-sample sum-of-squares decomposition, and why squaring (not absolute value) is the analytically natural choice — the precise hook Regression R3 requests.
   - `Var(aX+b)=a²Var(X)` derived; why variance is *not* linear; standardization (z-scores).
3. **Assumes:** PROB-5.
4. **Sets up:** PROB-7 (covariance generalizes this to pairs), PROB-17 (covariance matrix is the vector version), PROB-19 (Chebyshev uses variance). **Cross-track payoff:** Regression R3 (variance as sum of squares), R2.
5. **Depth:** medium (~12–16).

### PROB-7 — Joint Distributions, Covariance, and Correlation
1. **The one question:** How do we describe two random variables *together*, and how do we measure whether they move with each other?
2. **Scope / inside:**
   - Joint pmf/pdf; **marginal** distributions by summing/integrating out; the joint CDF.
   - **Covariance** `Cov(X,Y)=E[(X−μ_X)(Y−μ_Y)]` and its computational form; **correlation** as the scale-free, `[−1,1]`-bounded version; the bilinearity of covariance, derived.
   - `Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)` derived in full — the identity that powers everything from portfolio variance to the variance of a sum.
   - Honest edge case: **zero covariance does not imply independence** (a worked counterexample) — settles the classic interview trap.
3. **Assumes:** PROB-5, PROB-6.
4. **Sets up:** PROB-8 (independence), PROB-17 (covariance matrix), PROB-18 (variance of linear combinations). **Cross-track payoff:** Regression R2/R6, Geometry of Data (covariance as Gram matrix), Unsupervised Learning (PCA).
5. **Depth:** medium–deep (~14–18).

### PROB-8 — Independence and the i.i.d. Sample
1. **The one question:** What does it mean for random variables to be independent, and what exactly are we assuming when we say a dataset is "i.i.d."?
2. **Scope / inside:**
   - Independence of random variables via factoring joint = product of marginals; independence ⇒ zero covariance (and the converse failure, tied to PROB-7).
   - **Expectation and variance of sums** under independence: `E[ΣXᵢ]` always, `Var(ΣXᵢ)=ΣVar(Xᵢ)` under independence — derived; the `√n` shrink of the sample-mean's SD foreshadowed.
   - **Identically distributed + independent = i.i.d.**; what real data violates this (dependence, non-stationarity) as the honest boundary every applied track hits.
3. **Assumes:** PROB-7.
4. **Sets up:** the i.i.d. backbone of Statistical Inference (A1), Regression, Classification; PROB-19/PROB-21 (limit theorems are about i.i.d. sums); PROB-22 (the empirical CDF is built from an i.i.d. sample).
5. **Depth:** medium (~12–16).

### PROB-9 — Conditional Distributions and Conditional Expectation
1. **The one question:** Once we know the value of one random variable, what is the distribution — and the mean — of another, and why is `E[Y|X]` itself a random variable?
2. **Scope / inside:**
   - Conditional pmf/pdf `f(y|x)=f(x,y)/f(x)`; the conditional CDF; rebuilding PROB-1's conditioning at the random-variable level.
   - **Conditional expectation `E[Y|X=x]`** as a number, and **`E[Y|X]`** as a *function of `X`* (hence a random variable) — the conceptual leap, made carefully.
   - The **law of total expectation** `E[Y]=E[E[Y|X]]` and the **law of total variance** `Var(Y)=E[Var(Y|X)]+Var(E[Y|X])`, both derived in full.
   - `E[Y|X]` as the **best predictor** in mean-squared error (the result Regression's whole "estimate `E[Y|X]`" framing rests on), derived.
3. **Assumes:** PROB-5, PROB-7, PROB-1.
4. **Sets up:** Regression R0/R23 (regression *is* estimating `E[Y|X]`; kernel regression), Causal Inference (conditioning), Classification (Bayes-optimal classifier). 
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the two laws of total expectation/variance into *PROB-9a "Conditional Distributions & Conditional Expectation"* and *PROB-9b "The Laws of Total Expectation/Variance & Best Prediction,"* at the boundary where `E[Y|X]` becomes a predictor.

---

## Movement 3 — The distribution catalog

### PROB-10 — Counting: Permutations and Combinations
1. **The one question:** When outcomes are equally likely, how do we count the arrangements and selections that probabilities are ratios of?
2. **Scope / inside:**
   - The multiplication principle; **permutations** `n!/(n−k)!` (order matters) and **combinations** `C(n,k)` (order doesn't), each derived, not stated.
   - The binomial coefficient's symmetry and Pascal's recurrence; the **binomial theorem** stated (sets up the binomial pmf normalizing to 1).
   - Sampling with vs. without replacement, ordered vs. unordered — the 2×2 table — and where permutation *tests* (Inference E3) get their count.
3. **Assumes:** PROB-0 (equally-likely events).
4. **Sets up:** PROB-11 (binomial pmf), PROB-23 (order statistics), and **cross-track** Statistical Inference E3 (combinatorics of permutations).
5. **Depth:** medium (~12–16).

### PROB-11 — Bernoulli, Binomial, and Negative-Binomial
1. **The one question:** How do we model a single yes/no trial, a fixed number of them, and "how long until success" — and how are the three related?
2. **Scope / inside:**
   - **Bernoulli(p)**: pmf, mean `p`, variance `p(1−p)` derived.
   - **Binomial(n,p)** as a sum of i.i.d. Bernoullis: pmf via PROB-10's count, mean `np` and variance `np(1−p)` via PROB-8's sum rules — derived two ways.
   - **Geometric** and **negative-binomial** (number of failures before the `r`-th success); the overdispersion role the negative-binomial plays as a Poisson alternative (forward link to Regression R19).
   - Real examples: conversion rates, defect counts, the honest "trials aren't really independent" caveat.
3. **Assumes:** PROB-5, PROB-6, PROB-8, PROB-10.
4. **Sets up:** PROB-12 (Poisson as a binomial limit), PROB-13 (normal approximation). **Cross-track payoff:** Regression R17 (logistic), R19 (negative-binomial); Inference B1 (Bernoulli/binomial likelihoods), E4 (Beta-Binomial); Classification.
5. **Depth:** medium–deep (~14–18).

### PROB-12 — The Poisson Distribution
1. **The one question:** How do we model the count of rare events in a fixed window, and why does one parameter control both its mean and its variance?
2. **Scope / inside:**
   - The **Poisson(λ)** pmf; derivation as the **limit of Binomial(n, λ/n)** as `n→∞` (every step of the limit shown), and the law-of-rare-events story.
   - Mean `=` variance `= λ` derived (the **equidispersion** property), and the additivity of independent Poissons.
   - The Poisson process sketch (link to the exponential inter-arrival times in PROB-14); overdispersion as the honest failure mode where real counts break Poisson (forward to Regression R19).
3. **Assumes:** PROB-11; PROB-5/PROB-6 (mean & variance); limits at the floor's level.
4. **Sets up:** PROB-14 (exponential gaps), Regression R19. **Cross-track payoff:** Inference B1 (Poisson likelihood).
5. **Depth:** medium (~12–16).

### PROB-13 — The Normal (Gaussian) Distribution
1. **The one question:** Why is the bell curve the single most important distribution in statistics, and where do its density and its magic properties come from?
2. **Scope / inside:**
   - The **density** `(1/√(2πσ²))exp(−(x−μ)²/2σ²)`; the **Gaussian integral** `∫e^{−x²/2}dx=√(2π)` derived in full (the polar-coordinates double-integral trick, built to the floor's level — the one flagged multivariable touch).
   - Mean `μ`, variance `σ²`; standardization to `Z`; the **closure under linear combinations** of independent normals, derived (sets up why estimators are asymptotically normal).
   - Why it's everywhere (preview of the CLT, owned by Inference A2) and the honest boundary: thin tails mislead under heavy-tailed reality.
3. **Assumes:** PROB-4, PROB-5, PROB-6, PROB-8; the Gaussian-integral derivation flags its one above-floor step and builds it.
4. **Sets up:** PROB-15 (chi-square/t/F are built from normals), PROB-17–PROB-18 (the multivariate normal), PROB-20 (its MGF). **Cross-track payoff:** Regression R9/R12, Inference everywhere.
5. **Depth:** deep (~18–24). **Split seam if needed:** the Gaussian-integral derivation can spin out as *PROB-13a "The Gaussian Integral"* if it crowds the distribution's properties.

### PROB-14 — Gamma, Exponential, and Beta
1. **The one question:** How do we model waiting times and bounded proportions, and what is the gamma function that ties them together?
2. **Scope / inside:**
   - The **gamma function** `Γ(α)` and its `Γ(α)=(α−1)Γ(α−1)` recurrence, derived (the normalizing constant the next three distributions all need).
   - **Exponential(λ)** as the memoryless waiting time (memorylessness derived; link to the Poisson process in PROB-12); the **Gamma(α,β)** as a sum of exponentials.
   - The **Beta(α,β)** on `[0,1]` for proportions; its mean/variance; the Beta–Gamma relationship; why Beta is the natural prior for a probability (forward to Inference E4 conjugacy).
3. **Assumes:** PROB-4, PROB-5, PROB-6, PROB-12 (Poisson-process link).
4. **Sets up:** PROB-15 (chi-square is a special gamma), PROB-16 (all are exponential-family members). **Cross-track payoff:** Inference E4 (Beta, Gamma for conjugate Bayes).
5. **Depth:** deep (~18–22). **Split seam if needed:** cut into *PROB-14a "Gamma & Exponential"* and *PROB-14b "The Beta Distribution,"* at the waiting-times/proportions boundary.

### PROB-15 — Chi-Square, Student's t, and F
1. **The one question:** Where do the three "sampling" distributions of classical statistics come from, and why do they arise from normal samples?
2. **Scope / inside:**
   - **Chi-square** as a sum of squared standard normals (a special **Gamma**, from PROB-14); its df, mean `k`, variance `2k`, derived; the distribution of the **sample variance**.
   - **Student's t** as `Z/√(χ²_k/k)` — a standard normal over a scaled chi-square root — derived; why its tails are heavy and why `t→Normal` as `df→∞`.
   - **F** as a ratio of two scaled chi-squares; its role in comparing variances and nested models (forward to Regression R9 and Inference D2).
3. **Assumes:** PROB-13 (normal), PROB-14 (gamma), PROB-8 (independence of the numerator/denominator pieces).
4. **Sets up:** **cross-track** Regression R9 (t/F/χ² inference), Inference C2 (t and chi-square), D2 (z/t/χ²/F tests).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after chi-square into *PROB-15a "The Chi-Square Distribution & the Sample Variance"* and *PROB-15b "Student's t and F,"* at the single-sample/ratio boundary.

### PROB-16 — The Exponential Family: One Form Behind Many Distributions
1. **The one question:** What single algebraic form contains the Bernoulli, Poisson, normal, gamma, and beta as special cases, and why does that unification matter?
2. **Scope / inside:**
   - The canonical form `f(x|θ)=h(x)exp(η(θ)·T(x)−A(θ))`; identifying the **natural parameter `η`**, the **sufficient statistic `T(x)`**, and the **log-partition `A(θ)`**.
   - Re-expressing PROB-11–PROB-14's distributions in this form, one worked example each.
   - The headline properties derived: moments of `T(x)` are derivatives of `A(θ)` (`A′=E[T]`, `A″=Var(T)`) — the result GLMs (Regression R18) and exponential-family inference run on.
   - Honest boundary: which common distributions are *not* in the family (e.g. Student's t, uniform with unknown support) and why that matters.
3. **Assumes:** PROB-11, PROB-12, PROB-13, PROB-14; PROB-5/PROB-6 (moments).
4. **Sets up:** **cross-track** Regression R18 (GLM framework), Inference (sufficiency, exponential-family MLE).
5. **Depth:** deep (~18–24).

---

## Movement 4 — Going to vectors, then to the limit

### PROB-17 — Random Vectors, Mean Vectors, and Covariance Matrices
1. **The one question:** How do we package several random variables into one vector object, and what replaces the mean and variance when we do?
2. **Scope / inside:**
   - A **random vector** `X=(X₁,…,X_d)`; its **mean vector** `μ=E[X]` (component-wise); the **covariance matrix** `Σ` with variances on the diagonal and covariances off it (built directly from PROB-7).
   - Why `Σ` is **symmetric and positive semidefinite**, derived from `aᵀΣa=Var(aᵀX)≥0` (the bridge to Geometry of Data's PD matrices — built here only to the extent probability needs it, the linear-algebra theory owned there).
   - The **multivariate normal** introduced via its mean vector and covariance matrix; the bivariate case visualized (contours, correlation as tilt).
3. **Assumes:** PROB-7, PROB-13; vectors/matrices used at a notational level, with the linear-algebra machinery flagged as cross-track (Geometry of Data).
4. **Sets up:** PROB-18 (linear transforms), **cross-track** Regression R6 (covariance of `β̂`), Geometry of Data, Unsupervised Learning (PCA on `Σ`).
5. **Depth:** deep (~18–24). **Split seam if needed:** the multivariate-normal density can spin out as *PROB-17a "The Multivariate Normal"* if the covariance-matrix mechanics fill the budget.

### PROB-18 — Linear Transforms of Random Vectors
1. **The one question:** When we hit a random vector with a matrix, `Y=AX+b`, what happens to its mean vector and covariance matrix?
2. **Scope / inside:**
   - `E[AX+b]=Aμ+b` and **`Cov(AX+b)=AΣAᵀ`**, both derived from first principles (the single identity Regression R6 leans on for `Var(β̂)=σ²(XᵀX)⁻¹`).
   - The scalar special cases recovered (`Var(aᵀX)=aᵀΣa`); how a linear map rotates/stretches the covariance ellipse (visual).
   - Closure of the multivariate normal under linear maps; the whitening transform `Σ^{−1/2}X` that decorrelates (forward link to Regression R11 GLS and Geometry of Data).
3. **Assumes:** PROB-17.
4. **Sets up:** **cross-track** Regression R6 (sampling distribution of `β̂`), R11 (whitening/GLS), Geometry of Data, Optimization (quadratic forms).
5. **Depth:** medium–deep (~14–18).

### PROB-19 — Chebyshev's Inequality and the Concentration Idea
1. **The one question:** Without knowing the full distribution, how much probability can possibly sit far from the mean — and why does that make averages predictable?
2. **Scope / inside:**
   - **Markov's inequality** derived first (the one-line bound for non-negative variables), then **Chebyshev's** `P(|X−μ|≥kσ)≤1/k²` derived from it.
   - What Chebyshev buys: a distribution-free guarantee; why it's loose for nice distributions and tight for adversarial ones (honest boundary).
   - **Chebyshev ⇒ the (weak) Law of Large Numbers sketch**: the sample mean concentrates — built far enough to hand cleanly to Inference A2, which *owns* the LLN/CLT.
3. **Assumes:** PROB-5, PROB-6, PROB-8.
4. **Sets up:** PROB-21 (convergence in probability is what Chebyshev delivers), **cross-track** Inference A2 (LLN via Chebyshev, by explicit request).
5. **Depth:** medium (~12–16).

### PROB-20 — Moment Generating and Characteristic Functions
1. **The one question:** Is there a single transform that encodes *all* of a distribution's moments and turns sums of independent variables into products?
2. **Scope / inside:**
   - The **MGF** `M(t)=E[e^{tX}]`; generating moments by differentiation at 0, derived; MGFs of the catalog distributions (Bernoulli, Poisson, normal, gamma) worked.
   - The **uniqueness** and **convolution** properties: the MGF of a sum of independents is the product — the engine behind "sum of normals is normal," "sum of Poissons is Poisson," derived.
   - When the MGF fails to exist (heavy tails) and the **characteristic function** `E[e^{itX}]` as the always-existing fix; its role in the CLT flagged (the proof owned by Inference A2).
3. **Assumes:** PROB-5, PROB-8, PROB-11–PROB-14 (catalog to compute MGFs of); complex exponentials introduced gently for the characteristic function.
4. **Sets up:** PROB-21 (convergence in distribution via characteristic functions), **cross-track** Inference A2 (CLT machinery, by explicit request).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the MGF into *PROB-20a "Moment Generating Functions"* and *PROB-20b "Characteristic Functions,"* at the existence boundary.

### PROB-21 — Modes of Convergence: In Probability and In Distribution
1. **The one question:** A *sequence* of random variables can "approach" a limit in more than one sense — what are the senses we actually use, and how do they relate?
2. **Scope / inside:**
   - **Convergence in probability** (what the LLN delivers) and **convergence in distribution** (what the CLT delivers), each defined precisely; almost-sure and `L²` convergence stated for contrast.
   - The **hierarchy**: a.s. ⇒ in probability ⇒ in distribution, with the implications proved or carefully argued and the converses shown to fail by counterexample.
   - **Slutsky's theorem** and the **continuous mapping theorem** stated and motivated (the glue Inference uses to combine limits, e.g. plugging `σ̂` into a CLT statement).
3. **Assumes:** PROB-19 (Chebyshev gives convergence in probability), PROB-20 (characteristic functions characterize convergence in distribution).
4. **Sets up:** **cross-track** Inference A2 (the LLN/CLT are stated in these modes), B4 (asymptotic normality of the MLE), the delta method.
5. **Depth:** deep (~18–24). **Split seam if needed:** cut into *PROB-21a "Convergence in Probability"* and *PROB-21b "Convergence in Distribution & Slutsky,"* at the two-modes boundary.

---

## Movement 5 — The objects sampling theory is built from

### PROB-22 — The Empirical CDF and Sampling With Replacement
1. **The one question:** Given a finite sample, what is the data's own estimate of the distribution it came from, and why can we resample *from the data itself*?
2. **Scope / inside:**
   - The **empirical CDF** `F̂ₙ(x)=(1/n)Σ 1{Xᵢ≤x}` as the data-driven stand-in for `F` (the PROB-2 object, estimated); each `F̂ₙ(x)` as a scaled binomial, hence unbiased with variance `F(1−F)/n`, derived.
   - The **plug-in principle**: estimate any functional of `F` by the same functional of `F̂ₙ`; **sampling with replacement** as drawing from `F̂ₙ`.
   - Glivenko–Cantelli stated (the empirical CDF converges uniformly, in the PROB-21 sense) — the theoretical license for the bootstrap, handed to Inference E1, which *owns* the bootstrap method itself.
3. **Assumes:** PROB-2, PROB-8, PROB-11 (the indicator-as-Bernoulli view), PROB-21 (the convergence statement).
4. **Sets up:** **cross-track** Inference E1 (the bootstrap), Unsupervised Learning / Classification (resampling, bagging).
5. **Depth:** medium (~12–16).

### PROB-23 — Order Statistics and the Uniform Distribution of Null p-Values
1. **The one question:** When we sort a sample, what is the distribution of the `k`-th smallest value — and why are valid p-values uniform under the null?
2. **Scope / inside:**
   - **Order statistics** `X₍₁₎≤…≤X₍ₙ₎`; the density of the `k`-th order statistic derived via the multinomial/combinatorial count (payoff from PROB-10); the distributions of the **min, max, and median**.
   - The **probability integral transform** `F(X)∼Uniform(0,1)` derived — the fact that makes a correctly-computed p-value uniform under the null.
   - Order statistics of the uniform (the Beta connection, from PROB-14); the honest boundary where extreme order statistics have non-normal limits (extreme-value theory flagged, not built).
3. **Assumes:** PROB-10 (counting), PROB-4 (densities), PROB-14 (Beta link).
4. **Sets up:** **cross-track** Inference D5 (multiple comparisons: order statistics + uniform null p-values, by explicit request), and any extreme-value / quantile work downstream.
5. **Depth:** medium–deep (~14–18).

---

## Cross-track prerequisites (belong to OTHER tracks)

Probability Foundations is the root track and consumes very little. The few items it leans on above the Calc-1 floor are either built inline at the floor's level (and flagged in the article) or named here so the chain (§1.4) is explicit.

**From the Geometry of Data / Applied Linear Algebra track**
- *Vectors, matrices, matrix multiplication and transpose* (notation + the `AΣAᵀ` mechanics) — touched at **PROB-17, PROB-18**. Probability uses them operationally; the linear-algebra *theory* (vector spaces, rank, eigenstructure) is owned there.
- *Symmetric positive-semidefinite matrices* (the property of a covariance matrix) — touched at **PROB-17**; proved here only to the extent `aᵀΣa≥0` requires, with the general PD theory owned by Geometry of Data.

**From the Calc-1 floor (assumed, not a track)**
- *Single-variable differentiation/integration, the fundamental theorem, substitution, limits* — used throughout (PROB-4, PROB-5, PROB-12, PROB-14, PROB-20). These are *at* the floor and therefore assumable.
- *The one double-integral (Gaussian integral, polar coordinates)* at **PROB-13** and the *one Jacobian change-of-variables* at **PROB-4/PROB-18** are above the floor and are **built inline and flagged**, not assumed.

This track has **no inbound dependency on Regression, Inference, Classification, Unsupervised Learning, Optimization, or Causal Inference** — it sits beneath all of them.

---

## Overlaps & ownership

Probability Foundations is foundational, so most "overlaps" are really *clean hand-offs*: this track builds the object, a downstream track applies it. The contract:

| Shared / adjacent topic | **Owner** | Rationale & hand-off |
|---|---|---|
| Sample spaces, axioms, random variables, distributions, expectation, variance, covariance | **Probability** | The base objects. Everyone consumes; nobody re-derives. |
| Conditional probability & Bayes' **for events** | **Probability** (PROB-1) | Inference E4 / Causal / Classification consume it; **Bayes for *parameters*** (posterior ∝ likelihood × prior) is **Inference's** (E4) — different altitude, written there. |
| Conditional **expectation** `E[Y|X]` and "best predictor" | **Probability** (PROB-9) | Built here; **Regression** consumes it (R0/R23) as the thing it estimates, and **Causal Inference** consumes it for conditioning — neither re-derives it. |
| The named **distributions** (Bernoulli…exponential family) | **Probability** (PROB-11–PROB-16) | Catalogued once here. Regression (R17/R19/R18), Inference (B1/C2/E4) link rather than restate. |
| **Chebyshev / Markov** inequalities | **Probability** (PROB-19) | Built here; **Inference A2** uses Chebyshev to *prove the LLN* — the **LLN/CLT themselves are Inference's**, by their explicit request. Clean seam: Probability supplies the inequality and the convergence *modes*; Inference supplies the limit *theorems*. |
| **Modes of convergence** | **Probability** (PROB-21) | The definitions and hierarchy live here; the theorems that produce convergence (LLN, CLT, MLE asymptotics) live in **Inference** (A2, B4). |
| **MGF / characteristic functions** | **Probability** (PROB-20) | Built here as transform machinery; Inference A2 uses them in the CLT proof. |
| **Covariance matrices, PSD-ness, linear transforms of random vectors** | **shared with Geometry of Data** | **Probability owns the *random-vector* mean/covariance and the `AΣAᵀ` identity** (PROB-17–PROB-18, the form Regression R6 needs); **Geometry of Data owns the *deterministic* linear-algebra theory** (eigendecomposition, SVD, PD matrices, projection). The covariance matrix is the natural bridge: its probabilistic meaning here, its spectral analysis there (and in Unsupervised Learning's PCA). |
| **Empirical CDF & sampling with replacement** | **Probability** (PROB-22) | The object and the plug-in principle here; **the bootstrap *method*** is **Inference's** (E1). |
| **Order statistics & uniform null p-values** | **Probability** (PROB-23) | Built here; **Inference D5** (multiple comparisons) consumes the uniform-p-value fact. |
| **Combinatorics of permutations** | **Probability** (PROB-10) | Built here; **Inference E3** (permutation tests) consumes the count. |
| **Exponential family** | **Probability** (PROB-16) | The distributional *form* and its `A′=E[T]` moments here; **Regression R18** (GLM link/canonical form) and **Inference** (sufficiency) apply it. |
| **Variance as a sum of squares** | **Probability** (PROB-6) | Built here exactly as Regression R3 requests; Regression uses it in the SST=SSR+SSE decomposition. |

**One-line ownership rule:** *Probability owns the random objects, the named distributions, and the convergence/transform machinery; every downstream track links to those objects and applies them to its own deliverable, and the limit theorems (LLN/CLT/MLE asymptotics) live with Inference even though their raw materials (Chebyshev, convergence modes, MGFs) are built here.*

---

### Design notes / opinionated calls
- **PROB-0–PROB-2 are deliberately unglamorous** — sample spaces, conditioning, and the CDF — because every track in the series silently assumes them. Putting them at the true entry point is what lets every other track honor the Calc-1 floor.
- **Conditional expectation (PROB-9) is placed as a hinge, not a footnote.** `E[Y|X]` as the best MSE predictor is the single result that makes Regression's entire "we are estimating `E[Y|X]`" framing rigorous rather than asserted — so it gets a full, possibly split, article.
- **The catalog (PROB-10–PROB-16) is one contiguous movement** so the family resemblances (binomial→Poisson→normal limits; gamma→chi-square; everything→exponential family) land as a connected story, not sixteen isolated formula sheets.
- **The LLN and CLT are intentionally NOT here.** They are *theorems of inference about samples*, and the Statistical Inference track explicitly requests only their raw materials (Chebyshev PROB-19, convergence modes PROB-21, MGF/CF PROB-20). Building the inequality and the convergence vocabulary here, and the limit theorems there, is the cleanest possible seam and avoids double-ownership.
- **Random vectors (PROB-17–PROB-18) stop exactly where linear-algebra *theory* begins.** We build the mean vector, covariance matrix, and `AΣAᵀ` because Regression R6 needs them by name — but eigen/SVD/projection theory is handed to Geometry of Data, so the two tracks meet at the covariance matrix without overlapping.

This roadmap is **24 articles** (PROB-0–PROB-23) in five movements. Several deep articles (PROB-9, PROB-13, PROB-14, PROB-15, PROB-17, PROB-20, PROB-21) carry pre-marked split seams should they push the 30-page ceiling during drafting. Every probability prerequisite requested by the existing Regression and Statistical Inference tracks is supplied by exactly one article here.
