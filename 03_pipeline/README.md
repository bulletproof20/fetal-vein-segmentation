# Scientific Pipeline (`03_pipeline/`)

The scientific workflow is organised into three independent computational stages responsible for image preprocessing, segmentation model training and quantitative evaluation. Each stage is implemented as a self-contained notebook to ensure reproducibility, modularity and clear separation of responsibilities.

| Stage         | Notebook                 | Purpose                                                                          | Main Outputs                                |
| ------------- | ------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------- |
| Preprocessing | `01_preprocessing.ipynb` | Generation of enhanced image datasets through multiple filtering strategies      | `02_dataset/images_pp_1/` … `images_pp_5/`  |
| Segmentation  | `02_segmentation.ipynb`  | Training and inference of the segmentation model                                 | `Save_Models/*.pth`, `02_dataset/results_*` |
| Evaluation    | `03_evaluation.ipynb`    | Quantitative assessment of segmentation performance and post-processing analysis | `04_pipeline_results/*.csv`                 |

---

## Pipeline Structure

```text
Raw Ultrasound Images
          │
          ▼
01_preprocessing.ipynb
          │
          ▼
Preprocessed Datasets
(PP1–PP5)
          │
          ▼
02_segmentation.ipynb
          │
          ▼
Predicted Segmentation Masks
          │
          ▼
03_evaluation.ipynb
          │
          ▼
Performance Metrics
and Comparative Analysis
```

---

## Preprocessing Stage

The preprocessing stage generates alternative image representations intended to reduce noise and enhance image characteristics prior to segmentation.

The following preprocessing strategies are evaluated:

| Configuration | Description      |
| ------------- | ---------------- |
| Original      | No preprocessing |
| PP1           | Average Filter   |
| PP2           | Median Filter    |
| PP3           | Gaussian Filter  |
| PP4           | Sobel Filter     |
| PP5           | Laplacian Filter |

The resulting datasets are stored independently to ensure complete experimental reproducibility and facilitate direct comparison between preprocessing approaches.

---

## Segmentation Stage

The segmentation stage is responsible for model training, validation and inference.

For each preprocessing configuration, the segmentation model is trained independently, generating:

* Trained model weights (`.pth`);
* Training and validation loss curves;
* Predicted segmentation masks.

This experimental design enables a controlled evaluation of the influence of image preprocessing on segmentation performance.

---

## Evaluation Stage

The evaluation stage performs quantitative analysis of segmentation quality using standard segmentation metrics.

Performance is assessed both before and after morphological post-processing, enabling the study of the impact of mathematical morphology on segmentation refinement.

The evaluated post-processing operations include:

* Erosion
* Dilation
* Opening
* Closing

Performance comparisons are generated automatically and exported as structured result tables for subsequent analysis.

---

## Experimental Objective

The primary objective of the pipeline is to determine how different preprocessing strategies and morphological post-processing operations influence segmentation performance in fetal ultrasound images.

The study focuses on identifying:

* The preprocessing strategy that produces the most informative image representation;
* The post-processing operation that provides the greatest segmentation refinement;
* The combination that yields the highest overall segmentation accuracy.

---

## Reproducibility

The workflow was designed to ensure experimental reproducibility through:

* Independent execution of each processing stage;
* Explicit separation between input data, trained models and generated results;
* Consistent dataset organisation;
* Automated metric computation and result aggregation.

This structure facilitates experimental replication, result verification and future extension of the pipeline.

---

## Related Documentation

* `../02_dataset/README.md`
* `../06_documentation/portal/implementation.md`
* `../05_report/results.md`
