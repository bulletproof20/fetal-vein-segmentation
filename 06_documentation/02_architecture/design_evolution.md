# Design evolution

**Version:** 4.0  
**Scope:** architectural decisions (WHY the repository is structured as it is)

---

## Initial concept

The project was first planned as a **highly automated pipeline**: a single training entry point, automated environment validation, and interchangeable runtimes (containers, local GPU/CPU adapters) sharing one codebase. That model prioritises operational repeatability and environment independence.

It was explored during early design work recorded under `99_system/` but is **not** the delivered execution model.

---

## Final architecture

The delivered solution is a **notebook-based scientific pipeline** executed on **Google Colab**, with artefacts under `02_dataset/`, processing under `03_pipeline/`, aggregated metrics under `04_pipeline_results/`, and the written report under `05_report/`. Lecturer reference material remains read-only in `01_academic/`.

Operational execution is documented in [`03_pipeline/entrypoint.ipynb`](../../03_pipeline/entrypoint.ipynb). Repository overview and setup are in the root [`README.md`](../../README.md).

---

## Justification

| Factor | Decision |
|--------|----------|
| Assignment focus | Emphasis on preprocessing quality, segmentation, and comparative metrics—not multi-runtime DevOps |
| Experiment load | Baseline plus five preprocessing variants require clear, repeatable stages without adapter overhead |
| Academic transparency | Notebooks expose methodology and parameters for review and grading |
| Reference alignment | Segmentation follows the course UNet/MONAI notebook; the repository adds paths, pairing, and experiment organisation |
| Maintenance | A small number of normative markdown pages plus notebooks reduces duplicated documentation |

---

## Related documents

- [System architecture](system_architecture.md)
- [Data flow](data_flow.md)
