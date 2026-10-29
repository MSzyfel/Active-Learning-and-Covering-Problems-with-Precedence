# Higher-order moments: a certified escape from the covariance gap

This research note establishes a fixed-level obstruction to extending the
particular near-cube-root gap in `sdp-strong-gap.md`. It does **not** establish
a general approximation exponent below `1/3`. The manuscript is unchanged.

The new conclusion concerns every feasible solution to the stronger
relaxation on a suitable realization of that random instance, not only the
explicit degree-two moment solution in the earlier note. No equality
between cloned prerequisite indicators is assumed.

## A precise sufficient hierarchy level

Use the Boolean test/witness formulation of the earlier note, with
prerequisite clone indicators `Y_(r,ell)` and witness indicators `Q_i`.
Keep the exact witness quota `sum_i Q_i = k`, the linear prerequisite
inequalities `Y_(r,ell)-Q_i >= 0` for every prerequisite of witness `i`,
and the actual total-test budget `K-C >= 0`.

By a degree-six Boolean SoS relaxation here we mean a linear
pseudoexpectation `E` on polynomials of degree at most six, with:

* `E[1]=1`, and `E[f^2]>=0` for every polynomial `f` of degree at most three;
* all Boolean identities `X^2=X` multiplied by every polynomial that
  keeps total degree at most six;
* `E[g^2 D]>=0` for every displayed linear inequality slack `D`, for
  every `g` of degree at most two;
* all displayed equalities multiplied by polynomials of allowable degree.

This is a standard sufficient level-three moment/localizing formulation.
Level numbering conventions differ, so the degree specification is the
intended claim. The number of variables and constraints is polynomial in
the explicit input. Additional original constraints may be retained.

All statements below are consequences of this formulation.

## Closure triples are forced at this level

Let `Q` be a witness and let `Y_a,Y_b,Y_c` be any three required
prerequisite clone indicators, belonging to distinct prerequisite types.
Then

```
E[Q] <= E[Y_a Y_b Y_c].
```

First use the localizer for `Y_a-Q>=0` with multiplier `g=Q` to obtain
`E[Q Y_a-Q]>=0`. Boolean positivity of
`(Q(1-Y_a))^2=Q(1-Y_a)` gives the reverse inequality, hence
`E[Q(1-Y_a)]=0`. Its squared norm is also zero. Positive semidefiniteness
therefore implies `E[Q(1-Y_a)h]=0` whenever `h` has degree at most three.
The same applies to `b,c`. In particular
`E[Q Y_b Y_c]=E[Q]`. Finally apply the localizer for `Y_a-Q>=0` with
`g=Y_bY_c`. Boolean reduction gives

```
E[(Y_a-Q)(Y_bY_c)^2]
  = E[Y_aY_bY_c]-E[QY_bY_c] >= 0.
```

The unreduced localizer has degree five, within the declared level.

## Averaging clones gives the correct budget bound

There are `q` prerequisite types and `L` unit-cost clones per type. Define

```
A_r = (1/L) sum_(ell=1)^L Y_(r,ell),
S = sum_r A_r,
s = K/L.
```

The `A_r` are linear forms, not Boolean variables. We never identify the
clones. Since `C = L S + sum_i Q_i`, the inequality `s-S>=0` has valid
localizers: add the budget localizer divided by `L` to the nonnegative
localizers of the own-test indicators divided by `L`. Equivalently, each
term `E[g^2 Q_i]` is nonnegative because it is
`E[(gQ_i)^2]` after Boolean reduction, and has degree at most six for
the multipliers used here.

The first-moment budget gives `E[S]<=s`. Summing the localizers of
`s-S>=0` with multiplier `g=Y_(r,ell)`, with coefficients `1/L`, gives
`E[S^2]<=s E[S]`. Its localizer with `g=S` gives
`E[S^3]<=s E[S^2]`. Consequently

```
E[S^3] <= s^3.
```

Every monomial of at most three prerequisite clone indicators has
nonnegative pseudoexpectation, because its square reduces to itself and
its unreduced square has degree at most six. Expansion of `S^3` therefore
gives

```
6 sum_(a<b<c) E[A_a A_b A_c] <= E[S^3] <= s^3.
```

This avoids any use of integer or Boolean identities for `S` or `A_r`.

## A general triple-codegree lower bound

Suppose every witness has exactly `d` distinct prerequisite types. Let

```
D = max_(a<b<c) |{i : {a,b,c} subset of P_i}|.
```

Average the closure-triple inequality over all `L^3` choices of clones
of its three prerequisite types. This yields
`E[Q_i]<=E[A_aA_bA_c]` whenever `{a,b,c} subset of P_i`.
Summing over witnesses and their prerequisite triples gives

```
k binom(d,3)
 = sum_i E[Q_i] binom(d,3)
 <= sum_(a<b<c) |{i:{a,b,c} subset of P_i}| E[A_aA_bA_c]
 <= (D/6) s^3.
```

Thus every feasible degree-six pseudoexpectation satisfies

```
K >= L [ k d(d-1)(d-2) / D ]^(1/3).
```

Nonuniform witness marginals do not affect this argument. The budget
includes every informative test's own cost, and ignoring that nonnegative
part only weakens the lower bound.

For a target reduced to `delta*k`, the same argument holds with `delta*k`
in place of `k`. Any fixed positive coverage loss leaves the exponent
unchanged; a polylogarithmic coverage loss changes only logarithmic factors.

## Triple codegrees in the cyclic random construction

Recall that there are `q` colors, `q` independently sampled seeds per
color, and `q` cyclic shifts per seed. Thus there are `q^3` witnesses.
Each seed is a uniformly random `d`-subset of `Z/qZ`, where
`d=ceil(100 log q)`.

Fix a triple `T` of distinct prerequisite types. For each of the `q^2`
independent seeds `D_j`, put

```
X_j(T) = |{t in Z/qZ : T subset of D_j+t}|.
```

Then `0<=X_j(T)<=d`: fixing one element of `T`, each of its possible
preimages in `D_j` determines the shift. Also

```
E[X_j(T)] = q (d)_3/(q)_3,
mu = E[sum_j X_j(T)] = q^3 (d)_3/(q)_3 <= 2d^3
```

for sufficiently large `q`. Here `(x)_3=x(x-1)(x-2)`.
The variance of the sum is at most `d*mu<=2d^4`.
Bernstein's inequality, with excess at least `6d^3`, gives

```
Pr[sum_j X_j(T) > 8d^3] <= exp(-c d^2)
```

for an absolute `c>0`. A union bound over fewer than `q^3` triples tends
to zero. Hence `D<=8d^3` with high probability. This property can be
required simultaneously with the expansion and pair-codegree properties
of `sdp-strong-gap.md`, since each of those also holds with high probability.

## Consequences for that instance family

For `k=q/4` and sufficiently large `d`, the triple-codegree lower bound
implies

```
K >= c L q^(1/3)
  = Omega(q^(4/3)/log^2 q).
```

The earlier covariance solution has budget `2q`, which is asymptotically
smaller. Therefore **no** degree-six feasible pseudoexpectation exists at
that budget on a realization satisfying the additional triple-codegree
property. This rules out extensions using completely different first
moments as well as extensions of the displayed covariance solution.

For comparison, buying all `Lq` prerequisite tests and one witness per
target blue gives an actual feasible solution of cost `Lq+k`.
Consequently this particular instance family has integrality gap at most

```
(Lq+k)/(c L q^(1/3)) = O(q^(2/3)) = O(m^(2/9))
```

against the degree-six relaxation. This is an upper bound on this
family's gap, not a general rounding theorem or an algorithm achieving
`m^(2/9)` on arbitrary instances. The `Omega(m^(1/3)/log^2 m)` lower bound
for the weaker covariance formulation remains valid.

## A constructive quarter-power guarantee with bounded triple codegree

There is a useful positive consequence for a restricted class; it does
not require solving an SDP to construct its output.

Consider singleton-blue red-blue cover: every available set covers one
blue, there are `M` available sets, every set has exactly `d>=3` red
neighbors, and the red universe has size `r>=d`. The target is `k`
distinct blues. Sets of the same blue remain separate choices. Let `D`
be the maximum number of sets containing a specified triple of reds.
Assume, for a parameter `C>=1`,

```
D <= C M binom(d,3)/binom(r,3).
```

This says that maximum triple codegree is at most `C` times its average.
It is checkable in polynomial time. Use exactly one Boolean assignment
witness per chosen blue, with total quota `k`, as in the preceding
formulation. The same degree-six proof, now without clones or witness
own costs, gives

```
K >= [ k d(d-1)(d-2)/D ]^(1/3).
```

Choose the cheaper of the following two explicit solutions:

1. Choose any `k` distinct coverable blues, and one available set for each.
   Their total red cost is at most `kd<=kK`. The inequality `d<=K` follows
   either from the usual individual-set filter or from conditioning the
   budget on any positive-marginal witness in the degree-six relaxation.
2. Choose one set for each of any `k` distinct coverable blues and charge
   all `r` reds. The actual returned union is no larger than `r`.

The second solution has ratio at most

```
r/K <= [D r^3/(k d(d-1)(d-2))]^(1/3)
     <= [C M/k]^(1/3) [r^3/(r(r-1)(r-2))]^(1/3)
     <= (9/2)^(1/3) [C M/k]^(1/3).
```

Here the final elementary bound holds for all integers `r>=3`.
Consequently the cheaper solution has ratio

```
O(min{k, (CM/k)^(1/3)}) = O((CM)^(1/4)).
```

For the last bound split at `k=(CM)^(1/4)`. This is an exact-target
guarantee, with no loss of blue coverage, relative to the degree-six
relaxation and hence relative to the integral optimum. If `C` is constant
or polylogarithmic, the exponent is `1/4` up to that factor. It is a
restricted-class result; `C` may be polynomially large in general.
The combinatorial triple-counting argument also proves the same lower
bound directly for integral solutions. No novelty claim is made.

For the grouped prerequisite construction, replace `r` by the number `q`
of prerequisite types, replicate every type `L` times, and include each
witness's own unit cost. Suppose again
`D<=C M binom(d,3)/binom(q,3)`. Buying every prerequisite clone and `k`
witnesses costs `Lq+k`. The relaxation satisfies `K>=k`, and the clone
argument above gives `K>=L[k(d)_3/D]^(1/3)`. Therefore this solution has
ratio at most `O((CM/k)^(1/3))+1`. Choosing `k` individual witness
closures has ratio at most `k`, by the valid individual-closure filter.
Taking the cheaper yields `O((CM)^(1/4)+1)`, still for exact target.
The total test count is `m=M+Lq>=M`, so for bounded `C` this is also an
`O(m^(1/4))` guarantee on this height-two subclass.

The cyclic random construction has `D<=8d^3` and average triple
codegree `M(d)_3/(q)_3=Theta(d^3)`, so it belongs to this bounded-`C`
subclass. At its particular target `k=q/4`, the all-prerequisite bound
is the sharper `O(m^(2/9))` established above.

## What is still missing for a general algorithm

Triple codegree alone cannot settle arbitrary instances: `D` can be as
large as the number of available sets. A viable extension needs a
constructive alternative when high-codegree triples prevent the moment
counting bound. The relevant alternative must cover distinct blue colors,
not merely find many witnesses containing a triple.

A precise useful target is a decomposition lemma with two outcomes:

1. A polynomial-time computable family covering a fixed fraction of the
   remaining assignment mass at cost `O(K m^(1/3-epsilon))`; or
2. A subinstance retaining a fixed fraction of assignment mass in which
   every prerequisite triple has sufficiently small **assignment-weighted,
   per-color** codegree, so that a higher-moment count yields the desired
   budget certificate.

The missing component is the first outcome for high triple codegree.
Conditioning on the triple preserves the quota and budget in the
remaining hierarchy, but does not itself bound how many distinct colors
can be realized together after rounding. Applying the existing pivot
rounding after conditioning reproduces its cube-root balance.

This is also why the `m^(1/4+epsilon)` algorithm for ordinary minimum
`k`-union cannot simply be imported: that problem asks for many selected
sets, while partial red-blue cover requires many distinct blue elements.
The near-cube-root example has `q^2` witnesses per color, so a cardinality
guarantee on witnesses may lose a polynomial factor in blue coverage.
The relevant primary references are
[Minimizing the Union](https://arxiv.org/abs/1611.07866) and
[Approximating Red-Blue Set Cover](https://arxiv.org/abs/2302.00213).

Standard correlation rounding also does not immediately supply the
missing lemma. Its additive errors must control rare witness events and
the union cost of their prerequisite closures. In a categorical encoding
one blue's witness alphabet can be polynomially large; constant error
in a pair marginal can exceed its witness probability by a polynomial
factor. In addition, the spectral theorem of
[Barak--Raghavendra--Steurer](https://arxiv.org/abs/1104.4680) depends on
the alphabet size and the graph's threshold rank, neither bounded on
these arbitrary instances. These are failures of direct application,
not impossibility results for modified conditioning methods.

### Direct higher-order pivots do not improve the exponent

The straightforward extension of the existing rounding to `t`-red
pivots has an explicit unfavorable balance. Here `t` is a fixed
positive integer. After buying singleton marginals at least `1/T`,
partition residual set sizes into dyadic scales `s`. For scales at least
`t`, a group is indexed by a `t`-subset `A` of reds and a scale; activate
it at probability proportional to `Y_A/s^t`, and select its incident
sets independently at conditional probabilities `x_j/Y_A`. Constant
factors depending on `t` can normalize the activation. The lifted
per-blue load inequalities give the same constant-coverage calculation
as with singleton pivots. Small residual sizes can be treated separately.

Call a set heavy when `x_j/Y_A>=theta/s`. If a heavy set in a group
contains an additional red `r`, closure consistency implies
`Y_(A union {r})>=theta Y_A/s`. Summing its group's activation
probabilities over permissible dyadic scales bounds this red's heavy
contribution by

```
O_t(Y_(A union {r})^t / (theta^t Y_A^(t-1)))
 <= O_t(Y_(A union {r})/theta^t).
```

The inequality uses `Y_(A union {r})<=Y_A`; zero moments contribute
zero. Conditioned budget constraints and the degree-`t` budget moment
give `sum_(A,r) Y_(A union {r})<=O_t(K^(t+1))`. Thus the heavy red cost
is `O_t(K^(t+1)/theta^t)`.

For light sets, conditional expected cost per group is at most
`O(theta D_(A,s))`. Singleton preprocessing guarantees only
`Y_A<=min_(r in A)y_r<1/T`. Since every set participates in `O_t(s^t)`
groups at its scale, total light cost is at most `O_t(theta M/T)`.
Including bought singleton reds yields

```
cost/K <= O_t(T + u^(-t) + u M/T),  where u=theta/K.
```

Optimizing `u` and then `T` gives exponent `t/(2t+1)`: `1/3` for
singletons, `2/5` for pairs, and `3/7` for triples. This is a bound on
this direct proof, not a lower bound for all algorithms using those
pivots. It identifies the precise missing gain: singleton preprocessing
does not give the joint-marginal bound `Y_A<=T^(-t)`.

### Raw high triple codegree does not guarantee color progress

An arbitrary number of witnesses may share one prerequisite triple and
all cover the same blue. The remaining colors can have completely
separate witness choices. Increasing the number of those duplicate
witnesses makes the raw codegree as large as desired while the common
triple's entire star covers one blue. The per-blue assignment equality
correctly caps that star's total assignment mass at one. Therefore a
useful decomposition must account for assignment mass across distinct
colors, rather than only raw witness count.

Even if the triple appears in witnesses for every color, it need not
make the residual instance easier: append three common prerequisites to
every witness of an arbitrary instance. Buying or conditioning on the
common triple then returns the original instance. Such a step can be
useful preprocessing, but a general proof needs a potential measuring
real progress and a bound on its accumulated cost or conditioning depth.

Finally, the distinct CSP construction in `sdp-csp-gap-investigation.md`
still supplies a polynomial gap approaching exponent `2/53` even for a
polynomial number of levels. It rules out polylogarithmic relative-to-SDP
rounding guarantees for the indicated encoding. It does not rule out an
exponent strictly between `2/53` and `1/3`, and it does not turn the
covariance gap into a lower bound for every fixed SoS level.

## Appendix: an improved light-cost term fails even for actual moments

The universal estimate `O(theta*m/T^2)` for the existing singleton-pivot
rounding's light contribution is false. This remains false when the
moments come from an actual distribution on feasible integral covers,
so additional SoS constraints alone cannot prove that estimate for the
unchanged rounding. The following example also has an exact quarter
target and a realization by the manuscript's decision-tree map `xi`.

Let `T>=2` be a power of two. Make `2T` disjoint blocks of `T`
prerequisite tests each. Prerequisite tests have no blue coverage. There
are eight blue elements. For every block `c`, blue `b`, and alternative
`a in [2T]`, create a witness test `W_(c,b,a)` that covers only `b` and
requires all `T` prerequisite tests in block `c`. It also has its own
unit-cost red element. Thus

```
number of prerequisite tests = 2T^2,
number of witness tests = (2T)*8*(2T) = 32T^2,
m = 34T^2,
k = 2 = |B|/4,
K = T+2.
```

Consider this actual random feasible cover: choose one block uniformly,
choose two of the eight blues uniformly, and independently choose one
of the `2T` witness alternatives for each chosen blue. Buy those two
witness tests and the block's `T` prerequisites. Every outcome is
precedence-closed, has cost exactly `K`, and covers exactly `k` blues.
Use its moments, including all higher moments, in the relaxation.

The first moments are

```
y_p = x_p = 1/(2T)                  for prerequisite tests,
y_w = x_w = a_(b,w) = 1/(16T^2)    for witness w covering b,
z_b = 1/4                          for every blue.
```

All conditioned cost constraints and assignment quotas hold as actual
identities. Every moment and localizing matrix is valid. Each witness
closure has size `T+1<=K`, so the individual-set size filter keeps it.
No red is bought by the initial threshold `y_r>=1/T`.

Use the existing rounding with `theta=K/T` and examine only the witness
bucket `s=T`; all these closures have size `T+1` in `[T,2T)`. For a
prerequisite pivot `p` in block `c`, each incident witness has conditional
selection probability

```
x_w/y_p = 1/(8T) < theta/s = (T+2)/T^2.
```

Consequently all these choices are light. This pivot group activates
with probability `y_p/s=1/(2T^2)`. Given activation, it independently
selects among `16T` witnesses. The probability of selecting at least one
is

```
c_T = 1-(1-1/(8T))^(16T) >= 1-exp(-2).
```

Any such success buys all `T` prerequisite reds of its block. The `T`
prerequisite-pivot groups within a block act independently. Writing
`u=c_T/(2T^2)`, the probability that their light selections reach this
block is

```
1-(1-u)^T >= Tu/2 = c_T/(4T).
```

For example, the inequality follows from `1-(1-u)^T>=1-exp(-Tu)` and
`1-exp(-v)>=v/2` for `0<=v<=1`. Since the `2T` blocks are disjoint,
the expected number of prerequisite reds in the union reached by light
selections is at least

```
(2T)*T*c_T/(4T) = c_T*T/2 = Omega(T).
```

This counts the actual union, rather than counting one block repeatedly
for different pivots. Other rounding groups may add reds and cannot
invalidate this lower bound. In contrast, the proposed improved charge
is

```
theta*m/T^2 = ((T+2)/T)*(34T^2)/T^2 = O(1).
```

The established light bound `O(theta*m/T)` is of order `T` here and is
consistent with the lower bound.

For the `xi` realization, take eight hypotheses. A prerequisite test is
uninformative; witness `W_(c,b,a)` has replies `{b}` and the other seven
hypotheses. Thus `xi(W)={b}`, `xi(P)=empty`, and the separator target is
exactly two blues.

**Scope.** This is a counterexample to a universal improved *light-term*
lemma for the unchanged rounding, not an integrality gap or an
approximation lower bound. An optimal integral solution has cost `K`.
Here the threshold parameter is `T=Theta(sqrt(m))`, rather than
`m^(1/4)`. The example therefore does not refute a lemma stated only at
the latter parameter, nor the weaker total residual estimate
`O(K[1+sqrt(m)/T])`, which is `Theta(T)` here. It also does not refute a
modified rounding that explicitly detects and handles these correlated
blocks. Such a modification needs its own cost and color-coverage proof.
