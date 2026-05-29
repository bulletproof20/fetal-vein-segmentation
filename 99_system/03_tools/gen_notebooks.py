"""Gera notebooks de runtime (executar uma vez)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def md(text: str):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "execution_count": None,
        "source": text.splitlines(keepends=True),
    }


provider_code = r'''"""Abstração de runtime — sem lógica de treino."""
from __future__ import annotations

import os
import shutil
import zipfile
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", Path.cwd())).resolve()
RUNTIME_ROOT = PROJECT_ROOT / "99_system" / "01_runtime"

PROVIDERS = {
    "local_cpu": RUNTIME_ROOT / "local_cpu",
    "local_gpu": RUNTIME_ROOT / "local_gpu",
    "kaggle": RUNTIME_ROOT / "kaggle",
}


def get_provider(name: str | None = None) -> dict[str, Any]:
    """Devolve metadados do provider ativo ou solicitado."""
    selected = (name or os.environ.get("BOOTSTRAP_PROFILE") or "local_cpu").strip().lower()
    aliases = {"cpu": "local_cpu", "gpu": "local_gpu", "local-cpu": "local_cpu", "local-gpu": "local_gpu"}
    selected = aliases.get(selected, selected)
    if selected not in PROVIDERS:
        raise ValueError(f"Provider desconhecido: {selected}")
    runtime_dir = PROVIDERS[selected]
    config_path = runtime_dir / "config.yaml"
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    return {
        "name": selected,
        "runtime_dir": runtime_dir,
        "adapter": runtime_dir / "adapter.py",
        "config_path": config_path,
        "config": config,
    }


def export_config(provider_name: str, destination: Path | None = None) -> Path:
    """Exporta config.yaml do runtime."""
    provider = get_provider(provider_name)
    target = destination or (PROJECT_ROOT / "exports" / f"{provider['name']}-config.yaml")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(provider["config_path"], target)
    return target


def export_dataset(provider_name: str, destination: Path | None = None) -> Path:
    """Empacota dataset local (ex.: upload Kaggle)."""
    provider = get_provider(provider_name)
    dataset_path = Path(provider["config"].get("dataset_path", "./02_dataset"))
    if not dataset_path.is_absolute():
        dataset_path = (PROJECT_ROOT / dataset_path).resolve()
    target = destination or (PROJECT_ROOT / "exports" / f"{provider['name']}-dataset.zip")
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in dataset_path.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(dataset_path))
    return target


def download_results(source: Path | None = None, destination: Path | None = None) -> Path:
    """Copia outputs da pipeline para pasta local."""
    source_path = source or Path(
        os.environ.get("FETAL_OUTPUT_PATH", PROJECT_ROOT / "04_segmentation" / "outputs")
    )
    dest = destination or (PROJECT_ROOT / "exports" / "downloaded-results")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source_path, dest)
    return dest
'''

provider_nb = nb(
    [
        md("# Training Provider\n\nAbstração de runtime — **sem lógica de treino**."),
        md("## Funções\n\n- `get_provider()`\n- `export_config()`\n- `export_dataset()`\n- `download_results()`"),
        code(provider_code),
        code(
            'for name in ("local_cpu", "local_gpu", "kaggle"):\n'
            '    info = get_provider(name)\n'
            '    print(name, "->", info["config"].get("device"))'
        ),
    ]
)

launch_nb = nb(
    [
        md("# Launch — Runtime Kaggle\n\nExecuta a pipeline única `04_segmentation/train.py`."),
        code(
            "import sys\n"
            "from pathlib import Path\n\n"
            "PROJECT_ROOT = Path.cwd()\n"
            'if not (PROJECT_ROOT / "04_segmentation").exists():\n'
            '    PROJECT_ROOT = Path("/kaggle/working")\n'
            'sys.path.insert(0, str(PROJECT_ROOT / "99_system" / "01_runtime"))'
        ),
        code(
            "import importlib.util\n\n"
            'adapter_path = PROJECT_ROOT / "99_system" / "01_runtime" / "kaggle" / "adapter.py"\n'
            'spec = importlib.util.spec_from_file_location("kaggle_adapter", adapter_path)\n'
            "mod = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(mod)\n"
            "paths = mod.prepare_environment(PROJECT_ROOT)\n"
            "print(paths)"
        ),
        code("!python 04_segmentation/train.py"),
        code(
            "sync_target = mod.sync_outputs(PROJECT_ROOT)\n"
            'print(f"Outputs sincronizados: {sync_target}")'
        ),
    ]
)

(ROOT / "00_common" / "07_training_provider.ipynb").write_text(
    json.dumps(provider_nb, ensure_ascii=False, indent=1),
    encoding="utf-8",
)
(ROOT / "99_system" / "01_runtime" / "kaggle" / "launch.ipynb").write_text(
    json.dumps(launch_nb, ensure_ascii=False, indent=1),
    encoding="utf-8",
)
print("generated")
