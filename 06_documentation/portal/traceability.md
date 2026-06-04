# Academic traceability

--8<-- "includes/repo_links.md"

One-page map from **course reference material** to **this repository’s deliverables**. Link-only — no duplicated code or metrics.

---

## Traceability chain

```text
Lecturer reference (01_academic/04_reference_materials/03_code_exemple/)
        ↓  adaptation (paths, experiments, pairing)
03_pipeline/  library + execution notebooks
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
| Segmentation core | [FetalVeinSegmentationUS.ipynb][ref-fetal] | [fetal_vein_segmentation.ipynb][nb-segmentation] | `02_dataset/Save_Models/`, `results_*` |
| Post-processing & metrics | [Pos_Metrics.ipynb][ref-metrics] | [postprocessing_common.ipynb][nb-postprocess] | Used in [evaluation.ipynb][nb-evaluation] |
| Preprocessing concepts | Course slides & worksheets (see [Academic](academic.md)) | [01–05_preprocessing_pipeline.ipynb][nb-pp1] | `02_dataset/images_pp_1` … `images_pp_5` |
| Assignment scope | [Assigment_TP.pdf][assignment] | [entrypoint.ipynb][entrypoint] workflow | All stages |
| Dataset terms | [LICENSE][dataset-licence] | [02_dataset/README.md][dataset-readme] | `02_dataset/` |
| Comparative evaluation | Lecturer metric naming (`pos_process`, `calculate_metrics`) | [evaluation.ipynb][nb-evaluation] | [04_pipeline_results/][results-dir] |

Preserved lecturer identifiers are defined in [Lecturer identifier policy](../01_governance/lecturer_identifier_policy.md) (governance).

---

## What reviewers should open

1. [Assignment][assignment] — requirements  
2. [FetalVeinSegmentationUS.ipynb][ref-fetal] vs [fetal_vein_segmentation.ipynb][nb-segmentation] — segmentation alignment  
3. [entrypoint.ipynb][entrypoint] — execution order  
4. [Deliverables](deliverables.md) — report template and results  

---

## Related

- [Academic materials](academic.md)
- [Implementation](implementation.md)
- [Design decisions](../02_architecture/design_evolution.md)
- [System architecture](../02_architecture/system_architecture.md)
