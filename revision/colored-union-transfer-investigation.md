# Colored minimum union: exact transfer and the remaining obstruction

Research audit, 29 October 2026. This note does not establish a general
sub-cube-root approximation. It gives an exact reformulation, identifies
what the strongest nearby published algorithms actually provide, and
states an oracle condition that would suffice for a constant-coverage
improvement. The reductions and checks below are direct arguments; their
novelty is not asserted.

## Exact formulation for arbitrary coverage instances

Let the original tests be indexed by `i in [m]`. Write `C_i` for the
complete prerequisite closure of test `i`, including `i` itself, and
`B_i` for the blue elements covered by the test. Unit test costs give the
cost `|union_(i in I) C_i|`. The same argument works with nonnegative
weights on the closure elements.

Form a witness ground set

```
W = {(i,b): b in B_i},                 N=|W|=sum_i |B_i|.
color(i,b)=b,
f(A)=|union_((i,b) in A) C_i|,
r(A)=|{b: (i,b) in A for some i}|.
```

Here `f` is a monotone coverage submodular function, and `r` is the rank
function of the partition matroid with one class per blue element.
Exactly, for every target `k`,

```
OPT_cover(k) = min { f(A): A is partition-independent and |A|=k }
             = min { f(A): r(A)>=k }.
```

For the forward direction, choose `k` covered blues and one selected test
witnessing each; the resulting witnesses have distinct colors and use no
extra closures. For the reverse direction, select the original tests
appearing in the witnesses; their closure union is exactly the witness
cost, and they cover every represented color. Trimming to one witness per
represented color and then to `k` colors cannot increase cost.

Thus arbitrary cover does reduce to minimum union with a partition-rank
quota. It does **not** reduce, by this construction, to ordinary minimum
`k`-union. Moreover, `N` can be as large as `m |B|`; an approximation
parameterized by `N` need not have the same exponent in the number `m` of
tests. If every test covers one blue, then `N` is just the number of
informative tests.

## Why ignoring colors fails, even for quarter-universe targets

Fix integers `k>=2` and `R>=2`. There are `4k` blues. Color 1 has `k`
informative tests, each with no prerequisites and its own unit test cost.
Every other color has one informative test, requiring `R` private
prerequisite tests and its own test. All prerequisite tests are
uninformative. All colors are therefore distinguishable by singleton
binary tests, and the separator quota is exactly `|B|/4=k`.

The uncolored minimum union of `k` witnesses costs exactly `k`: choose all
the cheap witnesses of color 1. It covers only one blue. A colored solution
covering `k` blues costs exactly

```
1+(k-1)(R+1).
```

Consequently an exact ordinary minimum-union oracle is already insufficient
as a black box: its optimal output can have only `1/k` of the required
color coverage. This example retains own-test costs and is an actual
depth-two precedence instance, not a weighted abstraction.

A valid but limited transfer is available when every color has at most
`F` witnesses. Ordinary minimum `k`-union returns `k` witnesses of at
least `ceil(k/F)` colors. Its cost is at most its approximation factor
times `OPT_cover(k)`, because every colored optimum is an admissible
uncolored solution. This loses a factor `F` in coverage. The gap example
in `sdp-strong-gap.md` has `F=q^2=Theta(m^(2/3))`, so this observation
does not retain a constant fraction there.

## What the nearby published results establish

* Chlamtac--Makarychev--Vakilian, APPROX 2023, Theorem 1.3, gives
  `O(m^(1/3) log^(4/3)(r) log(b))` for full red-blue set cover; Appendix A
  treats partial cover. Their reduction in Section 5 runs from minimum
  `k`-union to red-blue set cover, not in the direction needed to import a
  better union algorithm. Their conditional lower bound is approximately
  `m^(1/4-epsilon)`. [Primary paper](https://arxiv.org/html/2302.00213).

* Chlamtac--Dinitz--Makarychev, SODA 2017, Theorem 1.6, gives
  `O(N^(1/4+epsilon))` for ordinary minimum union, equivalently bipartite
  expansion, where `N` is the number of candidate sets on the selected
  side. The algorithm uses asymmetric pruning and caterpillar-style
  neighborhood exploration. It has no partition-rank guarantee.
  [Primary paper](https://arxiv.org/html/1611.07866).

* Chlamtac--Dinitz--Krauthgamer, FOCS 2012, develops faithful rounding for
  smallest-edge subgraph with factor `n^(3-2sqrt(2)+epsilon)`. Its
  faithfulness bounds vertex marginals above by a factor times fractional
  values, edge marginals above by their fractional values, output vertex
  count deterministically, and expected total edge count below up to
  polylogarithmic loss. It does not give a lower marginal guarantee for
  each edge, nor a guarantee on the number of edge colors represented.
  [Definition 2.1 and the full framework](https://arxiv.org/html/1205.0144).

* Goemans--Harvey--Iwata--Mirrokni approximate arbitrary monotone
  submodular functions everywhere within `O(sqrt(N) log N)` using a value
  oracle. The resulting ellipsoidal surrogate can be optimized over a
  partition base, but this general-purpose ratio is worse than the
  desired exponent. [Primary paper](https://math.mit.edu/~goemans/PAPERS/approx-subm.pdf).

* Oettershagen--Wang--Gionis, WWW 2024, study edge-color constraints on
  ordinary graph density. Their constant-factor guarantee is for sparse
  input graphs and lower bounds on counts of edges of specified colors.
  This is a different objective and does not give a general colored
  minimum-union theorem. [Primary paper](https://arxiv.org/abs/2402.09124).

The search did not locate a later improvement to the general CMV exponent.
This is a literature-search finding, not a proof that no such publication
exists. A 2025 primary application still explicitly uses the CMV cube-root
bound: [Targeted Least Cardinality Candidate Key, Theorem 11](https://drops.dagstuhl.de/storage/00lipics/lipics-vol328-icdt2025/LIPIcs.ICDT.2025.21/LIPIcs.ICDT.2025.21.pdf).

## Two separate obligations for dense-subgraph methods

First, a witness activates **all** red elements of its closure. A dense
bipartite subgraph algorithm may select many witness-red incidences while
omitting private red neighbors. For example, `t` witnesses can share `d`
red neighbors and each have one extra private neighbor. Their common
incidence subgraph is dense, but their actual red union costs `d+t`.
Density guarantees alone do not bound that union cost.

Second, witness count is not color count. Faithful upper marginals and
an expected total witness count do not exclude concentration on a small
set of colors. The partition equalities and same-color exclusions in a
relaxation help formulate this obligation, but a rounding theorem must
actually carry it into its integral output.

Even the exact unconstrained density primitive used by ordinary union
algorithms changes character. Minimizing

```
f(A)-lambda |A|
```

is submodular minimization, and for union functions has a standard
minimum-cut representation. Replacing cardinality by `r(A)` gives
`f(A)-lambda r(A)`, a difference of submodular functions. This expression
need not be submodular: take two witnesses of the same color, with
disjoint singleton red sets. At `lambda>0`, the submodular inequality for
the two singleton witness subsets fails. Thus the old minimum-cut
primitive cannot simply be called after replacing cardinality by color
rank. This explains a specific missing step in a colored caterpillar
extension; it does not prove such an extension impossible.

## A sufficient general-instance oracle target

The following density statement would suffice. Let `K` be a budget that
admits a solution covering `q` currently uncovered blues. Suppose an
algorithm returns a nonempty set of tests `I` with capped gain

```
g=min(q, number of newly covered blues)>0,
cost(I) <= rho(m) K g/q.
```

Run the oracle on residual targets `q=k-c`, where `c` is the number of
already covered blues, stopping once `c>=delta k` for any fixed
`0<delta<1`. A solution of original cost `K` still covers at least `q`
uncovered blues. Charge each batch's union cost separately; this only
overestimates the final closure union. All nonfinal batches have total
gain below `delta k` and have `q>(1-delta)k`, so their total cost is at
most `rho K delta/(1-delta)`. The last batch costs at most `rho K`,
because `g<=q`. Hence the final cost is at most

```
rho(m) K/(1-delta).
```

This elementary reduction shows that an `m^(1/4+epsilon)` colored
**density** oracle would already suffice; it need not directly solve a
fixed quota in one call. It must use actual feasibility at budget `K` or
a stronger valid relaxation, rather than assume that feasibility of the
particular SDP in `sdp-strong-gap.md` certifies integral feasibility.

A useful randomized interface is also precise. If one can sample a batch
with `E[cost]<=U` and `E[g]>=v>0`, where `g` is already capped at `q`,
put `lambda=2U/v`. Then

```
E[lambda g-cost]>=U,
lambda g-cost<=lambda q,
Pr[lambda g-cost>0]>=v/(2q).
```

Whenever `v/q` is inverse-polynomial, repeated sampling finds a positive
score and therefore cost/gain at most `2U/v`. Establishing these bounds
with `U/v=O(m^(1/4+epsilon)K/q)` is a concrete research target. Merely
lower-bounding uncapped witness count does not provide the required `v`.

## Stress test against the strong SDP gap

The construction in `sdp-strong-gap.md` has `qL` prerequisite tests and
target `k=q/4`. Activating all prerequisites and any `k` witnesses of
distinct colors costs

```
qL+k.
```

For every fixed positive coverage fraction, its lower bound is `qL/2`.
Thus this elementary integral algorithm is a `2+o(1)` approximation to
the integral optimum on the family. The family is therefore not itself
hard for an optimum-relative approximation algorithm.

What it rules out is using its feasible SDP budget `K=2q` as the reference
cost for a sub-cube-root constant-coverage guarantee. For such a proposed
guarantee, `rho(m)K=o(qL)` whenever
`rho(m)=O(m^(1/3-epsilon))`, contradicting the integral lower bound.
Any successful higher-moment or combinatorial method must reject that
small budget, change its benchmark, or use information absent from that
relaxation. The gap does not rule out the colored density-oracle approach
with an actual integral feasibility promise.
