# Scientific pipeline (`03_pipeline/`)

Notebook-based fetal vein segmentation workflow executed on **Google Colab**.

**Start here:** [`entrypoint.ipynb`](entrypoint.ipynb)

---

## Official workflow

```text
GitHub → Google Colab → 02_dataset → 03_pipeline → 04_pipeline_results → 05_report
```

---

## Structure

| Stage | Path | Type |
|-------|------|------|
| Guide | `entrypoint.ipynb` | Orchestration (markdown only) |
| Preprocessing library | `01_preprocessing/00_common/` | Library (`%run`) |
| Preprocessing runs | `01_preprocessing/0N_preprocessing_pipeline.ipynb` | Execution |
| Segmentation | `02_segmentation/fetal_vein_segmentation.ipynb` | Execution |
| Post-processing library | `03_postprocessing/postprocessing_common.ipynb` | Library |
| Evaluation | `04_evaluation/evaluation.ipynb` | Execution |

---

## Library vs execution notebooks

| Type | Behaviour |
|------|-----------|
| **Library** | Defines functions; imported via `%run`; not experiment entry points |
| **Execution** | Reads/writes `02_dataset/`; evaluation writes `04_pipeline_results/` |

---

## Documentation

- [`../02_dataset/README.md`](../02_dataset/README.md)
- [`entrypoint.ipynb`](entrypoint.ipynb) (execution workflow)
- [`../06_documentation/02_architecture/`](../06_documentation/02_architecture/) (architectural rationale)
- [`../99_system/design_history.md`](../99_system/design_history.md)
