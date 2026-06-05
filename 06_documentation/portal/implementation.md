# Implementation

Index of **execution artefacts** under `03_pipeline/`. Full pipeline description: [Scientific Pipeline](pipeline.md).

---

## Start here

| Item | Open |
|------|------|
| Pipeline README | [Scientific Pipeline](pipeline.md) |
| Dataset contract | [Dataset](dataset.md) |

---

## Primary scientific notebooks

| Stage | Notebook |
|-------|----------|
| Pre-processing | [01_preprocessing.ipynb](../repo_files/03_pipeline/01_preprocessing.ipynb) |
| Segmentation | [02_segmentation.ipynb](../repo_files/03_pipeline/02_segmentation.ipynb) |
| Evaluation | [03_evaluation.ipynb](../repo_files/03_pipeline/03_evaluation.ipynb) |

Each notebook is self-contained (no `%run` between files). Evaluation applies configurable morphological post-processing (`POSTPROCESS_METHOD`) and exports method-specific CSV files to `04_pipeline_results/`.

---

## Lecturer alignment

| Lecturer reference | Project notebook |
|--------------------|------------------|
| [FetalVeinSegmentationUS.ipynb](../repo_files/01_academic/04_reference_materials/03_code_exemple/FetalVeinSegmentationUS.ipynb) | [02_segmentation.ipynb](../repo_files/03_pipeline/02_segmentation.ipynb) |
| [Pos_Metrics.ipynb](../repo_files/01_academic/04_reference_materials/03_code_exemple/Pos_Metrics.ipynb) | Metric naming; `pos_process` retained as reference in evaluation |

Details: [Traceability](traceability.md) · [Lecturer Identifier Policy](../01_governance/lecturer_identifier_policy.md).

---

## Related

- [Home](../index.md) · [Scientific Pipeline](pipeline.md) · [Deliverables](deliverables.md)
