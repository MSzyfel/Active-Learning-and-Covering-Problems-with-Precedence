# CMV approximation investigation

This note records a proof sketch for an improved logarithmic factor in the
Chlamtac--Makarychev--Vakilian (CMV) red-blue set-cover algorithm. It does
**not** prove a pure `O(m^(1/3))` bound for exact coverage, or an exponent
below `1/3` for a fixed coverage fraction. It does contain a candidate
sub-cube-root bicriteria tradeoff when the coverage fraction may decrease
with `m`. The calculations should be independently checked before use in the
paper; their novelty has not been established.

## Candidate bound

For partial red-blue set cover with `m` sets, `r` red elements, `b` blue
elements, and any feasible target `k`, the CMV decomposition and a capped
rounding argument appear to give a randomized polynomial-time approximation
with high probability of

```
O(m^(1/3) log(2r) log^(2/3)(2k)).
```

For the precedence-cover reduction in `sections/set_covering_section.tex`,
there are `m` red elements and `n` blue elements, giving
`O(m^(1/3) log(2m) log^(2/3)(2k))`. In particular, this still includes
logarithmic factors. The claimed result concerns unit red costs.

## Proof sketch

Write `L = log_2(2r)`, `H = log_2(2k)`, and guess an integer budget `K`.
For the analysis take a correct guess `OPT <= K <= 2 OPT`. The algorithm
can try every integer `K` from 1 to `r` and keep the cheapest feasible
output. First handle `k = 0` and `OPT = 0` by taking all red-free sets. Discard
sets with more than `K` red elements. A correct guess retains an optimum.

Set

```
T = m^(1/3) L H^(2/3),     a = sqrt(m L / T).
```

If `T >= m`, selecting every retained set costs at most `mK <= TK`. If
`KT >= r`, the same selection costs at most `r <= KT`. Otherwise `a >= 1`
and `KT < r`. Use the CMV nested red-deletion and degree-bucketing
construction, deleting `floor(KT/L)` red elements per level. Since
`KT/L >= 1`, this gives a common excluded red set of size at most `KT`.
In each nonzero bucket of projected red degree in `[s, 2s]`, every
remaining red element has bucket degree

```
D = O(m s L / (K T)).
```

Save sets whose projected red degree is zero at each decomposition stage,
and select all saved sets before rounding:
their red neighborhoods are contained in the common excluded set. Remove
their covered blues. Excluded red elements are charged only once, regardless
of how many rounds or buckets use them. Every remaining bucket has `s <= K`.

Suppose the current quota is `q > 0`. A correct optimum still covers at
least `q` currently uncovered blue elements. CMV's averaging over buckets
and pivot red elements gives a local LP with objective `Z` and scale `s`
such that

```
Z/s >= q/(K L).
```

Trying every bucket and pivot, and choosing the largest `Z/s`, finds an LP
with at least this value. Round its set variables independently. Splitting
them at `x_j = K/(s a)`, the red elements adjacent to heavy sets number at
most `s a`, while the expected number reached through light sets is
`O(m s L/(T a))`. Hence the expected projected red cost `R` satisfies

```
E[R] = O(s (a + m L/(T a))) = O(s a).
```

If a retained original set covers at least `q` currently uncovered blues,
select it and finish; its original red cost is at most `K`. Otherwise every
retained set covers fewer than `q` current blues. Let `X` be the number of
current blues covered by the rounded collection, and `mu = E[X]`. Standard
coverage rounding gives `mu >= (1 - 1/e) Z`.

The following capped-coverage estimate controls the final round without
adding a concentration logarithm:

```
Var(X) <= q mu,
E[min(X,q)] >= q mu/(mu + 2q) >= (1/3) min(mu,q).
```

For the variance bound, use Efron--Stein on independent set choices. A
single set's marginal contribution is at most `q`, while the sum of the
unique contributions of the selected sets is at most `X`. For the second
bound, put `G = min(X,q)` and apply Cauchy--Schwarz:

```
mu^2 <= E[G] E[X^2/G]
     <= E[G] (mu + E[X^2]/q)
     <= E[G] (2mu + mu^2/q),
```

where `X^2/G` is interpreted as zero when `X = G = 0`. Since `s <= K`, the
LP guarantee implies

```
E[G] = Omega(q s/(K L)).
```

Choose `lambda = C a K L/q` for a sufficiently large absolute constant
`C`. The preceding estimates give positive slack
`E[lambda G - R] = Omega(s a)`. Also `lambda G <= C a K L`. Consequently,
one independent trial has inverse-polynomial probability of producing a
nonempty output with `R < lambda G`; polynomially many trials and standard
amplification find such an output with high probability. This avoids
assuming that `E[min(X,q)]` can be computed exactly by conditional
expectations.

In a successful round, charge only the capped gain `G` against the remaining
quota. The sum of `G/q` over rounds is at most the harmonic number `H_k`,
including the last round. Thus projected red costs total
`O(a K L H_k)`, and including the excluded reds gives

```
O(K [T + L H sqrt(mL/T)])
  = O(K m^(1/3) L H^(2/3)).
```

## Bicriteria tradeoffs

For `0 < epsilon < 1`, let `h = floor(epsilon k)` and
`J = 1 + ln(k/(h+1))`. Stop the above process once it covers at least
`k-h` blue elements. Continue to compare each round against the *original*
residual quota `q = k - (number already covered)`, and charge the capped
gain `min(X,q)`. Before the last round, `q > h`; the last round contributes
at most one to the harmonic charge, even if it overshoots the stopping
threshold. Consequently the total charge is at most `J`.

Using `T = m^(1/3) L J^(2/3)` and `a = sqrt(mL/T)` gives red cost

```
O(OPT m^(1/3) log(2r) J^(2/3)),
J <= 1 + ln(1/epsilon).
```

The output covers at least `(1-epsilon)k` elements (with the integer
rounding above). For every fixed `epsilon > 0`, its cost factor is
`O(m^(1/3) log(2r))`, independent of the number of blues. This is a
general-instance bicriteria proof sketch, not a sub-cube-root result.
Applying the project's cost-and-coverage-preserving closure reduction gives
the same guarantee for partial precedence-constrained set cover with
`r = m`. Trying every target transfers it to budgeted precedence cover;
the existing budget-to-min-sum reduction then yields its corresponding
min-sum bicriteria guarantee, after amplifying all randomized calls.

### Scaled rounding for a larger coverage loss

The following stronger tradeoff is another derived proof sketch; its novelty
and all details still need independent review. For `beta >= 2`, let

```
h = ceil(k/beta),    q0 = k-h+1,    delta = h/q0.
```

The goal is to cover `h` blues, while the cost benchmark remains the
optimum `K` for covering the original target `k`. There is a randomized
polynomial-time algorithm with cost at most `alpha OPT` and coverage at
least `h`, where

```
alpha = O(1 + m^(1/3) [L delta^(2/3) + L^(2/3) delta^(1/3)]).
```

Here `L = ceil(log_2(2K))` can be used for the correct budget guess; a
uniform bound is obtained by replacing it with `ceil(log_2(2r))`. If
`h = 1`, simply take an eligible set covering one blue, at cost at most
`K`. Otherwise `delta = O(1/beta)` for `beta >= 2` and `beta < k`, giving

```
alpha = O(1 + m^(1/3) [L beta^(-2/3) + L^(2/3) beta^(-1/3)]).
```

For precedence cover, `r = m`. Thus taking `beta = m^eta` for fixed
`0 < eta < 1` gives `alpha = O_tilde(m^((1-eta)/3))`, but only an
`m^(-eta)` fraction of the target is guaranteed. For example,
`beta = m^(1/4)` gives an `O_tilde(m^(1/4))` cost factor at coverage
`m^(-1/4)`. The coverage fraction is not constant. Taking
`beta = Theta(log^2(2m))` gives an `O(m^(1/3))` cost factor with a
polylogarithmically small coverage fraction.

Proof outline:

1. Guess `K`, discard original sets with more than `K` red neighbors, and
   handle original red-free sets. Every unfinished iteration has covered
   at most `h-1` blues, so the original optimum covers at least `q0` still
   uncovered blues. Each set has at most `K` red neighbors after filtering;
   there are at most `L` positive red-degree buckets.
2. Set `T = (mL)^(1/3) (L delta + sqrt(L delta))^(2/3)` and
   `a = sqrt(mL/T)`. Delete `ceil(KT/L)` high-degree reds per bucket in
   CMV's nested decomposition. The common excluded-red set costs at most
   `KT+L = O(K(T+1))`, since `L <= 2K`. Every surviving red in a bucket
   of projected degree scale `s` has bucket degree
   `D = O(msL/(KT))`. If all reds would be excluded, selecting all retained
   sets already has this cost bound. If `T >= m`, selecting all retained
   sets costs at most `mK <= TK`. Save sets of zero projected red degree
   at every decomposition stage, and select all saved sets before rounding.
3. At each unfinished iteration, if one retained set covers at least `h`
   current blues, select it and finish at additional cost at most `K`.
   Otherwise, the CMV bucket-and-pivot LP supplies `Z/s >= q0/(K L)`.
   Choose a bucket and pivot maximizing `Z/s`, and independently sample
   each set with probability `rho x_j`, where `rho = min(1,h/Z)`.
4. Splitting at `x_j = K/(s a sqrt(rho))` gives expected projected red
   cost `O(s a sqrt(rho))`: the heavy reds cost at most
   `s a sqrt(rho)`, while the expected light cost is at most
   `2s D rho K/(s a sqrt(rho))`. Let `X` be newly covered blues and
   `G = min(X,h)`. The capped-coverage lemma above, applied with cap `h`,
   gives `E[G] = Omega(min(Z,h))`, since every candidate set has fewer
   than `h` current blues and `E[X] >= (1-1/e) rho Z`.
5. If `Z <= h`, the expected red-to-capped-gain ratio is
   `O(a K L/q0)`. If `Z >= h`, it is at most
   `O(a K sqrt(L/(h q0)))`, using `Z >= q0 s/(K L)` and `s <= K`.
   Both cases are bounded by
   `O((aK/h) [L delta + sqrt(L delta)])`. More explicitly, let
   `U = C s a sqrt(rho)` upper-bound expected red cost and let
   `v = c min(Z,h)` lower-bound expected capped gain. Set `lambda = 2U/v`
   and accept a sample with `R < lambda G`. The score `lambda G - R` has
   expectation at least `U` and is at most `lambda h`; hence acceptance
   has probability at least `v/(2h) = Omega(1/(K L))`. Polynomially many
   independent trials find a nonempty batch with the stated density with
   high probability.
6. Before the final batch, the total number of new blues is below `h`;
   the final capped batch contributes at most `h`. Hence the sum of
   capped gains is below `2h`, and total projected red cost is
   `O(a K [L delta + sqrt(L delta)])`. Add the one-time exclusion cost
   and optimize `T`. Trying all integer `K` gives a feasible output for
   the correct guess; retain the cheapest output meeting the relaxed
   target. Amplify to cover all iterations and guesses.

The same factor transfers to budgeted precedence cover by trying every
target. However, the project's reduction to min-sum cover multiplies the
cost factor by `O(beta^3)`, and its decision-tree reductions add a factor
depending on `beta`. A polynomially growing `beta` therefore does not
automatically improve the final decision-tree exponents.

### Refinement: nonuniform red deletion

A further proof sketch improves the preceding tradeoff to

```
alpha = O(1 + m^(1/3) [L delta^(2/3) + delta^(1/3)]),
```

with the same definitions of `h`, `q0`, `delta`, and `L`, and the same
coverage guarantee. In particular, for `beta >= 2`, the bound is uniformly

```
O(1 + m^(1/3) [L beta^(-2/3) + beta^(-1/3)]).
```

For general precedence instances, `L = O(log(2m))`. For any fixed
`0 < eta < 1`, setting `beta = m^eta` gives the **pure** cost bound
`O_eta(m^((1-eta)/3))`, while covering only an `m^(-eta)` fraction of
the target. For example, `beta = m^(1/4)` gives a candidate
`(O(m^(1/4)), m^(1/4))` bicriteria approximation. This is not a
constant-coverage result. Setting `beta = Theta(log^(3/2)(2m))` gives
`O(m^(1/3))` cost with a polylogarithmic coverage loss.

The improvement replaces uniform deletion across degree buckets by a
schedule weighted toward larger buckets. Fix all dyadic scales `s_i` in
advance, from the largest power of two at most `K` down to one. Include
empty scales, and let `L` be their number. Define

```
w_i = 1/(2L) + sqrt(s_i)/(2 sum_j sqrt(s_j)).
```

These weights sum to one. At scale `s_i`, delete the top
`ceil(K T w_i)` current-red-degree elements before forming the bucket.
The total excluded cost is at most `KT+L = O(K(T+1))`. Every surviving
red in that bucket has bucket degree

```
D_i = O(m s_i/(K T w_i)).
```

This holds despite adaptive bucket membership: at the start of the stage,
each unassigned set has current red degree below `2s_i`. Save zero-degree
sets at every stage, as before. Sampling an anchored bucket with the scaled
probabilities from the previous subsection gives expected projected red
cost `O(s_i sqrt(m/(T w_i)) sqrt(rho))`.

For each bucket and pivot, solve the local LP and compute the score

```
P_i = sqrt(w_i) min(Z_i/s_i, sqrt(h Z_i)/s_i).
```

Select the bucket and pivot with largest score `P`. Assign `q0` currently
uncovered blues covered by the optimum to covering optimum sets, and let
`q_i` be the number assigned to bucket `i`. CMV's pivot argument gives an
LP value `Z_i >= q_i s_i/K` in each relevant bucket. If `P <= u`, then

```
q0 <= K u sum_i w_i^(-1/2) + (K u^2/h) sum_i s_i/w_i
   = O(K L^(3/2) u + K^2 u^2/h).
```

The first sum is `O(L^(3/2))` because `w_i >= 1/(2L)`. The second is
`O(K)` because the scales are geometric and
`w_i >= sqrt(s_i)/(2 sum_j sqrt(s_j))`. Therefore

```
P = Omega(min(q0/(K L^(3/2)), sqrt(q0 h)/K)).
```

The red-to-capped-gain ratio of the chosen bucket is at most

```
O(K sqrt(m/T) [L^(3/2)/q0 + 1/sqrt(q0 h)]).
```

As before, capped gains sum to less than `2h`; the expected-density
potential has inverse-polynomial success probability and can be amplified.
The total red cost is therefore

```
O(K [1 + T + sqrt(m/T) (L^(3/2) delta + sqrt(delta))]).
```

Choose `T = m^(1/3) (L^(3/2) delta + sqrt(delta))^(2/3)` and use
`(x+y)^(2/3) <= x^(2/3)+y^(2/3)` to obtain the displayed factor.
Square-root weights and scores can be approximated to constant factors by
rational arithmetic, with constants absorbed in the guarantee. As with the
earlier sketch, stop unsuccessful budget guesses after a polynomial trial
limit and amplify over all rounds and guesses.

## Remaining research problem

The cube-root exponent comes from balancing the deletion budget with the
heavy/light rounding cost. The above tuning lowers logarithmic factors but
does not alter that balance. Neither repeatedly applying CMV's local density
guarantee nor a straightforward global precedence LP is sufficient by
itself to establish the requested pure or sub-cube-root guarantee.

Source: Chlamtac, Makarychev and Vakilian, *Approximating Red-Blue Set
Cover and Minimum Monotone Satisfying Assignment*, Section 3 and Appendix A,
https://arxiv.org/html/2302.00213.
