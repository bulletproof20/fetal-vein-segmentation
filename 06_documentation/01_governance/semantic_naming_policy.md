# Semantic naming policy

**Version:** 6.0  
**Status:** normative  
**Scope:** all project-authored identifiers outside `01_academic/` and `02_dataset/`

This document defines **meaning**, not only **style**. Syntax rules live in [naming_conventions.md](naming_conventions.md).

**Translation alone is insufficient.** Renaming `mascara` to `mask` does not comply. The name must state role, origin, and usage context.

---

## 1. Core principle

Every variable and parameter name must answer:

1. **What** does this object represent?
2. **Where** did it come from (input, model, file, stage)?
3. **How** is it used in this cell or function?

The objective is **self-documenting** notebook code without reading surrounding cells.

---

## 2. Mask semantics

The bare name `mask` is **non-compliant** when multiple masks appear in the same scope.

| Context | Required naming (examples) |
|---------|----------------------------|
| Model output before post-processing | `prediction_mask` |
| Ground truth from `labels/` | `ground_truth_mask` |
| After thresholding / binarisation step | `binary_mask` |
| After `pos_process()` | `post_processed_mask` |
| Largest connected component step | `largest_component_mask` |
| Input to metric function | `prediction_mask`, `ground_truth_mask` (pair explicitly) |

### Bad → good

```python
# Bad
mask = load_mask_png(path)
gt = load_mask_png(label_path)

# Good
prediction_mask = load_mask_png(prediction_path)
ground_truth_mask = load_mask_png(label_path)
```

---

## 3. Image semantics

The bare name `image` or `img` is **non-compliant** for general use.

| Context | Required naming (examples) |
|---------|----------------------------|
| Raw file load | `input_image` |
| After grayscale conversion | `grayscale_image` |
| After global operations | `processed_image` |
| After spatial filter | `filtered_image` |
| Display buffer | `display_image` or `visualisation_image` |

### Bad → good

```python
# Bad
def convert_to_grayscale(img):
    ...

# Good
def convert_to_grayscale(input_image):
    ...
```

---

## 4. Dataset and file-collection semantics

| Bad | Good | Meaning |
|-----|------|---------|
| `data` | `training_dataset` | MONAI dataset for training |
| `data` | `validation_dataset` | Validation split |
| `data` | `evaluation_dataset` | Evaluation split |
| `files` | `training_file_list` | List of dict paths |
| `pares` | `image_label_pairs` | Paired paths |

---

## 5. Path and directory semantics

| Bad | Good |
|-----|------|
| `path` | `image_path`, `label_path`, `prediction_path` |
| `pasta` | `results_folder`, `images_folder` |
| `caminho` | `file_path`, `output_csv_path` |
| `dir` | `labels_directory`, `project_root` |

---

## 6. Metric and scalar semantics

| Bad | Good |
|-----|------|
| `res` | `dice_score`, `evaluation_results` |
| `hist` | `histogram_values`, `gray_level_histogram` |
| `ac`, `pr`, `re` | Allowed **only** as short unpack names inside `calculate_metrics()` aligned with lecturer code; document in docstring |
| `lista` | `metric_tuples`, `batch_metric_list` |

---

## 7. Tensor and batch semantics (segmentation)

| Context | Examples |
|---------|----------|
| Single batch from loader | `batch_dict`, `batch_images`, `batch_labels` |
| Model output tensor | `prediction_logits`, `prediction_tensor` |
| Decollated sample | `prediction_sample`, `label_sample` |

Do not use `x`, `y`, `out` for tensors unless in a documented one-line scope with comment.

---

## 8. Preprocessing-specific semantics

| Context | Examples |
|---------|----------|
| Convolution input | `input_image` (uint8 grayscale) |
| Kernel | `filter_kernel`, `gaussian_kernel` |
| Padded array | `padded_image` |
| Loop indices | `row_index`, `column_index` (preferred over `i`, `j`) |
| Channel planes | `red_channel`, `green_channel`, `blue_channel` |

---

## 9. When bare short names are tolerated

| Name | Condition |
|------|-----------|
| `gt` | Parameter in `calculate_metrics(predicted, gt)` — lecturer-aligned; see [lecturer_identifier_policy.md](lecturer_identifier_policy.md) |
| `pred` | Only inside metric function body with comment |
| `tp`, `tn`, `fp`, `fn` | Confusion matrix locals in `calculate_metrics()` |

All other bare names (`mask`, `img`, `data`, `path`) require semantic replacement during Phase 3.

---

## 10. Refactor guidance

Phase 3 renames must apply **semantic upgrades**, not literal translation:

| Non-compliant | Wrong refactor | Correct refactor |
|---------------|----------------|------------------|
| `mascara` | `mask` | `prediction_mask` or `binary_mask` (by stage) |
| `imagem_cinza` | `image` | `grayscale_image` |
| `previsao` | `pred` | `prediction_array` or `prediction_mask` |
| `dados` | `data` | `training_dataset` or `image_label_pairs` |

---

## 11. Related documents

- [naming_conventions.md](naming_conventions.md)
- [lecturer_identifier_policy.md](lecturer_identifier_policy.md)
- [comment_standards.md](comment_standards.md)
