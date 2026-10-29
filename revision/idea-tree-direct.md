# Direct-tree refinements and a barrier for fixed closure seeds

This note continues `direct-tree-ideas.md`. It gives a modest refinement
of its positive bound and two precise obstructions to proposed shortcuts.
It does **not** establish a general approximation below `m^(1/3)`, and
none of the obstructions is a computational hardness result. No manuscript
changes are proposed here.

Write `K=OPT_W` and `L=OPT_A`, with the latter the unnormalized uniform
sum. Tests have unit cost. A closure contains its endpoint.

## Count distinct informative partitions, rather than all successors

For the current hypothesis set `H`, two tests are equivalent when their
partitions of `H` are equal, regardless of the labels attached to replies.
Ignore the trivial one-block partition. Define

```
delta_H(p) = number of distinct nontrivial partitions induced on H
             by tests t with p <= t.
```

These numbers and partition classes can be computed in polynomial time
from the explicit test table. If `p<=q`, then
`delta_H(p)>=delta_H(q)`. Consequently

```
A_D(H) = {p : delta_H(p)>D}
```

is a prerequisite ideal. The following bound improves the successor-count
bound in `direct-tree-ideas.md`, sometimes by a large factor:

```
cost_W <= |A_D(H)| + C D log(2n) K,
cost_A <= n |A_D(H)| + C D log(2n) L.                 (1)
```

Here and below `D>=1` is integral. As in the previous note, run the
polynomially many choices of `D` and retain the best resulting tree.

To prove (1), execute `A=A_D(H)` first. On each resulting hypothesis
class give a remaining test `t` surrogate cost
`c_A(t)=|downarrow(t) minus A|`, and use a logarithmic approximation for
ordinary weighted decision trees. Such an approximation is supplied by
the private-chain construction and the manuscript's inforest algorithm,
exactly as explained in `direct-tree-ideas.md`.

Restrict an original optimal tree to one resulting class. For the
unconstrained weighted comparator, delete nodes whose answers are
already determined, including all tests in `A`. This deletion is only
for the comparator: prerequisite execution is accounted for in `c_A`.
No retained path contains two tests inducing the same partition on the
original `H`: after the first test, the answer to the second is known.
For a residual prerequisite `p`, at most `delta_H(p)<=D` retained tests
on this path can require `p`. Every such `p` belongs to the corresponding
original feasible path. Double counting therefore gives

```
sum_(retained tests t on the path) c_A(t)
   <= D (length of the original path).
```

Implement a requested test by executing all missing real predecessors,
ignoring extra replies if necessary. Its real cost is at most its
surrogate cost. The worst-case bound follows; for average cost, sum the
comparator inequality over the disjoint classes produced by `A`.

For example, suppose arbitrarily many disjoint prerequisite chains lead
to endpoints that all induce the same useful partition. The old global
successor degree can be as large as a chain, whereas `delta_H(p)<=1`
everywhere. Formula (1) gives the ordinary logarithmic guarantee without
prepaying all chains.

There is also an exact optimality statement about these threshold
ideals. For every ideal `A` and `p notin A`, no successor of `p` belongs
to `A`. Thus the distinct-partition successor count of a residual `p`
is still exactly `delta_H(p)`. Any ideal that leaves this count at most
`D` must contain `A_D(H)`, and `A_D(H)` itself suffices. It is the unique
smallest such ideal. Searching for a different ideal cannot improve the
certificate (1) with the same global residual-degree criterion. This
does not exclude stronger analyses that use which alternatives an
optimal comparator actually selects.

## A cube-root obstruction to threshold ideals plus fixed closure seeds

Consider the following concrete family of direct algorithms. It may
choose any threshold ideal above, execute it, and then seed the run by
executing the union of the closures of at most `t` arbitrary tests, for
any fixed integer `t`. It subsequently chooses an informative test with
minimum marginal closure cost per newly eliminated color. It may
enumerate all such seed choices and thresholds and select its best
output. This also includes ordinary marginal-closure greedy with no
seeds. The example below gives this entire family an `Omega(m^(1/3))`
ratio for both objectives.

Let `s>t+3` be a prime power. There are `k=s^2` colors, indexed by
`(a,b) in F_s^2`, and `s` disjoint copies of the affine plane `F_s^2`.
Each point in each copy is an uninformative prerequisite test. In copy
`j`, color `(a,b)` has a good informative test requiring exactly the
`s` points on the nonvertical line

```
{(x,a x+b): x in F_s}.
```

Every color also has one bad informative test with a fresh private set
of `s-t-2` prerequisite tests. Its complete closure has size `s-t-1`.
All informative tests are maximal; all prerequisites are minimal. Use
two hypotheses `c^0,c^1` for each color `c`. Every test of color `c`
has replies `{c^0}`, `{c^1}`, and all other hypotheses. Hence every
normalized tree has one internal path, and every color must be tested.

The number of tests is exactly

```
m = s^3                     good point prerequisites
    + s^3                   good informative tests
    + s^2(s-t-2)            private bad prerequisites
    + s^2                   bad informative tests
  = 3s^3-(t+1)s^2.
```

Executing every point in any one copy, followed by that copy's good
test for each color, costs `2s^2`. Every feasible full solution executes
at least `s^2` informative tests. Therefore

```
OPT_W = Theta(s^2).
```

There are `n=2s^2` hypotheses. The same solution has total average cost
at most

```
2s^2 * s^2 + 2 sum_(i=1)^(s^2) i = 3s^4+s^2.
```

Every solution's informative tests alone contribute at least
`2 sum_(i=1)^(s^2) i = s^4+s^2`. Thus

```
OPT_A = Theta(s^4).
```

Each good point is required by `s` tests of distinct colors, one for
each slope. Its informative-partition diversity is `s`. Each private
bad point and each informative endpoint has diversity one. Consequently
every threshold `1<=D<s` buys **all `s^3` good points** before any
hypothesis is identified. This already costs `s^3` in the worst case
and `2s^5` in total average cost. For `D>=s`, the threshold ideal is
empty. The original all-successor-count thresholds have the same
dichotomy, with their transition shifted by one and a possible extra
case that also purchases all private prerequisites.

It remains to analyze any choice of at most `t` initial closures when
the threshold ideal is empty. Such seeds identify at most `t` colors.
Consider a good test of a remaining color. Its line intersects each
seeded good line in its own copy in at most one point; lines in other
copies and private bad closures give no overlap. A seeded single point
can also save at most one point. Since the color remains uncovered,
the identical good line was not seeded. Thus at least `s-t` of its
predecessors are still missing, and its marginal closure cost is at
least `s-t+1`.

Every remaining bad test has marginal closure cost at most `s-t-1`.
Its roots are private, and executing it has no effect on any good
test's prerequisites. All informative tests eliminate exactly one
remaining color. Therefore greedy strictly prefers bad tests at every
subsequent step, independently of tie breaking. After excluding the at
most `t` colors initially identified and the at most `t` additional bad
closures that might have been partly seeded, at least `s^2-2t` bad
tests have their full `s-t-1` marginal cost. In particular, its worst
cost is `Omega(s^3)`.

For the average bound, the same full-cost bad tests occur along the
single internal path. Even placing all exceptions first, their
contribution is at least

```
2 (s-t-1) sum_(i=1)^(s^2-2t) i = Omega(s^5).
```

Both approximation ratios are therefore `Omega(s)=Omega(m^(1/3))`.
The conclusion holds for every fixed seed budget `t`, including
enumerating all `m^t` choices. The fixed `t` affects only the constant
offset in the bad closure size.

This obstruction does not refute arbitrary useful-ideal algorithms:
buying all points of one copy is optimal up to a constant. It shows why
global degree thresholds and a fixed number of immediately executable
closures do not automatically find that useful ideal. The incidence
components in this particular example reveal it directly, so the
example is not a hardness reduction.

Disconnectedness is inessential to the obstruction. Number the copies
cyclically, and add to good test `(j,a,b)` the prerequisite point
`(a,a^2+b+1)` in copy `j+1`. This maps colors bijectively to points, and
the added point does not lie on the line of the same color in its own
copy. Every good point now has exactly `s+1` distinct informative
successor partitions. Good predecessor sets still intersect pairwise in
at most one point: sets from the same copy intersect only through their
lines, and sets from consecutive copies can intersect only through the
one extra point. Here `s>=4` avoids a two-copy cycle. Thus the threshold
dichotomy and fixed-seed analysis persist, with a shifted threshold and
one larger good closure. Executing all points in two consecutive copies
and the good endpoints in the first costs `3s^2`, so both optimal orders
remain unchanged. The total number of tests is unchanged, and the good
test/prerequisite incidence graph is now connected. This modification
still makes no hardness claim.

## Small global average optimum is not a general easy regime

There is a useful difference between worst-case and normalized-average
parameters. The worst-case small-`K` bound in `direct-tree-ideas.md` is
valid. A comparably easy small-mean regime would already contain the
whole uniform-average problem when arbitrary reply counts are allowed.

Take any nontrivial instance `I` with `n_0` hypotheses, `m_0` tests,
and unknown total average optimum `L_0`. Add `N` dummy hypotheses and
one new test `r`. Its replies are the complete original hypothesis
set and one singleton for every dummy. Make `r` a predecessor of every
original test; extend original tests arbitrarily to dummy hypotheses.
The new root must be `r`, after which only the original branch needs
more work. Therefore, exactly,

```
OPT_A(I_N) = n_0+N+L_0,
a(I_N)    = 1+L_0/(n_0+N).
```

Enumerate powers of two `N` up to `2n_0m_0`. One choice satisfies
`L_0<=N<2L_0`, since `n_0<=L_0<=n_0m_0`. For that choice,

```
a(I_N)<=2,
OPT_A(I_N)<4L_0.
```

Run any proposed algorithm guaranteed on instances with normalized
average optimum at most two on all these polynomial-size instances.
Extract the original branch from every returned tree and select its
cheapest extracted solution. An `alpha` guarantee on the small-mean
instances yields a `4 alpha` guarantee on the original instance, with
only one additional test and polynomially many additional hypotheses.
No knowledge of `L_0` is required.

Thus a general `O(a polylog(m,n))` approximation based solely on the
global normalized average `a` would imply a polylogarithmic
approximation on all uniform-average instances. This is not a proof
that such an algorithm cannot exist. It explains why a global small-
`a` claim cannot be justified merely by deleting the second moment
from the surrogate analysis. The reduction uses an unrestricted-output
root; it makes no constant-`a` claim for binary tests.

## What remains

The positive bound (1) removes useless and duplicate successor tests
from the charge, and its threshold ideals are optimal for that precise
certificate. The affine-plane example still attains the cube-root
barrier for threshold prepayment combined with any fixed number of
closure seeds and one-test marginal greedy. Progress beyond it needs a
way to find or assemble an informative prerequisite ideal based on
shared residual unions. A multi-phase rule that can do this on arbitrary
instances remains unproved.
