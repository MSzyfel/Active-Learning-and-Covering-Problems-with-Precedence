# Global LP approach to decision-tree approximation

This research note records a candidate general-instance improvement derived
from a pair-conditioned relaxation. Independent agent checks found no
specific error in the cost and coverage calculations, but this is a proof
sketch, not a reviewed theorem; novelty has not been established. The
original manuscript has not been changed.

## Candidate result and implications

For unit-cost partial red-blue set cover with `m` available sets, a target
of `k` blue elements, and optimum red cost `K >= 1`, the relaxation and
rounding below appear to give a deterministic polynomial-time
solution covering at least `ceil(k/8)` blues and using

```
O(K m^(1/3))
```

red elements. The implementation guesses `K`, uses the conditional-expectation
procedure below, verifies coverage, and returns the cheapest valid candidate.
The zero-optimum case is handled using all red-free sets. A randomized
implementation can instead amplify independent trials.

The manuscript's closure reduction has one red element per original set.
Thus this would give a general-precedence `(O(m^(1/3)), 8)`
bicriteria approximation for partial precedence cover. By trying all blue
targets, it also gives the corresponding budgeted-coverage guarantee. The
manuscript's existing reductions would then yield deterministic

```
O(m^(1/3) log(2n))
```

approximations for both worst-case and uniform-average decision trees. Here `m` is the number of
tests and `n` the number of hypotheses. This removes the covering-side
logarithms; the power of `m` remains `1/3`. The original manuscript's displayed
general bound is `O(m^(1/3) log^(4/3)(m) log^2(n))` for each objective.

For exact partial cover, repeatedly apply the constant-fraction procedure
to the current uncovered blues and residual quota. An original optimum
still covers at least the residual quota at red cost at most `K`; each
successful call reduces that quota by a constant factor. This yields an
`O(m^(1/3) log(2k))` deterministic exact-target factor. This is separate
from the constant-loss guarantee used in
the decision-tree construction.

Independently of the new LP, the uniform-average reduction appears to admit
a simplification: an `(alpha,beta)` partial-PCSC oracle directly yields
an `O(alpha beta log n)` average-case decision tree, without passing through
min-sum cover. This is explained below.

## A valid polynomial-size relaxation

Let `R_j` and `B_j` denote the red and blue neighbors of set `j`. After
guessing `K`, discard sets with `|R_j| > K`. For each red `p`, set `j`, and
blue `b`, use variables `y_p, x_j, z_b` in `[0,1]`. For each incidence
`b in B_j`, use `a_bj >= 0`; for red pairs `p,r`, use `Y_pr >= 0`.
Require

```
sum_p y_p <= K,                     sum_b z_b = k,
sum_{j:b in B_j} a_bj = z_b,       a_bj <= x_j,
sum_{b in B_j} a_bj <= k x_j,
x_j <= y_p                         for p in R_j,
sum_{j:p in R_j,b in B_j} a_bj <= y_p            for every p,b,
sum_{j:p in R_j} sum_{b in B_j} a_bj <= k y_p  for every p,
x_j <= Y_pr                        for p,r in R_j,
sum_r Y_pr <= K y_p                for every p.
```

These constraints are valid for an integral solution of red cost at most
`K`: choose any `k` covered blues and assign each to one selected set;
let `x`, `y`, and `Y` be indicators of selected sets, covered reds, and
their red pairs. The two load constraints are needed in the rounding
analysis. The LP has polynomial size in the explicit input. A true optimum
survives the individual-set filter and yields a feasible solution for its
correct budget guess.

## Rounding and red cost

Let `T = ceil(m^(1/3))`. Buy all red elements
`p` with `y_p >= 1/T`; their number is at most `KT`. Remove them from red
neighborhoods. Select every set whose remaining red neighborhood is empty.
If these sets cover at least `ceil(k/8)` blues, return them. Otherwise,
the remaining blue elements retain LP mass greater than `7k/8`, since
`z_b <= 1`.

Partition the nonempty residual red neighborhoods into dyadic buckets
`s <= |R'_j| < 2s`, for at most `1 + floor(log_2 K)` scales. For each bucket and each
residual red pivot `p` with `y_p > 0`, independently activate the group
with probability `y_p/s`. Conditional on activation, independently select
each bucket set `j` containing `p` with probability `x_j/y_p`. These are
valid probabilities because `x_j <= y_p` for `p in R_j`.

The log-free cost bound sums heavy *red pairs* across the dyadic scales
before summing over pairs. Let `D_{p,s}` be pivot `p`'s degree in bucket
`s`, and let `theta = K/T`. Call a set in that bucket heavy for
`p` if `x_j/y_p >= theta/s`, and light otherwise.

Fix residual reds `p,r`. If any heavy set at scale `s` contains both,
the pair constraint gives `Y_pr >= x_j >= theta y_p/s`. Thus such scales
must satisfy `s >= theta y_p/Y_pr`. Union-bounding over group activations
and summing the geometric tail gives a contribution of at most
`2Y_pr/theta` for this ordered pair. The sum of `Y_pr` over all ordered
pairs is at most `K sum_p y_p <= K^2`, so expected heavy-red cost is at
most `2K^2/theta`. Skip pivots with `y_p = 0`; they cannot have a neighbor
with positive `x_j`. Pairs with `Y_pr = 0` cannot support a heavy set.

For light sets, the conditional expected projected red cost of a group is
at most `2s D_{p,s} (theta/s) = 2 theta D_{p,s}`. Multiplying by the
activation probability `y_p/s`, and using `y_p < 1/T`, gives

```
E[light red cost]
  <= (2 theta/T) sum_{p,s} D_{p,s}/s
  <= 4 theta m/T,
```

because each set contributes its residual red degree divided by its scale,
which is below two. Hence, using `m <= T^3`,

```
E[total red cost]
  <= KT + 2K^2/theta + 4 theta m/T
  <= 7 K T.
```

If an endpoint makes taking all retained sets already satisfy this bound,
use that solution instead.

## Coverage and simultaneous success

The following random certificates are solely for analysis. Whenever a set
`j` is selected within a pivot group, independently draw a random subset of
`B_j` of size at most `k`, with inclusion probabilities `a_bj/x_j`. Such a
distribution exists because each marginal lies in `[0,1]` and their sum is
at most `k`. Different selected sets and groups use independent draws.
Actual coverage contains the certified blues.

For a fixed blue `b`, the per-red/per-blue load constraint ensures that the
sum of conditional certificate probabilities within a group is at most
one. As the total projected degree of a set in its bucket lies in
`[s,2s)`, summing the independent group opportunities shows that `b` is
certified with probability at least `c z_b`, where
`c = 1 - exp(-(1 - 1/e)) > 0.46`. Consequently, if `Y` counts *distinct*
remaining certified blues, `E[Y] > 0.4k`. The weaker bound `E[Y] > 7k/24`
is convenient for explicit constants.

For a group conditional on activation, let `F` be the number of distinct
certified blues. The total-load constraint gives `E[F] <= k`. Since each
independent certificate subset has size at most `k`, Efron--Stein gives
`Var(F) <= k E[F]`, hence `E[F^2] <= 2k E[F]`. Let `W` be the sum of the
distinct certificate counts over independently activated groups. The
bucket-degree bounds imply `E[W] <= 2k`; independence gives
`E[W^2] <= 8k^2`. Since `Y <= W`, Cauchy--Schwarz gives
`Pr[Y >= k/8] >= 1/288`. Markov's inequality and the red-cost bound give
`Pr[cost > 4032 K T] <= 1/576`. Thus both events hold simultaneously with
probability at least `1/576`. The algorithm observes the actual red cost
and coverage, so independent repetitions can be checked and amplified; it
need not generate the certificates. The integer choice of `T` and rational
LP solutions also avoid irrational sampling probabilities.

## Candidate deterministic rounding

The random argument appears to admit an explicit polynomial-time
conditional-expectation implementation. This part also requires independent
review. Let `Y` be the number of distinct certified remaining blues, `W` the
sum of distinct certified-blue counts over all pivot groups, and
`R = |H| + (number of residual reds reached)`. Thus `R` upper-bounds the
actual red cost. For `k >= 1`, define

```
Phi = Y - W^2/(80k) - k R/(70 K T) - k/8.
```

The previous bounds give `E[Y] > 0.4k`, `E[W^2] <= 8k^2`, and
`E[R] <= 7KT`. Therefore `E[Phi] > 0.075k`. Any outcome with `Phi > 0`
has `Y > k/8`; it also has `R < 1400KT`, because `W >= Y` and
`Y - Y^2/(80k) <= 20k` for every nonnegative `Y`.

For each selected occurrence of set `j`, construct its bounded-size
certificate distribution explicitly. List its blue marginals
`p_b = a_bj/x_j` as consecutive intervals of lengths `p_b` on
`[0,sum_b p_b)`. Draw one uniform offset `U in [0,1)`, and include an
element if its interval contains `U+t` for an integer `t`. Each marginal is
`p_b`, and the selected subset has at most `ceil(sum_b p_b) <= k` elements.
The rational interval endpoints partition `[0,1)` into polynomially many
intervals with constant outcomes, providing a polynomial-support rational
distribution. Skip certificate draws when `x_j=0`.

Expose pivot groups one at a time: first fix whether the group activates,
then, for an active group, fix each incident set occurrence's outcome
(unselected, or selected with one of its certificate subsets). At each step,
choose a positive-probability outcome that maximizes the conditional
expectation of `Phi`. These conditional expectations are polynomial-time
computable: single-red and single-blue miss probabilities use products over
the independent set occurrences and groups; within-group one- and two-blue
miss probabilities give first and second moments of each group count; and
independence of the remaining groups gives the cross terms of `E[W^2]`.
Already fixed outcomes are treated as constants. Thus the final `Phi` is
positive. A feasible result for the correct guessed `K` is retained; the
returned cover contains only original selected sets, not the accounting
set `H`.

## Direct partial cover to uniform-average decision trees

Consider the sepcover `S` of an optimal uniform-average decision tree, using
the definition in `sections/approximating_learning.tex`. Every test node on
that path is reached by more than `n/2` hypotheses. Indeed, every strict
prefix fails the separator stopping condition, so it has a component with
more than `n/2` leaves. That component must contain the endpoint of `S`:
otherwise it would remain a too-large component even after deleting the
entire sepcover path. Therefore

```
OPT_average >= COST_average(S) > (n/2) |S|.
```

The proof of `lemma:cover_sep_worst_case` uses only the sepcover property,
not worst-case optimality. Applied to this average-optimal tree, it shows
that the induced partial-PCSC optimum is at most `|S|`. An
`(alpha,beta)` PCSC oracle returns a family of at most `alpha |S|` sets.
Topologically order it and use the existing decision-tree procedure. Its
current path contributes at most

```
n alpha |S| <= 2 alpha OPT_average.
```

The existing average-case induction applies: recursive subinstances are
disjoint, their optimal unnormalized total costs sum to at most the parent
optimum, and every recursive group has size at most
`(1-1/(5 beta)) n`. This yields
`O(alpha log(n)/log(5 beta/(5 beta-1))) = O(alpha beta log n)`.
The argument is for the manuscript's uniform-hypothesis objective; it
does not claim an arbitrary-distribution result. Repeated previously
performed tests can be removed as in the manuscript.

## Separate observation: budgeted cover to min-sum cover

The manuscript's `O(alpha beta^3)` transfer from budgeted cover to
min-sum cover also appears improvable to `O(alpha beta)` by changing the
phase schedule. For each budget `2^i`, call the `(alpha,beta)` budgeted
oracle `t = ceil(beta ln 4)` times on the residual universe and append
each returned ideal in topological order, omitting sets already appended.
Cap a budget exceeding `m` at `m`. The original optimum prefix of that
budget remains a feasible comparator on every residual instance.

Let `q_i` be the number of uncovered elements after phase `i`, let `q_i*`
be the number not covered by the original optimum's prefix of length
`min(2^i, |C*|)`, and put `a=(1-1/beta)^t <= 1/4`. Repeated calls give

```
q_i <= a q_(i-1) + (1-a) q_i*.
```

If `C*` is the optimum min-sum cost and `ell=ceil(log_2 |C*|)`, dyadic
charging gives

```
sum_{i=0}^{ell-1} 2^i q_i* <= 2 C* - n,
sum_{i=0}^{ell} 2^i q_(i-1) <= 6 C*.
```

Since phase `i` appends at most `alpha t 2^i` sets, its latency is at most
that length times `q_(i-1)`. The accumulated latency is therefore at
most `6 alpha ceil(beta ln 4) C*`. By the first phase whose budget reaches
the optimum sequence length, coverage is at least the original target
divided by `beta`, so stopping at the required coverage is safe. This
observation does not improve the fixed-beta decision-tree asymptotic above;
the direct uniform-average reduction already bypasses min-sum cover.

## Open checks and limitations

- The relaxation and the deterministic proof need a complete independent
  line-by-line review and a literature check before being claimed as new.
- A subsequent explicit construction shows an `Omega(m^(1/3))` gap for
  this LP even on binary decision-tree separator instances with target
  `|U_xi|/4` and any fixed coverage fraction; see
  `decision-tree-cover-gap.md`. This is a limitation of this relaxation,
  not a lower bound for all algorithms or for decision trees.
- A positive-semidefinite strengthening with conditioned witness quotas
  rules out that low-intersection construction; its analysis and the
  unresolved general rounding problem are in `sdp-gap-investigation.md`.
- A fixed fraction of target coverage is essential to the stated partial
  rounding. Repeated residual calls can reach exact coverage with an
  additional logarithmic factor; no exact `O(m^(1/3))` result is claimed.
- This does not prove an exponent below `1/3`. The present red-cost balance
  is `T + sqrt(m/T)`.
- The reduction to decision trees relies on the manuscript's stated
  covering-to-tree theorems. Deterministic rounding avoids failure-probability
  accounting; the randomized variant needs amplification across all calls.

Background: https://arxiv.org/html/2302.00213, especially Section 3 and
Appendix A.
