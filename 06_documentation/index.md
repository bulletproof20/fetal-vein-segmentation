# Fetal Vein Segmentation Using Deep Learning and Image Processing Techniques

This project addresses **semantic segmentation of the fetal umbilical vein** in ultrasound images. Five classical preprocessing strategies (PP1–PP5) are compared against an original-image baseline; a **UNet** model (MONAI/PyTorch) is trained under identical conditions for each variant; and **mathematical morphology** is applied to refine predicted masks. Results are reported through metric tables, training analysis, and a formal written report.

**Course:** Processamento de Imagem Biomédica (EIM) · IPCA

**Lecturer:** Helena Torres

### Authors

**Ivo Sá**  
Student Number: 22604

**Diogo Sousa**  
Student Number: 22588

---

## Summary

The experimental pipeline evaluates whether preprocessing and post-processing improve deep-learning segmentation of the fetal umbilical vein. Each preprocessing variant produces a dedicated dataset; segmentation models are trained with a shared protocol; and morphological operators (erosion, dilation, opening, closing) are compared through quantitative metrics exported to `04_pipeline_results/`.

---

## Objectives

- Construct reproducible preprocessed datasets from the same acquisitions (PP1–PP5).
- Train and evaluate segmentation models per preprocessing variant with consistent protocol.
- Quantify the impact of erosion, dilation, opening, and closing on segmentation metrics.
- Document methodology, governance, and traceability for academic review.

---

## Quick navigation

| Section | Description |
|---------|-------------|
| [Project Overview](portal/project_overview.md) | Workflow, experimental design, deliverables |
| [Assignment](portal/assignment.md) | Official project brief (PDF) |
| [Literature](portal/literature.md) | Bibliography and sources |
| [Articles](portal/articles.md) | Annotated bibliography index |
| [State of the Art](portal/state_of_the_art.md) | Formal literature review |
| [Dataset](portal/dataset.md) | Data layout, pairing, licence |
| [Scientific Pipeline](portal/pipeline.md) | Three-stage notebook workflow |
| [Results](portal/results.md) | Training curves, metrics, conclusions |
| [Final Report](portal/final_report.md) | Submitted PDF report |
| [Implementation](portal/implementation.md) | Notebook and execution index |
| [Documentation](02_architecture/system_architecture.md) | Architecture and governance |

---

## Repository map

| Path | Role |
|------|------|
| `01_academic/` | Assignment, literature, dataset licence, lecturer references |
| `02_dataset/` | Images, labels, preprocessed data, models, masks |
| `03_pipeline/` | Preprocessing · segmentation · evaluation notebooks |
| `04_pipeline_results/` | Evaluation CSV tables and training figures |
| `05_report/` | Results narrative and final PDF |
| `06_documentation/` | This website |

**Run the project:** [Scientific Pipeline](portal/pipeline.md)

---

## About this site

This MkDocs site is a **navigation layer** over the repository: it indexes academic artefacts, links to PDFs and notebooks, and documents architecture and standards. Algorithms and parameters remain in the pipeline notebooks; governance policies remain in `06_documentation/01_governance/`.

Repository artefacts (PDFs, notebooks, CSV files, figures) are mirrored under `repo_files/` at build time so links work in the generated site. Deploy instructions: `06_documentation/MKDOCS_PUBLISHING.md` (excluded from navigation; open in the repository).
