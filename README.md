# paper-blueprint

**Plan once, write section by section with durable state.**

`paper-blueprint` is a skill for the **setup phase** of an academic paper project in LaTeX. It turns scattered materials into a structured paper workspace with:

- a clear manuscript plan
- a canonical lightweight manifest for section structure and current status
- section-specific materials folders
- reusable templates and helper scripts
- state files for restartable later sessions
- a deterministic setup validator before setup is considered done

The skill is built on durable state and follows best practices in harness engineering, including intentional context management, bounded autonomy, and a clean handoff to subsequent writing sessions.

## Installation

Before using this skill, make sure a LaTeX distribution is installed on your system.

- **Linux / WSL:** TeX Live quick install guide: <https://tug.org/texlive/quickinstall.html>
- **macOS:** MacTeX download page: <https://www.tug.org/mactex/>

Then clone this repository into your local skills directory:

```bash
git clone https://github.com/<user>/paper-blueprint.git ~/.claude/skills/paper-blueprint
```

or:

```bash
git clone https://github.com/<user>/paper-blueprint.git ~/.codex/skills/paper-blueprint
```

## Usage

Open **Codex** or **Claude** in your terminal, then paste a prompt like this:

```text
Use the paper-blueprint skill.

Goal:
Create a paper writing plan based on the following materials.

Style reference:
- /path/to/style_reference_paper/ (ideally a LaTeX source version from the target journal, but a PDF also works)

Content sources:
- /path/to/notes.md
- /path/to/outline.txt
- /path/to/abstract_draft.md
- /path/to/raw_draft.tex
- /path/to/results.txt
- /path/to/table1.csv
- /path/to/plot1.png
- /path/to/reference_list.md
- /path/to/references.bib
- /path/to/result1.png
- /path/to/figure_overview.pdf
```

Typical inputs include:

- notes, outlines, and abstract drafts
- raw manuscript drafts
- results, data, tables, and plots
- reference lists or BibTeX files
- user-provided figures
- optional style reference papers

After setup is complete, review `./paper-folder-name/state/writing-plan.md`. If the plan does not fully match your intention, refine it with a follow-up prompt.

## Continue in a new session

Once the plan is finalized, resume from the paper project itself rather than from the full skill:

```text
Read ./paper-folder/state/next-session-prompt.md and continue.
```

Later sessions should then follow the order in:

- `state/next-session-prompt.md`
- `state/plan.json`
- `references/session-protocol.md`

## Why use this workflow

- **Better focus per session.** Later sessions can write one section at a time instead of re-planning the whole paper.
- **Better recovery.** A new session can resume from state files instead of rebuilding context from chat history.
- **Lower drift.** The paper structure, materials map, and next-step instructions live on disk.
- **Safer setup.** The skill includes a machine-readable manifest plus a deterministic validator for section coverage, material traceability, and next-session readiness.

## Main project artifacts

After setup, the paper project should contain state such as:

- `state/plan.json`
- `state/writing-plan.md`
- `state/project-map.md`
- `state/source-index.md`
- `state/checkpoint.md`
- `state/next-session-prompt.md`
- `state/section-summaries.md`

Optional when needed:

- `state/style-analysis.md`

## Bundled resources

### Scripts

- `scripts/init_paper_workspace.py` — initialize the project structure
- `scripts/validate_setup.py` — run deterministic setup validation
- `scripts/compile_paper.py` — compile the paper later
- `scripts/render_pdf_pages.py` — render PNG page snapshots later
- `scripts/quality_check.py` — lightweight quality checks later
- `scripts/verify_citations.py` — citation consistency checks later
- `scripts/session_status.py` — summarize resume status later
- `scripts/compact_checkpoint.py` — refresh checkpoint and handoff files later

### Templates

- `templates/writing-plan-template.md`
- `templates/plan-template.json`
- `templates/project-map-template.md`
- `templates/source-index-template.md`
- `templates/checkpoint-template.md`
- `templates/next-session-prompt-template.md`
- `templates/section-summaries-template.md`
- `templates/style-analysis-template.md`

### Reference

- `references/session-protocol.md` — canonical resume and later-writing workflow

## Setup completion standard

The setup phase should end only after lightweight validation gates pass, including:

- workspace integrity
- section coverage
- material traceability
- template integration
- cross-file consistency
- next-session readiness

In practice, this means the setup session should run:

```bash
python scripts/validate_setup.py --project-dir /path/to/paper-project
```

## Notes

- This skill is for **setup and planning**, not automatic full-paper drafting.
- It is intentionally lightweight in the main `SKILL.md`; detailed structure lives in templates, scripts, and project state files.
- It is suitable for use across different AI sessions as long as the paper project files persist on disk.
