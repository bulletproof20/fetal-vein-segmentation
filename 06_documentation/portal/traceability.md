# Academic traceability

One-page map from **course reference material** to **this repository’s deliverables**. Link-only — no duplicated code or metrics.

---

## Traceability chain

```text
Lecturer reference (01_academic/04_reference_materials/03_code_exemple/)
        ↓  adaptation (paths, experiments, pairing)
03_pipeline/  three self-contained stage notebooks
        ↓  training & inference
02_dataset/  images_pp_* , Save_Models/ , results_*
        ↓  metrics & comparison
04_pipeline_results/  evaluation table
        ↓
05_report/  written deliverable
```

---

## Mapping table

| Stage | Lecturer / course source | Project implementation | Output location |
|-------|-------------------------|------------------------|-----------------|
| Segmentation core | [FetalVeinSegmentationUS.ipynb](../repo_files/01_academic/04_reference_materials/03_code_exemple/FetalVeinSegmentationUS.ipynb) | [02_segmentation.ipynb](../repo_files/03_pipeline/02_segmentation.ipynb) | `02_dataset/Save_Models/`, `results_*` |
| Post-processing & metrics | [Pos_Metrics.ipynb](../repo_files/01_academic/04_reference_materials/03_code_exemple/Pos_Metrics.ipynb) | [03_evaluation.ipynb](../repo_files/03_pipeline/03_evaluation.ipynb) | `pos_process`, `calculate_metrics` |
| Preprocessing concepts | Course slides & worksheets (see [Academic](academic.md)) | [01_preprocessing.ipynb](../repo_files/03_pipeline/01_preprocessing.ipynb) (PP1–PP5) | `02_dataset/images_pp_1` … `images_pp_5` |
| Assignment scope | [Assigment_TP.pdf](../repo_files/01_academic/01_assignment/Assigment_TP.pdf) | [Scientific Pipeline](pipeline.md) workflow | All stages |
| Dataset terms | [Dataset licence](licence.md) | [Dataset](dataset.md) | `02_dataset/` |
| Comparative evaluation | Lecturer metric naming; morphology CSV per `POSTPROCESS_METHOD` | [03_evaluation.ipynb](../repo_files/03_pipeline/03_evaluation.ipynb) | [Results](results.md) |

Preserved lecturer identifiers are defined in [Lecturer identifier policy](../01_governance/lecturer_identifier_policy.md) (governance).

---

## What reviewers should open

1. [Assignment specification](../repo_files/01_academic/01_assignment/Assigment_TP.pdf) — requirements  
2. [FetalVeinSegmentationUS.ipynb](../repo_files/01_academic/04_reference_materials/03_code_exemple/FetalVeinSegmentationUS.ipynb) vs [02_segmentation.ipynb](../repo_files/03_pipeline/02_segmentation.ipynb) — segmentation alignment  
3. [Scientific Pipeline](pipeline.md) — execution order  
4. [Deliverables](deliverables.md) — report template and results  

---

## Related

- [Academic materials](academic.md)
- [Implementation](implementation.md)
- [Design decisions](../02_architecture/design_evolution.md)
- [System architecture](../02_architecture/system_architecture.md)
