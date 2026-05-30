# Core Sample — Track Roadmap: **Unsupervised Learning**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

*An inch wide, a mile deep. There are no labels — only the data and its shape. This track asks what "structure" even means when nothing tells you the answer, then builds the tools that find it: clusters, latent mixtures, low-dimensional skeletons, and densities.*

## PART 0 — Charter and the Boundaries

### Charter (one paragraph)

> **Unsupervised Learning** is the track that finds structure in data when no target variable supervises the search. Given only an unlabeled cloud of points, it asks: *are there groups? a smaller number of underlying dimensions? a density that generated all of this?* — and, harder, *how would we ever know we found something real rather than imposed it?* The track builds the three great families of unsupervised method: **clustering** (partition the data into groups — k-means, mixtures via EM, hierarchical, density-based), **dimensionality reduction** (find a faithful low-dimensional representation — PCA as application, kernel PCA, manifold learning), and **density estimation** (recover the generating distribution — KDE). Around them it builds the discipline that unsupervised learning lives or dies on: **validation** — because without labels, "it worked" is a claim that must be earned, not assumed. The reader finishes able to choose a clustering algorithm for the shape of the data in front of them, derive EM from the ELBO, interpret a PCA biplot, read a t-SNE plot without lying to themselves, and — above all — judge whether the structure they found is signal or wishful thinking.

### What this track does NOT own (explicit contract)

This track is an *application and synthesis* layer. It consumes heavy machinery from three upstream tracks and is scrupulous about not re-deriving it:

| Machinery | Owned by | This track's posture |
|---|---|---|
| **SVD / eigendecomposition / spectral theorem** | **Geometry of Data** | Link, do not re-derive. PCA *uses* the decomposition; Geometry *proves* it. |
| **The EM algorithm as general optimization theory** (ELBO, MM, convergence) | **see flag at UNSP-05** | Recommend Unsupervised owns the *operational* EM; Inference co-owns the *general latent-variable* statement. |
| **Convexity, gradient/coordinate descent, Lloyd's-as-coordinate-descent framing** | **Optimization** | Consume the optimization vocabulary; build only the clustering-specific objective. |
| **Probability densities, multivariate Gaussian, KL divergence, Jensen's inequality** | **Probability Foundations** | Consume; KL and Jensen are imported at the EM article. |
| **Inner products, projection, eigenvalues, quadratic forms, distances/norms** | **Geometry of Data** | Consume; this is the geometric substrate of all of it. |

The rule of thumb: **if the deliverable is "structure discovered in unlabeled data, or a judgment about that structure," it is this track's job; if the deliverable is a linear-algebra factorization or a generic optimization guarantee, it belongs upstream and we link to it.**

---

## The flow diagram

```
                    [UNSP-00] What Is Structure Without Labels?
                         (the unsupervised problem)
                                    │
        ┌───────────────────────────┼───────────────────────────────┐
        ▼                           ▼                                ▼
  ── CLUSTERING ──         ── DIMENSIONALITY REDUCTION ──     ── DENSITY ──
        │                           │                                │
  [UNSP-01] Distance & the     [UNSP-07] PCA: The Application  [UNSP-12] Kernel Density
       Cluster Objective           (variance, projection)         Estimation
        │                     ◄── needs Geometry: SVD            ◄── needs UNSP-01, Prob
        ▼                           │
  [UNSP-02] k-means & Lloyd's  [UNSP-08] Choosing & Interpreting
       Algorithm                   PCA (scree, biplot, whiten)
        │                           │
        ▼                           ▼
  [UNSP-03] k-means++ &        [UNSP-09] Kernel PCA
       Initialization             (the kernel trick on PCA)
        │                           │
        ▼                           ▼
  [UNSP-04] GMMs: Soft Clusters [UNSP-10] Manifold Learning I:
       as a Mixture Model           the Manifold Hypothesis & MDS/Isomap
        │                           │
        ▼                           ▼
  [UNSP-05] EM via the ELBO    [UNSP-11] Manifold Learning II:
   ◄FLAG: EM theory co-owned        t-SNE & UMAP
    with Statistical Inference      (neighbor embeddings, honest reading)
        │
        ▼
  [UNSP-06a] Hierarchical /
        Agglomerative Clustering
        │
        ▼
  [UNSP-06b] Density-Based Clustering
        (DBSCAN, HDBSCAN)
        │
        └──────────────┐
                        ▼
              [UNSP-13] Did We Find Anything?
                    Cluster Validation
              (silhouette, gap statistic,
               stability, choosing k)
                        │
                        ▼
              [UNSP-14] The Unsupervised Reality Check
              (when there is no ground truth —
               synthesis & practitioner judgment)
```

Three families fan out from **UNSP-00** and all reconverge at **UNSP-13–UNSP-14**: validation and judgment are the spine that makes the rest honest. Linear reading order is given at the end.

---

## A. The Problem

### UNSP-00 — What Is "Structure" When There Are No Labels?
1. **The one question:** With no target variable to predict, what are we even looking for, and what makes a discovered pattern *real* rather than imposed?
2. **Scope / inside:**
   - The supervised/unsupervised split framed as the absence of `y`: we model `p(x)` or geometry of `X`, not `p(y|x)`. The three jobs — clustering, dimensionality reduction, density estimation — as three answers to "describe the data's shape."
   - Why unsupervised problems are *ill-posed by default*: there is no loss to minimize against a truth, so every method smuggles in an **assumption about what structure looks like** (compactness, low dimension, high density). Name that assumption up front as the recurring theme of the track.
   - The validation problem stated early as a promissory note: without labels, how could you possibly know? (Forward ref to UNSP-13.) The honest framing that clustering can always return *a* partition — the question is whether it means anything.
3. **Assumes:** Only the floor (functions, a scatterplot, the idea of distance and of an average). *(cross-track)* the notion of a random sample [Probability Foundations].
4. **Sets up:** the whole track; UNSP-01 (distance), UNSP-13 (validation).
5. **Depth:** short (~8–12). Motivational; light on derivation.

---

## B. Clustering

### UNSP-01 — Distance, Similarity, and the Clustering Objective
1. **The one question:** Before any algorithm, what does it mean for points to be "close," and how does a choice of distance silently decide what clusters can even exist?
2. **Scope / inside:**
   - Metrics and the metric axioms; Euclidean, Manhattan, cosine, Mahalanobis — each defined, and the *shape of the unit ball* each implies (so the reader sees why cosine ignores magnitude, why Mahalanobis is scale-and-correlation aware).
   - **Why feature scaling/standardization is not optional** for distance-based methods — a worked example where unscaled features make one variable dominate the partition.
   - The generic clustering objective: minimize within-group dissimilarity / maximize between-group separation. Stating it abstractly so k-means, hierarchical, and DBSCAN each read as a *different commitment* to the same goal.
3. **Assumes:** UNSP-00; *(cross-track)* norms, inner products, the Euclidean metric, positive-definite matrices for Mahalanobis [Geometry of Data].
4. **Sets up:** UNSP-02 (k-means picks squared-Euclidean), UNSP-06a (linkage = a distance choice), UNSP-06b (density needs a radius in some metric), UNSP-12 (KDE kernels are distance-weighted).
5. **Depth:** medium (~12–16).

### UNSP-02 — k-means and Lloyd's Algorithm
1. **The one question:** What exactly is k-means minimizing, and why does the simple "assign, then recenter" loop drive that objective down every single step?
2. **Scope / inside:**
   - The **within-cluster sum of squares (WCSS / inertia)** objective `Σₖ Σ_{i∈Cₖ} ‖xᵢ − μₖ‖²` written out; the joint minimization over assignments *and* centroids.
   - **Lloyd's algorithm** derived as **coordinate descent** on that objective: fix centroids → optimal assignment is nearest centroid (proved); fix assignments → optimal centroid is the group mean (derived by setting the gradient of the sum of squares to zero — the Calc-1-level argument shown in full). Hence WCSS is **monotonically non-increasing**, so the algorithm **terminates** (finite partitions).
   - The honest catch: monotone decrease guarantees a **local** optimum, not the global one; k-means is NP-hard in general. Sensitivity to initialization motivates UNSP-03. Worked example on real data + the centroid-and-assignment figure animated across iterations.
3. **Assumes:** UNSP-01; *(cross-track)* gradient of a sum of squares / setting a derivative to zero [Calc-1 floor + Geometry of Data]; *coordinate descent as an optimization scheme* [Optimization].
4. **Sets up:** UNSP-03 (fixing the initialization weakness), UNSP-04 (k-means as a hard/degenerate special case of a GMM).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the convergence proof into *UNSP-02a "The k-means Objective and Lloyd's Algorithm"* and *UNSP-02b "Why Lloyd's Converges (and Only Locally),"* at the monotonicity argument.

### UNSP-03 — k-means++ and the Initialization Problem
1. **The one question:** Since Lloyd's only finds a local optimum, how do we seed the centroids so the answer is both good and provably close to optimal?
2. **Scope / inside:**
   - Why random initialization fails: the worked pathological case where two seeds land in one true cluster and never recover. Multiple-restart-and-keep-best as the crude baseline.
   - **k-means++** seeding: sample the next center with probability `∝ D(x)²` (distance to nearest chosen center); the full procedure, and the intuition that it spreads seeds out probabilistically.
   - The guarantee stated honestly: k-means++ is `O(log k)`-competitive in expectation with the optimal WCSS (theorem stated, the proof sketch's key inequality shown, full proof deferred as out of scope with a citation). Choosing `k` itself flagged as deferred to UNSP-13.
3. **Assumes:** UNSP-02; *(cross-track)* sampling from a discrete probability distribution, expectation [Probability Foundations].
4. **Sets up:** UNSP-13 (choosing k); a reusable seeding idea referenced when GMMs need initialization (UNSP-04/UNSP-05).
5. **Depth:** medium (~12–16).

### UNSP-04 — Gaussian Mixture Models: Soft Clusters as a Generative Story
1. **The one question:** What if each point was *generated* by one of several Gaussian sources, and we want the probability it came from each — how do we even write that model down?
2. **Scope / inside:**
   - The **generative model**: a latent cluster label `z ∼ Categorical(π)`, then `x | z=k ∼ N(μₖ, Σₖ)`; the resulting **mixture density** `p(x) = Σₖ πₖ N(x; μₖ, Σₖ)`, written and pictured (overlapping bells summing to a multimodal density).
   - **Soft vs. hard assignment**: the posterior **responsibility** `γ(z=k) = πₖ N(x;μₖ,Σₖ) / Σⱼ πⱼ N(x;μⱼ,Σⱼ)` derived from Bayes' rule. The payoff connection: **k-means is the limiting case** of a GMM with shared isotropic `Σ = σ²I` as `σ→0` (hard assignment falls out) — derived, making k-means feel like a special case rather than a separate trick.
   - Why we can't just maximize the mixture log-likelihood directly: the **sum inside the log** blocks a closed form (shown), which is exactly the wall EM is built to climb. Covariance structure choices (full / diagonal / tied / spherical) as a bias–variance dial.
3. **Assumes:** UNSP-02; *(cross-track)* the **multivariate Gaussian density**, **Bayes' rule for a latent label**, marginalization over a latent variable [Probability Foundations].
4. **Sets up:** UNSP-05 (EM is how we fit this), UNSP-13 (BIC for choosing the number of components).
5. **Depth:** deep (~18–24).

### UNSP-05 — The EM Algorithm, Derived via the ELBO
1. **The one question:** When a latent variable puts a sum inside the log and kills the closed-form MLE, how do we maximize the likelihood anyway — and why does iterating a lower bound provably work?
2. **Scope / inside:**
   - The latent-variable likelihood `log p(x;θ) = log Σ_z p(x,z;θ)` and the obstruction restated from UNSP-04. Introduce a variational distribution `q(z)` and derive the decomposition `log p(x;θ) = ELBO(q,θ) + KL(q ‖ p(z|x;θ))` **in full**, using Jensen's inequality to establish the ELBO as a genuine lower bound (every line shown).
   - **EM as alternating maximization of the ELBO**: the **E-step** sets `q = p(z|x;θ_old)` (drives KL to 0, making the bound tight — proved); the **M-step** maximizes the ELBO's expected-complete-log-likelihood term over `θ`. Why this guarantees the *marginal* likelihood is **monotonically non-decreasing** (the central convergence theorem, derived) — and why that still only gives a local optimum.
   - **EM specialized to the GMM** end-to-end: E-step = compute responsibilities (from UNSP-04); M-step = closed-form weighted means, covariances, and mixing weights (each derived). Worked example fitting a GMM to real data; the **degeneracy failure mode** where a component collapses onto a single point and the likelihood diverges — the honest boundary, with the regularization fix.
3. **Assumes:** UNSP-04; *(cross-track)* **Jensen's inequality**, **KL divergence** and its non-negativity, **concavity of log** [Probability Foundations]; **MLE as a principle** [Statistical Inference, B2]; the idea of alternating/coordinate optimization [Optimization].
4. **Sets up:** consumed anywhere a latent-variable model needs fitting; pairs back to UNSP-02 (k-means = "hard EM"). Connects forward to any future latent-factor / topic-model track.
5. **Depth:** deep (~24–30). **Split seam if needed:** cut after the convergence theorem into *UNSP-05a "EM and the ELBO: the General Algorithm"* and *UNSP-05b "EM for Gaussian Mixtures (worked)."* This is the natural seam because the general theory and the GMM specialization are each a full inch-wide idea.

> **OWNERSHIP FLAG (EM).** The **general EM / latent-variable / ELBO theory** is genuinely co-claimable with **Statistical Inference** (it is "MLE when there's missing data," squarely in Inference's MLE charter). **Recommended ownership: Unsupervised Learning owns the *operational* EM article (UNSP-05), because every canonical motivating instance — GMMs, soft clustering, latent assignments — lives here and EM is introduced where it is most motivated.** Statistical Inference should carry at most a short *connection* note ("the MLE with a latent variable is solved by EM — see Unsupervised UNSP-05") rather than re-deriving the ELBO. If the series later grows a dedicated latent-variable / variational track, the *general* ELBO theory migrates there and both Unsupervised and Inference link to it. **Decision to confirm with the orchestrator before drafting UNSP-05.**

### UNSP-06a — Hierarchical (Agglomerative) Clustering
1. **The one question:** What if we don't want to commit to a number of clusters at all, and instead build the entire nested family of groupings at once?
2. **Scope / inside:**
   - **Agglomerative** bottom-up merging: start with `n` singletons, repeatedly merge the two closest clusters; the **dendrogram** as the complete record, and how a horizontal cut yields any `k` (the headline advantage: one fit, all granularities).
   - **Linkage criteria** — single, complete, average, and **Ward's** (minimizing the WCSS increase, tying directly back to UNSP-02) — each defined; the chaining failure of single linkage vs. the compactness bias of complete linkage shown on real data. The **Lance–Williams update** that makes recomputation cheap, stated.
   - Honest cost boundary: `O(n²)`–`O(n³)` time and `O(n²)` memory — why this does not scale, and when the interpretable dendrogram is worth it anyway (small-`n`, taxonomy-style problems).
3. **Assumes:** UNSP-01 (distance + Ward needs the WCSS idea from UNSP-02); *(cross-track)* none new beyond UNSP-01's metrics.
4. **Sets up:** UNSP-13 (cutting a dendrogram is a "choose k" decision); contrast partner for UNSP-06b.
5. **Depth:** medium–deep (~16–20).

### UNSP-06b — Density-Based Clustering: DBSCAN
1. **The one question:** What if clusters are arbitrary *shapes* and the data has noise — how do we find groups defined by being densely packed rather than by being near a center?
2. **Scope / inside:**
   - The reframing: a cluster is a **maximal region of high density**, not a ball around a centroid — so k-means' convexity assumption is abandoned. The **DBSCAN** definitions: `ε`-neighborhood, `minPts`, **core / border / noise** points, density-reachability and density-connectivity, all defined precisely; the algorithm walked through.
   - Why DBSCAN **finds non-convex clusters and labels outliers as noise** (the two-moons / concentric-rings example where k-means fails outright). Choosing `ε` via the **k-distance plot**; the headline weakness: a single global density threshold fails on **clusters of varying density** — the honest failure case, with **HDBSCAN** named as the hierarchical-density fix.
   - The curse-of-dimensionality caveat: in high dimensions distances concentrate and `ε` stops separating anything (forward link to UNSP-10's manifold hypothesis as the escape).
3. **Assumes:** UNSP-01; UNSP-06a (as the contrasting clustering paradigm); *(cross-track)* none new.
4. **Sets up:** UNSP-12 (KDE makes the "density" notion fully explicit); UNSP-13 (validating non-convex/noise-aware clusterings).
5. **Depth:** medium–deep (~16–20).

---

## C. Dimensionality Reduction

### UNSP-07 — Principal Component Analysis: The Application
1. **The one question:** Given high-dimensional data, what are the orthogonal directions that capture the most variance, and why is projecting onto them the best linear summary?
2. **Scope / inside:**
   - The two equivalent objectives, both stated and shown equivalent: **maximize variance of the projection** and **minimize reconstruction error** of the projection. Centering the data; the sample covariance matrix `Σ = (1/n)XᵀX` (on centered `X`).
   - The result *consumed, not re-derived*: principal directions are the **eigenvectors of `Σ`** / the **right singular vectors of `X`**, with variance explained `= eigenvalue = σ²`. **We state the SVD/eigendecomposition and cite Geometry of Data for its proof**, then spend the article on *what it means here*: scores, loadings, the rank-`k` truncation as the best rank-`k` approximation (Eckart–Young, stated with citation).
   - Worked example on a real high-dimensional dataset (e.g. faces / spectra): the projection, the reconstruction at increasing `k`, and a first variance-explained plot.
3. **Assumes:** UNSP-00; UNSP-01 (centering, distances/variance). *(cross-track, heavy)* **eigendecomposition of a symmetric matrix, the spectral theorem, the SVD, and the Eckart–Young theorem** [Geometry of Data]; **covariance matrix of a random vector** [Probability Foundations].
4. **Sets up:** UNSP-08 (how to choose `k` and read the output), UNSP-09 (kernelizing it), UNSP-10 (linear PCA as the baseline manifold method).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the variance/reconstruction equivalence into *UNSP-07a "PCA as Variance Maximization"* and *UNSP-07b "PCA via the SVD and Reconstruction,"* if the dual derivation crowds the worked example.

> **OWNERSHIP FLAG (PCA / SVD).** The **SVD and eigendecomposition machinery is OWNED by Geometry of Data** — this track does **not** re-derive the spectral theorem, the existence/uniqueness of the SVD, or Eckart–Young. **UNSP-07–UNSP-09 own the *application and interpretation* of PCA** (variance, scores/loadings, scree, whitening, the kernel trick on PCA) and **link** to Geometry for every factorization fact. Geometry owns "here is the decomposition and why it exists"; Unsupervised owns "here is what it does to a data cloud and how to read it." Confirm this split with the orchestrator so Geometry's roadmap claims the SVD/eigen articles as prerequisites UNSP-07 can point to.

### UNSP-08 — Choosing and Interpreting PCA: Scree, Biplots, and Whitening
1. **The one question:** Once PCA hands back components, how many do we keep, what do they *mean*, and how do we avoid the classic ways of fooling ourselves?
2. **Scope / inside:**
   - Choosing `k`: the **scree plot / elbow**, cumulative variance explained, Kaiser's rule and parallel analysis (stated, with their honest limitations). **Standardize-or-not** as a real modeling decision — PCA on covariance vs. correlation, with a worked example where unscaled units hijack PC1.
   - **Interpretation**: loadings as the recipe for each component; the **biplot** read end-to-end; **whitening / sphering** the scores and when it helps. The interview-grade cautions: components are **not** guaranteed interpretable, signs are arbitrary, and PCA is **unsupervised** so the top components need not be the predictive ones.
   - The honest boundary: PCA assumes **linear** structure and that **variance = signal** — the worked counterexample (a low-variance direction carrying the real label; or curved structure a line can't capture) that motivates the entire nonlinear arc UNSP-09–UNSP-11.
3. **Assumes:** UNSP-07; *(cross-track)* none new.
4. **Sets up:** UNSP-09, UNSP-10, UNSP-11 (each answers a failure PCA exposes here); UNSP-13 (variance-explained is a validation-adjacent diagnostic).
5. **Depth:** medium (~12–16).

### UNSP-09 — Kernel PCA: PCA in a Feature Space You Never Visit
1. **The one question:** PCA only finds linear structure — how do we find *curved* principal directions without ever computing the high-dimensional features explicitly?
2. **Scope / inside:**
   - The **kernel trick** built carefully: an implicit feature map `φ(x)` and a kernel `K(x,x') = ⟨φ(x),φ(x')⟩` (RBF, polynomial) that gives inner products without coordinates. Why PCA can be written **entirely in terms of inner products** (the Gram matrix), which is exactly what makes it kernelizable — derived.
   - **Centering in feature space** done via the kernel matrix (the double-centering formula, derived); eigendecomposition of the centered Gram matrix; projecting a new point. The two-rings / Swiss-roll example where kernel PCA separates what linear PCA cannot.
   - Honest costs and boundaries: the Gram matrix is `n×n` (scales with samples, not features — the opposite trade-off from linear PCA); **no explicit reconstruction** (the pre-image problem); kernel and bandwidth choice is unsupervised and unguided — a real practitioner pain.
3. **Assumes:** UNSP-07, UNSP-08; *(cross-track)* **inner products, the Gram matrix, eigendecomposition** [Geometry of Data]; *the kernel trick / positive-definite kernels* (introduced inline here, the canonical owner is Geometry/Optimization — flagged).
4. **Sets up:** UNSP-10–UNSP-11 (kernel PCA is the bridge from linear PCA to nonlinear manifold methods).
5. **Depth:** deep (~18–24).

### UNSP-10 — Manifold Learning I: The Manifold Hypothesis, MDS and Isomap
1. **The one question:** What if the data lives on a curved low-dimensional surface bent through high-dimensional space — how do we unfold it by preserving *distances along the surface*?
2. **Scope / inside:**
   - The **manifold hypothesis** stated: real high-dimensional data concentrates near a low-dimensional manifold; why **Euclidean distance through the ambient space lies** (two points across a fold are "close" though far along the surface). This is the precise failure of PCA/UNSP-08 that the arc fixes.
   - **Classical MDS**: given a distance matrix, recover coordinates that preserve those distances — derived via double-centering to a Gram matrix and its eigendecomposition (and the result that **MDS with Euclidean distances = PCA**, shown, tying the arc together). **Isomap**: replace ambient distance with **geodesic distance** approximated by shortest paths on a `k`-nearest-neighbor graph, then run MDS — the full pipeline.
   - The honest boundaries: sensitivity to the neighborhood-graph parameter, short-circuiting when the graph bridges folds, and that these methods give a global embedding but scale poorly — the setup for the local neighbor-embedding methods in UNSP-11.
3. **Assumes:** UNSP-07 (PCA as the linear baseline), UNSP-01 (distances), UNSP-06b (neighbor graphs echo DBSCAN's neighborhoods); *(cross-track)* eigendecomposition, the Gram matrix [Geometry of Data]; *shortest-path / graph basics* (built inline).
4. **Sets up:** UNSP-11 (t-SNE/UMAP as the modern, local, probabilistic successors).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut into *UNSP-10a "The Manifold Hypothesis and Classical MDS"* and *UNSP-10b "Isomap and Geodesic Distances"* at the MDS/geodesic boundary.

### UNSP-11 — Manifold Learning II: t-SNE and UMAP, and How to Read Them Honestly
1. **The one question:** How do the neighbor-embedding methods that dominate modern visualization actually work, and — critically — what can and cannot be trusted in the pictures they produce?
2. **Scope / inside:**
   - **t-SNE**: convert pairwise distances to **probabilities of being neighbors** (Gaussian in high-D, **heavy-tailed Student-t in low-D** to relieve crowding — the reason for the t, derived); minimize the **KL divergence** between the two neighbor distributions by gradient descent. **Perplexity** as the effective-neighborhood knob. **UMAP** sketched as the faster, theory-grounded cousin (fuzzy-simplicial neighbor graph + cross-entropy) with the practical differences called out.
   - **The honest-reading section — the heart of the article**: t-SNE/UMAP preserve *local* neighborhoods, so **cluster sizes are meaningless, between-cluster distances are largely meaningless, and apparent clusters can be artifacts of perplexity/seed**. Worked demonstrations: the same data under different perplexities producing different "stories"; random data producing spurious blobs. The rule that these are **exploration and visualization tools, not clustering or distance-preserving tools**.
   - When to reach for what: PCA for a faithful linear summary and preprocessing; Isomap for global geometry; t-SNE/UMAP for local-neighborhood visualization only — never as the input to a downstream metric computation without care.
3. **Assumes:** UNSP-10; *(cross-track)* **KL divergence** and the **Student-t / Gaussian densities** [Probability Foundations]; **gradient descent** [Optimization].
4. **Sets up:** UNSP-13–UNSP-14 (these plots are where over-claiming structure is most tempting — the validation arc cashes the warning).
5. **Depth:** deep (~20–26). **Split seam if needed:** cut into *UNSP-11a "t-SNE"* and *UNSP-11b "UMAP and Reading Neighbor Embeddings Honestly,"* keeping the honest-reading material attached to whichever side carries the demonstrations.

---

## D. Density Estimation

### UNSP-12 — Kernel Density Estimation
1. **The one question:** How do we estimate the full probability density that generated a sample — a smooth curve, not just a histogram — without assuming a parametric family?
2. **Scope / inside:**
   - From the **histogram** (and its bin-edge arbitrariness) to the **KDE**: place a kernel bump at every point and sum, `f̂(x) = (1/nh) Σ K((x−xᵢ)/h)`; kernel choices (Gaussian, Epanechnikov) and why the kernel shape matters far less than the bandwidth. Derived as a smoothed empirical density.
   - **Bandwidth `h` is the whole game**: the bias–variance trade-off (small `h` = spiky/high-variance, large `h` = oversmoothed/biased); the **MISE / AMISE** criterion and the optimal `h ∝ n^{-1/5}` rate derived to the floor's level; **Silverman's rule** and cross-validation for selecting it. (Mirrors the bandwidth story in Regression's nonparametric branch — flagged as a deliberate cross-track echo.)
   - The honest boundary: KDE **breaks in high dimensions** (the curse of dimensionality, the same `n^{-1/(d+4)}` rate collapse) — why density estimation is essentially a low-dimensional tool, and the link back to UNSP-06b (DBSCAN is implicitly a level-set of a density KDE makes explicit) and to UNSP-04 (GMM = a *parametric* density estimator, the contrast).
3. **Assumes:** UNSP-00, UNSP-01; *(cross-track)* **probability density, expectation, bias/variance of an estimator** [Probability Foundations / Statistical Inference]; *convolution/smoothing intuition* (built inline).
4. **Sets up:** UNSP-13 (density-ratio and likelihood-style validation); closes the density family. Connects to GMM (UNSP-04) as the parametric counterpart.
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the estimator definition into *UNSP-12a "Kernel Density Estimation"* and *UNSP-12b "Bandwidth Selection and the Curse of Dimensionality."*

---

## E. Validation and Judgment

### UNSP-13 — Did We Actually Find Anything? Cluster Validation
1. **The one question:** With no labels to check against, how do we measure whether a clustering is good, and how do we choose the number of clusters honestly?
2. **Scope / inside:**
   - **Internal indices** (no labels): the **silhouette** coefficient derived per-point and aggregated; the Davies–Bouldin and Calinski–Harabasz indices stated; the **elbow method** on WCSS and *why it is unreliable* (no sharp elbow on real data). The **gap statistic** derived end-to-end — comparing within-cluster dispersion to its expectation under a null reference distribution — as the principled "how many clusters, including possibly *one*" answer.
   - **Stability / consistency** validation: does the clustering survive resampling/perturbation? **BIC/AIC for model-based clustering** (choosing GMM components, the payoff from UNSP-04/UNSP-05). **External indices** for the rare labeled-benchmark case (Adjusted Rand Index, normalized mutual information) — stated, with the caution that they need ground truth you usually don't have.
   - The interview-grade boundary: every index encodes its *own* assumption about cluster shape (silhouette favors convex/compact clusters and will punish a correct DBSCAN partition) — so validation must match the algorithm's geometry; there is no assumption-free cluster-quality number.
3. **Assumes:** UNSP-02, UNSP-04, UNSP-06a, UNSP-06b (the things being validated); *(cross-track)* **expectation under a reference/null distribution, BIC/AIC** [Statistical Inference]; resampling/bootstrap [Statistical Inference, E1].
4. **Sets up:** UNSP-14 (synthesis).
5. **Depth:** deep (~20–26). **Split seam if needed:** cut into *UNSP-13a "Internal Indices and the Gap Statistic"* and *UNSP-13b "Stability, Model Selection (BIC), and External Indices."*

### UNSP-14 — The Unsupervised Reality Check
1. **The one question:** Across every method in this track, how does a practitioner decide what to run, trust, and report when there is no answer key — and when is the honest answer "there is no structure here"?
2. **Scope / inside:**
   - A **decision map** synthesizing the track: data shape → method. Convex blobs → k-means/GMM; arbitrary shapes + noise → DBSCAN; need all granularities → hierarchical; reduce-then-cluster vs. cluster-in-high-D; visualize → t-SNE/UMAP (with UNSP-11's warnings); estimate density → KDE/GMM. Each with the *assumption* it commits to (the recurring theme from UNSP-00, now cashed).
   - The **null-result discipline**: how to test "is there *any* clustering structure?" (the gap statistic returning `k=1`, the Hopkins statistic, stability collapse) — and the professional courage to report "no reliable structure," the most under-taught skill in the subject.
   - The overfitting-without-a-test-set danger unique to unsupervised learning: how preprocessing, distance choice, and parameter tuning can *manufacture* structure, and the guardrails (hold-out stability, multiple methods agreeing, domain sanity-check) that keep a discovery honest.
3. **Assumes:** the whole track (UNSP-01–UNSP-13).
4. **Sets up:** Terminal node. Hands off to a future **Representation Learning / Autoencoders** track (nonlinear, learned embeddings), a **Recommender / Matrix Factorization** track (NMF, latent factors), and an **Anomaly Detection** track (density + distance, built on UNSP-06b/UNSP-12).
5. **Depth:** medium (~12–16). Synthesis and judgment; light on new derivation.

---

## Linear reading order

**UNSP-00 → UNSP-01 → UNSP-02 → UNSP-03 → UNSP-04 → UNSP-05 → UNSP-06a → UNSP-06b → UNSP-07 → UNSP-08 → UNSP-09 → UNSP-10 → UNSP-11 → UNSP-12 → UNSP-13 → UNSP-14.**

The three families (clustering UNSP-01–UNSP-06b, dimensionality reduction UNSP-07–UNSP-11, density UNSP-12) are independent after UNSP-00 and may be read in any order; **UNSP-13–UNSP-14 require having seen at least the clustering family** and are the intended close.

---

## Cross-track prerequisites (belong to OTHER tracks)

Pulled in at the points noted. This track does **not** build these; they are named so the prerequisite chain (§1.4) is explicit.

**From Geometry of Data / Applied Linear Algebra**
- *Norms, inner products, the Euclidean metric; positive-definite matrices (Mahalanobis)* — needed at **UNSP-01**.
- *Gradient of a sum of squares / setting a derivative to zero* — needed at **UNSP-02** (also Calc-1 floor).
- *Eigendecomposition of a symmetric matrix, the spectral theorem, the SVD, Eckart–Young* — needed at **UNSP-07** (**this is the core thing PCA consumes — Geometry owns it**).
- *Inner products and the Gram matrix; positive-definite kernels / the kernel trick* — needed at **UNSP-09** (kernel trick co-owned with Optimization; introduced inline here).
- *Eigendecomposition and double-centering to a Gram matrix* — needed at **UNSP-10**.

**From Probability Foundations**
- *Random sample; covariance matrix of a random vector* — needed at **UNSP-00, UNSP-07**.
- *Sampling from a discrete distribution; expectation* — needed at **UNSP-03**.
- *Multivariate Gaussian density; Bayes' rule for a latent label; marginalization over a latent variable* — needed at **UNSP-04**.
- *Jensen's inequality; KL divergence and its non-negativity; concavity of log* — needed at **UNSP-05** (the EM derivation).
- *Student-t and Gaussian densities; KL divergence* — needed at **UNSP-11**.
- *Probability density; bias/variance of an estimator* — needed at **UNSP-12**.

**From Optimization**
- *Coordinate descent / alternating minimization* — needed at **UNSP-02** (Lloyd's) and **UNSP-05** (EM).
- *Gradient descent* — needed at **UNSP-11** (t-SNE/UMAP).
- *Positive-definite kernels / the kernel trick (theory)* — co-owner for **UNSP-09**.

**From Statistical Inference**
- *MLE as a general estimation principle* — needed at **UNSP-04, UNSP-05** (GMM/EM are MLE under latent variables).
- *AIC/BIC for model selection; expectation under a null/reference distribution; the bootstrap (stability)* — needed at **UNSP-13**.

---

## Overlaps & ownership

Recommendation, consistent with the rest of the series: **this track owns the *unsupervised structure-discovery* methods and their interpretation; it links to other tracks for the generic machinery underneath.**

| Shared topic | **Recommended owner** | Rationale |
|---|---|---|
| **SVD / eigendecomposition / spectral theorem / Eckart–Young** | **Geometry of Data** | The factorization and its existence are linear algebra; Unsupervised (UNSP-07–UNSP-09) *applies* it. **Do not re-derive here.** |
| **PCA as a method** (variance, scores/loadings, scree, biplot, whitening, kernel PCA) | **Unsupervised Learning (UNSP-07–UNSP-09)** | The data-analysis application and interpretation; Geometry supplies only the decomposition. |
| **EM algorithm + the ELBO (general latent-variable theory)** | **Unsupervised Learning (UNSP-05), co-claimable with Statistical Inference** | EM's canonical motivating instances (GMM, soft clustering) live here, so UNSP-05 is where it is most motivated. Inference carries a *connection* note ("MLE with a latent variable → EM, see UNSP-05"), not a re-derivation. If a future variational/latent-variable track appears, the general ELBO migrates there and both link. **Confirm with orchestrator.** |
| **GMM as a density estimator / mixture model** | **Unsupervised Learning (UNSP-04)** | A clustering + density method; the multivariate Gaussian itself is Probability's. |
| **MLE principle; Fisher info; AIC/BIC; bootstrap** | **Statistical Inference** | General estimation/uncertainty machinery; UNSP-04/UNSP-05/UNSP-13 consume it. |
| **Multivariate Gaussian, KL divergence, Jensen's inequality** | **Probability Foundations** | Core probability objects; imported at UNSP-04/UNSP-05/UNSP-11. |
| **Convexity, coordinate/gradient descent** | **Optimization** | Lloyd's (UNSP-02) and EM (UNSP-05) are *instances* of alternating minimization; t-SNE (UNSP-11) uses gradient descent. We name the framing and link. |
| **Kernel trick / positive-definite kernels** | **Geometry of Data / Optimization (co-owned)** | Used here at UNSP-09 (kernel PCA); introduced inline minimally and flagged for the owning track. The same kernel theory is consumed by Regression (kernel regression) and any future SVM/Classification track — a strong reason to own it centrally upstream. |
| **Bandwidth selection / bias–variance of smoothing** | **Shared with Regression (deliberate echo)** | KDE's bandwidth story (UNSP-12) mirrors Regression's kernel/local-regression bandwidth articles. Each track derives it in its own context (density vs. conditional mean); they cross-reference rather than one owning both. |
| **DBSCAN / density-based clustering, hierarchical clustering, validation indices** | **Unsupervised Learning** | No other track claims these; fully owned here. |

**Relation to Classification and Causal Inference (being designed concurrently):** Unsupervised feeds **Classification** (clusters/PCA features as inputs; the kernel trick is shared; GMM is a generative classifier's unsupervised half) but does **not** own any labeled-prediction method — that boundary is clean. There is **no overlap with Causal Inference**; structure discovery makes no causal claim, and UNSP-14 explicitly warns that a cluster or component is not a cause.

**One-line ownership rule:** *the unsupervised method and how to read its output are this track's; the linear-algebra factorization, the probability objects, and the generic optimization/estimation guarantees beneath it belong upstream, and this track links rather than re-derives — with EM (UNSP-05) the one piece this track claims as primary owner against Statistical Inference.*

---

### Summary of decisions
- **Name:** Unsupervised Learning.
- **Aim:** find structure in unlabeled data — clustering, dimensionality reduction, density estimation — and, equally, judge whether that structure is real.
- **Boundary:** owns the methods and their interpretation; links to Geometry (SVD/eigen), Probability (densities, KL, Jensen), Optimization (descent), and Inference (MLE, BIC, bootstrap) for the machinery beneath.
- **Two flagged ownership calls:** **PCA/SVD** — Geometry owns the decomposition, Unsupervised owns the application (UNSP-07–UNSP-09); **EM** — Unsupervised owns the operational article (UNSP-05), co-claimable with Inference, to confirm.
- **16 articles** (UNSP-00–UNSP-14, with UNSP-06a/UNSP-06b split) across four families plus a validation spine, each inch-wide and building on the last, with 8 named split seams for the deep articles.
