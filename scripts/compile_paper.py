#!/usr/bin/env python3
"""
Compile LaTeX paper to PDF.

Usage: EVERY SESSION (after writing)
Run this after editing section files to compile the manuscript.
Use --word-count to estimate length.
Use --bibtex when you want an explicit BibTeX run in the compile pipeline.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile a LaTeX paper project to PDF.")
    parser.add_argument("--project-dir", required=True, help="Paper project directory")
    parser.add_argument("--main-file", default="main.tex", help="Main LaTeX file")
    parser.add_argument(
        "--engine",
        choices=["latexmk", "pdflatex"],
        default="latexmk",
        help="Compilation engine",
    )
    parser.add_argument(
        "--bibtex",
        action="store_true",
        help="Run an explicit BibTeX step (useful with pdflatex fallback or when forcing bibliography refresh)",
    )
    parser.add_argument("--word-count", action="store_true", help="Show word count after compilation")
    return parser.parse_args()


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def combine_results(command: list[str], runs: list[subprocess.CompletedProcess[str]]) -> subprocess.CompletedProcess[str]:
    stdout = "\n".join((run.stdout or "") for run in runs)
    stderr = "\n".join((run.stderr or "") for run in runs)
    returncode = 0
    for run in runs:
        if run.returncode != 0:
            returncode = run.returncode
            break
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def extract_errors(log_content: str) -> list[str]:
    """Extract error messages from LaTeX log output."""
    errors = []
    lines = log_content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("!"):
            error_msg = line
            if i + 1 < len(lines):
                error_msg += "\n" + lines[i + 1]
            errors.append(error_msg)
    return errors


def count_words_in_pdf(pdf_path: Path) -> int | None:
    """Try to count words using pdftotext if available."""
    if not shutil.which("pdftotext"):
        return None
    try:
        result = subprocess.run(
            ["pdftotext", str(pdf_path), "-"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return len(result.stdout.split())
    except Exception:
        pass
    return None


def compile_with_latexmk(project_dir: Path, build_dir: Path, main_file: str, run_bibtex: bool) -> subprocess.CompletedProcess[str]:
    command = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={build_dir.name}",
    ]
    if run_bibtex:
        command.append("-bibtex")
    command.append(main_file)
    return run_command(command, project_dir)


def compile_with_pdflatex(project_dir: Path, build_dir: Path, main_file: str, run_bibtex: bool) -> subprocess.CompletedProcess[str]:
    pdflatex_command = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={build_dir.name}",
        main_file,
    ]
    runs: list[subprocess.CompletedProcess[str]] = []

    first = run_command(pdflatex_command, project_dir)
    runs.append(first)
    if first.returncode != 0:
        return combine_results(pdflatex_command, runs)

    if run_bibtex:
        if not shutil.which("bibtex"):
            raise SystemExit("BibTeX requested but `bibtex` is not available on PATH.")
        aux_name = Path(main_file).stem
        bibtex_run = run_command(["bibtex", aux_name], build_dir)
        runs.append(bibtex_run)
        if bibtex_run.returncode != 0:
            return combine_results(pdflatex_command, runs)
        runs.append(run_command(pdflatex_command, project_dir))
        if runs[-1].returncode != 0:
            return combine_results(pdflatex_command, runs)
        runs.append(run_command(pdflatex_command, project_dir))
    else:
        runs.append(run_command(pdflatex_command, project_dir))

    return combine_results(pdflatex_command, runs)


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()

    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        return 1

    build_dir = project_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    main_file = args.main_file
    main_path = project_dir / main_file

    if not main_path.exists():
        print(f"Error: Main file not found: {main_path}")
        return 1

    if args.engine == "latexmk" and shutil.which("latexmk"):
        result = compile_with_latexmk(project_dir, build_dir, main_file, args.bibtex)
    else:
        if not shutil.which("pdflatex"):
            raise SystemExit("Neither latexmk nor pdflatex is available on PATH.")
        result = compile_with_pdflatex(project_dir, build_dir, main_file, args.bibtex)

    log_path = build_dir / "compile.log"
    log_path.write_text((result.stdout or "") + "\n" + (result.stderr or ""), encoding="utf-8")

    pdf_path = build_dir / (Path(main_file).stem + ".pdf")
    if result.returncode == 0 and pdf_path.exists():
        print(f"✓ Compilation succeeded: {pdf_path}")
        print(f"  Log written to: {log_path}")
        if args.word_count:
            word_count = count_words_in_pdf(pdf_path)
            if word_count is not None:
                print(f"  Word count: ~{word_count} words")
            else:
                print("  Word count: (install pdftotext for word counting)")
        return 0

    print(f"✗ Compilation failed. See log: {log_path}")
    log_content = log_path.read_text(encoding="utf-8", errors="ignore")
    errors = extract_errors(log_content)

    if errors:
        print("\nKey errors found:")
        for i, error in enumerate(errors[:5], 1):
            print(f"\n{i}. {error}")
        if len(errors) > 5:
            print(f"\n... and {len(errors) - 5} more errors (see log)")
    else:
        print("\nNo specific errors extracted. Check the full log file.")

    return result.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
