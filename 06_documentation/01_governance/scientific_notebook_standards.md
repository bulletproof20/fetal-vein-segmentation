# Scientific notebook standards

**Version:** 6.0  
**Status:** normative  
**Scope:** all notebooks under `03_pipeline/`

The repository is **notebook-centric**. Each notebook belongs to exactly one **category**. Category rules override generic layout suggestions when they conflict.

Companion: [notebook_standards.md](notebook_standards.md) (language, tone, configuration format).

---

## Category overview

| Category | Code | Role | Produces experiment artefacts |
|----------|------|------|-------------------------------|
| Library | **A** | Reusable functions (`%run`) | No (when imported) |
| Execution | **B** | Complete processing stage | Yes |
| Orchestration | **C** | Execution guide | No |
| Research | **D** | Exploratory studies (reserved) | Optional |

---

## Category A — Library notebook

### Purpose

Provide **reusable functions** imported by execution notebooks. Behaves as an in-notebook library, not an experiment report.

### Current examples

| Notebook | Responsibility |
|----------|----------------|
| `01_preprocessing/00_common/00_generic.ipynb` | I/O, grayscale, project root |
| `01_preprocessing/00_common/01_global_operations.ipynb` | Point operations, histogram tools |
| `01_preprocessing/00_common/02_filtering.ipynb` | Spatial filters (Average, Median, Gaussian, Sobel, Laplacian) |
| `03_postprocessing/postprocessing_common.ipynb` | Pairing, metrics, `pos_process`, path validation |

### Required structure (markdown `##` sections)

| Order | Section | Content |
|-------|---------|---------|
| 1 | **Purpose** | Functions provided; which execution notebooks import this file |
| 2 | **Dependencies** | Imports; `%run` prerequisites (if any) |
| 3 | **Function definitions** | Grouped implementations with docstrings |
| 4 | **Usage notes** | How to `%run`; side effects; optional quick validation cell |

### Forbidden content

- Experiment results and conclusions
- Dataset-wide research discussion
- Full architecture documentation (link to MkDocs)
- Training or evaluation tables as primary narrative

### Header requirement

```markdown
**Type:** library notebook (import via `%run`; not an experiment entry point).
```

### Import discipline

- Loaded with `%run` from execution notebooks.
- Must not write experiment outputs when imported passively.
- Optional validation cells must be clearly labelled and non-destructive.

---

## Category B — Execution notebook

### Purpose

Execute a **complete processing stage** and produce artefacts under `02_dataset/` or `04_pipeline_results/`.

### Current examples

| Notebook | Stage |
|----------|--------|
| `01_preprocessing/01_preprocessing_pipeline.ipynb` | Preprocessing PP1 |
| `01_preprocessing/02_preprocessing_pipeline.ipynb` | Preprocessing PP2 |
| `01_preprocessing/03_preprocessing_pipeline.ipynb` | Preprocessing PP3 |
| `01_preprocessing/04_preprocessing_pipeline.ipynb` | Preprocessing PP4 |
| `01_preprocessing/05_preprocessing_pipeline.ipynb` | Preprocessing PP5 |
| `02_segmentation/fetal_vein_segmentation.ipynb` | UNet training and inference |
| `04_evaluation/evaluation.ipynb` | Metrics and comparison table |

### Required structure

| Order | Section | Content |
|-------|---------|---------|
| 1 | **Purpose** | Scientific goal, inputs, outputs, limitations |
| 2 | **Imports** | Packages and `%run` library loads |
| 3 | **Configuration** | `EXPERIMENT CONFIGURATION` cell; constants |
| 4 | **Processing logic** | Core stage implementation |
| 5 | **Validation** | Paths, pairing, sanity checks |
| 6 | **Outputs** | Files, tables, figures produced |
| 7 | **Conclusions** | Summary and next step for the operator |

### Header requirement

```markdown
**Type:** execution notebook.
```

### Notes

- Helper functions should be minimal; prefer Category A libraries.
- Segmentation notebook may combine validation with data preparation until Phase 3 reorganisation; target structure remains §7 sections.

---

## Category C — Orchestration notebook

### Purpose

Guide **execution order** and configuration matrix. No scientific implementation.

### Current example

| Notebook | Role |
|----------|------|
| `03_pipeline/entrypoint.ipynb` | First-time runner guide |

### Required structure

| Order | Section | Content |
|-------|---------|---------|
| 1 | **Repository context** | Workflow diagram; Colab setup; pointer to governance/architecture |
| 2 | **Execution order** | Ordered list of notebooks to run |
| 3 | **Configuration matrix** | Segmentation `DATASET_FOLDER` / `RESULTS_FOLDER` table |
| 4 | **Expected outputs** | Where artefacts appear (`02_dataset/`, `04_pipeline_results/`) |

### Forbidden content

- Implementation code cells (setup example in markdown fence is allowed; no training/preprocessing algorithms)
- Filter or UNet definitions
- Metric implementations

### Header requirement

```markdown
Orchestration notebook — execution guide (markdown only).
```

---

## Category D — Research notebook (reserved)

### Purpose

Future **exploratory** work (hypothesis-driven experiments not part of the graded pipeline).

### Required structure (when introduced)

| Order | Section |
|-------|---------|
| 1 | Hypothesis |
| 2 | Methodology |
| 3 | Experiment |
| 4 | Results |
| 5 | Discussion |

### Current status

No Category D notebooks are required in the delivered pipeline. Do not convert Category B notebooks into research notebooks without academic approval.

---

## Category assignment table (current repository)

| Path | Category |
|------|----------|
| `03_pipeline/entrypoint.ipynb` | **C** |
| `03_pipeline/01_preprocessing/00_common/*.ipynb` | **A** |
| `03_pipeline/01_preprocessing/0N_preprocessing_pipeline.ipynb` | **B** |
| `03_pipeline/02_segmentation/fetal_vein_segmentation.ipynb` | **B** |
| `03_pipeline/03_postprocessing/postprocessing_common.ipynb` | **A** |
| `03_pipeline/04_evaluation/evaluation.ipynb` | **B** |

---

## Audit and refactor implications

| Finding type | Governed by |
|--------------|-------------|
| Missing Purpose / Conclusions | Category B §Required structure |
| Library notebook with experiment narrative | Category A §Forbidden |
| Implementation code in entrypoint | Category C §Forbidden |
| Section naming mismatch | Phase 3 may rename headings to match this document |

---

## Related documents

- [notebook_standards.md](notebook_standards.md)
- [documentation_standards.md](documentation_standards.md)
- [lecturer_identifier_policy.md](lecturer_identifier_policy.md)
- [../portal/implementation.md](../portal/implementation.md)
