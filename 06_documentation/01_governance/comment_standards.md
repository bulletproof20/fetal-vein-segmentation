# Comment standards

**Version:** 5.0  
**Status:** normative  
**Scope:** all project-authored code in `03_pipeline/` and future project Python

Part of [coding_standards.md](coding_standards.md).

---

## 1. Purpose

Comments explain **intent**, **assumptions**, and **non-obvious decisions**. They must not repeat what the code already states.

---

## 2. Language

- **English only** (same policy as code).
- No Portuguese in comments or block headers.

---

## 3. Good comments

Explain why or provide context:

```python
# Apply contrast using a linear intensity transform (lecturer worksheet convention).
adjusted_image = apply_brightness_contrast(input_image, contrast_factor, brightness_offset)

# row_index — iterate over image rows for manual convolution
for row_index in range(image_height):
    ...

# Keep lecturer metric names (tp, tn, fp, fn) for confusion-matrix clarity.
```

---

## 4. Bad comments

| Bad | Why |
|-----|-----|
| `# Contrast` | Labels the line without explaining |
| `# Apply contrast` | Repeats the function name |
| `# Loop` | Obvious from syntax |
| `# Fix` | No diagnostic value |
| `# TODO` without issue context | Incomplete |

---

## 5. Block headers

Large notebooks may use section banners:

```python
# ==========================================================
# GLOBAL OPERATIONS — BRIGHTNESS AND CONTRAST
# ==========================================================
```

- English only.
- Describe the **section topic**, not a single vague word.

---

## 6. Docstrings (library functions)

Required on public functions in library notebooks:

```python
def resolve_label_path(prediction_file_name: str, labels_dir: Path = LABELS_DIR) -> Path:
    """Map a prediction filename to the ground-truth label path.

    Strips preprocessing suffix _PP_PL_N when present.

    Args:
        prediction_file_name: Prediction or image filename.
        labels_dir: Directory containing label masks.

    Returns:
        Path to the matching label file.

    Raises:
        FileNotFoundError: If no label exists for the original identifier.
        ValueError: If the filename does not match expected patterns.
    """
```

---

## 7. Exception and print messages

User-facing strings must be English and actionable:

```python
raise FileNotFoundError(
    f"Directory 02_dataset/ not found from {start_path}. "
    "Set the working directory to the repository root."
)
```

---

## 8. When not to comment

- Self-explanatory MONAI transform chains (prefer markdown in notebook above the cell).
- Standard `import` lines.
- Variable assignments that already use descriptive names.

---

## 9. Related documents

- [coding_standards.md](coding_standards.md)
- [naming_conventions.md](naming_conventions.md)
