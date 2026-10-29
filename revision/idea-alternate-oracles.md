# Alternate oracle routes: exact reductions and their limits

Research note, 29 October 2026. This investigation does not establish an
unrestricted approximation with exponent below `1/3`. It identifies the
strongest applicable general submodular ingredients found in the search,
an original-test formulation that avoids incidence blowup, and a simple
frequency-sensitive partial-cover guarantee. The latter is stronger than
the layer reduction in its applicable fixed-fraction quota regime. No
novelty claim is made.

## 1. Keep the original tests for general submodular methods

For the `m` original tests, let `C_i` be the prerequisite closure of `i`
and `B_i` its blue neighborhood. Define, on subsets of `[m]`,

```
f(I) = |union_(i in I) C_i|,
g(I) = |union_(i in I) B_i|.
```

Both are normalized monotone coverage submodular functions. The original
problem is exactly

```
min { f(I) : g(I) >= k }.
```

This is Submodular Cost Submodular Cover (SCSC), already on a ground set
of size `m`. There is no need to create `sum_i |B_i|` witness records.
Arbitrary nonnegative red weights are allowed by the same argument.

The partition-rank formulation in `colored-union-transfer-investigation.md`
is also exact, but its advantage is the simple constraint; it does not
improve the known objective approximation. The original-test SCSC
formulation is preferable whenever the algorithm accepts a general
submodular benefit function.

Iyer and Bilmes, *Submodular Optimization with Submodular Cover and
Submodular Knapsack Constraints*, NIPS 2013, provide SCSC/SCSK approximation
methods. Their ellipsoidal method has a square-root dependence on ground
set size, with curvature and logarithmic refinements (Theorem 4.4 and
Corollary 4.5). It therefore preserves the right parameter `m` but does
not improve the cube-root guarantee. [Primary paper](https://papers.nips.cc/paper_files/paper/2013/file/a1d50185e7426cbb0acad1e6ca74b9aa-Paper.pdf).

The relevant curvature is that of **cost**. For a coverage cost,

```
1-kappa_f = min_i |C_i \ union_(j != i) C_j| / |C_i|.
```

An own-test red does not necessarily give a positive numerator: it can
also occur in a successor's prerequisite closure. Even when every own-test
red is private, the ratio can be `1/|C_i|`; no constant curvature bound
follows from unit test costs. Consequently the curvature guarantee has no
unrestricted exponent improvement.

## 2. A published density oracle applies, but gives square root

For a residual target `q`, let

```
g_q(I) = min(q, number of currently uncovered blues covered by I).
```

Truncating a monotone submodular function at a nonnegative constant
preserves monotone submodularity. Thus minimizing `f(I)/g_q(I)` over
positive-gain subsets is a ratio-of-submodular-functions problem on the
original `m` tests. Bai, Iyer, Wei, and Bilmes, ICML 2016, Theorem 3.5,
give an `O(sqrt(m) log m)` approximation for this ratio. Their SCSC-based
reduction explicitly accommodates constant bicriteria coverage.
[Primary paper](https://proceedings.mlr.press/v48/baib16.pdf).

If an integral solution of cost `K` covers `q` residual blues, the optimum
ratio is at most `K/q`. The published oracle therefore returns a nonempty
batch `I` satisfying

```
f(I) / g_q(I) <= O(sqrt(m) log m) K/q.
```

Apply the residual-density argument already proved in
`colored-union-transfer-investigation.md`: iterating until half the
original target is covered gives cost `O(sqrt(m) log m) K` with coverage
loss `beta=2`. The capped benefit is important; uncapped blue count does
not by itself give the same last-batch bound.

This supplies a fully valid interface for an alternate oracle, but its
exponent is `1/2`. A better algorithm specialized to the explicit
coverage functions `f,g_q` would be needed. Replacing the published ratio
bound by a hypothetical `rho(m)` bound would give exactly
`O(rho(m))` cost with constant coverage loss, without witness blowup.

## 3. Why a general matroid/submodular theorem cannot supply the exponent

Svitkina and Fleischer, *Submodular Approximation: Sampling-based
Algorithms and Lower Bounds*, Theorem 4.2, prove that polynomially many
value queries cannot achieve a bicriteria `(rho,sigma)` approximation to
monotone submodular minimization with a cardinality lower bound when

```
rho/sigma = o(sqrt(m/log m)).
```

Here the output must have at least `sigma` times the target cardinality
and cost at most `rho` times the promised budget. Theorem 4.3 gives the
corresponding square-root-order bicriteria algorithm.
[Primary full version](https://arxiv.org/pdf/0805.1071).

The cardinality benefit is already a special case of partition rank,
with one witness per color. Thus a theorem for arbitrary monotone
submodular cost and a partition-rank quota, using only a cost value oracle,
cannot give the requested sub-cube-root ratio with constant or
polylogarithmic coverage loss. For any fixed `epsilon>0` and fixed
polylogarithmic loss, `m^(1/3-epsilon)` times that loss is still
`o(sqrt(m/log m))`.

This is **not** a hardness result for explicitly listed coverage costs,
and in particular not for explicitly given precedence instances. The
ordinary Minimum k-Union algorithm already demonstrates that explicit
incidence information can outperform this oracle barrier. A useful
colored extension has to exploit that information too.

### Direct extension to a quarter-color quota

The cited cardinality lower bound permits arbitrary target size. That
alone does not prove a lower bound with target one quarter of the number
of colors. The following extension supplies that distinction. This is a
direct argument using their hidden-set construction, not a theorem
claimed verbatim from their paper.

Take `m` witnesses. For a proposed `(rho,sigma)` guarantee with
`rho>=1`, `0<sigma<=1`, put `r=rho/sigma` and use the integer parameters

```
alpha = 2 floor(m/(40r)),
beta  = ceil(5 alpha^2/m).
```

When `r=o(sqrt(m/log m))`, these satisfy
`alpha^2/m=omega(log m)` and, for sufficiently large `m`,
`1<=beta<alpha`. For a uniformly random `alpha`-element set `R`, use
the following normalized monotone submodular functions from the
hidden-set construction:

```
f_0(A) = min(|A|, alpha),
f_R(A) = min(beta + |A\R|, |A|, alpha).
```

For completeness, `f_R` is the truncation at `alpha` of
`|A\R|+min(|A intersect R|,beta)`, so it is monotone submodular.
For a fixed query, the disagreement probability is maximized at
`|A|=alpha`, where disagreement requires `|A intersect R|>beta`.
Its mean is `alpha^2/m`, and `beta` is at least five times that mean.
The Chernoff argument in their Lemma 4.1 therefore gives disagreement
probability `m^(-omega(1))`, also with these rounded parameters.

Fix a balanced partition of the witnesses into `2 alpha` nonempty
colors, independent of `R`, and set `k=alpha/2`. Thus the target is
exactly one quarter of the number of colors. Let `Z` count unordered
same-color pairs in `R`. If every part has size at most
`ceil(m/(2 alpha))`, the probability that two uniformly chosen distinct
witnesses have the same color is at most

```
(ceil(m/(2 alpha))-1)/(m-1) <= m/(2 alpha (m-1)).
```

It follows that

```
E[Z] <= (alpha-1)m/(4(m-1)) <= alpha/4.
```

If a color contributes `s` witnesses, its duplicate loss `s-1` is at
most `binom(s,2)`. Hence `rank(R)>=alpha-Z`. By Markov's inequality,
the event `H={rank(R)>=alpha/2}` has probability at least `1/2`.
Condition the distribution of `R` on `H`. Every fixed-query
disagreement probability increases by at most a factor of two, so the
same polynomial-query indistinguishability conclusion holds. The
partition and its rank oracle are fixed and reveal no hidden-set data.

On every conditioned `f_R` instance, `R` is feasible for quota `k` and
costs `beta`. On the `f_0` instance, any set covering at least `sigma k`
colors has at least `sigma alpha/2` elements and therefore costs at
least `sigma alpha/2`, for `0<sigma<=1`.

For the integer parameter choice above,

```
(rho beta)/(sigma alpha) = r beta/alpha
    <= 5r alpha/m + r/alpha
    <= 1/4 + o(1) < 1/2.
```

Its successful output on `f_R` would have both cost at most `rho beta`
and the required color count; no output can meet these two conditions
on `f_0`. Include one final query of the returned objective value.
Testing these two conditions then distinguishes the distributions with
the algorithm's constant success probability, a contradiction. Since
`alpha<=m/20`, the balanced nonempty partition exists.

Thus the same oracle barrier persists with a quarter-color quota.
The hard objectives above are general submodular functions; the argument
still does not supply explicitly listed closure-union instances. In
particular, it does not preserve the condition `f(A)>=|A|` forced by
distinct witnesses' own unit-cost tests. It limits an unrestricted
submodular black box, and does not rule out an algorithm exploiting
own-test structure or explicit red neighborhoods.

A recent primary source does not remove this obstacle: Chen, Chen, Ye,
and Zhang, *Approximation algorithms for two extensions of min-k-union*,
JCSS 157, May 2026, gives a `2 sqrt(n)` approximation for monotone
submodular minimization with a cardinality constraint. Its other extension
is maximum coverage interdiction, where a leader deletes sets before a
follower maximizes coverage. Neither result imposes distinct-color
selection. [Publisher article](https://www.sciencedirect.com/science/article/pii/S0022000025001321).

## 4. A stronger low-frequency result for fixed-fraction quotas

Let `n=|B|`, let `F_b` be the number of original tests covering blue `b`,
let `F=max_b F_b`, and let `M=sum_b F_b`. Assume the target `k>=1` is
feasible. The following deterministic bound uses only a polynomial-size
LP and applies to arbitrary blue neighborhoods and arbitrary red unions:

```
coverage >= ceil(k/2),
cost <= (2M/k) OPT(k) <= (2nF/k) OPT(k).
```

In particular, when `k>=n/4`, the ratio is at most `8F`, with `beta=2`.
It is below `m^(1/3)` whenever `F=O(m^(1/3-epsilon))`; more generally
`M/k=O(m^(1/3-epsilon))` suffices. This avoids the `M^(1/4+epsilon)`
cost term of the witness-layer reduction. It is a restricted guarantee,
not a high-frequency solution.

### LP and threshold proof

Use variables `x_r` for reds, `y_i` for original tests, and `z_b` for
blues. Solve

```
minimize sum_r x_r
subject to
    y_i <= x_r                  for every r in C_i,
    z_b <= sum_(i: b in B_i) y_i for every b,
    sum_b z_b >= k,
    0 <= x_r,y_i,z_b <= 1.
```

An integral optimum of cost `OPT(k)` is feasible, so the LP value `L` is
at most `OPT(k)`. Put `t=k/(2M)` and select all tests with `y_i>=t`.
The selected red union consists only of reds with `x_r>=t`, hence has
cost at most `L/t`.

Let `U` be the blues left uncovered. Every witness test of `b in U` has
`y_i<t`, so `z_b<=F_b t`. Consequently

```
sum_(b in U) z_b <= t sum_(b in U) F_b <= tM = k/2.
```

The covered blues therefore carry at least `k/2` units of `z` mass.
Since each `z_b<=1`, there are at least `ceil(k/2)` of them. Finally,
`L/t=(2M/k)L<=(2M/k)OPT(k)`, proving the claim. Because feasibility
implies `M>=k`, the threshold lies in `(0,1]`. Zero-cost optima also
cause no difficulty: all selected reds have positive threshold and their
total weighted cost is zero when `L=0`.

The weighted-red version follows by replacing `sum x_r` by
`sum w_r x_r`; threshold charging is identical. Weighted blue profits
can also be included, replacing cardinality and `M` by the corresponding
profit-weighted sums.

This is consistent with the established frequency-based submodular
cover literature. Iwata and Nagano, Theorem 8, give an `F` approximation
for full submodular-cost set cover. Shi, Zhang, and Du give
`O(F/epsilon)` bicriteria partial-cover guarantees with additive
`epsilon` loss in the fraction of all profits covered. The proof above
specializes to an explicit coverage cost and makes the quota dependence
and average-frequency improvement transparent.
[Iwata--Nagano primary paper](https://www.kurims.kyoto-u.ac.jp/preprint/file/RIMS1668.pdf),
[Shi--Zhang--Du primary paper](https://arxiv.org/pdf/1701.05339).

### A computable frequency-profile improvement

For any threshold `t in (0,1]`, put

```
P(t) = sum_b min(1,F_b t).
```

The same argument shows that thresholding at `t` covers at least
`k-P(t)` blues and costs at most `L/t`. Choose the largest `t` with
`P(t)<=k/2`. This is a piecewise-linear computation using the known
frequencies. It is never worse than `t=k/(2M)`. It also exploits a small
number of exceptionally high-frequency blues without requiring a
uniform maximum-frequency bound. The condition is about the whole
input's frequency profile, and does not assert that the unknown optimum
avoids the high-frequency colors.

The actual LP values give a still more direct implementation: enumerate
the at most `m` positive thresholds `y_i`, retain every threshold output
covering at least `ceil(k/2)` blues, and return the cheapest. The proof
above certifies that one of these outputs satisfies the stated bound.

## 5. What remains unresolved

The most promising published exponent is still the
`m^(1/4+epsilon)` ordinary Minimum k-Union guarantee in
Chlamtac--Dinitz--Makarychev, Theorem 1.6. Its ground set is the family of
candidate sets; its quota is their count. It does not provide the colored
ratio oracle above. [Primary paper](https://arxiv.org/html/1611.07866).

The new-to-this-audit low-frequency observation improves a restricted
regime, especially the quarter-universe separator quota, but taking its
minimum with CMV's guarantee leaves the unrestricted `m^(1/3)` exponent
unchanged. An instance can have all relevant blues at frequency at least
`m^(1/3)` and `M/k` at least that large. Neither a partition-matroid
representation, generic submodular optimization, nor the recent
cardinality/interdiction extension supplies the missing high-frequency
routine.

An unconditional improvement therefore still requires a new result
specialized to explicit coverage incidence: either a sub-cube-root
colored density oracle, or a structural high-frequency procedure whose
cost and capped blue gain meet that oracle interface. No such general
result is proved in this note.
