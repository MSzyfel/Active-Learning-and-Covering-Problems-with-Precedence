# A balanced obstruction to two pivot–layering shortcuts

This note gives a self-contained family in the balanced regime of
`pivot-regime-investigation.md`. It does not prove hardness or rule out
a new sub-cube-root algorithm. It shows that the numerical CMV bucket
properties alone imply neither of the following hoped-for improvements:

1. low color multiplicity inside an optimum-bearing pivot neighborhood;
2. a smaller local integral benchmark when that multiplicity is high.

In the construction, every color represented at a useful pivot has high
multiplicity, and covering even a constant fraction of those colors
already costs a constant fraction of the global optimum. All witnesses
have exactly the same red degree, so separating witnesses by red degree
does not remove this phenomenon. Every witness also has its own distinct
red element, as required by the precedence interpretation.

## A simple hybrid calculation that does not suffice

Suppose a pivot contains at most `D` witnesses and at least `Q` fixed
optimum colors. Delete all local colors whose frequency exceeds
`2D/Q`. There are fewer than `Q/2` such colors, so at least `Q/2` fixed
optimum colors survive. Applying the bounded-color theorem to this
restricted neighborhood, with MkU exponent `a`, gives local cost

```
O(K D^a (D/Q)^(1-a)) = O(K D / Q^(1-a)).
```

Thus its density is `O(K D/Q^(2-a))`. In the balanced regime,
`D = Theta(m^(1/2))`, `Q = Theta(m^(1/3))`, and the global target is
`k = Theta(m^(1/2))`. Repeating progress to a constant fraction of `k`
gives the factor

```
k D / Q^(2-a) = m^((1+a)/3).
```

At `a = 1/4`, this is `m^(5/12)`, larger than the cube root. This trimming
does fix a maximum-frequency estimate spoiled by a few irrelevant colors,
but it does not resolve uniformly high multiplicity among useful colors.

## Explicit balanced family

Let `q >= 5` be an odd prime. Arithmetic below is over `F_q`. There are
`q^3` colors `c = (c_1,c_2,c_3)` and `q^3` witnesses of every color,
indexed by `b in F_q^3`. Therefore

```
m = q^6,       k = F = q^3.
```

Use three disjoint red universes:

* core reds `U = F_q^3 x F_q`, of size `q^4`;
* outside reds `V = F_q^3 x F_q^3`, of size `q^6`;
* one private red `z_(c,b)` for every witness, of total size `q^6`.

The total red universe has size `Theta(m)`.

### Core hyperplanes

Put `P(c) = c_1 c_2 + c_3^2` and define

```
S_c = {(u,v) in U : v = c dot u - P(c)}.
```

Every `S_c` has `q^3` elements. If `c != d`, the equation obtained by
subtracting the two defining equations is a nonzero affine equation in
`u`, so

```
|S_c intersect S_d| = q^2.
```

For a fixed core red `p=(u,v)`, let `N(p)` be the number of hyperplanes
containing it. Completing the square transforms its color equation to

```
(c_1-u_2)(c_2-u_1) + (c_3-u_3/2)^2
  = u_1 u_2 + u_3^2/4 - v.
```

For a fixed third coordinate, the equation `xy=w` has `q-1` solutions
if `w != 0` and `2q-1` solutions if `w=0`. Hence

```
N(p) = q^2-q + q rho,
```

where `rho` is the number of square roots of the right-hand side and
belongs to `{0,1,2}`. In particular,

```
q^2-q <= N(p) <= q^2+q.                            (1)
```

### Outside graphs

For `c,b in F_q^3`, define the diagonal affine graph

```
G_(c,b) = {(x,y) in V : y_i = c_i x_i + b_i for i=1,2,3}.
```

Every graph has size `q^3`. Graphs belonging to two different colors
intersect in at most `q^2` points: at least one coordinate equation fixes
the corresponding `x_i`. For each outside point and each color, exactly
one label `b` gives a graph containing that point. Thus the full family
of graphs has outside-red degree exactly `q^3`.

### Witness neighborhoods

Fix subsets `A,C of F_q` of respective sizes `(q+1)/2` and `(q-1)/2`.
For each color `c`, use the following witnesses, always adding its own
private red `z_(c,b)`:

1. The label `b=0` is the good witness, with public neighborhood `S_c`.
2. For each `t != 0`, the label `b=(t,0,0)` is a mixed witness, with
   public neighborhood

   ```
   { (u,v) in S_c : u_1 in A+t }
     union
   { (x,y) in G_(c,b) : x_1 in C }.
   ```

3. Every other label has public neighborhood `G_(c,b)`.

The two parts of a mixed witness have sizes `(q+1)q^2/2` and
`(q-1)q^2/2`. Consequently every witness has exactly

```
r = q^3+1
```

reds. In particular, the construction has one red-degree scale.

For a core point `p=(u,v)` lying in `S_c`, its multiplicity among the
witnesses of color `c` is

```
f(p) = 1 + |{t != 0 : u_1 in A+t}|
     = |A| + 1[u_1 not in A]
     in {(q+1)/2, (q+3)/2}.                       (2)
```

It is the same for every color represented at that point. Thus the
pivot neighborhood at `p` has exactly `N(p)` colors, each with exactly
`f(p)` witnesses, and has size `N(p)f(p) = Theta(q^3)`.

Core-red degrees are at most `(q^2+q)(q+3)/2 <= q^3` for `q >= 5`.
An outside red has degree at most `q^3`, since each witness uses at most
its own distinct graph. Private-red degree is one. Therefore the global
maximum red degree is at most `q^3`.

## The global and local integral benchmarks

Selecting the good witness of every color covers all `k=q^3` colors
and costs exactly `q^4+q^3`: every core point belongs to a good witness
by (1), and the selected private reds are distinct. Thus

```
OPT(k) <= q^4+q^3.
```

For a matching order lower bound, consider any selected witnesses of
at least `2q` distinct colors, retaining just one witness for each color.
There are either at least `q` good witnesses or at least `q` nongood
witnesses.

If there are `q` good witnesses, their public neighborhoods each have
size `q^3` and pairwise intersections `q^2`. The standard second-moment
union inequality gives

```
|union S_c| >= (q q^3)^2 / (q q^3 + q(q-1)q^2)
             > q^4/2.
```

If there are `q` nongood witnesses, let `E_1,...,E_q` be their outside
parts. Every `E_j` has size at least `q^3/3`, and pairwise intersections
are at most `q^2`, because their colors differ. Write `S=sum_j |E_j|`.
The same inequality gives

```
|union E_j| >= S^2 / (S + q(q-1)q^2)
             >= (q^4/3)^2 / (q^4/3 + q^4)
             = q^4/12.
```

The second inequality uses that `x^2/(x+B)` increases for `x>=0`.
Thus every solution covering at least `2q` colors costs at least
`q^4/12`, and in particular

```
K = OPT(k) = Theta(q^4) = Theta(m^(2/3)).            (3)
```

The same lower bound applies to every core-pivot subinstance. Such a
pivot has `Q=N(p)=Theta(q^2)` colors, with all their good witnesses
available. Its full-color optimum is at most `q^4+Q`. Its optimum for
half of its colors is at least `q^4/12`, since
`ceil(Q/2) >= 2q` for `q>=5`. More generally, for every fixed positive
coverage fraction the same lower bound holds once `q` is large enough.
Consequently the relevant local integral benchmark is `Theta(K)` even
for constant-fraction local coverage.

### Core pivots also contain the true optimum's witnesses

The preceding benchmark is not merely an explicitly supplied feasible
solution. A sharper counting bound shows that every optimum uses good
witnesses for all but `O(q)` colors. First trim an optimum to one
witness per color; this retains optimality.

For two colors `c,d`, let `e(c,d)` be the number of equal coordinates.
Their outside graphs intersect in at most `q^e(c,d)` points, irrespective
of their labels. For each fixed `c`,

```
sum_(d in F_q^3) q^e(c,d) = (2q-1)^3 < 8q^3.
```

If an optimum has `t` nongood witnesses, their outside parts therefore
have total size at least `t q^3/3` and sum of ordered pairwise
intersections, including self-intersections, at most `8t q^3`. The
second-moment inequality gives

```
outside union >= (t q^3/3)^2/(8t q^3) = t q^3/72
```

when `t>0`. Since the whole optimum costs at most `q^4+q^3`, it follows
that `t <= 72(q+1)`. Every core pivot consequently contains the fixed
good optimum witnesses of at least

```
N(p)-72(q+1) = q^2-O(q) = Theta(q^2)
```

distinct colors, for sufficiently large `q`. Thus the bad anchored
multiplicity and the `Theta(K)` local benchmark occur at pivots that
are genuinely useful to the true optimum's witness assignment.

## What the family rules out

The balanced parameters are all realized simultaneously:

```
m=q^6,  k=F=q^3,  r=q^3+1,  K=Theta(q^4),
D=O(q^3),  Q=Theta(q^2),  K/r=Theta(q).
```

For every useful core pivot, the anchored multiplicity parameter of
`bounded-color-rounding.md` satisfies

```
mu >= K f(p)/r = Theta(q^2) = Theta(m^(1/3)).        (4)
```

This exceeds the limiting `m^(2/9)` threshold needed by the conditional
pivot-layer theorem. It is not caused by a few nuisance colors: all
`Q` locally represented colors have the same multiplicity (2), and all
are fixed optimum colors. Deleting colors above a frequency threshold
either retains all these colors or removes all of them.

Nor can one rescue the calculation simply by replacing its local `K`
benchmark with a quantity smaller by a polynomial factor: the local
lower bound above is `Omega(K)` even for half coverage.

For an exclusion parameter `T=o(q^2)`, the original family already
satisfies the numerical CMV bucket-degree bound

```
D <= O(m r L/(K T)),
```

with one bucket and no excluded reds. Therefore a decomposition with
these properties need not have small anchored multiplicity. Any
preprocessing rule that deletes only reds exceeding that displayed
degree cap makes no deletion here. This statement is about what the
listed decomposition properties imply; it does not say that every
possible implementation or a more informed exclusion rule must retain
the core. Indeed, identifying and buying all `q^4` core reds would solve
the instance at constant approximation, and that is within the budget
of an informed preprocessing rule.

For the ordinary local layering estimate, every nonempty layer has
`Q=Theta(q^2)` witnesses and there are `f=Theta(q)` layers. Its sum
`sum_h n_h^a` is `Theta(q^(1+2a))`. Without a new argument correlating
the layer order with the useful witnesses, this reproduces the
unhelpful exponent in the first calculation. The explicit labels in
this presentation reveal which witnesses are good; this is not an
algorithmic lower bound on choosing a better order.

## Consequence for further work

A successful general hybrid needs information beyond the current
degree, frequency, and local-optimum parameters. Potential routes
include identifying useful core reds, coordinating representative
choices across colors, or exploiting correlations among overlapping
pivot neighborhoods. A purely numerical dichotomy asserting either
low anchored multiplicity or a substantially cheaper local benchmark
is false, even with equal witness degrees, own-test reds, `Theta(m)`
total reds, and constant-fraction coverage throughout.

The construction can be realized as a height-two precedence instance:
make each public red an uninformative prerequisite test and make each
witness an informative test with exactly its public reds as
prerequisites. Its private red is its own test. The resulting total
number of tests remains `Theta(m)`. No manuscript claim has been
changed, and no unrestricted approximation improvement is asserted.
