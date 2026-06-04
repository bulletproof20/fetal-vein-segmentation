# Project governance

**Version:** 6.0  
**Status:** normative  
**Scope:** entire repository except protected directories (`01_academic/`, `02_dataset/`)

This page is the **governance index**. All refactoring must comply with the documents below **before** any notebook or code changes.

---

## Governance documents

### Core standards

| Document | Responsibility |
|----------|----------------|
| [coding_standards.md](coding_standards.md) | Python style, paths, data integrity, scientific constraints |
| [naming_conventions.md](naming_conventions.md) | Syntax: `snake_case`, constants, forbidden generic names |
| [semantic_naming_policy.md](semantic_naming_policy.md) | **Meaning**: masks, images, datasets, paths |
| [lecturer_identifier_policy.md](lecturer_identifier_policy.md) | Preserved names; **refactor protection rule** |
| [comment_standards.md](comment_standards.md) | Comment intent and docstrings |

### Notebook and documentation

| Document | Responsibility |
|----------|----------------|
| [scientific_notebook_standards.md](scientific_notebook_standards.md) | **Taxonomy**: Categories A–D and required structure |
| [notebook_standards.md](notebook_standards.md) | Language, tone, configuration cell format |
| [documentation_standards.md](documentation_standards.md) | Markdown vs notebooks; MkDocs; single source of truth |

---

## Decision order (refactor conflicts)

When policies appear to conflict, apply this order:

1. [coding_standards.md](coding_standards.md) §9 — scientific behaviour unchanged  
2. [lecturer_identifier_policy.md](lecturer_identifier_policy.md) — do not rename preserved identifiers without justification  
3. [semantic_naming_policy.md](semantic_naming_policy.md) — disambiguate masks, images, data  
4. [naming_conventions.md](naming_conventions.md) — English verb-led function names  
5. [scientific_notebook_standards.md](scientific_notebook_standards.md) — notebook category structure  

---

## Protected directories (read-only)

| Directory | Rule |
|-----------|------|
| `01_academic/` | No edits, renames, translations, or moves |
| `02_dataset/` | No edits to data, README, or structure |

---

## Execution model (reference)

```text
GitHub Repository → Google Colab → 02_dataset → 03_pipeline → 04_pipeline_results → 05_report
```

---

## Approval workflow

| Phase | Activity | Code changes |
|-------|----------|--------------|
| 1–2 | Governance + audit | Documentation only |
| 3 | Refactor implementation | After explicit approval |

Do not rename functions, variables, or notebook sections until Phase 3 is approved.

---

## Related architecture pages

- [System architecture](../02_architecture/system_architecture.md)
- [Implementation index](../portal/implementation.md)
- [Design decisions](../02_architecture/design_evolution.md)
