---
name: paper-blueprint
description: Plan and initialize an academic paper project in LaTeX from user materials with a lightweight, self-contained, harness-oriented workflow. Use when Codex/Claude should analyze notes, drafts, results, reference lists, style examples, or user-provided figures; choose a paper structure; initialize a paper workspace; organize materials by section; create restartable state files; and prepare later writing sessions without drafting manuscript prose yet.
---

# Paper Blueprint

Plan the setup phase of a paper project. Build durable state, keep context intentional, and leave a clean handoff for later writing sessions.

This skill is self-contained. Use its own `scripts/`, `templates/`, and `references/` files instead of depending on another skill.

## Core rules

- Stay in setup and planning mode.
- Do not draft manuscript prose unless the user explicitly asks.
- Do not parse references into BibTeX unless the user explicitly asks.
- Distinguish source-backed facts from inference.
- Prefer durable files over conversational memory.
- Prefer concise plans that enable the next session over exhaustive commentary.

## Use this skill for

- planning a new paper project from research materials
- initializing a LaTeX paper workspace
- deciding section structure and production order
- organizing materials by section
- preparing state files for later writing in separate sessions
- adapting a user-provided LaTeX reference paper as the manuscript template

## Do not use this skill for

- writing the actual content sections after setup is complete
- whole-paper revision passes
- final citation cleanup unless explicitly requested
- replacing the paper project's own resume protocol once setup exists

## Harness principles

Apply these principles while working:

1. **Externalize important state.** Store plans, status, and handoff details in files.
2. **Keep context intentional.** Read what is needed; summarize and split large materials.
3. **Prefer bounded autonomy.** Stop at setup completion instead of drifting into drafting.
4. **Validate deterministically where possible.** Check files, mappings, and section wiring before ending.
5. **Design for interruption and recovery.** Leave the next session able to resume directly from state files.
6. **Avoid state drift.** Give each stable fact one canonical home.
7. **Use one canonical structural manifest.** Keep section IDs, order, and current target in a lightweight machine-readable file.

## Bundled resources

Use these bundled files:

- `scripts/init_paper_workspace.py`: initialize the paper workspace
- `scripts/validate_setup.py`: deterministic setup validator
- `scripts/compile_paper.py`: compile the manuscript later
- `scripts/render_pdf_pages.py`: render PNG snapshots later
- `scripts/quality_check.py`: lightweight checks later
- `scripts/verify_citations.py`: citation consistency checks later
- `scripts/session_status.py`: resume-oriented project status later
- `scripts/compact_checkpoint.py`: refresh checkpoint and handoff files later
- `templates/*.md`: seed the state files and planning files
- `references/session-protocol.md`: canonical resume and later-writing workflow

Load reference files only when needed. Keep the main skill body light.

## Canonical state ownership

Use one primary file for each fact class:

- `state/plan.json`: canonical section IDs/order, section file paths, materials-folder mapping, workflow state, current target, and setup-validator status
- `state/writing-plan.md`: canonical section structure, section goals, page targets, visual/formula/citation plans, and section-level material mapping
- `state/project-map.md`: canonical stable project facts, constraints, materials organization, and manuscript-template choice
- `state/source-index.md`: canonical source-material inventory, provenance notes, and explicit unused-with-reason records
- `state/checkpoint.md`: canonical current status, open questions, validation outcome, and immediate next actions
- `state/next-session-prompt.md`: canonical instructions for the very next writing session

Other files may summarize these facts, but should not redefine them.

Use the following workflow states in `state/plan.json`:

- `setup_not_started`
- `setup_in_progress`
- `setup_validated`
- `section_drafting`
- `final_pass`

## Expected inputs

You may receive:

- notes, outlines, abstracts, or draft text
- results, tables, plots, or exported figures
- reference lists in any format
- user-owned assets that must appear in the manuscript
- optional style-reference papers
- optional LaTeX source for a reference paper

## Setup workflow

1. **Read the materials.**
   - Extract the research story, contribution, evidence, and constraints.
   - Mark uncertainty instead of inventing missing facts.

2. **Understand the paper target.**
   - Identify paper type, target venue or style, emphasis, page budget, and non-negotiables.

3. **Create style analysis only if needed.**
   - If style references exist, create `state/style-analysis.md` using `templates/style-analysis-template.md`.
   - Focus on structure, visuals, formulas, citations, tone, and layout tendencies.
   - If a style reference is provided in LaTeX source form, reuse its layout and preamble as the default manuscript template unless the user says otherwise.

4. **Initialize the workspace.**
   - Run `python scripts/init_paper_workspace.py --project-dir <dir> --title "<working-title>"` from this skill folder or by absolute path.
   - Expect the script to create the base directories, state-file templates, `state/plan.json`, `state/source-index.md`, minimal `main.tex`, `refs/references.bib`, and `build/snapshots/`.
   - Create section files only after planning.

5. **Create `state/writing-plan.md`.**
   - Use `templates/writing-plan-template.md` as the structure guide.
   - Decide the working title, section structure, section purpose, length targets, and production order.
   - Assign every major section a stable section ID such as `01-introduction` or `03-method`.
   - Put detailed figure, table, formula, citation, and source-material planning inside each section block.
   - Record the expected creation method for each important figure: reuse asset, TikZ/LaTeX, Python/matplotlib, or another explicitly approved method.
   - Keep only brief paper-level totals and balance notes outside the section blocks.
   - Mirror the final section IDs, file paths, and materials directories in `state/plan.json`.

6. **Organize materials by section.**
   - Keep untouched originals in `materials/original/`.
   - Put cross-cutting items in `materials/shared/`.
   - Create `materials/<section-id>/` for section-specific inputs.
   - Split or summarize large sources into focused section files when helpful.
   - Record the organization in `state/project-map.md` and record explicit source-to-section mapping or unused-with-reason notes in `state/source-index.md`.

7. **Create section files.**
   - Default to one file per major section in `sections/` with filenames that match the section IDs.
   - Use finer granularity only when the structure clearly needs it.
   - Add the correct section heading and otherwise leave the file empty.

8. **Wire `main.tex`.**
   - Replace `{{SECTION_INPUTS}}` if the default stub is present.
   - If using a user-provided LaTeX template, preserve its structure and insert the `\input{sections/...}` lines in the correct location.
   - Ask before making large structural changes to a user-provided template beyond the minimum needed to wire section inputs.

9. **Refresh state files.**
   - Update `state/plan.json`.
   - Update `state/project-map.md`.
   - Update `state/source-index.md`.
   - Update `state/checkpoint.md` using `templates/checkpoint-template.md` as a guide.
   - Create `state/next-session-prompt.md` using `templates/next-session-prompt-template.md` as a guide.
   - Append one concise line to `state/session-log.md`.
   - Leave `state/section-summaries.md` initialized from `templates/section-summaries-template.md` and empty if no section is written yet.
   - Keep stable facts in `plan.json`, `project-map.md`, and `source-index.md`; keep only volatile status in `checkpoint.md`.

10. **Run one refinement pass.**
    - Re-read the most important source details with the new structure in mind.
    - Refine the writing plan, project map, materials split, checkpoint, and next-session prompt if needed.
    - Stop before drafting prose.

11. **Run setup validation gates.**
    - Run `python scripts/validate_setup.py --project-dir <dir>` and do not end setup until it passes.
    - Record the validator result in `state/checkpoint.md` and `state/plan.json`.

## Required outputs after setup

Create or update these files:

- `main.tex`
- `sections/*.tex`
- `materials/original/`
- `materials/shared/`
- `materials/<section-id>/`
- `state/plan.json`
- `state/writing-plan.md`
- `state/project-map.md`
- `state/source-index.md`
- `state/checkpoint.md`
- `state/next-session-prompt.md`
- `state/session-log.md`
- `state/section-summaries.md`

Optional:

- `state/style-analysis.md` when style references are provided
- additional machine-readable state only when project complexity justifies it; do not mirror all Markdown state manually

## Setup validation gates

Before ending setup, verify all of the following:

1. **Workspace integrity**
   - `main.tex`, `sections/`, `refs/references.bib`, `materials/shared/`, `materials/original/`, and required `state/` files exist.

2. **Section coverage**
   - Every planned major section in `state/plan.json` has a matching `sections/*.tex` file.
   - Every planned major section has a matching materials folder or an explicit shared-material rationale.

3. **Material traceability**
   - Every important input is mapped in `state/source-index.md` to a section, `shared/`, or an explicit unused-with-reason note.

4. **Template integration**
   - `main.tex` includes all intended section inputs.
   - No placeholder such as `{{SECTION_INPUTS}}` remains.

5. **Cross-file consistency**
   - Section IDs and order agree across `state/plan.json`, `writing-plan.md`, `project-map.md`, and the created section files.
   - `checkpoint.md`, `next-session-prompt.md`, and `state/plan.json` agree on the first writing target.

6. **Next-session readiness**
   - `state/next-session-prompt.md` names exactly what to read, what to write next, the expected outputs, and any open questions.

If a gate fails, fix the setup before stopping.

## Lightweight quality check

After the validation gates pass, leave a short note in `state/checkpoint.md` covering:

- overall setup readiness: `strong`, `acceptable`, or `needs work`
- top 1-3 remaining risks or open questions

Keep this brief. Do not add a heavy scorecard unless the user asks.

## Figure and citation policy

- Reuse user-provided figures when available.
- Use TikZ/LaTeX for notation-heavy diagrams and clean academic schematics.
- Use Python or similar tooling for data-driven plots.
- Use AI image generation only when the figure genuinely needs synthetic illustration and the user has explicitly enabled that workflow.
- Ask before overwriting or replacing user-provided figures, template files, or manually curated material folders.
- Never invent citations, quotes, page numbers, or results.
- Mark must-cite gaps and uncertain references explicitly.

## Later-session handoff

After setup, later sessions should work from the paper project's own state files and `references/session-protocol.md` rather than reloading this full skill.

Direct the next session to:
1. read `state/next-session-prompt.md`
2. follow the resume order in `references/session-protocol.md`
3. write one section unless the user explicitly asks for a different scope
4. finish that section's own figures, tables, and formulas before moving on
5. compile, inspect layout if possible, and refresh the state files before ending
6. treat `state/plan.json` as the canonical structural source if any text files disagree

## Keep the harness light

- Prefer templates, scripts, and state files over long narrative instructions.
- Avoid repeating the same rule in multiple places.
- Avoid adding bookkeeping that duplicates stable facts across files.
- Add machine-readable state only when it reduces drift or validation cost.
