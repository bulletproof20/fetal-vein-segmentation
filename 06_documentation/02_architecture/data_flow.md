# Data flow

**Version:** 5.0  
**Scope:** artefact movement and integrity (not algorithms)

Folder names, pairing steps, and per-stage I/O are defined in the [dataset README](../portal/implementation.md#dataset-overview) and [pipeline README](../portal/implementation.md#start-here). This page states **what moves where** and **which invariants the architecture enforces**.

---

## Artefact flow

```text
02_dataset/images, labels
        ↓
03_pipeline (preprocessing → segmentation → evaluation)
        ↓
02_dataset/images_pp_* , Save_Models/ , results_*
        ↓
04_pipeline_results/
        ↓
05_report/
```

Preprocessing produces alternative training inputs; segmentation writes models and masks; evaluation aggregates metrics for comparison. Morphological post-processing at metric time runs inside `03_evaluation.ipynb` (`pos_process`).

---

## Integrity rules

| Rule | Rationale |
|------|-----------|
| Do not modify `images/` or `labels/` | Preserve originals and ground truth for all experiments |
| One `results_*` folder per experiment configuration | Prevent mask overwrites when comparing runs |
| Preprocessed images only under `images_pp_*` | Keep baseline and PP variants explicit |
| Aggregated tables under `04_pipeline_results/` | Separate published metrics from raw dataset tree |

Violations of pairing or path layout are detected in `03_pipeline/03_evaluation.ipynb` (and during training in `02_segmentation.ipynb`).

---

## Related documents

- [System architecture](system_architecture.md)
- [Design evolution](design_evolution.md)
- [Dataset contract](../portal/implementation.md#dataset-overview)
