# Fetal Vein Segmentation Using Deep Learning and Image Processing Techniques

This project addresses **semantic segmentation of the fetal umbilical vein** in ultrasound images. Five classical preprocessing strategies (PP1–PP5) are compared against an original-image baseline; a **UNet** model (MONAI/PyTorch) is trained under identical conditions for each variant; and **mathematical morphology** is applied to refine predicted masks.

**Course:** Processamento de Imagem Biomédica (EIM) · IPCA

**Lecturer:** Helena Torres

### Authors

**Ivo Sá** — Student Number: 22604

**Diogo Sousa** — Student Number: 22588

---

## Summary

The experimental pipeline evaluates whether preprocessing and post-processing improve deep-learning segmentation of the fetal umbilical vein. Metrics are exported to `04_pipeline_results/`; the written report is in `05_report/`.

---

## Navigation

| Section | Description |
|---------|-------------|
| [Project Overview](portal/project_overview.md) | Workflow and objectives |
| [Assignment](portal/assignment.md) | Official brief (PDF) |
| [State of the Art](portal/state_of_the_art.md) | Literature review |
| [Dataset](portal/dataset.md) | Data layout and pairing |
| [Results](portal/results.md) | Metrics and training analysis |
| [Final Report](portal/final_report.md) | Submitted PDF |
| [Scientific Pipeline](portal/pipeline.md) | Three-stage notebooks |
| [Governance](01_governance/project_governance.md) | Project standards |

---

## Repository map

| Path | Role |
|------|------|
| `01_academic/` | Assignment, literature, dataset licence |
| `02_dataset/` | Images, labels, models, masks |
| `03_pipeline/` | Preprocessing · segmentation · evaluation |
| `04_pipeline_results/` | CSV tables and training figures |
| `05_report/` | Results narrative and final PDF |
| `06_documentation/` | This site |

---

## About this site

MkDocs renders repository source files via snippets and links to GitHub for binaries (PDFs, notebooks, CSV). Authoritative content lives in the repository tree, not in duplicated portal copies.

Deploy: `mkdocs gh-deploy` from the repository root (see `06_documentation/MKDOCS_PUBLISHING.md`).
