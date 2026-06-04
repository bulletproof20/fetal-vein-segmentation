# Naming conventions

**Version:** 6.0  
**Status:** normative  
**Scope:** repository-wide (except `01_academic/`, `02_dataset/`)

**Semantic meaning** (what to name things): [semantic_naming_policy.md](semantic_naming_policy.md)  
**Preserved lecturer names**: [lecturer_identifier_policy.md](lecturer_identifier_policy.md)

---

## 1. General rules

| Element | Convention | Example |
|---------|------------|---------|
| Directories | `snake_case` | `02_dataset`, `images_pp_1` |
| Notebook files | `snake_case` | `fetal_vein_segmentation.ipynb` |
| Python modules | `snake_case` | N/A (notebook-based project) |
| Functions | `snake_case`, English, verb-led | `apply_gaussian_filter()` |
| Variables | `snake_case`, English, descriptive | `input_image` |
| Parameters | `snake_case`, English, descriptive | `ground_truth_mask` |
| Constants | `UPPER_SNAKE_CASE` | `IMAGE_EXTENSIONS` |
| Classes | `PascalCase` (if used) | `CustomTransform` |

---

## 2. Function names

Functions must describe **one clear responsibility**. Use verb + object.

### Mandatory patterns

```python
apply_gaussian_filter()
compute_dice_score()
build_data_dicts()
resolve_label_path()
find_project_root()
load_mask_png()
validate_pairing_folder()
```

### Forbidden patterns

Generic or ambiguous names:

```python
process()      # forbidden
helper()       # forbidden
calculate()    # forbidden — too vague; use compute_dice_score(), etc.
aux()          # forbidden
handle()       # forbidden
run()          # forbidden (except framework)
do_filter()    # forbidden — specify which filter
```

### Prefix guidance

| Prefix | Use for |
|--------|---------|
| `apply_` | Image transforms and filters |
| `compute_` / `calculate_` | Metrics and numeric results (`calculate_metrics` retained when matching lecturer API) |
| `build_` | Data structures and dictionaries |
| `load_` / `save_` | I/O |
| `validate_` | Checks and assertions |
| `resolve_` | Path or ID resolution |
| `convert_` / `ensure_` | Representation changes |
| `list_` | Enumerations |
| `print_` | Display-only diagnostics |
| `create_` | UI or factory helpers |

### Language-specific names

Portuguese function names (e.g. `filtro_gaussian`, `aplicar_operacoes_globais`) are **non-compliant** and must be renamed in Phase 3.

### Lecturer-aligned names

See [lecturer_identifier_policy.md](lecturer_identifier_policy.md) for the normative preserved list (`pos_process`, `calculate_metrics`, framework APIs). Do not rename without justification under the refactor protection rule.

---

## 3. Variable names

Variables must state **what is stored**.

### Mandatory examples

```python
input_image
processed_image
prediction_mask
ground_truth_mask
contrast_factor
brightness_offset
project_root
results_folder
original_identifier
```

### Forbidden examples

```python
img          # forbidden — use input_image, grayscale_image, etc.
img2         # forbidden
tmp          # forbidden
data         # forbidden
var          # forbidden
res          # forbidden
hist         # forbidden — use histogram_values
x, y, z      # forbidden as generic data holders
```

### Documented exceptions

See [lecturer_identifier_policy.md](lecturer_identifier_policy.md) §4. Bare `mask`, `img`, and `data` are **not** exceptions — use [semantic_naming_policy.md](semantic_naming_policy.md).

---

## 4. Parameter names

Parameters follow the same rules as variables.

### Good

```python
def apply_brightness_contrast(input_image, contrast_factor, brightness_offset):
    ...

def resolve_label_path(prediction_file_name, labels_dir: Path):
    ...
```

### Bad

```python
def apply_brightness_contrast(img, alpha, b):  # non-compliant unless alpha/b documented as lecturer notation
def load_image(path):                          # use file_path or image_path
def binarize_mask(mask, threshold):            # use prediction_mask or input_mask
```

---

## 5. Constants

Configuration and module-level fixed values use `UPPER_SNAKE_CASE`.

```python
IMAGE_EXTENSIONS = {".png", ".jpg", ...}
EXPECTED_MODEL_FILES = [...]
DATASET_FOLDER = "images_pp_1"
APPLY_ORIENTATION_CORRECTION = True
DEFAULT_THRESHOLD = 127.0
```

Experiment configuration cells may use `SCREAMING_SNAKE_CASE` for tunable parameters.

---

## 6. Single-letter variables

### Default rule

**Avoid** single-letter names except documented cases below.

### Allowed categories

| Category | Example | Requirement |
|----------|---------|-------------|
| Loop index (discouraged) | `for row_index in range(height):` | Prefer descriptive index names |
| Matrix notation | `kernel[row_index, column_index]` | Comment if `i`, `j` used |
| Lecturer metric tuple | `dice, ac, pr, re` | Local unpacking only; short scope |

### If `i` / `j` are kept (e.g. convolution loops)

```python
for row_index in range(image_height):      # preferred
    for column_index in range(image_width):
        ...

# If retained for performance/clarity in tight loops:
for i in range(image_height):  # row_index — image row
    for j in range(image_width):  # column_index — image column
```

### Forbidden without comment

```python
for i in range(10):   # non-compliant if meaning is not documented
    ...
```

---

## 7. Repository layout names

| Directory | Purpose |
|-----------|---------|
| `01_academic/` | Lecturer materials (immutable) |
| `02_dataset/` | Data artefacts (immutable) |
| `03_pipeline/` | Scientific notebooks |
| `04_pipeline_results/` | Evaluation tables |
| `05_report/` | Written deliverable template |
| `06_documentation/` | Governance and architecture (MkDocs) |
| `99_system/` | Design history |

### Dataset file patterns

| Pattern | Meaning |
|---------|---------|
| `P080_IMG1.png` | Original image or label stem |
| `P080_IMG1_PP_PL_1.png` | Preprocessed (pipeline 1) |
| `best_metric_model_pp_3.pth` | Checkpoint for PP3 |
| `results_pp_2/` | Segmentation outputs for PP2 |

---

## 8. Related documents

- [coding_standards.md](coding_standards.md)
- [notebook_standards.md](notebook_standards.md)
- [../02_architecture/system_architecture.md](../02_architecture/system_architecture.md)
