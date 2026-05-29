# Relatório de Uniformização Global da Estrutura — Fase 3.1

**Projeto:** `fetal_vein_segmentation`  
**Data:** 2026-05-29  
**Tipo:** análise e proposta definitiva — **sem implementação**  
**Princípio:** `NN_nome_em_snake_case` para elementos organizacionais criados pelo projeto

---

## Resumo executivo

| Dimensão | Conformidade atual | Proposta |
|----------|-------------------|----------|
| Pastas raiz 00–10 | **Não conforme** (hífens) | `NN_snake_case` — **RECOMENDADO** |
| Notebooks `00_common` | **Não conforme** | `01_functions.ipynb` … — **RECOMENDADO** |
| Runtime subpastas | **Não conforme** | Duas opções analisadas (secção 4) |
| `99_system` interno | **Parcial** | Reestruturação numerada — **OPCIONAL** |
| `07_results` subpastas | **Parcial** | Prefixos `01_`…`05_` — **OPCIONAL** |
| Ficheiros canónicos | Conforme exceções | **Manter** lista oficial (secção 8) |

**Conclusão:** a uniformização **completa** (Nível B) multiplica o custo de migração. **Decisão do projeto (2026-05-29): aplicar apenas Nível A.** Ver [level_a_decision.md](level_a_decision.md).

**Nível A aprovado:** pastas raiz + notebooks + `snake_case` sem hífens; runtime `local_cpu`/`local_gpu`/`kaggle`; `99_system/05_documentation/01_governance` …; subpastas de results **sem** `01_figures`.

---

## 1. Estrutura atual (inventário completo)

### 1.1 Raiz do repositório

```text
fetal_vein_segmentation/
├── README.md                          # vazio
├── requirements.txt
├── .gitignore
│
├── 00-common/                         # NÃO CONFORME (hífen)
├── 01-literature-review/              # NÃO CONFORME
├── 02-dataset/                        # NÃO CONFORME
├── 03-preprocessing/                  # NÃO CONFORME (referenciado; pode estar vazio)
├── 04-segmentation/                   # NÃO CONFORME
├── 05-postprocessing/                 # NÃO CONFORME
├── 06-evaluation/                     # NÃO CONFORME
├── 07-results/                        # NÃO CONFORME
├── 08-report/                         # AUSENTE
├── 09-presentation/                   # AUSENTE
│
├── 10-runtime/                        # NÃO CONFORME
├── 10-docker/                         # NÃO CONFORME (deprecado)
├── scripts/                           # NÃO CONFORME (sem NN_)
│
└── 99_system/                         # CONFORME (parcial — falta NN_ em subpastas)
    ├── README.md
    └── documentation/                 # NÃO CONFORME (sem índice 05_)
        ├── audit_report.md
        ├── governance/                # 6 × .md
        ├── architecture/              # 4 × .md
        ├── templates/                 # 6 × .md
        └── migration/                 # 3 × .md (Fase 3)
```

### 1.2 `00-common/`

```text
00-common/
├── 01-functions.ipynb                 # NÃO CONFORME
├── 02-filters.ipynb
├── 03-morphology.ipynb
├── 04-metrics.ipynb                   # 0 bytes
├── 05-visualization.ipynb
├── 06-uploading.ipynb
├── 07-training-provider.ipynb
├── runtime_paths.py                     # ficheiro — exceção implícita (nome já snake_case)
└── bootstrap/                         # subpasta SEM NN_ — NÃO CONFORME (regra estrita)
    ├── __init__.py
    ├── bootstrap.py
    ├── config.py
    └── checks.py
```

### 1.3 `04-segmentation/`

```text
04-segmentation/
├── train.py                           # EXCEÇÃO OFICIAL
├── dataset.py                         # EXCEÇÃO (canónico)
├── model.py                           # EXCEÇÃO (canónico)
├── config.yaml                        # EXCEÇÃO
└── outputs/                           # subpasta SEM NN_ — debate secção 7
    └── .gitkeep
```

### 1.4 `10-runtime/`

```text
10-runtime/
├── README.md
├── entrypoint.sh                      # EXCEÇÃO
├── local-cpu/                         # NÃO CONFORME (hífen + sem NN_)
├── local-gpu/
├── kaggle/
│   ├── adapter.py
│   ├── config.yaml
│   ├── requirements.txt
│   ├── README.md
│   └── launch.ipynb                   # sem NN_
```

### 1.5 `02-dataset/` e outputs de módulos

```text
02-dataset/                            # pasta vazia no inventário
├── images/                            # sem NN_ (dados, não “módulo”)
└── masks/

03-preprocessing/outputs/              # bootstrap cria; sem NN_
06-evaluation/metrics|tables|plots/    # sem NN_
07-results/figures|comparisons|final-results/  # final-results NÃO CONFORME
```

### 1.6 `99_system` (estado Fase 2–3)

```text
99_system/
├── README.md
├── documentation/                     # legado Fase 2
│   ├── audit_report.md
│   ├── governance/*.md
│   ├── architecture/*.md
│   ├── templates/*.md
│   └── migration/*.md
└── 05_documentation/                  # criado apenas para este relatório (Fase 3.1)
    └── 04_migration/
        └── uniformization_report.md
```

**Nota:** `99_system/05_documentation/` reflete a **proposta**; o conteúdo normativo vive ainda em `99_system/documentation/`.

---

## 2. Estrutura proposta (uniformização total)

### 2.1 Visão global alvo

```text
fetal_vein_segmentation/
├── README.md
├── requirements.txt
├── .gitignore
│
├── 00_common/
│   ├── 01_functions.ipynb
│   ├── 02_filters.ipynb
│   ├── 03_morphology.ipynb
│   ├── 04_metrics.ipynb
│   ├── 05_visualization.ipynb
│   ├── 06_uploading.ipynb
│   ├── 07_training_provider.ipynb
│   ├── 08_pipeline.ipynb              # NOVO — opcional (ver 2.2)
│   ├── runtime_paths.py
│   └── 02_bootstrap/                  # OPCIONAL: mover bootstrap para 99_system
│       └── ...
│
├── 01_literature_review/
├── 02_dataset/
│   ├── 01_images/                     # OPCIONAL — numeração em dados
│   └── 02_masks/
├── 03_preprocessing/
│   └── 01_outputs/
├── 04_segmentation/
│   ├── train.py
│   ├── dataset.py
│   ├── model.py
│   ├── config.yaml
│   └── 01_outputs/
│       ├── 01_checkpoints/
│       └── 02_logs/
├── 05_postprocessing/
│   └── 01_outputs/
├── 06_evaluation/
│   ├── 01_metrics/
│   ├── 02_tables/
│   └── 03_plots/
├── 07_results/
│   ├── 01_figures/
│   ├── 02_metrics/
│   ├── 03_comparisons/
│   ├── 04_reports/
│   └── 05_experiments/
│       └── exp_YYYYMMDD_NNN/
├── 08_report/
├── 09_presentation/
│
├── 10_runtime/
│   ├── entrypoint.sh
│   ├── 01_local_cpu/                  # ver secção 4
│   ├── 02_local_gpu/
│   └── 03_kaggle/
│
└── 99_system/
    ├── README.md
    ├── 01_runtime/                    # OPCIONAL — espelho lógico vs 10_runtime
    ├── 02_bootstrap/                    # OPCIONAL — mover de 00_common
    ├── 03_automation/                   # OPCIONAL — CI, hooks
    ├── 04_tools/
    │   └── generate_notebooks.py
    └── 05_documentation/
        ├── 00_audit_report.md           # OPCIONAL — prefixo em ficheiro .md
        ├── 01_governance/
        ├── 02_architecture/
        ├── 03_templates/
        ├── 04_migration/
        └── 05_mkdocs/
            └── mkdocs.yml
```

### 2.2 Notebook `08_pipeline.ipynb`

| Aspeto | Proposta |
|--------|----------|
| Função | Orquestrar treino (`train.py`) + provider sem duplicar lógica |
| Relação com `07_training_provider` | Pode fundir-se no 07 ou manter 08 como “runbook” académico |
| Classificação | **OPCIONAL** — só criar se houver narrativa pedagógica clara |

### 2.3 Modelo de dois níveis (recomendação pragmática)

| Nível | Âmbito | Obrigatoriedade |
|-------|--------|-----------------|
| **A** | Pastas raiz `NN_snake_case`; notebooks `NN_*.ipynb`; runtime `10_runtime/NN_provider`; sem hífens | **RECOMENDADO** |
| **B** | Subpastas internas com `01_`, `02_` (results, documentation, outputs) | **OPCIONAL** |
| **C** | Reorganizar `99_system` com `01_runtime` espelhando `10_runtime` | **NÃO RECOMENDADO** (duplicação) |

---

## 3. Elementos conformes

| Elemento | Motivo |
|----------|--------|
| `99_system` (nome) | `snake_case` + índice 99 |
| Ficheiros `train.py`, `dataset.py`, `model.py` | Exceções canónicas; já `snake_case` |
| `runtime_paths.py`, `bootstrap.py`, `config.py`, `checks.py` | `snake_case` (sem NN_ — ver regra ficheiros) |
| `requirements.txt`, `.gitignore` | Convenções de ecossistema |
| Subpastas `images`, `masks` | Nomes descritivos padrão de dataset |
| Documentos `.md` em governance | Conteúdo `snake_case` no nome do ficheiro |
| Princípio pipeline única | Arquiteturalmente conforme (não é naming) |

---

## 4. Elementos não conformes

### 4.1 Tabela consolidada (prioridade)

| ID | Atual | Alvo (mínimo Fase 3) | Alvo (uniformização total) | Prioridade |
|----|-------|----------------------|----------------------------|------------|
| N01 | `00-common` | `00_common` | `00_common` | Alta |
| N02–N08 | `01-…` a `07-…` | `01_…` a `07_…` | idem | Alta |
| N09 | — | `08_report`, `09_presentation` | idem | Média |
| N10 | `10-runtime` | `10_runtime` | idem | Alta |
| N11 | `10-docker` | remover | remover | Alta |
| N12 | `scripts/` | `99_system/04_tools` | idem | Média |
| N13 | `01-functions.ipynb` | `01_functions.ipynb` | idem | Alta |
| N14 | `07-training-provider.ipynb` | `07_training_provider.ipynb` | idem | Alta |
| N15 | `local-cpu` | `local_cpu` | `01_local_cpu` | Ver 4.2 |
| N16 | `final-results` | `reports` | `04_reports` | Média |
| N17 | `documentation/` | manter ou mover | `05_documentation/01_governance` | Ver 5 |
| N18 | `bootstrap/` | manter em `00_common` | `99_system/02_bootstrap` | Ver 6 |

---

## 5. Runtime — análise `01_local_cpu` vs `local_cpu`

### 5.1 Opção A — snake_case sem índice (Fase 3)

```text
10_runtime/
├── 01_local_cpu/    # NÃO — esta linha é Opção B
local_cpu/           # Opção A
local_gpu/
kaggle/
```

### 5.2 Opção B — subpastas numeradas (Fase 3.1)

```text
10_runtime/
├── 01_local_cpu/
├── 02_local_gpu/
└── 03_kaggle/
```

### 5.3 Vantagens da Opção B

| Vantagem | Descrição |
|----------|-----------|
| Ordenação | Explorador de ficheiros e MkDocs listam por ordem pedagógica (CPU → GPU → cloud) |
| Consistência | Alinha com `00_common`, `07_results`, `99_system/05_documentation` |
| Extensibilidade | `04_runpod`, `05_aws` sem ambiguidade de ordem |
| Documentação | Nav MkDocs previsível: «01 Local CPU» antes de «03 Kaggle» |

### 5.4 Desvantagens / impacto da Opção B

| Impacto | Detalhe |
|---------|---------|
| **Código** | `adapter_map`, `PROVIDERS`, `entrypoint.sh`, Docker COPY — +3 segmentos de path |
| **Config YAML** | Campo `provider: local_cpu` **não** deve incluir `01_` (provider é ID semântico, não path) |
| **Docker Compose** | `dockerfile: 10_runtime/01_local_cpu/Dockerfile` — paths mais longos |
| **Documentação externa** | Comandos `docker compose -f 10_runtime/local_cpu/...` deixam de ser óbvios |
| **Kaggle** | `03_kaggle` é estável; pouco ganho vs `kaggle` |
| **Dupla chave** | Risco de confusão: pasta `01_local_cpu` vs provider `local_cpu` |

### 5.5 Mapeamento provider ↔ pasta (recomendado se Opção B)

| Pasta | `provider` (YAML/env) | `BOOTSTRAP_PROFILE` |
|-------|----------------------|---------------------|
| `01_local_cpu` | `local_cpu` | `local_cpu` |
| `02_local_gpu` | `local_gpu` | `local_gpu` |
| `03_kaggle` | `kaggle` | `kaggle` |

### 5.6 Classificação

| Opção | Classificação |
|-------|---------------|
| `10_runtime` + `local_cpu` (sem `01_`) | **RECOMENDADO** — melhor relação custo/benefício |
| `10_runtime` + `01_local_cpu` | **OPCIONAL** — só se prioridade máxima em ordenação visual |
| Manter `local-cpu` (legado) | **NÃO RECOMENDADO** |

---

## 6. Documentation — `99_system/05_documentation/`

### 6.1 Proposta

```text
99_system/
└── 05_documentation/
    ├── 01_governance/
    ├── 02_architecture/
    ├── 03_templates/
    ├── 04_migration/
    └── 05_mkdocs/
        ├── mkdocs.yml
        └── docs/
```

Mover de: `99_system/documentation/{governance,architecture,templates,migration}`.

### 6.2 Vantagens

- Uma única regra `NN_` em todo o projeto organizacional.
- MkDocs `nav` espelha pastas (`01_governance/index.md`).
- Separação clara: código em `00–10`, meta em `99_system`.

### 6.3 Impacto

| Área | Impacto |
|------|---------|
| Links relativos | **Alto** — ~25 ficheiros `.md` com cross-links |
| Fase 2 docs | Requer atualização ou redirects no MkDocs |
| `audit_report.md` | Mover para `05_documentation/00_audit_report.md` ou `04_migration/` |
| Este relatório | Já em `05_documentation/04_migration/` (caminho alvo) |
| Grep / bookmarks | Utilizadores com paths antigos quebram |
| CI/docs build | Um único `docs_dir` em `05_mkdocs` |

### 6.4 Ficheiros `.md` — numerar ou não?

| Abordagem | Exemplo | Classificação |
|-----------|---------|---------------|
| Só pastas numeradas | `01_governance/project_governance.md` | **RECOMENDADO** |
| Pastas + ficheiros numerados | `01_project_governance.md` | **OPCIONAL** (ruído em links) |
| Prefixo em audit apenas | `00_audit_report.md` | **OPCIONAL** |

**Regra proposta:** numerar **diretórios**; ficheiros `.md` mantêm `snake_case` descritivo (`project_governance.md`).

### 6.5 Classificação global

| Alteração | Classificação |
|-----------|---------------|
| `documentation/` → `05_documentation/` | **RECOMENDADO** (junto com Fase 10) |
| Subpastas `01_governance` … `05_mkdocs` | **RECOMENDADO** |
| Renumerar nomes dos `.md` internos | **NÃO RECOMENDADO** |

---

## 7. Results — `07_results/01_figures/…`

### 7.1 Proposta

```text
07_results/
├── 01_figures/
├── 02_metrics/
├── 03_comparisons/
├── 04_reports/          # ex final-results
└── 05_experiments/
```

### 7.2 Vantagens

- Ordem fixa para relatório académico (figuras antes de experiências).
- Consistência com princípio `NN_`.

### 7.3 Impacto

| Área | Impacto |
|------|---------|
| Bootstrap `required_directories` | 5 paths a atualizar |
| `experiment_standards.md` | Paths nos exemplos |
| Scripts de promoção (futuro) | `07_results/05_experiments/` |
| Env vars | `RESULTS_DIR` pode manter raiz `07_results` sem subpath |
| Utilizador humano | Paths mais longos (`04_reports` vs `reports`) |

### 7.4 Subpastas de `05_experiments/<exp_id>/`

Proposta: **não** numerar dentro de cada experiência (`checkpoints/`, `figures/` — nomes canónicos de ML).

| Alteração | Classificação |
|-----------|---------------|
| `07-results` → `07_results` | **RECOMENDADO** |
| `final-results` → `04_reports` | **RECOMENDADO** |
| Prefixos `01_`–`05_` em subpastas | **OPCIONAL** |
| Numerar `images/` → `01_images/` em dataset | **NÃO RECOMENDADO** (convenção ML universal) |

---

## 8. System — `99_system/01_runtime/…`

### 8.1 Proposta

```text
99_system/
├── 01_runtime/        # documentação/espelho de 10_runtime?
├── 02_bootstrap/      # mover código bootstrap/
├── 03_automation/     # CI, pre-commit
├── 04_tools/
└── 05_documentation/
```

### 8.2 Análise crítica

| Subpasta | Função pretendida | Problema |
|----------|-------------------|----------|
| `01_runtime` | Duplicar `10_runtime`? | **Duplicação** — runtimes executáveis devem viver só em `10_runtime` |
| `02_bootstrap` | Centralizar bootstrap | **Desloca** código de `00_common` — quebra mental “common = biblioteca” |
| `03_automation` | CI | **RECOMENDADO** como pasta vazia inicial |
| `04_tools` | `generate_notebooks.py` | **RECOMENDADO** (mover `scripts/`) |
| `05_documentation` | Docs | **RECOMENDADO** |

### 8.3 Modelo corrigido (recomendado)

```text
99_system/
├── 01_tools/              # ou 04_tools se 01-03 reservados
├── 02_automation/
└── 03_documentation/      # única documentação; SEM 01_runtime duplicado
    ├── 01_governance/
    ├── 02_architecture/
    ├── 03_templates/
    ├── 04_migration/
    └── 05_mkdocs/
```

**Bootstrap** permanece em `00_common/02_bootstrap/` (numerado) **ou** `00_common/bootstrap/` sem índice (**RECOMENDADO** manter `bootstrap/` — pacote Python reconhecível).

### 8.4 Classificação

| Alteração | Classificação |
|-----------|---------------|
| `99_system/01_runtime/` (código Docker) | **NÃO RECOMENDADO** |
| `99_system/04_tools/` | **RECOMENDADO** |
| `99_system/03_automation/` | **OPCIONAL** |
| Mover bootstrap para `99_system` | **NÃO RECOMENDADO** |
| `99_system/05_documentation/NN_*` | **RECOMENDADO** |

---

## 9. Exceções oficiais (sem numeração)

### 9.1 Ficheiros canónicos — lista validada

| Ficheiro | Manter nome | Motivo |
|----------|-------------|--------|
| `train.py` | **Sim** | Decisão de projeto; entry point |
| `dataset.py` | **Sim** | Par com train; imports estáveis |
| `model.py` | **Sim** | Idem |
| `README.md` | **Sim** | Convenção Git/hosting |
| `Dockerfile` | **Sim** | Convenção Docker |
| `docker-compose.yml` | **Sim** | Convenção Compose |
| `requirements.txt` | **Sim** | Convenção Python |
| `mkdocs.yml` | **Sim** | Convenção MkDocs |
| `entrypoint.sh` | **Sim** | Convenção containers |
| `config.yaml` | **Sim** | Configuração por convenção |
| `.gitignore` | **Sim** | Convenção Git |
| `.gitkeep` | **Sim** | Placeholder |

### 9.2 Ficheiros recomendados como exceção adicional

| Ficheiro | Classificação |
|----------|---------------|
| `adapter.py` → `runtime_adapter.py` | Renome **recomendado** na Fase 10, mas nome final **sem** `01_` |
| `runtime_paths.py` | **Manter** |
| `__init__.py` | **Manter** |
| `launch.ipynb` / `launch_kaggle.ipynb` | **OPCIONAL** renome |
| Artefactos gerados (`last.pt`, `metrics.json`) | **Manter** |

### 9.3 Pastas excecionadas (sem `NN_`)

| Pasta | Motivo |
|-------|--------|
| `images/`, `masks/` | Convenção dataset |
| `outputs/` dentro de módulos | Convenção pipeline |
| `checkpoints/`, `logs/` | Convenção ML |
| `bootstrap/` (se não renumerar) | Módulo Python estável |

### 9.4 Valores semânticos (não são paths)

| Valor | Formato |
|-------|---------|
| `provider` | `local_cpu`, `local_gpu`, `kaggle` — **sem** prefixo `01_` |
| `experiment_id` | `exp_YYYYMMDD_NNN` |

---

## 10. Impacto transversal

### 10.1 Imports Python

| Cenário | Impacto |
|---------|---------|
| Renomear só pastas raiz | **Médio** — strings em ~15 ficheiros |
| `01_local_cpu` + provider `local_cpu` | **Médio** — separar path de ID |
| Mover bootstrap para `99_system` | **Alto** — `sys.path`, adapters, entrypoint |
| `train.py` / `dataset.py` inalterados | **Nenhum** em imports relativos pipeline |

### 10.2 Bootstrap

| Alteração | Ficheiros |
|-----------|-----------|
| Paths `02-dataset` etc. | `config.py`, `checks.py` |
| Lista notebooks | `config.py`, `checks.py` |
| Runtime paths `local-cpu/adapter.py` | `checks.py`, `config.runtime_adapter_dir` |
| `07_results/01_figures` | `required_directories` |

### 10.3 Runtime / Docker

| Alteração | Risco |
|-----------|-------|
| `10_runtime` | **Crítico** |
| `01_local_cpu` vs `local_cpu` | **Adicional** sobre Fase 3 |
| `runtime_adapter.py` | **Médio** |

### 10.4 Notebooks

| Item | Impacto |
|------|---------|
| Renomear 7 notebooks | **Alto** |
| `%run 01_functions.ipynb` | 1 célula crítica |
| Novo `08_pipeline.ipynb` | **Baixo** se opcional |

### 10.5 MkDocs

| Decisão | Efeito |
|---------|--------|
| `docs_dir: 99_system/05_documentation` | Nav hierárquica `01_governance/...` |
| mkdocstrings paths | `00_common`, `04_segmentation` pós-migração |
| Plugins `mkdocs-monorepo` | **NÃO RECOMENDADO** — complexidade desnecessária |

**Ordem recomendada:** uniformização nível A → migração Fase 10 → MkDocs (Fase 5).

### 10.6 Documentação existente

| Conjunto | Ficheiros afetados |
|----------|-------------------|
| Fase 2 governance/architecture | ~16 |
| Fase 3 migration | 3 + este relatório |
| README raiz | 1 |

---

## 11. Matriz de recomendações finais

| # | Alteração | Classificação |
|---|-----------|---------------|
| R1 | Pastas raiz `00_common` … `10_runtime`, `99_system` | **RECOMENDADO** |
| R2 | Notebooks `01_functions.ipynb` … `07_training_provider.ipynb` | **RECOMENDADO** |
| R3 | Remover `10-docker`, mover `scripts` → `99_system/04_tools` | **RECOMENDADO** |
| R4 | `10_runtime/local_cpu` (sem `01_`) | **RECOMENDADO** |
| R5 | `adapter.py` → `runtime_adapter.py` | **RECOMENDADO** |
| R6 | `07_results` + `reports` + `experiments` (sem prefixo 01–05) | **RECOMENDADO** |
| R7 | `99_system/documentation` → `05_documentation/01_governance` … | **RECOMENDADO** |
| R8 | `10_runtime/01_local_cpu` numerado | **OPCIONAL** |
| R9 | `07_results/01_figures` numerado | **OPCIONAL** |
| R10 | `99_system/01_runtime` duplicado | **NÃO RECOMENDADO** |
| R11 | Mover bootstrap para `99_system` | **NÃO RECOMENDADO** |
| R12 | `02_dataset/01_images` | **NÃO RECOMENDADO** |
| R13 | `08_pipeline.ipynb` | **OPCIONAL** |
| R14 | Renumerar ficheiros `.md` internos | **NÃO RECOMENDADO** |
| R15 | `00_common/02_bootstrap/` numerado | **OPCIONAL** |
| R16 | `04_segmentation/01_outputs/` numerado | **OPCIONAL** |

---

## 12. Proposta definitiva consolidada (para Fase 10 + MkDocs)

Estrutura **mínima recomendada** (nível A + documentação):

```text
fetal_vein_segmentation/
├── 00_common/
│   ├── 01_functions.ipynb … 07_training_provider.ipynb
│   ├── runtime_paths.py
│   └── bootstrap/
├── 01_literature_review/ … 09_presentation/
├── 04_segmentation/
│   ├── train.py | dataset.py | model.py | config.yaml
│   └── outputs/
├── 10_runtime/
│   ├── entrypoint.sh
│   ├── local_cpu/
│   ├── local_gpu/
│   └── kaggle/
└── 99_system/
    ├── 04_tools/
    └── 05_documentation/
        ├── 01_governance/
        ├── 02_architecture/
        ├── 03_templates/
        ├── 04_migration/
        └── 05_mkdocs/
```

Estrutura **uniformização máxima** (nível A + B — se aprovada explicitamente):

- Acrescentar `01_`–`05_` em `07_results/*`
- Acrescentar `01_`–`03_` em `10_runtime/*`
- Renumerar `99_system` para `03_documentation` se não usar `05_` por conflito com proposta anterior

**Conflito a resolver antes da Fase 10:** numeração de `99_system` top-level:

| Opção | Estrutura |
|-------|-----------|
| **X1** (proposta utilizador) | `99_system/05_documentation/01_governance/` |
| **X2** (simplificada) | `99_system/03_documentation/01_governance/` |

**Recomendação:** **X1** se `01_tools`, `02_automation` forem criados; caso contrário **X2** evita saltar índices.

---

## 13. Relação com documentos Fase 3

| Documento | Ação na implementação |
|-----------|----------------------|
| `naming_validation_report.md` | Atualizar com decisões 3.1 (nível A vs B) |
| `migration_map.md` | Acrescentar linhas `01_local_cpu`, `05_documentation`, etc. |
| `migration_plan.md` | Nova onda 1b se uniformização máxima |

**Localização legado:** `99_system/documentation/migration/`  
**Localização proposta:** `99_system/05_documentation/04_migration/` (unificar na Fase 10).

---

## 14. Critérios de aceitação — Fase 3.1

- [x] Inventário completo
- [x] Estrutura proposta documentada
- [x] Runtime numerado analisado
- [x] Documentation numerada analisada
- [x] Results numerados analisados
- [x] System layout analisado
- [x] Exceções oficiais validadas
- [x] Classificação RECOMENDADO / OPCIONAL / NÃO RECOMENDADO
- [x] Nenhuma alteração ao código ou pastas do projeto (exceto este relatório)

---

## Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Fase 3.1 — uniformização global (análise) |
