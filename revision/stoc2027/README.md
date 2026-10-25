# STOC 2027 manuscript review

This record tracks 100 separately scoped, focused revision rounds requested by the authors. Each round has a question, source evidence and an outcome; a round need not produce an edit. Rounds 1--12 were already recorded when this continuation began at commit `46ddc3c`. Rounds 13--100 were distributed across ten review agents, then every exact proposed change was circulated to all ten for consultation before application. Their unanimous decisions and exact replacements are recorded in `consultations.json`.

Every changed manuscript round is compiled in both editions, committed separately, and pushed to `szyfel` before proceeding. No-change round entries are included in the next changed-round commit or the final audit commit. The full round record is `rounds.json`; its validation entries describe checks actually run.

The official call for papers was checked on 25 October 2026: https://acm-stoc.org/stoc2027/stoc2027-cfp.html. `main.tex` is the letter-paper submission edition; `main_arxiv.tex` is the separate arXiv edition. The manuscript review prioritizes readable exposition in the first twelve pages, complete arguments, accurate source attribution, linked references and truthful AI disclosure.

The latest author instruction preserves the existing table structure and moves shared hardness assumptions into the setting column. The approximation table remains byte-for-byte unchanged from the continuation baseline. The hardness table keeps five columns, result formulas, theorem references and result groupings; only assumptions and the space they require are redistributed. Total specified column width stays 0.96 linewidth.

The retained table font sizes include footnotesize text and a 0.80 scaling factor, below the call's requested 11-point size. The review therefore does not certify full formatting compliance. External submission consent, conflicts, author submission limits and the author-presented video require author action and are outside this editing task.

Two supplementary checks were reported by the responsible reviewers: exact-state verification of 523 feasible small random decision-tree instances (seed 73038), and 495 exact-rational PDS parameter samples for r=2,...,100. These support the source review and do not replace proofs. Round 88 records the limited verification of an arXiv theorem without asserting independent verification of journal theorem numbering.
