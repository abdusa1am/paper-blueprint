# paper-blueprint

**A harness-engineered paper planning skill for Codex/Claude that turns messy research materials into a clean, resumable LaTeX writing workspace.**

`paper-blueprint` helps you set up an academic paper project **before drafting begins**.  
Instead of jumping straight into prose, it builds a durable project structure with:

- a planned section outline
- section-specific materials folders
- restartable state files
- a lightweight structural manifest
- deterministic setup validation

The result is a paper workspace that is easier to resume, safer to iterate on, and much less likely to drift across AI sessions.

---

## Why this exists

Most AI-assisted paper writing workflows fail for predictable reasons:

- context gets bloated
- the model forgets prior decisions
- materials are scattered
- section plans drift over time
- the next session has no clean handoff

`paper-blueprint` solves that by applying **harness engineering principles** to paper setup:

- **externalize important state**
- **keep context intentional**
- **prefer bounded autonomy**
- **validate deterministically**
- **design for interruption and recovery**
- **avoid state drift**

---

## What it does

This skill helps Codex/Claude:

- analyze notes, outlines, drafts, results, and figures
- decide on a paper structure
- initialize a LaTeX paper workspace
- organize materials by section
- create durable state files for future sessions
- prepare a clean handoff for later section-by-section writing

It is especially useful for:

- survey papers
- technical reports
- research manuscripts
- long, multi-session writing projects
- AI-assisted LaTeX workflows

---

## What it does **not** do

`paper-blueprint` is intentionally scoped.

It does **not** aim to:

- draft the full manuscript automatically
- replace later writing/revision workflows
- invent citations or unsupported claims
- do final citation cleanup unless explicitly requested

This is a **setup and planning skill**, not an end-to-end autonomous paper writer.

---

## Key features

- **Durable on-disk state**
  - `state/writing-plan.md`
  - `state/project-map.md`
  - `state/source-index.md`
  - `state/checkpoint.md`
  - `state/next-session-prompt.md`

- **Canonical structural manifest**
  - `state/plan.json` stores section IDs, order, paths, workflow state, and validator status

- **Deterministic setup validation**
  - `scripts/validate_setup.py` checks that setup is complete before handoff

- **Resumable workflow**
  - later sessions can continue from the paper project itself rather than reloading the entire skill

- **LaTeX-first project structure**
  - creates a minimal manuscript layout that can evolve into a real paper

---

## Installation

Before using this skill, make sure a LaTeX distribution is installed.

- **Linux / WSL:** <https://tug.org/texlive/quickinstall.html>
- **macOS:** <https://www.tug.org/mactex/>

Then clone the repo into your skills directory:

```bash
git clone https://github.com/abdusa1am/paper-blueprint.git ~/.codex/skills/paper-blueprint
```

or:

```bash
git clone https://github.com/abdusa1am/paper-blueprint.git ~/.claude/skills/paper-blueprint
```

If you already have the folder locally, you can also copy `paper-blueprint/` into your skills directory manually.

---

## Quick start

Ask Codex or Claude to use the skill with your materials:

```text
Use the paper-blueprint skill.

Goal:
Create a paper writing plan and initialize a LaTeX workspace from my materials.

Style reference:
- /path/to/style_reference_paper/

Content sources:
- /path/to/notes.md
- /path/to/outline.txt
- /path/to/abstract_draft.md
- /path/to/results.txt
- /path/to/table1.csv
- /path/to/plot1.png
- /path/to/reference_list.md
- /path/to/references.bib
- /path/to/figure_overview.pdf
```

---

## What gets created

After setup, a typical project contains:

```text
paper-project/
├── main.tex
├── sections/
├── refs/
│   └── references.bib
├── materials/
│   ├── original/
│   ├── shared/
│   └── 01-introduction/
├── figures/
├── build/
│   └── snapshots/
└── state/
    ├── plan.json
    ├── writing-plan.md
    ├── project-map.md
    ├── source-index.md
    ├── checkpoint.md
    ├── next-session-prompt.md
    ├── section-summaries.md
    └── session-log.md
```

---

## Setup workflow

The skill is designed around a clean first-session workflow:

1. read and analyze the provided materials
2. decide the paper structure
3. assign stable section IDs
4. initialize the workspace
5. organize materials by section
6. create the writing plan and project map
7. wire `main.tex`
8. generate the next-session handoff
9. run deterministic setup validation

Setup should end only after:

```bash
python scripts/validate_setup.py --project-dir /path/to/paper-project
```

passes.

---

## Why the workflow is different

Unlike simple prompt-only workflows, `paper-blueprint` treats setup as a **stateful engineering task**.

That means:

- important decisions live in files, not chat memory
- the next session has a clear target
- materials are traceable
- section structure is explicit
- setup can be validated before drafting starts

This makes the workflow better for long-running and interruption-prone projects.

---

## Main bundled resources

### Scripts

- `scripts/init_paper_workspace.py`
- `scripts/validate_setup.py`
- `scripts/compile_paper.py`
- `scripts/render_pdf_pages.py`
- `scripts/quality_check.py`
- `scripts/verify_citations.py`
- `scripts/session_status.py`
- `scripts/compact_checkpoint.py`

### Templates

- `templates/plan-template.json`
- `templates/writing-plan-template.md`
- `templates/project-map-template.md`
- `templates/source-index-template.md`
- `templates/checkpoint-template.md`
- `templates/next-session-prompt-template.md`
- `templates/section-summaries-template.md`
- `templates/style-analysis-template.md`

### Reference

- `references/session-protocol.md`

---

## Resume in a later session

After setup, do **not** reload the whole skill by default.

Instead, resume from the project itself:

```text
Read ./paper-folder/state/next-session-prompt.md and continue.
```

Later sessions should primarily follow:

1. `state/next-session-prompt.md`
2. `state/project-map.md`
3. `state/plan.json`
4. `state/writing-plan.md`
5. `references/session-protocol.md`

---

## Best fit

`paper-blueprint` is a strong fit if you want:

- AI-assisted academic writing with better structure
- resumable paper sessions
- less context drift
- a LaTeX-first workflow
- a setup process aligned with harness-engineering ideas

---

## Release

Current release: **v1.0.0**

See the release page here:  
<https://github.com/abdusa1am/paper-blueprint/releases/tag/v1.0.0>

---

## License

MIT License
