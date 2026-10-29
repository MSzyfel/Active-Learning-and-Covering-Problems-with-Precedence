# Triple decomposition with explicit color and overlap accounting

Research note, 29 October 2026. This note gives a polynomial decomposition
of every instance into common-core pieces with regular triple codegrees,
and an algorithmically checkable sufficient condition for combining their
quarter-power guarantees. The combining condition is not proved to hold
with a sub-cube-root value on every instance. Consequently this is **not**
a general improvement to the approximation exponent. The manuscript is
unchanged; no novelty claim is made.

## 1. Model and the useful local guarantee

There are `M` available sets/tests. Test `i` has red closure `R_i` and
covers blue set `B_i`. Red costs are one; a precedence closure includes
the test itself. A solution pays the union of its red closures. Let `m`
denote the original total number of tests when this is a precedence
instance, so `M<=m`. Nothing below replaces `M` by the number of
test-blue incidence copies.

A piece consists of a subfamily `J`, a common core

```
H subset intersection_(i in J) R_i,
P_i = R_i \ H,
U = union_(i in J) P_i,
r=|U|,              N=|J|.
```

Suppose `d<=|P_i|<2d` for every `i in J`, where `d>=3`. Write

```
c(A) = |union_(i in J: A subset P_i) B_i|,      |A|=3,
C3 = max_A c(A).
```

Thus `c(A)` counts distinct available blues, not witnesses. Assume the
checkable condition

```
C3 <= C N binom(d,3)/binom(r,3),               C>=1.       (1)
```

For every feasible target `q`, selecting arbitrary witnesses for `q`
distinct blues gives residual red cost at most

```
rho(N,C) OPT_tail(q),
rho(N,C) = 2 (C N)^(1/4).                                  (2)
```

Here `OPT_tail(q)` minimizes the union of the `P_i`; the core is charged
separately once. This guarantee remains valid after deleting any subset
of the blue universe. Deleting blue labels can only decrease `C3`.

Proof: fix optimum residual union `S`, `s=|S|`, and assign each of `q`
covered blues to one chosen witness. Counting its residual triples gives

```
q binom(d,3) <= C3 binom(s,3).
```

By (1),

```
r/s <= [(9/2) C N/q]^(1/3),
```

using `r^3/[r(r-1)(r-2)]<=9/2` for `r>=3`. The arbitrary representatives
have union at most `min(2dq,r)`, while `s>=d`. Their ratio is therefore

```
min(2q, [(9/2) C N/q]^(1/3)) <= 2 (C N)^(1/4).
```

The selected witnesses may cover extra blues; crediting only `q` is
allowed. The proof also permits a test to cover several blues. For an
empty-tail piece, buying `H` covers all its available blues, so its
residual problem is solved exactly at cost zero.

This is a distinct-color version of the bounded-codegree argument in
`higher-order-rounding-investigation.md`; it uses an integral counting
bound and requires no relaxation.

## 2. Every instance has a polynomial regular-core decomposition

Fix any desired constant `C>=1`. The following procedure partitions the
available tests into at most `M` nonempty leaves. Every leaf has either
empty residual tails, or tails satisfying (1) and lying in one degree
range `[d,2d)`, `d>=3`.

At a node containing nonempty test family `J`:

1. Set `H=intersection_(i in J) R_i`, removing the **entire** common
   intersection for the purposes of this node's accounting. Its residual
   tails consequently have empty common intersection.
2. Partition the tests by residual degree into the buckets `{0}`,
   `{1,2}`, and `[3*2^h,6*2^h)` for integers `h>=0`. If several buckets
   are nonempty, recurse on these buckets.
3. If the sole bucket is `{0}`, stop. If it is `{1,2}`, choose a residual
   red occurring in some test and split into its star and complement.
4. Otherwise compute `C3`. If (1) holds, stop. If not, choose a violating
   triple `A`, and split into `J_A={i:A subset P_i}` and `J\J_A`.

Every split is proper. For step 3, no residual red belongs to every test.
For step 4, a violating triple occurs somewhere, but a triple belonging
to every test would be part of the removed common intersection. Both
children are therefore nonempty. Each internal node has at least two
children, and the leaves partition the original `M` tests. There are at
most `M` leaves and `2M-1` nodes. All intersections, buckets and
distinct-color triple counts can be computed in polynomial time in the
explicit input.

This supplies the requested structural alternative in a literal sense:
an irregular triple yields a smaller proper test subfamily, while a
common triple is charged to a core. It does **not** promise a constant
factor decrease in subinstance size, preserve a constant fraction of an
unknown optimum's colors in one child, or partition the optimum red
budget. Those three quantitative distinctions matter.

Core charges are shared red costs, not separate artificial red copies.
The algorithm stores each core as a subset of the original red universe.
The recursive bookkeeping does not buy cores merely because they occur
in the decomposition.

## 3. A fractional overlap certificate that is sufficient for rounding

The following combining theorem works for arbitrary overlapping pieces,
not just the partition above.

Take a polynomial family of pieces `(J_l,H_l,U_l)`. Suppose piece `l`
has an exact-target residual algorithm with approximation `rho_l>=1`,
valid for every restriction of the blue labels. The regular leaves above
have `rho_l=2(C N_l)^(1/4)`; empty-tail leaves need no residual
approximation. Other valid local algorithms may be included as well.

Define the red charge coefficient

```
c_l(r) = 1       if r in H_l,
         rho_l  if r in U_l,
         0       otherwise.
```

The core and residual support are disjoint. Solve the polynomial LP

```
minimize Lambda
subject to
    w_l >= 0,
    sum_(l: i in J_l) w_l >= 1                 for every test i,
    sum_l w_l c_l(r) <= Lambda                  for every red r.   (3)
```

Rational upper bounds on the displayed fourth roots, within a constant
factor, may be used as LP coefficients.

**Combining theorem.** Given feasible weights in (3), there is a
polynomial algorithm covering at least `ceil(k/2)` blues at total cost
at most `2 Lambda OPT(k)`. There is also an exact-target guarantee
`Lambda H_k OPT(k)`.

Proof of the density step: fix any solution with red union `S`, cost
`K`, covering at least `q` currently uncredited blues. Fix exactly `q`
of these blues and assign each to one of its selected tests. For each
piece let `q_l` be the number of
these assigned blues whose assigned test belongs to `J_l`. The test
covering constraints imply

```
sum_l w_l q_l >= q.                                      (4)
```

For `q_l>0`, the optimum assigned tests in this piece witness feasibility
of residual target `q_l` within `S intersect U_l`. Also `H_l subset S`.
The local algorithm, together with its core, returns a candidate of cost
at most

```
|H_l| + rho_l |S intersect U_l|
  = sum_(r in S) c_l(r).                                  (5)
```

Summing (5) with weights `w_l`, using only pieces with `q_l>0`, gives at
most `Lambda K`. By (4), some such candidate has cost per credited new
blue at most `Lambda K/q`. The algorithm finds a candidate at least as
good by enumerating all pieces and all feasible integer targets
`t<=q`, running their local algorithms, and choosing minimum actual
cost per credited new blue. Actual marginal union cost can be used in
this comparison; it is no greater than the cost in (5).

Repeat this step on the uncredited blue labels, with residual target
`q=k-c`, where `c` is the number of distinct credited blues, until
`c>=ceil(k/2)`. Extra actual coverage may be ignored. The original
optimum covers at least
`q` uncovered blues. Each iteration credits `g<=q`, so its cost is at
most `Lambda K g/q`. Before the stopping step, `q>k/2`. The total gains,
including the stopping step, are at most `k`, giving cost at most
`2 Lambda K`. Repeating to exact coverage instead gives

```
sum_steps g/q <= H_k.
```

The local algorithm can always be run with the original red costs and
the current blue restriction. We do **not** presume that deleting
previously purchased reds preserves the degree/codegree promise.
Counting full local costs again only overestimates the final union.

The distinct-color proof does not require disjoint blue sets, independent
piece events, or a laminar family of stars. Piece overlaps enter exactly
through (3). Own-test reds are ordinary reds in that LP.

For the partition leaves, every test appears in exactly one piece, so
their weights must be at least one. The resulting certificate is the
maximum accumulated core/tail charge of any original red. Allowing
overlapping additional candidate pieces may lower the LP value. One may
also include the whole instance with any existing exact-target
approximation guarantee; thus a family of extra candidates need never
force an inferior certified bound.

In particular, `Lambda=O(m^(1/3-epsilon))` in (3) is a concrete sufficient
condition for a sub-cube-root constant-coverage oracle. A bound merely on
each individual `rho_l` is insufficient. No universal bound of the
required form on `Lambda` is established here.

## 4. Why the missing overlap bound is substantive

### A proper high-color triple star can leave an arbitrary residual

Start with any singleton-blue precedence instance `J` on `m_J` unit
tests, with feasible target `k`. Add three prerequisite tests `T` to
every informative test. Add `D` new dummy blues, each with a test
requiring a fresh common block of `m_J+4` red tests.

Any solution containing a dummy witness costs more than `m_J+3`.
Executing all original tests and `T` costs at most `m_J+3`. Therefore

```
OPT_new(k) = OPT_J(k)+3.
```

The `T`-star is proper and contains every original color; no prerequisite
is globally common to original and dummy witnesses. Removing `T` from
its star leaves exactly the arbitrary instance `J`. The total number of
tests is `2m_J+D+7`, a constant-factor expansion when `D<=m_J`.

Thus the obstruction is not removed by testing only for globally common
prerequisites. A high distinct-color core need not make its residual
problem algorithmically easier. Nor does contracting a constant-size
core by itself reduce the input parameter by a polynomial factor.

### Disjoint color pieces can share almost their entire red cost

Let `S` be partitioned into `p>=2` groups `U_j`, each with `a` reds.
Block `j` has `B` private colors, each with a unique witness requiring
`S\U_j` and a private marker triple `T_j`. The target is every color.
In the red-blue model without own-test charges, the global cost is

```
pa+3p.
```

The sum of the individually optimal block costs is

```
p(p-1)a+3p.
```

There is no globally common red. Each red in `S` occurs in `p-1`
pieces, exactly the overlap appearing in (3). To realize unit-cost
precedence, give each witness its own red; both displayed costs acquire
the same additive `pB`. Taking `a` sufficiently larger than `B` preserves
the factor of order `p`.

This example is easy if actual unions are considered globally. It is an
obstruction to a proof that assigns budget `K_l` independently to the
pieces and then asserts `sum_l K_l<=K`. Neither partitioning tests nor
partitioning colors justifies that assertion.

### Triple stars need not be laminar

Given arbitrary subsets `Q_j` of the blue colors, create one marker
triple for each `j` and attach it to every witness whose color lies in
`Q_j`. Its triple star has exactly that prescribed color set. Consequently
arbitrary set-system overlap can occur among high-color stars.

## 5. A stronger practical core candidate and its precise guarantee

The arbitrary-representative obstruction in
`core-enumeration-investigation.md` can be repaired on that example by a
computable fourth-order support statistic. Here use that note's
height-two singleton-blue model and apply the filter only to prerequisite
types. Informative tests retain their own unit costs separately; otherwise
their private own-test reds would cause the filter to delete every
witness. Within a prerequisite triple star `T`, set

```
f_T(r)=|{b: some witness for b contains T union {r}}|,
H_tau={r:f_T(r)>=tau}.
```

For each integer threshold `tau`, consider only witnesses whose
prerequisites are contained in `H_tau` and evaluate representatives'
actual marginal union cost, including their own execution costs.

Suppose `g` comparator witnesses of distinct colors in this star have
prerequisite union `S`, `s=|S|`. At least

```
g-s(tau-1)
```

of their colors still have a comparator witness with prerequisites in
`H_tau`. Indeed a removed prerequisite belongs to comparator witnesses
of fewer than `tau` colors; union-bound those losses over `S`. If
additionally every prerequisite type outside `S` has frequency below
`tau`, every retained candidate's prerequisites lie in `S`. Choosing
representatives for `g'` such colors then costs at most `W(S)+g'`.

In the affine-hyperplane example, each shared red of `S` occurs in
witnesses of every color in the star, whereas each private red has
frequency one. Threshold two therefore recovers the shared optimum
witnesses. The general numerical lower bound above can be vacuous even
when this filtering succeeds; it is not a universal guarantee.

These candidates can be added to a core algorithm without losing its
previous guarantee. They go beyond raw triple codegree and specifically
test whether many colors share additional reds. However, arbitrary
outside alternatives can also have large frequency, so no general
sub-cube-root conclusion follows from this filter alone.

## Outcome

Low-codegree residual pieces and a polynomial core decomposition can be
obtained generally. The unresolved theorem is a quantitative bound on
how their red costs can be combined, or a different selection rule that
exploits shared cores beyond the sufficient LP certificate (3). This
isolates an explicit, auditable missing condition; it does not assert
that this particular certificate is necessary for every successful
rounding method.
