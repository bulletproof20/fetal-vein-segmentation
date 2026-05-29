#!/usr/bin/env python3
"""One-shot architecture consolidation — run from repository root."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYS = ROOT / "99_system"
WORKSHEETS_SRC = ROOT.parent.parent / "Worksheets"


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)


def mv(src: Path, dst: Path) -> None:
    if not src.exists():
        print(f"SKIP missing: {src.relative_to(ROOT)}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.is_dir() and src.is_dir():
            for child in src.iterdir():
                target = dst / child.name
                if target.exists():
                    _remove_path(target)
                shutil.move(str(child), str(target))
            _remove_path(src)
            print(f"MERGE {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
            return
        _remove_path(dst)
    shutil.move(str(src), str(dst))
    print(f"MOVE {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        print(f"SKIP copy missing: {src}")
        return
    if dst.exists():
        print(f"SKIP copy exists: {dst.relative_to(ROOT)}")
        return
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(".ipynb_checkpoints", "__pycache__"),
    )
    print(f"COPY {src.name} -> {dst.relative_to(ROOT)}")


def main() -> None:
    for name in (
        "01_runtime/docker",
        "02_bootstrap",
        "03_tools",
        "04_documentation/01_governance",
        "04_documentation/02_architecture",
        "04_documentation/03_templates",
        "04_documentation/04_migration",
        "04_documentation/05_mkdocs",
        "05_academic_context/01_assignment",
        "05_academic_context/02_worksheets",
        "05_academic_context/03_course_material",
    ):
        (SYS / name).mkdir(parents=True, exist_ok=True)

    rt_legacy = ROOT / "10-runtime"
    rt_new = SYS / "01_runtime"
    if rt_legacy.exists() and any(rt_legacy.iterdir()):
        for old, new in (
            ("local-cpu", "local_cpu"),
            ("local-gpu", "local_gpu"),
            ("kaggle", "kaggle"),
        ):
            mv(rt_legacy / old, rt_new / new)
        if (rt_legacy / "README.md").exists() and not (rt_new / "README.md").exists():
            shutil.copy2(rt_legacy / "README.md", rt_new / "README.md")
        if rt_legacy.exists():
            shutil.rmtree(rt_legacy, ignore_errors=True)
            print("REMOVED 10-runtime")

    td = ROOT / "10-docker"
    if td.exists():
        for item in td.iterdir():
            dest = rt_new / "docker" / item.name
            if item.is_file():
                shutil.copy2(item, dest)
            else:
                copy_tree(item, dest)
        shutil.rmtree(td, ignore_errors=True)
        print("REMOVED 10-docker")

    boot_legacy = ROOT / "00-common" / "bootstrap"
    if boot_legacy.exists():
        for item in boot_legacy.iterdir():
            dest = SYS / "02_bootstrap" / item.name
            if dest.exists() and item.is_dir():
                shutil.rmtree(dest, ignore_errors=True)
            mv(item, dest)
        _remove_path(boot_legacy)

    rp_legacy = ROOT / "00-common" / "runtime_paths.py"
    rp_new = rt_new / "runtime_paths.py"
    if rp_legacy.exists() and not rp_new.exists():
        mv(rp_legacy, rp_new)

    scripts = ROOT / "scripts"
    if scripts.exists():
        for item in scripts.iterdir():
            if item.name == "consolidate_architecture.py":
                continue
            dest = SYS / "03_tools" / item.name
            if not dest.exists():
                mv(item, dest)
        try:
            scripts.rmdir()
        except OSError:
            pass

    leg_doc = SYS / "documentation"
    if leg_doc.exists():
        mapping = {
            "governance": "04_documentation/01_governance",
            "architecture": "04_documentation/02_architecture",
            "templates": "04_documentation/03_templates",
            "migration": "04_documentation/04_migration",
        }
        for sub, target in mapping.items():
            src = leg_doc / sub
            if src.exists():
                dest = SYS / target
                for f in src.glob("*.md"):
                    shutil.copy2(f, dest / f.name)
        audit = leg_doc / "audit_report.md"
        if audit.exists():
            shutil.copy2(audit, SYS / "04_documentation/04_migration/audit_report.md")
        shutil.rmtree(leg_doc, ignore_errors=True)

    mig_old = SYS / "05_documentation" / "04_migration"
    if mig_old.exists():
        for f in mig_old.glob("*.md"):
            shutil.copy2(f, SYS / "04_documentation/04_migration" / f.name)

    mk_old = SYS / "05_documentation" / "05_mkdocs"
    mk_new = SYS / "04_documentation" / "05_mkdocs"
    if mk_old.exists():
        if mk_new.exists():
            shutil.rmtree(mk_new)
        shutil.move(str(mk_old), str(mk_new))
        print("MOVE mkdocs -> 04_documentation/05_mkdocs")

    sync_src = mk_new / "sync_source_docs.py"
    sync_dst = SYS / "03_tools" / "sync_source_docs.py"
    if sync_src.exists() and not sync_dst.exists():
        shutil.copy2(sync_src, sync_dst)

    old_05 = SYS / "05_documentation"
    if old_05.exists():
        shutil.rmtree(old_05, ignore_errors=True)

    renames = [
        ("00-common", "00_common"),
        ("01-literature-review", "01_literature_review"),
        ("02-dataset", "02_dataset"),
        ("03-preprocessing", "03_preprocessing"),
        ("04-segmentation", "04_segmentation"),
        ("05-postprocessing", "05_postprocessing"),
        ("06-evaluation", "06_evaluation"),
        ("07-results", "07_results"),
    ]
    for old, new in renames:
        mv(ROOT / old, ROOT / new)

    for extra in ("08_report", "09_presentation"):
        (ROOT / extra).mkdir(exist_ok=True)

    common = ROOT / "00_common"
    if common.exists():
        for old, new in {
            "01-functions.ipynb": "01_functions.ipynb",
            "02-filters.ipynb": "02_filters.ipynb",
            "03-morphology.ipynb": "03_morphology.ipynb",
            "04-metrics.ipynb": "04_metrics.ipynb",
            "05-visualization.ipynb": "05_visualization.ipynb",
            "06-uploading.ipynb": "06_uploading.ipynb",
            "07-training-provider.ipynb": "07_training_provider.ipynb",
        }.items():
            mv(common / old, common / new)

    if WORKSHEETS_SRC.exists():
        copy_tree(WORKSHEETS_SRC, SYS / "05_academic_context" / "02_worksheets")

    for sub, title in (
        ("01_assignment", "Enunciado e documentação oficial da UC"),
        ("03_course_material", "Material complementar fornecido pela docente"),
    ):
        readme = SYS / "05_academic_context" / sub / "README.md"
        if not readme.exists():
            readme.write_text(
                f"# {sub.split('_', 1)[1].title()}\n\n{title}.\n",
                encoding="utf-8",
            )

    print("Consolidation complete.")


if __name__ == "__main__":
    main()
