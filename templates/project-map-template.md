# Project Map

- Title: {{TITLE}}
- Paper type: {{PAPER_TYPE}}
- Venue/style: TBD
- Manuscript template/layout: TBD
- Manifest schema version: 1
- Execution mode: single_agent
- Audience: TBD
- Thesis/question: TBD
- Main contribution/angle: TBD
- Citation style: TBD
- Figure creation methods/tools: TBD

## Source materials

- Background: (e.g., "User's draft notes about diffusion models - organized in materials/")
- Reference list: (e.g., "User provided 15 citations - will parse during writing")
- Notes: (e.g., "User's research notes on denoising - split by section")
- Figures: (e.g., "User provided 3 figures in figures/")
- Style references: (e.g., "Example papers in folder X for style matching")
- User requirements: (e.g., "Formal CVPR paper", "Survey style", etc.)

## Materials organization

- materials/01-introduction/: (list what's here)
- materials/02-related-work/: (list what's here)
- materials/shared/: (materials relevant to multiple sections)
- materials/original/: (original unsorted files for reference)

## Section map

1. `[section-id]` — title — `sections/[section-id].tex` — `materials/[section-id]/`
2. `[section-id]` — title — `sections/[section-id].tex` — `materials/[section-id]/`
3. `[section-id]` — title — `sections/[section-id].tex` — `materials/[section-id]/`

## Source traceability

- Canonical source-to-section mapping and unused-with-reason notes live in `state/source-index.md`.
- Do not duplicate the full source inventory here.

## Approvals / policies

- User-provided LaTeX template reuse choice: TBD
- AI image generation allowed: no unless user explicitly enables it
- User-provided visual assets that must be preserved: TBD

## Non-negotiables

- Preserve factual accuracy.
- Do not invent citations.
- Mark unsupported claims for verification.
- Keep the manuscript LaTeX-compilable after section edits.

## Stable-facts-only reminder

Keep this file for durable project facts. Put volatile session status in `state/checkpoint.md`.

## Current files

- Sections: `sections/`
- Bibliography: `refs/references.bib`
- Materials: `materials/` (organized by section)
- Style analysis: `state/style-analysis.md` (if style references provided)
