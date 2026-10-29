# A constant-target LP gap inside the decision-tree separator family

This note establishes a limitation of the pair-conditioned relaxation in
`global-lp-decision-tree-investigation.md`. Its `Omega(m^(1/3))`
constant-coverage-loss integrality gap persists when the target is exactly
one quarter of the blue universe and the cover instance is induced by
binary decision-tree tests through the manuscript's map `xi`. This is an
LP integrality gap, not a computational hardness theorem and not a proof
that decision trees cannot be approximated below exponent `1/3`.

## The colored finite-field construction

Let `q=2^s >= 8`, let `F` be the field with `q` elements, and put

```
m = q^2 + q^3,       k = q/4,       K = 2q.
```

There is a point-test `P_(t,u)` for every `(t,u) in F^2`, and a graph-test
`G_f` for every polynomial `f(t)=a t^2+b t+c`. The predecessors of `G_f`
are exactly the `q` point-tests `P_(t,f(t))`. Point-tests cover no blue
elements. There is one blue element `b_a` for each `a in F`; the graph-test
with leading coefficient `a` covers the single element `b_a`. Thus the
blue universe has size `q`, and the target is exactly its quarter.

In the closure reduction, `R_P={P}` and
`R_(G_f)={G_f} union {P_(t,f(t)):t in F}`. The corresponding blue
neighborhoods are empty and `{b_a}`, respectively. Each color has `q^2`
graph-tests. Every point is a predecessor of exactly `q^2` graph-tests,
and of exactly `q` graph-tests of each color.

Use the following fractional variables:

```
x_P = y_P = 1/q,
x_G = y_G = a_(b_a,G) = 1/(4q^2),
z_(b_a) = 1/4.
```

All other assignment variables are zero. Define symmetric pair variables
by

```
Y_(P,P) = y_P,
Y_(P,Q) = 1/q^2                         for distinct point-tests P,Q,
Y_(P,G) = x_G                           if P precedes G,
Y_(P,G) = 0                             otherwise,
Y_(G,G) = y_G,
Y_(G,H) = 0                             for distinct graph-tests G,H.
```

## Feasibility for the stated LP

The red mass is `q+q/4=5q/4 <= K`. The blue mass is `q/4=k`.
For every blue, its `q^2` assignments sum to `1/4=z_b`. Every graph's
one assignment equals its `x_G`, and is at most `k x_G`, since `k>=1`.
The individual closure-size filter retains every test, as `q+1<=K`.
The constraints `x_j<=y_p` for `p in R_j` hold directly.

For a point `P` and a color `b_a`, the assignment load is

```
q/(4q^2) = 1/(4q) <= y_P.
```

Its total assignment load is `q^2/(4q^2)=1/4=k y_P`.
For the red element of a graph-test, its only assignment has value `x_G`,
so its per-blue load is `y_G` and its total load is at most `k y_G`.

Every pair in a graph-test's red neighborhood has `Y>=x_G`: the cases
are two distinct points, a point diagonal, an incident point and the
graph's own red, or the graph diagonal. The point-test singleton
neighborhoods also satisfy the pair lower bounds.

The row sum at a point is

```
1/q + (q^2-1)/q^2 + q^2/(4q^2)
  = 5/4 + 1/q - 1/q^2
  <= 2 = K y_P.
```

The row sum at a graph-test is `(q+1)x_G <= K y_G`. All variables are
in their allowed ranges. In addition to the stated LP, this solution
satisfies `x_j=y_j` for every test's own red, `sum_j x_j<=K`, symmetry,
`Y_pp=y_p`, and `Y_pr<=min(y_p,y_r)`. It also satisfies the exact
comparable-pair identities `Y_(P,G)=y_G` on every precedence edge.
Unlike the private-blue example in `lp-gap-investigation.md`, the pair
row budgets here need not be tight.

## The integral cost of a constant fraction of the target

Fix any constant `delta>0` with `delta<=1`. Covering at least `delta k`
distinct colors requires at least `t=ceil(delta k)` distinct graph-tests.
Consider exactly `t` of them. Two distinct polynomials of degree at most
two agree at at most two points of `F`; hence their predecessor sets
intersect in at most two points.

If `d_P` is the number of these graphs incident to point `P`, then

```
sum_P d_P = tq,
sum_P d_P^2 <= tq + 2t(t-1).
```

Cauchy--Schwarz gives the following lower bound on the number of point
predecessors that must be executed:

```
|{P:d_P>0}| >= (tq)^2 / (tq+2t(t-1))
             = t q^2 / (q+2(t-1))
             = Omega_delta(q^2).
```

Thus the integral cost of covering even a fixed fraction of the target is
`Omega_delta(q^2)`, while the displayed LP is feasible at `K=2q`.
Since `m=q^3+q^2`, the gap is `Omega_delta(m^(1/3))`.

## Exact realization as a decision-tree separator instance

Take the hypotheses to be the `q` colors `a in F`. Make every point-test
uninformative, with its single reply equal to the entire hypothesis set.
For `f(t)=a t^2+b t+c`, give `G_f` the binary replies

```
{a},       F minus {a}.
```

Keep the same precedence order. All hypotheses are distinguishable. Since
`q>4`, the large reply has size `q-1>3q/4`, so the manuscript's definition
in `sections/approximating_learning.tex` gives

```
xi(P) = empty set,       xi(G_f) = {a},       U_xi = F.
```

Consequently the separator call has exactly the preceding cover instance
and target `|U_xi|/4=q/4`. No padding, diagnostic tests, or growing
coverage-loss factor is needed. This rules out improving the exponent by
rounding the displayed LP solely through the observation that the target
is a constant fraction or that the sets come from binary test partitions.
It does not rule out a stronger relaxation or another algorithm.

## Structural context and the remaining route

For an arbitrary test partition, `xi(t)` is either the whole hypothesis
set, or the complement of a unique reply of size greater than `3n/4`.
In the latter case it is an arbitrary subset of size less than `n/4`;
every such subset is realized by a binary test. There is therefore no
general overlap or laminarity restriction on the small `xi` sets.

The full-cover reductions already proved at
`sections/hardness.tex:715` and `sections/hardness.tex:732` are a different
statement: paired hypotheses make every normalized decision tree a single
internal path, with worst-case cost equal to full-PCSC cost and total
average cost equal to twice full-MSSC cost. They show that a general
decision-tree improvement also improves the associated full covering
problem. They do not, by themselves, establish a constant-fraction
separator LP gap; the colored construction above supplies that missing
step for this particular relaxation.

Pair separation and entropy alone do not avoid the full-cover embedding.
After `r` of its `N` universe elements are covered, the hypothesis
partition consists of `2r` singleton replies and one block of size
`2(N-r)`. Its separated-pair count is

```
C(2N,2)-C(2(N-r),2) = r(4N-2r-1),
```

and its entropy under the uniform distribution is

```
log(2N) - ((N-r)/N) log(2(N-r)),
```

with the last term interpreted as zero when `r=N`. Both are functions
only of ordinary coverage. Replacing coverage with these potentials does
not introduce an extra structural restriction on this subfamily.

A viable unresolved direction is to condition *coverage and set-selection
constraints*, not merely red-cost moments. In the displayed gap,
`Y_(G,H)=0` for distinct graph-tests: interpreted probabilistically,
conditioning on selecting one graph would forbid every other graph, even
though covering `k=q/4>1` colors requires other graphs. The current LP
never enforces that conditional implication. A consistent lift with
conditioned blue variables and assignments would reject this particular
moment solution. This is a research direction, not a proved rounding
guarantee: a replacement feasible fractional solution might still exist,
and a below-`1/3` theorem requires both a stronger lower bound and a new
rounding analysis.
