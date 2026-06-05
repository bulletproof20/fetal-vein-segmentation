# Results

Quantitative and qualitative outcomes of model training, segmentation evaluation, and morphological post-processing.

Extended narrative (repository): [05_report/results.md](https://github.com/bulletproof20/fetal-vein-segmentation/blob/main/05_report/results.md)

Evaluation tables (`04_pipeline_results/`, one CSV per morphology method):

| Method | CSV |
|--------|-----|
| Opening | [tabela_avaliacao_experiencias_opening.csv](https://github.com/bulletproof20/fetal-vein-segmentation/blob/main/04_pipeline_results/tabela_avaliacao_experiencias_opening.csv) |
| Closing | [tabela_avaliacao_experiencias_closing.csv](https://github.com/bulletproof20/fetal-vein-segmentation/blob/main/04_pipeline_results/tabela_avaliacao_experiencias_closing.csv) |
| Erosion | [tabela_avaliacao_experiencias_erosion.csv](https://github.com/bulletproof20/fetal-vein-segmentation/blob/main/04_pipeline_results/tabela_avaliacao_experiencias_erosion.csv) |
| Dilation | [tabela_avaliacao_experiencias_dilation.csv](https://github.com/bulletproof20/fetal-vein-segmentation/blob/main/04_pipeline_results/tabela_avaliacao_experiencias_dilation.csv) |

---

## Training analysis

Training and validation loss curves (`04_pipeline_results/Segmentation_training_results/`):

### Original dataset

![Original training curves](https://github.com/bulletproof20/fetal-vein-segmentation/raw/main/04_pipeline_results/Segmentation_training_results/original.png)

### PP1 — Average filter

![PP1 training curves](https://github.com/bulletproof20/fetal-vein-segmentation/raw/main/04_pipeline_results/Segmentation_training_results/test1.png)

### PP2 — Median filter

![PP2 training curves](https://github.com/bulletproof20/fetal-vein-segmentation/raw/main/04_pipeline_results/Segmentation_training_results/test2.png)

### PP3 — Gaussian filter

![PP3 training curves](https://github.com/bulletproof20/fetal-vein-segmentation/raw/main/04_pipeline_results/Segmentation_training_results/test3.png)

### PP4 — Sobel filter

![PP4 training curves](https://github.com/bulletproof20/fetal-vein-segmentation/raw/main/04_pipeline_results/Segmentation_training_results/test4.png)

### PP5 — Laplacian filter

![PP5 training curves](https://github.com/bulletproof20/fetal-vein-segmentation/raw/main/04_pipeline_results/Segmentation_training_results/test5.png)

Gaussian preprocessing (PP3) yielded the most favourable validation behaviour and segmentation metrics.

---

## Morphological post-processing

Four operators were evaluated in separate notebook runs (`POSTPROCESS_METHOD`): erosion, dilation, opening, and closing. Each run produces a **No / Yes** comparison table (12 rows: 6 experiments × 2).

**Best overall result:** PP3 + Opening — **Dice 0.5015**

---

## Comparative summary

| Configuration | Best operation | Best Dice |
|---------------|----------------|-----------|
| Original | Closing | 0.4720 |
| PP1 (Average) | None | 0.4745 |
| PP2 (Median) | Closing | 0.4444 |
| PP3 (Gaussian) | Opening | **0.5015** |
| PP4 (Sobel) | Opening | 0.3426 |
| PP5 (Laplacian) | Dilation | 0.1135 |

---

## Conclusions

Gaussian filtering provided the strongest preprocessing input. **Opening** achieved the highest Dice score. **Recommended pipeline:** Gaussian preprocessing → UNet segmentation → opening post-processing.

[Final Report](final_report.md)

---

## Related documentation

| Section | Description |
|---------|-------------|
| [State of the Art](state_of_the_art.md) | Literature review and clinical context |
| [Dataset overview](dataset.md) | Data used for training and evaluation |
| [Scientific Pipeline](pipeline.md) | Experimental workflow |
| [Final Report](final_report.md) | Submitted written deliverable |
