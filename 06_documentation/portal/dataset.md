# Dataset layout (`02_dataset/`)

## Introduction

The `02_dataset/` directory is the **central data layer** of the fetal vein segmentation study. It holds original ultrasound acquisitions, ground-truth annotations, preprocessed image variants produced for controlled comparison, trained model weights, and predicted masks generated during segmentation experiments.

This layout was designed so that each experimental stage — preprocessing, training, inference and evaluation — reads and writes predictable locations without altering source images or labels. The structure therefore supports reproducibility, traceability to the literature review, and direct linkage to the three-stage pipeline documented under `03_pipeline/`.

---

## Purpose within the experimental workflow

| Phase | Role of `02_dataset/` |
|-------|------------------------|
| **Baseline input** | `images/` and `labels/` supply the common reference for all experiments |
| **Preprocessing comparison** | `images_pp_1/` … `images_pp_5/` hold parallel datasets (PP1–PP5) derived from the same patients |
| **Segmentation** | `Save_Models/` and `results_*` store checkpoints and predicted masks per configuration |
| **Evaluation** | Predictions are compared against `labels/`; aggregated metrics are published under `04_pipeline_results/` |

Paths are resolved relative to the repository root (see `find_project_root()` in `03_pipeline/*.ipynb`).

---

## Directory reference

| Directory | Purpose | Produced by | Consumed by |
|-----------|---------|-------------|-------------|
| `images/` | Original ultrasound images (read-only input) | External dataset / course distribution | `01_preprocessing.ipynb`; segmentation when `DATASET_FOLDER = "images"` |
| `labels/` | Ground-truth segmentation masks (read-only) | External dataset / course distribution | `02_segmentation.ipynb`; `03_evaluation.ipynb` |
| `images_pp_1/` | Preprocessed images — Average filter (`_PP_PL_1`) | `01_preprocessing.ipynb` (PP1) | `02_segmentation.ipynb` (`DATASET_FOLDER = "images_pp_1"`) |
| `images_pp_2/` | Preprocessed images — Median filter (`_PP_PL_2`) | `01_preprocessing.ipynb` (PP2) | `02_segmentation.ipynb` (`images_pp_2`) |
| `images_pp_3/` | Preprocessed images — Gaussian filter (`_PP_PL_3`) | `01_preprocessing.ipynb` (PP3) | `02_segmentation.ipynb` (`images_pp_3`) |
| `images_pp_4/` | Preprocessed images — Sobel filter (`_PP_PL_4`) | `01_preprocessing.ipynb` (PP4) | `02_segmentation.ipynb` (`images_pp_4`) |
| `images_pp_5/` | Preprocessed images — Laplacian filter (`_PP_PL_5`) | `01_preprocessing.ipynb` (PP5) | `02_segmentation.ipynb` (`images_pp_5`) |
| `results_original/` | Predicted masks — original images experiment | `02_segmentation.ipynb` (`RESULTS_FOLDER = "results_original"`) | `03_evaluation.ipynb` |
| `results_pp_1/` … `results_pp_5/` | Predicted masks per preprocessing experiment | `02_segmentation.ipynb` (one run per `images_pp_X`) | `03_evaluation.ipynb` |
| `Save_Models/` | Best checkpoint per experiment (`.pth`) | `02_segmentation.ipynb` | Same notebook (inference / resume) |

Aggregated metrics tables are written under `04_pipeline_results/` at the repository root (not inside `02_dataset/`).

---

## Naming and image–label pairing

- **Original images:** e.g. `P080_IMG1.png` in `images/`.
- **Preprocessed images:** `{original_stem}_PP_PL_{N}.png`, e.g. `P080_IMG1_PP_PL_1.png` in `images_pp_1/`.
- **Labels:** same stem as the original image, e.g. `P080_IMG1.png` in `labels/`.

Pairing is performed by **original identifier**, not by list position:

1. Remove the suffix `_PP_PL_<N>` when present.
2. Resolve `labels/{original_id}.png`.

Example: `P080_IMG1_PP_PL_1.png` → `P080_IMG1.png`.

Implementation: `resolve_label_path()` in `03_pipeline/03_evaluation.ipynb` (and pairing helpers in `02_segmentation.ipynb` for training).

---

## Expected model files (`Save_Models/`)

| File | Experiment |
|------|------------|
| `best_metric_model_original.pth` | Training on `images/` |
| `best_metric_model_pp_1.pth` … `best_metric_model_pp_5.pth` | Training on `images_pp_1` … `images_pp_5` |

---

## Data integrity rules

1. Do not modify files in `images/` or `labels/`.
2. Preprocessing writes only to `images_pp_*`.
3. Segmentation writes predictions only to `results_*` and weights only to `Save_Models/`.
4. Evaluation reads predictions and labels; it does not alter ground truth.

---

## Populating preprocessed folders

Run all cells in `03_pipeline/01_preprocessing.ipynb` once. Outputs are written directly to `02_dataset/images_pp_{1..5}/`.

---

## Summary

The dataset tree separates **immutable inputs** (`images/`, `labels/`), **experimental variants** (`images_pp_*`), and **model outputs** (`Save_Models/`, `results_*`). Licensing and attribution requirements are documented in `01_academic/03_dataset_documentation/licence.md`. Quantitative outcomes based on these artefacts are reported under `04_pipeline_results/` and `05_report/`, following the workflow defined in `03_pipeline/README.md`.
