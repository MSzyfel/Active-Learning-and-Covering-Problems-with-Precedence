# Repository guidance

This repository contains the LaTeX manuscript **Precedence-Constrained Decision Trees and Coverings**, studying approximation algorithms and hardness for decision trees and set covering under precedence constraints.

## Build and validation

Run commands from the repository root so that relative `\input` paths and the local document classes resolve. Use a TeX distribution providing pdfLaTeX, BibTeX, TikZ, algorithm2e, natbib, bbm, mdframed, and the other packages in the entry-point preambles.

For a one-shot build of a single document, run this PowerShell sequence, stopping if any command fails:

```powershell
$job = 'main'
pdflatex -interaction=nonstopmode -halt-on-error "$job.tex"
bibtex $job
pdflatex -interaction=nonstopmode -halt-on-error "$job.tex"
pdflatex -interaction=nonstopmode -halt-on-error "$job.tex"
```

Set `$job` to `main_arxiv` or `extended_abstract` to build that variant. For a quick compile check of the main document:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Use the complete sequence after citation or cross-reference changes; a single pass does not resolve those reliably. Inspect the target's `.log` and `.blg` for undefined references/citations and the PDF for table, diagram, and algorithm layout.

The existing Windows scripts `.\cont_build.bat`, `.\cont_build_arxiv.bat`, and `.\cont_build_extended_abstract.bat` repeatedly run pdfLaTeX, BibTeX, and two more pdfLaTeX passes. They are continuous loops, not one-shot checks; avoid invoking them for automated validation.

`extended_abstract.tex` currently inputs four files under `ea_sections/`, but that directory is absent from the tracked checkout. A build of this target requires resolving those missing sources; do not substitute the full-paper sections without an explicit request.

Generated PDFs and LaTeX/BibTeX auxiliary files are ignored by `.gitignore`.

## Document architecture

- `main.tex` is the full paper using the article class, shared notation from `macros.tex`, and the `plain` bibliography style.
- `main_arxiv.tex` uses the same full-paper sections but has its own inline macro definitions, A4 formatting, the `alpha` bibliography style, and acknowledgments. Changes to shared sections affect both versions; macro changes in `macros.tex` alone do not affect the arXiv version.
- `extended_abstract.tex` is the anonymized COLT 2026 variant, using the local `colt2026.cls` / JMLR class stack and inline macros. It expects shortened `ea_sections/` material in the body and includes full-paper sections in an appendix. The `ea_figures/`, `ea_tables/`, and `ea_pseudocodes/` assets are separate copies, not automatically synchronized with the full-paper assets. Preserve the `anon` setting unless asked to prepare a final version.
- All variants use the BibTeX database `bib-pcal.bib`.

The full-paper dependency chain is:

1. `sections/preliminaries.tex` defines notation, precedence closure, cost measures, optimization problems, and bicriteria approximation conventions.
2. `sections/approximating_learning.tex` reduces worst-case decision trees to fractional set cover and average-case decision trees to fractional min-sum set cover, using a common recursive decision-tree procedure with a covering black box.
3. `sections/set_covering_with_constrainst.tex` is an include wrapper for `sections/mdpcs_section.tex` and `sections/set_covering_section.tex`. The former supplies max-density precedence-closed subfamily primitives; the latter builds budgeted/fractional covering algorithms from them and handles special precedence structures.
4. `sections/hardness.tex` supplies complementary hardness reductions. `sections/introduction.tex` summarizes the relationships and guarantees through reduction diagrams and approximation/hardness tables.

Algorithm bodies live in `pseudocodes/` and are included by the proof sections. Figures are LaTeX/TikZ fragments, typically wrapped in figure environments by the including section; tables generally contain their own table environments. These assets rely on the parent document's packages and macros rather than standalone preambles.

## Manuscript conventions

- Reuse semantic macros for problem and procedure names (`\ProblemPCWCDT`, `\ProblemPCACDT`, `\ProblemPCSC`, `\ProblemBPCSC`, `\ProblemPCMSSC`, `\ProcedureFPCMSSC`) rather than spelling names independently in prose, tables, or diagrams. Preserve the distinction between fractional `f-` and budgeted `b-` variants.
- Use the existing notation macros such as `\cH`, `\cT`, `\cU`, `\cS`, `\br`, `\brc`, `\spr`, `\closure`, and `\coverageTime`. Check each affected entry point before introducing a macro into shared sections: the arXiv and extended-abstract definitions are independent and already differ from `macros.tex`.
- The average-case decision-tree objective is the **sum** of identification costs, not that sum divided by the number of hypotheses. Preserve this convention in statements and derivations.
- Precedence-closed families contain all predecessors; sequences and decision-tree paths must execute strict predecessors earlier. Covering procedures distinguish families from topologically ordered sequences, and min-sum costs depend on the order. Do not interchange these objects in algorithm or proof edits.
- When changing a guarantee or reduction, trace its uses in the proof, associated pseudocode, introduction/abstract/conclusions, result tables, and reduction/hardness diagrams. Preserve the meaning and order of bicriteria parameters defined in the preliminaries.
- Labels use semantic prefixes such as `sec:`, `subsection:`, `problem:`, `thm:`, `lem:`/`lemma:`, `cor:`, `alg:`, `fig:`, and `tab:`. Extended-abstract assets use `ea:`-prefixed labels to avoid collisions with the full-paper appendix. Preserve existing labels and their `\ref`/`\hyperref` consumers.
- Pseudocode uses `algorithm2e` with `\DontPrintSemicolon`, `\LinesNumbered`, procedure blocks, and math-mode assignments. Follow those patterns rather than introducing another algorithm package.
- `\DD`, `\MS`, and `\TP` are colored author annotations. Treat them and commented-out passages as manuscript editorial material, not disposable generated content.
- `sections/binary_search.tex` is currently commented out in the entry points. Do not re-enable it as a side effect of another edit.
- The nested `Active-Learning-and-Covering-Problems-with-Precedence/` path is a Git submodule, not the working manuscript source tree. Make manuscript changes in the outer repository.
