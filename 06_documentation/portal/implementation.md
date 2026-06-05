# Implementation

--8<-- "includes/repo_links.md"

Index of **execution artefacts** under `03_pipeline/`. Full pipeline description: [Scientific Pipeline](pipeline.md).

---

## Start here

| Item | Open |
|------|------|
| Pipeline README | [03_pipeline/README.md][pipeline-readme] |
| Dataset contract | [02_dataset/README.md][dataset-readme] |

---

## Primary scientific notebooks

| Stage | Notebook |
|-------|----------|
| Pre-processing | [01_preprocessing.ipynb][nb-preprocessing] |
| Segmentation | [02_segmentation.ipynb][nb-segmentation] |
| Evaluation | [03_evaluation.ipynb][nb-evaluation] |

Each notebook is self-contained (no `%run` between files). Evaluation applies configurable morphological post-processing (`POSTPROCESS_METHOD`) and exports method-specific CSV files to `04_pipeline_results/`.

---

## Lecturer alignment

| Lecturer reference | Project notebook |
|--------------------|------------------|
| [FetalVeinSegmentationUS.ipynb][ref-fetal] | [02_segmentation.ipynb][nb-segmentation] |
| [Pos_Metrics.ipynb][ref-metrics] | Metric naming; `pos_process` retained as reference in evaluation |

Details: [Traceability](traceability.md) · [Lecturer Identifier Policy](../01_governance/lecturer_identifier_policy.md).

---

## Related

- [Home](../index.md) · [Scientific Pipeline](pipeline.md) · [Deliverables](deliverables.md)
