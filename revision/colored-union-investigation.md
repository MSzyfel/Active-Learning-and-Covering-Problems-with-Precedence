# Colored minimum union and the minimum-expansion oracle

This note isolates an obstruction to importing the minimum-k-union
algorithm of Chlamtac, Dinitz, and Makarychev (CDM) into general partial
red-blue cover. It gives an exact reduction to partition-constrained
minimum union and proves that the corresponding exact minimum-expansion
subroutine is NP-hard. It does not rule out a useful approximation to that
subroutine, or a different algorithm with an exponent below one third.

## Exact witness formulation

For every incidence of a blue element b with an available set j, create a
witness vertex (b,j), with red neighborhood R_j. Partition these vertices
by b. Find k witness vertices, at most one from each partition class,
minimizing the cardinality of their combined red neighborhood.

This is exactly equivalent to covering k distinct blues. From a cover,
retain k covered blues and assign one witnessing set to each. Conversely,
the original sets named by a feasible witness collection cover its k
distinct colors at exactly the witness collection's red-union cost. The
same original set can witness several different blues; this causes no
extra red cost.

The number of witness vertices is the number of blue-set incidences,
which can exceed the number of original sets. Even when every original
set covers just one blue, ordinary minimum-k-union is obtained only when
the partition constraint is vacuous. Several alternative sets for one
blue remain a nontrivial partition class.

For a collection S of witnesses, let c(S) be the number of represented
colors. A colorful subcollection containing one witness per represented
color has the same color count and no larger red union. Consequently the
appropriate unconstrained density problem is

```
minimize |N_R(S)| / c(S),  over S with c(S)>0.
```

Replacing c(S) by |S| is not valid.

## An exact colored density oracle is NP-hard

Take an instance (G,t) of CLIQUE, with 3<=t<=|V(G)| and G simple. Make one
red element (i,v) for every position i in [t] and vertex v of G. Make one
blue color {i,j} for every unordered pair of distinct positions. For each
edge uv of G and each i<j, create two witnesses of color {i,j}, with red
neighborhoods

```
{(i,u),(j,v)}  and  {(i,v),(j,u)}.
```

Every witness has exactly two red neighbors. The construction has
t|V(G)| red elements and at most t(t-1)|E(G)| witnesses, so is polynomial.

Consider any witness collection with L distinct red neighbors and C>0
represented colors. Necessarily

```
C <= binomial(t,2),
C <= binomial(L,2).
```

The second inequality holds because each covered color has an edge
between two selected red elements, and an unordered pair of red elements
determines at most one color. If L<t, then

```
L/C >= 2/(L-1) > 2/(t-1).
```

If L>t, then L/C>=L/binomial(t,2)>2/(t-1). If L=t, the density is at most
2/(t-1) precisely when every one of the binomial(t,2) colors is covered.
Covering all those colors requires a selected red element in every
position. Since L=t, there is exactly one selected element (i,v_i) per
position. All pairs v_i,v_j must be adjacent in G; since G has no loops,
the vertices v_i are distinct. They form a t-clique.

Conversely, a t-clique supplies one label per position and all pair
witnesses, attaining density t/binomial(t,2)=2/(t-1). Therefore deciding
whether the minimum nonempty colored density is at most 2/(t-1) is
NP-hard, even with red neighborhoods of size two.

This also obstructs exact Lagrangian minimization. Put a=2/(t-1) and

```
lambda = a + 1/(2 (t-1) binomial(t,2)).
```

If G has no t-clique, every feasible density L/C exceeds a by at least
1/((t-1) binomial(t,2)): the numerator of L/C-a is a positive integer
divided by C(t-1). Thus minimizing |N_R(S)|-lambda*c(S), allowing the
empty collection, has a negative optimum if and only if G contains a
t-clique. All numbers have polynomial bit length.

This is exact NP-hardness. The proof gives no polynomial approximation
hardness and does not preclude an approximate colored density oracle.

## A color-collision example

Let h be even, and give every h/2-subset of a common h-element red core
the same blue color. There are M=binomial(h,h/2) distinct witnesses. None
dominates another by red-neighborhood inclusion. Selecting every witness
has ordinary expansion h/M but represents just one color.

Pruning that collection to one representative produces red cost h/2,
and hence colored expansion h/2. The density deteriorates by M/2. This
example survives deduplication and removal of inclusion-dominated
alternatives. Thus arbitrary pruning cannot preserve a bound expressed
using the number of selected witness vertices.

The same issue affects an early exit based on finding k candidate
vertices: all k may belong to one color. Sampling one candidate uniformly
from each color does not repair this uniformly. If a color has M
alternatives and exactly one belongs to a fixed optimum, that optimum's
witness survives with probability 1/M. Independent sampling of colors
without sampling their alternatives leaves the within-color collision
unchanged.

## The exact missing step in the CDM framework

CDM obtain an O(m^(1/4+epsilon)) approximation for ordinary minimum
k-union. Their minimum-expansion subroutine, Lemma 2.1, finds an exact
least-expanding subset by a flow computation. The hair and backbone
steps in Section 3.2 repeatedly use that subroutine; their output size and
progress accounting use witness cardinality. The partition-constrained
version would require counting represented colors, and the NP-hardness
above shows that its exact substitute cannot simply be supplied by an
efficient flow routine unless P=NP.

An ordinary cut formulation rewards each chosen witness separately. A
single reward per blue instead requires the condition that a rewarded
blue has at least one chosen alternative. Arcs from that blue to all its
alternatives would impose all alternatives, not the required existential
condition. The reduction above makes this distinction algorithmically
substantive, rather than just a deficiency of one proposed cut gadget.

Source: [CDM, Minimizing the Union: Tight Approximations for Small Set
Bipartite Vertex Expansion](https://arxiv.org/html/1611.07866), Lemma 2.1
and Section 3.2. The reductions and counterexamples in this note are
derived directly here.

## A valid substitute when blue frequency is bounded

There is a simple approximation transfer with an explicit frequency
loss. Suppose every blue belongs to at most mu original sets, and let
A(m) be an approximation factor for ordinary minimum-k-union with at
most m sets. General partial red-blue cover then has a constant-coverage
algorithm with red-cost factor

```
O(mu A(m) log(2m)).
```

Unlike cloning every incidence, this bound uses the number m of original
sets, even when each original set covers many blues. Here is the argument.

Fix an original feasible cover of k blues with red cost K. Until k/2
blues have been covered, that cover still contains at least k/2 uncovered
blues. For each available original set j, put

```
v_j = min(k, number of its currently uncovered blues).
```

Assign k/2 uncovered optimum blues to optimum sets. The sum of v_j over
those optimum sets is at least k/2. Sets with v_j<k/(4m) contribute less
than k/4 to this sum. Partition the remaining positive v_j into dyadic
buckets [w,2w). Their number L is at most 2+ceil(log_2(4m)); this follows
from the ratio between k and k/(4m), including the bucket intersecting
the lower cutoff. At least one bucket's optimum sets have total v_j at
least k/(4L). Thus that bucket contains at least

```
t = ceil(k/(8Lw))
```

optimum sets. Invoke the ordinary minimum-t-union algorithm on the red
neighborhoods in each bucket, skipping t larger than the bucket size.
For the good bucket, the output has red cost at most A(m)K. Its t sets
have at least tw>=k/(8L) blue incidences. Because a blue can occur in at
most mu of those sets, their union contains at least k/(8Lmu) currently
uncovered blues.

Among all bucket outputs, select one minimizing red cost divided by
min(k, its actual newly covered blue count). Its ratio is at most
8Lmu A(m)K/k. Repeat until at least ceil(k/2) blues are covered. Before the
last batch the total gain is below k/2, and the last capped gain is at
most k, so the sum of capped gains is below 3k/2. The red costs sum to
at most 12Lmu A(m)K. Counting a red more than once only overestimates
the final union cost. The same argument handles odd k, since before
termination the integer number already covered is strictly below k/2.
Zero-red-cost cases are
handled first by selecting all red-free sets.

Substituting CDM's A(m)=O(m^(1/4+epsilon)) yields a sub-cube-root bound
when mu grows sufficiently slowly, for example
mu<=m^(1/12-eta) with any fixed eta>0 and epsilon<eta. This is a
bounded-frequency result, not a general-instance improvement: mu can
be as large as m. Uniform representative sampling and the simple
pruning method above do not remove this dependence.

## Why the existing cover approximation is not a direct recursive fix

An (A(n),beta) constant-coverage cover algorithm can approximate the
unconstrained colored density objective within A(n)*beta: try every
possible color target, apply the cover algorithm, and return the output
of best actual density. The target equal to an optimal density solution's
color count provides the comparison. Thus an approximate oracle is
available in principle. Its quantitative loss matters in CDM's proof.

Consider the balanced caterpillar regime with n witnesses, k=sqrt(n),
uniform red degree r, and optimum average back-degree
d=k^(1/2+epsilon). With their positive slack constant c<1, the first
guessed red pivot gives a candidate pool of size at most
D=n/k^(1-c*epsilon)=k^(1+c*epsilon), containing at least
d/(4k^(c*epsilon)) optimum witnesses. Those optimum witnesses expand
into at most kr/d=r*k^(1/2-epsilon) red vertices, so their density is
at most 4r*k^(-(2-c)*epsilon). They are colorful when the original
optimum is colorful.

An exact oracle finds density at most this value. Substituting the
available O(D^(1/3)) constant-coverage algorithm only guarantees density
O(r*k^(1/3-2epsilon+(4c/3)*epsilon)), up to constants or logarithms in
the selected oracle. For epsilon<1/6 this does not even give a density improvement
over one degree-r witness, whereas the caterpillar early exit needs a
polynomial improvement. Merely recursively calling the existing
one-third-exponent algorithm therefore does not establish the next
inductive step. This is a failure of that direct substitution, not a
lower bound for all recursive algorithms or all possible retunings.
