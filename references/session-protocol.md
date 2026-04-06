# Session Protocol for New Paper Writing

Use this file when the exact on-disk state format or writing-session workflow matters.

This is the canonical protocol for sessions **after** the first-session initialization performed by `SKILL.md`.

Note for the first session: after the initial project files are created and materials are organized, do one setup-refinement pass before handing off to later sessions. Re-read the important source details and refine the generated planning/state/materials files so the on-disk setup is mature before section drafting begins.

## File Roles

### `main.tex`

Purpose: top-level manuscript that includes section files and bibliography commands.

Keep:
- document class and package preamble
- title, author, date if available
- `\input{sections/...}` lines in manuscript order
- bibliography invocation

If the user provided a style/reference paper in LaTeX source form and did not say otherwise, reuse that paper's LaTeX layout/preamble as the baseline manuscript template instead of reverting to the minimal default stub.

### `sections/*.tex`

Purpose: primary drafting units.

Default:
- keep one major section per file

Allowed when clearly useful:
- split a very large section into subsection-level files, as long as numbering and manuscript order remain explicit

### `refs/references.bib`

Purpose: central BibTeX store unless the user already has a different bibliography layout.

### `figures/`

Purpose: figure source files, exported images, user-provided visual assets, and figure-specific helper files.

Use this folder for:
- user-provided figures that must appear in the paper
- newly generated figure assets
- figure-specific `.pdf`, `.png`, `.jpg`, `.tikz`, or helper `.tex` files

### `build/snapshots/`

Purpose: PNG page snapshots generated after section-level figure/table work and during the final whole-paper pass.

Use this folder to:
- render pages that contain newly added or updated figures/tables
- inspect layout issues such as clipping, tiny text, excessive whitespace, bad float placement, or awkward caption breaks
- keep a lightweight visual record of what was checked

### `materials/`

Purpose: background materials organized by section so later sessions can load only what is relevant.

Structure:
- `materials/<section-folder>/` - materials specific to one target section
- `materials/shared/` - materials relevant to multiple sections
- `materials/original/` - original unsorted files kept for reference

Organization rule:
- create the writing plan first
- then organize materials according to that planned section structure
- extract focused per-section notes/excerpts where helpful
- map user-provided figures or figure ingredients to the section that will use them

### `state/project-map.md`

Purpose: stable project memory that should survive the full project.

Keep concise bullets for:
- paper title or working title
- paper type and venue/style target
- manuscript template / LaTeX layout source
- research question or thesis
- audience
- section map
- citation style
- non-negotiable constraints
- source materials provided by the user and how they were organized/used

### `state/plan.json`

Purpose: canonical lightweight structural manifest and validator handoff.

Keep:
- schema version
- execution mode
- workflow state
- current target
- section IDs in manuscript order
- canonical section file paths
- canonical materials directories
- setup validator status and last-run date

Do not duplicate long prose planning here.

### `state/writing-plan.md`

Purpose: comprehensive writing plan created in the first session. Detailed operational planning should live primarily inside the corresponding section blocks, not in large duplicated end-of-document plan sections.

Aim for **200-250 lines** unless the user explicitly requests a different level of detail.

Keep:
- decided paper title
- section outline and descriptions
- key points per section
- per-section length/page allocation
- per-section figure/table/formula/citation budgets
- tentative placement of planned figures/tables/formulas within each section
- explicit section-level inventory for planned figures/tables/formulas where useful
- provenance notes for planned figures/tables (user-provided / newly created / data-derived)
- planned figure-creation method where relevant (e.g., TikZ/LaTeX, Python/matplotlib, user-provided asset, or AI image generation when explicitly enabled by the user)
- section-specific citation roles, must-cite items, dependencies, and likely layout risks
- approximate total page/length budget when relevant
- brief paper-level totals / balance summary only (for counts, budget, and cross-section constraints)
- explicit note on how the plan follows the style analysis when style references exist
- reminder that each content-writing session follows: prose -> section-level figures/tables -> compile -> snapshot-based layout check

### `state/style-analysis.md`

Purpose: optional style guidance extracted from reference papers.

Aim for **180-230 lines** unless the user explicitly requests a different level of detail.

Keep:
- quantitative style snapshot (pages, citation density, references cited, figure/table/formula counts where available)
- section-level figure usage
- section-level table usage
- section-level formula usage
- section-level citation usage
- writing style observations
- argument-evolution patterns
- layout tendencies that should guide later float refinement

### `state/section-summaries.md`

Purpose: concise summaries of completed sections for efficient later context loading.

Keep one entry per completed section with:
- section name and number
- main argument or contribution
- key points or findings
- important citations used
- figures/tables/formulas created or finalized for that section
- layout verification status for that section's visuals
- connection to adjacent sections if relevant

Aim for **3-5 bullets plus brief asset/layout notes** per completed section.

### `state/checkpoint.md`

Purpose: compact volatile memory for the next session.

Keep brief bullets for:
- workflow state
- current or next section
- setup validator result
- drift status
- short status label
- compile status
- visual/layout verification status for the current section
- whole-paper pass status
- 2-5 key arguments already developed
- references used in the most recent session
- what was extracted or written from user materials
- unresolved issues
- next 1-3 concrete actions

### `state/next-session-prompt.md`

Purpose: direct handoff text the next session can start from.

Keep it short and explicit. It should say:
- what to read first
- exact target section or whole-paper-pass task
- which section-specific materials folder to read
- what not to redo
- stopping point
- whether the next task is a content section or the final whole-paper pass

### `state/session-log.md`

Purpose: append-only historical trace.

Keep one concise entry per session (single line preferred, max 2 lines):
- date
- target section or final-pass task
- compile result if relevant
- next step

## Start-of-Session Protocol

For resuming an existing project, read in this order:

1. `state/next-session-prompt.md` - authoritative next-step instructions
2. `state/project-map.md` - stable project context
3. `state/plan.json` - canonical section IDs, target, and validator state
4. `state/writing-plan.md` - full writing plan
5. `state/style-analysis.md` - optional style guide
6. `state/section-summaries.md` - overview of completed sections
7. `state/checkpoint.md` - current progress and open issues
8. the target `sections/*.tex` file you will work on
9. section-specific materials in `materials/<section-folder>/`
10. `materials/shared/` if the target section needs cross-cutting context
11. adjacent sections only if needed for coherence or tight integration

Default skips:
- `state/session-log.md`
- compile logs
- the full manuscript beyond the target section and truly necessary adjacent context

**Important:** do **not** read `materials/original/` during ordinary writing sessions. Those files are preserved for reference but should not be the default working context after materials were organized.

**Critical:** for normal content-writing sessions, write **only one content section**. You may read adjacent sections for coherence, but do not modify them unless the user explicitly asks or a small coherence fix is necessary.

**State safety:** if `state/plan.json`, `state/checkpoint.md`, and `state/next-session-prompt.md` disagree on the current target or section order, fix the state first before drafting.

## Section Drafting + Asset/Layout Loop

Use this loop for ordinary writing sessions:

1. Read the target section plan in `state/writing-plan.md`, including planned figures/tables/formulas and any mapped user-provided assets.
2. Draft or revise the target section prose and formulas.
3. Immediately create or update the figures/tables for that same section. Choose the production method that best matches the actual figure need: TikZ/LaTeX for schematic or notation-heavy academic diagrams, Python/matplotlib for data-driven plots, user-provided assets when available, or AI image generation only when the user explicitly enabled it by providing the required access details. Do not defer section-level floats to the end of the manuscript.
4. Save the section file and any figure/table assets or helper files.
5. Run `python scripts/compile_paper.py --project-dir <paper-dir>`.
6. Render PNG snapshots for the relevant pages:
   - `python scripts/render_pdf_pages.py --project-dir <paper-dir> --pages 3,4`
   - or render the whole PDF if page selection is unclear
7. Inspect the PNG snapshots if your runtime can actually display local images.
8. Check for layout issues such as:
   - clipping or overflow
   - tiny or unreadable text
   - excessive whitespace
   - bad float placement
   - broken captions
   - tables extending beyond margins
   - poor scaling of user-provided figures
9. If layout is not acceptable, refine the LaTeX and repeat the compile + snapshot loop.
10. If the runtime cannot really display the PNGs, still generate them and record that visual inspection is pending. Never claim a visual check that did not happen.

## End-of-Session Protocol

1. Save the updated target section and any associated figure/table assets.
2. Compile the manuscript.
3. Generate PNG snapshots for the relevant pages.
4. If possible, review the snapshots and refine layout until acceptable.
5. Manually append a concise summary of the completed section to `state/section-summaries.md`.
   - Include the section's main contribution, key citations, and figures/tables/formulas created or finalized.
   - Include whether snapshot-based layout verification was completed or is still pending.
6. Refresh `state/checkpoint.md`.
   - Record current section, compile status, visual/layout status, and whole-paper-pass status.
   - Record what was extracted/written from the user materials.
   - `compact_checkpoint.py` may help.
7. Refresh `state/next-session-prompt.md`.
   - If more content sections remain, specify exactly one next target section and its materials folder.
   - If the final content section is complete, set the next task to the whole-paper pass.
   - `compact_checkpoint.py` may help.
8. Append one concise item to `state/session-log.md`.
   - `compact_checkpoint.py` may help.

If the current section is incomplete, clearly record the stopping point in `state/next-session-prompt.md` so the next session can resume without re-reading unnecessary context.

## Final Whole-Paper Pass

When the final content section and its own section-level figures/tables/layout work are complete, run a whole-paper pass.

1. Compile the full manuscript.
2. Run `python scripts/quality_check.py --project-dir <paper-dir> --check all`.
3. Run `python scripts/verify_citations.py --project-dir <paper-dir>`.
4. Read enough of the manuscript to check global consistency:
   - thesis and contribution alignment across abstract/introduction/results/conclusion
   - consistent terminology and notation
   - consistent tense and voice where appropriate
   - figure/table numbering, captions, callouts, and cross-references
   - leftover TODO/TBD markers
   - repeated claims or contradictions
   - citation completeness and obvious bibliography issues
5. Render PNG snapshots for the whole PDF or at least the float-heavy pages.
6. Inspect the snapshots and fix global layout problems such as float pileups, awkward page breaks, crowded captions, or inconsistent sizing.
7. Recompile and repeat until the paper is globally coherent and visually acceptable, or clearly log any blocker.
8. Update `state/checkpoint.md`, `state/next-session-prompt.md`, and `state/session-log.md` to show whether the whole-paper pass is complete or what remains.

## Suggested Session Granularity

Prefer one of these per session to avoid context exhaustion:
- one content section plus its own figures/tables/layout verification
- one difficult subsection only if the project intentionally uses subsection-level section files
- one citation verification / bibliography cleanup pass
- one LaTeX cleanup / compile-repair pass
- one final whole-paper pass after all content sections are drafted

Avoid mixing major drafting and whole-paper polishing in the same session unless the paper is short or the user explicitly asks for it.
