# Mapa de Migração — Nomenclatura

**Versão:** 2.0  
**Fase:** Consolidação arquitetural — **aplicada** (2026-05-29)  
**Legenda:** `RENAME` | `KEEP` | `MOVE` | `CREATE` | `DELETE` | `OPTIONAL`

> **Nota:** `10_runtime` / `10_docker` deixaram de existir como pastas de topo. Runtime → `99_system/01_runtime/`; bootstrap → `99_system/02_bootstrap/`. Ver `architecture_consolidation_report.md`.

---

## A. Diretórios (raiz)

| # | Atual | Destino | Operação |
|---|-------|---------|----------|
| A1 | `00-common` | `00_common` | RENAME |
| A2 | `01-literature-review` | `01_literature_review` | RENAME |
| A3 | `02-dataset` | `02_dataset` | RENAME |
| A4 | `03-preprocessing` | `03_preprocessing` | RENAME |
| A5 | `04-segmentation` | `04_segmentation` | RENAME |
| A6 | `05-postprocessing` | `05_postprocessing` | RENAME |
| A7 | `06-evaluation` | `06_evaluation` | RENAME |
| A8 | `07-results` | `07_results` | RENAME |
| A9 | — | `08_report` | CREATE |
| A10 | — | `09_presentation` | CREATE |
| A11 | — | `00_project` | CREATE (opcional) |
| A12 | `10-runtime` | `99_system/01_runtime` | MOVE |
| A13 | `10-docker` | `99_system/01_runtime/docker` | MOVE |
| A14 | `scripts` | `99_system/03_tools` | MOVE |
| A15 | `99_system` | `99_system` | KEEP |

---

## B. Diretórios (subpastas)

| # | Atual | Destino | Operação |
|---|-------|---------|----------|
| B1 | `07-results/final-results` | `07_results/reports` | RENAME |
| B2 | — | `07_results/metrics` | CREATE |
| B3 | — | `07_results/experiments` | CREATE |
| B4 | `10-runtime/local-cpu` | `99_system/01_runtime/local_cpu` | MOVE |
| B5 | `10-runtime/local-gpu` | `99_system/01_runtime/local_gpu` | MOVE |
| B6 | `10-runtime/kaggle` | `99_system/01_runtime/kaggle` | MOVE |
| B7 | `02-dataset/images` | `02_dataset/images` | KEEP (com pai) |
| B8 | `02-dataset/masks` | `02_dataset/masks` | KEEP (com pai) |
| B9 | `04-segmentation/outputs` | `04_segmentation/outputs` | KEEP (com pai) |

---

## C. Ficheiros Python

| # | Atual | Destino | Operação |
|---|-------|---------|----------|
| C1 | `04-segmentation/train.py` | `04_segmentation/train.py` | KEEP |
| C2 | `04-segmentation/dataset.py` | `04_segmentation/dataset.py` | KEEP |
| C3 | `04-segmentation/model.py` | `04_segmentation/model.py` | KEEP |
| C4 | `00-common/runtime_paths.py` | `00_common/runtime_paths.py` | RENAME (path) |
| C5 | `00-common/bootstrap/bootstrap.py` | `00_common/bootstrap/bootstrap.py` | RENAME (path) |
| C6 | `00-common/bootstrap/config.py` | `00_common/bootstrap/config.py` | RENAME (path) |
| C7 | `00-common/bootstrap/checks.py` | `00_common/bootstrap/checks.py` | RENAME (path) |
| C8 | `00-common/bootstrap/__init__.py` | `00_common/bootstrap/__init__.py` | RENAME (path) |
| C9 | `10-runtime/local-cpu/adapter.py` | `10_runtime/local_cpu/runtime_adapter.py` | RENAME |
| C10 | `10-runtime/local-gpu/adapter.py` | `10_runtime/local_gpu/runtime_adapter.py` | RENAME |
| C11 | `10-runtime/kaggle/adapter.py` | `10_runtime/kaggle/runtime_adapter.py` | RENAME |
| C12 | — | `00_common/training_provider.py` | CREATE |
| C13 | `scripts/gen_notebooks.py` | `99_system/tools/generate_notebooks.py` | MOVE+RENAME |

---

## D. Notebooks

| # | Atual | Destino | Operação |
|---|-------|---------|----------|
| D1 | `00-common/01-functions.ipynb` | `00_common/01_functions.ipynb` | RENAME |
| D2 | `00-common/02-filters.ipynb` | `00_common/02_filters.ipynb` | RENAME |
| D3 | `00-common/03-morphology.ipynb` | `00_common/03_morphology.ipynb` | RENAME |
| D4 | `00-common/04-metrics.ipynb` | `00_common/04_metrics.ipynb` | RENAME |
| D5 | `00-common/05-visualization.ipynb` | `00_common/05_visualization.ipynb` | RENAME |
| D6 | `00-common/06-uploading.ipynb` | `00_common/06_uploading.ipynb` | RENAME |
| D7 | `00-common/07-training-provider.ipynb` | `00_common/07_training_provider.ipynb` | RENAME |
| D8 | `10-runtime/kaggle/launch.ipynb` | `10_runtime/kaggle/launch_kaggle.ipynb` | OPTIONAL |

---

## E. Configuração e infraestrutura

| # | Atual | Destino | Operação |
|---|-------|---------|----------|
| E1 | `04-segmentation/config.yaml` | `04_segmentation/config.yaml` | RENAME (path) |
| E2 | `10-runtime/local-cpu/config.yaml` | `10_runtime/local_cpu/config.yaml` | RENAME (path) + valores |
| E3 | `10-runtime/local-gpu/config.yaml` | `10_runtime/local_gpu/config.yaml` | RENAME (path) + valores |
| E4 | `10-runtime/kaggle/config.yaml` | `10_runtime/kaggle/config.yaml` | RENAME (path) |
| E5 | `10-runtime/local-cpu/Dockerfile` | `10_runtime/local_cpu/Dockerfile` | RENAME (path) + COPY lines |
| E6 | `10-runtime/local-gpu/Dockerfile` | `10_runtime/local_gpu/Dockerfile` | RENAME (path) + COPY lines |
| E7 | `10-runtime/local-cpu/docker-compose.yml` | `10_runtime/local_cpu/docker-compose.yml` | RENAME (path) + refs |
| E8 | `10-runtime/local-gpu/docker-compose.yml` | `10_runtime/local_gpu/docker-compose.yml` | RENAME (path) + refs |
| E9 | `10-runtime/entrypoint.sh` | `10_runtime/entrypoint.sh` | RENAME (path) + refs |
| E10 | `10-runtime/*/requirements.txt` | `10_runtime/*/requirements.txt` | RENAME (path) |
| E11 | `requirements.txt` (raiz) | `requirements.txt` | KEEP |
| E12 | `README.md` (raiz) | `README.md` | KEEP |

---

## F. Valores semânticos (não são paths)

| # | Contexto | Atual | Destino |
|---|----------|-------|---------|
| F1 | `config.yaml` `provider` | `local-cpu` | `local_cpu` |
| F2 | `config.yaml` `provider` | `local-gpu` | `local_gpu` |
| F3 | `BOOTSTRAP_PROFILE` | `local-cpu` | `local_cpu` |
| F4 | `BOOTSTRAP_PROFILE` | `local-gpu` | `local_gpu` |
| F5 | Alias `BOOTSTRAP_PROFILE` | `cpu` | `local_cpu` (via alias) |
| F6 | Alias `BOOTSTRAP_PROFILE` | `gpu` | `local_gpu` (via alias) |
| F7 | `FETAL_PROVIDER` | `local-cpu` | `local_cpu` |
| F8 | `PROVIDERS` dict keys | `local-cpu` | `local_cpu` |
| F9 | `dataset_path` default | `./02-dataset` | `./02_dataset` |
| F10 | `output_path` default | `./04-segmentation/outputs` | `./04_segmentation/outputs` |
| F11 | Docker image tag | `fetal-vein-segmentation:local-cpu` | `fetal_vein_segmentation:local_cpu` | OPTIONAL |
| F12 | Compose service | `fetal-runtime-local-cpu` | `fetal_runtime_local_cpu` | OPTIONAL |

---

## G. Exceções (sem alteração de nome)

| Item |
|------|
| `train.py` |
| `dataset.py` |
| `model.py` |
| `README.md` |
| `Dockerfile` |
| `docker-compose.yml` |
| `mkdocs.yml` (futuro) |
| `config.yaml` |
| `requirements.txt` |
| `entrypoint.sh` |
| `.gitignore` |
| `/kaggle/input/fetal-vein` |

---

## H. Referências de código a atualizar (checklist Fase 10)

### H.1 Por ficheiro (código executável)

| Ficheiro | Tipo de alteração |
|----------|-------------------|
| `00_common/bootstrap/config.py` | Paths, notebook list, `final-results`→`reports`, profiles |
| `00_common/bootstrap/checks.py` | Markers, runtime file list, messages |
| `00_common/runtime_paths.py` | `detect_project_root` markers |
| `04_segmentation/train.py` | `adapter_map` paths |
| `04_segmentation/dataset.py` | default `02_dataset` |
| `10_runtime/*/runtime_adapter.py` | `00_common` path, train path, sys.path |
| `10_runtime/entrypoint.sh` | All paths |
| `10_runtime/local_cpu/Dockerfile` | COPY paths |
| `10_runtime/local_gpu/Dockerfile` | COPY paths |
| `10_runtime/local_cpu/docker-compose.yml` | dockerfile path, env |
| `10_runtime/local_gpu/docker-compose.yml` | idem |
| `10_runtime/*/config.yaml` | provider + relative paths |
| `00_common/07_training_provider.ipynb` | paths + provider keys |
| `10_runtime/kaggle/launch.ipynb` | paths |
| `99_system/tools/generate_notebooks.py` | paths |

### H.2 Notebooks — referências internas

| Ficheiro | Strings |
|----------|---------|
| `06_uploading.ipynb` | `%run 01_functions.ipynb`, texto `01-functions` |
| `05_visualization.ipynb` | `01-functions.ipynb` |
| `03_morphology.ipynb` | `01-functions.ipynb` |
| `01_functions.ipynb` | `06-uploading` |

### H.3 Documentação (commit separado recomendado)

| Área | Ficheiros |
|------|-----------|
| `99_system/documentation/governance/` | ~6 |
| `99_system/documentation/architecture/` | ~4 |
| `99_system/README.md` | 1 |
| `10_runtime/README.md` | 1 |
| `audit_report.md` | 1 |

---

## I. Contagem de impacto (estimativa)

| Categoria | Itens a renomear/mover |
|-----------|------------------------|
| Diretórios raiz | 11 RENAME + 3 CREATE + 1 DELETE |
| Subpastas runtime | 3 RENAME |
| Ficheiros Python (nome) | 3 adapters + 1 script |
| Notebooks | 7–8 RENAME |
| Ficheiros Docker/shell | 5 paths |
| Valores YAML/env | ~12 campos |
| Referências em código | ~120 substituições |

---

## J. Ordem de dependência (resumo)

```text
99_system (já OK)
    ↑
00_common + 02_dataset … 07_results   (onda 1 — científico)
    ↑
04_segmentation                      (onda 2 — pipeline)
    ↑
10_runtime                           (onda 3 — execução)
    ↑
notebooks + training_provider        (onda 4)
    ↑
docs 99_system                       (onda 5)
```

Detalhe completo em [migration_plan.md](migration_plan.md).

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
