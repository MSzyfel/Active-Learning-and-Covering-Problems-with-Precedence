# Scenario and storyboard

**Target runtime:** about 20–22 minutes at roughly 155–165 words per minute. A more deliberate 125–135 words per minute delivery runs about 24–27 minutes. The timing is a rehearsal target; let technical passages breathe rather than rushing.

**Audience:** STOC program committee and subreviewers in theoretical computer science. The intended contribution is the reduction framework and the proof ideas behind both the approximation and hardness results.

**Visual style:** dark chalkboard, warm white text, cyan for precedence, gold for covered items, coral for uncovered or forbidden choices. Draw each object as it is introduced, keep formulas short, and return to the decision-tree/covering correspondence throughout.

## 1. A search problem with a rulebook (about 1:40)

**Visual:** Use the same twelve-hypothesis pool to compare three alternative tests: $6+6$, $9+3$, and $4+4+4$. Keep the outcomes color-coded and make clear that these are alternative partitions, not successive tests on one branch. Then show a nontrivial precedence DAG with a fork, merge, and second branch; compare two valid topological orders with an invalid order that tries to run a blocked test first.

**Narration:** Use Chapter 1 in `voiceover.txt`.

## 2. The two objectives (about 1:40)

**Visual:** Draw a branching eight-outcome binary decision tree with mixed leaf depths $2,3,3,3,3,3,4,4$. Trace a deepest path, then clear the tree and calculate $max=4$ and total path length $=25$. Explain that the uniform average is $25/8$. Keep the formulas on their own calculation beat.

**Narration:** Use Chapter 2.

## 3. Why greedy information gain stops being enough (about 1:50)

**Visual:** A large test promises to split the remaining hypotheses well, but its parent test has not run. Animate the valid prerequisite chain, then compare two legal sequences. Make the precedence-closed ideal visible as a shaded set of DAG nodes.

**Narration:** Use Chapter 3.

## 4. Sepcover is a path prefix, not a layer (about 2:30)

**Visual:** Show the contracted 16-leaf tree and state that each badge gives an exact subtree leaf count. Move to a clean calculation card: root removal leaves $(12,4)$, so the 12-component exceeds $8$; removing the path $(r,a)$ leaves $(8,4,4)$, which meets the half-size condition. Separately compare the three test partitions $6+6$, $9+3$, and $4+4+4$ on a 12-hypothesis universe. With the $3|\mathcal H|/4=9$ threshold, every reply in each test qualifies for $\xi(t)$.

**Narration:** Use Chapter 4.

## 5. The recursive algorithm and its shrinkage invariant (about 2:30)

**Visual:** Select a precedence-respecting cover of a quarter of the separated hypotheses, execute its tests in order, split into reply classes, and recurse. Repeatedly shrink a pool. Show the factor `(5 beta - 1)/(5 beta)` and a logarithmic stack of recursive levels.

**Narration:** Use Chapter 5.

## 6. The average-case bridge and budget doubling (about 2:50)

**Visual:** Each hypothesis contributes its first coverage time. Contrast that sum with total path length. Grow budgets geometrically, showing early-covered elements receive smaller contribution. Flow from budgeted precedence-constrained cover to Partial Red-Blue Set Cover, then back to min-sum cover and average decision trees.

**Narration:** Use Chapter 6.

## 7. Approximation guarantees and forest structure (about 2:00)

**Visual:** A reduction map ends at Partial Red-Blue Set Cover. Display the general `O*(m^(1/3))` covering guarantee (with logarithmic factors made explicit in the article), then branch to inforests and outforests. Draw maximum coverage on one branch and group Steiner orienteering on the other; show the resulting logarithmic vs. squared-logarithmic decision-tree factors.

**Narration:** Use Chapter 7.

## 8. Hardness: planted dense subgraph (about 2:30)

**Visual:** Generate a seeded sample with $N=36$, $k=6$, and independent edge draws at the stated outside and planted-set probabilities. Select the planted vertices randomly and do not force them to form a clique. Put the model on a separate panel. Then derive $R=\binom r2$, $M=k^r\rho^R=\Theta(N^\gamma)$, and $\gamma>1/2$ on a clean algebra card. Explain the reduction gadget for a candidate $r=3$ clique (a template, not a claim about the sampled graph): representative sets, auxiliary sets, witness intersection, and precedence arcs. Give the YES expectation, concentration, and cost calculation on its own card; separate the NO-side clique-count bound and bicriteria consequence. Finish with the marked-block, repetition, and union-bound steps for covering every universe item, separated so each calculation remains legible.

**Narration:** Use Chapter 8.

## 9. Hardness: Label Cover and expander walks (about 2:30)

**Visual:** Draw the bipartite Label Cover graph around a left vertex $u$, with its incident constraints $e_i=(u,v_i)$. Beside it, draw the local expander whose vertices are those incident constraint positions; a $t-1$-step walk gives the ordered list $e_1,\ldots,e_t$ and the walk-indexed star $(u,e_1,\ldots,e_t)$. Show the exact projection compatibility needed for the witness and its predecessor bundles. For soundness, set $B_0=2T/(\theta H)$, mark vertices with more than $B_0$ selected label bundles as heavy, and derive the $\theta H/2$ light-star count. Show the expander-walk probability bound, the random-label contradiction, and the resulting cost and min-sum lower bounds. Note that the reduction has height-two precedence and singleton-or-empty sets.

**Narration:** Use Chapter 9.

## 10. What the framework says, and what it leaves open (about 1:30)

**Visual:** Reassemble the story as a loop: constrained decision trees → separator cover → partial cover → recursive identification. Place the hardness results beside the approximation results. End on two open questions: can a local greedy rule work, and can the average-case reduction handle non-uniform priors?

**Narration:** Use Chapter 10.

## Notes for the author recording

- Keep the proof explanations at the level of the paper: the talk must not introduce a new claim or supply a proof missing from the submission.
- Pause after the sepcover construction and the heavy/light soundness idea; those are the two conceptual pivots.
- Replace the scratch narration with an author speaking on camera. Keep the visual sequence and use this script as rehearsal notes, not as a substitute for the author's own explanation.
