# Enumerating small prerequisite cores: a planted-instance bypass

This note proves a deterministic core-enumeration lemma and applies it to
the random instances behind `sdp-strong-gap.md`, with arbitrary planted
solutions added. It gives a polylogarithmic approximation on that promised
family and distinguishes its planted and unplanted regimes with high
probability. It does not improve the general `m^(1/3)` approximation.
An explicit counterexample at the end shows why enumerating cores and
choosing arbitrary representatives cannot by itself provide that
improvement.

## A deterministic structural lemma

Consider depth-two precedence cover. Each informative test covers one
blue and has its own unit execution cost. Its prerequisites are weighted
types: selecting type `r` costs `w_r`, which can equivalently represent
`w_r` identical unit-cost predecessor tests. Exact twins can be compressed
into these types in polynomial time. With no twins, each prerequisite is
its own type of weight one.

Assume there exist witnesses for `k` distinct blues whose prerequisite
union is `S`. Write

```
s=|S|,                 W(S)=sum_(r in S) w_r,
d=min prerequisite-type degree of those witnesses,
D=max prerequisite cost of any informative test.
```

Fix a positive integer `t<=d`. For every `t`-subset `T` of types, its
star consists of all informative tests whose prerequisites contain `T`.
Suppose the following structural condition holds for the unknown set `S`:

> Every `t`-subset `T` of `S` belongs to at most `B` tests whose
> prerequisite set is not contained in `S`.

There is a deterministic polynomial-time algorithm, for every fixed `t`,
that covers `k` blues at total cost at most

```
k + (W(S)+BD) [binom(s,t)/binom(d,t)] H_k,
```

where `H_k=sum_(i=1)^k 1/i`. The algorithm need not know `S`, its
witnesses, `B`, `d`, or `D`.

The algorithm repeatedly considers every `t`-star. For each previously
uncovered color in that star, it chooses its first test in a fixed input
order, truncating the list of colors if necessary to avoid exceeding the
remaining target. It computes the actual marginal prerequisite and own
test cost, divided by the number of new colors. It executes the candidate
with minimum ratio, and repeats. Empty candidates are ignored.

To prove the guarantee, let `r` be the remaining target and let `h>=r`
be the number of uncovered colors among the comparator's `k` colors.
Each of their witnesses contains at least `binom(d,t)` cores in `S`.
Pigeonholing over `binom(s,t)` choices yields one core that belongs to
at least

```
h binom(d,t)/binom(s,t)
```

of these witnesses. Its star therefore contains that many distinct
uncovered colors. All tests in that star have their prerequisites either
inside `S`, or in the at most `B` exceptional sets. Thus the union cost
of the star's prerequisites is at most `M=W(S)+BD`. Choosing arbitrary
representatives cannot increase that bound. After truncation, the
candidate gain `g` is at least `r/R`, where
`R=binom(s,t)/binom(d,t)>=1`; its marginal cost is at most `g+M`.
Consequently the chosen candidate's cost per new color is at most
`1+MR/r`.

Charging the successive gains uses

```
sum_steps g/r <= H_k.
```

This follows because a step reducing `r` to `r-g` contributes
`g/r<=sum_(i=r-g+1)^r 1/i`. Summing the marginal costs proves the
claim. The proof also permits arbitrary positive type weights.

This is a structural approximation guarantee, not a universal estimate
on `B`. The key remaining inequality for a general improvement is control
of the number or union cost of the exceptional sets around a useful
optimal core. Large `B` can be harmless when those exceptions have a small
union, so the stronger sufficient condition is directly

```
cost(union of all prerequisite sets containing T) <= M
```

for enough cores of the unknown optimum. The proof uses only such a
union-cost bound, not the count `B` itself.

## The planted promise family

Use the background incidence distribution of `sdp-strong-gap.md`:

```
q colors, q prerequisite types, q^2 tests per color,
d=ceil(100 log q),
L=ceil(q/(64d^2)) identical unit-cost copies of every type,
k=q/4.
```

Each color has `q` independent uniform random `d`-subsets of the cyclic
group `Z/qZ` as seeds, and includes all `q` shifts of every seed.
There are `q^3` background informative tests. All logarithms here are
natural, and `q` is sufficiently large and divisible by four.

In a YES instance, an adversary chooses a set `S` of at most `C d^2`
types, for a fixed constant `C`, and adds a degree-`d` witness contained
in `S` for each of at least `k` colors. No randomness or independence is
assumed about these planted witnesses. More tests entirely contained in
`S` may be added without harming the argument. Alternatively the planted
tests may replace background tests; deleting background tests only
improves the estimates below.

In a NO instance no planted tests are added. This is a promise problem:
the theorem does not assert that every arbitrary instance has one of these
forms.

## Uniformly bounded background triple stars

With probability tending to one, every triple of distinct types is
contained in at most `8d^3` background tests.

Fix a triple `T`. For each of the `q^2` independent seeds, let `X` be
the number of its cyclic shifts containing `T`. Then `0<=X<=d`: fixing
one member of `T` leaves at most `d` possible shifts. Moreover,

```
E[X]=(d)_3/((q-1)(q-2)),
mu=E[sum X]<=2d^3,
```

where `(d)_3=d(d-1)(d-2)`. The first formula follows by summing over
the `q` shifts, each of which contains the specified distinct triple with
probability `(d)_3/(q)_3`.

The convexity bound `exp(X/d)<=1+(e-1)X/d` for `0<=X<=d` gives

```
Pr[sum X>=8d^3]
 <=exp(-8d^2+(e-1)mu/d)
 <=exp(-(10-2e)d^2)
 <=exp(-4d^2).
```

A union bound over fewer than `q^3` triples proves the uniform claim.
This argument permits the substantial dependence among shifts of a single
seed; only different seeds are treated as independent.

## The algorithm and its quantitative guarantee

Apply the structural lemma with `t=3`. In a YES instance, every test
outside `S` is a background test, so `B<=8d^3`. Also

```
s<=C d^2,    W(S)=Ls,    D=Ld,
binom(s,3)/binom(d,3)=O_C(d^3).
```

The deterministic algorithm therefore returns a feasible solution of
cost

```
k+L(s+8d^4) O_C(d^3) H_k
 = O_C(q d^5 log q)
 = O_C(q log^6 q).
```

Any feasible solution has cost at least `k`, because each informative
test covers just one color and has its own unit cost. Thus this is an
`O_C(log^6 q)` approximation on YES instances. In fact the planted
solution itself has cost at most `Ls+k=O_C(q)`.

On NO instances, the expansion calculation in `sdp-strong-gap.md` shows
with high probability that every `k` witnesses of distinct colors use
more than `q/2` prerequisite types. Their execution cost exceeds

```
Lq/2 = Omega(q^2/log^2 q).
```

The triple-star and expansion events hold simultaneously with high
probability by a union bound. Therefore, for sufficiently large `q`, run
the deterministic algorithm and declare YES exactly when its returned
feasible solution costs less than `q^(3/2)`. It distinguishes the two
promised regimes with high probability over the background. No SDP
rounding, spectral certificate, or knowledge of the hidden core `S` is
used.

For a NO instance, selecting any one witness in each of `k` colors costs
at most `Lq+k`, which is at most `2+o(1)` times the optimum lower bound.
Returning the cheaper of this trivial solution and the triple-star
solution therefore gives a polylogarithmic approximation on both regimes
of the promise family.

This establishes that the explicit degree-two SDP gap is not by itself
an algorithmic barrier on the random family supporting that gap. The
large SDP gap on NO instances coexists with a simple combinatorial
approximation and a stronger small-core algorithm for planted instances.

## A higher-order counting inequality that rejects the SDP witness

There is also a useful general lower bound. Let `c(T)` be the number of
colors with some available test containing a type core `T`, and put
`C_t=max_(|T|=t)c(T)`. If `k` chosen witnesses each have at least `d`
types and their union has `s` types, then

```
k binom(d,t) <= C_t binom(s,t).
```

Count pairs consisting of a chosen witness and one of its `t`-subsets.
The lower bound counts through witnesses; the upper bound counts through
the cores in the union, using at most one chosen witness per color.
This inequality does not require the planted promise or the exceptional
set condition of the algorithmic lemma.

For fixed `t`, a polynomial-size valid moment strengthening enforces the
same lower bound. For every type subset `T` of size at most `t`, introduce
a nonnegative moment `mu_T`, with `mu_empty=1`. Guess an integral type
budget `s0`, and impose

```
sum_(r not in T) mu_(T union {r}) <= (s0-|T|) mu_T
                                      for every |T|<t.
```

These are the budget inequalities conditioned on selecting every type
in `T`. Also impose, for every blue `b` and every size-`t` core `T`,

```
sum_(i:color(i)=b, T subset P_i) a_i <= mu_T,
```

where `a_i` is the witness assignment mass. Each inequality is valid
integrally: at most one witness is assigned to a color, and any such
witness requires every type in `T`. The analogous assignment-incidence
formula applies when a test can cover several blues.

Summing the conditioned budget constraints at level `ell` yields

```
(ell+1) sum_(|T|=ell+1) mu_T
 <= (s0-ell) sum_(|T|=ell) mu_T.
```

Consequently `sum_(|T|=t)mu_T<=binom(s0,t)`. Summing the per-blue core
loads, and using the exact assignment quota, gives

```
k binom(d,t)
 <=sum_(|T|=t)c(T)mu_T
 <=C_t binom(s0,t).
```

Thus these explicit inequalities alone enforce the counting lower bound;
no unspecified hierarchy property or PSD completion is needed for this
claim.

For the random NO family above, `C_3<=8d^3` with high probability, so
every feasible solution of this third-order strengthening has

```
s0=Omega(k^(1/3))=Omega(q^(1/3)).
```

In contrast, the degree-two construction in `sdp-strong-gap.md` has
fractional type mass `q tau=64d^2`. Since each type costs `L`, the new
lower bound raises its budget to at least
`Omega(L q^(1/3))=Omega(q^(4/3)/d^2)`. Selecting all types and `k`
informative witnesses costs at most `Lq+k`, so on this family the
integrality gap of the new strengthening is at most

```
O(q^(2/3))=O(m^(2/9)).
```

This defeats the particular degree-two obstruction. It is not a general
rounding theorem: in arbitrary instances `C_3` may be much larger, and a
large core's many alternative witnesses can have a large union. The
counterexample below exhibits exactly that unresolved alternative.

## A constructive guarantee from distinct-color triple codegree

The counting inequality also gives an elementary parameterized algorithmic
theorem. Suppose each prerequisite type has the same cost `L`, each
informative test covers one blue and costs one, and every informative test
has between `d>=3` and `D` prerequisite types. Let `C_3` be the maximum
number of distinct colors available at a triple, as above. Choosing any
one informative test in each of any `k` distinct colors is an

```
O((D/d) k^(2/3) C_3^(1/3))
```

approximation. This guarantee is deterministic and uses distinct-color
codegree, which can be much smaller than raw test codegree.

Indeed, its cost is at most `k+LkD`. If the optimum uses `s` types,
the counting inequality and the estimates
`binom(d,3)>=d^3/27`, `binom(s,3)<=s^3/6` give

```
s >= (d/2)(k/C_3)^(1/3).
```

The optimum cost is at least `k+Ls`, so the ratio is at most

```
max(1, 2(D/d) k^(2/3) C_3^(1/3)).
```

Consequently, when `D/d=O(1)` and `k^2 C_3<=m^(3/4)`, this gives an
`O(m^(1/4))` approximation. In particular, for the low-codegree random
family with `k=Theta(m^(1/3))` and `C_3=polylog(m)`, it gives
`O(m^(2/9) polylog(m))` directly. These parameter restrictions are
essential to the claim; this is not a quarter-power approximation on all
instances with an arbitrary target or arbitrary codegree.

A high-codegree pivot alone does not supply the missing complementary
theorem. If a size-`t` core appears in `B` colors, choosing one witness
for each of `g=min(B,k)` of those colors costs at most

```
g + L[t+g(D-t)].
```

For fixed `t` and large `D`, this saves only `L(g-1)t` compared with
unrelated witnesses. More fundamentally, adding `t` universal prerequisite
types to every test of an arbitrary colored-cover instance creates a core
available in every color while changing the optimum by only `Lt`.
Thus the high-`C_t` condition alone contains arbitrary residual colored
cover. A successful complementary rule needs information about the
residual unions or overlaps, not just the existence of a popular core.

## An explicit obstruction to the unrestricted core algorithm

Fix any constant core size `t>=1`. Let `s=2^h` tend to infinity with
`h>=t`, and identify a shared prerequisite set `S` with `F_2^h`.
There are `q=s` colors and target `k=s/4`. For each color `b`, include
an optimal test whose prerequisite set is exactly `S`.

Let `U_1,...,U_A` be all affine hyperplanes in `F_2^h`, so
`A=2(s-1)` and every `U_j` has `s/2` points. For each color `b` and
hyperplane `U_j`, add an alternative test with prerequisites

```
U_j union V_(b,j),
```

where each `V_(b,j)` is a fresh, private set of `s/2` prerequisite
tests. All prerequisite and informative tests have unit cost. List the
alternative tests in hyperplane order before the optimal test of every
color.

Every `t`-subset of `S` lies in some affine hyperplane: its affine span
has dimension at most `t-1<h`, and extends to a hyperplane. Therefore a
core `T` contained in `S` has a star containing all `q` colors, and the
first representative of every color is an alternative using the same
first hyperplane containing `T`. When truncated to the target `k`, this
candidate costs

```
s/2+k(s/2)+k,
```

with ratio `s/2+3` per newly covered color.

A core containing a private prerequisite is contained in at most one
test, and its nonempty star costs `s+1` to cover one color. A core
meeting two different private sets belongs to no test. Thus for `s>4`,
the fixed-order representative algorithm selects an `S`-core in its
first iteration, immediately covers `k` colors, and pays
`s^2/8+3s/4`.

An optimum solution costs at most `s+k=5s/4`, by using the tests
whose prerequisites are `S`. The number of tests, including all private
prerequisites, is

```
m=s+s A(s/2)+s(A+1)=Theta(s^3).
```

Consequently this core-star algorithm has approximation ratio
`Omega(s)=Omega(m^(1/3))`, for every fixed `t`. The structural condition
fails for every optimal core: each such core has at least `q` exceptional
tests, with large private union.

This example targets the specified arbitrary-representative rule. It is
not hardness for selecting representatives intelligently, and simple
frequency information identifies the shared set `S` in this example.
Finding a general rule that handles both this heavy-overlap obstruction
and the sparse random planted family is the remaining algorithmic task.
