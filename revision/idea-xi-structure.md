# Xi structure: an exact cover core and a binary reduction

This note investigates whether the fact that the separator sets arise from
decision-tree partitions gives additional structure usable below exponent
`1/3`. It proves a structural obstruction, including a constant-factor
reduction for binary tests and both tree objectives. It does not prove a
computational lower bound at exponent `1/3`, and it does not provide a
general approximation below that exponent.

The obstruction is broader than the finite-field singleton example in
`decision-tree-cover-gap.md`: arbitrary overlapping small sets and arbitrary
precedence orders occur exactly as xi instances, even when every decision
tree has a single internal path. For singleton-blue covering, restricting
every test to two replies still retains the full covering problem with
only a factor-two increase in the number of tests.

## 1. Exact realization of arbitrary small-set systems

Let `U` have size `N`, and let `(S_t : t in T)` be an indexed family whose
union is `U`, with an arbitrary precedence partial order on `T`. Assume

```
|S_t| < N/4                         for every t.
```

Empty sets and repeated sets are allowed. Form the hypotheses
`H = U x {0,1}`. For each `t`, use one test with the following replies:

```
{(u,i)}                            for u in S_t and i in {0,1},
(U minus S_t) x {0,1}.
```

Omit empty replies, and retain exactly the original precedence order.
The complement reply has size `2(N-|S_t|)>3|H|/4`; each singleton reply
has size at most `3|H|/4`. Thus

```
xi(t) = S_t x {0,1},                U_xi = H.
```

The instance is distinguishable because every `u` is covered somewhere.
For every precedence-closed family `A`, simultaneously,

```
|A| is unchanged,
|union_(t in A) xi(t)| = 2 |union_(t in A) S_t|.
```

For every precedence-closed sequence, all coverage times, including the
truncated times of uncovered elements, are duplicated. Consequently the
root xi problem with target `|U_xi|/4` is exactly the original partial
cover problem with target `N/4`; the cardinality cost is unchanged and
the min-sum cost is multiplied by two. There is no coverage loss and no
increase in the number `m=|T|` of tests.

This realizes an entire set system at once, not merely one arbitrary
small subset. In particular, overlapping small xi sets need not be
laminar, low-frequency, linear, or governed by any special incidence
property. Their precedence order has no further restriction.

The strict inequality on set size is necessary for this literal xi
identity: if `|S_t|=N/4`, the complement reply has size exactly
`3|H|/4`, so xi contains all of `H`. Such a test is already a valid
constant-fraction separator after its predecessors have been executed.

## 2. Full tree optimization is still ordinary covering here

Every test in the construction has at most one nonsingleton reply.
After pruning unreachable branches and stopping at identified hypotheses,
every decision tree therefore has a single path of internal nodes.
Let `sigma` be its test sequence. The pair `(u,0),(u,1)` is
indistinguishable until some test covering `u` has been executed, so
`sigma` covers all of `U`. Conversely, every feasible full-cover sequence
gives such a tree. Precisely,

```
tree worst cost       = |sigma|,
tree total mean cost  = 2 sum_(u in U) tau_sigma(u).
```

The phrase "total mean cost" denotes the manuscript's sum over all
hypotheses. This is the full-cover embedding already used in
`sections/hardness.tex`; the extra observation here is that, under the
small-set hypothesis, its root xi instance is also exactly the desired
partial-cover instance.

It follows that a comparison against the full optimal tree, rather than
only its separator prefix, does not introduce an extra structural promise
on this family. The optimal tree itself is an optimal covering sequence.
The same conclusion applies to both objectives, with their correct
cardinality and latency comparisons.

## 3. All symmetric partition potentials collapse to coverage

After any sequence prefix covering `r` elements of `U`, the partition
induced by its complete reply transcript consists of `2r` singleton
blocks and one block of size `2(N-r)`. Omit the latter if it is empty.

Thus **every potential invariant under permutation of the hypotheses and
depending only on the current partition** is a scalar function of `r` on
this family. This includes separated-pair count, Shannon entropy, Renyi
entropy, and any sum of a fixed function of block sizes. For example,

```
separated pairs = C(2N,2) - C(2(N-r),2),

Shannon entropy = log(2N) - ((N-r)/N) log(2(N-r)),
```

where the last summand is zero at `r=N`. Therefore optimizing such a
potential cannot claim an advantage solely from simultaneous separation
of many pairs or from the shape of the induced partition: in this
subfamily the same progress is exactly ordinary coverage. This statement
does not rule out a stronger algorithm for the resulting coverage problem.

## 4. Binary tests retain the full singleton-blue problem

Here is a reduction avoiding the multi-reply tests in Sections 1--3.
Start with an arbitrary full precedence-cover instance on `N>=3` colors,
where every indexed source test covers either no color or one color.
All colors occur in at least one test. This includes the shared-
prerequisite, many-alternatives-per-color problem in the other notes.

Replace each source test `t` by a chain

```
t^0 < t^1.
```

For each strict original relation `s<t`, impose `s^1<t^0`. If `t`
covers color `u`, the binary test `t^i` has replies

```
{(u,i)},             H minus {(u,i)},       H=U x {0,1}.
```

If `t` covers nothing, both copies are uninformative. Uninformative tests
have one nonempty reply, which is allowed by the binary-at-most-two-reply
convention. The construction has exactly `2m` tests and `2N` hypotheses.
Its xi sets are empty or singletons. The source partial order can be
arbitrary; the construction does not claim to preserve its height.

Let `K` and `L` be respectively the source full-cover cardinality optimum
and full-cover min-sum optimum. Let `W` and `A` be the binary tree's worst
and total-average optima. Then

```
K <= W <= 2K,
2L <= A <= 4L.
```

**Upper bounds.** Expand any source sequence by replacing each occurrence
of `t` with `t^0,t^1`. This is precedence-feasible. If source color `u`
is first covered at position `tau(u)`, the two hypotheses have depths at
most `2tau(u)-1` and `2tau(u)`, respectively. Stop once identification is
possible. A sequence of length `K` gives worst cost at most `2K`; a
sequence of latency `L` gives total cost at most `4L`.

**Lower bounds and solution extraction.** Normalize any resulting binary
tree by pruning unreachable branches, deleting repeated tests on a path,
and stopping at identification. Every informative test peels off just
one singleton, so its internal nodes form a single spine. Project that
spine onto the first copies `t^0`, keeping their order and replacing each
by its source label `t`. Call this projected sequence `pi`.

The projected sequence is precedence-feasible: before `t^0` the spine
already contains `s^1`, and therefore `s^0`, for every original
predecessor `s` of `t`. It covers every color. Otherwise both hypotheses
of a missing color would have identical replies throughout the spine
and could not both be identified.

The sequence length is at most the binary spine length, proving the
worst-case lower bound. For the latency bound, let `p_u` be the position
of the first source test covering `u` in `pi`. Its corresponding first
copy occurs on the binary spine at some position `d_u>=p_u`. Before
that copy, neither hypothesis of color `u` can have been separated:
no earlier first copy covering `u` has occurred, and a second copy
requires its own first copy. Hence both hypothesis depths are at least
`d_u`, and

```
2 sum_u p_u <= sum_u [depth(u,0)+depth(u,1)].
```

This proves `L(pi)<=A(tree)/2` and the stated optimum lower bound.

Consequently an `alpha(2m,2N)` approximation for either binary tree
objective gives a `2 alpha(2m,2N)` approximation for the corresponding
full singleton-blue cover objective. In particular, a general factor
`O(m^gamma polylog(m,N))` transfers with the same exponent `gamma`.
The reduction uses full solutions and introduces no bicriteria loss.

## 5. What remains open

These statements reject a structural shortcut, not the desired theorem.
Xi's small-set form, the existence of an optimal separator path, many
simultaneously separated pairs, and even binary tests with only one
internal tree path do not remove the shared-prerequisite colored-cover
core. A sub-`1/3` tree algorithm may still exist, but on these instances
it must yield new progress on that core rather than rely on adaptivity
or a general restriction of xi incidences.

The additive prerequisite-purchase bounds in `direct-tree-ideas.md`
remain useful on favorable instances. The reductions above do not
invalidate them, nor do they prove that every favorable structural
parameter must be large. They only show why those parameter bounds
cannot be completed by a universal extra promise coming from the
decision-tree interpretation itself.
