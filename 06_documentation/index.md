# Fetal Vein Segmentation

**IPCA — Biomedical Imaging** · Academic project portal

Semantic segmentation of the fetal umbilical vein in ultrasound: five preprocessing variants (PP1–PP5), UNet/MONAI training, morphological post-processing, and comparative evaluation against ground-truth labels.

---

## Start here

| | |
|---|---|
| **[Assignment specification](portal/academic.md#assignment)** | What the project had to deliver |
| **[Run the project](portal/implementation.md#start-here-execution-index)** | Official guide: `entrypoint.ipynb` |
| **[Academic materials](portal/academic.md)** | Literature, licence, lecturer references |
| **[Deliverables](portal/deliverables.md)** | Report template and evaluation outputs |
| **[Reference implementation](portal/academic.md#lecturer-reference-implementation)** | Lecturer UNet/metrics notebooks |

**Design rationale:** [Project → Architecture](02_architecture/system_architecture.md)

---

## Repository map

| Path | Role |
|------|------|
| `01_academic/` | Assignment, literature, dataset licence, course references |
| `02_dataset/` | Images, labels, preprocessed data, models, masks |
| `03_pipeline/` | Notebooks — implementation and execution |
| `04_pipeline_results/` | Aggregated evaluation tables |
| `05_report/` | Written report template |
| `06_documentation/` | This website (index + architecture + standards) |

---

## What this website is

| On this site | In the repository |
|--------------|-------------------|
| Academic artefact index | PDF, DOCX, notebook **content** |
| Pipeline & notebook links | Algorithms and parameters |
| Architectural **why** | Step-by-step **how** ([entrypoint](portal/implementation.md)) |
| Standards index | Governance policy text |

This site is a **concierge desk**, not a second copy of the repository.

---

## Open repository

Browse the full project on GitHub: configure `repository_owner` in `includes/repo_links.md` (used by portal pages), set `repo_url` in `mkdocs.yml`, then deploy.

Authors: see `06_documentation/MKDOCS_PUBLISHING.md` in the repository.

---

## Quick links

- [Academic](portal/academic.md) · [Implementation](portal/implementation.md) · [Deliverables](portal/deliverables.md)
- [Project](02_architecture/system_architecture.md) · [Standards](01_governance/project_governance.md)
