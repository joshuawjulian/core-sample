# Core Sample — Track Roadmap: **Classification & Supervised Learning**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

*An inch wide, a mile deep. From "what is the best possible classifier" all the way down to the kernel trick, the splitting criterion, and the boosting recursion — every supervised method for predicting a category, derived in full.*

This track is the supervised-learning sibling of Regression. Where Regression predicts a *number*, this track predicts a *category*. It opens with the theory that defines what "best" even means (statistical decision theory and the Bayes classifier), then walks the major method families — instance-based, generative, linear-discriminant, margin-based, tree-based, and ensemble/boosting — each motivated by a specific failure of the one before. It closes with multi-class strategies and the honest question of how you *measure* a classifier's quality.

**Hard boundary with Regression.** Logistic regression, the GLM framework, and the link/exponential-family machinery are **owned by the Regression track** (REGR-17–REGR-19). This track *links* to them as the canonical probabilistic linear classifier and as a discriminative contrast to the generative models built here. It does **not** re-derive the logit, the Bernoulli likelihood, or IRLS.

---

## The flow diagram

```
                    [CLAS-00] What Is Classification? (decision theory)
                                    │
                                    ▼
                    [CLAS-01] The Bayes-Optimal Classifier (0-1 loss, the irreducible floor)
                                    │
        ┌───────────────────┬───────────────┴───────────┬────────────────────┐
        ▼                   ▼                            ▼                    ▼
 INSTANCE-BASED       GENERATIVE                   LINEAR/MARGIN          (eval, far right)
 [CLAS-02] k-NN        [CLAS-03] Naive Bayes         [CLAS-05] The Perceptron
        │             [CLAS-04] LDA / QDA                   │
        │                   │                            ▼
        │                   │              [CLAS-06] The Margin (max-margin idea)
        │                   │                            │
        │                   │                            ▼
        │                   │              [CLAS-07] Hard-Margin SVM (the primal QP)
        │                   │                            │
        │                   │                            ▼
        │                   │              [CLAS-08] Soft-Margin SVM & the Hinge Loss
        │                   │                            │
        │                   │                            ▼
        │                   │              [CLAS-09] The Dual & Support Vectors
        │                   │                            │
        │                   │                            ▼
        │                   │              [CLAS-10] Kernels & the Kernel Trick
        │                   │
        └───────────────────┴──────────────► (all feed multi-class & evaluation)

 TREE-BASED & ENSEMBLES (own sub-spine off CLAS-01)
   [CLAS-11] Decision Trees (CART, splitting) ─► [CLAS-12] Pruning & Tree Variance
                                                       │
                          ┌────────────────────────────┼───────────────────┐
                          ▼                             ▼                   ▼
            [CLAS-13] Bagging & the Bootstrap [CLAS-14] Random Forests [CLAS-15] AdaBoost
            Aggregate (variance reduction)    (decorrelated trees)   (reweighting)
                                                                            │
                                                                            ▼
                                                          [CLAS-16] Gradient Boosting
                                                          (additive models, functional
                                                           gradient descent)

 CONVERGENCE — strategy & measurement
   [CLAS-17] Multi-Class Strategies (OvR, OvO, softmax, error-correcting codes)
   [CLAS-18] The Confusion Matrix & Threshold Metrics
   [CLAS-19] ROC, AUC, and Precision–Recall Curves
   [CLAS-20] Probability Calibration (are the scores honest?)
```

Linear reading order: **CLAS-00 → CLAS-01**, then the three method families (instance-based **CLAS-02**; generative **CLAS-03–CLAS-04**; margin **CLAS-05–CLAS-10**) and the tree/ensemble spine (**CLAS-11–CLAS-16**) are parallel and may be read in any order once CLAS-01 is done. The convergence articles **CLAS-17–CLAS-20** assume the reader has met at least one classifier and are read last.

---

## A. The Classification Problem & Decision Theory

### CLAS-00 — What Is Classification? The Decision-Theoretic Frame
1. **The one question:** What problem are we solving when we "predict a category," and how is it formally different from predicting a number?
2. **Scope / inside:**
   - The supervised setup: inputs `x`, a discrete label `y ∈ {1,…,K}`, a joint distribution `P(x,y)`, and a classifier as a function `ĝ: 𝒳 → {1,…,K}`.
   - The discrete-output contrast with Regression: there is no residual to minimize; we minimize *expected misclassification* instead — which forces the loss-function question.
   - The **loss function** as the object that defines "best": the 0-1 loss `L(y, ĝ(x)) = 𝟙[y ≠ ĝ(x)]` and the **risk** `R(g) = E[L]` as the thing we actually want to minimize. Asymmetric losses previewed (a false negative ≠ a false positive).
   - Historical *why*: from Fisher's iris discrimination and the pattern-recognition problem to the modern framing — classification as the canonical supervised task.
3. **Assumes:** *(this track)* none — entry point. *(cross-track)* joint and conditional distributions, expectation [Probability Foundations]; the idea of a regression/loss objective [Regression REGR-00].
4. **Sets up:** CLAS-01 (the optimal rule under 0-1 loss), and every downstream method (each one is an *approximation* to the rule CLAS-01 derives).
5. **Depth:** short–medium (~10–14). Motivational, light on derivation.

### CLAS-01 — The Bayes-Optimal Classifier: The Best Any Method Could Do
1. **The one question:** If we knew the true distribution `P(y|x)` exactly, what classifier would minimize the misclassification rate, and what error remains even then?
2. **Scope / inside:**
   - Full derivation that under **0-1 loss** the risk-minimizing rule is `ĝ*(x) = argmax_k P(y=k | x)` — the **Bayes classifier** — by minimizing the conditional risk pointwise.
   - The **Bayes error rate** as the irreducible floor (`1 − E[max_k P(y=k|x)]`); why no classifier can beat it; the binary-case decision boundary `{x : P(y=1|x) = 1/2}`.
   - Generalization to arbitrary loss: the rule becomes `argmin_k Σ_j L(j,k) P(y=j|x)`; cost-sensitive classification and the moved threshold.
   - The fork this sets up: **discriminative** methods estimate `P(y|x)` directly; **generative** methods estimate `P(x|y)` and `P(y)` then apply **Bayes' rule** — both are *attempts to approximate the Bayes classifier*.
3. **Assumes:** *(this track)* CLAS-00. *(cross-track)* Bayes' rule / posterior `P(y|x)`, conditional expectation [Probability Foundations].
4. **Sets up:** the generative/discriminative split that organizes the whole track; the Bayes-error benchmark used in every evaluation article; CLAS-02 (k-NN as a nonparametric estimate of `P(y|x)`), CLAS-03–CLAS-04 (generative), CLAS-09/CLAS-08 (margin methods as boundary estimators).
5. **Depth:** medium (~12–18). **Split seam if needed:** cut after the 0-1-loss optimal rule; "Cost-Sensitive Bayes Rules and Asymmetric Loss" can stand alone if the general-loss treatment crowds the page.

---

## B. Instance-Based Classification

### CLAS-02 — k-Nearest Neighbors: Classification With No Model At All
1. **The one question:** How well can we classify by simply asking "what were the labels of the closest training points," and what governs whether that works?
2. **Scope / inside:**
   - The k-NN rule as a *local, nonparametric estimate* of `P(y|x)` — the empirical class proportions in a neighborhood — and hence a direct approximation to the Bayes classifier (payoff from CLAS-01).
   - The role of `k` as the bias–variance dial (`k=1` jagged/high-variance; large `k` smooth/biased); distance metrics and why **feature scaling is mandatory**; ties under voting.
   - The famous result that 1-NN's asymptotic error is at most **twice** the Bayes error — stated and motivated.
   - **Curse of dimensionality** as the honest failure mode: neighbors stop being "near" in high dimensions (derived via the volume/concentration argument); computational cost of search and the k-d tree / approximate-NN escape hatches.
3. **Assumes:** *(this track)* CLAS-01. *(cross-track)* norms and distance/metric in `ℝᵈ`, volumes of balls [Geometry of Data]; bias–variance decomposition [Regression REGR-13].
4. **Sets up:** the nonparametric baseline every other method is measured against; the curse-of-dimensionality theme reused in CLAS-10 (why kernels help) and CLAS-14.
5. **Depth:** medium (~14–18).

---

## C. Generative Classifiers

### CLAS-03 — Naive Bayes: When "Pretend Features Are Independent" Wins Anyway
1. **The one question:** How do we turn the Bayes classifier into a usable method by *modeling* `P(x|y)`, and why does the blatantly false independence assumption work so often?
2. **Scope / inside:**
   - The generative recipe: estimate class priors `P(y)` and class-conditional `P(x|y)`, classify by `argmax_k P(y=k)·P(x|y=k)` (Bayes' rule, from CLAS-01).
   - The **naive (conditional-independence) assumption** `P(x|y) = Π_j P(xⱼ|y)`, derived as the factorization that makes high-dimensional density estimation tractable.
   - The variants and their likelihoods: **multinomial** and **Bernoulli** Naive Bayes (text/spam), **Gaussian** Naive Bayes (continuous features); **Laplace/additive smoothing** derived as the fix for the zero-frequency problem; working in log-space.
   - Why it survives its own false assumption: it only needs the *argmax* to be right, not the probabilities — and the honest flip side: its probability estimates are badly **miscalibrated** (forward ref to CLAS-20). Edge case where correlated features break it.
3. **Assumes:** *(this track)* CLAS-01. *(cross-track)* Bernoulli/multinomial/Gaussian distributions, likelihood and MLE for these [Probability Foundations; MLE principle owned by Statistical Inference INFR-B1–INFR-B2 — linked, not re-derived].
4. **Sets up:** CLAS-04 (LDA is "Gaussian Naive Bayes without the independence assumption, sharing a covariance"); the spam/text running example reused in evaluation articles.
5. **Depth:** medium (~14–18).

### CLAS-04 — Discriminant Analysis: LDA, QDA, and the Gaussian Decision Boundary
1. **The one question:** If each class is a Gaussian, what is the exact shape of the Bayes-optimal boundary between them, and when is it a line versus a curve?
2. **Scope / inside:**
   - Model `P(x|y=k) = N(μₖ, Σₖ)`; plug into the Bayes rule (CLAS-01) and derive the **discriminant function**. **Shared covariance** `Σₖ = Σ` ⇒ the quadratic term cancels ⇒ a **linear** boundary (**LDA**); per-class `Σₖ` ⇒ the term survives ⇒ a **quadratic** boundary (**QDA**) — both derived line by line.
   - LDA the *other* way: Fisher's original between-class/within-class scatter ratio `max_w (wᵀS_B w)/(wᵀS_W w)`, solved as a generalized eigenproblem — and the proof it gives the *same* projection. LDA as supervised dimensionality reduction.
   - Parameter estimation (pooled vs. per-class covariance); the bias–variance reason LDA beats QDA when data is scarce (fewer parameters).
   - **Failure modes:** singular/ill-conditioned `Σ` in high dimensions (regularized/shrinkage discriminant analysis), non-Gaussian classes; the honest contrast with logistic regression — *same linear boundary form, different fitting philosophy* (generative vs. discriminative).
3. **Assumes:** *(this track)* CLAS-01, CLAS-03 (the generative recipe). *(cross-track)* multivariate Gaussian density, covariance matrix [Probability Foundations]; quadratic forms, eigenvalues, the generalized eigenproblem, matrix inverse [Geometry of Data]; **link to Regression REGR-17 (logistic regression)** for the discriminative contrast — not re-derived here.
4. **Sets up:** the generative/discriminative comparison threaded through the rest of the track; LDA's projection reused as a dimensionality-reduction tool (hand-off to Unsupervised Learning / Geometry of Data).
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the LDA/QDA boundary derivation; "Fisher's Discriminant: The Scatter-Ratio View" can become its own article carrying the eigenproblem.

---

## D. Linear & Margin-Based Methods

### CLAS-05 — The Perceptron: The First Learning Machine
1. **The one question:** How can a machine *learn* a separating hyperplane one mistake at a time, and what can we guarantee about it?
2. **Scope / inside:**
   - The linear classifier `ĝ(x) = sign(wᵀx + b)` and the geometry of a separating hyperplane (normal vector, signed distance) — built from scratch.
   - The **perceptron update rule** `w ← w + y·x` on each misclassification, derived as (sub)gradient descent on the perceptron loss `max(0, −y(wᵀx+b))`.
   - The **Perceptron Convergence Theorem**: if the data is linearly separable with margin `γ`, the algorithm makes at most `(R/γ)²` mistakes — proved in full (the classic two-bound sandwich on `wᵀw*`).
   - **Failure modes:** non-separable data (never converges), the arbitrary boundary it settles on (any separator, not the best one) — the precise gap that *motivates the margin* (CLAS-06) and the historical XOR/Minsky-Papert wall (motivates kernels/networks).
3. **Assumes:** *(this track)* CLAS-01. *(cross-track)* dot product, hyperplanes, vector norms, projection / signed distance to a plane [Geometry of Data]; (sub)gradient descent basics [Optimization].
4. **Sets up:** CLAS-06 (the perceptron finds *a* separator; the margin asks for the *best*); the linear-boundary geometry reused by every SVM article.
5. **Depth:** medium–deep (~16–22).

### CLAS-06 — The Margin: Which Separating Hyperplane Is Best?
1. **The one question:** Among infinitely many separating hyperplanes, which one should we prefer, and how do we make "widest street between the classes" precise?
2. **Scope / inside:**
   - **Functional vs. geometric margin** defined and reconciled; the geometric margin `= y(wᵀx+b)/‖w‖` derived from the point-to-hyperplane distance formula.
   - The scale ambiguity of `(w,b)` and the **canonical normalization** (set the margin's functional value to 1) that pins it down — the move that turns "maximize the margin" into a clean objective.
   - Maximizing the margin `= maximizing 2/‖w‖ = minimizing (1/2)‖w‖²` — derived — subject to all points being correctly classified by at least the margin.
   - Why a large margin is a good idea (intuition + the generalization/VC-flavored argument stated honestly, built to the floor).
3. **Assumes:** *(this track)* CLAS-05. *(cross-track)* point-to-hyperplane distance, vector norms [Geometry of Data].
4. **Sets up:** CLAS-07 (this objective *is* the hard-margin SVM); the margin concept reused in CLAS-08 (slack) and CLAS-15–CLAS-16 (boosting maximizes a margin too).
5. **Depth:** medium (~12–18).

### CLAS-07 — The Hard-Margin SVM: A Quadratic Program for the Widest Street
1. **The one question:** How do we turn "maximize the margin" into a solvable optimization problem, and what kind of problem is it?
2. **Scope / inside:**
   - The **primal hard-margin program**: `min (1/2)‖w‖²` s.t. `yᵢ(wᵀxᵢ+b) ≥ 1 ∀i` — assembled directly from CLAS-06.
   - Why this is a **convex quadratic program** (convex objective, linear constraints) with a unique global optimum — and why that uniqueness is a feature versus the perceptron's arbitrariness.
   - Geometric reading of the constraints; the support points that sit *on* the margin (preview of CLAS-09's support vectors).
   - **Failure mode:** hard margin requires perfect linear separability — a single noisy point makes it infeasible or pathological — which forces the soft margin (CLAS-08).
3. **Assumes:** *(this track)* CLAS-06. *(cross-track)* convex sets/functions, constrained optimization, what a QP is [Optimization].
4. **Sets up:** CLAS-08 (relax the constraints), CLAS-09 (solve via the dual).
5. **Depth:** medium–deep (~16–20).

### CLAS-08 — The Soft-Margin SVM and the Hinge Loss
1. **The one question:** How do we let an SVM tolerate misclassifications and non-separable data without throwing away the margin idea?
2. **Scope / inside:**
   - **Slack variables** `ξᵢ ≥ 0` relaxing each constraint to `yᵢ(wᵀxᵢ+b) ≥ 1 − ξᵢ`; the penalized objective `min (1/2)‖w‖² + C Σ ξᵢ` and the **regularization parameter `C`** as the margin-width vs. violation trade-off.
   - The equivalence to **unconstrained hinge-loss minimization** `Σ max(0, 1 − yᵢ f(xᵢ)) + (1/2C)‖w‖²` — derived by eliminating the slacks — revealing the SVM as **regularized empirical risk minimization** with the hinge as a convex surrogate for the 0-1 loss.
   - The hinge plotted against 0-1, logistic, and exponential losses — the surrogate-loss family that unifies this track (forward ref to CLAS-16's exponential loss); why each is a convex upper bound on misclassification.
   - **Tuning `C`** by cross-validation; the bias–variance reading; the honest small/large-`C` failure modes.
3. **Assumes:** *(this track)* CLAS-07. *(cross-track)* convex surrogate losses, regularization as a penalty [Optimization]; cross-validation [Statistical Inference / Regression REGR-13]; **link to Regression REGR-14** for the `‖w‖²` ridge penalty parallel.
4. **Sets up:** CLAS-09 (the dual of *this* program is what's actually solved); the surrogate-loss view that connects SVMs, logistic regression, and boosting.
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the slack formulation; "The Hinge Loss and Surrogate Losses for Classification" can stand alone and serve CLAS-16.

### CLAS-09 — The Dual, the KKT Conditions, and Support Vectors
1. **The one question:** Why do we solve the SVM in its dual form, and why does the solution depend on only a handful of training points?
2. **Scope / inside:**
   - **Lagrangian duality** built to the needed level: the Lagrangian of the soft-margin program, the **KKT conditions**, and the derivation of the **dual** `max Σαᵢ − (1/2)ΣΣ αᵢαⱼyᵢyⱼ(xᵢ·xⱼ)` s.t. `0 ≤ αᵢ ≤ C`, `Σαᵢyᵢ = 0` — every step.
   - **Support vectors:** complementary slackness ⇒ `αᵢ ≠ 0` only for points on/inside the margin; recovering `w = Σαᵢyᵢxᵢ` and `b`; the model depends on the data *only through inner products* `xᵢ·xⱼ`.
   - Why that last fact is the whole game — it is exactly the opening the kernel trick walks through (CLAS-10).
   - Sparsity of the solution as a strength (compact model, fast prediction); the honest cost (training is `O(n²)`–`O(n³)`, poor scaling to huge `n`).
3. **Assumes:** *(this track)* CLAS-08. *(cross-track)* Lagrange multipliers, duality, KKT conditions [Optimization]; inner products [Geometry of Data].
4. **Sets up:** CLAS-10 (replace `xᵢ·xⱼ` with a kernel); the dual/inner-product structure is the prerequisite for kernelization.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the dual derivation; "KKT, Complementary Slackness, and Support Vectors" can split from the duality build-up.

### CLAS-10 — Kernels and the Kernel Trick: Linear Methods in a Curved World
1. **The one question:** How do we get nonlinear decision boundaries without ever computing high-dimensional feature vectors?
2. **Scope / inside:**
   - The trick: since the dual (CLAS-09) uses inputs *only* as inner products, replace `xᵢ·xⱼ` with `K(xᵢ,xⱼ) = φ(xᵢ)·φ(xⱼ)` for an implicit feature map `φ` — compute the inner product in the rich space without ever forming `φ(x)`.
   - **Mercer's condition** / positive-semidefinite kernels: which functions `K` are legitimate inner products (stated, with the Gram-matrix PSD requirement derived); the kernel as a similarity measure.
   - The standard kernels worked end-to-end: **polynomial** (with the explicit `φ` for degree 2 shown so the reader *sees* the lift), **Gaussian RBF** (the infinite-dimensional feature space made intuitive), and what each does to the boundary.
   - **Failure modes & judgment:** RBF bandwidth as the bias–variance dial (overfitting at small bandwidth — the curse of dimensionality returns, tie to CLAS-02); kernel choice as the real modeling decision; why kernel SVMs lost ground to trees/nets on large tabular and high-`n` data.
3. **Assumes:** *(this track)* CLAS-09. *(cross-track)* inner-product/feature spaces, positive-semidefinite matrices, the Gram matrix [Geometry of Data].
4. **Sets up:** terminal node of the margin sub-spine; hands the "implicit feature map" idea to Unsupervised Learning (kernel PCA) and Geometry of Data.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the trick + Mercer condition; "A Catalog of Kernels and How to Choose One" can carry the polynomial/RBF worked examples separately.

---

## E. Trees & Ensembles

### CLAS-11 — Decision Trees: Classification by Asking Questions (CART)
1. **The one question:** How do we build a classifier by recursively splitting the feature space into axis-aligned boxes, and how do we pick each split?
2. **Scope / inside:**
   - The tree as a partition of `𝒳` into rectangles, each labeled by its majority class; the **CART** greedy recursive-partitioning algorithm.
   - **Splitting criteria** derived and compared: node **impurity** via **Gini index** and **entropy / information gain**; why we maximize the impurity *decrease* of a split; the proof both are concave so any pure split helps; misclassification impurity and why it's a worse splitting criterion (less sensitive).
   - Handling numeric vs. categorical splits, the greedy search over thresholds; surrogate splits for missing values.
   - **Strengths/failure modes:** interpretability and no scaling needed (strength); high **variance** and instability — a small data change reshapes the tree — and axis-aligned bias (the diagonal-boundary failure). This variance is exactly what bagging/forests (CLAS-13–CLAS-14) attack.
3. **Assumes:** *(this track)* CLAS-01. *(cross-track)* entropy/log, expectation [Probability Foundations]; concavity / Jensen-flavored argument [Optimization, light].
4. **Sets up:** CLAS-12 (controlling tree complexity), CLAS-13–CLAS-16 (every ensemble in this track uses trees as its base learner).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the splitting criteria; "Impurity Measures: Gini, Entropy, and Why Not Error Rate" can stand alone.

### CLAS-12 — Pruning and the Variance of a Single Tree
1. **The one question:** A fully grown tree memorizes the training data — how do we cut it back to the right size?
2. **Scope / inside:**
   - Overfitting of deep trees as a bias–variance story (tie to Regression REGR-13); pre-pruning (depth/min-samples/min-impurity-decrease stopping) vs. post-pruning.
   - **Cost-complexity (weakest-link) pruning** derived: the penalized criterion `R_α(T) = R(T) + α|T|`, the nested sequence of subtrees as `α` grows, and choosing `α` by cross-validation — the full algorithm.
   - The honest verdict: even a well-pruned single tree is rarely competitive — its variance is the unfixable problem that *ensembles* exist to solve.
3. **Assumes:** *(this track)* CLAS-11. *(cross-track)* bias–variance, cross-validation [Regression REGR-13 / Statistical Inference].
4. **Sets up:** the ensemble sub-spine (CLAS-13–CLAS-16) — pruning manages one tree's variance; ensembles average it away instead.
5. **Depth:** medium (~12–18).

### CLAS-13 — Bagging: Averaging Away the Variance
1. **The one question:** If a single tree is high-variance, can we average many trees trained on resampled data to get a stable classifier?
2. **Scope / inside:**
   - **Bootstrap aggregating**: train a base learner on each bootstrap resample, vote/average the predictions; the variance-reduction argument derived (`Var of an average of B identically distributed estimators with pairwise correlation ρ` → `ρσ² + (1−ρ)σ²/B`) — and why it reduces variance without inflating bias.
   - Why bagging helps *unstable* learners (deep trees) and barely helps stable ones (linear/k-NN) — the honest applicability call.
   - **Out-of-bag (OOB) error** as a free cross-validation estimate, derived from the ~37% of points each resample omits.
3. **Assumes:** *(this track)* CLAS-11, CLAS-12. *(cross-track)* the bootstrap / sampling with replacement [Statistical Inference INFR-E1 — linked]; variance of a sum of correlated random variables [Probability Foundations].
4. **Sets up:** CLAS-14 (random forests = bagging + a decorrelation trick); the correlation `ρ` term is precisely what forests attack.
5. **Depth:** medium–deep (~14–20).

### CLAS-14 — Random Forests: Decorrelating the Trees
1. **The one question:** Bagged trees are still correlated because they keep choosing the same strong splits — how do we force them to disagree, and why does that help?
2. **Scope / inside:**
   - The random-subspace trick: at each split consider only a random subset of `m` features — reducing the pairwise tree correlation `ρ` from CLAS-13, which the variance formula shows drops the ensemble variance further.
   - `m` (and tree count, depth) as the tuning dials; the standard `m ≈ √p` default and its rationale; why forests rarely overfit by adding trees.
   - **Feature importance** done two honest ways (impurity-decrease vs. permutation importance) and the known bias of the impurity version toward high-cardinality features.
   - **Applicability:** why random forests are the strong default for tabular data; their limits (large memory, weak extrapolation, less interpretable than one tree, miscalibrated probabilities → CLAS-20).
3. **Assumes:** *(this track)* CLAS-13. *(cross-track)* permutation / resampling [Statistical Inference INFR-E3 — linked].
4. **Sets up:** the bagging-vs-boosting contrast (forests reduce variance by parallel averaging; boosting reduces bias by sequential correction — CLAS-15).
5. **Depth:** medium–deep (~16–20).

### CLAS-15 — AdaBoost: Turning Weak Learners Into a Strong One
1. **The one question:** Can a sequence of barely-better-than-chance classifiers, each focused on the previous one's mistakes, combine into an accurate one?
2. **Scope / inside:**
   - The **AdaBoost** algorithm in full: reweight misclassified points up each round, train a weak learner on the weighted data, combine with weights `αₜ = (1/2)log((1−εₜ)/εₜ)` — every formula derived.
   - The key reframing: AdaBoost is **forward stagewise additive modeling minimizing exponential loss** `Σ exp(−yᵢ F(xᵢ))` — derived line by line, recovering the reweighting and the `αₜ` as the exact minimizers each round. This is the conceptual hinge of the whole boosting sub-track.
   - The margin-maximization interpretation (why boosting can keep improving test error after training error hits zero) — stated honestly alongside its overfitting risk on noisy data.
   - **Failure mode:** sensitivity to label noise and outliers (exponential loss punishes them brutally) — the precise weakness that motivates gradient boosting's flexible losses (CLAS-16).
3. **Assumes:** *(this track)* CLAS-11 (weak learner = stump/shallow tree), CLAS-08 (the surrogate-loss view), CLAS-12. *(cross-track)* exponential/log, weighted empirical risk [Optimization]; **additive-model framing links to Regression REGR-26 (GAMs)** as the regression cousin of stagewise fitting.
4. **Sets up:** CLAS-16 (generalize "minimize exponential loss stagewise" to *any* differentiable loss via functional gradients).
5. **Depth:** deep (~18–26). **Split seam if needed:** cut after the algorithm; "AdaBoost as Forward Stagewise Additive Modeling" can carry the exponential-loss derivation separately.

### CLAS-16 — Gradient Boosting: Boosting as Gradient Descent in Function Space
1. **The one question:** How do we boost with *any* loss function, not just exponential, by treating the ensemble as a point we move downhill?
2. **Scope / inside:**
   - The generalization of CLAS-15: at each stage fit a base learner to the **negative gradient (pseudo-residuals)** of the loss evaluated at the current model — **functional gradient descent**, derived; AdaBoost recovered as the exponential-loss special case.
   - Concrete instances: squared-error (regression), **log-loss / deviance** for classification (the link back to logistic loss — connecting to **Regression REGR-17** without re-deriving it); the learning rate (shrinkage), subsampling (stochastic GB), and tree-size as the regularizers.
   - A practitioner's note on modern implementations (the second-order / regularized refinements behind gradient-boosted trees) — kept secondary to the math, stated as where the field went.
   - **Applicability & failure:** why gradient-boosted trees win most tabular competitions; the tuning burden and overfitting-without-regularization risk; the honest forest-vs-boosting decision table.
3. **Assumes:** *(this track)* CLAS-15. *(cross-track)* gradient descent as moving along the negative gradient [Optimization]; differentiable loss functions, the chain rule [Calc-1 floor]; **log-loss link to Regression REGR-17 (logistic regression)**; additive-model framing shared with **Regression REGR-26**.
4. **Sets up:** terminal node of the ensemble sub-spine; hands the "additive models + functional gradients" idea forward to a future deep-learning / advanced-ML track.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after the functional-gradient-descent derivation; "Gradient Boosting for Classification: Log-Loss and Regularization" can stand alone.

---

## F. Strategy & Measurement (convergence)

### CLAS-17 — Multi-Class Strategies: From Two Labels to Many
1. **The one question:** Most of the binary machinery above assumes two classes — how do we honestly extend it to `K > 2`?
2. **Scope / inside:**
   - **Inherently multi-class** methods (k-NN, Naive Bayes, LDA/QDA, trees) vs. **inherently binary** ones (perceptron, SVM) — and the reductions for the latter.
   - **One-vs-Rest (OvR)** and **One-vs-One (OvO)** derived: number of classifiers, the voting/argmax-of-scores decision, the ambiguous-region and class-imbalance problems of each, and the score-calibration issue when combining binary outputs.
   - The native multi-class generalizations: the **softmax / multinomial** formulation (the multi-class extension of the logit — **links to Regression's logistic/GLM machinery**, not re-derived) and the multi-class hinge; **error-correcting output codes** as the redundancy-for-robustness approach.
3. **Assumes:** *(this track)* CLAS-05–CLAS-10 (binary SVM/perceptron), and any one classifier. *(cross-track)* softmax / multinomial logit links to **Regression REGR-17–REGR-18** — not re-derived.
4. **Sets up:** the evaluation articles (CLAS-18–CLAS-20), which must handle the multi-class confusion matrix and averaging schemes.
5. **Depth:** medium (~12–18).

### CLAS-18 — The Confusion Matrix and What "Accuracy" Hides
1. **The one question:** Once we have predictions, how do we measure quality — and why is raw accuracy so often a lie?
2. **Scope / inside:**
   - The **confusion matrix**; TP/FP/FN/TN; and the family of threshold metrics derived from it: **precision, recall/sensitivity, specificity, F1** (and `Fβ`), with the precise question each answers.
   - The **accuracy paradox** under class imbalance (the honest motivating failure — 99% accuracy by predicting the majority class); base rates; the cost-sensitive tie back to CLAS-01's asymmetric-loss Bayes rule.
   - Multi-class extension: micro vs. macro vs. weighted averaging, and which to report when.
3. **Assumes:** *(this track)* CLAS-01 (asymmetric loss), CLAS-17 (multi-class). *(cross-track)* conditional probability / rates [Probability Foundations].
4. **Sets up:** CLAS-19 (a metric that sweeps the threshold rather than fixing one).
5. **Depth:** medium (~12–16).

### CLAS-19 — ROC, AUC, and Precision–Recall Curves: Evaluating Across All Thresholds
1. **The one question:** A scoring classifier has no single threshold — how do we evaluate it across *all* of them, and which curve should we trust?
2. **Scope / inside:**
   - The **ROC curve** (TPR vs. FPR as the threshold sweeps) constructed step by step; **AUC** derived and given its probabilistic meaning (`P(score of a random positive > score of a random negative)` — the Mann–Whitney equivalence, proved).
   - **Precision–Recall curves** and **average precision**; the rigorous argument for *why PR beats ROC under heavy class imbalance* (ROC's optimism when negatives dominate) — the central honest judgment of the article.
   - The diagonal baseline, the convex hull, operating-point selection tied to the cost structure (back to CLAS-01); multi-class one-vs-rest ROC.
3. **Assumes:** *(this track)* CLAS-18. *(cross-track)* the Mann–Whitney / rank-statistic argument and order statistics [Probability Foundations]; **the underlying test/rank theory overlaps Statistical Inference** (see Overlaps).
4. **Sets up:** CLAS-20 (a good ranking — high AUC — still need not give honest probabilities).
5. **Depth:** medium–deep (~16–20).

### CLAS-20 — Probability Calibration: Are the Predicted Scores Honest?
1. **The one question:** When a classifier says "70% chance of class 1," does it happen 70% of the time — and how do we check and fix it?
2. **Scope / inside:**
   - **Calibration** defined; the **reliability diagram** and the **Brier score** / log-loss as calibration-sensitive metrics; the crucial distinction between *discrimination* (ranking, CLAS-19) and *calibration* (honest probabilities) — a model can have high AUC and terrible calibration.
   - Why specific methods miscalibrate: Naive Bayes (independence pushes scores to extremes, from CLAS-03), SVM margins (not probabilities at all), random forests (variance shrinks scores toward the middle, from CLAS-14) — each explained mechanistically.
   - Post-hoc fixes derived: **Platt scaling** (fit a logistic on the scores — **links to Regression REGR-17**) and **isotonic regression** (nonparametric monotone fit); the honest cost (needs a held-out set, can overfit on little data).
3. **Assumes:** *(this track)* CLAS-19, and the methods CLAS-03/CLAS-14 it diagnoses. *(cross-track)* logistic transform links to **Regression REGR-17**; isotonic / monotone fitting [Optimization, light].
4. **Sets up:** terminal node of the evaluation arc; hands calibration forward to a recommended **Model-Evaluation track** (see Overlaps) and to decision-making/Causal contexts where calibrated probabilities matter.
5. **Depth:** medium (~14–18).

---

## Cross-track prerequisites (belong to OTHER tracks)

Pulled in at the points noted. Classification does **not** build these; they are named so the prerequisite chain (§1.4) is explicit.

**From Probability Foundations**
- *Joint / conditional distributions, conditional expectation, Bayes' rule for `P(y|x)`* — needed at **CLAS-00, CLAS-01**.
- *Bernoulli, multinomial, Gaussian (univariate & multivariate) distributions; their likelihoods* — needed at **CLAS-03, CLAS-04**.
- *Entropy and information* — needed at **CLAS-11** (information gain).
- *Variance of a sum of correlated random variables* — needed at **CLAS-13** (the bagging variance formula).
- *Order statistics / rank statistics; the Mann–Whitney probability* — needed at **CLAS-19** (AUC).
- *Conditional probability / rates* — needed at **CLAS-18, CLAS-20**.

**From Geometry of Data / Applied Linear Algebra**
- *Norms, distance/metric in `ℝᵈ`, volumes of balls* — needed at **CLAS-02** (k-NN, curse of dimensionality).
- *Dot product, hyperplanes, point-to-plane signed distance, projection* — needed at **CLAS-05, CLAS-06**.
- *Quadratic forms, eigenvalues, the generalized eigenproblem, matrix inverse* — needed at **CLAS-04** (LDA/QDA, Fisher's discriminant).
- *Inner-product / feature spaces, positive-semidefinite matrices, the Gram matrix* — needed at **CLAS-09, CLAS-10** (the dual and the kernel trick).

**From Optimization**
- *(Sub)gradient descent* — needed at **CLAS-05** (perceptron), **CLAS-16** (functional gradient descent).
- *Convex sets/functions, constrained optimization, quadratic programs* — needed at **CLAS-07** (the SVM primal).
- *Lagrangian duality, KKT conditions, complementary slackness* — needed at **CLAS-09** (the SVM dual).
- *Convex surrogate losses, regularization as a penalty* — needed at **CLAS-08** (hinge loss).
- *Concavity / Jensen-type argument; monotone (isotonic) fitting* — needed at **CLAS-11, CLAS-20**.

**From Regression** *(link, do NOT re-derive — Regression owns these)*
- *Logistic regression, the logit/sigmoid, the Bernoulli likelihood, IRLS* (**REGR-17**) — linked at **CLAS-04** (discriminative contrast), **CLAS-16, CLAS-20** (log-loss / Platt scaling), **CLAS-17** (softmax).
- *The GLM framework, link functions, the exponential family* (**REGR-18**) — linked at **CLAS-17** (multinomial/softmax).
- *Generalized Additive Models / forward stagewise additive fitting* (**REGR-26**) — linked at **CLAS-15, CLAS-16** (boosting as additive modeling — the regression cousin).
- *Ridge / `ℓ₂` penalty* (**REGR-14**) — linked at **CLAS-08** (the `‖w‖²` regularizer parallel).
- *Bias–variance decomposition & cross-validation* (**REGR-13**) — needed at **CLAS-02, CLAS-08, CLAS-12, CLAS-16**.

**From Statistical Inference** *(link, do NOT re-derive — Inference owns the general machinery)*
- *MLE as a general estimation principle* (**INFR-B1–INFR-B2**) — linked at **CLAS-03, CLAS-04** (fitting the generative models).
- *The bootstrap / sampling with replacement* (**INFR-E1**) — linked at **CLAS-13** (bagging is bootstrap aggregation).
- *Permutation / resampling* (**INFR-E3**) — linked at **CLAS-14** (permutation importance).

---

## Overlaps & ownership

This track sits between Regression, Statistical Inference, and several tracks being designed concurrently (Probability Foundations, Geometry of Data, Optimization, Unsupervised Learning, Causal Inference). Recommended ownership calls:

| Shared topic | Recommended owner | Rationale |
|---|---|---|
| **Logistic regression, the logit, GLMs, exponential family, IRLS** | **Regression (REGR-17–REGR-19)** | Already owned and derived there. Classification links for the discriminative contrast (CLAS-04), softmax (CLAS-17), log-loss boosting (CLAS-16), and Platt scaling (CLAS-20) — never re-derives. |
| **Additive models / forward stagewise fitting** | **Shared, two altitudes** | Regression owns GAMs (REGR-26) for *regression* smooths; Classification owns *boosting* (CLAS-15–CLAS-16) as the stagewise-additive-classifier instance. Each links the other as its cousin. |
| **The Bayes classifier & statistical decision theory (0-1 loss, risk)** | **Classification (CLAS-00–CLAS-01)** | This is the foundational frame for *classification specifically*. If a future general **Decision Theory** stub is wanted, it could lift CLAS-01 — but it belongs here by default. |
| **The bootstrap, permutation, resampling** | **Statistical Inference (INFR-E1, INFR-E3)** | General uncertainty machinery. Classification consumes it for bagging (CLAS-13) and importance (CLAS-14). |
| **MLE as an estimation principle** | **Statistical Inference (INFR-B1–INFR-B2)** | General; Classification instantiates it for Naive Bayes / discriminant analysis. |
| **Classifier evaluation: confusion matrix, ROC/AUC, PR, calibration (CLAS-18–CLAS-20)** | **FLAGGED — recommend a future Model-Evaluation track owns the *general* theory; Classification owns the *classifier-specific* treatment** | See note below. Strong overlap with Statistical Inference (AUC = Mann–Whitney rank test; calibration = goodness-of-fit). |
| **Curse of dimensionality, distance geometry, kernels/feature maps, PSD matrices** | **Geometry of Data** | Classification consumes (CLAS-02, CLAS-10). Kernel PCA / spectral methods belong to Unsupervised Learning, which can reuse CLAS-10's kernel-trick build. |
| **Convex optimization, duality/KKT, gradient & coordinate methods** | **Optimization** | Classification consumes heavily (CLAS-05, CLAS-07–CLAS-09, CLAS-16). The SVM dual is the marquee *application*; the duality *theory* is Optimization's. |
| **LDA as supervised dimensionality reduction** | **Shared with Unsupervised Learning / Geometry of Data** | The classifier derivation is here (CLAS-04); the dimensionality-reduction *use* (and its unsupervised PCA sibling) is better owned by Unsupervised Learning, linking back to CLAS-04. |
| **Cost-sensitive / asymmetric-loss decisions; calibrated probabilities for actions** | **Link to Causal Inference where decisions are the deliverable** | CLAS-01 and CLAS-20 supply the loss/calibration machinery; how a *decision* is taken from a probability under intervention is Causal Inference's concern. |

**Recommendation on the evaluation overlap (the flagged item).** Articles **CLAS-18–CLAS-20** (confusion matrix, ROC/AUC, precision–recall, calibration) are written here so the Classification reader finishes able to *measure a classifier*. But they overlap materially with Statistical Inference (AUC is the Mann–Whitney–Wilcoxon statistic; calibration is a goodness-of-fit question) and with regression-error evaluation. **Recommend that a dedicated future Model-Evaluation track own the general cross-method theory of evaluation** (proper scoring rules, the full taxonomy of metrics, calibration theory, evaluation under distribution shift), at which point CLAS-18–CLAS-20 should be **slimmed to the classifier-specific essentials and link out** to it. Until that track exists, CLAS-18–CLAS-20 stand as the home of this material — flagged here so ownership is decided deliberately rather than by default duplication. The AUC ↔ rank-test identity (CLAS-19) should in any case **cite Statistical Inference's rank-statistic article** rather than re-deriving the Mann–Whitney distribution.

---

### Design notes / opinionated calls
- **Decision theory comes first (CLAS-00–CLAS-01) on purpose.** Every subsequent method is framed as an *approximation to the Bayes classifier* — k-NN estimates `P(y|x)` locally, generative models estimate `P(x|y)` then invert, margin methods estimate the boundary directly. The Bayes-error floor gives every evaluation article a benchmark. Without this spine the track is a disconnected zoo of algorithms.
- **The generative/discriminative axis is the organizing contrast,** introduced at CLAS-01 and paid off repeatedly (CLAS-03–CLAS-04 generative vs. linked logistic regression discriminative; CLAS-16's log-loss boosting as discriminative).
- **The SVM is built as a six-article staircase (CLAS-05–CLAS-10)** — perceptron → margin → primal → soft margin/hinge → dual → kernel — because each step answers exactly one failure of the previous, and the inner-product structure at CLAS-09 is what *earns* the kernel trick at CLAS-10. Collapsing these would violate inch-wide.
- **Boosting is anchored on the additive-model reframing (CLAS-15–CLAS-16),** not presented as an algorithmic trick, so it connects honestly to Regression's GAMs and reads as "gradient descent in function space."
- **Bagging before forests before boosting (CLAS-13→CLAS-14→CLAS-15)** so the variance-reduction (parallel) vs. bias-reduction (sequential) contrast lands as a punchline the reader has half-derived via the correlation term `ρ`.
- **Evaluation is last and flagged for re-homing** — see the overlap recommendation above.

This roadmap is **21 articles** (CLAS-00–CLAS-20): 2 foundation, 1 instance-based, 2 generative, 6 margin-based, 6 tree/ensemble, 4 strategy/evaluation. Several deep articles (CLAS-04, CLAS-08, CLAS-09, CLAS-10, CLAS-11, CLAS-15, CLAS-16) carry pre-marked split seams should they push the 30-page ceiling during drafting.
