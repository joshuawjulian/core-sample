# Core Sample — Track Roadmap: **Geometry of Data**

> Roadmap only — no article prose. Governed by `../CLAUDE.md`. Read on demand.

*An inch wide, a mile deep. Linear algebra told as geometry — every matrix is a picture, every column is a direction, every dataset is a cloud of points in a room with as many walls as it has features.*

This is a **foundational track**. Its job is to hand the rest of the series — Regression, Statistical Inference, Optimization, Classification, Unsupervised Learning, Causal Inference — every linear-algebra tool they lean on, built from the Calc-1 floor and told **geometrically**: we always ask *where is this in space and what is it doing to the cloud*, never "manipulate these symbols." Abstract vector-space axiomatics, field theory, and proof-for-proof's-sake are deliberately out of scope; we build exactly the geometry the data-science tracks request, and we build it all the way down.

The spine is: **what a vector is → how vectors combine and span space → length, angle, and orthogonality → projection (the single most important operation in the series) → matrices as maps → solving and inverting → rank and the four subspaces → eigenstructure → the spectral picture of symmetric/PD matrices → the SVD (the master decomposition) → vector calculus on top of all of it (gradient, Hessian, quadratic forms) → numerical reality (conditioning, Cholesky, stability)**. Every above-the-floor idea is built inside an article here; this track assumes essentially nothing but precalc/Calc-1.

---

## The flow diagram

```
                         [GEOM-0] What Is a Vector, Really? (an arrow and a row of data)
                                          │
                                          ▼
                         [GEOM-1] Adding & Scaling: Linear Combinations
                                          │
                                          ▼
                         [GEOM-2] Span & Subspaces (the set of places you can reach)
                                          │
                                          ▼
                         [GEOM-3] Linear Independence, Basis & Dimension
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                                                ▼
   [GEOM-4] The Dot Product: Length & Angle              [GEOM-5] Orthogonality & Orthonormal Bases
                  │                                                │
                  └───────────────────────┬────────────────────────┘
                                          ▼
                         [GEOM-6] Orthogonal Projection onto a Subspace  ◄── the keystone
                                          │
                                          ▼
                         [GEOM-7] Gram–Schmidt & the QR Decomposition
                                          │
                                          ▼
                         [GEOM-8] Matrices as Linear Maps (columns are where the axes go)
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                        ▼                        ▼
   [GEOM-9] Matrix Multiplication      [GEOM-10] Transpose &        [GEOM-11] Solving Ax=b:
   as Composition                  What It Means            Inverse, Singularity
                  │                        │                        │
                  └───────────────────────┼────────────────────────┘
                                          ▼
                         [GEOM-12] Rank & the Four Fundamental Subspaces
                                          │
                                          ▼
                         [GEOM-13] Determinant: Signed Volume & Invertibility
                                          │
                                          ▼
                         [GEOM-14] Eigenvalues & Eigenvectors (the directions a map only stretches)
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                                                ▼
   [GEOM-15] Diagonalization &                        [GEOM-16] Symmetric Matrices &
   the Eigendecomposition                         the Spectral Theorem
                  │                                                │
                  └───────────────────────┬────────────────────────┘
                                          ▼
                         [GEOM-17] Quadratic Forms (a number from a matrix and a direction)
                                          │
                                          ▼
                         [GEOM-18] Positive-Definite Matrices (the "good" matrices)
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                                                ▼
   [GEOM-19] Cholesky & the                            [GEOM-20] The Singular Value
   Matrix Square Root                              Decomposition (the master factorization)
                  │                                                │
                  └───────────────────────┬────────────────────────┘
                                          ▼
                         [GEOM-21] SVD in Action: Low-Rank Approximation & the Pseudoinverse
                                          │
       ┌──────────────────────────────────┼──────────────────────────────────┐
       ▼                                   ▼                                   ▼
[GEOM-22] Vectors of Numbers:        [GEOM-23] The Gradient as a         [GEOM-24] The Hessian &
Vector & Matrix Calculus         Direction in Space              the Curvature of a Surface
(differentiating wrt a vector)   (steepest ascent, geometrically)        │
       │                                   │                              │
       └───────────────────────────────────┼──────────────────────────────┘
                                          ▼
                         [GEOM-25] The Gradient & Hessian of a Quadratic Form
                                          │
                                          ▼
                         [GEOM-26] Condition Number & Numerical Stability
                                          │
                                          ▼
                         [GEOM-27] How These Tools Power Data Science (the bridge article)
```

Linear reading order: **GEOM-0 → GEOM-1 → … → GEOM-27.** The track is a single mostly-linear build with a handful of "read-as-a-pair" forks (GEOM-4/GEOM-5, GEOM-9–GEOM-11, GEOM-15/GEOM-16, GEOM-19/GEOM-20, GEOM-22–GEOM-24). The keystone is **GEOM-6 (projection)**; the two summits are **GEOM-20 (SVD)** and **GEOM-25 (gradient/Hessian of a quadratic form)**, which between them discharge the heaviest cross-track requests.

---

## Movement I — Vectors and the Space They Live In

### GEOM-0 — What Is a Vector, Really?
1. **The one question:** What *is* a vector — as a geometric arrow, as a list of numbers, and as a row of a dataset — and why are those the same object?
2. **Scope / inside:**
   - The three faces of a vector: an arrow with magnitude and direction; an ordered tuple in `ℝⁿ`; one observation's feature values (one row of a data table).
   - Coordinates as "how far along each axis"; the zero vector; why a point and the arrow from the origin to it are interchangeable.
   - The leap past visual intuition: a 100-feature row *is* a point in `ℝ¹⁰⁰`, and we reason about it with the same rules even though we cannot draw it.
3. **Assumes:** Only the floor (the Cartesian plane, ordered pairs, functions).
4. **Sets up:** GEOM-1 (combining vectors), and the whole "a dataset is a cloud of points" framing the track runs on.
5. **Depth:** short (~8–12). Motivational, picture-first.

### GEOM-1 — Adding and Scaling: The Linear Combination
1. **The one question:** What are the only two operations linear algebra lets you do to vectors, and what do they look like geometrically?
2. **Scope / inside:**
   - Vector addition (tip-to-tail / parallelogram) and scalar multiplication (stretch/flip) — defined componentwise, drawn geometrically.
   - The **linear combination** `c₁v₁ + … + c_k v_k` as the one move from which everything else is built; the eight vector-space rules stated *as the rules these two operations obey*, not as abstract axioms.
   - Worked example: combining feature vectors; a weighted average as a linear combination with coefficients summing to one.
3. **Assumes:** GEOM-0.
4. **Sets up:** GEOM-2 (span is "all linear combinations"), GEOM-8 (a matrix acts by taking linear combinations of its columns).
5. **Depth:** short–medium (~10–14).

### GEOM-2 — Span and Subspaces: The Set of Places You Can Reach
1. **The one question:** Given a handful of vectors, exactly which points in space can you build from them, and what shape does that set form?
2. **Scope / inside:**
   - **Span** as the set of all linear combinations; building intuition from one vector (a line), two (a plane or a line), three, up.
   - **Subspace** defined by closure under addition and scaling; why every subspace contains the origin; lines and planes through the origin as the canonical pictures.
   - The honest edge case: vectors that *look* independent but span a lower-dimensional set (collinearity preview, ties to Regression's multicollinearity).
3. **Assumes:** GEOM-1.
4. **Sets up:** GEOM-3 (independence/basis), GEOM-6 (we project onto a subspace), GEOM-12 (column space and the four subspaces).
5. **Depth:** medium (~12–18).

### GEOM-3 — Linear Independence, Basis, and Dimension
1. **The one question:** When does a set of vectors carry redundant information, and what is the smallest set that still reaches every point in a subspace?
2. **Scope / inside:**
   - **Linear independence** defined via the only-the-trivial-combination-gives-zero condition; the geometric reading (no vector lies in the span of the others).
   - **Basis** as a minimal spanning set; **dimension** as the (provably) invariant count; coordinates *relative to a basis*.
   - Worked example: detecting that one feature is a linear combination of others (a redundant column) and what that does to dimension.
3. **Assumes:** GEOM-2.
4. **Sets up:** GEOM-5 (orthonormal bases), GEOM-12 (rank = dimension of the column space), GEOM-14 (eigenvectors as a basis).
5. **Depth:** medium (~12–18).

---

## Movement II — Length, Angle, and the Keystone: Projection

### GEOM-4 — The Dot Product: Length and Angle from Coordinates
1. **The one question:** How do we recover geometric length and the angle between two vectors from nothing but their coordinates?
2. **Scope / inside:**
   - The **dot product** `xᵀy = Σ xᵢyᵢ` defined; the **norm** `‖x‖ = √(xᵀx)` as length (Pythagoras in `n` dimensions, derived).
   - `xᵀy = ‖x‖‖y‖cosθ` derived via the law of cosines; the **Cauchy–Schwarz** inequality and what it guarantees.
   - The inner product as the general object (dot product is the standard one); data meaning: dot products measure alignment/similarity (cosine similarity preview).
3. **Assumes:** GEOM-1; floor-level trig (`cos`, law of cosines — restated inline).
4. **Sets up:** GEOM-5 (orthogonality is "dot product zero"), GEOM-6 (projection is built from dot products), GEOM-17 (quadratic forms generalize `xᵀx`).
5. **Depth:** medium (~12–18).

### GEOM-5 — Orthogonality and Orthonormal Bases
1. **The one question:** What does it mean for vectors to be perpendicular in `n` dimensions, and why are orthonormal bases the nicest coordinate systems to work in?
2. **Scope / inside:**
   - **Orthogonality** as `xᵀy = 0`; orthogonal *sets*; the generalized **Pythagorean theorem** `‖x+y‖² = ‖x‖²+‖y‖²` when orthogonal, derived.
   - **Orthonormal** vectors; why coordinates in an orthonormal basis are just dot products (`cᵢ = qᵢᵀx`) — derived, and the headline reason orthonormal bases are computationally golden.
   - **Orthogonal complement** of a subspace; every vector splits uniquely into "in the subspace" + "perpendicular to it" (the decomposition GEOM-6 exploits).
3. **Assumes:** GEOM-3, GEOM-4.
4. **Sets up:** GEOM-6 (projection), GEOM-7 (Gram–Schmidt produces orthonormal bases), GEOM-16 (spectral theorem gives an orthonormal eigenbasis).
5. **Depth:** medium (~12–18).

### GEOM-6 — Orthogonal Projection onto a Subspace  ⟂ *(the keystone)*
1. **The one question:** Given a point and a subspace, what is the closest point in the subspace to it, and why is "drop a perpendicular" the answer?
2. **Scope / inside:**
   - Projection onto a single vector derived from scratch (`(aᵀx / aᵀa) a`); the residual is orthogonal to `a` — proved.
   - Projection onto a general subspace = column space of `A`: the **normal equations** `AᵀA ĉ = Aᵀx` derived purely geometrically (residual ⟂ every column), giving the **projection matrix** `P = A(AᵀA)⁻¹Aᵀ`.
   - `P` is symmetric and idempotent (`P² = P`) — proved; projection as "the part of `x` that lives in the subspace"; the closest-point / least-distance characterization.
   - This is the article Regression's least-squares geometry stands on; the *why* is explicitly "least squares = projection."
3. **Assumes:** GEOM-2, GEOM-3, GEOM-5; matrix notation for `A`, `Aᵀ`, `(AᵀA)⁻¹` is used lightly here and built properly in GEOM-8–GEOM-11 (forward-referenced; the geometry is self-contained, the algebra is named).
4. **Sets up:** GEOM-7 (an orthonormal basis makes `P` trivial), GEOM-12 (column space), GEOM-20–GEOM-21 (SVD/pseudoinverse as the stable projection); **directly feeds Regression R4/R5**.
5. **Depth:** deep (~20–28). **Split seam if needed:** cut after projection-onto-a-line into *GEOM-6a "Projection onto a Line"* and *GEOM-6b "Projection onto a Subspace & the Projection Matrix,"* at the single-vector / general-subspace boundary.

### GEOM-7 — Gram–Schmidt and the QR Decomposition
1. **The one question:** Given any basis, how do we manufacture an orthonormal one spanning the same space, and what factorization falls out for free?
2. **Scope / inside:**
   - The **Gram–Schmidt** process built one projection at a time (each new vector minus its projection onto the span so far) — derived using GEOM-6.
   - The **QR decomposition** `A = QR` (`Q` orthonormal columns, `R` upper-triangular) as Gram–Schmidt bookkept in matrix form; why `Q` makes projection `P = QQᵀ`.
   - Numerical aside (kept secondary): classical vs. modified Gram–Schmidt and why orthogonality decays — first taste of the numerical-stability theme that closes the track.
3. **Assumes:** GEOM-5, GEOM-6.
4. **Sets up:** GEOM-11/GEOM-12 (QR as a way to solve least-squares stably), GEOM-26 (stability); offered to Regression as the numerically sound least-squares route.
5. **Depth:** medium–deep (~16–22).

---

## Movement III — Matrices as Maps

### GEOM-8 — Matrices as Linear Maps: Columns Are Where the Axes Go
1. **The one question:** What does a matrix *do* to space, and why is "the columns tell you where the basis vectors land" the whole story?
2. **Scope / inside:**
   - A matrix as a **linear transformation** `x ↦ Ax`; `Ax` as a linear combination of `A`'s columns (the single most useful reading in the track).
   - The two equivalent views of `Ax`: combination-of-columns vs. row-by-row dot products; what linearity (`A(x+y)=Ax+Ay`, `A(cx)=cAx`) buys us.
   - Geometric gallery: rotation, scaling, shear, reflection, projection — each as a small matrix acting on a unit grid, drawn.
3. **Assumes:** GEOM-1, GEOM-4.
4. **Sets up:** GEOM-9 (composition), GEOM-14 (eigenvectors = directions a map only scales), the entire matrix half of the track.
5. **Depth:** medium (~12–18).

### GEOM-9 — Matrix Multiplication as Composition of Maps
1. **The one question:** Why is matrix multiplication defined by that row-times-column rule, and why isn't it commutative?
2. **Scope / inside:**
   - `AB` = "do `B`, then `A`"; deriving the row-dot-column entry formula *from* the composition requirement (so the rule is inevitable, not arbitrary).
   - Dimensions and conformability; associativity (proved) vs. non-commutativity (counterexample with two rotations/shears, drawn).
   - Block multiplication and the outer-product view (`AB = Σ` column-times-row), which the SVD will reuse.
3. **Assumes:** GEOM-8.
4. **Sets up:** GEOM-10, GEOM-11, GEOM-20 (outer-product sum is the SVD), and every downstream derivation.
5. **Depth:** medium (~12–18).

### GEOM-10 — The Transpose and What It Means Geometrically
1. **The one question:** Beyond "flip rows and columns," what does the transpose *mean*, and why does `Aᵀ` keep showing up next to `A`?
2. **Scope / inside:**
   - Transpose defined; the identities `(AB)ᵀ = BᵀAᵀ`, `(Aᵀ)ᵀ = A` derived; the adjoint relation `⟨Ax, y⟩ = ⟨x, Aᵀy⟩` and what it says geometrically.
   - Why `AᵀA` (Gram matrix) is the natural object: it holds all pairwise dot products of columns; it is symmetric and (next track entry) positive semidefinite.
   - **Symmetric matrices** introduced as `A = Aᵀ`; preview of why they are special (spectral theorem in GEOM-16).
3. **Assumes:** GEOM-4, GEOM-9.
4. **Sets up:** GEOM-6's `AᵀA`, GEOM-12 (the four subspaces pair `A` with `Aᵀ`), GEOM-16, GEOM-17–GEOM-18 (`AᵀA` is PSD).
5. **Depth:** medium (~12–16).

### GEOM-11 — Solving `Ax = b`: The Inverse, Singularity, and What "No Solution" Means
1. **The one question:** When can we undo a linear map to solve `Ax = b`, when can't we, and what is the geometric meaning of each case?
2. **Scope / inside:**
   - Gaussian elimination as a sequence of linear maps; the **inverse** `A⁻¹` defined and computed; `(AB)⁻¹ = B⁻¹A⁻¹`, `(Aᵀ)⁻¹ = (A⁻¹)ᵀ` derived.
   - Three geometric outcomes: unique solution (invertible), no solution (`b` outside the column space — the bridge back to projection/least-squares in GEOM-6), infinitely many (nontrivial null space).
   - When *not* to literally invert: solve, don't invert (numerical foreshadowing for GEOM-26); the inverse exists ⇔ full rank ⇔ nonzero determinant (pointers to GEOM-12/GEOM-13).
3. **Assumes:** GEOM-8, GEOM-9, GEOM-10.
4. **Sets up:** GEOM-12 (rank), GEOM-13 (determinant), GEOM-19 (Cholesky solve), GEOM-21 (pseudoinverse for the no-/many-solution cases); **feeds Regression R5** (the `(XᵀX)⁻¹` object).
5. **Depth:** medium–deep (~16–22).

### GEOM-12 — Rank and the Four Fundamental Subspaces
1. **The one question:** How much "real" dimensionality does a matrix carry, and how do its four associated subspaces fit together?
2. **Scope / inside:**
   - **Rank** as the dimension of the column space = dimension of the row space (proved equal); full rank vs. rank-deficient, with the data reading (redundant features).
   - The **four subspaces**: column space, null space, row space, left null space; the **rank–nullity theorem** derived; the orthogonality pairing (row space ⟂ null space) drawn.
   - The honest tie-in: near-rank-deficiency is multicollinearity (Regression R7) and the thing the condition number (GEOM-26) measures.
3. **Assumes:** GEOM-3, GEOM-6 (orthogonal complement), GEOM-8, GEOM-11.
4. **Sets up:** GEOM-14/GEOM-15 (eigenstructure), GEOM-20 (SVD reads rank off the singular values), GEOM-26; **feeds Regression R5/R7**.
5. **Depth:** deep (~18–24).

### GEOM-13 — The Determinant: Signed Volume and Invertibility
1. **The one question:** What single number tells you whether a map is invertible, and why is "volume scaling factor" the right way to understand it?
2. **Scope / inside:**
   - The determinant as the **signed volume** of the image of the unit cube; `det = 0` ⇔ the map collapses space ⇔ singular — derived geometrically before any cofactor formula.
   - Key properties (`det(AB)=det A det B`, effect of row ops, `det(Aᵀ)=det A`) derived from the volume picture; `2×2`/`3×3` formulas as special cases.
   - Where it actually matters in data science (the change-of-variables Jacobian for densities — a hook for Probability/Inference) and where it's overrated (don't test singularity by `det≈0`; use the condition number — pointer to GEOM-26).
3. **Assumes:** GEOM-8, GEOM-9, GEOM-11.
4. **Sets up:** GEOM-14 (the characteristic polynomial `det(A−λI)=0`), the Jacobian hook for the Probability track.
5. **Depth:** medium (~12–18).

---

## Movement IV — Eigenstructure and the Spectral Picture

### GEOM-14 — Eigenvalues and Eigenvectors: The Directions a Map Only Stretches
1. **The one question:** Are there special directions a matrix leaves pointing the same way, only scaled, and how do we find them?
2. **Scope / inside:**
   - **Eigenvector/eigenvalue** defined by `Av = λv`; the geometric picture (invariant directions of the transformation gallery from GEOM-8).
   - Finding them: the **characteristic polynomial** `det(A−λI)=0` (using GEOM-13), then the null space of `A−λI` for each `λ`; worked `2×2` and `3×3` by hand.
   - Honest complications: complex eigenvalues (rotation has none real), repeated eigenvalues, defective matrices that *can't* be diagonalized — stated so the reader knows the limits before GEOM-15.
3. **Assumes:** GEOM-8, GEOM-11, GEOM-13.
4. **Sets up:** GEOM-15 (diagonalization), GEOM-16 (symmetric case is clean), GEOM-18 (PD ⇔ positive eigenvalues), GEOM-26 (condition number = eigenvalue ratio).
5. **Depth:** deep (~18–24). **Split seam if needed:** cut after the definition/geometry into *GEOM-14a "What Eigenvectors Are"* and *GEOM-14b "Finding Them via the Characteristic Polynomial."*

### GEOM-15 — Diagonalization and the Eigendecomposition
1. **The one question:** When can we rewrite a matrix as `A = VΛV⁻¹`, and why does that make the matrix's action — and its powers — transparent?
2. **Scope / inside:**
   - **Eigendecomposition** `A = VΛV⁻¹` derived; the condition (a full set of independent eigenvectors); "change to the eigenbasis, scale, change back" as the geometric story.
   - Why it makes `Aᵏ`, matrix exponentials, and repeated application trivial (`Aᵏ = VΛᵏV⁻¹`) — derived; the data reading (dynamics, power iteration, PageRank-style processes).
   - The honest boundary: non-diagonalizable matrices, and why we'll often want a decomposition that *always* exists (motivating the SVD in GEOM-20).
3. **Assumes:** GEOM-14.
4. **Sets up:** GEOM-16 (symmetric ⇒ orthogonal `V`), GEOM-20 (SVD as the always-available cousin).
5. **Depth:** medium–deep (~16–22).

### GEOM-16 — Symmetric Matrices and the Spectral Theorem
1. **The one question:** Why are symmetric matrices the best-behaved matrices in all of linear algebra, and what does the spectral theorem promise?
2. **Scope / inside:**
   - **Spectral theorem**: a real symmetric matrix has real eigenvalues and an **orthonormal** eigenbasis, so `A = QΛQᵀ` — both claims proved (real eigenvalues; orthogonality of eigenvectors for distinct eigenvalues).
   - Geometric reading: a symmetric matrix acts by "rotate to the eigenaxes, scale along each, rotate back" — no shearing, ever; drawn on an ellipse.
   - Why this matters for data: covariance matrices, Gram matrices `AᵀA`, and Hessians are all symmetric — so this theorem is the engine behind PCA, quadratic forms, and second-order optimization.
3. **Assumes:** GEOM-5 (orthonormal bases), GEOM-10 (symmetry), GEOM-15.
4. **Sets up:** GEOM-17 (diagonalizing a quadratic form), GEOM-18 (PD via eigenvalues), GEOM-20 (SVD built from `AᵀA`'s spectral decomposition); **feeds Unsupervised Learning's PCA** and **Inference's Fisher-information matrix**.
5. **Depth:** deep (~18–24).

---

## Movement V — Quadratic Forms, Positive-Definiteness, and the SVD

### GEOM-17 — Quadratic Forms: A Number from a Matrix and a Direction
1. **The one question:** What is the geometry of the scalar `xᵀAx`, and why does every such surface turn out to be a (rotated, scaled) bowl, saddle, or ridge?
2. **Scope / inside:**
   - **Quadratic form** `q(x) = xᵀAx` defined; symmetrizing `A` WLOG; expanding it in coordinates so the reader sees the squares and cross-terms.
   - Diagonalizing the form with the spectral theorem (`x = Qz` ⇒ `q = Σ λᵢ zᵢ²`): the eigenvalues' **signs** decide bowl (all `>0`), inverted bowl (all `<0`), or saddle (mixed) — drawn as level sets (ellipses/hyperbolas).
   - Data meaning: variance along a direction `uᵀΣu`, the squared Mahalanobis distance, the loss surface of least squares — all quadratic forms; this is the unifying picture for the rest of the track.
3. **Assumes:** GEOM-4, GEOM-10, GEOM-16.
4. **Sets up:** GEOM-18 (definiteness), GEOM-25 (gradient/Hessian of `xᵀAx`); **feeds Inference B3–B4** (Fisher info quadratic form) and **Optimization** (quadratic model of a loss).
5. **Depth:** medium–deep (~16–22).

### GEOM-18 — Positive-Definite Matrices: The "Good" Matrices
1. **The one question:** What does it mean for a matrix to be positive-definite, why is that exactly "the quadratic form is a bowl with a unique bottom," and how do we check it?
2. **Scope / inside:**
   - **PD / PSD** defined by `xᵀAx > 0` (resp. `≥ 0`) for all `x ≠ 0`; equivalence to **all eigenvalues positive** (resp. nonnegative), proved via GEOM-17.
   - Why `AᵀA` is always PSD (and PD iff `A` has full column rank) — derived; covariance matrices and Gram matrices as the canonical PD/PSD objects in data.
   - Tests: eigenvalues, leading principal minors (Sylvester), and "a Cholesky factor exists" (forward ref to GEOM-19); the data payoff — PD Hessian ⇒ a genuine minimum (Optimization), PD covariance ⇒ a valid Gaussian (Probability/Inference).
3. **Assumes:** GEOM-16, GEOM-17.
4. **Sets up:** GEOM-19 (Cholesky / square root), GEOM-24–GEOM-25 (PD Hessian = local min); **feeds Regression R11** (PD covariance, whitening) and **Optimization** (convexity test).
5. **Depth:** deep (~18–24).

### GEOM-19 — Cholesky and the Matrix Square Root
1. **The one question:** How do we factor a positive-definite matrix into a "square," and why does that single trick power simulation, whitening, and fast solves?
2. **Scope / inside:**
   - **Cholesky** `A = LLᵀ` (`L` lower-triangular) derived constructively, entry by entry; existence ⇔ PD (ties to GEOM-18).
   - The **matrix square root** `A^{1/2} = QΛ^{1/2}Qᵀ` from the spectral theorem (GEOM-16) and how it differs from Cholesky (symmetric vs. triangular factor); both are "square roots" for different jobs.
   - Three data payoffs worked: **whitening/decorrelating** data (`Σ^{-1/2}` — directly Regression's GLS), **sampling** a correlated Gaussian (`Lz`), and **solving** PD systems faster than general inversion.
3. **Assumes:** GEOM-11, GEOM-18.
4. **Sets up:** GEOM-26 (Cholesky as the stable PD solve); **directly feeds Regression R11** (GLS / matrix square root) and Probability/Inference (Gaussian sampling).
5. **Depth:** medium–deep (~16–22).

### GEOM-20 — The Singular Value Decomposition: The Master Factorization
1. **The one question:** Is there one decomposition that works for *every* matrix — rectangular, rank-deficient, anything — and reveals its complete geometry?
2. **Scope / inside:**
   - **SVD** `A = UΣVᵀ` derived from the spectral theorem applied to `AᵀA` and `AAᵀ` (every step: singular values = `√` of eigenvalues of `AᵀA`, right/left singular vectors, the `Av_i = σ_i u_i` relation) — proved, always exists.
   - The geometry: *every* linear map is "rotate (`Vᵀ`), scale along orthogonal axes (`Σ`), rotate (`U`)" — the cleanest picture in the track, drawn as a circle → ellipse.
   - Reading structure off the SVD: rank (count of nonzero `σ`), the four subspaces (from `U`/`V` blocks), `‖A‖₂ = σ_max` — and the relationship to the eigendecomposition (identical for symmetric PSD `A`).
3. **Assumes:** GEOM-12, GEOM-15, GEOM-16.
4. **Sets up:** GEOM-21 (low-rank/pseudoinverse), GEOM-26 (condition number `= σ_max/σ_min`); **shared keystone with Unsupervised Learning's PCA** and **feeds Regression R14** (ridge in the SVD basis).
5. **Depth:** deep (~22–30). **Split seam if needed:** cut after the existence proof into *GEOM-20a "Deriving the SVD"* and *GEOM-20b "Reading a Matrix's Geometry off Its SVD,"* at the construction/interpretation boundary.

### GEOM-21 — SVD in Action: Low-Rank Approximation and the Pseudoinverse
1. **The one question:** Once we have the SVD, how do we get the best low-rank approximation of a matrix and a "solve" for systems that have no inverse?
2. **Scope / inside:**
   - **Eckart–Young**: truncating the SVD to the top `k` singular values gives the best rank-`k` approximation (in Frobenius/spectral norm) — stated and argued; the energy `Σσ²` and the variance-captured reading.
   - The **Moore–Penrose pseudoinverse** `A⁺ = VΣ⁺Uᵀ`; how it gives the minimum-norm least-squares solution — the stable, always-defined version of GEOM-6's projection and GEOM-11's solve.
   - Worked applications kept honest and tied to owners: image/data compression, latent structure; explicitly flagged that the *statistical interpretation* (PCA as variance maximization on centered data) is **Unsupervised Learning's** to own — this article supplies the linear-algebra machinery, not the statistics.
3. **Assumes:** GEOM-6, GEOM-11, GEOM-20.
4. **Sets up:** the PCA hand-off to Unsupervised Learning; the pseudoinverse used by Regression for rank-deficient designs.
5. **Depth:** deep (~18–24). **Split seam if needed:** cut into *GEOM-21a "Low-Rank Approximation"* and *GEOM-21b "The Pseudoinverse & Minimum-Norm Least Squares."*

---

## Movement VI — Calculus on Vectors: Gradients, the Hessian, and Numerical Reality

### GEOM-22 — Vectors of Numbers: Vector and Matrix Differentiation
1. **The one question:** What does it mean to differentiate a function with respect to a whole vector (or matrix) of variables, and how do we keep the bookkeeping straight?
2. **Scope / inside:**
   - From the Calc-1 derivative to the **partial derivative** (built inline from the floor — "vary one coordinate, hold the rest fixed") and the gradient as the vector of partials.
   - Layout conventions and the core identities derived from scratch: `∇(aᵀx) = a`, `∇(xᵀx) = 2x`, and the chain rule for `f(Ax)`; the Jacobian for vector-valued functions.
   - The data reading: a loss is a scalar function of a parameter *vector*, so its derivative is a gradient — this is the object every training loop chases.
3. **Assumes:** GEOM-4, GEOM-8; floor-level single-variable differentiation (restated inline). This article *builds* multivariable differentiation from the floor — the one place the track lifts calculus above Calc-1, done explicitly.
4. **Sets up:** GEOM-23 (gradient geometry), GEOM-24 (Hessian), GEOM-25 (quadratic form); **supplies Inference B2** (multivariable critical point) and the gradient Optimization consumes.
5. **Depth:** medium–deep (~16–22).

### GEOM-23 — The Gradient as a Direction in Space
1. **The one question:** Why does the gradient point in the direction of steepest ascent, and why is it perpendicular to the level sets?
2. **Scope / inside:**
   - The **directional derivative** `∇f·u` derived; maximized when `u` aligns with `∇f` (Cauchy–Schwarz from GEOM-4) ⇒ steepest-ascent meaning, drawn on a contour plot.
   - Gradient ⟂ level set, proved; the **first-order optimality** condition `∇f = 0` and what it does/doesn't guarantee (critical point, not necessarily a min — sets up the Hessian).
   - Gradient descent previewed *only* as motivation (it belongs to **Optimization**); here we own the geometry, not the algorithm.
3. **Assumes:** GEOM-4, GEOM-22.
4. **Sets up:** GEOM-24 (which kind of critical point?), GEOM-25; **the geometric foundation Optimization builds gradient descent on**.
5. **Depth:** medium (~12–18).

### GEOM-24 — The Hessian and the Curvature of a Surface
1. **The one question:** How does the matrix of second derivatives tell us the *shape* of a surface near a critical point — bowl, dome, or saddle?
2. **Scope / inside:**
   - The **Hessian** `H = ∇²f` defined; symmetry via equality of mixed partials (Clairaut, stated); the **second-order Taylor expansion** of a multivariable function derived, with `½ Δxᵀ H Δx` as the curvature term — a quadratic form (callback to GEOM-17).
   - The **second-derivative test** via the Hessian's definiteness (GEOM-18): PD ⇒ local min, ND ⇒ local max, indefinite ⇒ saddle — drawn.
   - Data meaning: curvature of a loss surface (conditioning of optimization), and the Hessian-as-Fisher-information connection flagged for Inference.
3. **Assumes:** GEOM-17, GEOM-18, GEOM-22, GEOM-23.
4. **Sets up:** GEOM-25 (Hessian of a quadratic form is constant), GEOM-26 (Hessian conditioning); **supplies Inference B3–B4** (Hessian/Fisher info) and **Optimization** (Newton's method, convexity).
5. **Depth:** medium–deep (~16–22).

### GEOM-25 — The Gradient and Hessian of a Quadratic Form
1. **The one question:** For the single most important function in applied math — `f(x) = ½xᵀAx − bᵀx` — what are its gradient and Hessian, and where is its minimum?
2. **Scope / inside:**
   - Full derivation of `∇f = Ax − b` (symmetric `A`) and `∇f = ½(A+Aᵀ)x − b` (general) — every step, both via component expansion and via the GEOM-22 identities; `∇²f = A`, constant.
   - Setting `∇f = 0` ⇒ `Ax = b`: minimizing a quadratic form *is* solving a linear system, and it has a unique minimum iff `A` is PD (tying GEOM-11, GEOM-18, GEOM-24 together in one result).
   - The payoff worked explicitly: this **is** the least-squares normal-equations derivation `∇‖y−Xβ‖² = 2(XᵀXβ − Xᵀy) = 0` — so Regression R5's "gradient of a quadratic form" prerequisite is discharged here in full.
3. **Assumes:** GEOM-17, GEOM-22, GEOM-24; GEOM-11/GEOM-18 for the solve-and-uniqueness reading.
4. **Sets up:** **discharges Regression R5's vector-differentiation prerequisite and Inference B3–B4's quadratic-form/Hessian need**; the canonical quadratic Optimization optimizes.
5. **Depth:** medium–deep (~16–22).

### GEOM-26 — Condition Number and Numerical Stability
1. **The one question:** Why do some perfectly invertible problems give garbage answers on a computer, and what number predicts it?
2. **Scope / inside:**
   - **Condition number** `κ(A) = σ_max/σ_min` (from the SVD, GEOM-20) = `λ_max/λ_min` for symmetric PD; derived as the worst-case amplification of relative error in solving `Ax=b`.
   - The geometric reading: a stretched-out ellipse (near-collinear columns) ⇒ huge `κ` ⇒ tiny data wiggles swing the solution wildly — this *is* multicollinearity (Regression R7) and the reason ridge (`XᵀX+λI`) and QR/SVD solves help.
   - Floating-point reality: why "solve, don't invert," why `det` is a bad singularity test, why normal equations square the condition number (so QR/SVD beat them) — the honest numerical edge cases.
3. **Assumes:** GEOM-14, GEOM-18, GEOM-20.
4. **Sets up:** GEOM-27; **discharges Regression R7** (eigenvalues/condition number) and informs Optimization (ill-conditioned loss surfaces).
5. **Depth:** medium–deep (~16–22).

### GEOM-27 — How These Tools Power Data Science (the bridge)
1. **The one question:** Now that the toolbox is built, where does each piece reappear across the rest of the series, and how do I choose the right tool for a problem I haven't seen?
2. **Scope / inside:**
   - A map from tool → consumer: projection → least squares; spectral theorem/SVD → PCA & covariance; PD/Cholesky → Gaussians & whitening; gradient/Hessian → optimization & Fisher information; condition number → multicollinearity & numerical care.
   - Two or three integrative worked examples that chain several tools end-to-end on a real dataset (e.g. center → covariance → spectral/SVD → project → reconstruct), with the honest "when does the geometric assumption break" discussion.
   - Interview-lens roundup: the standard linear-algebra interview questions across all the above, each answered, with applicability judgment.
3. **Assumes:** the whole track (GEOM-0–GEOM-26).
4. **Sets up:** terminal node — the explicit hand-off into Regression, Inference, Optimization, Classification, Unsupervised Learning, and Causal Inference.
5. **Depth:** medium (~12–18).

---

## Cross-track prerequisites (belong to OTHER tracks)

This is a **foundational track and consumes very little**. It builds essentially everything from the Calc-1 floor. The only outside touch-points are conceptual hooks, not hard dependencies:

**From Probability foundations** *(soft hooks only — used as motivating examples, not derivations)*
- *Variance / covariance and the covariance matrix as a concept* — referenced as a motivating example in **GEOM-16, GEOM-17, GEOM-18, GEOM-19** (the matrices we diagonalize are often covariance matrices). The geometry stands alone; the probabilistic meaning is Probability's to own. **Not a hard prerequisite** — Geometry can be read first.
- *The Gaussian density / change-of-variables Jacobian* — a forward hook mentioned in **GEOM-13, GEOM-19**; owned by Probability, not required to follow this track.

Everything else (functions, limits, single-variable differentiation, basic trig, the Cartesian plane) is at or below the **Calc-1 floor** and is restated inline where used. Notably, **multivariable differentiation is NOT assumed** — it is built from the floor in **GEOM-22**.

---

## Overlaps & ownership

This track is the **supplier** of linear algebra to the series, so most "overlaps" are really *ownership claims*: Geometry of Data builds the general tool; the consuming track applies it and links back rather than re-deriving.

| Shared topic | **Owner** | Rationale / boundary |
|---|---|---|
| **Vectors, span, subspaces, inner products, orthogonality** | **Geometry of Data** (GEOM-0–GEOM-5) | Pure linear-algebra foundation; everyone consumes it. |
| **Orthogonal projection / projection matrix** | **Geometry of Data** (GEOM-6) | The general geometric operation. **Regression R4** applies it as "least squares = projection" and links back. |
| **Matrix mult / transpose / inverse / rank** | **Geometry of Data** (GEOM-8–GEOM-12) | Discharges **Regression R5**'s matrix-algebra prerequisite. |
| **Eigenvalues / eigenvectors / condition number** | **Geometry of Data** (GEOM-14, GEOM-26) | Discharges **Regression R7**. |
| **Positive-definite matrices, Cholesky / matrix square root** | **Geometry of Data** (GEOM-18–GEOM-19) | Discharges **Regression R11** (GLS/whitening). |
| **SVD & eigendecomposition** | **Geometry of Data** (GEOM-15, GEOM-20) | Discharges **Regression R14** (ridge in the SVD basis). Shared with **Unsupervised Learning** — see PCA below. |
| **Gradient, Hessian, vector/matrix differentiation, quadratic forms** | **Geometry of Data** (GEOM-22–GEOM-25) | Discharges **Inference B2 (critical-point condition)** and **B3–B4 (quadratic-form / Hessian)**. Shared with **Optimization** — see below. |
| **PCA (the statistical method)** | **Unsupervised Learning owns it; Geometry supplies the SVD/spectral machinery** | Geometry GEOM-20–GEOM-21 own *SVD, low-rank approximation, the pseudoinverse, and the geometry of projection*. PCA *as a statistical procedure* — centering, covariance interpretation, variance maximization, choosing the number of components, scree plots, the probabilistic model — is **Unsupervised Learning's**. The seam: Geometry says "best rank-`k` approximation of a matrix"; UL says "directions of maximum variance in centered data." UL **links back** to GEOM-20/GEOM-21 rather than re-deriving the SVD. |
| **Gradient descent & second-order (Newton) methods** | **Optimization owns the algorithms; Geometry owns the geometry** | Geometry GEOM-23–GEOM-25 own *the gradient as steepest-ascent, the Hessian as curvature, the second-order Taylor model, and the gradient/Hessian of a quadratic form*. The **algorithms** (gradient descent, line search, Newton's method, momentum, convergence rates) are **Optimization's**, which consumes GEOM-22–GEOM-26 (including the condition-number story for convergence) and links back. Convexity *tests* (PD Hessian) are stated geometrically here; convexity *theory* belongs to Optimization. |
| **Fisher information matrix** | **Inference owns it; Geometry supplies the quadratic-form/Hessian view** | Geometry GEOM-24–GEOM-25 give the Hessian/quadratic-form machinery; **Inference B3–B4** build the statistical object on top. |
| **Covariance matrix** | **Probability/Inference own the statistics; Geometry uses it as an example** | Geometry treats covariance matrices only as instances of symmetric-PSD matrices (GEOM-16–GEOM-19); their probabilistic meaning is owned elsewhere. |
| **Numerical linear algebra (stability, conditioning)** | **Geometry of Data** (GEOM-26), at an applied level | We own the *condition number and the "solve don't invert" judgment*; a dedicated future Numerical Methods track (if created) could go deeper into algorithms. |

**One-line ownership rule:** *Geometry of Data owns every linear-algebra object as a piece of geometry; any statistical or algorithmic method built on top (PCA, gradient descent, Fisher information) is owned by its home track, which links back here rather than re-deriving the algebra.*

---

### Design notes / opinionated calls
- **Projection (GEOM-6) is the keystone, placed as early as the angle/orthogonality machinery allows.** It is the single operation the rest of the series leans on hardest (least squares, PCA reconstruction, the pseudoinverse), so it earns deep treatment up front and is paid off repeatedly (GEOM-7, GEOM-12, GEOM-20–GEOM-21, GEOM-25).
- **The SVD (GEOM-20) is built from the spectral theorem, not parachuted in.** Ordering GEOM-16 (spectral) → GEOM-17–GEOM-18 (quadratic forms / PD) → GEOM-20 (SVD) means the SVD's existence is *derived*, and the "every matrix is rotate-scale-rotate" picture lands as a theorem, not a slogan.
- **Vector calculus (GEOM-22–GEOM-25) comes last on purpose.** It needs matrices, quadratic forms, and definiteness already in hand, and placing it after the SVD lets GEOM-26 (conditioning) tie the optimization geometry back to the eigen/singular-value story in one stroke.
- **GEOM-25 is deliberately the convergence point of the whole track:** it fuses projection (GEOM-6), the inverse (GEOM-11), positive-definiteness (GEOM-18), and the Hessian (GEOM-24) into the one result — minimizing `½xᵀAx − bᵀx` is solving `Ax=b` — that simultaneously discharges Regression's and Inference's heaviest cross-track requests.

This roadmap is **28 articles** (GEOM-0–GEOM-27), a single foundational build with a few read-as-a-pair forks. Several deep articles (GEOM-6, GEOM-14, GEOM-20, GEOM-21) carry pre-marked split seams should they push the 30-page ceiling during drafting.
