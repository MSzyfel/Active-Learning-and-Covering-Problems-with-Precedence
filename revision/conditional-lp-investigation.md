# Conditional pair constraints: a surviving cubic-root gap

This note investigates the quadratic-polynomial precedence instance in
`lp-gap-investigation.md`. Full conditioning eliminates its particular
budget `K = 2q-1` witness. Nevertheless, a modified witness at budget
`K = 3q-1` survives the rank-two linear conditioning described below, so
this strengthening alone still has an `Omega(m^(1/3))` constant-coverage
gap. This is a statement about a reduced **private-blue formulation**,
not a claim of feasibility for every possible lift of the original
assignment-variable LP. Adding positive-semidefiniteness is a materially
stronger operation and eliminates this family, as explained at the end.

No rounding theorem below exponent `1/3` is established here.

## Instance and reduced formulation

Let `q >= 5` be a prime power. There are `q^2` point-tests `(t,u)` over
`F_q`, and `q^3` graph-tests indexed by the polynomials of degree at most
two. A graph-test `G` requires its `q` graph points and covers one private
blue. Put `k = q-1`. All tests have unit cost.

An integral solution covering at least `k` private blues can be reduced to
exactly `k` graph-tests by deleting surplus graph-tests. Thus the following
binary formulation has the correct optimum. Write `v_p` for a point-test
and `g_G` for a graph-test, and let `u` range over all these variables:

```
0 <= u <= 1,
g_G <= v_p                         for p on G,
sum_p v_p + sum_G g_G <= K,
sum_G g_G = k,
sum_{G containing p} g_G <= k v_p   for every point p.
```

The final load inequality is redundant for integral solutions but is
included because it is the private-blue version of the original LP's
per-red total-load constraint. Per-red/per-blue constraints reduce to the
precedence implications in this instance.

Introduce symmetric pair variables `M_uv`, set `M_uu = u`, and impose the
usual pair bounds

```
max(0,u+v-1) <= M_uv <= min(u,v).
```

For **each displayed linear equality or inequality**, multiply by every
variable `w` and by `1-w`, then replace `wu` by `M_wu` and `w^2` by `w`.
This explicitly defines the rank-two linear relaxation considered here.
For example, it includes

```
M_wG <= M_wp                         for p on G,
g_G - M_wG <= v_p - M_wp             for p on G,
sum_u M_wu <= K w,
sum_G M_wG = k w,
sum_{G containing p} M_wG <= k M_wp,
sum_{G containing p}(g_G-M_wG) <= k(v_p-M_wp).
```

The complementary budget inequality is also imposed. Since the witness
below has equality in both the original budget and every conditioned
budget row, that inequality follows immediately for this witness.

This relaxation also implies the earlier within-closure pair constraint:
if points `p,r` lie on `G`, lifted precedence gives
`M_pG = g_G` and then `g_G = M_pG <= M_pr`.

## Why the previous budget is impossible under these constraints

Suppose a feasible solution has `K = 2q-1` and some `g_G > 0`. Condition on
`G`. The conditional graph mass is exactly `k g_G`, so the conditioned
budget permits at most

```
(K-k) g_G = q g_G
```

point mass. Each of the `q` predecessors of `G` has pair value
`M_Gp = g_G`, exhausting that allowance. Every outside point therefore
has `M_Gp = 0`. Every other graph `H` contains a point outside `G`, since
distinct quadratics agree at at most two field points. Lifted precedence
then gives `M_GH = 0`. But the exact-count row requires
`sum_H M_GH = k g_G`, whereas its left side is now only `g_G`.
This contradicts `k > 1`. Since `sum_G g_G = k`, some positive graph
variable must exist. Hence this strengthened relaxation is infeasible at
that budget.

## Replacement witness at budget `3q-1`

Set

```
N = q^3,       L = q^2,       k = q-1,       K = 3q-1,
alpha = (q-1)/q^3,
beta  = 2/q,
gamma = alpha (q-2)/(q^3-1),
delta = 1/q^3,
epsilon = (4-2/q)/(q^2-1).
```

Give every graph marginal `alpha` and every point marginal `beta`.
Set diagonals equal to their marginals, and set the other pairs to

```
M_GH = gamma                    for distinct graphs,
M_pG = alpha                    if p lies on G,
M_pG = delta                    otherwise,
M_pr = epsilon                  for distinct points.
```

The original budget is `L beta + N alpha = K`, and graph mass is
`N alpha = k`. Every point lies on exactly `q^2` graphs. Consequently,

```
sum_G M_pG = q^2 alpha + (q^3-q^2) delta = k beta,
sum_H M_GH = alpha + (q^3-1) gamma = k alpha.
```

Every conditioned exact-count equation holds. The point portion of a
point row is

```
beta + (q^2-1) epsilon = 4 = (K-k) beta.
```

The point portion of a graph row is

```
q alpha + (q^2-q) delta = 2q alpha = (K-k) alpha.
```

Thus every conditioned budget row is an equality as well.

The pair bounds hold: all distinct marginals sum to less than one for
`q >= 5`, while `gamma <= delta <= alpha <= epsilon <= beta`.

For a precedence implication `g_G <= v_p`, positive conditioning is
immediate from these inequalities, separating whether the conditioning
variable is `G`, another graph, `p`, or another point. The only potentially
nonzero point-conditioned complementary case is bounded by

```
alpha-delta = (q-2)/q^3 <= beta-epsilon = 2(q-2)/(q^2-1).
```

For conditioning by a different graph, it suffices that
`alpha-gamma <= beta-alpha`, which follows from `2 alpha <= beta`.
Conditioning by `G` or `p` is immediate. Hence every positive and negative
lift of precedence holds.

It remains to verify the total-load lifts. The unconditioned load through
a point is

```
ell = q^2 alpha = k/q.
```

Let `L_(w,p) = sum_{G containing p} M_wG`. There are only five cases:

| Conditioning variable `w` | `L_(w,p)` |
| --- | --- |
| The point `p` itself | `ell` |
| Another point with the same first coordinate | `q^2 delta = 1/q` |
| A point with a different first coordinate | `q alpha + (q^2-q) delta = 2(q-1)/q^2` |
| A graph containing `p` | `alpha + (q^2-1) gamma` |
| A graph not containing `p` | `q^2 gamma` |

In the different-coordinate case there are exactly `q` quadratics
through the two points; in the same-coordinate case there are none.
The positive load inequalities follow from

```
ell <= k beta,
max(1/q, 2(q-1)/q^2) <= k epsilon,
alpha + (q^2-1) gamma <= k alpha,
q^2 gamma <= k delta.
```

For the negative lifts, conditioning on `p` gives `0 <= 0`.
For another point, `epsilon <= 1/q`, so
`k(beta-epsilon) >= ell >= ell-L_(w,p)`.
For a graph, its mixed pair with `p` is at most `alpha <= 1/q`, giving
the identical bound. All load lifts therefore hold.

This verifies every constraint of the stated reduced relaxation.

## The remaining gap and the stronger PSD distinction

Any solution covering a fixed fraction `eta > 0` of the target uses at
least `t = ceil(eta k)` graph-tests. If `U` is their union of points,
the pairwise intersection bound and Cauchy--Schwarz give

```
|U| >= t q^2 / (q+2(t-1)) = Omega_eta(q^2).
```

Against the feasible fractional budget `3q-1`, the gap remains
`Omega_eta(q) = Omega_eta(m^(1/3))`, where `m=q^3+q^2`. Thus full linear
conditioning at this rank removes the first witness but does not by
itself improve the exponent.

Positive-semidefiniteness of the pair matrix changes the conclusion.
Suppose the same exact-count and precedence consistency constraints hold,
all pair entries are nonnegative, and the pair matrix is PSD. Represent
it by vectors `h_u` with `M_uv = <h_u,h_v>`. For each point put
`w_p = sum_{G containing p} h_G`. Incidence consistency implies

```
sum_p <h_p,w_p> = q sum_G g_G = qk.
```

Writing `B = sum_p v_p`, Cauchy--Schwarz and the intersection bound give

```
(qk)^2 <= B sum_p ||w_p||^2
         <= B [qk + 2 sum_{G != H} M_GH]
         = B [qk + 2k(k-1)].
```

Here the last equality uses all graph exact-count rows. Therefore

```
B >= k q^2 / (q+2(k-1)) = Omega(q^2).
```

So the displayed linear witness cannot be PSD, and indeed no PSD witness
with this exact-count consistency can retain budget `O(q)` on this
private-blue family. This is an obstruction-elimination lemma, not a
general rounding algorithm. A sub-cubic-root result would still require
a coverage-preserving rounding theorem for the stronger relaxation on
arbitrary precedence instances; no such theorem is proved here.
