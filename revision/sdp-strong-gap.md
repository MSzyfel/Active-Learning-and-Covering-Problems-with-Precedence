# A colored covariance-SDP gap with conditioned quotas and budgets

This note gives an asymptotic integrality gap
`Omega_delta(m^(1/3)/log^2 m)` for a precisely specified polynomial-size
SDP strengthening of the global LP. The instances are depth-two precedence
cover instances, and are exactly realizable as binary decision-tree
separator instances with target one quarter of the blue universe. The
integral lower bound holds even when only a fixed positive fraction of the
target must be covered.

The relaxation includes a PSD moment matrix containing assignments,
conditioned assignment and blue-quota equalities, and conditioned red-budget
inequalities. Thus this construction survives the covariance strengthening
that eliminates the polynomial-graph example in `sdp-gap-investigation.md`.
The final strengthening below also conditions both aggregate assignment-load
inequalities. No claim is made for higher levels of Sherali--Adams or
sum-of-squares.

## The precise relaxation

Start with every constraint of the global LP in
`global-lp-decision-tree-investigation.md`. In the instances here each
informative test covers one blue, so use a Boolean witness `Q_i` for that
test and identify its selection variable, own-test red variable, and
assignment variable with `Q_i`. For an integral solution one may retain
exactly one informative witness per chosen blue and exactly `k` chosen
blues, so this restriction preserves integral feasibility at any budget
that permits covering `k` blues. All prerequisite tests remain available.

Let `Y_r` denote prerequisite-test indicators, and let `Z_b` denote chosen
blue indicators. Introduce a degree-two pseudoexpectation on these
variables. Require:

* The moment matrix indexed by `1`, the `Y_r`, the `Q_i`, and the `Z_b`
  is PSD, with Boolean diagonal identities.
* Every pair satisfies the Boolean McCormick bounds
  `max(0,E[A]+E[B]-1) <= E[AB] <= min(E[A],E[B])`.
* The equalities `sum_(i:color(i)=b) Q_i=Z_b` and `sum_b Z_b=k`
  hold both in expectation and after multiplication by every matrix-index
  variable. Distinct witnesses of the same blue have zero pair moment.
* For every prerequisite relation `Q_i<=Y_r`, retain this inequality
  after multiplication by any matrix-index variable `W` or by `1-W`.
* The red-budget inequality `C<=K`, where `C` is the sum of all
  prerequisite and own-test red indicators, holds in expectation and after
  multiplication by every matrix-index variable or its complement.
* Both aggregate assignment-load inequalities of the original LP hold
  after multiplication by every matrix-index variable or its complement.
  Their verification uses the additional codegree property proved below.

All of these constraints are valid for integral solutions. The closure
pair inequalities of the original LP are also retained. In particular,
this is stronger than adding PSD only to red moments or conditioning only
the total assignment quota. Its size is polynomial in the explicit input.

## The incidence system

Let `q` tend to infinity through multiples of four, let all logarithms in
this construction be natural, and set

```
d = ceil(100 log q),  R=q^2,  N=q^3,  k=q/4,
z=1/4,               p=1/(4q^2),
tau=64 d^2/q,        L=ceil(1/tau),  K=2q.
```

Take `q` sufficiently large that `tau<=1/4`, `d/q<=1/4`, and `q>=16`.
There are `q` prerequisite types indexed by the cyclic group `Z/qZ`, and
`q` blue colors. Independently for each color `b` and seed `ell in [q]`,
choose a uniformly random `d`-subset `D_(b,ell)` of the cyclic group. The
`R=q^2` informative tests of color `b` are indexed by `(ell,t)`, with
prerequisite types

```
P_(b,ell,t) = D_(b,ell)+t.
```

Replace each prerequisite type by `L` separate unit-cost prerequisite
tests, and require all `L` copies whenever the type occurs. The informative
test covers just its color and has its own unit cost. Thus the total number
of tests is

```
m=N+Lq=q^3+O(q^2/d^2)=Theta(q^3).
```

Each informative test has `Ld+1<=K` tests in its closure. There is no
precedence among prerequisite tests or among informative tests.

Let `M_b` be the `R by q` incidence matrix of color `b`, and let `M` stack
all `q` color blocks. Every row has sum `d`, and every column of `M_b` has
sum `qd`. Put

```
H_b=M_b-(d/q) J_(R,q),     H=M-(d/q) J_(N,q),
P_a=I_a-J_a/a.
```

Both row and column sums of every `H_b` vanish. Crucially, without any
probabilistic spectral estimate,

```
||H_b||^2 <= q d^2.
```

To see this, each seed contributes one `q by q` circulant incidence matrix
with row and column sums `d`, and hence operator norm at most `d`.
Centering is multiplication by the orthogonal projection `P_q`, which
cannot increase that norm. Stacking the `q` centered matrices gives the
stated squared-norm bound.

## The moment matrix and its PSD certificate

Assign mean `tau` to every prerequisite type and mean `p` to every witness.
All `L` copies of a prerequisite type have identical moment vectors. Define

```
beta=tau(1-tau) q/(q-1),
gamma=p(1-tau)/(1-d/q),
lambda=gamma^2/beta,
Omega=(3/16) q/(q-1) P_q.
```

The centered covariance blocks, before duplicating prerequisite types, are

```
B_cov = beta P_q,
C_cov = gamma H,
A_cov = lambda H H^T
        + blockdiag_b [p P_R-lambda H_b H_b^T]
        + (Omega/R^2) tensor J_R.
```

Here `A` is the witness block, `B` is the prerequisite-type block, and
`C` is the witness/type cross block. Add the outer product of the mean
vector to obtain raw degree-two moments, and append the constant row and
column. Define each blue vector as the sum of its color's witness vectors.

For the chosen parameters,

```
lambda <= 4 p^2/tau,
lambda ||H_b||^2 <= 4p^2 qd^2/tau = p/64.
```

Because `H_b^T 1_R=0`, each matrix
`p P_R-lambda H_b H_b^T` is PSD. So is `Omega`. Finally,

```
[ lambda HH^T   gamma H ]
[ gamma H^T     beta P_q]
```

is PSD: it is the Gram block obtained from the common factor
`[gamma H/sqrt(beta); sqrt(beta) P_q]`, using `H P_q=H`.
Adding the two remaining PSD terms proves the covariance matrix PSD;
appending the constant and adding the means then proves the full moment
matrix PSD. Duplicating prerequisite vectors and summing witness vectors
to form blue vectors preserve PSD.

The raw prerequisite moments are

```
E[Y_r^2]=tau,
E[Y_r Y_s]=b0=tau^2-tau(1-tau)/(q-1)   for r!=s.
```

For witness `i` and type `r`, they are

```
E[Q_i Y_r]=p                                if r in P_i,
E[Q_i Y_r]=c=p(tau q-d)/(q-d)               otherwise.
```

Within a color, `E[Q_i^2]=p` and `E[Q_i Q_j]=0` for distinct witnesses.
For different colors, writing `nu_ij=|P_i intersect P_j|`,

```
E[Q_i Q_j]
  = p^2(1-3/(q-1)) + lambda(nu_ij-d^2/q).
```

These formulas follow directly from the covariance blocks. In particular,
the diagonal of `A_cov` is `p-p^2`, and the off-diagonal entries within a
color are `-p^2`, as required.

## Bounds and conditioning checks

The following elementary bounds hold for sufficiently large `q`:

```
0 <= p <= b0 <= tau,
p tau/2 <= c <= p,
0 <= E[Q_i Q_j] <= c   for different colors,
tau>=4p.
```

For completeness, `b0>=tau^2/2>=p` because `q tau=64d^2`, and
`c>=p tau/2` because `tau>=2d/q`. The lower bound for different-color
witness pairs follows from

```
p^2(1-3/(q-1))-lambda d^2/q
  >= p^2(1-3/(q-1)-1/16) >=0.
```

For the upper bound, use `nu_ij<=d` and

```
E[Q_i Q_j] <= p^2+4p^2d/tau <= p tau/2 <= c.
```

The middle inequality is equivalent to
`2p tau+8pd<=tau^2`, which follows directly from
`p=1/(4q^2)` and `tau=64d^2/q` for sufficiently large `q`.

All witness and prerequisite means are at most `1/4`; the displayed
bounds therefore give their McCormick constraints. The blue means are
`z=1/4`, and summation gives

```
E[Z_b^2]=z,
E[Z_b Z_c]=z(k-1)/(q-1)                   for b!=c,
E[Y_r Z_b]=tau z,
E[Q_i Z_b]=p                             if color(i)=b,
E[Q_i Z_b]=p(k-1)/(q-1)                  otherwise.
```

These also satisfy McCormick bounds.

Every covariance row sums to zero over all prerequisite types and over
all witnesses separately. Consequently the moment vectors obey

```
sum_r Y_r = q tau * 1,
sum_i Q_i = k * 1,
sum_b Z_b = k * 1.
```

The color-sum assignment equalities hold by the definition of `Z_b`.
Thus the assignment and quota equalities hold after conditioning on any
variable. The total red-cost vector, including all prerequisite copies
and all informative-test own reds, is

```
C=(Lq tau+k)*1=K0*1,
K0<=q(1+tau)+q/4<=3q/2<K.
```

Hence both variable-conditioned and complement-conditioned red-budget
inequalities hold exactly with budget `K0`, and therefore with `K=2q`.

For a prerequisite relation `Q_i<=Y_r`, its conditioning by witness
`Q_j` follows from `E[Q_iQ_j]<=E[Y_rQ_j]`: the nontrivial different-color
case uses the upper bound by `c`, and the same-color case is zero unless
`i=j`, when prerequisite consistency gives equality. Its conditioning by
type `Y_s` follows from `E[Q_iY_s]<=E[Y_rY_s]`, using `b0>=p` for
different types and `tau>=p` for equal types. Blue conditioning follows by
summing the witness inequalities in a color.

For complement conditioning, the only equality case requiring attention
is `s=r`, where both `E[Q_i(1-Y_r)]` and `E[Y_r(1-Y_r)]` are zero.
For different types the available red mass is `tau-b0>=tau(1-tau)>=p`.
For witness complements it is `tau-E[Y_rQ_j]>=tau-p>=p`, which is at
least `p-E[Q_iQ_j]`. For blue complements it is
`tau(1-z)>=p`, again sufficient. These establish every claimed lift of
the individual prerequisite inequalities, including duplicate types.

## The original global LP constraints

Use `x=y=tau` for each prerequisite test, and `x=y=a=p` for each
informative test; each such assignment belongs to that test's unique
blue. Let `z_b=1/4`, and use the raw red pair moments above, including
informative-test own reds, for the original `Y_pr` variables.

The red budget is `K0<=K`, and the blue quota is `q/4=k`. Each color
has `R p=1/4` assignment mass. Selection domination and per-set loads
hold since each informative test has just its one assignment and `k>=1`.
Each prerequisite copy has per-color assignment load

```
(qd)p=d/(4q)<=tau,
```

and total assignment load `d/4<=k tau`. For an informative test's own
red, both loads are its single assignment `p`, which is at most `kp`.
Prerequisite selection domination is `p<=tau`.

Every pair in an informative closure has moment at least its selection
value `p`: distinct prerequisite types have moment `b0>=p`, duplicate
types have moment `tau>=p`, and the informative own red has incident
moment and diagonal both equal to `p`. A prerequisite test's singleton
closure satisfies its diagonal bound. All red pair row-budget constraints
follow from the exact total red-cost vector. The individual closure-size
filter holds because

```
Ld+1 <= d/tau+d+1 = q/(64d)+d+1 <=2q.
```

This verifies every constraint of the original global LP in addition to
the explicitly listed SDP strengthening.

## Conditioning the aggregate assignment-load inequalities

The random construction can additionally be required to satisfy

```
T_b(r,s)=(M_b^T M_b)_(r,s) <=8d^2    for all b and r!=s.
```

Indeed, for a fixed color and distinct types, `T_b(r,s)` is the sum of
`q` independent random variables, one per seed. Each lies in `[0,d]`, and
its expectation is `d(d-1)/(q-1)`. The sum has mean at most `2d^2` and
variance at most `2d^3`. Bernstein's inequality bounds its probability of
exceeding `8d^2` by `exp(-4d)`. A union bound over fewer than `q^3`
choices tends to zero. Thus this property and the expansion property
proved below hold simultaneously with positive probability.

For a color `b` and prerequisite type `r`, put

```
F_(b,r)=sum_(i:color(i)=b,r in P_i) Q_i,
D=qd,     ell=E[F_(b,r)]=Dp=d/(4q).
```

Its first-moment inequality is `ell<=tau`. Conditioned on a witness `Q_j`
of its own color, its moment is `p` if `r in P_j` and zero otherwise, so
`E[F_(b,r)Q_j]<=E[Y_rQ_j]`. For a different color, direct summation gives

```
E[F_(b,r)Q_j]
 = Dp^2(1-3/(q-1))
   +lambda(sum_(s in P_j)T_b(r,s)-D d^2/q).
```

If `r` is not a prerequisite of `j`, the right side is at most

```
Dp^2+8lambda d^3 <=3d/(32q^3) <=c/8.
```

If `r in P_j`, use `T_b(r,r)=D` to obtain the upper bound

```
Dp^2+lambda(D+8d^3)
 <=p/(64d)+3d/(32q^3) <=p/8
```

for sufficiently large `q`. Thus a different color contributes at most
`E[Y_rQ_j]/8` in either case.

Conditioned on type `Y_s`, the load moment is `ell` when `s=r`, and when
`s!=r` it is

```
T_b(r,s)p+(D-T_b(r,s))c
 <=ell tau+8d^2p <=tau^2/16 <=b0/8.
```

Also `ell<=tau/8`. These prove all variable-conditioned per-color load
inequalities; blue conditioning follows by summing witness inequalities.
Complement conditioning follows from nonnegativity and the large
first-order slack: `ell<=tau-p`, `ell<=tau-b0`, and
`ell<=tau(1-z)`. When conditioning on `1-Y_r`, both sides are zero.

For the total-load inequality, let `F_r=sum_b F_(b,r)`, with
`E[F_r]=d/4`. Witness conditioning gives

```
E[F_r Q_j] <=(1+(q-1)/8) E[Y_rQ_j]
             <=(q/4) E[Y_rQ_j]=k E[Y_rQ_j].
```

Type conditioning gives `E[F_rY_s]<=q E[Y_rY_s]/8`, which is also at
most `k E[Y_rY_s]`. Blue conditioning again follows by summation.
Complement conditioning uses

```
d/4 <= k(tau-p),
d/4 <= k(tau-b0),
d/4 <= k tau(1-z),
```

which all hold for sufficiently large `q`; conditioning on `1-Y_r`
again gives zero on both sides. Informative-test own reds have only their
single assignment, so their per-color and total load lifts follow from
the witness pair bounds directly.

This verifies the once-conditioned versions of both original aggregate
load constraints. The remaining original linear constraints have already
been checked under conditioning or are equalities or nonnegative multiples
of Boolean bounds. The original quadratic closure-pair constraints are
retained at degree two; they have not been lifted to degree three.

## Integral cost and the constant-fraction target

With positive probability, the random incidence system has the following
property: every choice of at least `ceil(q/log q)` tests of distinct
colors uses more than `q/2` prerequisite types.

Indeed, fix `t` distinct colors, one test per color, and a set `T` of
`floor(q/2)` types. The chosen prerequisite sets are independent across
colors, and each is a uniform `d`-subset, even after its specified cyclic
shift. The probability that all are contained in `T` is at most
`2^(-dt)`. The number of choices is at most `2^q q^(3t)`. Hence for each
`t>=ceil(q/log q)`, the failure probability is at most

```
exp(q log 2 + 3t log q -100t(log 2)(log q)) <= exp(-60q).
```

Summing over the at most `q` possible values of `t` still gives a
probability tending to zero. Fix any incidence system with this property.

For every fixed `delta in (0,1]` and sufficiently large `q`, covering
`ceil(delta k)` blues requires one informative test in each of that many
distinct colors, with `ceil(delta k)>=ceil(q/log q)`. More than `q/2`
prerequisite types are therefore required, at actual test cost exceeding
`Lq/2`. The SDP is feasible at `K=2q`, so its bicriteria gap is at least

```
(Lq/2)/(2q) = L/4 >=1/(4tau)
             = q/(256d^2)
             = Omega(m^(1/3)/log^2 m).
```

Finally take the `q` colors as hypotheses, make every prerequisite test
uninformative, and let each informative test of color `b` have binary
replies `{b}` and its complement. For `q>4`, its `xi` set is exactly
`{b}`, while prerequisite `xi` sets are empty. Thus `U_xi` has size `q`
and the separator target is exactly `|U_xi|/4=k`. All hypotheses are
distinguishable. The same gap applies to the separator-cover relaxation;
it is not a hardness theorem for decision trees.

## Scope and relation to the literature

Chlamtac, Dinitz, and Makarychev give a nearly square-root gap for the
natural SSBVE SDP in Section 4.2 of
[Minimizing the Union](https://arxiv.org/pdf/1611.07866). Their displayed
red moment block has off-diagonal entries `tau/2`, so its conditional
red-cost rows do not respect a small budget of order `q tau`. That gap
cannot simply be imported into the stronger formulation considered here.
The present construction instead has fixed total red-cost and witness
moment vectors, groups witnesses into actual blue colors, and handles
own-test costs by duplicating prerequisite types.

This result rules out a polynomial improvement in the exponent by rounding
this particular strengthening: for every fixed `epsilon>0`, its gap
eventually exceeds `m^(1/3-epsilon)`. It leaves open higher moment
relaxations and algorithms using additional structure beyond these moments.
