# Dataset layout (`02_dataset/`)

This directory stores **all image data, ground-truth labels, trained models, and segmentation outputs** used by the scientific pipeline. Original data must not be overwritten by preprocessing or training notebooks.

Paths are resolved relative to the repository root (see `encontrar_raiz_projeto()` in pipeline library notebooks).

---

## Directory reference

| Directory | Purpose | Produced by | Consumed by |
|-----------|---------|-------------|-------------|
| `images/` | Original ultrasound images (read-only input) | External dataset / course distribution | Preprocessing pipelines 01–05; segmentation when `DATASET_FOLDER = "images"` |
| `labels/` | Ground-truth segmentation masks (read-only) | External dataset / course distribution | Segmentation (`construir_data_dicts`); evaluation (`resolver_caminho_label`) |
| `images_pp_1/` | Preprocessed images — Average filter (`_PP_PL_1`) | `01_preprocessing_pipeline.ipynb` | `fetal_vein_segmentation.ipynb` (`DATASET_FOLDER = "images_pp_1"`) |
| `images_pp_2/` | Preprocessed images — Median filter (`_PP_PL_2`) | `02_preprocessing_pipeline.ipynb` | Segmentation (`images_pp_2`) |
| `images_pp_3/` | Preprocessed images — Gaussian filter (`_PP_PL_3`) | `03_preprocessing_pipeline.ipynb` | Segmentation (`images_pp_3`) |
| `images_pp_4/` | Preprocessed images — Sobel filter (`_PP_PL_4`) | `04_preprocessing_pipeline.ipynb` | Segmentation (`images_pp_4`) |
| `images_pp_5/` | Preprocessed images — Laplacian filter (`_PP_PL_5`) | `05_preprocessing_pipeline.ipynb` | Segmentation (`images_pp_5`) |
| `results_original/` | Predicted masks — original images experiment | `fetal_vein_segmentation.ipynb` (`RESULTS_FOLDER = "results_original"`) | `evaluation.ipynb` |
| `results_pp_1/` … `results_pp_5/` | Predicted masks per preprocessing experiment | `fetal_vein_segmentation.ipynb` (one run per `images_pp_X`) | `evaluation.ipynb` |
| `Save_Models/` | Best checkpoint per experiment (`.pth`) | `fetal_vein_segmentation.ipynb` | Same notebook (inference / resume) |

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

Implementation: `03_pipeline/03_postprocessing/postprocessing_common.ipynb`.

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

Run each preprocessing execution notebook once. Outputs are written directly to `02_dataset/images_pp_{1..5}/`. No separate copy step is required after the pipeline alignment described in the project documentation.
