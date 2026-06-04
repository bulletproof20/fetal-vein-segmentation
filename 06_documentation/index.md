# Fetal Vein Segmentation — Documentation

**Version:** 4.0  
**Scope:** normative architecture and governance (MkDocs site)

This site defines **rules, relationships, and design rationale**. It does not restate implementation detail, execution steps, or dataset contracts documented elsewhere.

---

## Authoritative sources

| Topic | Location |
|-------|----------|
| Repository overview and quick start | [`README.md`](../README.md) (repository root) |
| Execution workflow | [`03_pipeline/entrypoint.ipynb`](../03_pipeline/entrypoint.ipynb) |
| Pipeline folder index | [`03_pipeline/README.md`](../03_pipeline/README.md) |
| Dataset layout and pairing contract | [`02_dataset/README.md`](../02_dataset/README.md) |
| Algorithms, parameters, experiments | Notebooks under [`03_pipeline/`](../03_pipeline/) |
| Scientific dependencies | [`requirements.txt`](../requirements.txt) |
| Governance (standards) | [`01_governance/project_governance.md`](01_governance/project_governance.md) |
| Architectural rationale | [`02_architecture/`](02_architecture/) |

---

## This site contains

| Section | Responsibility |
|---------|----------------|
| [Governance](01_governance/project_governance.md) | Naming, notebooks, coding, documentation policy |
| [System architecture](02_architecture/system_architecture.md) | Component relationships and design principles |
| [Data flow](02_architecture/data_flow.md) | Artefact movement and integrity rules |
| [Design evolution](02_architecture/design_evolution.md) | Why the repository is notebook-centric |
| [MkDocs publishing](MKDOCS_PUBLISHING.md) | Build and deploy this site |

---

## Publishing

```bash
pip install -r requirements-mkdocs.txt
mkdocs build
```

See [MKDOCS_PUBLISHING.md](MKDOCS_PUBLISHING.md).
