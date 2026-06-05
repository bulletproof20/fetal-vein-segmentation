# Documentation standards

**Version:** 6.0  
**Status:** normative  
**Scope:** all project-authored documentation outside `01_academic/` and immutable dataset files

---

## 1. Language

- **English only** (academic, technical, professional tone).
- No Portuguese in markdown, tables, or MkDocs pages under project control.
- **Exception:** content inside `01_academic/` (immutable).

---

## 2. Documentation hierarchy (single source of truth)

Each concept has **one authoritative location**. The MkDocs site is a **reviewer portal**; thin portal pages use snippets or GitHub links—no mirrored copies.

| Concept | Authoritative location | MkDocs |
|---------|------------------------|--------|
| Repository overview | Root `README.md` | `index.md` (Home) |
| Literature review | `01_academic/02_literature/state_of_the_art.md` | Project → State of the Art |
| Dataset layout | `02_dataset/README.md` | Project → Dataset → Overview |
| Dataset licence | `01_academic/03_dataset_documentation/licence.md` | Project → Dataset → Licence |
| Pipeline workflow | `03_pipeline/README.md` | Technical Documentation → Scientific Pipeline |
| Execution index / traceability | Repository tree | Additional Documentation |
| Architecture, data flow | `06_documentation/02_architecture/` | Technical Documentation |
| Governance | `06_documentation/01_governance/` | Technical Documentation → Governance |
| Notebook structure (self-contained stages) | `scientific_notebook_standards.md`, `notebook_standards.md` | — |
| Preprocessing methodology | `03_pipeline/01_preprocessing.ipynb` | — |
| Segmentation | `03_pipeline/02_segmentation.ipynb` | — |
| Evaluation & post-processing | `03_pipeline/03_evaluation.ipynb` | `04_pipeline_results/` |
| Written report deliverable | `05_report/template.docx` | `portal/deliverables.md` |

---

## 3. Markdown responsibility

Markdown **is responsible for:**

- Architecture and repository organisation
- Governance and naming policy
- Execution index and design rationale (without algorithm steps)
- MkDocs portal structure and publishing instructions
- Pointers to notebooks and READMEs

Markdown **must not:**

- Reproduce notebook code line-by-line
- Duplicate filter equations, training loops, or metric formulas
- Replace notebook markdown as the methodology textbook

When implementation detail is required, use:

```markdown
See `03_pipeline/02_segmentation.ipynb` (Segmentation section).
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

---

## 5. MkDocs (`06_documentation/`)

| Rule | Detail |
|------|--------|
| Purpose | Reviewer portal: Project + Technical Documentation |
| Build | `mkdocs build --strict` from repository root |
| Deploy | `mkdocs gh-deploy` (once per release) |
| Snippets | `pymdownx.snippets` for authoritative Markdown outside `docs_dir` |
| Binaries | Link to GitHub (`blob` / `raw`) for PDFs, notebooks, CSV, figures |

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

Normative notebook layout is defined in [scientific_notebook_standards.md](scientific_notebook_standards.md) and [notebook_standards.md](notebook_standards.md).

---

## 8. Forbidden documentation content

Do not document as **active workflow**:

- Docker / docker-compose execution
- Local Jupyter server as requirement
- Bootstrap or `99_system` runtime adapters (historical mention only in design history)
- Kaggle as official runtime
- `%run` chains between pipeline notebooks
- Separate library notebooks under `03_pipeline/`

---

## 9. Related documents

- [project_governance.md](project_governance.md)
- [notebook_standards.md](notebook_standards.md)
- Maintainer guide: `06_documentation/MKDOCS_PUBLISHING.md` (repository only; excluded from site build)
