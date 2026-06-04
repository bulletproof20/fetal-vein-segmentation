# Implementation

--8<-- "includes/repo_links.md"

Index of **execution and technical artefacts** under `03_pipeline/` and `02_dataset/`. Algorithms, parameters, and step-by-step procedures are **inside the notebooks** — not on this site.

---

## Start here — execution index

| Item | Role | Open |
|------|------|------|
| **Entry point notebook** | Official execution guide (Category C) | [entrypoint.ipynb][entrypoint] |
| Pipeline folder README | Short stage index | [03_pipeline/README.md][pipeline-readme] |
| Root README | Colab setup and repository map | [README.md][readme] |
| Dependencies | Python packages | [requirements.txt][requirements] |

Open [entrypoint.ipynb][entrypoint] in **Google Colab** or the GitHub notebook viewer before running experiments.

---

## Dataset overview

| Item | Role | Open |
|------|------|------|
| Dataset layout & pairing rules | Folder contract (read-only inputs, produced outputs) | [02_dataset/README.md][dataset-readme] |

---

## Notebook inventory

### Orchestration

| Notebook | Type | Open |
|----------|------|------|
| `entrypoint.ipynb` | Orchestration (workflow only) | [Open][entrypoint] |

### Library notebooks (imported with `%run`)

| Notebook | Topic | Open |
|----------|-------|------|
| `00_generic.ipynb` | I/O, project root, display helpers | [Open][nb-generic] |
| `01_global_operations.ipynb` | Brightness, gamma, histogram tools | [Open][nb-global] |
| `02_filtering.ipynb` | Spatial filters | [Open][nb-filters] |
| `postprocessing_common.ipynb` | Metrics, morphology, pairing | [Open][nb-postprocess] |

### Execution notebooks (experiments)

| Stage | Notebook | Open |
|-------|----------|------|
| Preprocessing PP1 | `01_preprocessing_pipeline.ipynb` | [Open][nb-pp1] |
| Preprocessing PP2 | `02_preprocessing_pipeline.ipynb` | [Open][nb-pp2] |
| Preprocessing PP3 | `03_preprocessing_pipeline.ipynb` | [Open][nb-pp3] |
| Preprocessing PP4 | `04_preprocessing_pipeline.ipynb` | [Open][nb-pp4] |
| Preprocessing PP5 | `05_preprocessing_pipeline.ipynb` | [Open][nb-pp5] |
| Segmentation | `fetal_vein_segmentation.ipynb` | [Open][nb-segmentation] |
| Evaluation | `evaluation.ipynb` | [Open][nb-evaluation] |

??? note "Other files under 00_common/"

    Legacy or helper notebooks may exist in the repository. The **official pipeline** uses the four library notebooks listed above. Do not treat unrelated `00_common` files as experiment entry points unless documented in [entrypoint.ipynb][entrypoint].

---

## Execution index (not duplicated here)

Step order, segmentation configuration matrix, and evaluation comparison design are documented only in [entrypoint.ipynb][entrypoint].

---

## Related

- [Home](../index.md)
- [Academic materials](academic.md)
- [Deliverables](deliverables.md)
- [Traceability](traceability.md)
