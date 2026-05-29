#!/usr/bin/env python3
"""Copy normative markdown into MkDocs docs/ (idempotent)."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYS = ROOT / "99_system"
DOC = SYS / "04_documentation"
MKDOCS = DOC / "05_mkdocs"
DOCS = MKDOCS / "docs"
ACADEMIC = SYS / "05_academic_context"

MAPPINGS: list[tuple[Path, Path]] = [
    (DOC / "01_governance", DOCS / "governance"),
    (DOC / "02_architecture", DOCS / "architecture"),
    (DOC / "03_templates", DOCS / "templates"),
    (DOC / "04_migration", DOCS / "migration"),
    (ACADEMIC / "01_assignment", DOCS / "academic" / "assignment"),
    (ACADEMIC / "02_worksheets", DOCS / "academic" / "worksheets"),
    (ACADEMIC / "03_course_material", DOCS / "academic" / "course_material"),
]


def copy_tree(src: Path, dest: Path) -> int:
    if not src.exists():
        return 0
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    if src.is_file():
        shutil.copy2(src, dest)
        return 1
    for item in src.rglob("*"):
        if item.is_file() and item.suffix.lower() in (".md", ".ipynb"):
            rel = item.relative_to(src)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            count += 1
    return count


def main() -> None:
    total = 0
    for src, dest in MAPPINGS:
        total += copy_tree(src, dest)
    report = DOC / "04_migration" / "architecture_consolidation_report.md"
    if report.exists():
        dest = DOCS / "migration" / report.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(report, dest)
        total += 1
    print(f"Synced {total} file(s) into {DOCS}")


if __name__ == "__main__":
    main()
