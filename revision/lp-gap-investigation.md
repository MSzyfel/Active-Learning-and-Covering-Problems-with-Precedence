# A finite-field gap for the pair-conditioned LP

This construction gives an `Omega(m^(1/3))` constant-fraction integrality
gap for the LP in `global-lp-decision-tree-investigation.md`, even on the
closure instances arising from precedence cover. It also gives a tight
example for that note's stated rounding when a particular feasible LP
solution is supplied. Neither observation is a hardness result for the
underlying problem.

## Precedence instance and fractional solution

Let `q >= 5` be a prime power and let `F` be the field of order `q`. Create
one point-test `P_(t,u)` for each `(t,u) in F^2`. For each polynomial
`f(t) = a t^2 + b t + c`, create a graph-test `G_f` with one private blue
element `b_f`; its predecessors are the `q` point-tests
`P_(t,f(t))`. The point-tests have no predecessors or blue elements.
Hence there are `q^2 + q^3` tests. In the closure reduction, the set for a
test consists of its predecessor closure, with one red element per test.
Thus the closure set for `G_f` has `q+1` red elements and the blue `b_f`,
while the set for `P_(t,u)` has one red element and no blue.

Set the target `k = q-1` and LP budget `K = 2q-1`. For every point-test,
put `x_P = y_P = 1/q`. For every graph-test, put
`x_G = y_G = a_(b_G,G) = z_(b_G) = (q-1)/q^3`. All other assignments are
zero. Define symmetric pair variables by

```
Y_(p,p) = y_p,
Y_(p,r) = 1/[q(q+1)]       for distinct point-tests p,r,
Y_(p,G) = x_G              if p is a predecessor of G,
Y_(p,G) = 0                otherwise,
Y_(G,H) = [(q-2)/(q^3-1)] x_G   for distinct graph-tests G,H.
```

There are exactly `q^2` graphs through each point. Consequently the red
budget is `q + (q-1) = K`, the blue total is `q-1 = k`, and the total
assigned load through any point is `q^2 x_G = (q-1)/q = k y_P`. A
graph-test has only its own private-blue assignment, so both its blue-load
constraints hold. For a point-test, the pair-variable row sum is

```
1/q + (q^2-1)/[q(q+1)] + q^2 (q-1)/q^3
  = 1 + (q-1)/q = K y_P.
```

For a graph-test, the row sum is `(q+1)x_G + (q-2)x_G = K y_G`. For distinct point
tests, `1/[q(q+1)] >= (q-1)/q^3 = x_G`; thus every pair in a graph-test's
closure satisfies `x_G <= Y_pr`. The other LP constraints follow directly.
In particular, this solution has `x_j = y_j` for every test's own red
element, as well as symmetric `Y`, `Y_pp = y_p`,
`Y_pr <= min(y_p,y_r)`, and equality in every pair-row budget.

## The gap

Two distinct degree-at-most-two polynomials agree at at most two field
points. Let a family of `t` graph-tests reach `U` distinct point-tests.
The total point incidences are `tq`; the sum of squared point degrees is
at most `tq + 2t(t-1)`. By Cauchy--Schwarz,

```
|U| >= (tq)^2 / (tq + 2t(t-1))
     = t q^2 / (q + 2(t-1)).
```

To cover any fixed fraction `delta > 0` of `k`, the solution must choose
at least `ceil(delta k)` graph-tests. Taking exactly that many among them
in the inequality shows that it incurs `Omega_delta(q^2)` red cost. The
LP budget is `K = 2q-1`, so the constant-fraction gap is `Omega_delta(q) =
Omega_delta(m^(1/3))`. This also applies to precedence cover itself,
since a feasible solution is a downward-closed family of tests.

## Tightness of the stated rounding for a true optimum of size K

Add one graph-like test `G_*` with exactly `2q-2` point-test predecessors
and the private blues of any `q-1` original graph-tests. It has closure
cost `2q-1` and covers the full target. Give `G_*` and its own red element
LP value zero, as well as zero assignments and pair variables involving
its own red element. The displayed LP solution remains feasible, and
`m = q^3 + q^2 + 1`. For `q >= 5`, a cover avoiding `G_*` must choose
`q-1` original graph-tests and the above inequality makes its point-test
cost alone greater than `q`; including their `q-1` graph-tests gives a
total strictly above `2q-1`. A cover containing `G_*` costs at least
`2q-1`. Thus the true optimum is exactly `K = 2q-1`.

In the rounding, `T = ceil(m^(1/3)) = q+1`; every point-test has
`y_P = 1/q >= 1/T`, so all `q^2` point red elements are bought. No blue
is covered by their singleton sets, so the early-return condition does not
apply. The added test has `x_(G_*) = 0` and is never selected. Any rounded
output covering even a fixed fraction of the target therefore selects
`Omega(q)` original graph-tests, whose original closure costs
`Omega(q^2)` by the same intersection argument. The ratio is
`Omega(q) = Omega(m^(1/3))` against the true optimum.

This is a worst case for rounding the particular feasible LP solution,
not for every possible LP solution or every choice of optimal LP solver.
The added test itself supplies an integral LP solution of cost `K`.
