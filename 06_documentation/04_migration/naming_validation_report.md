# Relatório de Validação Definitiva da Nomenclatura

**Projeto:** `fetal_vein_segmentation`  
**Fase:** 3 — validação e planeamento (sem alterações no repositório)  
**Data:** 2026-05-29  
**Estado:** **APROVADO PARA EXECUÇÃO NA FASE 10**

---

## 0. Veredito executivo

A nomenclatura alvo em **`snake_case`** é **coerente, aplicável e recomendada** para todo o repositório numerado (00–10, 99), com **exceções documentadas** para nomes de indústria e decisões já aprovadas (`train.py`).

| Área | Validação |
|------|-----------|
| Diretórios 00–09, 99 | Aprovado |
| `10_runtime` + `local_cpu` / `local_gpu` | Aprovado |
| Ficheiros Python pipeline | **Manter** `train.py`, `dataset.py`, `model.py` |
| Adapters | **Recomendar** `adapter.py` → `runtime_adapter.py` (Fase 10) |
| Valores `provider` em YAML | Migrar `local-cpu` → `local_cpu` (com aliases temporários) |
| `07_results` + subpastas | Aprovado; renomear `final-results` → `reports`; criar `experiments` |
| `99_system/documentation/*` | Já conforme |
| MkDocs (fase futura) | Compatível se paths alvo forem usados na config |

**Nenhuma colisão de nomes** impede a migração se esta for feita por **ondas ordenadas** (ver `migration_plan.md`).

---

## 1. Diretórios

### 1.1 Pastas numeradas (raiz)

| Atual | Destino | Ação | Notas |
|-------|---------|------|-------|
| `00-common` | `00_common` | Renomear | 23+ refs em código ativo |
| `01-literature-review` | `01_literature_review` | Renomear | Vazia; baixo risco |
| `02-dataset` | `02_dataset` | Renomear | YAML + bootstrap + adapters |
| `03-preprocessing` | `03_preprocessing` | Renomear | Referenciada no bootstrap |
| `04-segmentation` | `04_segmentation` | Renomear | **Crítico** — pipeline + Docker + notebooks |
| `05-postprocessing` | `05_postprocessing` | Renomear | Bootstrap |
| `06-evaluation` | `06_evaluation` | Renomear | Bootstrap |
| `07-results` | `07_results` | Renomear | Bootstrap; subpasta `final-results` |
| `08-report` | `08_report` | **Criar** | Não existe no disco |
| `09-presentation` | `09_presentation` | **Criar** | Não existe no disco |
| `00-project` | `00_project` | **Criar** (opcional) | Planeado na governação; não referenciado no código |
| `10-runtime` | `10_runtime` | Renomear | **Crítico** — Docker, adapters, entrypoint |
| `10-docker` | — | **Remover** | Apenas README; redirecionar para `10_runtime` |
| `scripts` | `99_system/tools` | Mover | `gen_notebooks.py` |
| — | `99_system` | Já existe | Infraestrutura |

### 1.2 Subpastas `00_common`

| Atual | Destino | Ação |
|-------|---------|------|
| `00-common/bootstrap` | `00_common/bootstrap` | Renomear com pai |

### 1.3 Subpastas `02_dataset`

| Atual | Destino | Ação |
|-------|---------|------|
| `images` | `images` | **Manter** |
| `masks` | `masks` | **Manter** |
| `statistics` | `statistics` | **Manter** (bootstrap cria) |
| `figures` | `figures` | **Manter** |

### 1.4 Subpastas `04_segmentation`

| Atual | Destino | Ação |
|-------|---------|------|
| `outputs` | `outputs` | **Manter** |
| `outputs/checkpoints` | `outputs/checkpoints` | **Manter** |
| `outputs/logs` | `outputs/logs` | **Manter** |

### 1.5 Subpastas `07_results`

| Atual | Destino | Ação |
|-------|---------|------|
| `figures` | `figures` | **Manter** |
| `comparisons` | `comparisons` | **Manter** |
| `final-results` | `reports` | **Renomear** (governação) |
| — | `metrics` | **Criar** (bootstrap não cria hoje) |
| — | `experiments` | **Criar** |

### 1.6 Subpastas `06_evaluation`

| Atual | Destino | Ação |
|-------|---------|------|
| `metrics` | `metrics` | **Manter** |
| `tables` | `tables` | **Manter** |
| `plots` | `plots` | **Manter** |

### 1.7 Runtime `10_runtime`

| Atual | Destino | Ação |
|-------|---------|------|
| `10-runtime/local-cpu` | `10_runtime/local_cpu` | Renomear |
| `10-runtime/local-gpu` | `10_runtime/local_gpu` | Renomear |
| `10-runtime/kaggle` | `10_runtime/kaggle` | Renomear (nome já snake_case) |

### 1.8 `99_system` (já validado)

| Atual | Destino | Ação |
|-------|---------|------|
| `99_system/documentation/governance` | — | **Manter** |
| `99_system/documentation/architecture` | — | **Manter** |
| `99_system/documentation/templates` | — | **Manter** |
| `99_system/documentation/migration` | — | **Manter** |
| — | `99_system/documentation/mkdocs` | **Criar** (Fase 5) |
| — | `99_system/tools` | **Criar** (migração `scripts/`) |

---

## 2. Ficheiros

### 2.1 Pipeline `04_segmentation`

| Atual | Destino | Decisão | Justificação |
|-------|---------|---------|--------------|
| `train.py` | `train.py` | **MANTER** | Decisão aprovada; entry point canónico |
| `dataset.py` | `dataset.py` | **MANTER** | Já `snake_case`; imports `from dataset import` |
| `model.py` | `model.py` | **MANTER** | Idem |
| `config.yaml` | `config.yaml` | **MANTER** | Convenção standard |
| `outputs/.gitkeep` | `outputs/.gitkeep` | **MANTER** | |

**Nota:** `dataset_loader.py` é exemplo de estilo na governação, **não** rename obrigatório face a `dataset.py` funcional.

### 2.2 `00_common`

| Atual | Destino | Decisão |
|-------|---------|---------|
| `runtime_paths.py` | `runtime_paths.py` | **MANTER** |
| `bootstrap/bootstrap.py` | `bootstrap/bootstrap.py` | **MANTER** |
| `bootstrap/config.py` | `bootstrap/config.py` | **MANTER** |
| `bootstrap/checks.py` | `bootstrap/checks.py` | **MANTER** |
| `bootstrap/__init__.py` | `bootstrap/__init__.py` | **MANTER** |
| — | `training_provider.py` | **CRIAR** (Fase 10+) | Extrair de `07_training_provider.ipynb` |

### 2.3 Runtimes `10_runtime/*`

| Atual | Destino | Decisão |
|-------|---------|---------|
| `local_cpu/adapter.py` | `local_cpu/runtime_adapter.py` | **RENOMEAR** (recomendado) |
| `local_gpu/adapter.py` | `local_gpu/runtime_adapter.py` | **RENOMEAR** |
| `kaggle/adapter.py` | `kaggle/runtime_adapter.py` | **RENOMEAR** |
| `*/config.yaml` | `*/config.yaml` | **MANTER** |
| `*/requirements.txt` | `*/requirements.txt` | **MANTER** |
| `*/Dockerfile` | `*/Dockerfile` | **MANTER** (exceção indústria) |
| `*/docker-compose.yml` | `*/docker-compose.yml` | **MANTER** |
| `entrypoint.sh` | `entrypoint.sh` | **MANTER** |
| `kaggle/launch.ipynb` | `kaggle/launch_kaggle.ipynb` | **OPCIONAL** | Melhor descoberta; não obrigatório |

### 2.4 Raiz e infraestrutura

| Atual | Destino | Decisão |
|-------|---------|---------|
| `README.md` | `README.md` | **MANTER** (exceção) |
| `requirements.txt` | `requirements.txt` | **MANTER** |
| `.gitignore` | `.gitignore` | **MANTER** |
| `scripts/gen_notebooks.py` | `99_system/tools/generate_notebooks.py` | **MOVER + RENOMEAR** |
| `10-docker/README.md` | — | **REMOVER** após migração |

### 2.5 Documentação `99_system`

| Atual | Destino | Decisão |
|-------|---------|---------|
| Todos os `.md` em `governance/`, `architecture/`, `templates/` | — | **MANTER** (já snake_case) |
| `audit_report.md` | `audit_report.md` | **MANTER** |
| — | `migration_report.md` | **CRIAR** (Fase 11) |
| — | `mkdocs/mkdocs.yml` | **CRIAR** (Fase 5) |

---

## 3. Notebooks

### 3.1 Mapa de renomeação

| Atual | Destino | Estado atual |
|-------|---------|--------------|
| `01-functions.ipynb` | `01_functions.ipynb` | Com conteúdo |
| `02-filters.ipynb` | `02_filters.ipynb` | Com conteúdo |
| `03-morphology.ipynb` | `03_morphology.ipynb` | Com conteúdo |
| `04-metrics.ipynb` | `04_metrics.ipynb` | **Ficheiro vazio (0 B)** |
| `05-visualization.ipynb` | `05_visualization.ipynb` | Com conteúdo |
| `06-uploading.ipynb` | `06_uploading.ipynb` | Com conteúdo; **`%run 01-functions.ipynb`** |
| `07-training-provider.ipynb` | `07_training_provider.ipynb` | Com conteúdo |
| `10-runtime/kaggle/launch.ipynb` | `10_runtime/kaggle/launch_kaggle.ipynb` | Opcional |

### 3.2 Referências cruzadas (impacto)

| Origem | Referência legada | Atualização Fase 10 |
|--------|-------------------|---------------------|
| `06_uploading.ipynb` | `%run 01-functions.ipynb` | `%run 01_functions.ipynb` |
| `06_uploading.ipynb` | texto `01-functions.ipynb` | `01_functions.ipynb` |
| `05_visualization.ipynb` | markdown `01-functions.ipynb` | `01_functions.ipynb` |
| `03_morphology.ipynb` | markdown `01-functions.ipynb` | idem |
| `01_functions.ipynb` | markdown `06-uploading` | `06_uploading` |
| `bootstrap/config.py` | lista de 7 nomes | 7 nomes novos |

### 3.3 Conflitos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| `%run` com path antigo | **Alta** | Atualizar na mesma PR que renomeia notebooks |
| Jupyter «Recent» com path antigo | Baixa | Reabrir a partir de `00_common` |
| Dois nomes durante migração parcial | **Alta** | Renomear pasta `00_common` e notebooks na **mesma onda** |

### 3.4 Documentação MkDocs

Nav proposto usará paths estáveis:

```text
notebooks/01_functions.md   → pode ser página stub que aponta ao .ipynb
```

MkDocs não executa notebooks por defeito; links serão do tipo «abrir notebook no repo».

---

## 4. Runtime

### 4.1 Pastas

| Legado | Alvo |
|--------|------|
| `10-runtime` | `10_runtime` |
| `local-cpu` | `local_cpu` |
| `local-gpu` | `local_gpu` |
| `kaggle` | `kaggle` |

### 4.2 Valores semânticos (não só paths)

| Campo | Legado | Alvo |
|-------|--------|------|
| `provider` em YAML | `local-cpu` | `local_cpu` |
| `provider` em YAML | `local-gpu` | `local_gpu` |
| `BOOTSTRAP_PROFILE` | `local-cpu`, `local-gpu` | `local_cpu`, `local_gpu` |
| Aliases | `cpu`, `gpu` | **Manter 1 versão** → mapear para `local_cpu`, `local_gpu` |
| `FETAL_PROVIDER` | `local-cpu` | `local_cpu` |
| Docker image tag | `fetal-vein-segmentation:local-cpu` | `fetal_vein_segmentation:local_cpu` (opcional) |
| Compose service name | `fetal-runtime-local-cpu` | `fetal_runtime_local_cpu` (opcional) |

### 4.3 Ficheiros impactados (inventário)

| Ficheiro | Ocorrências path/profile |
|----------|--------------------------|
| `00_common/bootstrap/config.py` | ~23 |
| `00_common/bootstrap/checks.py` | ~16 |
| `00_common/runtime_paths.py` | 4 |
| `04_segmentation/train.py` | 7 |
| `10_runtime/*/adapter.py` | 6 cada |
| `10_runtime/entrypoint.sh` | 7 |
| `10_runtime/local_*/Dockerfile` | 2–3 cada |
| `10_runtime/local_*/docker-compose.yml` | 9 cada |
| `10_runtime/*/config.yaml` | paths + provider |
| `00_common/07_training_provider.ipynb` | 8 |
| `10_runtime/kaggle/launch.ipynb` | 5 |
| `scripts/gen_notebooks.py` | 15 |
| Documentação `99_system` | ~70 (não bloqueia runtime) |

### 4.4 Docker — validação

| Aspeto | Impacto | Notas |
|--------|---------|-------|
| `COPY 10-runtime/...` | **Alto** | Atualizar para `10_runtime` no mesmo commit |
| `context: ../..` | Nenhum | Mantém raiz do projeto |
| `dockerfile: 10-runtime/...` | **Alto** | Path no compose |
| Volumes bind `.:/workspace` | Nenhum | Path host independente do nome interno |
| NVIDIA / CUDA | Nenhum | |

### 4.5 Kaggle externo

Paths `/kaggle/input/fetal-vein` são **nome do dataset na plataforma Kaggle**, não pasta do repo — **não renomear** no código (exceção externa).

---

## 5. Resultados (`07_results`)

### 5.1 Estrutura alvo validada

```text
07_results/
├── figures/
├── metrics/
├── comparisons/
├── reports/          # substitui final-results
└── experiments/
    └── exp_YYYYMMDD_NNN/
        ├── manifest.yaml
        ├── metrics.json
        ├── config_snapshot.yaml
        ├── checkpoints/
        ├── logs/
        └── figures/
```

### 5.2 Alterações vs estado atual

| Item | Situação atual | Ação |
|------|----------------|------|
| `07-results` | Existe vazio | → `07_results` |
| `final-results` | Criado pelo bootstrap | → `reports` |
| `metrics/` em `07_results` | Não criado pelo bootstrap | Adicionar a `required_directories` |
| `experiments/` | Ausente | Criar |

### 5.3 Relação com `04_segmentation/outputs`

| Papel | Path | Mantém nome `outputs`? |
|-------|------|------------------------|
| Técnico (run) | `04_segmentation/outputs/` | **Sim** |
| Académico (citável) | `07_results/experiments/<id>/` | N/A |

Validado: **não há conflito de nome** entre `outputs` (pipeline) e `experiments` (results).

---

## 6. Documentação

### 6.1 Paths validados

```text
99_system/
└── documentation/
    ├── audit_report.md
    ├── migration/
    │   ├── naming_validation_report.md
    │   ├── migration_map.md
    │   └── migration_plan.md
    ├── governance/          # 6 ficheiros — OK
    ├── architecture/        # 4 ficheiros — OK
    ├── templates/           # 6 ficheiros — OK
    └── mkdocs/              # Fase 5 — a criar
        └── mkdocs.yml
```

### 6.2 MkDocs — implicações de nomenclatura

| Configuração | Valor recomendado |
|--------------|-------------------|
| `site_name` | Fetal Vein Segmentation |
| `docs_dir` | `docs` dentro de `mkdocs/` ou incluir `../governance` |
| `plugins` | `mkdocstrings`, `search` |
| Python paths | `../../..` (repo root), `00_common`, `04_segmentation` |

**Validação:** usar **apenas nomes alvo** no `mkdocs.yml` inicial (Fase 5) se MkDocs for configurado **após** migração; caso contrário, documentar dual-path temporário.

### 6.3 Atualização pós-migração

Ficheiros em `governance/` e `architecture/` referem `00-common` como legado — atualizar num commit **docs-only** após Fase 10.

---

## 7. Exceções confirmadas

| Nome | Manter? | Motivo |
|------|---------|--------|
| `README.md` | **Sim** | Convenção universal |
| `Dockerfile` | **Sim** | Convenção Docker |
| `docker-compose.yml` | **Sim** | Convenção Compose |
| `mkdocs.yml` | **Sim** | Convenção MkDocs |
| `train.py` | **Sim** | Decisão aprovada pelo autor do projeto |
| `config.yaml` | **Sim** | Config standard |
| `requirements.txt` | **Sim** | Python standard |
| `entrypoint.sh` | **Sim** | Shell standard |
| `.gitignore` | **Sim** | Git standard |
| `dataset.py` | **Sim** | Já conforme; evita churn de imports |
| `model.py` | **Sim** | Idem |
| `launch.ipynb` | **Opcional** | Pode manter-se se preferir brevidade |

### 7.1 Exceções externas (fora do repo)

| Nome | Manter? |
|------|---------|
| `/kaggle/input/fetal-vein` | **Sim** (dataset Kaggle) |
| Imagem Docker Hub upstream `pytorch/pytorch:...` | **Sim** |

---

## 8. Conflitos e riscos

### 8.1 Colisões de nomes

| Cenário | Risco | Conclusão |
|---------|-------|-----------|
| `00-common` e `00_common` coexistem | Impossível no mesmo pai sem conflito | Migração **atómica** por pasta |
| `local-cpu` vs `local_cpu` no mesmo YAML | Baixo | Um único valor após migração |
| `reports` vs `report` (08) | Nenhum | Pastas distintas |

### 8.2 Windows / OneDrive

| Problema | Probabilidade | Mitigação |
|----------|---------------|-----------|
| Renome lento em massa | Média | `git mv`; fechar Jupyter/Docker |
| Case-insensitivity | Baixa | Nomes distintos (`common` vs `cpu`) |
| Path length | Baixa | Prefixos `NN_` mantêm paths curtos |
| Ficheiro bloqueado | Média | Parar containers antes da onda Docker |

### 8.3 Imports Python

| Padrão | Após migração |
|--------|---------------|
| `from dataset import ...` em `04_segmentation` | **Sem alteração** (ficheiros não renomeados) |
| `import runtime_paths` via `sys.path` | Path `00_common` → atualizar insert |
| `importlib` load `adapter.py` | Atualizar path para `runtime_adapter.py` se renomeado |

### 8.4 Notebooks

| Problema | Mitigação |
|----------|-----------|
| `%run 01-functions.ipynb` | Uma célula a atualizar |
| Links markdown entre notebooks | grep + substituir em lote |

### 8.5 MkDocs

| Problema | Mitigação |
|----------|-----------|
| Links quebrados para paths antigos | Gerar `mkdocs.yml` com paths finais |
| mkdocstrings não encontra módulos | `paths: [repo_root, 00_common, 04_segmentation]` |

### 8.6 Docker

| Problema | Mitigação |
|----------|-----------|
| Build COPY falha | Commit único: pastas + Dockerfiles + compose |
| Utilizador com comando antigo `docker compose -f 10-runtime/...` | Documentar novo path; alias no README |

---

## 9. Identificadores Python (pós-migração — referência)

Funções **novas** (inglês); legado em notebooks pode permanecer até refatoração.

| Domínio | Exemplo alvo |
|---------|--------------|
| Dataset | `load_dataset()`, `resolve_dataset_paths()` |
| Treino | `train()` em `train.py` (manter) |
| Runtime | `prepare_environment()`, `validate_runtime()` |
| Provider | `get_provider()`, `export_results()` |
| Classes | `DatasetPaths`, `RuntimeAdapter`, `TrainingProvider` |
| Constantes | `PROJECT_ROOT`, `DEFAULT_BATCH_SIZE` |

---

## 10. Aprovação formal

| Critério | Resultado |
|----------|-----------|
| Consistência `snake_case` | Passa |
| Compatível MkDocs | Passa (com paths alvo) |
| Respeita decisões do autor | Passa (`train.py`, sem `src/`) |
| Plano de rollback | Definido em `migration_plan.md` |
| Sem renomeação nesta fase | **Cumprido** |

**Nomenclatura final validada para execução na Fase 10.**

---

## 11. Documentos relacionados

- [migration_map.md](migration_map.md) — tabelas completas máquina/humano
- [migration_plan.md](migration_plan.md) — ordem, riscos, rollback
- [../governance/naming_conventions.md](../governance/naming_conventions.md)

---

## Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Validação definitiva — Fase 3 |
