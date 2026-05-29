# Core Sample — Track Roadmap: **Regression**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

*An inch wide, a mile deep. From a single line through a cloud of points, all the way down to letting the data choose the curve.*

This track is deliberately decomposed into many razor-focused articles. The spine is: **build the line → understand it as projection → make it multivariate → judge it statistically → fix it when assumptions break → bend it (regularize, generalize, go nonparametric)**. Every above-the-floor tool (linear algebra, probability, optimization, inference) is either built inside an article or named as a cross-track prerequisite at the exact point it is needed.

---

## The flow diagram

```
                          [R0] Why a Line? (the regression question)
                                        │
                                        ▼
                          [R1] OLS, One Predictor (calculus derivation)
                                        │
                  ┌─────────────────────┼─────────────────────┐
                  ▼                                            ▼
   [R2] What the Line Assumes                    [R3] How Good Is the Fit?
   (the Gauss–Markov conditions)                 (R², residuals, RMSE)
                  │                                            │
                  └─────────────────────┬─────────────────────┘
                                        ▼
                          [R4] Regression as Projection
                          (geometry: ŷ = Hy, the hat matrix)   ◄── needs Geometry track
                                        │
                                        ▼
                          [R5] Multiple Regression (the normal equations in matrix form)
                                        │
              ┌─────────────────────────┼──────────────────────────┐
              ▼                          ▼                          ▼
   [R6] Sampling Distribution    [R7] Multicollinearity      [R8] Categorical &
   of β̂ (Gauss–Markov + var)     (when X'X goes bad)         Interaction Terms
              │                          │                   (encoding, design matrix)
              ▼                          │                          │
   [R9] Inference on Coefficients        │                          │
   (t, F, confidence/prediction          │                          │
    intervals, hypothesis tests)         │                          │
              │                          │                          │
              └──────────────┬───────────┴──────────────────────────┘
                             ▼
              [R10] Diagnostics & Leverage
              (residual analysis, influence, outliers)
                             │
              ┌──────────────┼───────────────────────────────┐
              ▼              ▼                                 ▼
  [R11] When Variance     [R12] Maximum-Likelihood       [R13] Bias–Variance &
  Isn't Constant          View of Regression             Model Selection
  (WLS / GLS, robust SE)  (OLS = Gaussian MLE)           (AIC/BIC, CV, subset)
                             │                                 │
        ┌────────────────────┘                                 │
        ▼                                                       │
  ┌─────────────────── REGULARIZATION SUB-BRANCH ──────────┐    │
  │ [R14] Ridge Regression (the bias you pay on purpose)    │◄───┘
  │            │                                            │
  │            ▼                                            │
  │ [R15] Lasso & the Geometry of Sparsity                  │
  │            │                                            │
  │            ▼                                            │
  │ [R16] Elastic Net & the Regularization Path             │
  └─────────────────────────────────────────────────────────┘
        │
        │   ┌──────────────────── GLM SUB-BRANCH ──────────────────┐
        │   │ [R17] Logistic Regression (regression for a yes/no)   │
        │   │            │                                          │
        │   │            ▼                                          │
        │   │ [R18] The GLM Framework (link + exponential family)   │
        │   │            │                                          │
        │   │            ▼                                          │
        │   │ [R19] Poisson & Count Regression                      │
        │   └────────────────────────────────────────────────────┘
        │
        ▼
  ┌──────────────── NONPARAMETRIC / FLEXIBLE SUB-BRANCH ───────────────┐
  │ [R20] Polynomial & Basis-Function Regression (still linear in β)     │
  │            │                                                         │
  │            ▼                                                         │
  │ [R21] Regression Splines (piecewise polynomials, knots)             │
  │            │                                                         │
  │            ▼                                                         │
  │ [R22] Smoothing Splines (the roughness penalty)                     │
  │            │                                                         │
  │            ▼                                                         │
  │ [R23] Kernel Regression (Nadaraya–Watson: a local weighted mean)    │
  │            │                                                         │
  │            ▼                                                         │
  │ [R24] Local Regression (LOESS / local polynomials)                  │
  │            │                                                         │
  │            ▼                                                         │
  │ [R25] The Bias–Variance Trade-off of the Bandwidth (smoothing param)│
  │            │                                                         │
  │            ▼                                                         │
  │ [R26] Generalized Additive Models (GAMs: sum of smooths)            │
  └─────────────────────────────────────────────────────────────────────┘
```

The three sub-branches (Regularization, GLM, Nonparametric) all hang off the same trunk (R1–R13) and can be read in parallel once the trunk is done. See the branching note at the end.

---

## The trunk: building the line and understanding it

### R0 — Why a Line? The Regression Question
1. **The one question:** What problem is regression actually solving when we "fit a line to data," and why a line first?
2. **Scope / inside:**
   - The prediction-vs-explanation framing: estimating `E[Y | X]` as the thing we're after.
   - Why "draw the best line through the cloud" is ill-posed until we define *best* (sets up the loss-function choice).
   - Historical *why*: Galton's regression to the mean, Legendre/Gauss and least squares for astronomy/geodesy — the original motivating problem.
3. **Assumes:** Only the floor (functions, a scatterplot, the idea of an average).
4. **Sets up:** R1 (commits to squared-error loss and derives the line).
5. **Depth:** short (~8–12). Motivational, light on derivation.

### R1 — Ordinary Least Squares, One Predictor
1. **The one question:** Given one predictor, what straight line minimizes squared error, and exactly how do we derive its slope and intercept?
2. **Scope / inside:**
   - Define the squared-error objective `S(β₀,β₁) = Σ(yᵢ − β₀ − β₁xᵢ)²`.
   - Full Calc-1 derivation: partial derivatives set to zero, solve the two normal equations, get `β̂₁ = Sxy/Sxx`, `β̂₀ = ȳ − β̂₁x̄`.
   - The decomposition of the answer in terms of covariance/variance; the fitted line passes through `(x̄, ȳ)`.
   - Worked examples on real bivariate data + the figure of the fitted line and residuals.
3. **Assumes:** R0; floor-level partial differentiation (built inline — "treat the other variable as constant," shown explicitly, since multivariable calc is above the floor and we only need its Calc-1 shadow here).
4. **Sets up:** R2, R3, R4. This is the true entry point.
5. **Depth:** medium (~12–20).

### R2 — What the Line Assumes: The Gauss–Markov Conditions
1. **The one question:** Under what conditions on the errors is the least-squares line actually a good estimator, stated precisely?
2. **Scope / inside:**
   - The model `Y = β₀ + β₁X + ε`; the four classical conditions (linearity, zero-mean errors, constant variance/homoscedasticity, uncorrelated errors), each stated and pictured.
   - What each condition buys and what its violation looks like in a residual plot (forward reference to R10/R11).
   - Distinguish "assumptions for unbiasedness" from "assumptions for efficiency" from "assumptions for inference" — a map the reader carries through the whole track.
3. **Assumes:** R1; **cross-track:** *expectation, variance, and covariance of a random variable* [Probability track]; *the idea of an estimator and bias* [Estimation & Inference track].
4. **Sets up:** R6 (Gauss–Markov theorem proper), R10, R11.
5. **Depth:** medium (~12–20).

### R3 — How Good Is the Fit? R², Residuals, and Error Measures
1. **The one question:** Once we have a line, how do we quantify how well it explains the data — and what do those numbers *not* tell us?
2. **Scope / inside:**
   - The sum-of-squares identity `SST = SSR + SSE`, derived in full (the cross-term vanishes — show why).
   - `R²` as proportion of variance explained; its geometric meaning previewed; why `R²` always rises with more predictors (sets up adjusted `R²`).
   - RMSE/MAE as scale-bearing error measures; Anscombe's quartet as the honest edge case where the same `R²` hides wildly different realities.
3. **Assumes:** R1, R2; **cross-track:** *variance as a sum of squares* [Probability track].
4. **Sets up:** R5 (adjusted R²), R13 (model selection).
5. **Depth:** medium (~12–20).

### R4 — Regression as Projection: The Geometry of Least Squares
1. **The one question:** Why is least squares the *orthogonal projection* of the response vector onto the column space of the predictors, and why does that make it optimal?
2. **Scope / inside:**
   - Reframe `y`, `ŷ`, residual `e` as vectors in ℝⁿ; the fitted vector is the projection of `y` onto `span(1, x)`.
   - Orthogonality of residuals to the column space ⇔ the normal equations — derive the equivalence both directions.
   - The hat matrix `H = X(XᵀX)⁻¹Xᵀ`, `ŷ = Hy`; `H` is the projection matrix (idempotent, symmetric — proven).
   - Why this picture makes multiple regression "the same idea in higher dimensions."
3. **Assumes:** R1; **cross-track (heavy):** *vector spaces, span, subspaces, inner product and orthogonality* and *orthogonal projection onto a subspace* [Geometry of Data / Applied Linear Algebra track]; *matrix inverse and transpose* [same].
4. **Sets up:** R5, R6, R10 (leverage = diagonal of H).
5. **Depth:** deep (~20–30). **Split seam if needed:** cut after the orthogonality-↔-normal-equations equivalence; the hat matrix + idempotency could become a short companion ("The Hat Matrix") if the projection build runs long.

### R5 — Multiple Regression: The Normal Equations in Matrix Form
1. **The one question:** How does least squares generalize to many predictors at once, and what is the closed-form solution `β̂ = (XᵀX)⁻¹Xᵀy`?
2. **Scope / inside:**
   - The design matrix `X`; objective `‖y − Xβ‖²`; full matrix-calculus derivation of the normal equations `XᵀXβ̂ = Xᵀy` (gradient of a quadratic form, shown step by step).
   - When `(XᵀX)⁻¹` exists (full column rank) and what it means when it doesn't (forward ref to R7).
   - Adjusted `R²` and the degrees-of-freedom bookkeeping.
   - Worked example with several real predictors; interpreting a coefficient as "holding the others fixed."
3. **Assumes:** R1, R3, R4; **cross-track:** *matrix multiplication, transpose, inverse, rank* and *gradient of a quadratic form / vector differentiation* [Applied Linear Algebra track]; the projection picture from R4 carries the geometry.
4. **Sets up:** R6, R7, R8, R9, and everything downstream (the matrix form is the lingua franca of the rest of the track).
5. **Depth:** deep (~20–30). **Split seam if needed:** vector-differentiation rules (`∂(βᵀAβ)/∂β`, `∂(bᵀβ)/∂β`) could be peeled into a tiny prerequisite or an appendix; cut there if the derivation crowds the examples.

---

## Statistical judgment: trusting the coefficients

### R6 — The Sampling Distribution of β̂ and the Gauss–Markov Theorem
1. **The one question:** Treating the data as one draw, what is the distribution of the estimated coefficients, and in what precise sense is OLS the *best* linear unbiased estimator?
2. **Scope / inside:**
   - `β̂` as a linear function of `y`; derive `E[β̂] = β` (unbiasedness) and `Var(β̂) = σ²(XᵀX)⁻¹`.
   - Statement and full proof of the **Gauss–Markov theorem** (OLS is BLUE) — the "no other linear unbiased estimator has smaller variance" argument.
   - Estimating `σ²` with `s² = SSE/(n−p)`; why the divisor is `n−p` (degrees of freedom, tied back to R4 geometry).
3. **Assumes:** R2, R4, R5; **cross-track:** *mean/variance of a random vector, covariance matrix* and *linear transformations of random vectors* [Probability track]; *unbiasedness and estimator efficiency* [Estimation & Inference track].
4. **Sets up:** R9 (inference), R14 (ridge deliberately breaks unbiasedness for lower variance).
5. **Depth:** deep (~20–30).

### R7 — Multicollinearity: When XᵀX Goes Bad
1. **The one question:** What happens to the fit and the coefficients when predictors are nearly linearly dependent, and how do we detect and respond to it?
2. **Scope / inside:**
   - Geometric cause: near-collinear columns ⇒ `XᵀX` near-singular ⇒ exploded coefficient variance (tie to `Var(β̂) = σ²(XᵀX)⁻¹`).
   - Variance Inflation Factor, condition number; the honest example where coefficients flip sign with a tiny data change.
   - Remedies preview: drop/combine predictors, or shrink (forward ref to R14 ridge as the principled fix).
3. **Assumes:** R5, R6; **cross-track:** *eigenvalues / condition number of a matrix* [Applied Linear Algebra track].
4. **Sets up:** R14 (ridge as the cure).
5. **Depth:** medium (~12–20).

### R8 — Categorical Predictors and Interaction Terms
1. **The one question:** How do we put non-numeric predictors and "it depends on the combination" effects into a linear model honestly?
2. **Scope / inside:**
   - Dummy/one-hot encoding; the reference category and the dummy-variable trap (perfect collinearity with the intercept — ties to R7).
   - Interaction terms as products of columns; interpreting them; why the design matrix stays linear *in the parameters*.
   - Worked example mixing continuous + categorical predictors with an interaction; visualizing differing slopes.
3. **Assumes:** R5; R7 (for the dummy trap).
4. **Sets up:** R20 (basis functions generalize "build new columns"), R26 (GAMs).
5. **Depth:** medium (~12–20).

### R9 — Inference on Coefficients: t-tests, F-tests, and Intervals
1. **The one question:** How do we test whether a coefficient (or a group of them) matters, and build confidence and prediction intervals?
2. **Scope / inside:**
   - The `t`-statistic for a single coefficient from `Var(β̂)` + estimated `σ²`; where the `t`-distribution and `n−p` df come from.
   - The `F`-test for nested models / overall significance; partial `F` for groups of coefficients.
   - Confidence interval for a mean response vs. **prediction interval** for a new observation — derive why the latter is wider.
   - The multiple-testing / p-hacking caution as the edge-of-applicability warning.
3. **Assumes:** R6; **cross-track:** *normal distribution, t- and F-distributions and where they arise* and *hypothesis testing, p-values, confidence intervals* [Estimation & Inference track].
4. **Sets up:** R13 (model selection contrasts inference-based vs. predictive selection).
5. **Depth:** deep (~20–30). **Split seam if needed:** cut after the single-coefficient `t`-test; "The F-test and Comparing Nested Models" can stand alone.

### R10 — Diagnostics, Leverage, and Influence
1. **The one question:** After fitting, how do we read the residuals to find where the model is lying, and which points are secretly steering the fit?
2. **Scope / inside:**
   - Residual plots: detecting nonlinearity, heteroscedasticity, non-normality (QQ plots).
   - **Leverage** as the diagonal of the hat matrix `H` (direct payoff from R4); standardized/studentized residuals.
   - **Cook's distance** and influence; the honest example where one high-leverage outlier dominates everything.
3. **Assumes:** R4 (hat matrix), R5, R6; R9 for studentization.
4. **Sets up:** R11 (heteroscedasticity fix), the whole "when does this break" muscle for the rest of the track.
5. **Depth:** medium (~12–20).

### R11 — When Variance Isn't Constant: WLS, GLS, and Robust Standard Errors
1. **The one question:** When the homoscedasticity/independence assumptions fail, how do we still get efficient estimates and trustworthy standard errors?
2. **Scope / inside:**
   - Weighted least squares: re-derive the normal equations with a weight matrix `W`; `β̂ = (XᵀWX)⁻¹XᵀWy`.
   - Generalized least squares for correlated errors (covariance `Σ`); the whitening transformation that turns GLS back into OLS.
   - Heteroscedasticity-robust ("sandwich") standard errors as the fix when you can't model the variance.
3. **Assumes:** R6, R10; **cross-track:** *positive-definite matrices and matrix square roots / Cholesky* [Applied Linear Algebra track].
4. **Sets up:** R18 (GLM's iteratively reweighted least squares is WLS in a loop).
5. **Depth:** deep (~20–30).

### R12 — The Maximum-Likelihood View of Regression
1. **The one question:** Why does minimizing squared error coincide with maximum likelihood, and what does that reframing unlock?
2. **Scope / inside:**
   - Assume Gaussian errors; write the likelihood; show maximizing it ⇒ minimizing SSE — OLS = Gaussian MLE, derived in full.
   - The MLE of `σ²` and why it differs from the unbiased `s²` (divisor `n` vs `n−p`).
   - Why this matters: it's the doorway to logistic/Poisson/GLM where there's no "sum of squares" to minimize.
3. **Assumes:** R5, R6; **cross-track:** *likelihood, log-likelihood, and the MLE principle* [Estimation & Inference track]; *the Gaussian density* [Probability track].
4. **Sets up:** R14 (ridge = MAP / penalized likelihood), R17–R19 (GLMs are MLE), R22 (smoothing-spline penalized likelihood).
5. **Depth:** medium (~12–20).

### R13 — Bias, Variance, and Choosing a Model
1. **The one question:** How do we decide *which* predictors and how much complexity, trading underfitting against overfitting in a principled way?
2. **Scope / inside:**
   - The bias–variance decomposition of expected prediction error, derived in full.
   - In-sample criteria: adjusted `R²`, Mallows' `Cp`, **AIC/BIC** (stated, with the likelihood link from R12); out-of-sample: **cross-validation** (k-fold, LOOCV, and the LOOCV-via-hat-matrix shortcut).
   - Stepwise/subset selection and an honest warning about its instability (motivates regularization).
3. **Assumes:** R3, R6, R12; **cross-track:** *expected prediction error / risk* and *resampling* [Estimation & Inference track].
4. **Sets up:** the entire Regularization sub-branch (R14–R16); the bandwidth/smoothing story (R25).
5. **Depth:** deep (~20–30). **Split seam if needed:** cut after the bias–variance decomposition; "Cross-Validation and Information Criteria" can be its own article.

---

## Sub-branch A — Regularization (shrinkage)

### R14 — Ridge Regression: The Bias You Pay on Purpose
1. **The one question:** How does adding an `ℓ₂` penalty cure ill-conditioning and reduce variance, and what does it cost?
2. **Scope / inside:**
   - Objective `‖y − Xβ‖² + λ‖β‖²`; derive `β̂_ridge = (XᵀX + λI)⁻¹Xᵀy` — note it's invertible even when `XᵀX` isn't (direct answer to R7).
   - Bias–variance trade-off as `λ` grows; the shrinkage seen in the SVD/eigenbasis.
   - Bayesian reading: ridge = MAP with a Gaussian prior (ties to R12); choosing `λ` by CV.
3. **Assumes:** R5, R6, R7, R12, R13; **cross-track:** *SVD / eigendecomposition* [Applied Linear Algebra]; *prior/posterior, MAP* [Estimation & Inference].
4. **Sets up:** R15, R16.
5. **Depth:** deep (~20–30).

### R15 — Lasso and the Geometry of Sparsity
1. **The one question:** Why does the `ℓ₁` penalty drive coefficients exactly to zero, doing variable selection, while ridge never does?
2. **Scope / inside:**
   - Objective with `‖β‖₁`; the constraint-region picture (diamond vs. circle) explaining corner solutions geometrically.
   - No closed form: soft-thresholding and coordinate descent (the optimization built to the floor's level, with the subgradient idea introduced carefully).
   - When lasso shines vs. fails (correlated predictors → arbitrary pick among them).
3. **Assumes:** R14; **cross-track:** *convex functions and subgradients*, *coordinate descent* [Optimization track].
4. **Sets up:** R16.
5. **Depth:** deep (~20–30). **Split seam if needed:** the optimization (soft-thresholding/coordinate descent) can split off as "Solving the Lasso" if the geometry + statistics already fill the budget.

### R16 — Elastic Net and the Regularization Path
1. **The one question:** How do we blend ridge and lasso, and how do the coefficients evolve as the penalty strength sweeps from heavy to none?
2. **Scope / inside:**
   - Elastic-net penalty as a convex combination; why it handles correlated-predictor groups better than pure lasso.
   - The full regularization path; warm starts; choosing `(λ, α)` by cross-validation.
   - The honest trade-off summary table: OLS vs ridge vs lasso vs elastic net — when to reach for which.
3. **Assumes:** R14, R15.
4. **Sets up:** (Hand-off to a future Machine Learning track; terminal within Regression.)
5. **Depth:** medium (~12–20).

---

## Sub-branch B — Generalized Linear Models

### R17 — Logistic Regression: Regression for a Yes/No
1. **The one question:** How do we model the probability of a binary outcome with a linear predictor, and why the log-odds?
2. **Scope / inside:**
   - The logit/sigmoid link and why a plain linear model fails for probabilities (unbounded, heteroscedastic).
   - The likelihood for Bernoulli data; log-likelihood; deriving the score equations — no closed form.
   - Fitting via Newton-Raphson / IRLS; interpreting coefficients as odds ratios; classification threshold vs. probability output.
3. **Assumes:** R12 (MLE view), R11 (reweighting); **cross-track:** *Bernoulli/binomial distribution* [Probability]; *Newton's method / gradient methods* [Optimization].
4. **Sets up:** R18.
5. **Depth:** deep (~20–30). **Split seam if needed:** "Fitting Logistic Regression by IRLS" can split from the modeling/interpretation half.

### R18 — The GLM Framework: Link Functions and the Exponential Family
1. **The one question:** What is the single framework that contains linear, logistic, and Poisson regression as special cases?
2. **Scope / inside:**
   - The exponential family form; the systematic component (linear predictor), random component, and link function.
   - The canonical link and why it simplifies the score equations; IRLS as the unifying fitting algorithm (WLS-in-a-loop, payoff from R11).
   - Deviance as the GLM generalization of SSE; deviance-based model comparison.
3. **Assumes:** R11, R12, R17; **cross-track:** *exponential family of distributions* [Probability / Estimation track].
4. **Sets up:** R19; R26 (GAMs extend GLMs with smooths).
5. **Depth:** deep (~20–30).

### R19 — Poisson and Count Regression
1. **The one question:** How do we model count outcomes, and what do we do when the counts are more dispersed than Poisson allows?
2. **Scope / inside:**
   - Poisson GLM with log link; the equidispersion assumption (`mean = variance`).
   - Overdispersion: quasi-Poisson and negative-binomial as the honest fixes; offsets for exposure/rate data.
   - Worked example on real count data showing the overdispersion failure and its remedy.
3. **Assumes:** R18; **cross-track:** *Poisson and negative-binomial distributions* [Probability track].
4. **Sets up:** (Terminal in GLM branch; feeds R26.)
5. **Depth:** medium (~12–20).

---

## Sub-branch C — Flexible & Nonparametric Regression

### R20 — Polynomial and Basis-Function Regression (Still Linear in β)
1. **The one question:** How do we fit curves while keeping all the linear-model machinery, by transforming the predictors instead of the parameters?
2. **Scope / inside:**
   - Polynomial features and general basis expansions `Σ βⱼ φⱼ(x)`; the key insight: still linear in `β`, so R5–R9 all apply unchanged.
   - Why high-degree polynomials behave badly (Runge phenomenon, wild tails) — the honest motivation for *local* basis functions.
   - Bias–variance as degree grows (ties to R13).
3. **Assumes:** R5, R8, R13.
4. **Sets up:** R21 (splines = better local bases).
5. **Depth:** medium (~12–20).

### R21 — Regression Splines: Piecewise Polynomials with Knots
1. **The one question:** How do we get local flexibility without the global instability of high-degree polynomials, by stitching low-degree pieces together smoothly?
2. **Scope / inside:**
   - Truncated power basis and B-spline basis; continuity/smoothness constraints at knots, derived.
   - Natural cubic splines and why the linear-tail constraint tames the boundary.
   - Knot placement and count as the complexity dial; fit via the same least-squares solve.
3. **Assumes:** R20; **cross-track:** (none new beyond linear algebra from R5).
4. **Sets up:** R22 (penalize instead of choosing knots).
5. **Depth:** deep (~20–30).

### R22 — Smoothing Splines: The Roughness Penalty
1. **The one question:** What if instead of choosing knots we put a knot everywhere and penalize wiggliness — what curve does that produce?
2. **Scope / inside:**
   - The penalized objective `Σ(yᵢ − f(xᵢ))² + λ∫f''(x)²dx`; the remarkable result that the minimizer is a natural cubic spline (stated, with the variational intuition built carefully).
   - The smoother matrix `S_λ`; **effective degrees of freedom** as `trace(S_λ)` (echo of the hat matrix from R4/R10).
   - Choosing `λ` by generalized cross-validation.
3. **Assumes:** R21, R13; R12 (penalized-likelihood reading); **cross-track:** *functionals and the calculus of variations, gently* [Optimization track] — built inline to the floor's level, flagged as the one place we touch above-floor calculus.
4. **Sets up:** R25 (smoothing parameter selection), R26 (smooths inside GAMs).
5. **Depth:** deep (~20–30). **Split seam if needed:** the variational "why it's a natural cubic spline" result can split into a companion if the derivation strains the ceiling.

### R23 — Kernel Regression: A Local Weighted Mean (Nadaraya–Watson)
1. **The one question:** What if we estimate `E[Y|X=x]` directly as a weighted average of nearby `y`'s, with no global form at all?
2. **Scope / inside:**
   - From "the conditional mean" to the Nadaraya–Watson estimator; kernels (Gaussian, Epanechnikov) and the bandwidth.
   - Derive it as locally-weighted least squares of *degree zero* (a local constant) — the bridge to R24.
   - Boundary bias as the honest failure mode (the estimator flattens at the edges).
3. **Assumes:** R1, R3; **cross-track:** *conditional expectation* [Probability track]; *kernels / weighting functions* (built inline).
4. **Sets up:** R24, R25.
5. **Depth:** medium (~12–20).

### R24 — Local Regression: LOESS and Local Polynomials
1. **The one question:** How does fitting a small weighted regression in a moving window beat a local average, especially at the boundaries?
2. **Scope / inside:**
   - Local linear/quadratic regression; the weighted-least-squares solve at each target point (direct reuse of R11's WLS).
   - Why local linear fixes the boundary bias of Nadaraya-Watson — derived.
   - Span/bandwidth as the complexity knob; robustness iterations (LOESS); computational cost as the honest downside.
3. **Assumes:** R11, R23.
4. **Sets up:** R25.
5. **Depth:** deep (~20–30).

### R25 — The Bandwidth Is the Model: Bias-Variance of Smoothing
1. **The one question:** How do we choose the bandwidth/span, and why is that choice the entire ballgame for any local method?
2. **Scope / inside:**
   - Asymptotic bias `∝ h²` and variance `∝ 1/(nh)`; the optimal-`h` rate that balances them (derived to the level the floor allows).
   - The curse of dimensionality for local methods — why kernel/local regression collapses in high dimensions (the honest "don't use this when" boundary for the whole sub-branch).
   - Practical selection: plug-in vs. cross-validation; comparison table of spline vs. kernel vs. local.
3. **Assumes:** R13, R22, R23, R24.
4. **Sets up:** R26 (motivates additive structure as the escape from the curse).
5. **Depth:** deep (~20–30).

### R26 — Generalized Additive Models: A Sum of Smooths
1. **The one question:** How do we keep nonparametric flexibility in many dimensions by adding one-dimensional smooths instead of one joint smooth?
2. **Scope / inside:**
   - The additive model `g(E[Y]) = β₀ + Σ fⱼ(xⱼ)`; fitting by **backfitting**; the GLM link reused (payoff from R18) for non-Gaussian responses.
   - Why additivity dodges the curse of dimensionality (from R25) — and what it gives up (no interactions unless added explicitly, tie to R8).
   - Interpretability as the headline strength; partial-dependence-style plots of each `fⱼ`.
3. **Assumes:** R8, R18, R22, R25.
4. **Sets up:** Terminal node of the track — hands off to a Machine Learning / trees track (boosting, GAMs vs. gradient-boosted trees) and a Time Series track.
5. **Depth:** deep (~20–30).

---

## Cross-track prerequisites (belong to OTHER tracks)

These are pulled in at the points noted. Regression does **not** build them; they are named so the prerequisite chain (§1.4) is explicit.

**From the Geometry of Data / Applied Linear Algebra track**
- *Vector spaces, span, subspaces, inner products, orthogonality* — needed at **R4**.
- *Orthogonal projection onto a subspace* — needed at **R4** (this is the spine of the geometric view).
- *Matrix multiplication, transpose, inverse, rank* — needed at **R5**.
- *Gradient of a quadratic form / vector differentiation* (`∂(βᵀAβ)/∂β`) — needed at **R5**.
- *Eigenvalues, condition number of a matrix* — needed at **R7**.
- *Positive-definite matrices, matrix square root / Cholesky* — needed at **R11**.
- *Singular value decomposition / eigendecomposition* — needed at **R14** (ridge shrinkage in the SVD basis).

**From the Probability track**
- *Expectation, variance, covariance of a random variable* — needed at **R2**.
- *Variance as a sum of squares* — needed at **R3**.
- *Mean/variance/covariance matrix of a random vector; linear transforms of random vectors* — needed at **R6**.
- *Normal (Gaussian) distribution and its density* — needed at **R9, R12**.
- *t-, F-, and chi-squared distributions and where they arise* — needed at **R9**.
- *Bernoulli/binomial; Poisson; negative-binomial distributions* — needed at **R17, R19**.
- *Exponential family of distributions* — needed at **R18**.
- *Conditional expectation `E[Y|X]`* — needed at **R23** (and conceptually as early as R0).

**From the Estimation & Inference track**
- *Estimators, bias, efficiency* — needed at **R2, R6**.
- *Hypothesis testing, p-values, confidence intervals* — needed at **R9**.
- *Likelihood, log-likelihood, the MLE principle* — needed at **R12**.
- *Prior/posterior and MAP estimation* — needed at **R14** (Bayesian reading of ridge).
- *Expected prediction error / risk; cross-validation as a resampling method* — needed at **R13**.

**From the Optimization track**
- *Convex functions and subgradients* — needed at **R15** (lasso).
- *Coordinate descent* — needed at **R15**.
- *Newton's method / gradient methods* — needed at **R17** (logistic fitting).
- *Calculus of variations (gentle)* — needed at **R22** (smoothing splines); partially built inline since it's the one above-floor calculus touch.

---

## Where the track branches

The track is a **trunk plus three parallel sub-branches**, and that shape is deliberate.

- **Trunk (R0–R13)** must be read in order. It ends at **R13 (bias–variance + model selection)**, which is the natural fork: everything after R13 is a different *answer* to "the simple linear model isn't enough."

- **Three parallel branches off the trunk, readable in any order:**
  - **Regularization (R14–R16)** — keep the linear model, *shrink* the coefficients. Branch trigger: R7 (multicollinearity) + R13 (overfitting). Closest sibling: feeds a future ML track.
  - **GLMs (R17–R19)** — keep linearity in the predictor, change the *response distribution*. Branch trigger: R12 (the MLE reframing is the gateway).
  - **Nonparametric/flexible (R20–R26)** — abandon the global functional form, let the *data choose the curve*. Branch trigger: R20 (basis functions) growing out of R13's complexity question.

- **The branches reconverge** at **R26 (GAMs)**, which deliberately fuses the GLM link function (from the GLM branch) with smooth terms (from the nonparametric branch) — the single best place to end the track because it requires command of two branches at once.

- **Natural earlier sub-split inside the trunk:** R4 (geometry) and R5 (matrix multiple regression) are the heaviest linear-algebra lift. If the cross-track Applied Linear Algebra prerequisites aren't yet written, R4–R6 form a coherent "linear-algebra-of-regression" mini-arc that can be drafted as a unit once those prerequisites land.

---

### Design notes / opinionated calls
- **R0 is intentionally a short motivator, not a derivation** — it exists so the *why* (§1.1) has a home before the algebra of R1, and so "regression to the mean" is demystified up front rather than left as folklore.
- **Projection (R4) comes before multiple regression (R5) on purpose.** The geometry makes the matrix normal equations feel inevitable rather than dropped from the sky, and it pays off three more times (degrees of freedom in R6, leverage in R10, effective df in R22).
- **The MLE article (R12) is placed as a hinge, not an afterthought.** It is the single prerequisite that makes both the GLM branch and the regularization-as-MAP and smoothing-spline branches feel like one idea instead of three unrelated tricks.
- **R23 (kernel) before R24 (local) and both before R25 (bandwidth)** so that "the bandwidth is the real model" lands as a punchline the reader has already half-derived twice.

This roadmap is **27 articles** (R0–R26). The trunk is 14, and each sub-branch is 3–7. Several deep articles (R4, R5, R9, R15, R17, R22) carry pre-marked split seams should they push the 30-page ceiling during drafting.
