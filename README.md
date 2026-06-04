# Fetal Vein Segmentation

Academic project — **Biomedical Imaging** (IPCA). Semantic segmentation of the fetal umbilical vein in ultrasound images using UNet/MONAI, five preprocessing experiments, morphological post-processing, and quantitative evaluation.

---

## Official workflow

```text
GitHub Repository
        ↓
   Google Colab
        ↓
     02_dataset
        ↓
     03_pipeline  (01_preprocessing → 02_segmentation → 03_evaluation)
        ↓
 04_pipeline_results
        ↓
      05_report
```

**Start here:** [`03_pipeline/README.md`](03_pipeline/README.md) — execution order and stage outputs.

Run the three scientific notebooks in order (each is self-contained; no `%run` between notebooks):

1. [`03_pipeline/01_preprocessing.ipynb`](03_pipeline/01_preprocessing.ipynb)
2. [`03_pipeline/02_segmentation.ipynb`](03_pipeline/02_segmentation.ipynb)
3. [`03_pipeline/03_evaluation.ipynb`](03_pipeline/03_evaluation.ipynb)

---

## Repository structure

| Path | Responsibility |
|------|----------------|
| [`01_academic/`](01_academic/) | Lecturer reference materials (read-only; not modified by the project pipeline) |
| [`02_dataset/`](02_dataset/) | Images, labels, preprocessed data, model checkpoints, prediction masks |
| [`03_pipeline/`](03_pipeline/) | Scientific implementation (three Colab notebooks + pipeline README) |
| [`04_pipeline_results/`](04_pipeline_results/) | Aggregated evaluation tables (e.g. comparison CSV) |
| [`05_report/`](05_report/) | Report template for the written deliverable |
| [`06_documentation/`](06_documentation/) | Architecture and governance (published via MkDocs) |
| [`99_system/`](99_system/) | Design history (initial concept → final decision) |

**Where to read what**

| Question | Location |
|----------|----------|
| How do I run the project? | `03_pipeline/README.md` and the three notebooks above |
| How is data organised? | `02_dataset/README.md` |
| What does each pipeline stage do? | `03_pipeline/README.md` + markdown sections inside each notebook |
| Architecture, data flow, governance | MkDocs site from `06_documentation/` (see below) |
| Lecturer segmentation reference | `01_academic/04_reference_materials/03_code_exemple/FetalVeinSegmentationUS.ipynb` |

---

## Google Colab setup

```python
%cd /content/fetal_vein_segmentation
!pip install -r requirements.txt
```

Run each stage notebook top to bottom. Use the repository root as the working directory (folder containing `02_dataset/` and `03_pipeline/`). Do not use `%run` to load other pipeline notebooks.

---

## Documentation site (MkDocs)

The **academic project portal** (MkDocs) is built from [`06_documentation/`](06_documentation/) — reviewer index for assignment, pipeline, deliverables, and architecture.

```bash
pip install -r requirements-mkdocs.txt
mkdocs build
mkdocs gh-deploy   # after configuring site_url and repo_url in mkdocs.yml
```

See [`06_documentation/MKDOCS_PUBLISHING.md`](06_documentation/MKDOCS_PUBLISHING.md).

---

## Dependencies

```bash
pip install -r requirements.txt
```

Core libraries: PyTorch, MONAI, NumPy, SciPy, scikit-image, Matplotlib, Pandas.

---

## Academic reference

Segmentation methodology follows the lecturer notebook:

`01_academic/04_reference_materials/03_code_exemple/FetalVeinSegmentationUS.ipynb`

Project notebooks adapt paths, experiment configuration, and pipeline organisation without changing the core UNet/MONAI training logic.
