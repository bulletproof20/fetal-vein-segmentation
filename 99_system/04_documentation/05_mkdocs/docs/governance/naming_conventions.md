# Convenções de Nomenclatura

**Versão:** 1.1  
**Estado:** normativo (alvo pós-migração Fase 10)  
**Uniformização:** **Nível A** — pastas raiz e notebooks numerados; subpastas internas sem prefixo `01_` (exceto `99_system/05_documentation/NN_*`)

---

## 1. Regra geral

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Diretórios | `snake_case` | `04_segmentation` |
| Ficheiros Python | `snake_case` | `train.py`, `runtime_adapter.py` |
| Ficheiros Notebook | `snake_case` + prefixo numérico | `01_functions.ipynb` |
| Ficheiros Markdown | `snake_case` | `audit_report.md` |
| Funções Python | `snake_case` (inglês) | `load_dataset()` |
| Classes Python | `PascalCase` (inglês) | `DatasetLoader` |
| Constantes | `SCREAMING_SNAKE_CASE` | `DEFAULT_BATCH_SIZE` |
| Variáveis de ambiente | `SCREAMING_SNAKE_CASE` | `FETAL_OUTPUT_PATH` |

---

## 2. Pastas numeradas (00–10, 99)

Formato: `NN_nome_descritivo`

| Atual (legado) | Alvo | Notas |
|----------------|------|-------|
| `00-common` | `00_common` | Biblioteca + bootstrap |
| `01-literature-review` | `01_literature_review` | |
| `02-dataset` | `02_dataset` | |
| `03-preprocessing` | `03_preprocessing` | |
| `04-segmentation` | `04_segmentation` | Pipeline única |
| `05-postprocessing` | `05_postprocessing` | |
| `06-evaluation` | `06_evaluation` | |
| `07-results` | `07_results` | |
| `08-report` | `08_report` | A criar na migração |
| `09-presentation` | `09_presentation` | A criar na migração |
| `10-runtime` | `10_runtime` | Runtimes |
| `10-docker` | *(remover)* | Redirecionar para `10_runtime` |
| — | `99_system` | Infraestrutura |

**Prefixo numérico:** mantém ordenação académica; usar sempre dois dígitos + underscore.

---

## 3. Subpastas de runtime

| Atual (legado) | Alvo |
|----------------|------|
| `10-runtime/local-cpu` | `10_runtime/local_cpu` |
| `10-runtime/local-gpu` | `10_runtime/local_gpu` |
| `10-runtime/kaggle` | `10_runtime/kaggle` |

Ficheiros fixos por runtime:

```text
runtime_adapter.py    # atualmente adapter.py — renomeação opcional na Fase 10
config.yaml
requirements.txt
```

Docker: `Dockerfile`, `docker-compose.yml` (nomes standard da indústria — **não** renomear).

---

## 4. Ficheiros Python — decisões explícitas

| Ficheiro | Nome alvo | Decisão |
|----------|-----------|---------|
| Pipeline de treino | **`train.py`** | **Manter** (aprovado) |
| Carregamento de dados | `dataset.py` | Manter (conteúdo: funções `load_*`, `resolve_*`) |
| Modelo | `model.py` | Manter (`build_model`) |
| Adapter | `adapter.py` ou `runtime_adapter.py` | `adapter.py` aceite; `runtime_adapter.py` preferido em código novo |
| Paths partilhados | `runtime_paths.py` | Manter em `00_common` |

**Não criar** `src/fetal_vein/` — imports permanecem relativos ao layout do repositório até decisão futura.

---

## 5. Notebooks `00_common`

| Atual (legado) | Alvo |
|----------------|------|
| `01-functions.ipynb` | `01_functions.ipynb` |
| `02-filters.ipynb` | `02_filters.ipynb` |
| `03-morphology.ipynb` | `03_morphology.ipynb` |
| `04-metrics.ipynb` | `04_metrics.ipynb` |
| `05-visualization.ipynb` | `05_visualization.ipynb` |
| `06-uploading.ipynb` | `06_uploading.ipynb` |
| `07-training-provider.ipynb` | `07_training_provider.ipynb` |

**Funções dentro de notebooks:** preferir inglês (`analyze_metadata`) em código novo; funções legadas em português podem coexistir até refatoração gradual.

**Markdown:** sempre português (decisão D2).

---

## 6. Subpastas de resultados (`07_results`)

| Atual (bootstrap) | Alvo |
|-------------------|------|
| `final-results` | `reports` |
| — | `experiments` (nova) |

Estrutura alvo:

```text
07_results/
├── figures/
├── metrics/
├── comparisons/
├── reports/
└── experiments/
    └── <experiment_id>/
```

---

## 7. Outputs da pipeline (`04_segmentation/outputs`)

```text
outputs/
├── checkpoints/
├── logs/
└── metrics.json
```

Nomes de ficheiros gerados: `snake_case` (ex.: `last.pt`, `metrics.json`).

---

## 8. Idioma

| Contexto | Idioma |
|----------|--------|
| Identificadores Python | Inglês |
| Docstrings | Inglês (Google Style) |
| Comentários inline técnicos | Inglês |
| Markdown de notebooks | Português |
| Documentação de governação (`99_system`) | Português |
| Mensagens de log para utilizador académico | Português ou inglês (consistente por módulo) |

---

## 9. Prefixos e sufixos proibidos

- `train_local.py`, `train_gpu.py`, `train_kaggle.py`
- `model_gpu.py`, `dataset_kaggle.py`
- Pastas `tmp`, `test_output` na raiz (usar `99_system/scratch` se necessário)

---

## 10. Aliases temporários (migração)

Durante a Fase 10, podem manter-se aliases de ambiente:

| Alias legado | Perfil normalizado |
|--------------|-------------------|
| `cpu` | `local_cpu` |
| `gpu` | `local_gpu` |

Documentar em `migration_report.md` quando removidos.

---

## 11. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação com decisões aprovadas |
