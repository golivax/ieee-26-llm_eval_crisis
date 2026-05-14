# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository hosts an in-progress academic article titled **"The Reproducibility Crisis of LLM Benchmarks in Software Engineering"** (authors: Gustavo A. Oliva, Dayi Lin, Ahmed E. Hassan; Queen's University). The article argues that current LLM benchmark reporting practices in SE (e.g., SWE-Bench, Aider Polyglot, LiveCodeBench) suffer from two problems — inherent non-determinism and parameter sensitivity — and proposes a two-tiered set of recommendations (immediate practitioner-adoptable + long-term community-coordinated).

The primary target venue is **IEEE Software** (a practitioner-focused magazine, not a pure research journal). An ICSE 2026 template is also kept in the tree as an alternative submission target.

## Top-Level Layout

- `paper/` — **The active working directory.** Contains the live LaTeX source, the bibliography, supporting tools, and editor notes for the IEEE Software submission. This directory has its own `CLAUDE.md` with detailed conventions for the article itself (word count rules, writing style, LaTeX patterns); **read `paper/CLAUDE.md` before editing anything inside `paper/`**.
- `ieee-software-template/` — Pristine IEEE CSMag (IEEE Software) template (`IEEEcsmag.cls`, sample `.tex`, sample PDF, supporting `.sty` files). Reference material only — do not edit unless explicitly asked to swap templates.
- `icse2026-template/` — Pristine ACM `acmart.cls` template for ICSE 2026 (alternative submission target). Reference material only.

The two template directories duplicate the upstream templates so the author can compare conventions; the active article copies the needed class files into `paper/latex/`.

## Working in This Repo

Almost all editing happens under `paper/`. From the repo root:

```bash
cd paper
./check_word_count.sh        # validates word count limits (4200 total, 150 abstract, 15 refs)
cd latex && latexmk -pdf main.tex   # build the article PDF
```

For anything beyond a trivial change inside `paper/` (LaTeX style, word-count rules, list/figure conventions, IEEE Software house style), follow the guidance in `paper/CLAUDE.md` — it captures hard requirements that are easy to violate (e.g., no `--` for sentence separation, UPPERCASE top-level section titles, `\ref{}` for all figure callouts).

## Notes on Context

- `paper/IEEESW.md` is the verbatim IEEE Software author guidelines, kept as ground truth for style decisions.
- `paper/related-work/` contains reference PDFs (downloaded arXiv papers) used while drafting — they are not part of the build.
- `paper/latex/Notes.md` and `icse2026-template/Notes.md` are author scratchpads (open ideas, TODOs that don't yet have a home in the prose). Treat `%`-prefixed LaTeX comments inside `main.tex` as inline TODOs as well.
