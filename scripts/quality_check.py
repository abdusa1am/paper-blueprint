#!/usr/bin/env python3
"""
Quality checks for a LaTeX paper project.

Usage: AS NEEDED (typically after writing a section)
Run this to check for common LaTeX issues, writing-style issues, and section balance.
Use --check to run: latex, style, balance, or all.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import NamedTuple


class QualityIssue(NamedTuple):
    file: str
    line: int
    severity: str  # error, warning, info
    category: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run quality checks on a LaTeX paper.")
    parser.add_argument("--project-dir", required=True, help="Paper project directory")
    parser.add_argument(
        "--check",
        choices=["all", "latex", "style", "balance"],
        default="all",
        help="Type of checks to run",
    )
    return parser.parse_args()


def strip_comments(line: str) -> str:
    escaped = False
    for idx, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:idx]
        escaped = False
    return line


def check_latex_issues(content: str, filename: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    lines = content.split("\n")

    brace_balance = 0
    env_stack: list[tuple[str, int]] = []

    for line_num, raw_line in enumerate(lines, 1):
        line = strip_comments(raw_line)

        if "TODO" in raw_line or "FIXME" in raw_line or "XXX" in raw_line:
            issues.append(QualityIssue(
                file=filename,
                line=line_num,
                severity="info",
                category="todo",
                message=f"TODO marker found: {raw_line.strip()[:80]}",
            ))

        if "TBD" in raw_line and not raw_line.lstrip().startswith("%"):
            issues.append(QualityIssue(
                file=filename,
                line=line_num,
                severity="warning",
                category="incomplete",
                message="TBD placeholder found",
            ))

        if re.search(r"\S  \S", line):
            issues.append(QualityIssue(
                file=filename,
                line=line_num,
                severity="info",
                category="style",
                message="Multiple consecutive spaces in prose",
            ))

        if re.search(r"(?<!\\)\.[A-Za-z]", line) and "http" not in line and "www." not in line:
            issues.append(QualityIssue(
                file=filename,
                line=line_num,
                severity="info",
                category="style",
                message="Possible missing space after period",
            ))

        visible = line.replace("\\{", "").replace("\\}", "")
        brace_balance += visible.count("{") - visible.count("}")
        if brace_balance < 0:
            issues.append(QualityIssue(
                file=filename,
                line=line_num,
                severity="error",
                category="latex_syntax",
                message="More closing braces than opening braces by this line",
            ))
            brace_balance = 0

        for env in re.findall(r"\\begin\{([^}]+)\}", line):
            env_stack.append((env, line_num))
        for env in re.findall(r"\\end\{([^}]+)\}", line):
            if not env_stack:
                issues.append(QualityIssue(
                    file=filename,
                    line=line_num,
                    severity="error",
                    category="latex_syntax",
                    message=f"Unmatched \\end{{{env}}}",
                ))
                continue
            open_env, open_line = env_stack.pop()
            if open_env != env:
                issues.append(QualityIssue(
                    file=filename,
                    line=line_num,
                    severity="error",
                    category="latex_syntax",
                    message=f"Environment mismatch: began {open_env} on line {open_line}, ended {env}",
                ))

    if brace_balance > 0:
        issues.append(QualityIssue(
            file=filename,
            line=0,
            severity="error",
            category="latex_syntax",
            message=f"Unclosed braces remain at end of file: {brace_balance}",
        ))

    for env, open_line in env_stack:
        issues.append(QualityIssue(
            file=filename,
            line=open_line,
            severity="error",
            category="latex_syntax",
            message=f"Environment opened but not closed: {env}",
        ))

    return issues


def check_style_issues(content: str, filename: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    lines = content.split("\n")

    style_patterns = [
        (r"\bvery\b", "Weak intensifier 'very' - consider a stronger word"),
        (r"\bquite\b", "Vague qualifier 'quite' - be more specific"),
        (r"\bbasically\b", "Filler word 'basically' - consider removing"),
        (r"\bin order to\b", "Verbose phrase 'in order to' - consider 'to'"),
        (r"\bdue to the fact that\b", "Verbose phrase - consider 'because'"),
        (r"\bit is important to note that\b", "Wordy phrase - consider being more direct"),
    ]

    for line_num, raw_line in enumerate(lines, 1):
        if raw_line.lstrip().startswith("%"):
            continue
        line = strip_comments(raw_line)
        for pattern, message in style_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(QualityIssue(
                    file=filename,
                    line=line_num,
                    severity="info",
                    category="style",
                    message=message,
                ))
        if len(line) > 120:
            issues.append(QualityIssue(
                file=filename,
                line=line_num,
                severity="info",
                category="readability",
                message=f"Very long line ({len(line)} chars) - consider breaking it",
            ))

    return issues


def count_words(content: str) -> int:
    content = re.sub(r"%.*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"\\[a-zA-Z*]+(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", content)
    content = re.sub(r"[{}$\\]", " ", content)
    words = content.split()
    return len([w for w in words if w.strip()])


def check_section_balance(project_dir: Path) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    sections_dir = project_dir / "sections"
    if not sections_dir.exists():
        return issues

    section_word_counts: list[tuple[str, int]] = []
    for tex_file in sorted(sections_dir.glob("*.tex")):
        content = tex_file.read_text(encoding="utf-8")
        section_word_counts.append((tex_file.name, count_words(content)))

    if len(section_word_counts) < 2:
        return issues

    total_words = sum(word_count for _, word_count in section_word_counts)
    avg_words = total_words / len(section_word_counts)

    for filename, word_count in section_word_counts:
        if 10 < word_count < avg_words * 0.3:
            issues.append(QualityIssue(
                file=filename,
                line=0,
                severity="info",
                category="balance",
                message=f"Short section: {word_count} words (avg: {avg_words:.0f})",
            ))
        elif word_count > avg_words * 2.5:
            issues.append(QualityIssue(
                file=filename,
                line=0,
                severity="info",
                category="balance",
                message=f"Long section: {word_count} words (avg: {avg_words:.0f}) - consider splitting",
            ))

    return issues


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()

    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        return 1

    sections_dir = project_dir / "sections"
    if not sections_dir.exists():
        print(f"Error: Sections directory not found: {sections_dir}")
        print("Run init_paper_workspace.py first to set up the project structure.")
        return 1

    section_files = list(sections_dir.glob("*.tex"))
    if not section_files:
        print(f"Warning: No section files found in {sections_dir}")
        print("Create section files before running quality checks.")
        return 0

    all_issues: list[QualityIssue] = []
    for tex_file in sorted(section_files):
        content = tex_file.read_text(encoding="utf-8")
        if args.check in ["all", "latex"]:
            all_issues.extend(check_latex_issues(content, tex_file.name))
        if args.check in ["all", "style"]:
            all_issues.extend(check_style_issues(content, tex_file.name))

    if args.check in ["all", "balance"]:
        all_issues.extend(check_section_balance(project_dir))

    if not all_issues:
        print("✓ No quality issues found.")
        return 0

    by_severity: dict[str, list[QualityIssue]] = {"error": [], "warning": [], "info": []}
    for issue in all_issues:
        by_severity.setdefault(issue.severity, []).append(issue)

    print(f"Found {len(all_issues)} quality issue(s):\n")

    for severity in ["error", "warning", "info"]:
        issues = by_severity.get(severity, [])
        if not issues:
            continue
        icon = {"error": "✗", "warning": "⚠", "info": "ℹ"}[severity]
        print(f"{icon} {severity.upper()} ({len(issues)})")

        by_category: dict[str, list[QualityIssue]] = {}
        for issue in issues:
            by_category.setdefault(issue.category, []).append(issue)

        for category, category_issues in sorted(by_category.items()):
            print(f"  [{category}]")
            for issue in category_issues[:10]:
                if issue.line > 0:
                    print(f"    {issue.file}:{issue.line} - {issue.message}")
                else:
                    print(f"    {issue.file} - {issue.message}")
            if len(category_issues) > 10:
                print(f"    ... and {len(category_issues) - 10} more")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
