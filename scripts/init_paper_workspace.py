#!/usr/bin/env python3
r"""
Initialize a new LaTeX paper workspace.

Usage: FIRST SESSION ONLY
This script sets up the project structure for new paper writing.
Run this during the first-session planning phase.

This script creates:
- directory structure (`sections/`, `refs/`, `state/`, `build/`, `figures/`, `materials/`)
- state-file templates (`project-map`, `checkpoint`, `writing-plan`, `next-session-prompt`, `section-summaries`, `session-log`, `source-index`)
- a canonical structural manifest (`state/plan.json`)
- a minimal default `main.tex`
- an empty `refs/references.bib`
- `build/snapshots/` for later PNG layout review

This script does NOT create section `.tex` files. After running this script:
1. analyze user materials
2. create `state/writing-plan.md` with the decided structure
3. manually create section files in `sections/`
4. if the user provided a reference paper in LaTeX source form, adapt that paper's layout/preamble as the manuscript template; otherwise keep the default stub and insert `\input{sections/...}` lines

Subsequent sessions should follow `state/next-session-prompt.md`.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


DEFAULT_MAIN_TEX = r"""\documentclass[11pt]{{article}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern}}
\usepackage{{hyperref}}

\title{{{title}}}
\author{{TBD}}
\date{{\today}}

\begin{{document}}

\maketitle

{{{{SECTION_INPUTS}}}}

\bibliographystyle{{plain}}
\bibliography{{refs/references}}

\end{{document}}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a minimal LaTeX workspace for paper writing."
    )
    parser.add_argument("--project-dir", required=True, help="Path to the paper project directory")
    parser.add_argument("--title", default="Untitled Paper", help="Working title")
    return parser.parse_args()


def load_template(skill_dir: Path, name: str) -> str:
    return (skill_dir / "templates" / name).read_text(encoding="utf-8")


def render(text: str, title: str) -> str:
    return (
        text.replace("{{TITLE}}", title)
        .replace("{{PAPER_TYPE}}", "TBD")
        .replace("{{DATE}}", str(date.today()))
    )


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def default_plan(title: str) -> dict:
    return {
        "schema_version": 1,
        "execution_mode": "single_agent",
        "workflow_state": "setup_in_progress",
        "title": title,
        "paper_type": "TBD",
        "venue_style": "TBD",
        "template_source": "TBD",
        "current_target": "TBD",
        "sections": [],
        "validation": {
            "setup_validator": "not_run",
            "last_run_date": None,
            "status": "unknown",
            "notes": [],
        },
    }


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    project_dir = Path(args.project_dir).expanduser().resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    sections_dir = project_dir / "sections"
    refs_dir = project_dir / "refs"
    state_dir = project_dir / "state"
    build_dir = project_dir / "build"
    snapshots_dir = build_dir / "snapshots"
    figures_dir = project_dir / "figures"
    materials_dir = project_dir / "materials"
    materials_shared_dir = materials_dir / "shared"
    materials_original_dir = materials_dir / "original"

    for directory in (
        sections_dir,
        refs_dir,
        state_dir,
        build_dir,
        snapshots_dir,
        figures_dir,
        materials_dir,
        materials_shared_dir,
        materials_original_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    main_tex = DEFAULT_MAIN_TEX.format(title=args.title)
    write_if_missing(project_dir / "main.tex", main_tex + "\n")

    template_targets = {
        "plan-template.json": state_dir / "plan.json",
        "project-map-template.md": state_dir / "project-map.md",
        "source-index-template.md": state_dir / "source-index.md",
        "checkpoint-template.md": state_dir / "checkpoint.md",
        "next-session-prompt-template.md": state_dir / "next-session-prompt.md",
        "writing-plan-template.md": state_dir / "writing-plan.md",
        "section-summaries-template.md": state_dir / "section-summaries.md",
    }
    for template_name, target_path in template_targets.items():
        content = render(load_template(skill_dir, template_name), args.title)
        suffix = "\n" if not target_path.name.endswith(".json") else ""
        write_if_missing(target_path, content + suffix)

    plan_path = state_dir / "plan.json"
    if not plan_path.exists():
        plan_path.write_text(
            json.dumps(default_plan(args.title), indent=2) + "\n",
            encoding="utf-8",
        )

    write_if_missing(
        state_dir / "session-log.md",
        "# Session Log\n\n- " + str(date.today()) + ": Workspace initialized.\n",
    )

    write_if_missing(refs_dir / "references.bib", "@comment{Add BibTeX entries here.}\n")

    print(f"✓ Initialized LaTeX paper workspace at: {project_dir}")
    print("\nCreated structure:")
    print("  sections/         - Empty after init; create section .tex files manually after planning")
    print("  refs/             - references.bib (empty)")
    print("  materials/        - Background materials organized by section")
    print("    shared/         - Materials relevant to multiple sections")
    print("    original/       - Original unsorted materials for reference")
    print("  state/            - State file templates")
    print("                      (plan.json, project-map, source-index, checkpoint,")
    print("                       writing-plan, section-summaries, next-session-prompt, session-log)")
    print("  figures/          - Figure files and user-provided visual assets")
    print("  build/            - Compilation output")
    print("    snapshots/      - PNG page snapshots for later layout review")
    print("  main.tex          - Minimal manuscript stub (adapt or replace later if needed)")
    print("\n" + "=" * 70)
    print("NEXT STEPS - First Session Workflow")
    print("=" * 70)
    print("1. Analyze user materials (notes, drafts, references, style examples)")
    print("2. If style references are provided, create state/style-analysis.md")
    print("3. Create state/writing-plan.md with stable section IDs, section structure,")
    print("   materials mapping, and planned figures/tables/formulas/citations")
    print("4. Mirror the section IDs, file paths, and materials dirs in state/plan.json")
    print("5. Organize materials by section BASED ON the writing plan")
    print("6. Manually create section .tex files in sections/")
    print("7. Update main.tex:")
    print("   - If the user provided a reference paper in LaTeX source form, reuse that paper's layout/preamble as the manuscript template")
    print("   - Otherwise, use the default stub and replace {{SECTION_INPUTS}} with \\input lines")
    print("   - When adapting a user template, insert the \\input lines manually at the correct location")
    print("8. Update state/project-map.md, state/source-index.md, state/checkpoint.md, and state/next-session-prompt.md")
    print("9. Append to state/session-log.md")
    print("10. Run a setup-refinement pass over the generated files and split materials:")
    print("   - re-read the key source/style/citation details")
    print("   - refine writing-plan.md, style-analysis.md, plan.json, project-map.md, source-index.md, and materials/ if needed")
    print("   - make sure the first next-session prompt points at the right section and materials folder")
    print("11. Run python scripts/validate_setup.py --project-dir <paper-dir>")
    print("\nIMPORTANT: DO NOT write manuscript content yet - planning only!")
    print("           References are usually parsed to BibTeX later during writing sessions.")
    print("\n" + "=" * 70)
    print("Subsequent sessions")
    print("=" * 70)
    print("Follow state/next-session-prompt.md to write one content section at a time")
    print("Finish that section's own figures/tables before moving on")
    print("Compile, generate PNG snapshots, and refine layout before ending the session")
    print("After the final section, run a whole-paper pass")
    print("Read section-specific materials first; do NOT default to materials/original/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
