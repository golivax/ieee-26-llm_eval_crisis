# Paper revision TODO

Tracking the revision work from the 2026-05-11 planning session. See conversation recap below for context on why each task exists.

## Context

The paper frames the reproducibility crisis along two dimensions:
1. **Parameter sensitivity** (configurable variables, currently under-reported — including the often-overlooked environment/harness sub-layer)
2. **Model non-determinism** (stochastic inference; mitigated by distribution reporting)

A planning session briefly added a third dimension on ground-truth/Oracle reliability, but on reflection it collapsed back into Dim 1: the colleagues' FeatBench evidence (paper-vs-replication 21.8% vs 29.94%; engineering arc 37% → 99.81%) is most naturally read as evidence that *environment/harness parameters are the dominant under-reported subset* of Dim 1, not as a separate problem class. The Oracle/no-op validation recommendation that wanted to be Dim 3 is now an immediate-tier recommendation in its own right — a meta sanity check on the measurement apparatus, untied to any single dimension.

**Scope discipline**: title stays "Reproducibility Crisis." Construct validity (corpus bias, task representativeness, weak test oracles per Ebrahimi & Rajbahadur) is *adjacent* work cited as complementary, not absorbed.

## Tasks

*(2026-05-13: task list cleared — switched to iterative text editing. Completed-task history is preserved below for reference. Remaining items that were in the task list before clearing are listed here as a brief reminder so they don't fall off the radar entirely.)*

- references.bib still needs `anthropic2026noise`, `shayanfar2026benchmark`, `ebrahimi2026edit`, `harbor2026`
- Empty `\ref{}` at `main.tex:54` (table TODO)
- Author block + biographies (existing placeholders for original three authors; Shayanfar/Gallaba need to be added with affiliations, order, emails)
- Placeholder GitHub URL in Supplementary Material
- Second under-specified-tests paper still pending (TODO comment inside the sidebar's "Strengthen the Tests" paragraph)
- Optional: Ebrahimi/Rajbahadur one-line handoff in conclusion
- Optional: discuss extra empirical material with new coauthors
- Final word-count check + build before submission

## Originally-tracked tasks (cleared)

- [x] **#1 — Add Dim 3 (ground-truth reliability) to abstract and intro** *(reverted — Dim 3 collapsed into Dim 1)*
  Originally added a third dimension. After further pushback, collapsed back to two. See completion log for what was reverted and why.

- [x] **#2 — Enrich Dim 1 with environment/infrastructure parameters and harness evidence**
  Expand the parameter-sensitivity section to make the "execution environment" sub-layer load-bearing. Three pieces: (a) name environment/infrastructure parameters explicitly — RAM floor + kill ceiling, CPU/concurrency caps, time limits, sandbox image hash, hardware family, harness version + commit, scaffold version, network/proxy config, pinned deps; (b) use our FeatBench paper-vs-replication gap (21.8% vs 29.94%) and the 37% → 99.81% engineering arc as the centerpiece evidence; (c) use Anthropic's Terminal-Bench 6pp / monotonic-with-RAM finding as supporting evidence. Extend `benchmark_spec.yaml`. Add infra-error rate as a separately reportable number. **This is now the primary home for the colleagues' evidence.**

- [x] **#3 — Reinforce Dim 2 with combined-variance line**
  One sentence in the non-determinism section: observed run-to-run variance is the sum of model stochasticity and infrastructure stochasticity, which makes single-point reports even more indefensible than the temperature-zero argument implies.

- [x] **#4 — Write the new Dim 3 section (ground-truth/Oracle reliability)** *(deleted — Dim 3 collapsed)*
  Obsolete. Colleagues' evidence relocated to Dim 1 (Task #2); the validation rec stays as a standalone immediate-tier rec (Task #5).

- [x] **#5 — Add Oracle + no-op validation as standalone immediate-tier rec**
  New immediate-tier recommendation, sitting alongside config reporting and distribution reporting — not tied to a single dimension. It's a meta sanity check on the whole measurement apparatus that bounds what either Dim 1 or Dim 2 can do to a score. Publish Oracle pass-rate and no-op pass-rate alongside every model score. Oracle → 100%, no-op → 0% ideal. Gap between Oracle and 100% defines the noise floor. Anchor on our FeatBench Oracle experience (first-person).

- [x] **#6 — Expand standardized-engineering rec with harness-engineering patterns** *(deleted — superseded by #17's four-pillar restructure)*
  Granular harness-engineering tactics (retries, memory budgeting, pytest discipline, host-side proxies, curated subsets) don't fit the magazine-register four-pillar restructure. Dropped.

- [x] **#7 — Add open-source platform paragraph (Harbor as lead example)** *(deleted — consolidated into #17)*
  Harbor content is absorbed into the "Decouple Tasks from Harness and Infrastructure" pillar of the four-pillar restructure.

- [ ] **#8 — Update references.bib with new citations**
  Add bib entries for: Anthropic infrastructure-noise post (`anthropic2026noise`), Shayanfar & Gallaba "Score the Benchmark" (`shayanfar2026benchmark`), Ebrahimi & Rajbahadur "Edit, But Verify" (`ebrahimi2026edit`, arxiv 2604.05100), Harbor framework (`harbor2026`), lm-evaluation-harness (only if cited), RepoLaunch (only if cited). Optional: OpenAI SWE-bench Verified deprecation, Microsoft "Saving SWE-Bench" if used. Stay under 15 refs — prune low-value entries if needed.

- [x] **#9 — Add collaboration disclosure to Acknowledgments** *(deleted — moot)*
  Originally to add disclosure noting collaboration with Shayanfar/Gallaba. Obsolete since they are now coauthors; no disclosure needed.

- [ ] **#10 — Fix empty `\ref{}` at `main.tex:54`**
  Currently `see Table~\ref{}` with empty ref. Paragraph has scratch numbers ("33.78% to 28.89%") and `% Add table` comment. Either add the table with a proper label, or restructure the prose. Decide direction with user.

- [ ] **#11 — Run word count + final PDF build**
  After all edits: `./check_word_count.sh` and `latexmk -pdf main.tex`. Verify under 4200 / 150 / 15. Trim if over.

- [ ] **#12 — Add complementary-work citation to Ebrahimi/Rajbahadur in conclusion** *(scope narrowed)*
  Now that Ebrahimi & Rajbahadur is cited in the body (Strengthen-the-Tests pillar, narrowed to test-oracle weakness), the conclusion mention has narrower scope: gesture at the broader validity arguments (corpus bias, domain mismatch, task representativeness) that this paper does not address. One sentence is enough — something like "reproducibility is the floor; construct validity (whether tasks reflect real workloads) is further work outside our scope, recently explored by Ebrahimi & Rajbahadur." May or may not need a re-citation depending on body framing.

- [ ] **#15 — Add Shayanfar & Gallaba to author block + biographies**
  Update main.tex author block to add Radin Shayanfar and Keheliya Gallaba. Add IEEEbiography entries for them at end of document. NEEDS USER INPUT: (a) affiliations (likely Centre for Software Excellence at Huawei, possibly also Queen's), (b) author order, (c) emails if applicable.

- [ ] **#16 — Discuss with coauthors what additional empirical material to surface**
  Ask whether the paper should carry empirical material beyond what's in the blog post — e.g., a stability-arc table (the eight-row Oracle progression), additional Oracle/no-op runs across more benchmarks, an infrastructure-error breakdown, or a Harbor-vs-bare-harness comparison sidebar. Trade-off: each figure/table costs 250 words against the 4200 budget.

- [x] **#17 — Restructure Standardized Benchmark Engineering into four pillars**
  Replace current Standardized Benchmark Engineering text with four-pillar structure: (a) Validate the Benchmark (condensed Oracle/no-op from former Task #5), (b) Strengthen the Tests (Ebrahimi/Rajbahadur narrowly for test-oracle weakness; placeholder for second paper from Task #18), (c) Standardize the Interface (less Docker-centric, more interface-focused), (d) Decouple Tasks from Harness and Infrastructure (Harbor as one example, no overselling). Also delete the immediate-tier "Validate the Measurement Apparatus Before Reporting Scores" subsection (former Task #5) — content relocated and condensed under pillar (a).

- [ ] **#18 — Locate and cite the second under-specified-tests paper**
  User mentioned a second paper on under-specified tests in benchmarks (separate from EBV), needs to find it. Currently a TODO comment in the sidebar's Strengthen-the-Tests paragraph. Action: locate the paper, add citation to references.bib (#8), replace TODO with actual citation.

- [x] **#19 — Restructure: move Validate/Strengthen-Tests to a sidebar**
  Refine #17's four-pillar restructure: move Validate the Benchmark and Strengthen the Tests out of the main flow into a sidebar titled "Benchmark Hygiene Beyond Reproducibility." Main flow keeps only Standardize the Interface and Decouple Tasks from Harness and Infrastructure.

## Completion log

- **#1 (2026-05-11)** — Abstract rewritten to single paragraph (~148 words), three causes in order: parameter sensitivity → non-determinism → unstable ground truth. New Dim 3 paragraph added in intro between the Aider figure and the "reproducibility crisis" summary; second paragraph after it explicitly calls Dim 3 "most damaging" because it contaminates Dims 1 & 2. Updated counts on the summary lines ("two problems" → "three problems"; "two aforementioned" → "three aforementioned"). Citation `\cite{shayanfar2026benchmark}` referenced — will be added to `references.bib` under Task #8.
  - Side note: line 53 of the intro still has typos (`pull-requrests`, `progres`, double space before "Aider Polyglot"). Out of scope for Task #1; flagging for a separate copy-edit pass.
  - **Follow-up after coauthor acceptance**: voice updated to first-person in both abstract and Dim 3 intro paragraphs ("our industrial replication of FeatBench" instead of "a recent industrial replication"; quote attribution to Shayanfar & Gallaba removed since they are now coauthors).

- **#9 (2026-05-11)** — Deleted as moot. Shayanfar & Gallaba accepted coauthorship, so the disclosure-in-Acknowledgments rationale no longer applies.

- **#1 reverted (2026-05-11)** — Dim 3 was rolled back after editorial pushback that surfaced a real conceptual problem: with Dim 1 expanded to cover environment/harness parameters, what remained of Dim 3 collapsed into either (a) "Dim 1 taken to its logical limit" or (b) a recommendation (Oracle/no-op validation) rather than a problem class. Paper edits reverted: abstract now states "two fundamental causes" with FeatBench evidence retained as Dim 1 evidence; intro reverted to "two fundamental problems" and "these two problems"; the two Dim 3 paragraphs after the Aider figure were removed. Task #2 reframed to absorb the colleagues' evidence under Dim 1; Task #5 reframed as a standalone immediate-tier rec, not dimension-tied; Task #4 deleted.

- **#2 (2026-05-13)** — Two paper edits applied. (a) Intro Dim 1 paragraph rewritten: now leads with the layer taxonomy, names "the environment layer" as the worst under-reported, and provides two empirical anchors — our FeatBench replication gap (21.8% vs 29.94%) and Anthropic's Terminal-Bench 2.0 6-point RAM-monotonic swing. The stale `% TODO: Replace this with actual results` comment was removed. (b) Execution Environment subsubsection substantially expanded from ~80 words to ~280 words, restructured into four `\paragraph{}` sub-categories: Sandbox and Hardware, Resource Envelope, Harness and Scaffold Integration (with the OpenHands `/workspace` vs SWE-bench `/testbed` example), and Infrastructure-Error Reporting (new — proposes infra-error rate alongside pass rate, classified by failure mode). New citations referenced: `\cite{shayanfar2026benchmark}` and `\cite{anthropic2026noise}`, both to be added in Task #8.

- **#3 (2026-05-13)** — Replaced the overclaiming "purely due to the stochastic nature of inference" with two added sentences that explicitly call out infrastructure stochasticity (transient OOM kills, network latency drift, flaky tests) as the second component of run-to-run spread, and close with the strengthened claim that single-point reporting is even less defensible than the temperature-zero argument alone implies. Bridges the Dim 1 environment evidence into the Dim 2 distribution-reporting story.

- **#5 (2026-05-13)** — Added new subsection "Validate the Measurement Apparatus Before Reporting Scores" as the third immediate-tier recommendation, inserted between Distribution Reporting and the LONG-TERM RECOMMENDATIONS section header. Opens with the framing that this is a meta sanity check (neither config nor distribution reporting checks whether the benchmark is in working order), then two `\paragraph{}` sub-sections: Oracle Pass-Rate (anchored on our FeatBench 37.31% → 99.81% experience, with the practitioner-facing claim that the Oracle-to-100% gap defines the benchmark's noise floor) and No-Op Pass-Rate (empty-patch agent — non-zero result indicates tasks passable without solving them). Closes with a cost/benefit line. ~270 words added. Citation: `\cite{shayanfar2026benchmark}` (pending in Task #8).
  - **Follow-up (2026-05-13)**: this subsection is being relocated and condensed under the new Task #17 (four-pillar restructure of Standardized Benchmark Engineering), as pillar (a) "Validate the Benchmark." The standalone immediate-tier placement was deemed structurally awkward.

- **#17 (2026-05-13)** — Two paper edits applied. (a) Deleted the immediate-tier "Validate the Measurement Apparatus Before Reporting Scores" subsection (former Task #5's output). (b) Replaced the Standardized Benchmark Engineering subsection (~180 words, two-paragraph spec/Docker text) with a four-pillar restructure (~380 words): "Validate the Benchmark" (condensed Oracle/no-op, anchored on FeatBench 37% → 99.8%), "Strengthen the Tests" (Ebrahimi/Rajbahadur narrowly for test-oracle weakness, with placeholder TODO for the second under-specified-tests paper), "Standardize the Interface" (containerization-is-not-enough, interface-level standardization), "Decouple Tasks from Harness and Infrastructure" (Harbor cited as one example with explicit "not to endorse any single project" disclaimer). New citations referenced: `\cite{ebrahimi2026edit}` and `\cite{harbor2026}` (pending in Task #8).

- **#19 (2026-05-13)** — Refactored #17 once more. Validate the Benchmark and Strengthen the Tests moved out of the main flow into a sidebar titled "Benchmark Hygiene Beyond Reproducibility," implemented as a `figure*` float with a framed minipage (IEEEcsmag.cls has no native sidebar environment). Main flow opening paragraph rewritten to introduce only the two directly-connected pillars (Standardize the Interface, Decouple Tasks from Harness and Infrastructure) and to point readers at the sidebar for the broader benchmark-engineering practices. Cross-reference uses "in the sidebar" rather than `Sidebar~\ref{}` since there is only one. PDF compiles cleanly at 6 pages, ~193KB. The sidebar costs ~250 words against the 4200-word budget per IEEE Software counting rules — modest cost for the narrative clarity gain.
