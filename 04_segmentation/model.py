"""Modelo da pipeline de segmentação (lógica única)."""

from __future__ import annotations

from typing import Any


def build_model(cfg: dict[str, Any]):
    """Constrói UNet MONAI a partir da configuração da pipeline."""
    try:
        from monai.networks.nets import UNet
    except ImportError as exc:
        raise RuntimeError(
            "MONAI/PyTorch necessários para treino. Use runtime local-gpu ou kaggle."
        ) from exc

    model_cfg = cfg.get("model", {})
    return UNet(
        spatial_dims=int(model_cfg.get("spatial_dims", 2)),
        in_channels=int(model_cfg.get("in_channels", 1)),
        out_channels=int(model_cfg.get("out_channels", 1)),
        channels=tuple(model_cfg.get("channels", [16, 32, 64, 128])),
        strides=tuple(model_cfg.get("strides", [2, 2, 2])),
        num_res_units=2,
    )
