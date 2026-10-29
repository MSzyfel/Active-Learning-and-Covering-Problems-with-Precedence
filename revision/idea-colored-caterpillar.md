# Colored caterpillars: safe stopping rules and the remaining occupancy loss

This investigation does not establish an exponent below one third for
general precedence-constrained decision trees. It gives two polynomial
substitutes for a colored density oracle, proves exactly where their
loss enters a caterpillar argument, and shows that a common-pivot
candidate pool need not remove the color-choice difficulty. These are
research lemmas, not a claimed new general approximation theorem.

The candidate-pool results below count **witnesses**. For general sets
covering several blues, the witness count is the number of incidences,
unless a separate argument works directly with original sets. This
distinction prevents an unjustified transfer to the number of tests.

## Model and the point at which colors matter

Let `U` be a pool of `N` witnesses. A witness `u` has red neighborhood
`R_u` and one blue color `b(u)`. Write `c(S)` for the number of colors
represented by `S`, and `R(S)` for its red union. Assume an unknown
colorful collection `O` has `q` witnesses and `|R(O)| <= K`.

The desired local objective is `|R(S)|/c(S)`. In the CDM framework,
ordinary least expansion is used both to return a cheap set and to infer
expansion of the unknown optimum when that return does not happen.
Merely rejecting outputs with too few distinct colors does not justify
the latter inference. Both implications must be replaced.

Reference: Chlamtac, Dinitz, and Makarychev,
[Minimizing the Union](https://arxiv.org/html/1611.07866), Lemma 2.1,
Lemmas 3.7--3.9. The lemmas and constructions below are derived here.

## 1. A safe flow oracle using local color frequencies

Let `f_b` be the number of witnesses of color `b` in the current pool.
Give every witness `u` weight `w_u=1/f_(b(u))`. For every collection,

```
w(S) = sum_(u in S) w_u <= c(S).
```

Ordinary weighted least expansion can be solved in polynomial time:
minimize `|R(S)|/w(S)` over nonempty `S`. For a rational trial value
`lambda`, the usual closure cut minimizes `|R(S)|-lambda w(S)`;
nonnegative rational weights are sufficient. Exact rational optimization,
or a constant-factor binary search, gives the stated bound exactly or
with an immaterial constant respectively.

If `S` is an exact optimum of this weighted problem, then

```
|R(S)|/c(S) <= |R(S)|/w(S)
             <= K / H(O),

H(O) = sum_(u in O) 1/f_(b(u)).                         (1)
```

Since `O` has distinct colors, Cauchy--Schwarz gives

```
H(O) >= q^2 / sum_(b represented in O) f_b >= q^2/N.
```

Thus a genuinely color-safe, polynomial-time output has

```
|R(S)|/c(S) <= K N/q^2.                                (2)
```

This improves a maximum-frequency bound whenever the surviving optimum
colors have favorable *local* frequencies. Frequencies must be
recomputed after restricting a pool. A large frequency outside the pool
is irrelevant to (1).

If all witnesses have at most `r` reds, the best single witness also
gives the valid combined bound

```
|R(S)|/c(S) <= min(r, K N/q^2).
```

The cost and the number of represented colors are observable, so the
algorithm can keep the best actual density among the weighted-flow
output and all singleton candidates. It does not need to know `O` or
`H(O)`.

### Target caps require separate care

On a fixed pool containing a colorful `k`-witness optimum of cost `K`,
repeat the weighted-flow call after removing witnesses of credited
colors. Before covering `ceil(k/2)` colors, more than `k/2` optimum
colors survive, so each call has density at most `4KN/k^2`. If a call
represents more than `k` colors, credit exactly `k` and retain one
witness per credited color. Its original color count is at most `N`,
so blindly truncating would not preserve the claimed density.

If the pool has at most `k` colors, total credited gain is below `3k/2`,
and repeated progress costs at most `6KN/k`. Without that restriction,
an uncapped density bound alone does not prove the same quota theorem:
the cost of an oversized final output requires an additional argument.

For the local pivot comparison below, only the density statement (2)
is needed; any global progress routine still needs valid gain caps or
an explicit bound on its last batch.

## 2. A stopping rule that either covers colors or certifies expansion

The following replacement handles both uses of the ordinary flow oracle.
Fix a positive threshold `tau` and an integer `q` for which the pool
contains a colorful `q`-witness collection `O`.

Start with the whole pool and no recorded colors. Repeatedly find an
ordinary least-expanding nonempty collection `S` in the remaining pool.
If its density exceeds `tau`, stop. Otherwise record `S` and remove
**all witnesses of every color represented by `S`** from the pool.
Stop as soon as at least `ceil(q/2)` colors have been recorded.

This procedure has one of two rigorously certified outcomes:

1. **Coverage outcome.** The recorded collections cover at least
   `ceil(q/2)` distinct colors, and their combined red union costs at
   most `tau N`.
2. **Expansion outcome.** Fewer than `q/2` colors were recorded. More
   than `q/2` witnesses of `O` remain, and every nonempty subset of the
   remaining pool has ordinary expansion strictly greater than `tau`.

For the first outcome, different recorded collections have disjoint
colors and hence disjoint witnesses. Therefore

```
sum_recorded |R(S)| <= tau sum_recorded |S| <= tau N.
```

For the second, removing a color removes at most one witness of `O`.
The final ordinary flow optimum certifies the expansion assertion for
all remaining subsets. The integer stopping rule is consistent: fewer
than `ceil(q/2)` recorded colors means strictly fewer than `q/2`.

No selected reds need be purchased until the outcome is known. In the
expansion outcome the removed colors can simply be discarded from the
local comparison. In the coverage outcome one can retain any
`ceil(q/2)` covered colors and one witness for each, decreasing cost.

To guarantee a successful output of colored density at most `lambda`,
choose

```
tau = lambda q/(2N).
```

Then the coverage outcome has density at most `lambda`, but the
expansion outcome certifies only

```
ordinary expansion > lambda q/(2N).                   (3)
```

This is the precise price of preserving distinct-color progress by
this stopping rule. It loses the optimum-occupancy factor `q/N` in the
expansion certificate. It is invalid to keep the original CDM backbone
growth bound after making this replacement.

### The conversion loss can really be large

Take `q` colors and `F` witnesses per color. Every witness of color `b`
has the same private-to-that-color red core of size `r`, together with
its own separate red. Cores of different colors are disjoint. The
witness neighborhoods have equal size `r+1`, are distinct, and are
pairwise incomparable within a color.

A full color class has ordinary density `1+r/F`; every nonempty
collection has ordinary density at least this value. The best colored
density is `r+1`, attained by choosing one witness per selected color.
Their ratio tends to `F=N/q` as `r/F` tends to infinity. Thus even
uniform degrees, own-test costs, and elimination of duplicate or
dominated witnesses do not control the ordinary-to-colored conversion.

This is a bound on that conversion, not approximation hardness: the
colored optimum in this particular example is easy to find.

## 3. Why these replacements do not complete the caterpillar induction

For orientation, consider the balanced first-pivot parameters from
`colored-union-investigation.md`. Write `s` for the original target,
with `n=s^2` witnesses, uniform red degree `r`, and optimum average
back-degree `d=s^(1/2+epsilon)`. A promised first candidate pool has

```
N <= s^(1+c epsilon),
q >= (1/4) s^(1/2+(1-c)epsilon),
K = r s^(1/2-epsilon).
```

Substitution into (2) gives only

```
colored density <= 16 r s^(1/2-(3-3c)epsilon).
```

For sufficiently small positive `epsilon` this is worse than the
singleton density `r`; it does not yield the needed polynomial
improvement below `r`. The color-peeling certificate (3) has the same
occupancy obstruction.

There is an additional issue in a backbone step. The proof needs many
*good* red neighbors of the unknown surviving optimum. Its pruning
bound subtracts a term proportional to `q` for bad neighbors. Replacing
an expansion lower bound proportional to `q` by one proportional to
`q^2/N` can make that subtraction consume the whole bound. One cannot
repair this merely by running more backbone steps; a new pruning or
color-frequency invariant is required before those steps have a proved
growth guarantee.

The bounds leave a useful, checkable sufficient condition: if a pool
has `H(O)` large enough that `K/H(O)` meets the target density, weighted
flow provides a correct early exit. What remains unproved is that some
pool on a guessed caterpillar branch always has this property, or has
an alternative useful exit, on general instances.

## 4. Common pivots alone do not simplify the exact colored oracle

The exact colored density problem remains NP-hard even when all
witnesses have equal red degree, have their own private red, and share
any fixed positive number `h` of common red pivots.

Start with the CLIQUE construction in `colored-union-investigation.md`:
positions `1,...,t`, red labels `(i,v)`, and a color `{i,j}` for every
position pair. An edge-compatible witness has two label reds. Add `h`
common reds to every witness and add one private own-test red to each
witness. Every witness now has degree `h+3`.

For any chosen collection, retain one witness per represented color.
This does not increase its red union or change its colors. If the
retained collection uses `L` label reds and covers `C` colors, its
colored density is

```
1 + (L+h)/C.
```

Put `T=binomial(t,2)`. We have `C<=T` and `C<=binomial(L,2)`.
If `L<t`, the function `(L+h)/binomial(L,2)` is strictly decreasing
for integers `L>=2`, so the density is greater than
`1+(t+h)/T`. If `L>t`, the bound `C<=T` gives the same strict
inequality. If `L=t`, reaching that threshold requires `C=T`, hence
one label per position and a `t`-clique. A clique achieves equality.
This proves the claim.

The whole hard instance is the neighborhood of any common pivot, and
also the intersection of the neighborhoods of all `h` pivots. Thus
being obtained by these neighborhood operations does not by itself
make the colored oracle exact-polynomial.

Even an absolute degree cap on those pivots is insufficient as a
structural promise. If the pool has `N` witnesses, embed it in a larger
uniform-degree instance by adding witnesses on disjoint reds. For any
target `k` and fixed `0<c epsilon<1`, taking the ambient witness count
`n>=Nk` ensures the CDM threshold

```
D=n/k^(1-c epsilon) >= N.
```

The common pivots then lie below this cutoff, while their candidate
pool is unchanged. This padding argument does **not** simultaneously
enforce the difficult log-density relation between `n`, `k`, and the
optimum back-degree. It rules out an argument relying only on the
common-pivot operation and a degree cap, not a stronger algorithm using
all numerical and optimum-occupancy promises.

The same construction is a depth-two precedence instance: label and
common reds are prerequisite tests, and witnesses are informative tests
with their own costs. Making the test of color `b` distinguish only
hypothesis `b` realizes the color alternatives in a separator problem.
This does not turn exact local-oracle hardness into an approximation
lower bound for full decision trees.

## Conclusion for the general-tree objective

A flow routine can safely exploit locally low color multiplicity, and
color peeling can give a sound coverage-or-expansion dichotomy. Neither
currently supplies a general sub-cube-root separator oracle. Their
explicit loss depends on the density of surviving optimum colors among
all candidates. The outstanding task is a theorem that improves this
occupancy, pays for high collisions using shared red cost, or supplies
an entirely different useful exit. General precedence closures do not
automatically provide any of these conditions.
