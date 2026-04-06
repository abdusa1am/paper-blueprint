#!/usr/bin/env python3
"""
Render PDF pages to PNG snapshots for layout review.

Usage: AFTER SECTION-LEVEL FIGURE/TABLE CHANGES OR DURING THE FINAL PAPER PASS
Run this after compile_paper.py to create PNG snapshots from the generated PDF.
These snapshots help verify table/figure layout, spacing, and caption placement.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG snapshots.")
    parser.add_argument("--project-dir", help="Paper project directory (uses build/main.pdf by default)")
    parser.add_argument("--pdf", help="Explicit path to PDF file")
    parser.add_argument("--main-file", default="main.pdf", help="PDF filename under build/ when using --project-dir")
    parser.add_argument("--output-dir", help="Directory for PNG snapshots")
    parser.add_argument("--pages", help="Page list such as 1,3-5. If omitted, render all pages.")
    parser.add_argument("--dpi", type=int, default=180, help="Rendering DPI (default: 180)")
    parser.add_argument("--prefix", default="page", help="Output filename prefix")
    return parser.parse_args()


def parse_page_spec(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start < 1 or end < start:
                raise ValueError(f"Invalid page range: {token}")
            pages.update(range(start, end + 1))
        else:
            page = int(token)
            if page < 1:
                raise ValueError(f"Invalid page number: {token}")
            pages.add(page)
    return sorted(pages)


def resolve_pdf_path(args: argparse.Namespace) -> tuple[Path, Path | None]:
    if args.pdf:
        pdf_path = Path(args.pdf).expanduser().resolve()
        return pdf_path, None
    if not args.project_dir:
        raise SystemExit("Provide either --project-dir or --pdf.")
    project_dir = Path(args.project_dir).expanduser().resolve()
    pdf_path = project_dir / "build" / args.main_file
    return pdf_path, project_dir


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "pdftoppm failed").strip()
        raise SystemExit(message)


def main() -> int:
    if not shutil.which("pdftoppm"):
        raise SystemExit("pdftoppm is not available on PATH.")

    args = parse_args()
    pdf_path, project_dir = resolve_pdf_path(args)
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
    elif project_dir is not None:
        output_dir = project_dir / "build" / "snapshots"
    else:
        output_dir = pdf_path.parent / "snapshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    generated: list[Path] = []
    if args.pages:
        pages = parse_page_spec(args.pages)
        for page in pages:
            stem = output_dir / f"{args.prefix}-p{page:03d}"
            command = [
                "pdftoppm",
                "-png",
                "-r",
                str(args.dpi),
                "-f",
                str(page),
                "-l",
                str(page),
                "-singlefile",
                str(pdf_path),
                str(stem),
            ]
            run_command(command)
            generated.append(stem.with_suffix(".png"))
    else:
        stem = output_dir / args.prefix
        command = [
            "pdftoppm",
            "-png",
            "-r",
            str(args.dpi),
            str(pdf_path),
            str(stem),
        ]
        run_command(command)
        generated = sorted(output_dir.glob(f"{args.prefix}-*.png"))

    print(f"✓ Rendered {len(generated)} snapshot(s) to: {output_dir}")
    for path in generated:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

