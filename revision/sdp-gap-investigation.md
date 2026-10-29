# A covariance strengthening and the polynomial-graph LP gap

This note records two concrete checks. The quadratic-graph gap for the
displayed global LP can be made to have a constant target fraction of the
blue universe. A polynomial-size positive-semidefinite moment strengthening
with a conditioned assignment quota eliminates this particular obstruction.
Neither observation supplies a general rounding algorithm below exponent
`1/3`.

## Making the gap use a constant blue target fraction

Let `q` be a prime power. There are `q^2` point tests, indexed by
`p=(u,v) in F_q^2`, and `q^3` graph tests, indexed by polynomials
`f(u)=a u^2+b u+c`. Graph test `f` has the `q` point tests on its graph as
prerequisites. Thus its closure consists of those points and its own graph
test. Point tests have no prerequisites and cover no blues.

Use just `q` blue elements, indexed by the leading coefficient `a`. Graph
test `f` covers blue `a`. Each blue therefore has `q^2` alternative graph
tests, and each point belongs to exactly `q` graph tests for each blue.
Different graph tests have at most two point prerequisites in common.

For any integer target `1 <= k <= q`, the following first moments satisfy
the original global LP:

```
y_p = x_p = 1/q                    for point tests p,
y_f = x_f = 1/q^2                  for graph tests f,
z_a = k/q                          for every blue a,
a_(a,f) = k/q^3                    when f has leading coefficient a.
```

In particular, every set variable equals its corresponding own-test red
variable, and `sum_j x_j = sum_r y_r = 2q`. Take `K=2q+1` and symmetric
pair variables as follows:

```
Y_pp = 1/q,
Y_pr = 1/q^2                       for distinct point tests p,r,
Y_pf = Y_fp = 1/q^2                when p lies on f,
Y_ff = 1/q^2,
all other graph-containing pairs = 0.
```

The point pair-row sum is
`1/q + (q^2-1)/q^2 + q^2/q^2 = 2+1/q-1/q^2`, which is at most
`K y_p = 2+1/q`. A graph row sums to `(q+1)/q^2`, at most `K y_f`.
Every pair in a graph closure has moment at least `x_f`.

The assignment constraints also hold. Each blue has assignment mass
`q^2(k/q^3)=k/q=z_a`. A point has assignment load `k/q^2` for each blue,
at most `y_p=1/q`, and its total assignment load is exactly
`q^2(k/q^3)=k/q=k y_p`. A graph-own red has total load `k/q^3`, at most
`k y_f=k/q^2`. The remaining per-set load and domination constraints are
immediate from these values.

Any integral solution covering `s` distinct blues contains at least `s`
distinct graph tests. If `U` is the union of the point prerequisites of
any `s` such tests, Cauchy--Schwarz gives

```
|U| >= (s q)^2 / (s q + 2 s(s-1))
     = s q^2 / (q + 2(s-1)).
```

Indeed, writing `d_p` for the number of chosen graphs through a point,
`sum_p d_p=sq` and `sum_p d_p^2 <= sq+2s(s-1)`.
For `k=Theta(q)` and any fixed positive covered fraction, `s=Theta(q)`,
so the actual point cost is `Omega(q^2)` whereas the displayed LP budget
is `O(q)`. Since there are `m=q^3+q^2` tests, this is an
`Omega(m^(1/3))` constant-fraction gap. One can take `k=q`, or
`k=floor(q/4)` if the intended auxiliary problem asks for one quarter of
the universe. Grouping the blues by leading coefficient removes the
vanishing-target-fraction issue of a private blue for every graph.

This is an integrality-gap statement about this relaxation; it is not a
hardness result for precedence cover or adaptive decision trees.

## A PSD inequality with a conditioned quota

The following statement applies to a general family of sets of point
prerequisites. Suppose every graph test `g` has exactly `r` point
prerequisites `P_g`, and distinct graph tests satisfy
`|P_g intersect P_h| <= d`.

Introduce a binary witness variable `Q_g` for each graph test. In the
grouped-blue construction, `Q_g=1` means that graph `g` is chosen as the
single witness for its blue. If a solution covers at least `k` blues,
choose exactly `k` of them and one witnessing graph per chosen blue.
Because each graph covers only one blue, these witnesses are distinct.
Consequently this is a valid integral encoding with

```
sum_g Q_g = k,
Q_g <= Y_p                         for every p in P_g.
```

Let `E_tilde` denote degree-two pseudoexpectations. Require:

* a positive-semidefinite moment matrix on `1`, all point variables
  `Y_p`, and all witness variables `Q_g`;
* Boolean diagonal identities, nonnegative witness pair moments, and
  `E_tilde[Y_p Q_g] = E_tilde[Q_g]` for `p in P_g`;
* the original quota and its conditioning by every witness:
  `sum_g E_tilde[Q_g]=k` and
  `sum_h E_tilde[Q_g Q_h]=k E_tilde[Q_g]` for every `g`.

These are polynomially many semidefinite and linear constraints, all
valid for integral solutions. Merely adding a PSD condition to the
original displayed LP does not by itself assert the conditioned quota.

Define the linear form `C_p=sum_(g:p in P_g) Q_g`. PSD Cauchy--Schwarz
and prerequisite consistency imply

```
(E_tilde[C_p])^2
  = (E_tilde[Y_p C_p])^2
  <= E_tilde[Y_p^2] E_tilde[C_p^2]
  = y_p E_tilde[C_p^2].
```

Summing these inequalities by Cauchy--Schwarz again gives

```
(r k)^2 <= (sum_p y_p) (sum_p E_tilde[C_p^2]).
```

Nonnegative witness pair moments, the intersection bound, and the
conditioned quota yield

```
sum_p E_tilde[C_p^2]
  = r k + sum_(g != h) |P_g intersect P_h| E_tilde[Q_g Q_h]
  <= r k + d (k^2-k).
```

Therefore every such moment solution satisfies

```
sum_p y_p >= r^2 k / (r+d(k-1)).
```

For quadratic graphs, `r=q`, `d=2`, and `k=Theta(q)`, this proves a
point budget of `Omega(q^2)`. Hence this PSD relaxation eliminates the
constant-target-fraction gap above, irrespective of how its second
moments are completed. The same argument eliminates degree-`d`
polynomial graph examples for fixed `d` and `k=Theta(q)`.

## What this does and does not establish

The sparse assignment moments with zero pair moment for distinct graph
witnesses fail the conditioned quota even before PSD is imposed: their
row sum equals `E_tilde[Q_g]`, whereas conditioning requires
`k E_tilde[Q_g]`. Thus a red-only higher-moment construction with those
values should not be described as a full Sherali--Adams solution.

For general red-blue or precedence cover, one can introduce assignment
indicators `Q_(b,j)` with exactly `k` chosen blues and exactly one witness
set per chosen blue. Their first moments are the existing `a_bj`, and
conditioned assignment quotas can be added with polynomially many
second moments. A PSD matrix can contain the red and assignment
indicators, with prerequisite consistency for every witness.

The displayed lower-bound proof does not become a general rounding
theorem from those constraints. In a general instance, many assignments
can use the same set; their red intersections can be as large as the
entire set. There is also no fixed small bound on intersections between
distinct sets. The calculation identifies a concrete strengthening
which defeats the known polynomial-graph obstruction, while leaving
the general exponent-below-`1/3` problem unresolved.
