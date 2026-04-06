#!/usr/bin/env python3
"""
Validate first-session paper setup.

Usage: END OF SETUP ONLY
Run this after the initial planning/setup session and before handing off to
later writing sessions.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class GateResult:
    name: str
    passed: bool
    details: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate paper project setup state.")
    parser.add_argument("--project-dir", required=True, help="Paper project directory")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write state/validation-report.md in addition to console output",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_plan(plan_path: Path) -> dict | None:
    try:
        return json.loads(plan_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {"_invalid_json": str(exc)}


def save_plan(plan_path: Path, plan: dict) -> None:
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")


def parse_inputs_from_main(main_text: str) -> list[str]:
    return re.findall(r"\\input\{sections/([^}]+)\}", main_text)


def gate_workspace_integrity(project_dir: Path, plan: dict | None) -> GateResult:
    required_paths = [
        project_dir / "main.tex",
        project_dir / "sections",
        project_dir / "refs" / "references.bib",
        project_dir / "materials" / "shared",
        project_dir / "materials" / "original",
        project_dir / "state" / "plan.json",
        project_dir / "state" / "project-map.md",
        project_dir / "state" / "source-index.md",
        project_dir / "state" / "writing-plan.md",
        project_dir / "state" / "checkpoint.md",
        project_dir / "state" / "next-session-prompt.md",
        project_dir / "state" / "section-summaries.md",
        project_dir / "state" / "session-log.md",
    ]
    missing = [str(path.relative_to(project_dir)) for path in required_paths if not path.exists()]
    if not plan:
        missing.append("state/plan.json missing or unreadable")
    elif "_invalid_json" in plan:
        missing.append(f"state/plan.json invalid JSON: {plan['_invalid_json']}")
    return GateResult("Workspace integrity", not missing, missing or ["All required files exist."])


def gate_section_coverage(project_dir: Path, plan: dict | None) -> GateResult:
    if not plan or "_invalid_json" in plan:
        return GateResult("Section coverage", False, ["state/plan.json unavailable for section checks."])

    details: list[str] = []
    sections = plan.get("sections", [])
    if not sections:
        details.append("No sections listed in state/plan.json.")
    for section in sections:
        section_id = section.get("id", "UNKNOWN")
        file_path = project_dir / section.get("file", "")
        materials_dir = project_dir / section.get("materials_dir", "")
        if not file_path.exists():
            details.append(f"Missing section file for {section_id}: {section.get('file', 'UNKNOWN')}")
        if not materials_dir.exists():
            details.append(f"Missing materials dir for {section_id}: {section.get('materials_dir', 'UNKNOWN')}")
    return GateResult("Section coverage", not details, details or ["All planned sections have files and materials dirs."])


def gate_material_traceability(project_dir: Path, plan: dict | None) -> GateResult:
    source_index = read_text(project_dir / "state" / "source-index.md")
    if not source_index.strip():
        return GateResult("Material traceability", False, ["state/source-index.md is empty or missing content."])

    details: list[str] = []
    if "unused" not in source_index.lower():
        details.append("state/source-index.md should include an explicit unused-with-reason section, even if empty.")
    if plan and "_invalid_json" not in plan:
        for section in plan.get("sections", []):
            section_id = section.get("id", "")
            if section_id and section_id not in source_index:
                details.append(f"Section ID missing from source index mapping: {section_id}")
    return GateResult("Material traceability", not details, details or ["Source index contains traceability structure."])


def gate_template_integration(project_dir: Path, plan: dict | None) -> GateResult:
    main_text = read_text(project_dir / "main.tex")
    details: list[str] = []
    if "{{SECTION_INPUTS}}" in main_text:
        details.append("main.tex still contains {{SECTION_INPUTS}} placeholder.")

    inputs = parse_inputs_from_main(main_text)
    if plan and "_invalid_json" not in plan:
        expected = [Path(section.get("file", "")).stem for section in plan.get("sections", [])]
        if expected and inputs != expected:
            details.append(
                "main.tex section input order does not match state/plan.json: "
                f"expected {expected}, found {inputs}"
            )
    elif not inputs:
        details.append("No \\input{sections/...} lines found in main.tex.")

    return GateResult("Template integration", not details, details or ["main.tex is wired to the planned sections."])


def gate_cross_file_consistency(project_dir: Path, plan: dict | None) -> GateResult:
    if not plan or "_invalid_json" in plan:
        return GateResult("Cross-file consistency", False, ["state/plan.json unavailable for consistency checks."])

    details: list[str] = []
    writing_plan = read_text(project_dir / "state" / "writing-plan.md")
    project_map = read_text(project_dir / "state" / "project-map.md")
    checkpoint = read_text(project_dir / "state" / "checkpoint.md")
    next_prompt = read_text(project_dir / "state" / "next-session-prompt.md")
    current_target = str(plan.get("current_target", "TBD"))

    for section in plan.get("sections", []):
        section_id = section.get("id", "")
        if section_id and section_id not in writing_plan:
            details.append(f"Section ID missing from writing plan: {section_id}")
        if section_id and section_id not in project_map:
            details.append(f"Section ID missing from project map: {section_id}")

    if current_target and current_target != "TBD":
        if current_target not in checkpoint:
            details.append(f"Current target not mentioned in checkpoint: {current_target}")
        if current_target not in next_prompt:
            details.append(f"Current target not mentioned in next-session prompt: {current_target}")

    return GateResult("Cross-file consistency", not details, details or ["Core state files agree on structure and current target."])


def gate_next_session_readiness(project_dir: Path) -> GateResult:
    next_prompt = read_text(project_dir / "state" / "next-session-prompt.md")
    required_phrases = [
        "Read first:",
        "Goal:",
        "Stop after:",
        "After completing the work:",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in next_prompt]
    return GateResult(
        "Next-session readiness",
        not missing,
        [f"Missing required prompt section: {phrase}" for phrase in missing] or ["Next-session prompt has the expected structure."],
    )


def write_report(project_dir: Path, results: list[GateResult]) -> None:
    report_lines = [
        "# Setup Validation Report",
        "",
        f"- Date: {date.today()}",
        "",
    ]
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        report_lines.append(f"## {result.name}: {status}")
        report_lines.extend(f"- {detail}" for detail in result.details)
        report_lines.append("")
    (project_dir / "state" / "validation-report.md").write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()

    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        return 1

    plan = load_plan(project_dir / "state" / "plan.json")
    results = [
        gate_workspace_integrity(project_dir, plan),
        gate_section_coverage(project_dir, plan),
        gate_material_traceability(project_dir, plan),
        gate_template_integration(project_dir, plan),
        gate_cross_file_consistency(project_dir, plan),
        gate_next_session_readiness(project_dir),
    ]

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}")
        for detail in result.details:
            print(f"  - {detail}")
        print()

    if args.write_report:
        write_report(project_dir, results)

    failed = [result for result in results if not result.passed]
    if plan and "_invalid_json" not in plan:
        validation = plan.setdefault("validation", {})
        validation["setup_validator"] = "pass" if not failed else "fail"
        validation["status"] = "validated" if not failed else "needs_attention"
        validation["last_run_date"] = str(date.today())
        validation["notes"] = [
            f"{result.name}: {'PASS' if result.passed else 'FAIL'}"
            for result in results
            if not result.passed
        ]
        save_plan(project_dir / "state" / "plan.json", plan)

    if failed:
        print(f"Setup validation failed: {len(failed)} gate(s) need attention.")
        return 1

    print("✓ Setup validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
