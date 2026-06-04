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

Each concept has **one authoritative location**. Other locations link to it; they do not restate implementation detail.

| Concept | Authoritative location | May reference, not duplicate |
|---------|------------------------|------------------------------|
| Repository overview, Colab setup, directory map | Root `README.md` | MkDocs home |
| System architecture, data flow, design summary | `06_documentation/02_architecture/` (MkDocs) | `99_system/design_history.md` for narrative |
| Execution order (high level) | `06_documentation/02_architecture/execution_workflow.md` | `03_pipeline/entrypoint.ipynb` |
| Dataset folder contract | `02_dataset/README.md` (immutable) | MkDocs `external/dataset_layout.md` (snippet) |
| Pipeline stage summary | `03_pipeline/README.md` | MkDocs `external/pipeline_overview.md` |
| Governance rules | `06_documentation/01_governance/` | Templates in `03_templates/` |
| Preprocessing methodology | `03_pipeline/01_preprocessing/` notebooks | — |
| Filtering implementation | `03_pipeline/01_preprocessing/00_common/02_filtering.ipynb` | — |
| Segmentation implementation | `03_pipeline/02_segmentation/fetal_vein_segmentation.ipynb` | — |
| Post-processing and metrics | `03_pipeline/03_postprocessing/postprocessing_common.ipynb` | — |
| Evaluation implementation | `03_pipeline/04_evaluation/evaluation.ipynb` | — |
| Written report deliverable | `05_report/template.docx` | — |

---

## 3. Markdown responsibility

Markdown **is responsible for:**

- Architecture and repository organisation
- Governance and naming policy
- Workflows and execution order (without algorithm steps)
- Design decisions and technology stack
- MkDocs site structure and publishing instructions
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
| Purpose | Publish architecture, governance, design history wrappers |
| Build | `mkdocs build` from repository root |
| Deploy | `mkdocs gh-deploy` after `site_url` / `repo_url` configured |
| Links | Use site-relative paths; avoid broken `../` links outside `docs_dir` |
| Snippets | `external/*.md` may include `02_dataset/README.md`, `03_pipeline/README.md`, `99_system/design_history.md` via pymdown snippets |

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

## 7. Templates (`06_documentation/03_templates/`)

Templates illustrate governance compliance. When governance changes, templates must be updated in the same phase.

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
- [../MKDOCS_PUBLISHING.md](../MKDOCS_PUBLISHING.md)
