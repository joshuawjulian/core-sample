# Core Sample — Track Roadmap: **Optimization**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

*An inch wide, a mile deep. From "set the derivative to zero" all the way down to the algorithms that train every model in the rest of the series.*

This is a **foundational, load-bearing track.** Most other tracks fit a model by *minimizing something* — squared error, a negative log-likelihood, a penalized loss. They are allowed to say "minimize this" and link here. Optimization owns the *machinery of minimization itself*: what an optimization problem is, when a stationary point is actually a minimum, how to descend toward one when there's no closed form, how convexity turns "a local minimum" into "the global minimum," how to honor constraints, and the specific algorithms (GD/SGD, Newton, coordinate descent, proximal methods) that ML training relies on.

The track is built so it can be read straight through, but it is also a **supply depot**: every cross-track prerequisite that Regression and Statistical Inference request — *convex functions & subgradients*, *coordinate descent*, *Newton's method*, *gradient descent / gradient ascent*, and *a gentle calculus of variations* — is supplied here at a named article, and is listed in the "What this track supplies to others" section at the end.

**Dependence on Geometry of Data.** This track does **not** re-derive the multivariable-calculus objects it runs on. The **gradient**, the **Hessian**, **directional derivatives**, **quadratic forms** `xᵀAx`, and **positive-(semi)definiteness** are owned by the *Geometry of Data / Applied Linear Algebra* track and are named as cross-track prerequisites at the exact article where each is first needed. Optimization assumes the reader can *compute* a gradient and a Hessian; it teaches what to *do* with them.

---

## The flow diagram

```
                    [OPTM-00] What Is an Optimization Problem?
                    (objective, argmin, feasible set — the vocabulary)
                                     │
                                     ▼
                    [OPTM-01] 1-D Minimization: the Derivative Test
                    (f'(x)=0, second-derivative test, the Calc-1 floor)
                                     │
                                     ▼
                    [OPTM-02] Minimizing in Many Variables: ∇f = 0
                    (stationary points, the Hessian test)   ◄── needs Geometry track
                                     │
              ┌──────────────────────┼───────────────────────────┐
              ▼                                                   ▼
  ┌──────── CONVEXITY SPINE ────────┐                  ┌──── DESCENT SPINE ─────┐
  │ [OPTM-03] Convex Sets               │                  │ [OPTM-06] Gradient Descent   │
  │        │                        │                  │   (the core algorithm)  │
  │        ▼                        │                  │        │                │
  │ [OPTM-04] Convex Functions          │                  │        ▼                │
  │   (and why convexity is the     │                  │ [OPTM-07] Step Size & the    │
  │    dividing line of the field)  │                  │   Convergence of GD     │
  │        │                        │                  │   (L-smoothness, rates) │
  │        ▼                        │                  │        │                │
  │ [OPTM-05] Subgradients              │                  │        ▼                │
  │   (calculus for kinks: |x|)     │                  │ [OPTM-08] Momentum &         │
  └─────────────────────────────────┘                  │   Accelerated GD        │
              │           │                             │        │                │
              │           │                             │        ▼                │
              │           │                             │ [OPTM-09] Newton's Method &  │
              │           │                             │   2nd-Order Methods     │
              │           │                             │   (incl. Gauss–Newton,  │
              │           │                             │    quasi-Newton/BFGS)   │
              │           │                             └────────────────────────┘
              │           │                                       │
              │           └───────────────┬───────────────────────┤
              │                           ▼                       ▼
              │              [OPTM-10] Coordinate Descent    [OPTM-11] Stochastic Gradient
              │              (one variable at a time;     Descent (SGD)
              │               lasso soft-thresholding)    (minibatches, noise, rates)
              │                                                   │
              │                                                   ▼
              │                                          [OPTM-12] Adaptive & Modern
              │                                          ML Optimizers
              │                                          (AdaGrad, RMSProp, Adam)
              ▼
  ┌──────── CONSTRAINED OPTIMIZATION ────────┐
  │ [OPTM-13] Optimizing Under Constraints:       │
  │        Lagrange Multipliers (equalities)  │
  │                  │                         │
  │                  ▼                         │
  │ [OPTM-14] Inequalities & the KKT Conditions   │
  │                  │                         │
  │                  ▼                         │
  │ [OPTM-15] Duality: the Problem Behind          │
  │        the Problem                         │
  │                  │                         │
  │                  ▼                         │
  │ [OPTM-16] Proximal & Projected Methods         │
  │   (proximal gradient / ISTA; the bridge    │
  │    from subgradients to lasso solvers)     │
  └────────────────────────────────────────────┘
                    │
                    ▼
  [OPTM-17] Optimizing Over Functions: a Gentle Calculus of Variations
  (Euler–Lagrange; the smoothing-spline objective ∫f''² )
```

Reading order is top-to-bottom, but the **Convexity spine (OPTM-03–OPTM-05)** and the **Descent spine (OPTM-06–OPTM-09)** are genuinely parallel after OPTM-02 and can be read in either order; they reconverge at the algorithm articles OPTM-10–OPTM-12. See the branching note at the end.

---

## The foundation: what minimizing even means

### OPTM-00 — What Is an Optimization Problem?
1. **The one question:** When we say "find the best" — the best line, the best parameters, the best policy — what is the precise mathematical object we are after?
2. **Scope / inside:**
   - The anatomy of an optimization problem: the **decision variable** `x`, the **objective** `f(x)`, the **feasible set** `C`, and the statement `minimize f(x) subject to x ∈ C`.
   - `min` vs **`argmin`** (the value vs. the location); maximization as `min` of `−f`; global vs local minima, defined and pictured.
   - Existence of a minimizer (the idea behind "closed and bounded ⇒ a minimum exists") stated at the floor's level; why some problems have no minimizer (unbounded, open feasible set) as the first honest edge case.
   - Real framings: least squares as "minimize total squared error," MLE as "maximize likelihood," a budget allocation as a constrained problem.
3. **Assumes:** Only the floor (functions, a graph, the idea of a largest/smallest value on an interval).
4. **Sets up:** OPTM-01 (the 1-D solution method), and the vocabulary every later article uses.
5. **Depth:** short (~8–12). Motivational, almost no derivation.

### OPTM-01 — One-Dimensional Minimization: the Derivative Test
1. **The one question:** For a function of a single variable, exactly how does calculus locate a minimum, and when does it fail to?
2. **Scope / inside:**
   - **First-order condition** `f'(x) = 0`: derived as "the tangent is flat at an interior optimum," with the full why (a nonzero slope means you can still go downhill).
   - **Second-derivative test** `f''(x) > 0`; the inconclusive `f''=0` case (e.g. `x⁴`); minima at endpoints where the derivative is *not* zero.
   - A first taste of *iterative* search: bisection / golden-section as "what you do when you can't solve `f'(x)=0` in closed form" — the seed of the whole descent story.
   - Worked examples: minimizing a quadratic cost by hand; a 1-D negative log-likelihood; a function whose only minimum is at a boundary (the honest "the derivative test alone lies here" case).
3. **Assumes:** OPTM-00; floor-level differentiation (Calc-1 — used directly, not built).
4. **Sets up:** OPTM-02 (the same logic in many variables).
5. **Depth:** short–medium (~10–16).

### OPTM-02 — Minimizing in Many Variables: Setting the Gradient to Zero
1. **The one question:** How does "set the derivative to zero" generalize to a function of many variables, and how do we tell a minimum from a maximum or a saddle?
2. **Scope / inside:**
   - **Stationarity** `∇f(x) = 0` as the multivariate first-order condition; the geometric reading (the gradient is the direction of steepest *ascent*, so a minimum has zero gradient) — derived from the directional-derivative picture.
   - The **Hessian test**: positive-definite ⇒ local min, negative-definite ⇒ local max, indefinite ⇒ **saddle point**; pictured on `x²+y²`, `−x²−y²`, `x²−y²`.
   - Why "stationary" is necessary but not sufficient, and why saddles matter enormously in high-dimensional ML (forward ref to OPTM-11/OPTM-12).
   - Worked example: deriving the OLS normal equations as "∇‖y−Xβ‖² = 0" (the exact move the Regression track links here for).
3. **Assumes:** OPTM-01; **cross-track (heavy):** *the gradient `∇f`, directional derivatives, the Hessian, quadratic forms `xᵀAx`, and positive/negative-definiteness* [Geometry of Data / Applied Linear Algebra track] — used, not re-derived.
4. **Sets up:** the Convexity spine (OPTM-03–OPTM-05, which explains *when* a stationary point is the global min) and the Descent spine (OPTM-06, *how* to reach one without a closed form).
5. **Depth:** medium (~14–20).

---

## Convexity spine — the dividing line of the whole field

### OPTM-03 — Convex Sets
1. **The one question:** What does it mean for a feasible region to have "no dents," and why is that the property that makes optimization tractable?
2. **Scope / inside:**
   - **Convex set** defined: the segment between any two points stays inside. Pictured for half-spaces, balls, polytopes; non-examples (a crescent, a union of two disks).
   - Operations that preserve convexity (intersection, affine image) — proved at the floor's level; the feasible set of linear constraints is convex.
   - **Hyperplanes and half-spaces**; the **separating-hyperplane** idea stated geometrically (the seed of duality in OPTM-15 and of SVM margins in Classification).
3. **Assumes:** OPTM-00; **cross-track:** *vectors, linear combinations, half-spaces* [Geometry of Data track].
4. **Sets up:** OPTM-04 (a convex function is one whose epigraph is a convex set), OPTM-13–OPTM-15 (constraint sets), OPTM-16 (projection onto a convex set).
5. **Depth:** medium (~12–16).

### OPTM-04 — Convex Functions: Why Convexity Is the Whole Ballgame
1. **The one question:** What makes a function convex, and why does convexity turn "we found *a* minimum" into "we found *the* minimum"?
2. **Scope / inside:**
   - Three equivalent definitions, with the equivalences proved: the **chord lies above the graph** (Jensen form), the **first-order/tangent-below** condition `f(y) ≥ f(x) + ∇f(x)ᵀ(y−x)`, and the **second-order** condition (Hessian positive-semidefinite).
   - **The headline theorem:** for a convex function, every stationary point / local minimum is a *global* minimum — proved. This is the article the rest of the series leans on.
   - **Strict vs. strong convexity** (unique minimizer; quadratic lower bound) and why strong convexity is what makes gradient descent fast (forward ref to OPTM-07).
   - Building convex objectives in practice: sums, max, composition rules; recognizing `‖y−Xβ‖²`, the logistic loss, and `‖β‖₁` as convex.
   - **Honest boundary:** non-convex objectives (neural nets, mixtures) where this guarantee evaporates and "a local min is all you get."
3. **Assumes:** OPTM-02, OPTM-03; **cross-track:** *Hessian and positive-semidefiniteness* [Geometry of Data track].
4. **Sets up:** OPTM-05 (subgradients extend this to non-smooth convex functions), OPTM-07 (convergence guarantees assume convexity), OPTM-13–OPTM-15 (convex constrained problems are the well-behaved case).
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the equivalence-of-definitions proof; "Local Minima Are Global: the Payoff of Convexity" can stand alone as a short companion.

### OPTM-05 — Subgradients: Calculus for Functions with Kinks
1. **The one question:** How do we do "set the derivative to zero" for a convex function that isn't differentiable — like `|x|` at the origin?
2. **Scope / inside:**
   - The **subgradient** and **subdifferential** `∂f(x)` defined from the tangent-below inequality of OPTM-04; the picture of "all the lines that stay below the graph at a kink."
   - The subdifferential of `|x|` (the interval `[−1,1]` at 0) and of `‖·‖₁`, derived — the exact objects the lasso needs.
   - The **optimality condition** `0 ∈ ∂f(x)` generalizing `∇f=0`; **soft-thresholding** derived as its solution for `½(x−a)² + λ|x|` (the lasso's per-coordinate update — the result Regression R15 links here for).
   - Why a plain gradient method stalls or chatters at a kink, motivating proximal methods (forward ref to OPTM-16).
3. **Assumes:** OPTM-04; **cross-track:** none new beyond OPTM-02's gradient.
4. **Sets up:** OPTM-10 (coordinate descent for lasso), OPTM-16 (proximal gradient / ISTA). **Supplies** the *subgradients* prerequisite requested by Regression.
5. **Depth:** medium–deep (~16–22).

---

## Descent spine — how to get there when there's no formula

### OPTM-06 — Gradient Descent: Walking Downhill
1. **The one question:** When we can't solve `∇f = 0` in closed form, how do we iteratively step toward a minimum — and why does following the negative gradient work?
2. **Scope / inside:**
   - The update `x_{k+1} = x_k − η ∇f(x_k)`; derived from the first-order Taylor expansion as "the locally steepest-descent direction."
   - **Gradient ascent** as the mirror image (`+η∇f`) for maximization — named explicitly so the Inference track's "maximize the log-likelihood" links here.
   - Walking the iterates downhill on a 2-D contour plot; the role of the **learning rate** `η` (too small = crawl, too large = diverge, shown with figures).
   - Worked examples: GD on a quadratic (where we can compare to the exact answer), and GD fitting logistic regression (no closed form — the case Regression R17 links here for).
3. **Assumes:** OPTM-02; **cross-track:** *gradient, Taylor's theorem (first order)* [Geometry of Data track / Calc-1 floor].
4. **Sets up:** OPTM-07 (when and how fast it converges), OPTM-08 (accelerating it), OPTM-11 (the stochastic version). **Supplies** the *gradient descent / gradient ascent* prerequisite for Regression and Inference.
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the basic algorithm + ascent; "Gradient Descent in Practice (learning-rate tuning, diagnostics)" can spin off.

### OPTM-07 — Step Size and Convergence: Why (and How Fast) Gradient Descent Works
1. **The one question:** Under what conditions does gradient descent actually reach the minimum, how fast, and how do we pick the step size to guarantee it?
2. **Scope / inside:**
   - **L-smoothness** (Lipschitz gradient) defined; the **descent lemma** derived; why `η ≤ 1/L` guarantees the objective decreases every step.
   - **Convergence rates**, derived: `O(1/k)` for convex + smooth, **linear** `O(ρ^k)` for strongly convex; the **condition number** `κ = L/μ` as the thing that governs speed (tie back to ill-conditioning in Regression R7).
   - **Line search** (exact, backtracking/Armijo) as the practical way to choose `η` without knowing `L`.
   - **Honest boundary:** non-convex objectives (only stationarity is guaranteed); pathological curvature (zig-zagging in a narrow valley) that motivates momentum (OPTM-08) and second-order methods (OPTM-09).
3. **Assumes:** OPTM-04 (convexity, strong convexity), OPTM-06; **cross-track:** *eigenvalues / condition number* [Geometry of Data track].
4. **Sets up:** OPTM-08 (momentum attacks the `κ` dependence), OPTM-09 (Newton makes it `κ`-independent), OPTM-11 (SGD's noisier rate).
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the descent lemma; "Convergence Rates of Gradient Descent" (the rate proofs + condition number) can be its own article.

### OPTM-08 — Momentum and Accelerated Gradient Descent
1. **The one question:** How can adding "memory of past steps" make gradient descent dramatically faster without using second derivatives?
2. **Scope / inside:**
   - **Heavy-ball / classical momentum**: the update with a velocity term; the rolling-ball intuition and why it damps the zig-zag of OPTM-07.
   - **Nesterov accelerated gradient**; the improved `O(1/k²)` rate for convex smooth problems stated and motivated (the look-ahead trick), with the optimality intuition.
   - When momentum helps vs. hurts (overshoot, oscillation); how it interacts with the learning rate.
3. **Assumes:** OPTM-06, OPTM-07.
4. **Sets up:** OPTM-12 (Adam = momentum + adaptive scaling), and the practical training recipes used across ML tracks.
5. **Depth:** medium–deep (~16–22).

### OPTM-09 — Newton's Method and Second-Order Optimization
1. **The one question:** How does using *curvature* (the Hessian) let us take far smarter steps than gradient descent — and what does that cost?
2. **Scope / inside:**
   - **Newton's method for root-finding** first (`x − f/f'`), then **Newton for minimization** `x_{k+1} = x_k − H⁻¹∇f`, derived by minimizing the second-order Taylor model exactly.
   - **Quadratic convergence** near the optimum (the why); affine invariance / condition-number independence vs. GD; the cost: forming and inverting `H` (`O(p³)`), and what breaks when `H` is not positive-definite (damping, trust regions).
   - **Gauss–Newton** and the link to **IRLS / Fisher scoring** — the exact algorithm Regression's logistic/GLM articles and Inference's MLE article link here for.
   - **Quasi-Newton (BFGS / L-BFGS):** approximating the Hessian from gradients to get most of the speed at a fraction of the cost — the workhorse for medium-scale problems.
3. **Assumes:** OPTM-02 (Hessian test), OPTM-06, OPTM-07; **cross-track:** *Hessian, matrix inverse, positive-definiteness, solving a linear system* [Geometry of Data track].
4. **Sets up:** consumed by Regression R17 (IRLS) and Inference B2/B4 (computing the MLE). **Supplies** the *Newton's method* prerequisite for both tracks.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after pure Newton; "Quasi-Newton Methods (BFGS & L-BFGS)" can stand alone, and "Gauss–Newton & IRLS" can be a short applied companion.

---

## The algorithms ML training actually runs on

### OPTM-10 — Coordinate Descent: One Variable at a Time
1. **The one question:** Instead of moving all variables together along the gradient, what if we minimize over one coordinate at a time — when is that smart, and when is it the *only* easy option?
2. **Scope / inside:**
   - The **coordinate-descent** scheme; the exact per-coordinate minimization for a quadratic; convergence for smooth convex objectives (and the cautionary non-smooth counterexample where it can stall — and *why lasso is the exception*).
   - **The lasso payoff:** with the non-smooth `ℓ₁` penalty, each coordinate update is **soft-thresholding** (derived in OPTM-05) — making coordinate descent the standard lasso/elastic-net solver. This is the exact article Regression R15 links here for.
   - Why it shines on separable penalties and sparse high-dimensional problems; the honest comparison to GD.
3. **Assumes:** OPTM-05 (subgradient / soft-thresholding), OPTM-06; **cross-track:** none new.
4. **Sets up:** Regression R15/R16 (lasso, elastic net). **Supplies** the *coordinate descent* prerequisite for Regression.
5. **Depth:** medium–deep (~16–22).

### OPTM-11 — Stochastic Gradient Descent: Optimizing on a Budget
1. **The one question:** When the objective is a sum over millions of data points, why do we step using *one* (or a few) at a time, and what does that randomness cost and buy?
2. **Scope / inside:**
   - The finite-sum objective `(1/n)Σ fᵢ`; the **stochastic gradient** as an unbiased estimate of the full gradient (derived); **minibatch** SGD as the variance/cost trade-off.
   - Why SGD needs a **decaying step size** `Σηₖ=∞, Σηₖ²<∞`; the noisy `O(1/k)` (convex) / `O(1/√k)` rate and why it plateaus at a noise floor; the role of saddle-point escape in non-convex problems (tie to OPTM-02).
   - **Variance-reduction** sketch (SVRG/SAG idea) as the honest "how the field fixed SGD's plateau."
   - **Edge of applicability:** when full-batch GD or L-BFGS is actually better (small/medium `n`, ill-conditioning).
3. **Assumes:** OPTM-06, OPTM-07; **cross-track:** *expectation, unbiased estimator, variance of an average* [Probability foundations track].
4. **Sets up:** OPTM-12 (adaptive optimizers refine SGD); the training engine for Classification, Unsupervised Learning, and any deep model.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the convergence discussion; "Variance Reduction & Minibatching" can be a companion.

### OPTM-12 — Adaptive and Modern Optimizers: AdaGrad, RMSProp, Adam
1. **The one question:** Why do practitioners rarely run plain SGD, and what exactly are the per-parameter adaptive methods doing under the hood?
2. **Scope / inside:**
   - **AdaGrad** (accumulate squared gradients, scale each coordinate) derived and motivated by sparse/badly-scaled features; its decaying-rate flaw.
   - **RMSProp** (exponential moving average fix) and **Adam** (momentum + RMSProp, with bias correction) — the update rules derived term by term, not dropped as a recipe.
   - The honest debate: Adam's fast progress vs. its sometimes-worse generalization; when SGD-with-momentum still wins; learning-rate warmup/schedules in practice.
3. **Assumes:** OPTM-08 (momentum), OPTM-11 (SGD).
4. **Sets up:** terminal practical node of the descent spine; consumed by every model-training track.
5. **Depth:** medium–deep (~16–22).

---

## Constrained optimization — honoring the rules

### OPTM-13 — Optimizing Under Equality Constraints: Lagrange Multipliers
1. **The one question:** How do we minimize a function when the solution is forced to lie on a constraint surface like `g(x)=0`?
2. **Scope / inside:**
   - The geometric heart: at a constrained optimum, **`∇f` is parallel to `∇g`** (you can't improve without leaving the surface) — derived from the picture before any formula.
   - The **Lagrangian** `L(x,λ) = f(x) − λg(x)`; the stationarity conditions `∇ₓL=0, ∂L/∂λ=0` as the bookkeeping of that geometry; multiple equality constraints.
   - The **multiplier as a shadow price** (sensitivity of the optimum to relaxing the constraint), derived — the interpretation that makes duality (OPTM-15) click.
   - Worked examples: maximize entropy subject to a fixed mean; the constrained-least-squares / norm-constrained view of ridge (tie to Regression R14).
3. **Assumes:** OPTM-02; **cross-track:** *gradient, level sets / the gradient ⟂ level set fact* [Geometry of Data track].
4. **Sets up:** OPTM-14 (inequalities), OPTM-15 (duality).
5. **Depth:** deep (~18–24).

### OPTM-14 — Inequality Constraints and the KKT Conditions
1. **The one question:** What changes when constraints are inequalities `g(x) ≤ 0`, and what is the full optimality condition that covers every constrained convex problem?
2. **Scope / inside:**
   - **Active vs. inactive** constraints; the intuition that an inactive constraint contributes nothing (its multiplier is zero).
   - The **Karush–Kuhn–Tucker (KKT) conditions** — stationarity, primal feasibility, dual feasibility (`μ ≥ 0`), and **complementary slackness** `μg=0` — each derived and interpreted, not just listed.
   - When KKT is *sufficient* (convex problems + a constraint qualification) vs. only necessary.
   - Worked examples: the constraint form of lasso/ridge (the `‖β‖ ≤ t` picture from Regression R15) and the SVM margin problem (forward ref to Classification).
3. **Assumes:** OPTM-04 (convexity), OPTM-13; **cross-track:** none new.
4. **Sets up:** OPTM-15 (the dual), OPTM-16 (projection), and is the optimality backbone Classification's SVM article links here for.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the KKT statement+derivation; "KKT in Action: Lasso, Ridge, and SVM as Constrained Problems" can be a worked-examples companion.

### OPTM-15 — Duality: the Problem Behind the Problem
1. **The one question:** Every constrained problem has a hidden twin — what is the dual, why does solving it bound (and often equal) the original, and why do we care?
2. **Scope / inside:**
   - The **Lagrange dual function** (minimize the Lagrangian over `x`); **weak duality** (the dual always lower-bounds the primal) proved; the **duality gap**.
   - **Strong duality** and **Slater's condition** for convex problems (gap closes) — stated with its geometric (separating-hyperplane, OPTM-03) justification.
   - Why duality matters operationally: it turns a hard primal into an easier dual (the SVM kernel trick lives here), and certifies optimality.
   - **Honest boundary:** non-convex problems where the gap doesn't close.
3. **Assumes:** OPTM-03 (separating hyperplane), OPTM-13, OPTM-14.
4. **Sets up:** the dual SVM (Classification track); a deeper appreciation of the multiplier as price.
5. **Depth:** deep (~18–26).

### OPTM-16 — Proximal and Projected Methods: Descent Meets Constraints and Kinks
1. **The one question:** How do we run a descent method when part of the objective is non-smooth (a penalty) or the iterate must stay in a constraint set?
2. **Scope / inside:**
   - **Projected gradient descent**: take a gradient step, then project back onto the feasible convex set (OPTM-03); the projection defined and computed for a box / ball / simplex.
   - The **proximal operator** defined; **proximal gradient descent (ISTA)** for "smooth + non-smooth" objectives, derived; recognizing that the `ℓ₁` prox **is** soft-thresholding (full circle to OPTM-05/OPTM-10) — this is the modern lasso solver, and **FISTA** as its accelerated (OPTM-08) form.
   - Why prox/projection generalizes both coordinate descent and constrained GD; when to reach for it.
3. **Assumes:** OPTM-03, OPTM-05, OPTM-06, OPTM-08, OPTM-14.
4. **Sets up:** the general-purpose solver behind regularized models; an alternative the Regression regularization branch can link here.
5. **Depth:** deep (~18–26). **Split seam if needed:** cut between *projected* gradient (constraints) and *proximal* gradient (non-smooth penalties).

---

## Optimizing over functions

### OPTM-17 — Optimizing Over Functions: a Gentle Calculus of Variations
1. **The one question:** What if the thing we're optimizing over isn't a vector but an entire *function* — how do we minimize a quantity like `∫f''(x)² dx`?
2. **Scope / inside:**
   - The leap from "minimize over a point in ℝⁿ" to "minimize over a function": the **functional**, and the variational analogue of `∇f=0` built carefully from the floor (perturb `f` by `εη`, differentiate in `ε`, set to zero at `ε=0`).
   - The **Euler–Lagrange equation** derived for a simple functional; integration-by-parts shown in full (the one place this track touches above-floor calculus, built inline as promised in Regression R22).
   - The **smoothing-spline objective** `Σ(yᵢ−f(xᵢ))² + λ∫f''² ` and the *statement* (with variational intuition) that its minimizer is a natural cubic spline — exactly the result Regression R22 links here for.
   - **Honest boundary:** what we are *not* doing (full functional analysis, existence theory) and where the reader would go for it.
3. **Assumes:** OPTM-00, OPTM-01 (the "set the derivative to zero" template it generalizes); **cross-track:** *integration by parts* [Calc-1 floor — reviewed inline].
4. **Sets up:** Regression R22 (smoothing splines), and any later functional-optimization need. **Supplies** the *gentle calculus of variations* prerequisite for Regression. Terminal node of the track.
5. **Depth:** deep (~18–26). **Split seam if needed:** cut after the Euler–Lagrange derivation; "The Smoothing-Spline Variational Problem" can be a focused companion.

---

## Cross-track prerequisites (belong to OTHER tracks)

These are pulled in at the points noted. Optimization does **not** build them; they are named so the prerequisite chain (§1.4) is explicit.

**From the Geometry of Data / Applied Linear Algebra track** (the heaviest dependency — this track *runs on* its objects):
- *Vectors, linear combinations, half-spaces / hyperplanes* — needed at **OPTM-03**.
- *The gradient `∇f` and directional derivatives* — needed at **OPTM-02** (and used everywhere after).
- *The Hessian and the second-order Taylor expansion* — needed at **OPTM-02, OPTM-04, OPTM-09**.
- *Quadratic forms `xᵀAx` and positive-/negative-(semi)definiteness* — needed at **OPTM-02, OPTM-04, OPTM-09**.
- *Eigenvalues and the condition number of a matrix* — needed at **OPTM-07** (convergence rate), **OPTM-09**.
- *Matrix inverse and solving a linear system* — needed at **OPTM-09** (Newton step).
- *Level sets and the fact that `∇g` ⟂ the level set `g=0`* — needed at **OPTM-13**.

**From the Probability foundations track:**
- *Expectation, unbiased estimator, variance of an average* — needed at **OPTM-11** (the stochastic gradient is an unbiased estimate).

**From Calc-1 (the floor — reviewed inline, not a separate article):**
- *Single-variable differentiation, the second-derivative test* — **OPTM-01**.
- *First-order Taylor expansion* — **OPTM-06**.
- *Integration by parts* — **OPTM-17** (reviewed inline since calculus of variations is the one above-floor calculus touch).

This track has **no inbound dependency** on Regression, Statistical Inference, Classification, or Unsupervised Learning — it is upstream of all of them.

---

## What this track SUPPLIES to other tracks (the supply-depot contract)

Every optimization prerequisite requested by an existing track is delivered here, at the named article:

| Requested by | Prerequisite requested | Supplied by this track at |
|---|---|---|
| **Regression R15** (lasso) | *Convex functions and subgradients* | **OPTM-04** (convex functions) + **OPTM-05** (subgradients) |
| **Regression R15** (lasso) | *Coordinate descent* | **OPTM-10** (with soft-thresholding from **OPTM-05**) |
| **Regression R17** (logistic) | *Newton's method / gradient methods* | **OPTM-06** (gradient) + **OPTM-09** (Newton / IRLS) |
| **Regression R22** (smoothing splines) | *Calculus of variations (gentle)* | **OPTM-17** |
| **Inference B2** (MLE, no closed form) | *Newton's method / gradient ascent* | **OPTM-06** (ascent) + **OPTM-09** (Newton) |
| **Inference B4** (MLE asymptotics) | *Newton's method / gradient ascent* | **OPTM-06**, **OPTM-09** |

Additional concepts this track owns and exports to tracks **currently being designed** (anticipated, see Overlaps below):
- *Gradient descent / SGD / Adam* (**OPTM-06, OPTM-11, OPTM-12**) → the training engine for **Classification** and **Unsupervised Learning** (e.g. k-means as alternating minimization, deep models).
- *KKT and duality* (**OPTM-14, OPTM-15**) → the **Support Vector Machine** in **Classification**.
- *Projected / proximal methods* (**OPTM-16**) → constrained and regularized solvers across tracks.

---

## Overlaps & ownership

This track is foundational, so it touches many others. Recommended ownership calls:

| Shared topic | **Owner** | Rationale / boundary |
|---|---|---|
| **The gradient, Hessian, quadratic forms, positive-definiteness** | **Geometry of Data** | These are linear-algebra/multivariable-calculus *objects*. Optimization *uses* them (links, never re-derives) and teaches what to *do* with them. The clean seam: Geometry owns "what a Hessian is"; Optimization owns "use the Hessian to take a Newton step." |
| **Convex sets & functions, subgradients** | **Optimization** | These exist *for* optimization. Geometry may mention convexity for a hull/region, but the convex-analysis theory (subdifferentials, optimality conditions) is owned here; other tracks link in. |
| **Gradient descent, SGD, Adam, Newton, coordinate/proximal methods** | **Optimization** | The algorithms themselves. Regression/Classification/Unsupervised *invoke* them ("fit by SGD") and link here rather than re-deriving an optimizer. |
| **Lagrange multipliers, KKT, duality** | **Optimization** | The general constrained-optimization theory. The **SVM** (Classification) is a specific *instance* — Classification owns the SVM model and links here for KKT/duality. |
| **Calculus of variations** | **Optimization** | Owned here (OPTM-17), gently. Regression R22 (smoothing splines) links in; it is the one above-floor calculus this track builds inline. |
| **MLE / maximizing a log-likelihood** | **Statistical Inference** | Inference owns *what* the MLE is and *why* it's a good estimator; Optimization owns *how to compute it* when there's no closed form (gradient ascent / Newton). Inference's B2 links here. |
| **Minimizing a loss to FIT a model** (OLS normal equations, logistic loss) | **Regression** owns the *model and loss*; **Optimization** owns the *minimization method* | OPTM-02 uses OLS as an *example* of `∇f=0`; Regression owns the regression interpretation and links here for the descent algorithm when there's no closed form. |
| **Ridge/lasso as constrained vs. penalized problems** | **Shared, at different altitudes** | Optimization owns the *general* `min smooth + nonsmooth` / `‖β‖ ≤ t` machinery (OPTM-14, OPTM-16); Regression owns the *specific* ridge/lasso statistics and links here for the solver and the constraint-region geometry. |
| **k-means / EM as alternating minimization** | **Unsupervised Learning** | UL owns the clustering/latent-variable models; it links here for coordinate/alternating-descent and (for EM) the optimization-as-bound-maximization framing. |
| **Optimization in causal/policy problems** | **Causal Inference** | CI owns identification and estimands; any optimization it needs (e.g. minimizing an influence-function-based loss) links to the relevant algorithm here. |

**One-line ownership rule:** *if the deliverable is "how to find the optimum of a given objective," it's Optimization's job; if the deliverable is "which objective to write down for this model/estimator," it belongs to the modeling track, which links here for the solver.*

---

### Design notes / opinionated calls
- **OPTM-00–OPTM-02 are the on-ramp, deliberately gentle.** The track starts exactly at the Calc-1 floor ("set `f'(x)=0`") so a rusty reader is never cold-started, then climbs to `∇f=0` only after the vocabulary is solid.
- **Convexity (OPTM-03–OPTM-05) and descent (OPTM-06–OPTM-09) are parallel on purpose.** Convexity answers *"is a stationary point the answer?"*; descent answers *"how do I reach a stationary point?"*. They are independent ideas that the reader should hold separately, then fuse at OPTM-07 (convergence *needs* convexity) and the algorithm articles.
- **Subgradients (OPTM-05) are placed inside the convexity spine, not bolted onto lasso.** They are a general extension of the derivative, so they're taught generally and then *cashed out* three times: OPTM-10 (coordinate descent), OPTM-16 (proximal), and Regression's lasso.
- **Newton (OPTM-09) carries Gauss–Newton/IRLS explicitly** because that is the precise link Regression's GLM articles and Inference's MLE articles request — it is cheaper to own it once here than to re-derive IRLS in two tracks.
- **The calculus of variations (OPTM-17) is the deliberate terminal node.** It is the one place the track exceeds the floor's calculus, it serves exactly one downstream consumer (smoothing splines), and putting it last keeps the above-floor material quarantined from the core descent/convexity story.

This roadmap is **18 articles** (OPTM-00–OPTM-17). The two spines (convexity OPTM-03–OPTM-05, descent OPTM-06–OPTM-09) are ~3–4 articles each; constrained optimization (OPTM-13–OPTM-16) is 4; the rest are the on-ramp and the variational coda. Several deep articles (OPTM-04, OPTM-06, OPTM-07, OPTM-09, OPTM-11, OPTM-14, OPTM-15, OPTM-16, OPTM-17) carry pre-marked split seams should they push the 30-page ceiling during drafting.
