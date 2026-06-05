# Project Overview

## Fetal Vein Segmentation Using Deep Learning and Image Processing Techniques

Academic project developed in the scope of **Processamento de Imagem Biomédica (EIM)**, IPCA.

| | |
|---|---|
| **Lecturer** | Helena Torres |
| **Authors** | Ivo Sá (22604) · Diogo Sousa (22588) |

---

## Objectives

1. Segment the fetal umbilical vein in ultrasound images using a **UNet** model (MONAI/PyTorch).
2. Evaluate **five preprocessing strategies** (PP1–PP5) against an original-image baseline under identical training conditions.
3. Assess whether **mathematical morphology** (erosion, dilation, opening, closing) improves predicted masks relative to raw network output.
4. Produce reproducible artefacts: datasets, model checkpoints, prediction masks, metric tables, and a written report.

---

## Scientific workflow

```text
01_academic/          Assignment, literature, licence, lecturer references
        ↓
02_dataset/           Images, labels, preprocessed data, models, masks
        ↓
03_pipeline/          01_preprocessing → 02_segmentation → 03_evaluation
        ↓
04_pipeline_results/  Evaluation CSV tables and training figures
        ↓
05_report/            Results narrative and final PDF report
```

Each pipeline notebook is **self-contained** (no `%run` between notebooks). Paths resolve from the repository root via `find_project_root()`.

---

## Experimental design

| Stage | Variable | Held constant |
|-------|----------|---------------|
| Preprocessing | Filter type (Original, PP1–PP5) | Geometry, patient IDs, label pairing |
| Segmentation | `DATASET_FOLDER` per run | UNet architecture, loss, epochs, split logic |
| Evaluation | `POSTPROCESS_METHOD` per run | Metrics, pairing, No/Yes comparison |

---

## Key deliverables

| Deliverable | Location |
|-------------|----------|
| Preprocessed datasets | `02_dataset/images_pp_1/` … `images_pp_5/` |
| Trained models | `02_dataset/Save_Models/` |
| Prediction masks | `02_dataset/results_*` |
| Metric tables | `04_pipeline_results/tabela_avaliacao_experiencias_*.csv` |
| Results analysis | [Results](results.md) |
| Final report | [Final Report](final_report.md) |

---

## Further reading

- [State of the Art](state_of_the_art.md) — literature review chapter
- [Scientific Pipeline](pipeline.md) — stage-by-stage description
- [Traceability](traceability.md) — lecturer reference → implementation mapping
- [System Architecture](../02_architecture/system_architecture.md)
