# Third red moments: what they remove and what remains

This note studies an economical strengthening of the LP in
`global-lp-decision-tree-investigation.md`. It is a collection of proved
relaxation facts and an explicitly unproved rounding target, not a
subcube-root approximation theorem. In particular, the red-only lift below
is **not** the full Sherali--Adams lift of the covering formulation.

## A valid third-moment strengthening

For every subset `A` of red elements with `|A| <= 3`, introduce a
nonnegative variable `M_A`, with `M_empty = 1`, `M_{p} = y_p`, and
`M_{p,r} = Y_pr` for distinct reds. Diagonal pair variables remain
`Y_pp = y_p`. In addition to the original constraints, impose

```
sum_{r not in A} M_{A union {r}} <= (K-|A|) M_A     (|A| <= 2),
x_j <= M_A                                      (A subset R_j, |A| <= 3).
```

One may also impose moment monotonicity and all local inclusion-exclusion
inequalities on at most three red variables. All these constraints are
valid: for an integral solution with selected red set `D`, put
`M_A = 1[A subset D]`. If `A subset D`, the first left side is
`|D|-|A| <= K-|A|`; otherwise it is zero. A selected set has every red
neighbor in `D`, proving the second inequality. The formulation has
polynomial size. Budgets below three can be handled separately by
enumerating red subsets of size at most two.

Summing the cardinality inequalities by levels gives

```
sum_{|A|=t} M_A <= binom(K,t),                    t = 1,2,3.
```

Indeed each size-`t+1` subset appears `t+1` times in the sum of the
size-`t` extension constraints. The falling-factorial version avoids
diagonal or repeated-index conventions.

**Bounded-multiplicity lemma.** Let `E` be any family of red triples, let
`J` be any subfamily of the available sets, and let

```
d_j = |{A in E : A subset R_j}|,
lambda = max_{A in E} |{j in J : A subset R_j}|.
```

Every feasible strengthened solution satisfies

```
sum_{j in J} d_j x_j <= lambda binom(K,3).
```

For each triple `A`, at most `lambda` terms `x_j` are charged to it and
each is at most `M_A`; sum this inequality over `E`. The same proof
works for order `t` when moments through order `t` and their cardinality
constraints are available.

## The quadratic-graph gap is excluded

Use the finite-field precedence instance in `lp-gap-investigation.md`:
there are `q^2` point-tests and `q^3` graph-tests, one for each polynomial
of degree at most two over `F_q`. Each graph-test has its own private blue
and has the `q` points of its graph as predecessors. The target is
`k = q-1`.

Let `E` consist of point triples with three distinct first coordinates.
Each graph contains exactly `binom(q,3)` such triples. Each triple in
`E` is contained in exactly one quadratic graph, by interpolation, so
the multiplicity is one. Unique blues imply
`sum_f x_{G_f} >= sum_f z_{b_f} = q-1`. Therefore every feasible third
moment solution satisfies

```
binom(K,3) >= (q-1) binom(q,3),
K(K-1)(K-2) >= q(q-1)^2(q-2),
K >= (1-o(1)) q^(4/3).
```

This proof applies unchanged to the precedence closure instance: point
triples are just a subfamily of all red triples; the private graph reds
only add further moment terms. In particular, the pair-LP budget
`K = 2q-1` is impossible for every prime power `q >= 11`. After cancelling
`q-1`, the desired strict contradiction is
`q^3-11q^2+18q-6 > 0`, which holds for all integers `q >= 10`.

The argument is independent of the specific displayed pair marginals.
It excludes **every** feasible third-moment solution at budget `O(q)`
on the unaugmented unique-blue instance. Thus merely finding another
pair-LP optimum cannot evade it. If a cheap additional test is inserted
to cover many of the original private blues, as in the final section of
`lp-gap-investigation.md`, the equality forcing graph mass no longer
holds; the strengthened LP can use that additional test.

## A cubic-graph gap survives this red-only strengthening

The next construction shows that these additional constraints still
have an `Omega(m^(1/4))` gap for any fixed positive coverage fraction.
Take a prime power `q >= 5`. Replace quadratics by all degree-at-most-three
polynomials. There are `q^4` graph-tests, `q^2` point-tests, and
`m = q^4+q^2`. Keep one private blue per graph-test and its `q` graph
points as predecessors. Put

```
k = q-1,                 K = 2q+1,
h = (q-1)/q^4,
x_P = y_P = 1/q,
x_G = y_G = z_{b_G} = a_{b_G,G} = h.
```

All other assignments are zero. For distinct-red subsets of size at
most three, define

```
M_A = q^(-|A|)  if A contains only point reds;
M_A = h        if A contains exactly one graph red G and
                    every point red in A lies on G;
M_A = 0        otherwise.
```

Set `M_empty = 1` and use `Y_pp = y_p`. These values obey all the
constraints of the red-only strengthening:

* The first-moment total is `q+(q-1)=2q-1 <= K`. Each point lies on
  `q^3` cubics, so its assigned load is `q^3 h = (q-1)/q = k y_P`.
  All other original assignment and load constraints follow immediately.
* For a point `p`, its positive extension sum is
  `(q^2-1)/q^2 + q^3 h = 2-1/q-1/q^2 <= (K-1)/q`.
  For a graph `G`, this sum is `q h <= (K-1)h`.
* For a pair of points with different first coordinates, at most `q^2`
  cubics contain both. Consequently its positive extension sum is at most
  `(q^2-2)/q^3 + q^2 h = 2/q-1/q^2-2/q^3`, which is at most
  `(K-2)/q^2 = 2/q-1/q^2`. For equal first coordinates the graph term
  is zero.
* An incident graph-point pair has extension sum `(q-1)h`, at most
  `(K-2)h`. A nonincident graph-point pair or a distinct graph pair
  has both moment and extension sum zero.
* Every size-at-most-three all-point subset of a graph has moment at
  least `q^(-3) >= h`; every subset also containing its own graph red
  has moment `h`. Hence `x_j <= M_A` holds for every required subset.

Monotonicity also holds. The moments admit valid distributions on every
set of at most three red variables, so adding local inclusion-exclusion
constraints does not remove this example. To see this, all-point local
distributions are independent Bernoulli variables with mean `1/q`.
With one graph variable and at most two point variables, carve probability
`h` from the point-pattern matching graph incidence; every such pattern
has probability at least `q^(-2) >= h`. With two graph variables and one
point, use two disjoint graph events of probability `h`, setting the
point according to incidence; both point atoms have enough mass since
`2h <= 1/q`. Three graph events can be mutually exclusive since
`3h <= 1`. These constructions have the specified moments.

Two distinct cubics agree at at most three field points. Thus a family
of `t` graph-tests reaches at least

```
|U| >= t q^2 / (q + 3(t-1))
```

point-tests, by counting incidences and applying Cauchy--Schwarz. Covering
`ceil(delta k)` private blues, for any fixed `delta > 0`, therefore costs
`Omega_delta(q^2)` reds. Relative to `K = 2q+1`, the gap is
`Omega_delta(q) = Omega_delta(m^(1/4))`.

This is not a full Sherali--Adams example. In particular, all distinct
graph-pair moments above are zero, whereas conditioning the coverage
equality on a graph would require

```
sum_H M_{G,H} = k M_G.
```

The left side in this assignment is only `M_G`. The full lifted covering
system, as well as a PSD requirement on the global moment matrix, may
exclude this assignment. The conclusion concerns exactly the red-only
strengthening defined above and its local red consistency constraints.

The construction extends to moments of any fixed order `d >= 2`: use all
degree-at-most-`d` graphs, take `h=(q-1)/q^(d+1)` and
`K=2q+d-2`, set all-point moments to `q^(-|A|)`, and use the same mixed
moment rule through order `d`. For an all-point `s`-subset, `s<d`, the
extension sum is at most
`[(2q-1)-s/q] q^(-s) <= (K-s)q^(-s)`. Other extension rows have the same
simple form as above. The intersection bound is now `d`, yielding an
`Omega(m^(1/(d+1)))` gap for this positive red-moment system. No local
distribution or full Sherali--Adams assertion is needed for this
general-order statement.

## Exact missing step toward an exponent below one third

The current rounding pays, up to constants,

```
KT + K^2/theta + theta m/T.
```

Optimizing gives `K[T+sqrt(m/T)]` and exponent `1/3`. Adding third
moments without changing the rounding leaves this calculation unchanged.
A concrete sufficient new lemma would give, after buying the reds with
`y_p >= 1/T`, constant-fraction residual coverage at expected additional
red cost

```
O(K [1 + sqrt(m)/T]).
```

Together with the initial `KT` cost and a simultaneous coverage/cost
argument, taking `T=m^(1/4)` would give a constant-loss
`O(m^(1/4))` approximation. An alternative sufficient estimate would
replace the last term of the current heavy/light analysis by
`theta m/T^2` while retaining the `K^2/theta` term. These are proposed
rounding targets, not established consequences of third moments.

The missing extra factor of `1/T` cannot be inserted merely by claiming
that small first marginals imply small pair marginals. Even actual
distributions over feasible integral solutions can have
`M_{p,r}=y_p=y_r`: choose one of many disjoint red clusters uniformly,
each cluster supporting the full blue target. Third moments do not turn
such positive correlation into a product bound. A successful proof must
exploit these correlated clusters algorithmically while controlling
overlapping blue coverage, or obtain a different global cost argument.
Conditioning on more red pivots alone does not supply that missing
argument: tuple activation introduces higher moment budget totals, and
the first-marginal threshold still only implies `M_A <= 1/T`, not
`T^(-|A|)`.

Thus the quadratic obstruction gives a concrete reason to pursue third
moments, and the cubic obstruction is consistent with a quarter-power
target. Neither supplies the new rounding lemma, a proof of any exponent
below `1/3`, or a universal integrality-gap upper bound.
