# Coding standards

**Version:** 6.0  
**Status:** normative  
**Scope:** `03_pipeline/`, root configuration, and any future project Python outside protected directories

Authoritative companions: [naming_conventions.md](naming_conventions.md), [comment_standards.md](comment_standards.md), [notebook_standards.md](notebook_standards.md).

---

## 1. Repository language policy

**English only** in all project-authored content outside `01_academic/` and `02_dataset/`.

| Must be English | Examples |
|-----------------|----------|
| Code | Function bodies, assignments |
| Identifiers | Functions, variables, parameters (see naming doc) |
| Comments | Inline and block comments |
| Docstrings | All public helper functions |
| Notebook markdown | Headers, explanations, assumptions |
| Print / log output | User-facing messages |
| Exceptions | `raise` and error strings |
| Project markdown | `06_documentation/`, `99_system/`, root `README.md` |

**Exceptions:** `01_academic/` remains untouched (may contain Portuguese or lecturer naming). `02_dataset/` data files are immutable; its README is project documentation and follows this policy.

---

## 2. Python style

| Rule | Requirement |
|------|-------------|
| Style guide | [PEP 8](https://peps.python.org/pep-0008/) where applicable |
| Indentation | 4 spaces |
| Line length | Prefer ≤ 100 characters; break long MONAI chains readably |
| Imports | Standard library → third party → project; no unused imports |
| Types | Type hints on new or refactored public functions (`Path`, `np.ndarray`, etc.) |
| Framework APIs | Do not rename MONAI, PyTorch, NumPy, Pandas, Matplotlib symbols |

---

## 3. Pipeline notebooks

| Rule | Detail |
|------|--------|
| Files | `01_preprocessing.ipynb`, `02_segmentation.ipynb`, `03_evaluation.ipynb` only |
| Model | Each file is a **self-contained** execution notebook |
| `%run` | Must not load other pipeline notebooks |
| Header | `**Type:** execution notebook (self-contained; …)` per [notebook_standards.md](notebook_standards.md) |
| Shared logic | Define helpers in the same notebook (grouped sections), not in separate library `.ipynb` files |
| Workflow text | Execution order in `03_pipeline/README.md`, not in code |

---

## 4. Comment and documentation style

See [comment_standards.md](comment_standards.md).

- Comments explain **intent** and **why**, not redundant labels.
- Docstrings: purpose, arguments, returns, raises (public helpers).
- No Portuguese in comments or docstrings (policy §1).

---

## 5. Readability requirements

| Requirement | Detail |
|-------------|--------|
| Configuration | Top-of-stage cell labelled `EXPERIMENT CONFIGURATION` or equivalent |
| Section headers | Markdown `##` hierarchy; match [notebook_standards.md](notebook_standards.md) |
| Magic numbers | Named constants in configuration or module-level `UPPER_CASE` |
| Dead code | Remove commented-out experiment blocks unless marked `ARCHIVE` with reason |
| Duplication | Avoid copy-pasting large blocks across the three notebooks; shared behaviour stays in one stage file |

---

## 6. Paths and runtime

| Rule | Detail |
|------|--------|
| Root resolution | `find_project_root()` — walk up until `02_dataset/` exists |
| Paths | `pathlib.Path`; repository-relative segments |
| Forbidden | Hard-coded `/content/drive/...`, local machine paths, Docker/bootstrap entry points as active workflow |
| Official runtime | Google Colab after clone from GitHub |

---

## 7. Data integrity

| Rule | Detail |
|------|--------|
| Read-only | `02_dataset/images/`, `02_dataset/labels/` |
| Preprocessing output | `02_dataset/images_pp_{1..5}/` only |
| Predictions | `02_dataset/results_*` only |
| Models | `02_dataset/Save_Models/*.pth` only |
| Aggregated metrics | `04_pipeline_results/` (`03_evaluation.ipynb`) |

---

## 8. Image–label pairing

- Pair by **original identifier** (`P080_IMG1`), never by sorted list index alone.
- Use `resolve_label_path()` from `03_evaluation.ipynb` (and pairing helpers in `02_segmentation.ipynb` for training).
- Strip `_PP_PL_N` suffix before resolving labels.

---

## 9. Scientific constraints (non-negotiable without academic approval)

Do not alter:

- Core UNet/MONAI training logic inherited from the lecturer reference
- Lecturer function names preserved by [lecturer_identifier_policy.md](lecturer_identifier_policy.md)
- Experiment comparison structure (Original + PP1–PP5; metrics with and without `pos_process`)

---

## 10. Related documents

- [scientific_notebook_standards.md](scientific_notebook_standards.md)
- [project_governance.md](project_governance.md)
