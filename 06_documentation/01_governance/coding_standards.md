# Coding standards

**Version:** 5.0  
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
| Docstrings | All library functions |
| Notebook markdown | Headers, explanations, assumptions |
| Print / log output | User-facing messages |
| Exceptions | `raise` and error strings |
| Project markdown | `06_documentation/`, `99_system/`, root `README.md` |

**Exceptions:** `01_academic/`, `02_dataset/` remain untouched (may contain Portuguese or lecturer naming).

---

## 2. Python style

| Rule | Requirement |
|------|-------------|
| Style guide | [PEP 8](https://peps.python.org/pep-0008/) where applicable |
| Indentation | 4 spaces |
| Line length | Prefer ≤ 100 characters; break long MONAI chains readably |
| Imports | Standard library → third party → project; no unused imports |
| Types | Type hints on new or refactored library functions (`Path`, `np.ndarray`, etc.) |
| Framework APIs | Do not rename MONAI, PyTorch, NumPy, Pandas, Matplotlib symbols |

---

## 3. Notebook types

### Library notebooks

- **Locations:** `03_pipeline/01_preprocessing/00_common/`, `03_pipeline/03_postprocessing/postprocessing_common.ipynb`
- **Import:** `%run` from execution notebooks only
- **Must not:** act as experiment entry points; write experiment artefacts when imported passively
- **Header:** `**Type:** library notebook (import via %run; not an experiment entry point).`

### Execution notebooks

- **Locations:** preprocessing `0N_preprocessing_pipeline.ipynb`, `fetal_vein_segmentation.ipynb`, `evaluation.ipynb`
- **Must:** declare `**Type:** execution notebook` in the first markdown cell
- **Must:** follow [notebook_standards.md](notebook_standards.md) section order where applicable
- **Orchestration:** `entrypoint.ipynb` is markdown-only guidance (no scientific implementation)

### Entry point notebook

- `03_pipeline/entrypoint.ipynb` — workflow and pointers only; no algorithm implementation

---

## 4. Comment and documentation style

See [comment_standards.md](comment_standards.md).

- Comments explain **intent** and **why**, not redundant labels.
- Docstrings: purpose, arguments, returns, raises (library functions).
- No Portuguese in comments or docstrings (policy §1).

---

## 5. Readability requirements

| Requirement | Detail |
|-------------|--------|
| Configuration | Top-of-notebook cell labelled `EXPERIMENT CONFIGURATION` or stage equivalent |
| Section headers | Markdown `##` hierarchy; match [notebook_standards.md](notebook_standards.md) |
| Magic numbers | Named constants in configuration or module-level `UPPER_CASE` |
| Dead code | Remove commented-out experiment blocks unless marked `ARCHIVE` with reason |
| Duplication | Shared logic in library notebooks, not copy-pasted across execution notebooks |

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
| Aggregated metrics | `04_pipeline_results/` (evaluation notebook) |

---

## 8. Image–label pairing

- Pair by **original identifier** (`P080_IMG1`), never by sorted list index alone.
- Use `resolve_label_path()` from `postprocessing_common.ipynb`.
- Strip `_PP_PL_N` suffix before resolving labels.

---

## 9. Scientific constraints (non-negotiable without academic approval)

Do not alter:

- Preprocessing filter mathematics (convolution, morphology in preprocessing stage)
- UNet architecture and MONAI transform pipeline core
- Dice loss, training loop structure, checkpoint selection logic
- `pos_process()` morphology (opening + largest connected component)
- `calculate_metrics()` definitions (Dice, accuracy, precision, recall)
- Train/validation/test split sizes where tied to lecturer reference

Refactoring may rename identifiers and improve prose **only** if behaviour remains identical.

---

## 10. Related documents

- [naming_conventions.md](naming_conventions.md)
- [documentation_standards.md](documentation_standards.md)
- [notebook_standards.md](notebook_standards.md)
- [../02_architecture/execution_workflow.md](../02_architecture/execution_workflow.md)
