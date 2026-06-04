# Notebook standards

**Version:** 6.0  
**Status:** normative  
**Scope:** all notebooks under `03_pipeline/` (and project templates)

**Authoritative taxonomy:** [scientific_notebook_standards.md](scientific_notebook_standards.md) (Categories A–D). This document covers language, tone, and shared formatting.

---

## 1. Language and tone

| Element | Requirement |
|---------|-------------|
| Markdown cells | English, academic tone |
| Code comments | English; see [comment_standards.md](comment_standards.md) |
| Print output | English |
| Identifiers | English `snake_case`; see [naming_conventions.md](naming_conventions.md) |

---

## 2. Required header (all notebooks)

First markdown cell must include:

1. Title (`# …`)
2. `**Type:**` — `library notebook` or `execution notebook` (or entry-point guidance for `entrypoint.ipynb`)
3. Short purpose (2–4 sentences)
4. For execution notebooks: inputs, outputs, and runtime (`Google Colab`)

---

## 3. Notebook categories and structure

See [scientific_notebook_standards.md](scientific_notebook_standards.md) for normative section lists:

| Category | Structure summary |
|----------|-------------------|
| **A — Library** | Purpose → Dependencies → Function definitions → Usage notes |
| **B — Execution** | Purpose → Imports → Configuration → Processing → Validation → Outputs → Conclusions |
| **C — Orchestration** | Repository context → Execution order → Configuration matrix → Expected outputs |
| **D — Research** | Reserved (Hypothesis → Methodology → Experiment → Results → Discussion) |

Phase 3 aligns headings; scientific behaviour unchanged.

---

## 5. Configuration cell format

```python
# ==========================================================
# EXPERIMENT CONFIGURATION — [STAGE NAME]
# ==========================================================

EXPERIMENT_ID = 1
DATASET_FOLDER = "images_pp_1"
```

- All tunable parameters in one place at the top of execution notebooks.
- Use `UPPER_SNAKE_CASE` for configuration constants.

---

## 6. `%run` discipline

| Rule | Detail |
|------|--------|
| Order | Load library notebooks before calling their functions |
| Paths | Relative to calling notebook (e.g. `%run ../00_common/00_generic.ipynb`) |
| Side effects | Library load should not train models or overwrite results |

---

## 7. Visualisation

- Use clear figure titles and axis labels (English).
- Prefer helper `display_images_side_by_side()` for comparisons.
- State colour map and normalisation in markdown when non-obvious.

---

## 8. What notebooks must not contain

- Long architecture essays (link to MkDocs)
- Portuguese prose
- Docker / local server setup as primary instructions
- Copy-pasted governance text

---

## 9. Template

See [scientific_notebook_standards.md](scientific_notebook_standards.md).

---

## 10. Related documents

- [coding_standards.md](coding_standards.md)
- [documentation_standards.md](documentation_standards.md)
- [../portal/implementation.md](../portal/implementation.md)
