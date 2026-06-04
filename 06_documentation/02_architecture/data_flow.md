# Data flow

**Version:** 4.0  
**Scope:** artefact movement and integrity (not algorithms)

Folder names, pairing steps, and per-stage I/O are defined in [`02_dataset/README.md`](../../02_dataset/README.md) and [`03_pipeline/entrypoint.ipynb`](../../03_pipeline/entrypoint.ipynb). This page states **what moves where** and **which invariants the architecture enforces**.

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

Preprocessing produces alternative training inputs; segmentation writes models and masks; evaluation aggregates metrics for comparison. Post-processing at metric time is applied inside the evaluation stage (see postprocessing library notebook).

---

## Integrity rules

| Rule | Rationale |
|------|-----------|
| Do not modify `images/` or `labels/` | Preserve originals and ground truth for all experiments |
| One `results_*` folder per experiment configuration | Prevent mask overwrites when comparing runs |
| Preprocessed images only under `images_pp_*` | Keep baseline and PP variants explicit |
| Aggregated tables under `04_pipeline_results/` | Separate published metrics from raw dataset tree |

Violations of pairing or path layout are detected in the postprocessing library; resolution logic is implementation detail in `03_pipeline/03_postprocessing/postprocessing_common.ipynb`.

---

## Related documents

- [System architecture](system_architecture.md)
- [Design evolution](design_evolution.md)
- [`02_dataset/README.md`](../../02_dataset/README.md)
