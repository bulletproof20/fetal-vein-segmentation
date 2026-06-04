# Notebook standards

**Version:** 7.0  
**Status:** normative  
**Scope:** all notebooks under `03_pipeline/`

**Authoritative structure:** [scientific_notebook_standards.md](scientific_notebook_standards.md). This document covers language, tone, and shared formatting.

---

## 1. Language and tone

| Element | Requirement |
|---------|-------------|
| Markdown cells | English, academic tone |
| Code comments | English; see [comment_standards.md](comment_standards.md) |
| Print output | English |
| Identifiers | English `snake_case`; see [naming_conventions.md](naming_conventions.md) |

---

## 2. Required header (pipeline notebooks)

First markdown cell must include:

1. Title (`# …`)
2. `**Type:**` — `execution notebook (self-contained; no %run of other pipeline notebooks).`
3. Short purpose (2–4 sentences)
4. Inputs, outputs, and runtime (`Google Colab`)

---

## 3. Section layout

See [scientific_notebook_standards.md](scientific_notebook_standards.md):

| Block | Summary |
|-------|---------|
| Purpose | Goal, inputs, outputs |
| Dependencies | One consolidated import cell |
| Configuration | Labelled experiment constants |
| Stage sections | Processing logic (preserved internal headings) |
| Validation / Outputs / Conclusions | As applicable per stage |

---

## 4. Self-contained execution

| Rule | Detail |
|------|--------|
| Cross-notebook `%run` | **Forbidden** between `01_`, `02_`, `03_` pipeline notebooks |
| Dependencies | All imports for a stage in that notebook’s **Dependencies** cell |
| Execution order | Documented in `03_pipeline/README.md`, not in a fourth notebook |
| Side effects | Running a notebook must not require another pipeline notebook to have been `%run` |

---

## 5. Configuration cell format

```python
# ==========================================================
# EXPERIMENT CONFIGURATION — [STAGE NAME]
# ==========================================================

EXPERIMENT_ID = 1
DATASET_FOLDER = "images_pp_1"
```

- All tunable parameters in one place at the top of the execution section for that stage.
- Use `UPPER_SNAKE_CASE` for configuration constants.

---

## 6. Visualisation

- Use clear figure titles and axis labels (English).
- Prefer helper `display_images_side_by_side()` for comparisons.
- State colour map and normalisation in markdown when non-obvious.

---

## 7. What notebooks must not contain

- Long architecture essays (link to MkDocs)
- Portuguese prose
- Docker / local server setup as primary instructions
- Copy-pasted governance text
- `%run` paths to other pipeline notebooks

---

## 8. Related documents

- [scientific_notebook_standards.md](scientific_notebook_standards.md)
- [coding_standards.md](coding_standards.md)
- [documentation_standards.md](documentation_standards.md)
- [../portal/implementation.md](../portal/implementation.md)
