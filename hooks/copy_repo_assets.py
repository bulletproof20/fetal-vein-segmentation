"""MkDocs hook: mirror repository artefacts into docs_dir/repo_files for local links."""

from __future__ import annotations

import shutil
from pathlib import Path

# Paths relative to repository root copied into 06_documentation/repo_files/
_ASSET_SOURCES = (
    "01_academic",
    "02_dataset/README.md",
    "03_pipeline",
    "04_pipeline_results",
    "05_report",
    "requirements.txt",
    "README.md",
)


def _copy_source(repo_root: Path, mirror_dir: Path, relative: str) -> None:
    source = repo_root / relative
    if not source.exists():
        return
    destination = mirror_dir / relative
    if source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return
    shutil.copytree(source, destination, dirs_exist_ok=True)


def _mirror_repository_files(config) -> Path:
    repo_root = Path(config["config_file_path"]).parent
    docs_dir = repo_root / config["docs_dir"]
    mirror_dir = docs_dir / "repo_files"
    mirror_dir.mkdir(parents=True, exist_ok=True)
    for relative in _ASSET_SOURCES:
        _copy_source(repo_root, mirror_dir, relative)
    return mirror_dir


def on_pre_build(**kwargs) -> None:
    _mirror_repository_files(kwargs["config"])


def on_post_build(**kwargs) -> None:
    """MkDocs may enumerate docs_dir before pre_build; ensure mirror is in site output."""
    config = kwargs["config"]
    mirror_dir = _mirror_repository_files(config)
    site_dir = Path(config["site_dir"])
    destination = site_dir / "repo_files"
    if mirror_dir.exists():
        shutil.copytree(mirror_dir, destination, dirs_exist_ok=True)
