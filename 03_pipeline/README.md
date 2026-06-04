# Scientific pipeline (`03_pipeline/`)

Three **self-contained** notebooks for Google Colab — no `%run` between stages.

| Stage | Notebook | Output |
|-------|----------|--------|
| Pre-processing | [`01_preprocessing.ipynb`](01_preprocessing.ipynb) | `02_dataset/images_pp_1/` … `images_pp_5/` |
| Segmentation | [`02_segmentation.ipynb`](02_segmentation.ipynb) | `Save_Models/*.pth`, `02_dataset/results_*` |
| Evaluation | [`03_evaluation.ipynb`](03_evaluation.ipynb) | `04_pipeline_results/tabela_avaliacao_experiencias.csv` |

---

## Workflow

```text
01_preprocessing.ipynb  →  02_segmentation.ipynb  →  03_evaluation.ipynb
```

1. Run **all cells** in `01_preprocessing.ipynb` to populate `images_pp_1` … `images_pp_5`.
2. Run `02_segmentation.ipynb` once per experiment row in its configuration table (Original + PP1–PP5).
3. Run `03_evaluation.ipynb` to compute metrics with and without `pos_process()` and write the comparison CSV.

Evaluation follows `Pos_Metrics.ipynb`: metrics on raw predictions and after morphological post-processing.

---

## Google Colab

Clone the repository, install `requirements.txt` from the repo root, then open each notebook in the order above. Each notebook contains its own **Dependencies** cell; do not load sibling pipeline notebooks with `%run`.

---

## Documentation

- [`../02_dataset/README.md`](../02_dataset/README.md)
- [`../06_documentation/portal/implementation.md`](../06_documentation/portal/implementation.md)
