# Lecturer-derived identifier preservation policy

**Version:** 6.0  
**Status:** normative  
**Scope:** identifiers in `03_pipeline/` and project documentation

The project **intentionally follows** lecturer reference material in `01_academic/`. Some names are preserved to maintain academic traceability and avoid unnecessary divergence from the reference implementation.

Companion: [semantic_naming_policy.md](semantic_naming_policy.md), [naming_conventions.md](naming_conventions.md).

---

## 1. Preservation criteria

An identifier **may remain unchanged** during refactoring when **all** of the following apply:

1. It is **academically established** in the course reference notebooks or slides.
2. It is **directly derived** from lecturer code the pipeline adapts (paths and organisation only).
3. It is **recognised** in MONAI/PyTorch documentation or standard image-processing literature.
4. Renaming would **not** reduce ambiguity in this repository (i.e. the name is already unambiguous in context).

If criterion 4 fails, apply [semantic_naming_policy.md](semantic_naming_policy.md) even when the lecturer used a short name.

---

## 2. Preserved project functions (normative list)

These **user-defined** function names must **not** be renamed in Phase 3 unless academic approval is obtained:

| Identifier | Source | Role |
|------------|--------|------|
| `pos_process()` | `01_academic/.../Pos_Metrics.ipynb` | Morphological post-processing before metrics |
| `calculate_metrics()` | `01_academic/.../Pos_Metrics.ipynb` | Dice, accuracy, precision, recall |

Project wrappers (`resolve_label_path`, `find_project_root`, etc.) remain governed by [naming_conventions.md](naming_conventions.md).

---

## 3. Preserved framework and literature identifiers

Do **not** rename symbols imported from libraries or defined by MONAI/PyTorch:

| Category | Examples |
|----------|----------|
| MONAI networks | `UNet` |
| MONAI losses / metrics | `DiceLoss`, `DiceMetric` |
| MONAI transforms | `LoadImaged`, `RandFlipd`, `Compose`, `EnsureChannelFirstd`, etc. |
| PyTorch | `torch`, `nn`, `optim`, tensor methods |
| Common ML abbreviations in framework docs | `batch`, `epoch` in MONAI training loops where matching lecturer structure |

---

## 4. Preserved parameters and locals (limited)

| Identifier | Allowed scope | Requirement |
|------------|---------------|-------------|
| `gt` | `calculate_metrics(predicted, gt)` signature | Document lecturer alignment in docstring |
| `predicted` | `pos_process(predicted, ...)` | Matches lecturer `Pos_Metrics` |
| `tp`, `tn`, `fp`, `fn` | Inside `calculate_metrics()` | Confusion-matrix standard |
| `dice`, `ac`, `pr`, `re` | Return tuple of `calculate_metrics()` | Lecturer metric naming |

For new code **outside** these functions, use semantic names (`ground_truth_mask`, `dice_score`, etc.).

---

## 5. Refactor protection rule (normative)

> **An identifier shall not be renamed solely because it is not perfectly descriptive.**

Renaming is **justified** only when one or more of the following hold:

| Justification | Example |
|---------------|---------|
| Readability improves | `filtro_gaussian` → `apply_gaussian_filter` (English + verb-led) |
| Ambiguity is reduced | `mask` → `prediction_mask` vs `ground_truth_mask` in same cell |
| Maintainability improves | `aplicar_operacoes_globais` → `apply_configured_global_operations` |
| Consistency improves | All filters use `apply_*_filter` prefix |

Renaming is **not justified** when:

- The name is on the preserved list (§2–§4).
- The change is cosmetic (e.g. `calculate_metrics` → `compute_metrics`) without ambiguity benefit.
- The name is established scientific terminology (`DiceMetric`, `UNet`).
- Translation replaces Portuguese with an equally vague English term (`mascara` → `mask` instead of `binary_mask`).

---

## 6. Portuguese identifiers

Portuguese function or variable names (`filtro_*`, `altura`, `caminho`) are **not** lecturer-preservation cases. They require English **semantic** renames in Phase 3.

---

## 7. Immutable reference material

`01_academic/` notebooks may use Google Drive paths, `cuda()`, and Portuguese prose. The pipeline **adapts** behaviour to the repository layout without requiring the academic folder to change.

`02_dataset/README.md` may reference legacy function names. Pipeline code uses current names; no edit to `02_dataset/` is required for preservation policy.

---

## 8. Audit implications

| Finding | Treatment under this policy |
|---------|----------------------------|
| `pos_process`, `calculate_metrics` | **Compliant** — do not rename |
| `DiceMetric`, `UNet`, MONAI transforms | **Compliant** — framework |
| `gt` in metrics function | **Compliant** — document only |
| `filtro_gaussian`, `aplicar_*` | **Non-compliant** — rename in Phase 3 |
| `img`, `mask` without qualifier | **Non-compliant** — apply semantic policy |

---

## 9. Related documents

- [semantic_naming_policy.md](semantic_naming_policy.md)
- [scientific_notebook_standards.md](scientific_notebook_standards.md)
- [coding_standards.md](coding_standards.md) §9 (scientific constraints)
