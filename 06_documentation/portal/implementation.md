# Implementation

--8<-- "includes/repo_links.md"

Index of **execution artefacts** under `03_pipeline/`. All algorithms live in the three primary scientific notebooks.

---

## Start here

| Item | Role | Open |
|------|------|------|
| Pipeline README | Official execution order and outputs | [03_pipeline/README.md][pipeline-readme] |
| Dataset contract | Folder layout | [02_dataset/README.md][dataset-readme] |

---

## Primary scientific notebooks

| Stage | Notebook | Open |
|-------|----------|------|
| Pre-processing | `01_preprocessing.ipynb` | [Open][nb-preprocessing] |
| Segmentation | `02_segmentation.ipynb` | [Open][nb-segmentation] |
| Post-processing + evaluation | `03_evaluation.ipynb` | [Open][nb-evaluation] |

No `%run` between these notebooks. Each file includes a **Dependencies** cell and stage sections preserved from the consolidated pipeline. Evaluation implements `pos_process()` and `calculate_metrics()` as in [Pos_Metrics.ipynb][ref-metrics].

---

## Dataset overview

Folder names, pairing rules, and artefact locations are defined in [02_dataset/README.md][dataset-readme].

---

## Related

- [Home](../index.md)
- [Academic materials](academic.md)
- [Deliverables](deliverables.md)
- [Traceability](traceability.md)
