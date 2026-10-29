# Direct tree algorithms: useful additive and parameter bounds

This note records positive direct-tree bounds obtained while seeking an
approximation below `m^(1/3)`. None gives that exponent improvement on every
general-precedence instance. They do beat the separator LP gap on the
finite-field family and identify sufficient conditions for an improvement.

Write `K=OPT_W`, `L=OPT_A`, and `a=L/n`, where the average objective is the
unnormalized sum used in the manuscript. All logarithms below can be
replaced by `log(2n)` to include singleton instances harmlessly.

## Buy the nonmaximal tests first

Let

```
A = {t : t has a strict successor},    r=|A|.
```

The set `A` is a precedence-closed ideal: a predecessor of a nonmaximal
test is itself nonmaximal. Execute its tests in a topological order. The
remaining tests are precisely the maximal elements of the original poset,
so they have no mutual precedence constraints and all their predecessors
have already been executed.

On each resulting hypothesis class, run an ordinary unit-cost decision-tree
approximation with factor `C log(2n)`. Such an algorithm also follows from
the manuscript's separator construction and greedy antichain covering.
Restriction of an optimal original tree to a hypothesis class gives a
valid unconstrained comparator. Therefore

```
cost_W <= r + C log(2n) K,
cost_A <= n r + C log(2n) L.
```

For the average bound, the classes after the initial ideal are disjoint,
and the sum of their optimal unconstrained total costs is at most `L`:
restrict the same original optimal tree to every class and sum its path
costs over their disjoint hypothesis sets. The first stage costs at most
`nr`. There is no assumption that the original optimum itself executes
all `r` tests, and no subtraction of `nr` from its cost is used.

Consequently the ratios are

```
O(log(2n) + r/K),
O(log(2n) + r/a).
```

The uniform-average ratio uses the global normalized optimum `a`; the
additive estimate itself remains valid even if that quantity is small.

For the colored finite-field construction, `r=q^2` and both `K` and `a`
are `Theta(q^2)`. Thus this direct method has an `O(log n)` guarantee on
the family exhibiting the `Omega(m^(1/3))` separator LP gap. In fact,
after the point tests are executed, one singleton test per color gives
a constant-factor solution on that particular family.

## Selectively buy tests with many successors

For any initial ideal `A`, let

```
d_A = max_(p notin A) |{t notin A : p <= t}|,
```

including `p` itself in its successor count. Set `d_A=0` when nothing
remains. For a remaining test `t`, assign the surrogate cost

```
c_A(t) = |{p notin A : p <= t}|.
```

Once `A` has been executed, a decision tree over the remaining tests can
be implemented by executing all missing predecessors immediately before
its requested test. Previously observed replies can be reused, and extra
replies can be ignored. The resulting feasible cost on each path is at
most that path's sum of surrogate costs.

Consider a path in any feasible original tree. Every predecessor of a test
on the path also lies on that path. Double-counting its residual
predecessor-test incidences gives

```
sum_(t on path, t notin A) c_A(t)
   <= d_A * (number of original tests on the path).
```

It follows that a logarithmic approximation for unconstrained weighted
decision trees, followed by this implementation, gives

```
cost_W <= |A| + C d_A log(2n) K,
cost_A <= n|A| + C d_A log(2n) L.
```

These weighted logarithmic approximations need not be assumed as a new
external theorem here. Replace each weighted test of integral cost
`c_A(t)` by a private chain of that many unit-cost tests, whose first
`c_A(t)-1` tests are uninformative. The chains form an inforest. Any
weighted tree has an equal-cost feasible chain tree. Apply the
manuscript's `O(log n)` inforest algorithm. When implementing its chain
tree in the actual instance, execute the real residual closure only when
the informative chain endpoint is reached. Uninformative intermediate
nodes can be skipped; charge the real closure to its chain's already
traversed nodes. Costs do not increase. The expansion has at most `m^2`
nodes and is polynomial.

For an explicit family of ideals, put

```
A_D = {p : |{t : p <= t}| > D},       1 <= D <= m.
```

Each `A_D` is an ideal, because every predecessor has at least as many
successors. After buying it, `d_(A_D) <= D`. Run the algorithm for every
`D` and return the cheapest tree for the requested objective. This gives
the valid tradeoffs

```
cost_W <= min_D {|A_D| + C D log(2n) K},
cost_A <= min_D {n|A_D| + C D log(2n) L}.
```

The choice `D=1` is exactly the nonmaximal-first algorithm. More generally,
this gives a ratio below `m^(1/3)` whenever an ideal with inexpensive
up-front cost leaves sufficiently little repeated prerequisite use. For
example, for fixed `epsilon>0`, it suffices in the worst case that some
`D` satisfy

```
D log(2n) = O(m^(1/3-epsilon)),
|A_D|/K   = O(m^(1/3-epsilon)).
```

For the average objective, replace `K` in the second condition by `a`.
The proof does not establish these conditions for arbitrary posets.

## A valid small-optimum bound and the unresolved middle regime

The same surrogate-cost method with `A=empty` yields a useful bound
without any degree promise. Along an optimal worst-case path of length at
most `K`, each closure has size at most `K`, and hence its surrogate cost
sum is at most `K^2`. The private-chain construction therefore gives

```
cost_W <= C K^2 log(2n).
```

The algorithm does not need to know `K`: build the chains using the actual
closure sizes and apply the inforest algorithm. The original optimal tree
is the comparator used only in the analysis. Also compute the tree that
executes every test in topological order, of cost at most `m`, and return
the cheapest candidate. Together with the nonmaximal-first algorithm,

```
cost_W / K
  <= min {m/K, C K log(2n), r/K + C log(2n),
          min_D (|A_D|/K + C D log(2n))}.
```

Thus, for a desired factor `B`, the simple algorithms already succeed
when `K <= B/(C log(2n))` or `K >= m/B`, as well as on the selective
unlocking regimes above. For `B=m^(1/3-epsilon)`, the still-unresolved
worst-case range is approximately

```
m^(1/3-epsilon)/log(2n) < K < m^(2/3+epsilon),
```

after excluding instances with a favorable unlocking ideal. These
inequalities are a partial regime theorem, not an algorithm covering the
remaining interval.

For the average objective the analogous surrogate comparator is

```
sum_h cost(D*,h)^2,
```

not `n a^2`. An average-optimal tree may have rare deep paths, so replacing
the second moment by the square of the mean would reverse Jensen's
inequality. Consequently no small-`a` analogue of the small-`K` theorem is
claimed. The large-`a` bound `m/a` and the additive unlocking guarantees
are valid.

## The precise remaining issue

The methods above pay globally for a chosen prerequisite ideal or pay for
its repeated use through the surrogate costs. A general improvement needs
an algorithm that chooses useful prerequisites selectively and charges
their shared cost substantially better than these two extremes. In the
paired-hypothesis full-cover embedding, this is already the problem of
finding a cheap union of prerequisite closures, since there is only one
internal tree path. Adaptivity gives a useful additive shortcut when the
expensive structure is concentrated in a small ideal, but does not by
itself resolve that general shared-closure optimization.
