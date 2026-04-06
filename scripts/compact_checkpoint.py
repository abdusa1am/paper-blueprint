#!/usr/bin/env python3
"""
Compact checkpoint and next-session prompt generator.

Usage: END OF EACH SESSION
Run this at the end of a writing session to update state files:
- checkpoint.md (current status)
- next-session-prompt.md (instructions for next session)
- session-log.md (append session entry)

This maintains session continuity for the next writing session.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a compact paper-writing checkpoint and next-session prompt."
    )
    parser.add_argument("--project-dir", required=True, help="Paper project directory")
    parser.add_argument("--title", default="Untitled Paper", help="Paper title")
    parser.add_argument("--current-section", required=True, help="Current or next target section")
    parser.add_argument("--materials-folder", help="Section-specific materials folder to read next")
    parser.add_argument("--workflow-state", default="section_drafting", help="Workflow state to store in state/plan.json and checkpoint.md")
    parser.add_argument("--status", default="drafting", help="Short status label")
    parser.add_argument("--setup-validator", default="unknown", help="Latest setup-validator status summary")
    parser.add_argument("--drift-status", default="unknown", help="Current drift summary")
    parser.add_argument("--compile-status", default="not run", help="Compile result summary")
    parser.add_argument("--visual-status", default="not run", help="Section-level layout/snapshot status")
    parser.add_argument("--paper-pass-status", default="pending", help="Whole-paper pass status")
    parser.add_argument(
        "--argument",
        action="append",
        default=[],
        help="Key argument developed this session; repeat as needed",
    )
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Reference used this session; repeat as needed",
    )
    parser.add_argument(
        "--material-note",
        action="append",
        default=[],
        help="What was extracted or written from user materials this session; repeat as needed",
    )
    parser.add_argument(
        "--issue",
        action="append",
        default=[],
        help="Open issue or blocker; repeat as needed",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Concrete next action; repeat as needed",
    )
    return parser.parse_args()


def bullet_list(items: list[str], fallback: str = "TBD") -> str:
    values = items or [fallback]
    return "\n".join(f"- {item}" for item in values)


def numbered_list(items: list[str], fallback: str = "TBD") -> str:
    values = items or [fallback]
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(values, start=1))


def infer_materials_folder(current_section: str, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    lowered = current_section.strip().lower()
    if any(token in lowered for token in ["whole-paper", "whole paper", "final pass", "final-pass"]):
        return None
    stem = Path(current_section).stem.strip()
    return stem or None


def load_plan(plan_path: Path) -> dict | None:
    try:
        return json.loads(plan_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def save_plan(plan_path: Path, plan: dict) -> None:
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    state_dir = project_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    plan_path = state_dir / "plan.json"
    plan = load_plan(plan_path)

    today = str(date.today())
    materials_folder = infer_materials_folder(args.current_section, args.materials_folder)
    materials_path = f"materials/{materials_folder}/" if materials_folder else "materials/TBD/"

    if plan is not None:
        known_section_ids = {str(section.get("id", "")) for section in plan.get("sections", [])}
        whole_paper_aliases = {"whole-paper", "whole paper", "final pass", "final-pass"}
        normalized_current = args.current_section.strip().lower()
        if (
            args.current_section not in known_section_ids
            and normalized_current not in whole_paper_aliases
            and known_section_ids
        ):
            raise SystemExit(
                f"Error: current section '{args.current_section}' is not present in state/plan.json. "
                "Update the manifest first or pass a known section ID."
            )

    checkpoint = f"""# Session Checkpoint

- Date: {today}
- Title: {args.title}
- Workflow state: {args.workflow_state}
- Current target: {args.current_section}
- Status: {args.status}
- Setup validator: {args.setup_validator}
- Drift status: {args.drift_status}
- Compile status: {args.compile_status}
- Visual/layout status: {args.visual_status}
- Whole-paper pass: {args.paper_pass_status}

## Done

{bullet_list(args.argument)}

## Sources used

{bullet_list(args.reference)}

## Materials extracted / written

{bullet_list(args.material_note)}

## Open issues

{bullet_list(args.issue)}

## Next actions

{numbered_list(args.next_step)}
"""

    next_prompt = f"""Resume working on \"{args.title}\".

Read first:
1. `state/next-session-prompt.md` (this file)
2. `state/project-map.md`
3. `state/plan.json`
4. `state/writing-plan.md`
5. `state/style-analysis.md` (if it exists)
6. `state/section-summaries.md`
7. `state/checkpoint.md`
8. the target section file for `{args.current_section}`
9. section-specific materials in `{materials_path}`
10. `materials/shared/` if needed
11. adjacent sections only if needed for coherence

Target for this session:
- Section ID or task: {args.current_section}
- Workflow state expected on entry: {args.workflow_state}

Materials for this session:
- Read files in `{materials_path}`
- Read `materials/shared/` only if this task needs cross-cutting context
- Do **not** read `materials/original/` during ordinary writing sessions

Goal:
- {args.next_step[0] if args.next_step else 'Advance the current target section.'}
- If `{args.current_section}` is a content section, finish the prose, then immediately create/update that section's planned figures/tables, compile, generate PNG snapshots, and refine layout if possible
- If all content sections are already complete, use this session for the whole-paper pass instead

Do not redo:
- already completed sections unless this prompt explicitly requires a coherence fix
- do not change section order, section IDs, or manuscript structure unless the user explicitly asks

State safety:
- Treat `state/plan.json` as the canonical structural source.
- If `state/plan.json`, `state/checkpoint.md`, and this file disagree on the current target, reconcile the state before drafting.

Stop after:
- the target section plus its own figures/tables and layout check are complete; or
- the whole-paper pass is complete

After completing the work:
- Append a concise summary to `state/section-summaries.md`
- Update `state/checkpoint.md`
- Update this file for the next session
- Append one entry to `state/session-log.md`
- Do not claim layout was visually checked unless you actually reviewed the generated PNG snapshot(s)
"""

    next_action = args.next_step[0] if args.next_step else "TBD"
    log_entry = (
        f"- {today}: {args.current_section} "
        f"({args.compile_status}; layout {args.visual_status}; final-pass {args.paper_pass_status}) "
        f"→ next: {next_action}\n"
    )

    (state_dir / "checkpoint.md").write_text(checkpoint, encoding="utf-8")
    (state_dir / "next-session-prompt.md").write_text(next_prompt, encoding="utf-8")
    session_log = state_dir / "session-log.md"
    if session_log.exists():
        previous = session_log.read_text(encoding="utf-8").rstrip() + "\n"
    else:
        previous = "# Session Log\n\n"
    session_log.write_text(previous + log_entry, encoding="utf-8")

    if plan is not None:
        plan["title"] = args.title
        plan["workflow_state"] = args.workflow_state
        plan["current_target"] = args.current_section
        validation = plan.setdefault("validation", {})
        validation["setup_validator"] = args.setup_validator
        validation["status"] = args.drift_status
        validation["last_run_date"] = today
        save_plan(plan_path, plan)

    print(f"Updated checkpoint files under: {state_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
