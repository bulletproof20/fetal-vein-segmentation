# Documentation standards

**Version:** 5.0  
**Status:** normative  
**Scope:** all project-authored documentation outside `01_academic/` and `02_dataset/`

---

## 1. Language

- **English only** (academic, technical, professional tone).
- No Portuguese in markdown, tables, or MkDocs pages under project control.
- **Exception:** content inside `01_academic/` and `02_dataset/` (immutable).

---

## 2. Documentation hierarchy (single source of truth)

Each concept has **one authoritative location**. The MkDocs site is a **reviewer portal** (Home, Academic, Implementation, Deliverables, Project). Portal pages index and link; they do not duplicate implementation detail.

| Concept | Authoritative location | MkDocs portal index |
|---------|------------------------|---------------------|
| Repository overview, Colab setup, directory map | Root `README.md` | `index.md` (Home) |
| Academic context, deliverables map | `01_academic/` (immutable) | `portal/academic.md`, `portal/deliverables.md` |
| Implementation index, notebook and README pointers | `03_pipeline/entrypoint.ipynb`, `03_pipeline/README.md`, `02_dataset/README.md` | `portal/implementation.md` |
| Lecturer ↔ pipeline traceability | Notebook identifiers + pipeline layout | `portal/traceability.md` |
| System architecture, data flow, design rationale | `06_documentation/02_architecture/` | Project → Architecture, Data Flow, Design Decisions |
| Governance rules | `06_documentation/01_governance/` | Project → Standards & Governance |
| Notebook structure (Category A/B/C) | `scientific_notebook_standards.md`, `notebook_standards.md` | — |
| Preprocessing methodology | `03_pipeline/01_preprocessing/` notebooks | — |
| Filtering implementation | `03_pipeline/01_preprocessing/00_common/02_filtering.ipynb` | — |
| Segmentation implementation | `03_pipeline/02_segmentation/fetal_vein_segmentation.ipynb` | — |
| Post-processing and metrics | `03_pipeline/03_postprocessing/postprocessing_common.ipynb` | — |
| Evaluation implementation | `03_pipeline/04_evaluation/evaluation.ipynb` | — |
| Written report deliverable | `05_report/template.docx` | `portal/deliverables.md` |

---

## 3. Markdown responsibility

Markdown **is responsible for:**

- Architecture and repository organisation
- Governance and naming policy
- Execution index and design rationale (without algorithm steps)
- MkDocs portal structure and publishing instructions
- Pointers to notebooks and immutable READMEs

Markdown **must not:**

- Reproduce notebook code line-by-line
- Duplicate filter equations, training loops, or metric formulas
- Replace notebook markdown as the methodology textbook

When implementation detail is required, use:

```markdown
See `03_pipeline/02_segmentation/fetal_vein_segmentation.ipynb` (Segmentation section).
```

---

## 4. Notebook responsibility

Notebooks **are responsible for:**

- Scientific methodology and experiment description
- Configuration and execution
- Validation, visualisation, and outputs
- Inline assumptions and limitations

Notebooks **must not:**

- Redefine full repository architecture (link to MkDocs instead)
- Duplicate root `README.md` setup instructions at length
- Contain governance policy text (link to `06_documentation/01_governance/`)

**Exception:** `entrypoint.ipynb` may summarise workflow for first-time runners (orchestration only).

---

## 5. MkDocs (`06_documentation/`)

| Rule | Detail |
|------|--------|
| Purpose | Reviewer portal: Home, Academic, Implementation, Deliverables, Project |
| Build | `mkdocs build` from repository root |
| Deploy | `mkdocs gh-deploy` after `site_url` / `repo_url` configured |
| Links | Use site-relative paths within `docs_dir`; link to repo READMEs and notebooks from `portal/implementation.md` |
| Snippets | `includes/repo_links.md` for GitHub URLs (not a published page) |

---

## 6. Document structure (normative pages)

Each governance and architecture page should include:

```markdown
# Title

**Version:** X.Y  
**Status:** draft | normative | archived  
**Scope:** …

---

## Content sections…
```

---

## 7. Notebook authoring structure

Normative notebook layout is defined in [scientific_notebook_standards.md](scientific_notebook_standards.md) and [notebook_standards.md](notebook_standards.md). There are no separate published template pages.

---

## 8. Forbidden documentation content

Do not document as **active workflow**:

- Docker / docker-compose execution
- Local Jupyter server as requirement
- Bootstrap or `99_system` runtime adapters (historical mention only in design history)
- Kaggle as official runtime

---

## 9. Related documents

- [project_governance.md](project_governance.md)
- [notebook_standards.md](notebook_standards.md)
- Maintainer guide: `06_documentation/MKDOCS_PUBLISHING.md` (repository only; excluded from site build)
