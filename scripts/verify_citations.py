#!/usr/bin/env python3
"""
Verify citations in a LaTeX paper project.

Usage: AS NEEDED (typically after adding citations)
Checks for:
- undefined citations (cited but not in bibliography)
- unused bibliography entries
- duplicate BibTeX entries
- empty citation commands

Optional:
- `--fix-duplicates` comments out later duplicate BibTeX entries in place,
  keeps the first occurrence, and creates a `.bak` backup file.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple


class CitationIssue(NamedTuple):
    file: str
    line: int
    issue_type: str
    citation_key: str
    message: str


@dataclass
class BibEntry:
    key: str
    start: int  # 0-based line index, inclusive
    end: int    # 0-based line index, exclusive


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify citations in a LaTeX paper.")
    parser.add_argument("--project-dir", required=True, help="Paper project directory")
    parser.add_argument(
        "--fix-duplicates",
        action="store_true",
        help="Comment out later duplicate BibTeX entries in place (keeps the first occurrence and creates .bak backups)",
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


def extract_cite_keys(tex_content: str) -> set[str]:
    pattern = r"\\[A-Za-z]*cite[A-Za-z*]*(?:\[[^\]]*\])*\{([^}]*)\}"
    keys: set[str] = set()
    for match in re.finditer(pattern, tex_content):
        for key in match.group(1).split(","):
            cleaned = key.strip()
            if cleaned:
                keys.add(cleaned)
    return keys


def has_empty_citation(line: str) -> bool:
    return re.search(r"\\[A-Za-z]*cite[A-Za-z*]*(?:\[[^\]]*\])*\{\s*\}", line) is not None


def parse_bib_entries(bib_content: str) -> list[BibEntry]:
    lines = bib_content.splitlines(keepends=True)
    entries: list[BibEntry] = []
    line_idx = 0

    while line_idx < len(lines):
        line = lines[line_idx]
        visible = strip_comments(line)
        match = re.match(r"\s*@\w+\s*\{\s*([^,\s]+)", visible)
        if not match:
            line_idx += 1
            continue

        key = match.group(1).strip()
        start = line_idx
        brace_balance = visible.count("{") - visible.count("}")
        line_idx += 1
        while line_idx < len(lines) and brace_balance > 0:
            visible = strip_comments(lines[line_idx])
            brace_balance += visible.count("{") - visible.count("}")
            line_idx += 1
        entries.append(BibEntry(key=key, start=start, end=line_idx))

    return entries


def extract_bib_key_counts(bib_content: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in parse_bib_entries(bib_content):
        counts[entry.key] = counts.get(entry.key, 0) + 1
    return counts


def collect_duplicate_entries(refs_dir: Path) -> dict[Path, list[tuple[BibEntry, Path]]]:
    seen: dict[str, Path] = {}
    duplicates_by_file: dict[Path, list[tuple[BibEntry, Path]]] = {}

    for bib_file in sorted(refs_dir.glob("*.bib")):
        content = bib_file.read_text(encoding="utf-8")
        for entry in parse_bib_entries(content):
            if entry.key in seen:
                duplicates_by_file.setdefault(bib_file, []).append((entry, seen[entry.key]))
            else:
                seen[entry.key] = bib_file

    return duplicates_by_file


def comment_out_duplicate_entries(bib_file: Path, entries: list[tuple[BibEntry, Path]]) -> int:
    original = bib_file.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    changed = 0

    backup = bib_file.with_suffix(bib_file.suffix + ".bak")
    if not backup.exists():
        backup.write_text(original, encoding="utf-8")

    for entry, _first_path in sorted(entries, key=lambda item: item[0].start, reverse=True):
        block = lines[entry.start:entry.end]
        commented_block = [
            f"% DUPLICATE BibTeX entry '{entry.key}' commented out automatically; first occurrence kept elsewhere.\n"
        ]
        for line in block:
            if line.startswith("%"):
                commented_block.append(line)
            elif line.strip():
                commented_block.append("% " + line)
            else:
                commented_block.append("%\n")
        lines[entry.start:entry.end] = commented_block
        changed += 1

    bib_file.write_text("".join(lines), encoding="utf-8")
    return changed


def find_citation_issues(project_dir: Path) -> list[CitationIssue]:
    issues: list[CitationIssue] = []
    sections_dir = project_dir / "sections"
    refs_dir = project_dir / "refs"

    all_cited_keys: set[str] = set()
    tex_files: list[Path] = []
    if sections_dir.exists():
        tex_files.extend(sorted(sections_dir.glob("*.tex")))
    main_tex = project_dir / "main.tex"
    if main_tex.exists():
        tex_files.append(main_tex)

    for tex_file in tex_files:
        content = tex_file.read_text(encoding="utf-8")
        for line_num, line in enumerate(content.split("\n"), 1):
            visible = strip_comments(line)
            all_cited_keys.update(extract_cite_keys(visible))
            if has_empty_citation(visible):
                issues.append(CitationIssue(
                    file=tex_file.name,
                    line=line_num,
                    issue_type="empty_citation",
                    citation_key="",
                    message="Empty citation command found",
                ))

    all_bib_keys: dict[str, int] = {}
    for bib_file in sorted(refs_dir.glob("*.bib")):
        content = bib_file.read_text(encoding="utf-8")
        bib_key_counts = extract_bib_key_counts(content)
        for key, count in bib_key_counts.items():
            all_bib_keys[key] = all_bib_keys.get(key, 0) + count
            if count > 1:
                issues.append(CitationIssue(
                    file=bib_file.name,
                    line=0,
                    issue_type="duplicate_entry",
                    citation_key=key,
                    message=f"BibTeX entry '{key}' appears {count} times in {bib_file.name}",
                ))

    duplicates = collect_duplicate_entries(refs_dir)
    for bib_file, entries in duplicates.items():
        for entry, first_path in entries:
            if first_path == bib_file:
                detail = "duplicates an earlier entry in the same .bib file"
            else:
                detail = f"duplicates an earlier entry in {first_path.name}"
            issues.append(CitationIssue(
                file=bib_file.name,
                line=entry.start + 1,
                issue_type="duplicate_entry",
                citation_key=entry.key,
                message=f"BibTeX entry '{entry.key}' {detail}",
            ))

    for key in sorted(all_cited_keys):
        if key not in all_bib_keys:
            issues.append(CitationIssue(
                file="multiple",
                line=0,
                issue_type="undefined_citation",
                citation_key=key,
                message=f"Citation '{key}' not found in bibliography",
            ))

    for key in sorted(all_bib_keys):
        if key not in all_cited_keys:
            issues.append(CitationIssue(
                file="refs/*.bib",
                line=0,
                issue_type="unused_entry",
                citation_key=key,
                message=f"BibTeX entry '{key}' is never cited",
            ))

    return issues


def fix_duplicate_entries_if_requested(project_dir: Path) -> int:
    refs_dir = project_dir / "refs"
    duplicates = collect_duplicate_entries(refs_dir)
    changed = 0
    for bib_file, entries in duplicates.items():
        changed += comment_out_duplicate_entries(bib_file, entries)
    return changed


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()

    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        return 1

    sections_dir = project_dir / "sections"
    refs_dir = project_dir / "refs"

    if not sections_dir.exists():
        print(f"Error: Sections directory not found: {sections_dir}")
        print("Run init_paper_workspace.py first to set up the project structure.")
        return 1

    if not refs_dir.exists():
        print(f"Error: References directory not found: {refs_dir}")
        print("Run init_paper_workspace.py first to set up the project structure.")
        return 1

    if args.fix_duplicates:
        changed = fix_duplicate_entries_if_requested(project_dir)
        noun = "entry" if changed == 1 else "entries"
        print(f"Applied duplicate-fix pass: commented out {changed} later duplicate BibTeX {noun}.")

    issues = find_citation_issues(project_dir)
    if not issues:
        print("✓ No citation issues found.")
        return 0

    by_type: dict[str, list[CitationIssue]] = {}
    for issue in issues:
        by_type.setdefault(issue.issue_type, []).append(issue)

    print(f"Found {len(issues)} citation issue(s):\n")
    for issue_type, type_issues in sorted(by_type.items()):
        print(f"[{issue_type.upper().replace('_', ' ')}]")
        for issue in type_issues:
            if issue.line > 0:
                print(f"  {issue.file}:{issue.line} - {issue.message}")
            else:
                print(f"  {issue.file} - {issue.message}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
