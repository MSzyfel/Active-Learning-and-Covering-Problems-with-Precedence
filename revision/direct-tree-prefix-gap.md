# A direct-tree obstruction and a simultaneous-prefix LP gap

This note gives a precise negative result for one route toward a decision-tree
approximation below `m^(1/3)`. It does not prove computational hardness at that
exponent. The finite-field instance from `decision-tree-cover-gap.md` already
has expensive optimal decision trees, and its fractional solution can be made
consistent across all prefix lengths under monotonicity and a unit-work-per-slot
constraint. Thus simply replacing separate separator LP calls by simultaneous
prefix copies does not remove that gap. Mixed-time conditioned constraints are
not included in the relaxation considered here.

## The instance and its actual optimal tree costs

Let `q=2^s >= 8`. There are `q^2` point tests `P_(t,u)`, for `(t,u)` in
`F_q^2`, and `q^3` graph tests `G_f`, for polynomials
`f(t)=a t^2+b t+c`. The predecessors of `G_f` are precisely the `q` point
tests on its graph. Thus `m=q^3+q^2`, and the precedence order has height two.

For the binary version, take hypotheses `a in F_q`. Point tests are
uninformative; `G_f` asks whether the hypothesis equals its leading
coefficient `a`. Every normalized decision tree has a single internal path:
each informative test peels off at most one singleton hypothesis. The path
must test at least `q-1` distinct colors.

If `t` distinct graph tests have been used, their point predecessor sets
each have size `q`, and any two intersect in at most two points. If `d_P`
counts the selected graphs incident to `P`, Cauchy--Schwarz gives

```
number of point predecessors
  >= (sum_P d_P)^2 / sum_P d_P^2
  >= t q^2 / (q+2(t-1)).
```

With `t=q-1`, this is `Omega(q^2)`. Executing every point test and then one
graph test for each of `q-1` colors costs at most `q^2+q-1`. Consequently

```
OPT_W = Theta(q^2).
```

For the total uniform-average objective, stop the internal path after its
first `t=q/2` distinct colors. Every test in this prefix is reached by at
least `q/2` hypotheses. Its point-test count is at least

```
(q/2) q^2 / (2q-2) > q^2/4.
```

The prefix therefore contributes more than `q^3/8` to the total average
cost. The same all-points-first strategy gives the upper bound
`q(q^2+q-1)`, proving

```
OPT_A = Theta(q^3).
```

To obtain exact correspondence with full covering, replace each color `a`
by two hypotheses `a^0,a^1`, and give `G_f` replies `{a^0}`, `{a^1}`, and
the remaining hypotheses. All `q` colors must then be covered. This is
the manuscript's paired-hypothesis reduction, with at most three outcomes
per test and the same `m`. A normalized tree still has one internal path.
Its worst cost equals full precedence-cover cost, and its total average
cost is exactly twice the full min-sum-cover cost. The displayed asymptotic
tree bounds continue to hold.

## A full-quota fractional point

Use the pair-conditioned LP from
`global-lp-decision-tree-investigation.md`, now with all `q` colors as the
target and budget `K=3q`. A point test covers nothing; a graph test covers
its leading-coefficient color. Define

```
x_P = y_P = 1/q,
x_G = y_G = a_(a,G) = 1/q^2,
z_a = 1.
```

All unspecified assignments are zero. Use symmetric red-pair variables

```
Y_(P,P) = 1/q,
Y_(P,Q) = 1/q^2                 for distinct point tests,
Y_(P,G) = 1/q^2                 when P precedes G,
Y_(P,G) = 0                    otherwise,
Y_(G,G) = 1/q^2,
Y_(G,H) = 0                    for distinct graph tests.
```

The total red mass is `2q <= K`; all colors receive assignment mass one.
For a point and one color, the load is `q/q^2=1/q=y_P`; its load over
all colors is `q^2/q^2=1=q y_P`. A graph's own red has only its own
assignment. The individual closure size is `q+1 <= K`.

The point row has sum

```
1/q + (q^2-1)/q^2 + q^2/q^2
  = 2+1/q-1/q^2 <= 3 = K y_P.
```

A graph row sums to `(q+1)/q^2 <= K y_G`. The pair lower bounds for
every closure hold, as do symmetry, diagonal consistency,
`Y_pr <= min(y_p,y_r)`, `x_j=y_j` for each test's own red, and the exact
precedence identities `Y_(P,G)=y_G`. Thus this is a feasible full-quota
point at budget `3q`, although full integral coverage costs `Omega(q^2)`.

## A precise simultaneous-prefix relaxation

The following is a valid relaxation of full precedence-constrained min-sum
cover. At every integer depth `d=0,...,m`, use a copy
`(x(d),y(d),a(d),z(d),Y(d))` of the pair-conditioned constraints, with
budget `K=d`, target parameter `k=q`, and no fixed equality on
`sum_a z_a(d)`. Require:

* all variables are componentwise nondecreasing in `d`;
* all variables start at zero;
* `x_j(d)=y_j(d)` for each test's own red;
* `sum_j (x_j(d+1)-x_j(d)) <= 1`;
* every final coverage marginal is one: `z_a(m)=1`.

Keep the equalities assigning each blue's covered mass:
`sum_(j:a in B_j) a_aj(d)=z_a(d)`. A set whose closure is larger than
`d` can additionally be forced to have zero selection at that depth.
Minimize

```
L = sum_(d=0)^(m-1) (q - sum_a z_a(d)).
```

This is a lower bound on integral latency: for an actual sequence, use
prefix selection indicators, their pair products, and assign each color
permanently to its first covering test. Those assignments are monotone,
and the objective is exactly the sum of coverage times. The constraints
do not assert the existence of a joint probability distribution over
complete sequences.

Let `v*` denote the full-quota fractional point above. Define

```
s_d = 0                         for d <= 3q,
s_d = (d-3q)/(2q)               for 3q <= d <= 5q,
s_d = 1                         for d >= 5q,
v(d) = s_d v*.
```

Every homogeneous constraint is preserved by scaling. At positive depths
`d>=3q`, the pair row bound with budget `d` follows from the base bound
with `3q`. Total red mass is `2q s_d <= d`. The closure-size filter also
holds whenever a variable is positive. The per-slot work bound holds
with equality during the ramp, because the base selection mass is `2q`.
All monotonicity, terminal coverage, diagonal, and comparable-pair
constraints hold. Since `5q <= m`, this defines a feasible full profile.

Its latency objective is

```
L = 3q^2 + sum_(r=0)^(2q-1) q(1-r/(2q))
  = 4q^2 + q/2.
```

Integral full-cover latency is greater than `q^3/8` by the first-half
prefix argument above. The simultaneous-prefix relaxation therefore has
an `Omega(q)=Omega(m^(1/3))` integrality gap. Through the paired-hypothesis
construction, the same ratio holds for the corresponding tree objective,
with both integral and fractional costs multiplied by two. Its natural
makespan version also has an `Omega(q)` gap: fractional completion occurs
by depth `5q`, while integral completion needs `Omega(q^2)` tests.

## What this does and does not rule out

The obstruction survives a global monotone schedule, a unit-work-per-slot
bound, full final coverage, and the fact that the original instance comes
from a very simple decision tree. It therefore rules out a proof that
these features alone repair the pair-conditioned LP's exponent.

It does not rule out a stronger global relaxation or an algorithm using
the actual prerequisite overlaps. In particular, conditioning the
coverage quota on selecting one graph test would detect that this moment
point has `Y_(G,H)=0` for all other graph tests. Mixed-time moments or a
joint decision-tree relaxation can impose further constraints not modeled
here. No below-`1/3` theorem follows from this note, and no universal
algorithmic lower bound at `1/3` is claimed.
