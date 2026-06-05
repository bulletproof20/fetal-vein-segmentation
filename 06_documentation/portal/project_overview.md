# Project Overview

Academic project — **Processamento de Imagem Biomédica (EIM)**, IPCA.

| | |
|---|---|
| **Lecturer** | Helena Torres |
| **Authors** | Ivo Sá (22604) · Diogo Sousa (22588) |

---

## Objectives

1. Segment the fetal umbilical vein in ultrasound images using a **UNet** model (MONAI/PyTorch).
2. Evaluate **five preprocessing strategies** (PP1–PP5) against an original-image baseline.
3. Assess **mathematical morphology** on predicted masks (erosion, dilation, opening, closing).
4. Produce reproducible artefacts and a written report.

---

## Workflow

```text
01_academic/  →  02_dataset/  →  03_pipeline/  →  04_pipeline_results/  →  05_report/
```

Each pipeline notebook is **self-contained** (no `%run` between notebooks).

---

## Key links

| Topic | Page |
|-------|------|
| Literature review | [State of the Art](state_of_the_art.md) |
| Data layout | [Dataset overview](dataset.md) |
| Pipeline | [Scientific Pipeline](pipeline.md) |
| Results | [Results](results.md) |
| Architecture | [System architecture](../02_architecture/system_architecture.md) |
