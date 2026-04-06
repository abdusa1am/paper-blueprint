# Writing Plan: {{TITLE}}

**Target length:** 200-250 lines unless the user explicitly asks for a different level of detail.

## Decided Title

[Final or working title based on content and scope]

## Project-Level Decisions

- paper type
- target venue/style
- manuscript template / LaTeX layout source
- target audience
- research question / thesis
- main contribution / angle
- overall page or length budget

## Section Outline

List the planned sections and subsections in manuscript order.

For each major section, record at minimum:
- section ID
- canonical section file path
- canonical materials folder
- purpose
- rough page/length allocation
- target citation count or range
- expected number of figures
- expected number of tables
- expected number of formulas
- production order reminder: prose first, then section-specific figures/tables, then compile + snapshot-based layout review

## Section-by-Section Writing and Production Plan

### 01-introduction
- Section ID: 01-introduction
- Section file: `sections/01-introduction.tex`
- Materials dir: `materials/01-introduction/`
- Purpose:
- Target length/pages:
- Planned argument progression / subsections:
  -
  -
- Key points to cover:
  -
  -
- Planned figures and tables:
  - [Fig/Table ID] [description] | type: [figure/table] | source: [new / data-derived / user-provided filename] | method: [TikZ/LaTeX / Python-matplotlib / user-provided asset / AI image generation if user-enabled] | placement: [where] | why needed: [purpose] | notes: [caption/layout intent]
- Planned formulas:
  - [Eq ID] [purpose] | placement: [where] | why needed: [purpose] | notes: [display/inline, dependency]
- Citation plan:
  - Target citations:
  - Citation role in this section:
  - Must-cite items / foundational references:
- Source coverage / provenance notes:
  - Which user materials feed this section:
  - Any unused-but-relevant materials to revisit:
- Relevant materials for `materials/01-introduction/`:
- Dependencies / cross-section links:
- Likely layout or production risks:
- Section-end production note:

### 02-[section-name]
- Section ID:
- Section file:
- Materials dir:
- Purpose:
- Target length/pages:
- Planned argument progression / subsections:
  -
  -
- Key points to cover:
  -
  -
- Planned figures and tables:
  -
- Planned formulas:
  -
- Citation plan:
  - Target citations:
  - Citation role in this section:
  - Must-cite items / foundational references:
- Source coverage / provenance notes:
  - Which user materials feed this section:
  - Any unused-but-relevant materials to revisit:
- Relevant materials for `materials/02-[section-name]/`:
- Dependencies / cross-section links:
- Likely layout or production risks:
- Section-end production note:

### 03-[section-name]
- Section ID:
- Section file:
- Materials dir:
- Purpose:
- Target length/pages:
- Planned argument progression / subsections:
  -
  -
- Key points to cover:
  -
  -
- Planned figures and tables:
  -
- Planned formulas:
  -
- Citation plan:
  - Target citations:
  - Citation role in this section:
  - Must-cite items / foundational references:
- Source coverage / provenance notes:
  - Which user materials feed this section:
  - Any unused-but-relevant materials to revisit:
- Relevant materials:
- Dependencies / cross-section links:
- Likely layout or production risks:
- Section-end production note:

## Materials Organization Plan

Create a concise index of how source materials will be organized after the writing plan is finalized.

- `materials/01-introduction/`: [what goes here]
- `materials/02-related-work/`: [what goes here]
- `materials/shared/`: [cross-cutting materials]
- `materials/original/`: [untouched originals kept for reference]

Also note any user-provided visuals and the section that will use them.

## Whole-Paper Summary and Cross-Section Constraints

Keep this section brief. It should summarize the section plans above rather than duplicate them.

- total planned figures
- total planned tables
- total planned formulas
- total planned citation count or range
- section-to-section balance summary (which sections are figure-heavy, formula-heavy, citation-dense, etc.)
- any cross-section constraints or shared assets
- any shared figure-generation constraints or tool requirements
- any whole-paper layout risks or venue constraints

## Writing Approach

Explain the intended tone, pacing, argument evolution, and any venue-specific constraints.

If style references were provided, explicitly state how the plan follows the style analysis in:
- argument evolution
- figure/table insertion rhythm
- formula density and placement
- citation rhythm
- layout tendencies worth reusing or avoiding

## Session-End Workflow Reminder

For each later writing session:
- finish the target section prose first
- then create/update that section's planned figures/tables
- compile the manuscript
- generate PNG snapshots for relevant pages
- inspect/refine layout before moving on
- after the final content section, schedule a whole-paper pass

## Key Materials

List all materials provided by the user and their overall purpose.

## First-Session Refinement Reminder

After the initial version of this writing plan and the split `materials/` folders are created, do one more pass over the key source materials and refine this plan if needed. In particular, check whether:
- the section structure is still the best fit
- the section-level figure/table/formula/citation plans are specific enough
- the chosen figure-generation methods are still appropriate
- the split materials under `materials/` match the actual needs of each section
- the next-session handoff targets the right first section
