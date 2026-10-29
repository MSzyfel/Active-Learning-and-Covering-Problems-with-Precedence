# Conditioning, overlap moments, and a precise pair-pivot promise

This investigation does **not** establish an improvement over `m^(1/3)`
for general partial red-blue cover. It establishes a constructive
degree-six promise theorem with factor `m^(2/7)`, identifies its exact
overlap-moment hypothesis, and shows that bounded literal conditioning
cannot enforce that hypothesis in general, even for actual integral-cover
distributions. The manuscript has not been changed.

The main useful distinction is between a higher-moment **budget
certificate**, such as the triple-codegree argument in
`higher-order-rounding-investigation.md`, and a **rounding certificate**.
The overlap statistic below is a rounding certificate: when it is small,
there is an explicit algorithm with constant blue coverage and a verified
cost bound. Establishing that it is small, or replacing it by a useful
correlated-block alternative, is the unresolved step.

## 1. Formulation and level bookkeeping

Let `R_j,B_j` be the red and blue neighborhoods of each of the `m` sets.
Use Boolean variables `Y_r,X_j,Z_b,A_bj`, where `A_bj` assigns chosen blue
`b` to set `j`. Require the integral-valid equalities and inequalities

```
sum_b Z_b = k,
sum_(j:b in B_j) A_bj = Z_b,
A_bj <= X_j,
X_j <= Y_r                         (r in R_j),
sum_r Y_r <= K,
sum_(b in B_j) A_bj <= k X_j,
sum_(j:p in R_j,b in B_j) A_bj <= Y_p       (every p,b),
sum_(j:p in R_j) sum_(b in B_j) A_bj <= k Y_p.
```

Use the degree-six Boolean SoS formulation specified in
`higher-order-rounding-investigation.md`: a PSD moment matrix for
polynomials of degree at most three, Boolean identities through degree
six, all equality multiples through degree six, and localizers
`E[g^2 D]>=0` for every displayed linear slack `D` and every `g` of degree
at most two. Nonnegativity of the Boolean indicators is available by
Boolean reduction and PSD. These are sufficient constraints; this is not
a claim that the much weaker covariance formulation already suffices.

Write `x_j=E[X_j]`, `a_bj=E[A_bj]`, `y_r=E[Y_r]`, and
`Y_A=E[product_(r in A) Y_r]`. The following consequences are needed.

* Closure consistency: `x_j <= Y_A` for every subset of at most three
  reds in `R_j`. The zero-norm argument and degree-five localizer proving
  this for triples appear in the earlier higher-order note; the same
  proof applies to `X_j`. It also gives
  `E[A_bj Y_r]=a_bj` whenever `r in R_j`.
* Pair-conditioned per-blue load:
  `sum_(j:A subset R_j,b in B_j) a_bj <= Y_A`, for every red pair `A`.
  For `A={p,q}`, multiply the displayed per-`p,b` load slack by `Y_q`
  using its `g=Y_q` localizer. Retain the terms from sets also containing
  `q`; their assignment moments equal `a_bj`. Dropping the other,
  nonnegative assignment moments proves the claim.
* The same argument on the total-load slack gives
  `sum_(j:A subset R_j) sum_b a_bj <= k Y_A`.
* Writing `S=sum_r Y_r`, one has `E[S^3]<=K^3`. The budget localizers
  with `g=Y_r`, summed over `r`, give `E[S^2]<=K E[S]`; the localizer
  with `g=S` gives `E[S^3]<=K E[S^2]`. Also `E[S]<=K`.
  In particular, nonnegative Boolean moments give

  ```
  sum_(A:|A|=2) sum_r Y_(A union {r}) <= E[S^3]/2 <= K^3/2.
  ```

The loads include distinct-blue assignment variables; they cannot be
replaced by counts of witnesses. This matters when one blue has many
alternative sets.

Conditioning on a positive-probability conjunction of `h` variable
literals consumes at most `h` levels. Starting at degree `2h+6` leaves
the degree-six formulation above, with the exact quota `k` and budget
`K` preserved. If `N` is the number of Boolean variables, enumerating all
such events takes `N^O(h) 2^h` arithmetic operations on the moment table.
For fixed `h`, the starting SDP has size `N^O(h+3)`. These are standard
moment-matrix size/arithmetic bounds, with the usual numerical accuracy
qualification for solving SDPs; they do not assert exact rational SDP
optimization in polynomial bit complexity.

## 2. A computable overlap statistic

Fix `T>=1`. Buy, for accounting purposes, all reds with `y_r>=1/T`;
their number is at most `KT`. Select all sets whose remaining red
neighborhood is empty. If this covers at least `ceil(k/32)` blues, return
those sets. Otherwise remove their covered blues from the certificates.
The remaining assignment mass is greater than `31k/32`.

For each remaining nonempty residual set `R'_j`, take the dyadic integer
`s_j` satisfying `s_j <= |R'_j| < 2s_j`. Sets with no remaining
assignment mass can be omitted. Define

```
L2(T) = sum_(j:s_j>=2) (1/s_j^2)
                         sum_(A subset R'_j, |A|=2) Y_A.
```

The statistic uses pair moments of the original/conditioned solution on
the residual red set; it is not a sum over pairs counted just once.
Every participating set contributes its own weighted pair sum. It is
polynomial-time computable. Since `y_r<1/T` on residual reds, the
unconditional generic bound is only `L2(T)=O(m/T)`.

If instead every relevant residual pair satisfies `Y_A<=C/T^2`, then
`binom(|R'_j|,2)/s_j^2<2` gives

```
L2(T) <= 2 C m/T^2.
```

The pointwise hypothesis is sufficient but stronger than necessary.
The actual rounding theorem uses only `L2(T)`.

## 3. Pair-pivot rounding and red cost

For each scale `s>=2` and each unordered red pair `A`, independently
activate the pair group with probability `Y_A/s^2`. Given activation,
independently select each incident bucket set `j` with probability
`x_j/Y_A`. A zero-moment group is omitted; closure consistency implies
that it has no positive-marginal incident set.

Handle residual size one separately: for each red `p`, activate its
singleton group with probability `y_p`, and independently select the
sets whose residual neighborhood is exactly `{p}` with probabilities
`x_j/y_p`. These groups incur expected red cost at most `sum_p y_p<=K`.
This treatment is essential: pairs do not exist in a size-one set.

Fix an arbitrary `theta>0`. In a pair group call set `j` heavy if
`x_j/Y_A >= theta/s`, and light otherwise. For an additional red `r`
reached by a heavy set, triple consistency gives

```
Y_(A union {r}) >= x_j >= theta Y_A/s.
```

Consequently its possible dyadic scales start at
`s >= theta Y_A/Y_(A union {r})`. Summing the activation probabilities
over those scales gives at most

```
(4/3) Y_(A union {r})^2/(theta^2 Y_A)
    <= (4/3) Y_(A union {r})/theta^2.
```

Summing over pairs and reds and using the cubic budget bound gives
expected heavy red cost at most `2 K^3/theta^2` (a deliberately loose
constant). This is a union upper bound and remains valid when a red is
reached by several groups.

For light sets, a group has conditional expected projected red cost at
most `2s * D_(A,s) * theta/s = 2 theta D_(A,s)`. Multiplying by its
activation probability and summing gives exactly the useful bound

```
E[light red cost] <= 2 theta L2(T).
```

Including the initially bought reds and the size-one groups, put

```
C = 2 K T + 2 K^3/theta^2 + 2 theta L2(T).
```

The expected total booked red cost is at most `C`; the actual union cost
is no greater. Thus the relaxed optimization is

```
C/K = O(T + u^-2 + u L2(T)),       u=theta/K.
```

For `L2(T)>0`, take `theta=K L2(T)^(-1/3)` to obtain

```
C/K = O(T + L2(T)^(2/3)).
```

If `L2(T)=0`, no retained positive-assignment set has residual size at
least two, by closure consistency. The singleton treatment suffices.

## 4. Constant blue coverage and simultaneous success

As in the existing singleton-pivot analysis, associate to a selected
occurrence of set `j` an independent certificate subset of its remaining
blues with marginals `a_bj/x_j` and size at most `k`. Such a distribution
exists since each marginal is at most one and their sum is at most `k`;
the interval-offset construction in
`global-lp-decision-tree-investigation.md` makes it explicit.

Conditional on a group activating, the per-blue conditional certificate
probabilities sum to at most one, by the pair-conditioned or singleton
load constraint. Therefore the probability that this group certifies
blue `b` is at least `(1-1/e)` times that sum. A set of residual size
`d>=2` contributes `binom(d,2)/s_j^2` group opportunities, which lies
between `1/4` and `2`; a size-one set contributes one.

Independence of different groups gives

```
Pr[b certified] >= 1-exp(-(1-1/e) z_b/4) >= (3/23) z_b.
```

For the last inequality, use `1-1/e>=3/5` and
`1-exp(-v)>=v/(1+v)`, with `0<=z_b<=1`. If `Y` denotes the number of
distinct remaining certified blues, then

```
E[Y] > (3/23)(31/32)k > k/8.
```

For a group conditional on activation, let `F` be its distinct
certificate count. The total-load bound gives `E[F]<=k`. The independent
certificate subsets each have size at most `k`, and the deletion form of
Efron--Stein gives `Var(F)<=k E[F]`: deleting one subset changes the union
by at most `k`, and the sum of the uniquely covered counts is at most
the union size. Hence `E[F^2]<=2k E[F]`.

Let `W` be the sum of distinct certificate counts over activated groups.
Its summands are independent, `E[W]<=2k`, and consequently

```
E[W^2] <= 2k E[W] + E[W]^2 <= 8k^2.
```

Since `Y<=W`, Cauchy--Schwarz yields

```
Pr[Y>=k/32] >= (E[Y]-k/32)^2/E[Y^2]
             >= 9/8192 >= 1/1024.
```

Markov gives `Pr[cost>2048 C]<=1/2048`. Thus coverage at least
`ceil(k/32)` and cost at most `2048 C` occur jointly with probability at
least `1/2048`. Both actual coverage and union cost can be verified.
Independent repetitions give a randomized polynomial-time algorithm
with any prescribed inverse-polynomial failure probability. The
certificates are for analysis only; actual set coverage contains them.
This note does not need to assert a new deterministic derandomization.

We have therefore proved the following promise guarantee, relative to
the displayed degree-six relaxation:

```
coverage >= ceil(k/32),
cost = O(K [T+L2(T)^(2/3)]).
```

In particular, if `L2(T)=O(m/T^2)` and `T=m^(2/7)`, the factor is
`O(m^(2/7))`. More generally, for any fixed
`alpha in [2/7,1/3)`, the sufficient condition at `T=m^alpha` is
`L2(T)=O(m^(3 alpha/2))`. No universal proof of that condition is known
here. Trying all bounded literal conditionings merely makes this a
polynomial-time, checkable promise on one of those conditional solutions.

## 5. Why ordinary entropy conditioning does not supply the promise

For fixed residual neighborhoods put

```
w_pr = sum_(j:{p,r} subset R'_j, s_j>=2) 1/s_j^2,
W = sum_(p<r) w_pr.
```

For participating sets, `W` lies between one quarter and twice their
number. Since residual marginals are below `1/T`,

```
L2(T) <= W/T^2 + sum_(p<r) w_pr (Y_pr-y_p y_r)_+.
```

Thus at the `2/7` exponent, a sufficient overlap-weighted additive
covariance accuracy is `O(T^-2)`, not constant accuracy. Even merely
achieving `alpha=1/3-epsilon` this way asks for accuracy on the order of
`m^(-1/2-3epsilon/2)` when `W=Theta(m)`.

Here is the exact limitation of the generic entropy argument. Normalize
the overlap weights to a symmetric distribution `q` on ordered pairs,
and suppose, for a fixed vertex distribution `pi`, that
`q_pr <= Lambda pi_p pi_r`. Conditioning on `h` coordinates sampled from
`pi`, and choosing a uniformly random earlier conditioning time, gives

```
E[ sum_(p,r) pi_p pi_r I(Y_p;Y_r | conditioning) ] <= log(2)/h.
```

This is the entropy telescoping identity: the weighted average entropy
starts at most `log(2)`, and its expected drop at each step is the
displayed average mutual information. Pinsker and Cauchy--Schwarz then
give overlap-weighted covariance error at most

```
sqrt(Lambda log(2)/(2h)).
```

To obtain `T^-2` through this bound requires
`h=Omega(Lambda T^4)`, up to constants. This is a limitation of this
sufficient entropy estimate, not a lower bound on every possible
conditioning algorithm. It already ceases to be a constant-degree,
polynomial-size hierarchy argument. Recomputing the overlap weights
after each threshold deletion also makes the weights branch-dependent;
the fixed-weight telescoping proof does not automatically cover that
extra adaptation.

The spectral local-to-global correlation theorem of
[Barak, Raghavendra, and Steurer](https://arxiv.org/abs/1104.4680)
requires control of the relevant graph's threshold rank. The overlap
graph here is arbitrary and can be a union of many separate dense
blocks. Replacing uniform averages by overlap weights therefore needs
a structural or spectral argument; it is not a free consequence of
degree-six PSD. Encoding each blue as a categorical choice introduces
the additional issue that its witness alphabet can grow with `m`.

## 6. An actual-distribution obstruction to bounded conditioning

The failure of the clean promise is not merely an artifact of
pseudomoments. Let `v` tend to infinity through integers, and put

```
H=v^5,       G=2v^9,       d=v^5.
```

Make `G` disjoint blocks of `d` prerequisite tests each. There are `4H`
blue colors. For every block and color create one witness test covering
that color and requiring the entire block. Include the witness's own
unit cost. Thus

```
m = Gd + 4HG = 10v^14,
k = H = |B|/4,
K = Hd+H = v^10+v^5.
```

Consider the actual feasible distribution that selects a uniform
`H`-subset of blocks, a uniform `H`-subset of colors, and a uniform
bijection between these subsets. Buy all selected blocks and their `H`
matched witnesses. Every outcome covers exactly `k` blues and costs
exactly `K`. All SoS constraints at every level hold.

Every prerequisite has marginal `H/G=1/(2v^4)`. Every pair of different
prerequisites in the same block has that same pair moment. The threshold
`T=m^(2/7)=10^(2/7)v^4` satisfies `1/T>1/(2v^4)`, because `10^(2/7)<2`.
Thus none of these prerequisites is initially bought.

Condition on any positive-probability conjunction of at most `h`
test, assignment, or blue-variable literals, where `h` is a fixed
constant. At most `h` blocks are mentioned by its test/assignment
literals. The untouched blocks remain exchangeable. Their conditional
selection marginal lies between

```
(H-h)/G    and    H/(G-h).
```

For sufficiently large `v`, both are `Theta(v^-4)`, and the upper bound
is still below `1/T`. Every pair inside an untouched block still has
pair moment equal to that marginal, because those indicators are
identical in every integral outcome. Only `O(h)` colors can be excluded
by blue or witness literals, so `Theta(GH)=Theta(m)` untouched
block/color witness sets remain available with positive assignment mass.
Their within-block pairs alone give

```
L2(T) = Omega(m/T),
overlap-weighted positive covariance = Omega(1/T).
```

This exceeds `O(m/T^2)` by a polynomial factor. The obstruction persists
after buying high singleton marginals in the conditional solution.
Consequently no lemma claiming that **a bounded number of ordinary
literal conditionings always makes this L2 promise true** can hold.
It also refutes the stronger pointwise promise on all residual pair
moments at the desired threshold.

This is not a hard cover instance or an integrality gap. Its blocks are
explicit and easy to handle; selecting one witness per target color has
cost at most `Hd+H=K` even if all chosen blocks differ. That is precisely
the lesson: correlated blocks need an alternative constructive rule,
rather than being forced into a false universal decorrelation lemma.
The example does not address arbitrary polynomial reweighting of a
pseudoexpectation, as opposed to bounded literal conditioning.

## 7. What remains genuinely open in this route

Perfectly correlated reds can be detected by the zero PSD distance
`E[(Y_p-Y_r)^2]=0`. One may book their entire equivalence class as a
weighted red atom: positive-marginal witnesses using one member are
pseudoconsistent with all members, and booking extra reds cannot hurt
feasibility of the original returned set family. The obstruction above
is amenable to this contraction or to the simple closure-size bound.
What is missing is a general algorithm for approximate and overlapping
correlation classes, with a cost bound and progress in **distinct blue
coverage**. Pairwise correlation alone does not show that all the reds
of a witness belong to one affordable class.

A precise remaining target is: for some fixed `h` and
`alpha in [2/7,1/3)`, either produce a family of cost `O(K m^alpha)`
covering `k/polylog(m)` distinct blues, or find a bounded conditioning
and a justified correlated-block reduction for which the residual
statistic satisfies `L2(m^alpha)=O(m^(3alpha/2))`, while retaining the
needed assignment mass. Neither the existence of this alternative nor
its progress potential has been proved here.

The degree-six refutation of the near-cube-root covariance gap in
`higher-order-rounding-investigation.md` is compatible with this gap in
the rounding argument: a stronger lower bound on `K` for one random
family does not construct a cover on arbitrary instances. Conversely,
`sdp-csp-gap-investigation.md` gives a gap approaching `m^(2/53)` even
with polynomially many levels, for the indicated Boolean encoding.
It precludes a universal polylogarithmic relative-to-SDP guarantee, but
does not exclude the `2/7` exponent or another exponent strictly
between `2/53` and `1/3`.

The relevant comparison with ordinary minimum union must preserve
colors: the algorithms in
[Minimizing the Union](https://arxiv.org/abs/1611.07866) select many
vertices/sets, whereas this rounding must certify many distinct blues.
The general red-blue result in
[Approximating Red-Blue Set Cover](https://arxiv.org/abs/2302.00213)
provides the cube-root benchmark; no direct stronger hierarchy rounding
theorem for the present colored partial problem has been extracted here.
