# Local pivots, color quotas, and the remaining balanced regime

This note isolates a rigorous local progress lemma and an instance-sensitive
consequence. The subsequent optimization through degree preprocessing is a
research calculation with an explicit scale condition; it is not a new
unrestricted approximation theorem. The manuscript has not been changed.

The input is partial red-blue set cover. There are `m` available sets, a
target of `k` distinct blue elements, and red-union optimum `K`. Red sets
may be precedence closures, including each selected test's own red. A
set may cover many blues; the local lemma does not create incidence copies.

## A proved local pivot lemma

Suppose a collection `J` has the following properties:

1. Every set has between `r` and `2r` red neighbors, where `r>=1`.
2. Every red element occurs in at most `D` sets of `J`.
3. Some subcollection has red union of size at most `K` and covers at
   least `q` distinct blues.

Assume an available partial-cover oracle, on any family of at most `N`
sets, returns red cost at most `C N^delta OPT(t)` and covers at least
`ceil(t/beta)` blues, for every feasible target `t>=1`. Here `C>=1`,
`beta>=1`, and `0<delta<1` are fixed bounds. Its guarantee is against the
integral optimum. In particular, substituting an LP lower bound for `K`
would not be justified.

Then, by trying every red pivot and every feasible integer target, one can
find a solution with a positive number `g<=q` of credited distinct blues
and

```
cost / g <= C beta D^delta K^2 / (q r).
```

Proof: choose exactly `q` optimum-covered blues and assign each to one
optimum set covering it. There are at least `q r` paths from these blues,
through their assigned sets, to optimum red elements. The optimum red
union has at most `K` elements. Consequently some red `p` is incident,
through the assignments, to at least

```
d = ceil(q r/K)
```

distinct assigned blues. Its set neighborhood `J(p)` contains at most
`D` sets; the optimum sets in that neighborhood cover at least `d` blues
at red cost at most `K`. Run the oracle with target `d` on this family.
Credit exactly `ceil(d/beta)` of its covered blues, even if its actual
coverage is larger. Then `g>=d/beta`, `g<=d<=q`, and the asserted density
bound follows. A surviving optimum set has at least `r` reds, so `r<=K`
and hence `d<=q`. The correct pivot and target occur in the enumeration.

This argument applies directly to multi-blue sets: distinctness comes
from choosing one witness for each blue in the proof, not from treating
all blue incidences as different sets in the algorithm.

## A proved consequence for a fixed scale

Under the same hypotheses, repeatedly apply the pivot procedure to the
uncredited blues until at least `ceil(q/2)` have been credited. The original
optimum continues to cover more than `q/2` uncredited fixed blues before
the last iteration. Enumerate oracle targets only up to `q` and select the
candidate of minimum cost per credited blue, crediting only the promised
`ceil(t/beta)` blues from a target-`t` call.

Every iteration has a candidate of density at most

```
2 C beta D^delta K^2/(q r).
```

The total credited gain is less than `3q/2`: before the last iteration it
is less than `q/2`, and the last candidate credits at most `q` blues.
Adding the costs of the returned red unions therefore proves

```
cost <= 3 C beta D^delta K^2/r,
coverage >= ceil(q/2).
```

If the analyzed graph omits a common accounting set `H` of reds, add
`|H|` to this cost bound once. Actual returned red-union cost is at most
this accounting bound. Already purchased reds need not be charged again,
although doing so in the upper bound is harmless.

If the oracle is randomized, amplify all calls to a suitably small
inverse-polynomial error probability. The call count is polynomial, and
conditioning on earlier outputs still leaves the stated per-input
guarantee for a fresh call. Costs and credited coverage are observable.

## Substitution into degree preprocessing: conditional calculation

The degree preprocessing of Chlamtac, Makarychev, and Vakilian (CMV),
Lemma 3.1, gives at most `L=O(log(2|R|))` scales after omitting at most
`A K` reds in total. A scale with red degree in `[r,2r]` has

```
D <= 2 m r L/(A K).
```

The omitted red collections are nested, so one common accounting set of
size at most `A K` suffices. Assign fixed optimum witnesses to the
scales. Some scale covers at least `ceil(k/L)` fixed optimum blues.
Applying the fixed-scale consequence to that scale gives coverage at
least `k/(2L)` and cost at most

```
K [ A + 3 C beta (2mL/A)^delta (K/r)^(1-delta) ].       (1)
```

There is no polynomial loss of target coverage here: the global coverage
parameter is `2L`. Local `beta` enters the cost of the repeated progress
procedure, rather than multiplying the final coverage parameter again.
Enumerating scales, the budget guess `K`, and oracle targets handles the
unknown optimum data. The algorithm can keep the cheapest candidate
meeting the required `ceil(k/(2L))` credited quota.

Writing `s=K/r`, the algebraic balance in (1) is

```
A + O(C beta (mL)^delta A^(-delta) s^(1-delta)).
```

If a scale with `s<=s0` and the required number of optimum blues exists
for the chosen preprocessing parameter `A`, choosing `A` on the order of

```
(C beta)^(1/(1+delta))
  (mL)^(delta/(1+delta))
  s0^((1-delta)/(1+delta))
```

gives that same order of approximation factor, with coverage loss `2L`.
Rounding `A K` to an integer and capping it at the total red count only
affects constants; buying all reds handles the capped endpoint.

**Scale condition:** the bucket degree `r` is determined *after*
preprocessing, which itself depends on `A`. It is invalid to optimize
this expression while silently treating an unknown, changing `r` as a
fixed favorable parameter. The displayed optimized guarantee requires a
promise that a suitable scale with `K/r<=s0` exists at the selected `A`,
or a new proof of that property. The local and fixed-scale lemmas above
require no such extra promise.

For the available cube-root partial-cover oracle, `delta=1/3`, this
conditional factor becomes

```
O( (C beta)^(3/4) (mL)^(1/4) sqrt(s0) ).
```

Ignoring logarithms and constant oracle parameters, it improves on
`m^(1/3)` when `K/r < m^(1/6)`. This is a useful regime to isolate, but
there is no reason in general that a required optimum-bearing scale has
this property.

## The balanced regime left by these bounds

The following parameter values are mutually consistent at the level of
the counting constraints, and expose the unhandled case:

```
number of informative sets          Theta(m)
number of blue colors              Theta(m^(1/2))
target k                           Theta(m^(1/2))
per-color witness multiplicity F   Theta(m^(1/2))
useful residual red degree r        Theta(m^(1/2))
integral optimum K                  Theta(m^(2/3)).
```

They give

```
K/r                    = Theta(m^(1/6)),
k r/K                  = Theta(m^(1/3)),
m/K                    = Theta(m^(1/3)),
m^(1/4) sqrt(K/r)       = Theta(m^(1/3)).
```

Thus the pivot calculation, selecting one witness per desired color,
and executing all tests can all stop at the cube root. This is a parameter
obstruction to these *bounds*, not an approximation lower bound or a
hardness construction. It remains possible that a further algorithm
recognizes an exploitable structure in every instance with these values.

The deterministic rainbow-layer theorem in `bounded-color-rounding.md`
does not resolve this regime. With `a=1/4+epsilon`, it gives

```
m^a F^(1-a) = m^(5/8+epsilon/2),
```

before taking the better of this and the existing cube-root algorithm.
An elementary high-frequency alternative also fails: if each relevant
color has at least `F` witnesses, there are at most `m/F` colors, so
choosing one feasible witness per color costs at most `(m/F)K`.
Balancing this with the rainbow-layer bound gives

```
F = m^((1-a)/(2-a)),
factor = m^(1/(2-a)),
```

whose exponent tends to `4/7`, not a value below `1/3`. More generally,
splitting at a frequency threshold does not guarantee that a constant
fraction of the optimum-covered colors occurs on the favorable side.

## Decision-tree implication and its limitation

The fixed-scale procedure, together with the stated favorable-scale
condition on every required separator subinstance, supplies a partial
cover oracle with cost factor `alpha` from (1) or its justified
optimization and coverage factor `2L`. The manuscript's covering-to-tree
transfer, and the direct uniform-average transfer in
`global-lp-decision-tree-investigation.md`, then give

```
O(alpha L log(2n))
```

for both worst-case and uniform-average decision trees. An oracle with
polylogarithmic `beta` changes only polylogarithmic factors in this
calculation. Fresh randomized oracle calls must be amplified across the
polynomially many calls made by the entire tree construction.

No unconditional full-tree exponent below `1/3` follows: a separator
subinstance can enter the balanced regime, and the favorable-scale
condition has not been proved for general precedence instances.

## Sources and context

The red-degree preprocessing and assignment-to-pivot idea are from
Chlamtac, Makarychev, and Vakilian, *Approximating Red-Blue Set Cover and
Minimum Monotone Satisfying Assignment*, Section 3:
https://arxiv.org/html/2302.00213.

The motivation for repeated pivots and restricted neighborhoods is
Chlamtac, Dinitz, and Makarychev, *Minimizing the Union: Tight
Approximations for Small Set Bipartite Vertex Expansion*, Section 3:
https://arxiv.org/html/1611.07866.

The formula above is a black-box substitution of an existing partial
oracle into a local pivot. No novelty claim is made.
