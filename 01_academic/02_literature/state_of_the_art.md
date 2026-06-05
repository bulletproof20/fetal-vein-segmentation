# State of the Art

Formal literature review supporting the fetal umbilical vein segmentation project. Sources include peer-reviewed publications indexed in [Articles.md](Articles.md), the University of Porto anatomical reference [PTG_Cord_Umb_UPorto.pdf](PTG_Cord_Umb_UPorto.pdf), and course materials on image processing, deep learning, and mathematical morphology.

---

## Introduction

Fetal ultrasound is a primary modality for monitoring intrauterine development. It is non-invasive, widely available, and suitable for repeated acquisition during pregnancy. However, ultrasound images are characterised by speckle noise, attenuation, shadowing, and operator-dependent acquisition variability. These factors complicate both visual interpretation and automated analysis.

Vessel segmentation in fetal ultrasound addresses a clinically relevant problem: delineating vascular structures that support diagnosis, biometric assessment, and the study of fetal circulation. Automation reduces inter-observer variability and enables reproducible quantitative measures when paired with validated ground-truth annotations.

The present work focuses on semantic segmentation of the fetal umbilical vein using deep learning, preceded by classical preprocessing and followed by morphological post-processing. This chapter contextualises that pipeline within established literature on fetal vascular imaging, ultrasound preprocessing, convolutional segmentation architectures, and mathematical morphology.

---

## Fetal Vessel Segmentation

### Umbilical and portal venous anatomy

The fetal umbilical-portal venous system connects placental circulation to the fetal liver. Understanding this anatomy is prerequisite to meaningful segmentation and evaluation.

Mavrides *et al.* (2001) describe the anatomy of the umbilical, portal, and hepatic venous systems in human fetuses at 14–19 weeks of gestation using ultrasound, establishing reference spatial relationships between vessels that inform image interpretation and label semantics. Kivilevitch *et al.* (2009) extend this with two- and three-dimensional ultrasonic evaluation of the fetal umbilical-portal venous system *in utero*, demonstrating that detailed vascular assessment is feasible with standard clinical ultrasound platforms.

The University of Porto document [PTG_Cord_Umb_UPorto.pdf](PTG_Cord_Umb_UPorto.pdf) complements these publications by consolidating anatomical identification criteria and visual patterns relevant to umbilical cord vein studies in the project dataset context.

### Clinical motivation

Accurate delineation of fetal vessels supports:

- Visualisation and measurement of vascular morphology;
- Consistency across operators and acquisition sessions;
- Quantitative comparison of segmentation algorithms against expert annotations.

Segmentation errors—false positives from speckle artefacts or false negatives from low contrast—directly affect downstream metrics such as Dice coefficient, precision, and recall used in this project.

---

## Ultrasound Image Preprocessing

Classical preprocessing aims to improve the signal-to-noise ratio and stabilise intensity distributions before higher-level analysis. In spatial-domain processing, linear and non-linear filters are commonly applied.

| Approach | Principle | Relevance to this project |
|----------|-----------|---------------------------|
| **Average filter** | Local mean smoothing | Reduces speckle; may blur thin structures (PP1) |
| **Median filter** | Order-statistic smoothing | Preserves edges better than mean; robust to outliers (PP2) |
| **Gaussian filter** | Weighted local averaging | Controlled smoothing; widely used pre-segmentation (PP3) |
| **Sobel operator** | Gradient magnitude | Emphasises edges; alters intensity appearance (PP4) |
| **Laplacian operator** | Second-order derivative | Highlights high-frequency detail (PP5) |

Point operations—brightness/contrast adjustment, gamma correction, histogram equalisation—modify grey-level mapping without changing spatial geometry. The preprocessing notebook implements optional global transforms (brightness, contrast, gamma) prior to a single spatial filter per pipeline, enabling controlled comparison of filtering strategies while holding downstream training protocol constant.

Speckle is multiplicative noise inherent to coherent ultrasound imaging. Filtering trades noise suppression against preservation of anatomical boundaries required for vein segmentation. The experimental design in `01_preprocessing.ipynb` therefore treats preprocessing as an explicit scientific variable rather than an undocumented heuristic.

---

## Deep Learning for Medical Image Segmentation

### From CNNs to encoder–decoder architectures

Convolutional neural networks learn hierarchical feature representations from labelled data. For dense prediction tasks, fully convolutional architectures output pixel-wise class maps aligned with input images.

Encoder–decoder networks compress spatial context in a bottleneck and recover resolution through upsampling or transpose convolutions, combining semantic abstraction with local localisation—essential for organ and vessel segmentation.

### U-Net

Ronneberger *et al.* introduced U-Net as an encoder–decoder architecture with skip connections preserving fine spatial detail. It remains a standard baseline in biomedical segmentation because of its balance between complexity, training stability, and performance on limited datasets.

### MONAI and project implementation

The Medical Open Network for AI (MONAI) provides PyTorch implementations of medical imaging networks, transforms, losses, and metrics. The project segmentation stage adopts a **2D U-Net** via MONAI with:

- Identical training protocol across Original and PP1–PP5 datasets;
- Dice loss and validation-driven checkpoint selection;
- Paired image–label loading with identifier-based pairing.

The lecturer reference notebook `FetalVeinSegmentationUS.ipynb` defines the core training workflow adapted in `02_segmentation.ipynb`. Architectural and optimisation choices are held constant so that observed performance differences are attributable primarily to preprocessing and post-processing rather than ad hoc training changes.

---

## Mathematical Morphology

Mathematical morphology analyses binary or grey-scale images using structuring elements. For binary masks **A** and structuring element **B**:

| Operation | Definition | Effect on segmentation masks |
|-----------|------------|------------------------------|
| **Erosion** | \(A \ominus B\) | Shrinks foreground; removes thin protrusions |
| **Dilation** | \(A \oplus B\) | Expands foreground; bridges small gaps |
| **Opening** | \(A \circ B = (A \ominus B) \oplus B\) | Removes small artefacts |
| **Closing** | \(A \bullet B = (A \oplus B) \ominus B\) | Fills small holes |

In this project, post-segmentation morphology is evaluated as a **refinement step** applied to predicted masks before metric computation. The evaluation notebook selects one operator per run (`POSTPROCESS_METHOD`) and compares **without** versus **with** post-processing (`No` / `Yes` rows in the results table), exporting method-specific CSV files for cross-run comparison.

Opening and closing are implemented as explicit compositions of erosion and dilation, reflecting standard course definitions (see course material: *Mathematical morphology*).

---

## Comparative Review

| Theme | Representative approaches | Reported limitations |
|-------|-------------------------|----------------------|
| Ultrasound preprocessing | Mean, median, Gaussian smoothing; histogram methods | Over-smoothing removes thin vessels; gradient-based filters alter appearance |
| Deep segmentation | U-Net, FCN variants, MONAI pipelines | Requires labelled data; sensitive to domain shift |
| Post-processing | Morphological opening/closing; connected-component analysis | Operator/kernel selection affects precision–recall trade-off |
| Evaluation | Dice, precision, recall on hold-out test masks | Metrics alone do not capture clinical acceptability |

The project adopts a **controlled factorial-style comparison**: six preprocessing inputs (Original + PP1–PP5) × morphological post-processing strategies evaluated in separate evaluation runs, with consistent metrics and pairing rules throughout.

---

## Research Challenges

Several challenges remain active in fetal ultrasound segmentation:

1. **Intensity variability** — Gain settings, shadowing, and fetal position alter appearance across acquisitions.
2. **Speckle and noise** — Classical and learned methods must suppress noise without erasing thin venous structures.
3. **Limited annotated data** — Educational subsets constrain model capacity and generalisation analysis.
4. **Robustness** — Models trained on one preprocessing distribution may not transfer without retraining.
5. **Evaluation scope** — Pixel-wise metrics do not fully encode clinical utility; they nevertheless provide reproducible comparison across experiments.

These challenges motivate the project's emphasis on transparent preprocessing variants, fixed training protocol, and systematic post-processing evaluation.

---

## Relation to the Present Work

The implemented pipeline operationalises the literature review as follows:

| Literature theme | Project artefact |
|------------------|------------------|
| Fetal venous anatomy | Label semantics and pairing in `02_dataset/labels/` |
| Spatial preprocessing | `01_preprocessing.ipynb` — PP1–PP5 |
| U-Net / MONAI segmentation | `02_segmentation.ipynb` |
| Morphological refinement | `03_evaluation.ipynb` — configurable `POSTPROCESS_METHOD` |
| Quantitative comparison | `04_pipeline_results/tabela_avaliacao_experiencias_*.csv` |
| Synthesis | [Results](../../05_report/results.md) and [final report PDF](../../05_report/a22588_a22604.pdf) |

Empirical findings (see [Results](../portal/results.md)) indicate that **Gaussian preprocessing (PP3)** combined with **opening** post-processing achieved the highest Dice score in the conducted experiments, while gradient-emphasising filters (Sobel, Laplacian) degraded segmentation quality—consistent with the expectation that vein segmentation benefits from preserved intensity information rather than edge-only representations.

---

## References

See [Articles.md](Articles.md) for bibliographic entries (Kivilevitch *et al.*, 2009; Mavrides *et al.*, 2001) and the Porto anatomical supplement. Dataset licensing and attribution are documented in [LICENSE.md](../03_dataset_documentation/LICENSE.md).
