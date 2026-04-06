#!/usr/bin/env python3
"""
Display current session status for paper project.

Usage: WHEN RESUMING (helpful but optional)
Run this to see project status, section progress, and next steps.
Useful when resuming work to get oriented.

Files are displayed in the recommended reading order from session-protocol.md:
1. next-session-prompt.md (what to do)
2. project-map.md (stable context)
3. plan.json (canonical structure + validator status)
4. writing-plan.md (comprehensive plan)
5. style-analysis.md (if exists)
6. section-summaries.md (completed sections overview)
7. checkpoint.md (current progress)

However, state/next-session-prompt.md is the authoritative source
for what to do next.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show current paper project status.")
    parser.add_argument("--project-dir", required=True, help="Paper project directory")
    return parser.parse_args()


def read_file_safe(path: Path) -> str:
    """Read file content safely, return empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def read_json_safe(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    
    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        return 1
    
    state_dir = project_dir / "state"
    sections_dir = project_dir / "sections"
    plan = read_json_safe(state_dir / "plan.json")
    
    print("=" * 70)
    print("PAPER PROJECT STATUS")
    print("=" * 70)
    print("\nFiles are displayed in the recommended reading order for resuming work.")
    print("See session-protocol.md for details.")

    if plan:
        print("\n🧭 MANIFEST")
        print("-" * 70)
        print(f"  workflow_state: {plan.get('workflow_state', 'unknown')}")
        print(f"  current_target: {plan.get('current_target', 'unknown')}")
        validation = plan.get("validation", {})
        print(f"  setup_validator: {validation.get('setup_validator', 'unknown')}")
        print(f"  validator_status: {validation.get('status', 'unknown')}")

    # 1. Next session prompt (FIRST - tells you what to do)
    next_prompt = read_file_safe(state_dir / "next-session-prompt.md")
    if next_prompt:
        print("\n➡️  1. NEXT SESSION INSTRUCTIONS")
        print("-" * 70)
        for line in next_prompt.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"  {line}")
    
    # 2. Project map (stable context)
    project_map = read_file_safe(state_dir / "project-map.md")
    if project_map:
        print("\n📋 2. PROJECT MAP (Stable Context)")
        print("-" * 70)
        for line in project_map.split('\n')[:10]:  # First 10 lines
            if line.strip() and not line.startswith('#'):
                print(f"  {line}")
    
    # 3. Writing plan
    writing_plan = read_file_safe(state_dir / "writing-plan.md")
    if writing_plan:
        print("\n📝 3. WRITING PLAN")
        print("-" * 70)
        for line in writing_plan.split('\n')[:15]:  # First 15 lines
            if line.strip():
                print(f"  {line}")
    
    # 4. Style analysis (if exists)
    style_analysis = read_file_safe(state_dir / "style-analysis.md")
    if style_analysis:
        print("\n🎨 4. STYLE ANALYSIS")
        print("-" * 70)
        # Show first few sections only
        lines = style_analysis.split('\n')
        line_count = 0
        for line in lines:
            if line_count > 20:  # Limit output
                print("  ... (see full file for complete analysis)")
                break
            if line.strip():
                print(f"  {line}")
                line_count += 1
    
    # 5. Section summaries (completed sections overview)
    section_summaries = read_file_safe(state_dir / "section-summaries.md")
    if section_summaries:
        print("\n📚 5. SECTION SUMMARIES (Completed Sections)")
        print("-" * 70)
        # Show summaries
        lines = section_summaries.split('\n')
        line_count = 0
        for line in lines:
            if line_count > 30:  # Limit output
                print("  ... (see full file for all summaries)")
                break
            if line.strip():
                print(f"  {line}")
                line_count += 1
    
    # 6. Checkpoint (current progress)
    checkpoint = read_file_safe(state_dir / "checkpoint.md")
    if checkpoint:
        print("\n📍 6. CHECKPOINT (Current Progress)")
        print("-" * 70)
        for line in checkpoint.split('\n'):
            if line.strip() and not line.startswith('#'):
                print(f"  {line}")
    
    # Section status
    if sections_dir.exists():
        print("\n📝 SECTIONS")
        print("-" * 70)
        sections = sorted(sections_dir.glob("*.tex"))
        section_names = [section_file.stem for section_file in sections]
        for section_file in sections:
            content = section_file.read_text(encoding="utf-8")
            lines = [l for l in content.split('\n') if l.strip() and not l.startswith('%')]
            word_count = len(' '.join(lines).split())
            
            # Determine status
            if word_count < 20 or 'TBD' in content:
                status = "TODO"
                icon = "⭕"
            elif 'TODO' in content or 'FIXME' in content:
                status = "IN PROGRESS"
                icon = "🔄"
            else:
                status = "DONE"
                icon = "✅"
            
            print(f"  {icon} {section_file.name:40s} {word_count:4d} words  [{status}]")

        warnings: list[str] = []
        if plan:
            manifest_sections = [str(section.get("id", "")) for section in plan.get("sections", [])]
            if manifest_sections != section_names:
                warnings.append(
                    f"Manifest section order differs from on-disk files: manifest={manifest_sections}, files={section_names}"
                )

            current_target = str(plan.get("current_target", ""))
            if current_target and current_target != "TBD" and current_target not in next_prompt:
                warnings.append(f"Current target missing from next-session prompt: {current_target}")
            if current_target and current_target != "TBD" and current_target not in checkpoint:
                warnings.append(f"Current target missing from checkpoint: {current_target}")

        main_tex = read_file_safe(project_dir / "main.tex")
        if "{{SECTION_INPUTS}}" in main_tex:
            warnings.append("main.tex still contains {{SECTION_INPUTS}} placeholder.")

        if warnings:
            print("\n⚠️  DRIFT / CONSISTENCY WARNINGS")
            print("-" * 70)
            for warning in warnings:
                print(f"  - {warning}")
    
    # Recent session log
    session_log = read_file_safe(state_dir / "session-log.md")
    if session_log:
        print("\n📅 RECENT SESSIONS")
        print("-" * 70)
        log_lines = [l for l in session_log.split('\n') if l.strip() and l.startswith('-')]
        for line in log_lines[-5:]:  # Last 5 sessions
            print(f"  {line}")
    
    # Build status
    build_dir = project_dir / "build"
    pdf_path = build_dir / "main.pdf"
    if pdf_path.exists():
        import os
        import datetime
        mtime = os.path.getmtime(pdf_path)
        mod_time = datetime.datetime.fromtimestamp(mtime)
        print("\n📄 BUILD STATUS")
        print("-" * 70)
        print(f"  ✅ PDF exists: {pdf_path}")
        print(f"  📅 Last compiled: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("\n📄 BUILD STATUS")
        print("-" * 70)
        print("  ⚠️  No PDF found - run compile_paper.py")
    
    print("\n" + "=" * 70)
    print("\nTo continue work, simply say: 'Continue working on my paper'")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
