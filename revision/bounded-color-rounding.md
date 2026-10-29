# A bounded-color reduction to Minimum k-Union

This note proves a restricted approximation theorem. It does **not** give a
sub-cube-root approximation for unrestricted partial red-blue set cover or
for unrestricted precedence-constrained decision trees. No novelty claim
is made.

The reduction uses the polynomial-time `O_epsilon(n^(1/4+epsilon))`
approximation for Minimum k-Union (MkU), where `n` is its number of sets,
from Chlamtac, Dinitz, and Makarychev, *Minimizing the Union: Tight
Approximations for Small Set Bipartite Vertex Expansion*, Theorem 1.6:
https://arxiv.org/html/1611.07866.

## Model and theorem

A witness `j` has a red neighborhood `R_j` and exactly one blue color
`c(j)`. Selecting witnesses costs the cardinality of the union of their
red neighborhoods and covers their distinct colors. Red neighborhoods
may be arbitrary sets, including entire precedence closures and each
witness's own unit-cost test. Let:

* `m` be the number of witnesses;
* `F` be the maximum number of witnesses of one color;
* `k >= 1` be the target, assumed feasible;
* `K=OPT(k)` be the minimum red cost of covering at least `k` colors.

Fix `0 < epsilon < 3/4` and put `a=1/4+epsilon < 1`. There is a
polynomial-time algorithm covering at least `ceil(k/2)` distinct colors
with red cost

```
O_epsilon( m^a F^(1-a) ) K.
```

More precisely, order the witnesses of each color arbitrarily. For
`h=1,...,F`, let layer `L_h` consist of the `h`-th witness of each color
that has at least `h` witnesses, and put `n_h=|L_h|`. The cost bound is

```
3 C_epsilon K sum_h n_h^a
  <= 3 C_epsilon K m^a F^(1-a),
```

where `C_epsilon n^a` is the MkU approximation guarantee. The layer
construction and the reduction are deterministic. Any randomness or
failure probability comes only from the chosen implementation of the
MkU approximation; see the probability discussion below.

In particular, if `F <= m^gamma`, the exponent is

```
a + gamma(1-a).
```

This is strictly below `1/3` when
`gamma < (1/3-a)/(1-a)`. For arbitrarily small fixed positive `epsilon`,
this threshold approaches `1/9` from below.

## Algorithm

Keep a set of credited covered colors, initially empty. Until it contains
at least `ceil(k/2)` colors:

1. Remove witnesses of credited colors from each layer. Do not reorder
   witnesses or move them between layers.
2. For every nonempty residual layer `L_h` and every integer
   `1 <= t <= min(k,|L_h|)`, run the MkU approximation on the red
   neighborhoods of that layer with target `t`.
3. Every such output has exactly `t` witnesses of distinct previously
   uncredited colors. Compute its actual red-union cost divided by `t`.
   Choose a candidate minimizing this ratio, select its witnesses, and
   credit its `t` colors.

The MkU routine may return more than `t` witnesses; if so, retain any `t`.
This cannot increase red cost. No knowledge or guess of `K` is needed.
Zero-cost candidates are allowed. If `K=0`, the same proof shows that
each iteration has a zero-cost candidate, under a multiplicative MkU
guarantee.

Each iteration credits at least one new color. There are at most
`ceil(k/2)` iterations and at most `F k` MkU calls per iteration, so the
reduction is polynomial in the explicit input size for fixed `epsilon`.
The layers contain at most `m` witness records in total.

## Proof of the progress guarantee

Fix an optimum solution of red cost `K`, fix exactly `k` of its covered
colors, and choose one optimum witness for each fixed color. Every subset
of these witnesses has red-union cost at most `K`.

At an unfinished iteration, the number `c` of credited colors satisfies
`c < ceil(k/2)`, hence `c < k/2`. At least

```
q >= k-c > k/2
```

of the fixed optimum colors remain uncredited. Partition their fixed
witnesses by their original layers. Write `q_h` for the number in layer
`h`, so `sum_h q_h=q`.

For each layer with `q_h>0`, the algorithm tries target `t=q_h`. Its
MkU optimum is at most `K`, since the `q_h` fixed optimum witnesses
are feasible in that layer. If `n'_h` is the current layer size, the
corresponding approximation candidate therefore has cost at most

```
C_epsilon (n'_h)^a K <= C_epsilon n_h^a K
```

and covers exactly `q_h` new colors. Let `S=sum_h n_h^a`, using initial
layer sizes. Weighted averaging gives

```
min_(h:q_h>0) n_h^a/q_h
  <= (sum_(h:q_h>0) n_h^a)/(sum_h q_h)
  <= S/q.
```

Thus the chosen candidate has actual cost per credited color at most

```
C_epsilon K S/q < 2 C_epsilon K S/k.
```

This uses the cost of its entire red union, so it remains valid if some
of those reds were already selected in earlier iterations.

## Total cost and the multiplicity bound

Immediately before the last iteration, fewer than `k/2` colors have been
credited. The last candidate credits at most `k` colors, by the target
restriction in Step 2. Therefore the total number `G` of credited colors
at termination satisfies `G < 3k/2`.

The union of all chosen red neighborhoods costs at most the sum of their
individual red-union costs. Summing the progress bound yields

```
total cost <= (2 C_epsilon K S/k) G <= 3 C_epsilon K S.
```

Since the layers partition all witnesses, `sum_h n_h=m`. Concavity of
`x^a`, equivalently Holder's inequality, gives

```
S=sum_h n_h^a <= F (m/F)^a = m^a F^(1-a).
```

This proves the theorem. Arbitrary ordering is sufficient. The
construction has
`n_h = |{b : frequency(b) >= h}|`, so these sizes depend only on the
color frequencies, not on the within-color ordering.

If an exact output cardinality is useful, retain any `ceil(k/2)` of the
credited colors and their selected witnesses. This only decreases red
cost. Thus the subroutine can return exactly `ceil(k/2)` credited colors.

## Probability and derandomization status

The reduction does not sample representatives. Enumerating all layers
replaces the initial randomized thinning idea and ensures that every
fixed optimum witness appears in exactly one of the tested layers.
Thus there is no probability of losing all useful optimum witnesses.

If the MkU oracle is deterministic with its stated guarantee, the whole
algorithm is deterministic. If its approximation guarantee holds with
constant probability on each input, amplify each call independently to
failure probability at most `eta/(F k^2)`, by retaining the cheapest valid
target-size output of repeated calls. There are at most `F k^2` calls.
Conditioning on previous outputs does not affect the per-input success
guarantee of a fresh amplified call. A union bound therefore gives the
stated approximation with probability at least `1-eta`.

This note does not supply a new derandomization of the underlying MkU
algorithm. It only establishes that the color-handling reduction adds
no intrinsic randomness.

## General sets: the incidence parameter is necessary in this argument

For a general red-blue set `j` with blue neighborhood `B_j`, create one
witness record `(j,b)` for each `b in B_j`. Its color is `b` and its red
neighborhood is the original `R_j`. Distinct records for the same original
set share the same reds, including its own-test red if present; they do
not receive distinct artificial own-test costs.

Let

```
M=sum_j |B_j|,
F=max_b |{j : b in B_j}|.
```

The transformation preserves the optimum cost for any target: an
original solution supplies one record per covered color, and a set of
records projects to original sets covering at least its record colors at
exactly the same red-union cost. The reduction above can credit only the
record colors even if the projected sets incidentally cover more blues.
This keeps the gain accounting in the proof unchanged.

Consequently the proved general-set bound is

```
O_epsilon( M^a F^(1-a) ) OPT(k),
```

for coverage at least `ceil(k/2)`. It is **not** legitimate to replace
`M` by the number `m` of original sets in this argument. If each original
set covers at most `d` blues, then `M <= md` is available.

Arbitrary red neighborhoods include the closure reduction for precedence
cover, so this theorem applies with the corresponding witness-incidence
parameters. The distinction between `M` and the number of tests must be
retained in any decision-tree application.

## Why this does not settle the high-multiplicity regime

The strong gap in `sdp-strong-gap.md` has `m=Theta(q^3)` witnesses and
`F=q^2=Theta(m^(2/3))`. The present bound is then approximately
`m^(3/4+epsilon/3)`, so it gives no improvement over CMV on that family.

Taking the better of this theorem and a valid CMV constant-coverage
algorithm improves restricted frequency ranges but leaves the worst-case
cube-root exponent unchanged. Color multiplicity can be high in every
optimum-covered color, so splitting colors at a frequency threshold does
not by itself show that the low-frequency part contains a constant
fraction of the optimum target.

Likewise, deleting or sampling witnesses to enforce a small frequency
must justify preservation of the unknown optimum's colors. If each of
`q` optimum colors has exactly one useful witness among `F` candidates,
retaining at most `f` uniformly chosen candidates preserves only `qf/F`
of those witnesses in expectation. Repeating enough restrictions to
restore a fixed fraction can consume the hoped-for exponent gain.

The theorem therefore identifies a proved restricted route and a precise
remaining requirement: a high-frequency progress routine with an
approximation factor below the cube root, or a structure-aware reduction
of color frequencies whose coverage and red-cost losses are both
controlled. Neither is established here.

## Conditional improvement from low multiplicity inside pivot neighborhoods

The layer theorem also gives the following conditional structural result.
The condition is checkable once a CMV decomposition has been constructed,
but no bound sufficient for an unrestricted improvement is proved here.
This subsection uses the singleton-blue witness model; for general sets,
the number of witnesses is again the incidence count `M` defined above.

Fix a feasible budget `K >= OPT(k)` and a parameter `T >= 1`. Filter out
witnesses whose original red neighborhoods have size more than `K`.
Use CMV's nested red-deletion and degree-bucketing decomposition, with a
total exclusion allowance `O(K(T+1))`. Let its nonzero buckets be
`J_i`, their projected red universes be `R_i`, and their degree scales
be `s_i`, for `i=1,...,L`, where `L=O(log(2K))`. The properties needed
below are:

```
s_i <= |R_j intersect R_i| <= 2s_i   for j in J_i,
s_i <= K,
|{j in J_i : r in R_j}| <= D_i = O(m s_i L/(KT))  for r in R_i.
```

All projected-away reds belong to one common excluded set of size
`O(K(T+1))`. The usual ceiling in the deletion count adds at most
`O(L)=O(K)` reds, which is absorbed in this cost. Save and select all
witnesses whose projected red degree becomes zero during the
decomposition; their reds lie in the common excluded set. These are
standard decomposition properties, not new claims about conditioning.
The relevant source is CMV, Section 3, Lemmas 3.1 and 3.2:
https://arxiv.org/html/2302.00213.

For every nonempty pivot neighborhood

```
J_(i,r) = {j in J_i : r in R_j},
```

let `F_(i,r)` be the maximum number of its witnesses of any one blue
color. Suppose that, for a number `mu`, all these neighborhoods satisfy

```
F_(i,r) <= mu s_i/K.                                      (A)
```

Equivalently, the least possible `mu` for this fixed decomposition is
`max_(i,r) K F_(i,r)/s_i`, taking the maximum only over nonempty pivot
neighborhoods. Deleting already credited colors preserves (A). In
particular, (A) is demanding at small degree scales: nonemptiness implies
`mu >= K/s_i >= 1`.

For any fixed `0 < epsilon < 1/4` and `a=1/4+epsilon`, condition (A)
implies a polynomial-time algorithm covering at least `ceil(k/2)`
colors with cost

```
O_epsilon( K [1+T+L (mL/T)^a mu^(1-a)] ).                  (B)
```

Here `K` is an integral feasible-solution benchmark. The result does not
follow merely from feasibility of an LP or SDP at budget `K`.

### Proof of (B)

Fix one optimum witness for each of `k` optimum-covered colors, with
total original red cost at most `K`. At any unfinished iteration, more
than `k/2` of these colors remain uncredited. Their witnesses cannot
belong to saved zero-degree families, since those families were already
selected. Partition the remaining fixed witnesses among the nonzero
buckets, and let `q_i` be their bucket counts. Thus
`sum_i q_i=q>k/2`.

In bucket `i`, count incidences from these `q_i` distinct-color witnesses
to their projected red neighborhoods. There are at least `q_i s_i`
incidences, all ending in at most `K` optimum reds. Some pivot `r` is
therefore incident to at least `q_i s_i/K` of the fixed witnesses.
They have distinct colors. Let `Q_i` be their actual integer count, so
`Q_i >= q_i s_i/K` and `Q_i <= k`.

The algorithm tries every pivot and every target `1 <= Q <= k` that
is feasible in its local color universe. On the correct pivot and target
`Q=Q_i`, the layer subroutine has a feasible red budget at most `K`,
using projected red neighborhoods. There are at most `D_i` witnesses,
and their maximum color multiplicity is at most `mu s_i/K`. Its output
can be trimmed to exactly `ceil(Q_i/2)` credited colors, at projected
red cost at most

```
O_epsilon( K D_i^a F_(i,r)^(1-a) )
  <= O_epsilon( K [m s_i L/(KT)]^a [mu s_i/K]^(1-a) )
  = O_epsilon( s_i (mL/T)^a mu^(1-a) ).
```

Because its credited gain is at least `q_i s_i/(2K)`, its cost per new
credited color is at most

```
O_epsilon( K (mL/T)^a mu^(1-a)/q_i ).
```

One bucket has `q_i >= q/L`. Trying all local candidates and choosing
the minimum observed projected-cost/gain ratio therefore gives ratio
at most

```
O_epsilon( K L (mL/T)^a mu^(1-a)/q )
  = O_epsilon( (K/k) L (mL/T)^a mu^(1-a) ).
```

Repeat until at least `ceil(k/2)` colors have been credited. Each local
call has target at most `k` and its output can be trimmed as above, so
each accepted batch credits at most `k` colors. Total credited gain,
including the last batch, is less than `3k/2`. Summing the density bound
gives total projected red cost

```
O_epsilon( K L (mL/T)^a mu^(1-a) ).
```

The red union of all selected witnesses is contained in the common
excluded set together with their respective projected neighborhoods.
Charge the excluded set only once. This adds `O(K(T+1))` and proves
(B). All candidate families, targets, layer constructions, and observed
red costs are explicit, so this is a polynomial reduction to MkU for
fixed `epsilon`. The subroutine's success probabilities can be amplified
over the polynomial number of calls as above.

### Balancing and the unresolved assumption

If condition (A) holds with an asserted bound `mu` at the choice

```
T = m^(a/(1+a)) L mu^((1-a)/(1+a)),
```

then (B) becomes

```
O_epsilon( K [1+m^(a/(1+a)) L mu^((1-a)/(1+a))] ).          (C)
```

The qualification "at the choice" is essential: `mu` is a property of
the decomposition and can depend on `T`. One cannot optimize (B) while
silently keeping `mu` fixed if its bound has only been proved for a
different decomposition. For very large `T`, selecting all retained
witnesses already costs at most `mK`; if all reds fit in the exclusion
allowance, their total cost is covered by that allowance instead.

For `a` approaching `1/4`, the leading factor in (C) approaches
`m^(1/5) mu^(3/5) L`. More precisely, if `mu <= m^eta`, its polynomial
exponent is

```
(a+eta(1-a))/(1+a).
```

This is below `1/3` when

```
eta < (1-2a)/(3(1-a)),
```

whose limiting threshold is `2/9`. A strict exponent margin absorbs the
factor `L=O(log(2K))` in the usual polynomial-size precedence setting.
No theorem here establishes this bound on `mu` for general instances.
In particular, a large global color frequency does not itself imply
that its witnesses spread across pivots enough to make (A) useful.

The final coverage guarantee is still `ceil(k/2)`, so its bicriteria
coverage-loss parameter is the constant `beta=2`. The factor of two in
each local call changes only the density constant; it is not multiplied
once per greedy iteration. Any subsequent decision-tree or min-sum
reduction must retain its own stated dependence on `beta`, but this
argument does not introduce a polynomially growing coverage loss.
Nor does it assert that (A) is inherited by recursive decision-tree
instances: that would require a separate proof for every relevant
residual instance, or checking a uniform bound over those instances.
