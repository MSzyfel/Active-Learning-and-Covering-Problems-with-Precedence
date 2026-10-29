# A CSP-based polynomial gap for the strengthened precedence-cover SDP

This note gives a reduction from the **specific random-CSP construction**
of Bhaskara, Charikar, Guruswami, Vijayaraghavan, and Zhou (BCGVZ), rather
than from an arbitrary Densest k-Subgraph integrality gap. It produces a
polynomial gap with a constant blue target fraction, includes the cost of
every witness test, and satisfies conditioned cost and assignment quotas.
The exponent obtained below approaches `2/53`, not `1/3`.

## Source facts and notation

Source: [BCGVZ, Polynomial integrality gaps for strong SDP relaxations of
Densest k-subgraph](https://users.cs.utah.edu/~bhaskara/files/dksgaps.pdf),
full version, Section 4, especially Theorem 4.2, Observation 4.3, Lemmas
4.6, 4.9, and 4.12. The [published paper](https://doi.org/10.1137/1.9781611973099.34)
has different numbering.

Their construction supplies a random CSP with `n` variables, alphabet
size `q`, arity `h`, and `M=beta*n` constraints. Each constraint has
`q^t` satisfying assignments. Its label graph has left vertices
`(i,alpha)` for satisfying constraint assignments and right vertices
`(j,a,c)`, where `a` is a variable label and `c in [beta]` is a copy.
Every left vertex has exactly `beta*h` neighbors. The source supplies:

1. Perfect-completeness Lasserre moments for the CSP, locally choosing
   one label per variable and one satisfying assignment per constraint.
2. With high probability, every subgraph on at most `2M` left and `2M`
   right vertices has at most `17*beta*M*h/q` edges (Lemma 4.12).

We use both properties simultaneously; their probability tends to one.
The rectangular statement in item 2, rather than only the usual
`2M`-total-vertices DkS soundness statement, is useful below.

## Precedence-cover instance

There is one blue element `b_i` per CSP constraint, so the blue universe
has size `M`. Create the following unit-cost tests:

* For every right label-graph vertex `(j,a,c)`, create a prerequisite test
  `P_(j,a,c)` with no predecessors and no blue coverage.
* For every left vertex `(i,alpha)`, create a witness test `W_(i,alpha)`
  covering only `b_i`. Its immediate predecessors are exactly the
  `beta*h` label tests adjacent to `(i,alpha)`.

The precedence DAG has height two. Its number of tests is

```
m_tests = M*q^t + beta*n*q = M*(q^t+q).
```

Every witness test has its own unit cost. Thus the cost of a closed
solution is precisely the number of selected vertices on the two sides
of the source label graph. There are no zero-cost tests or omitted
witness-own red elements.

## Fractional solution and all relevant consistency constraints

Put `k=M/4`; the parameters below make `M` divisible by four. Independently
choose a random uniform `k`-subset `J` of the `M` constraints,
and let `H_i` be its indicator. Take the product of this actual
distribution and the source CSP pseudo-distribution. Interpret the test
indicators by

```
Y_(P_(j,a,c)) = indicator[X_j=a],
Y_(W_(i,alpha)) = H_i * indicator[X restricted to T_i equals alpha].
```

All copies of a variable-label test use the same indicator. Conditional
on any fixed `J`, a set of target indicators maps to the conjunction of
its local CSP assignments, or to zero if it contains a witness outside
`J`. Inconsistent local assignments also have moment zero. Otherwise use
the corresponding source CSP moment. For each `J`, the moment matrix is
a submatrix of a source Gram matrix with repeated indices and zero
vectors. Averaging over `J` preserves positive semidefiniteness, Boolean
consistency, and nonnegative conjunction moments. Thus the product
construction does not assume an actual global distribution for the CSP.

The perfect source solution gives the polynomial identities

```
sum_(alpha satisfying constraint i) Y_(W_(i,alpha)) = H_i,
sum_a Y_(P_(j,a,c)) = 1.
```

Consequently, within the available moment degree,

```
sum_all_tests Y_test = sum_i H_i + beta*n = k+M.
```

This is an identity under conditioning, not just an equality of first
moments. In particular, setting the guessed cost budget to `B=M+k=5M/4`
gives, for each red/test indicator `Y_r`,

```
sum_s E_tilde[Y_r Y_s] = B E_tilde[Y_r].
```

If prerequisite `p` belongs to witness `w`, its local assignment is a
restriction of the witness assignment, so

```
Y_p Y_w = Y_w.
```

For any two tests `r,s` in the closure of `w`, the moment of their
conjunction dominates the witness moment. Thus the original closure-pair
inequality `x_w <= Y_rs` also holds. Take each closure-set indicator
`x_j` to equal its own-test indicator `Y_j`.

Set the blue and assignment indicators to

```
Z_i = H_i;
Q_(i,w) = Y_w if w is a witness for i, and 0 otherwise.
```

Then each selected blue has exactly one assignment witness, all
assignment domination constraints hold, and

```
sum_(i,w) Q_(i,w) = k
```

holds under every available conditioning. In particular, the conditioned
witness quota from `sdp-gap-investigation.md` is satisfied. There are also
the required per-blue and total assignment-load inequalities: for each
red `r`, the load from a fixed blue is at most `Y_r`, and the total load
is at most `k Y_r`. These follow by multiplying the per-blue exact-one
identity by `Y_r` and using prerequisite consistency. A set witnesses
only its own blue, so its per-set assignment-load inequalities hold too.

In first moments every blue has value `z_i=1/4`. The relaxation has
feasible cost `M+k=5M/4` for target exactly one quarter of the entire blue
universe. The analogous construction with `H_i=1` for all `i` has cost
`2M` for full coverage. Each witness closure has size `beta*h+1<=B` for
the parameters below, so the original individual-set size filter removes
none of these witness tests.

This directly verifies the degree-two PSD strengthening together with
the original pair-row budgets and closure-pair constraints.

### Scope of the higher-level claim

The source displays a vector formulation; it does not separately list
every complement-conditioned inequality or every arbitrary polynomial
localizing matrix. Thus that terminology alone is not the justification
for a full localizing-matrix claim here. The necessary additional
argument for this target encoding is as follows.

The categorical CSP Gram matrix defines a positive pseudoexpectation on
label-indicator monomials: inconsistent label assignments have value
zero, and consistent ones use the source moment. Singleton label vectors
sum to the empty vector: source categorical orthogonality, singleton
normalization, and the empty-vector inner-product identity used in
Observation 4.10 give this by expanding the squared norm of their sum
minus the empty vector. Satisfying constraint-assignment vectors do
likewise (Observation 4.3). Taking
inner products with another source vector proves these identities under
conditioning. Linear combinations also allow complements and arbitrary
polynomial multipliers, provided the required supports fit within the
available source vectors.

Fix `J` first; averaging can be done afterwards. Each target indicator
is a Boolean local event on at most `h` CSP variables. Its complement is
also Boolean. If `p` precedes `w`, the slack `Y_p-Y_w` is idempotent
modulo `Y_p Y_w=Y_w`. Similarly, for two closure reds `r,s`,
`Y_r Y_s-Y_w` is idempotent. For any such slack `D` and polynomial `g`,

```
E_tilde[g^2 D] = E_tilde[(g D)^2] >= 0.
```

The equality uses the local Boolean identities and the inequality uses
the source Gram matrix. Products of test, witness, or blue indicators
and their complements are handled in the same way. The load slacks
decompose into sums of these nonnegative Boolean products. For example,
with `I_r` the assignment witnesses incident to red `r`,

```
k Y_r - sum_(w in I_r) Q_w
  = sum_(w not in I_r) Y_r Q_w,
```

using the exact assignment quota and `Y_r Q_w=Q_w` for incident witnesses.
For a fixed blue `i`, the analogous identity is

```
Y_r - sum_(w in I_r, w witnesses i) Q_w
  = Y_r(1-Z_i) + sum_(w not in I_r, w witnesses i) Y_r Q_w.
```

The cost and quota slacks are zero identities. This verifies arbitrary
squared-polynomial localizers for the standard Boolean formulation of
the displayed cover constraints, in addition to positive-monomial
conditioning.

If the source has vectors on at most `r` CSP variables, reserving, for
example, target level `floor(r/(4h))-4` keeps the entire support in each
multiplied identity within `r` and leaves the needed Gram vectors
available. Therefore the full Boolean moment/localizing formulation
also transfers with an `O(h)` level loss. This argument concerns the
explicit test, blue, assignment, closure, and budget encoding here; it
is not a claim about arbitrary unrelated SDP formulations.

## Integral soundness, including a constant coverage loss

Suppose a closed integral solution covers `s` different blues. Retain one
witness for each of those blues; let `A` be these `s` left vertices and
let `R_A` be all their right neighbors. Then `s<=M`, and all vertices of
`R_A` must be bought. There are exactly `s*beta*h` edges from `A` to
`R_A`.

Partition `R_A` into `ell=ceil(|R_A|/(2M))` blocks, each of size at most
`2M`. The same left set `A` has at most `M` vertices, so source Lemma
4.12 applies to `A` and every block. Hence

```
s*beta*h <= ell * (17*beta*M*h/q),
ell >= s*q/(17M),
|R_A| >= 2M * (s*q/(17M) - 1).
```

The last displayed weak inequality follows from
`ceil(u)<=u+1`; using a strict inequality there would only improve it.
It suffices even if the right side is initially negative.

For every fixed `delta>0`, a solution covering at least
`delta*k=delta*M/4` blues has `s>=delta*M/4`.
For sufficiently large `q`, the displayed bound implies

```
cost >= |R_A| = Omega_delta(M*q).
```

The relaxation budget is `5M/4`, so the constant-fraction gap is
`Omega_delta(q)`. Partitioning only the right side is important: a
partition of both sides would unnecessarily lose a square root.

## Explicit exponent accounting

Here is a conservative parameter choice obtained by substituting into
the source bounds. Let `q` run through sufficiently large prime powers
and fix any constant `gamma>0`. Choose

```
h = q^2 - 1,
t = 5,
beta = ceil(40*q^7*log(q)/h),
n = 4*ceil(q^(33/2 + gamma)/4),
M = beta*n.
```

The distance-four code from source Lemma 4.6 has codimension five, so its
dual predicate has `q^5` satisfying assignments. The hypotheses
`h<sqrt(n)`, `h>q^2/2`, and `t<=10` hold. Rounding `beta` upwards preserves
the soundness hypothesis and changes the completeness bounds by only a
constant factor.

The source completeness theorem, followed by local substitution and a
constant factor reserve in levels, permits

```
R = Omega(n / (beta * h^(23/4)))
  = Omega(q^gamma / log(q))
```

target hierarchy levels. Meanwhile

```
m_tests = M*(q^5+q)
        = Theta(q^(53/2+gamma)*log(q)).
```

Therefore the gap is

```
Omega_delta(q)
  = m_tests^(1/(53/2+gamma) - o(1)),
```

and the number of available levels is
`m_tests^(gamma/(53/2+gamma)-o(1))`. Choosing `gamma` sufficiently small
in terms of `epsilon` gives, for every fixed `0<epsilon<2/53`, a gap
`Omega_delta(m_tests^(2/53-epsilon))` surviving a positive polynomial
number of hierarchy levels, conventionally expressible as
`m_tests^Omega(epsilon)` after choosing `gamma=Theta(epsilon)`.

For example, `gamma=1` gives exponents approaching `2/55` for both the
gap and available levels; this is an easy conservative specialization.

## Exact realization by the decision-tree map xi

Take the hypothesis set to be the `M` constraint indices. Every
prerequisite test has the single reply consisting of all hypotheses.
Give every witness test `W_(i,alpha)` the binary partition

```
{i},        [M] minus {i}.
```

Keep the same precedence relation. Every hypothesis can be separated
from every other hypothesis because every constraint has satisfying
local assignments and therefore has witness tests. For `M>4`, the large
reply has size `M-1>3M/4`. The manuscript's map in
`sections/approximating_learning.tex` consequently gives

```
xi(P_(j,a,c)) = empty set,
xi(W_(i,alpha)) = {i},
U_xi = [M].
```

Thus the separator oracle sees precisely the constructed cover instance
with target `|U_xi|/4=M/4`. All informative tests are binary; prerequisite
tests are uninformative. Identical binary partitions for different
assignments remain different indexed tests with different predecessors,
as allowed in the manuscript.

The actual decision-tree optima on this realization can also be
estimated. The path that repeatedly takes the nonsingleton reply must
separate `M-1` colors, so its prerequisite cost is `Omega(Mq)` by the
same soundness argument. Buying all `Mq` prerequisite tests and then
using singleton witness tests gives the matching upper bound. Thus
`OPT_worst=Theta(Mq)`. Before half the colors have left this path, at
least `M/2` hypotheses share its `Omega(Mq)` cost. Consequently the
uniform sum-of-depths objective is `Theta(M^2 q)`. These observations do
not by themselves specify a decision-tree SDP or its integrality gap.

## Interpretation

This is an unconditional existence result for integrality-gap instances,
using probabilistic source constructions. It is not an approximation
hardness theorem, a lower bound for arbitrary decision-tree algorithms,
or a gap of exponent `1/3`.
It shows that the conditioned-quota PSD strengthening does not have a
constant or polylogarithmic gap in general, even on height-two precedence
instances with a target equal to one quarter of the universe. The
polynomial-graph obstruction can be eliminated while this different
CSP-based obstruction survives.

The reduction is stated here as a derivation from the cited source's
construction and lemmas; the source does not itself state this
precedence-cover corollary.
