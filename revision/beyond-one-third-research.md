# Research status: decision trees below the cube-root exponent

This is an index of the current investigation. No general approximation
factor `O(m^(1/3-epsilon) polylog(m,n))` has been established. All notes
are research arguments requiring independent review; novelty is not
claimed. Here `m` is the number of tests and `n` the number of hypotheses.

## Candidate improvement and a barrier

`global-lp-decision-tree-investigation.md` proposes a deterministic
`O(m^(1/3) log(2n))` approximation for worst-case and uniform-average
decision trees. Its covering oracle uses a fixed coverage loss. The tree
itself is complete. This is a candidate improvement in logarithmic
factors, not an exponent below `1/3`.

`sdp-strong-gap.md` gives a near-cube-root integrality gap for a specified
degree-two SDP, including the original LP, PSD, conditioned cost and
coverage equalities, once-conditioned original linear inequalities, and
closure-pair constraints. The instances are induced by binary
decision-tree separator tests with target exactly one quarter of the
hypotheses. The gap holds even when only a fixed fraction of that target
is required. This is not a hardness result for decision trees and it does
not apply to arbitrary stronger relaxations or algorithms.

`sdp-csp-gap-investigation.md` derives a smaller polynomial gap approaching
`m^(2/53)` for a stronger hierarchy, via the specific random-CSP
construction of Bhaskara, Charikar, Guruswami, Vijayaraghavan and Zhou.
Its scope and source assumptions are explicit in the note.

## Higher moments and constructive restricted guarantees

`higher-order-rounding-investigation.md` shows that degree-six Boolean
SoS detects the random degree-two gap family: a triple-codegree count
forces its fractional budget high enough that its remaining gap is at most
`O(m^(2/9))`. It also proves an exact-target `O(m^(1/4))` guarantee for
a restricted uniform singleton-blue class with bounded triple codegrees.
Neither claim is a general rounding theorem.

`bounded-color-rounding.md` proves a separate fixed-coverage guarantee
for singleton-blue instances when every color has at most `F` alternative
sets. It combines deterministic layers with the known minimum-union
algorithm, giving `O_epsilon(m^(1/4+epsilon) F^(3/4-epsilon))`.
For arbitrary sets the relevant number is the set-blue incidence count,
not necessarily the number of tests. High color frequency remains open.

`core-enumeration-investigation.md` proves a fixed-order core enumeration
lemma for instances with bounded leakage outside a planted prerequisite
core, and records why fixed-order core enumeration alone is insufficient.

`direct-tree-ideas.md` gives additive bounds obtained by first executing
the nonmaximal tests, and more general bounds for a chosen prerequisite
ideal. It also identifies a small-optimum regime for the worst-case
objective. These are parameter-sensitive, not general exponent bounds.

## The remaining general problem

`colored-union-investigation.md` and
`colored-union-transfer-investigation.md` identify the main obstacle to
importing the quarter-power minimum-union algorithm: its exact
least-expansion primitive counts witnesses, whereas decision-tree cover
must count distinct colors. The color-aware density problem is already
hard, and repeated exact uncolored minimum-union calls can perform badly.
The notes give explicit reductions and examples.

The most concrete open target is a polynomial-time, color-aware
decomposition that either finds cheap progress on many distinct blues in
the high-overlap regime, or certifies sufficient sparsity for a
higher-order counting/rounding bound. Existing triple counting handles a
restricted sparse case; no such general decomposition has been proved.

## Subsequent investigation

`idea-sos-conditioning.md` develops a pair-pivot rounding guarantee with
constant coverage loss. It would yield an `O(m^(2/7))` factor under an
explicit overlap-moment promise, and gives an example showing that the
promise cannot simply be forced by conditioning on a constant number of
variables. This is a conditional direction, not a general approximation.

`idea-triple-decomposition.md` gives a computable core-decomposition
certificate whose value bounds the approximation factor, while leaving
open whether every instance has a sufficiently small certificate.
`idea-pivot-hybrid.md` and `idea-colored-caterpillar.md` identify
obstructions to two proposed ways of achieving such a bound.
`idea-alternate-oracles.md`, `idea-xi-structure.md`, and
`idea-tree-direct.md` record further parameter-sensitive algorithms and
limitations of generic oracle and direct-tree approaches.
