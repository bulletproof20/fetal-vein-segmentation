#!/usr/bin/env python3
"""Bootstrap do ambiente fetal_vein_segmentation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Garantir imports locais quando executado como script
_BOOTSTRAP_DIR = Path(__file__).resolve().parent
if str(_BOOTSTRAP_DIR) not in sys.path:
    sys.path.insert(0, str(_BOOTSTRAP_DIR))

from config import load_config  # noqa: E402
from checks import (  # noqa: E402
    CheckReport,
    check_common_notebooks,
    check_cuda_profile,
    check_dataset,
    check_directory_structure,
    check_jupyter_stack,
    check_kaggle_environment,
    check_library_versions,
    check_monai_profile,
    check_python_dependencies,
    check_pytorch_profile,
    check_runtime_adapters,
    check_segmentation_pipeline,
    check_write_permissions,
    create_missing_directories,
    print_summary,
    run_runtime_adapter_validation,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida e prepara o ambiente do projeto fetal_vein_segmentation."
    )
    parser.add_argument(
        "--no-strict",
        action="store_true",
        help="Não terminar com código de erro em verificações FAIL.",
    )
    parser.add_argument(
        "--require-gpu",
        action="store_true",
        help="Tratar ausência de CUDA como FAIL.",
    )
    parser.add_argument(
        "--skip-dirs",
        action="store_true",
        help="Não criar diretórios em falta.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cfg = load_config()

    if args.no_strict:
        cfg.strict_mode = False

    report = CheckReport()

    print("Início do bootstrap...")
    print(f"Raiz: {cfg.root}\n")
    print(f"Perfil: {cfg.profile}\n")

    check_directory_structure(cfg, report)
    check_runtime_adapters(cfg, report)
    check_segmentation_pipeline(cfg, report)

    if not args.skip_dirs:
        create_missing_directories(cfg, report)

    run_runtime_adapter_validation(cfg, report)
    check_kaggle_environment(cfg, report)
    check_dataset(cfg, report)
    check_write_permissions(cfg, report)
    check_python_dependencies(cfg, report)
    check_library_versions(report)
    # Perfil CPU: PyTorch/MONAI/CUDA são opcionais (WARN); Perfil GPU: obrigatórios (FAIL)
    check_pytorch_profile(cfg, report)
    if args.require_gpu:
        cfg.profile = "local-gpu"
    check_cuda_profile(cfg, report)
    check_monai_profile(cfg, report)
    check_jupyter_stack(report)
    check_common_notebooks(cfg, report)

    print_summary(report, cfg)

    if report.has_fail and cfg.strict_mode:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
