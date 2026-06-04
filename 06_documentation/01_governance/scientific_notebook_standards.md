# Scientific notebook standards

**Version:** 7.0  
**Status:** normative  
**Scope:** all notebooks under `03_pipeline/`

The repository is **notebook-centric** on **Google Colab**. The delivered pipeline consists of **three self-contained execution notebooks**. Each notebook may contain internal sections (helpers, filters, metrics) but must not depend on `%run` or separate library notebook files.

Companion: [notebook_standards.md](notebook_standards.md) (language, tone, configuration format).

---

## Pipeline notebooks (normative)

| Notebook | Stage | Primary outputs |
|----------|-------|-----------------|
| `01_preprocessing.ipynb` | PP1–PP5 preprocessing | `02_dataset/images_pp_1` … `images_pp_5` |
| `02_segmentation.ipynb` | UNet training and inference | `02_dataset/Save_Models/`, `results_*` |
| `03_evaluation.ipynb` | Metrics and comparison table | `04_pipeline_results/` (with / without `pos_process`) |

Execution order and Colab guidance: `03_pipeline/README.md`.

---

## Required structure (each pipeline notebook)

| Order | Section | Content |
|-------|---------|---------|
| 1 | **Purpose** | Scientific goal, inputs, outputs, limitations |
| 2 | **Dependencies** | Single import cell; all packages for this notebook |
| 3 | **Configuration** | `EXPERIMENT CONFIGURATION` (or stage equivalent); constants |
| 4+ | **Stage sections** | Preserved internal organisation (e.g. I/O helpers, filters, PP1–PP5, training, metrics) |
| n−1 | **Validation** | Paths, pairing, sanity checks where applicable |
| n | **Outputs / Conclusions** | Artefacts produced; next notebook for the operator |

### Header requirement

```markdown
**Type:** execution notebook (self-contained; no %run of other pipeline notebooks).
```

### Forbidden

- `%run` of other files under `03_pipeline/`
- Separate library notebook files for shared pipeline logic
- Long architecture essays (link to MkDocs)
- Governance policy text inside notebooks

### Allowed

- Helper functions defined in the same notebook (grouped under markdown `##` sections)
- Provenance notes (“consolidated from …”) without operational paths to deleted files

---

## Internal sections (not separate notebooks)

Reusable logic lives **inside** the three notebooks, for example:

| Notebook | Typical internal sections |
|----------|---------------------------|
| `01_preprocessing.ipynb` | Project root / I/O, global operations, spatial filters, PP1–PP5 execution |
| `02_segmentation.ipynb` | Pairing, data dicts, UNet training, mask export |
| `03_evaluation.ipynb` | Pairing / path validation, `pos_process`, `calculate_metrics`, comparison table |

These sections are **not** separate Category-A files and must not be loaded via `%run`.

---

## Category D — Research notebook (reserved)

Future **exploratory** work not part of the graded pipeline. No Category D notebooks are required in the delivered project.

---

## Audit implications

| Finding | Action |
|---------|--------|
| Missing Purpose or Conclusions | Add per table above |
| `%run` of sibling pipeline notebooks | Remove; inline or use shared cells in same file |
| Extra `.ipynb` under `03_pipeline/` beyond the three stages | Remove or archive outside pipeline |
| Workflow only in a fourth orchestration notebook | Move to `03_pipeline/README.md` |

---

## Related documents

- [notebook_standards.md](notebook_standards.md)
- [documentation_standards.md](documentation_standards.md)
- [coding_standards.md](coding_standards.md)
- [lecturer_identifier_policy.md](lecturer_identifier_policy.md)
- [../portal/implementation.md](../portal/implementation.md)
