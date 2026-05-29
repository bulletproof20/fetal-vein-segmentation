# Relatório de Auditoria — Fase 1

**Projeto:** `fetal_vein_segmentation`  
**Data da auditoria:** 2026-05-29  
**Âmbito:** análise integral antes de governação, normalização e MkDocs  
**Estado:** apenas leitura do repositório; nenhum ficheiro existente foi modificado (exceto a criação deste relatório).

---

## 1. Resumo executivo

O projeto encontra-se numa fase **híbrida**: a arquitetura **pipeline vs runtime** está bem delineada (`04-segmentation` + `10-runtime`), mas a **nomenclatura**, **documentação**, **governação** e **estrutura académica completa** ainda não estão alinhadas com o modelo alvo (`snake_case`, `99_system`, MkDocs, templates).

| Dimensão | Estado atual | Risco |
|----------|--------------|-------|
| Arquitetura pipeline/runtime | Bom | Baixo |
| Nomenclatura global | Inconsistente | Alto |
| Documentação | Quase inexistente na raiz | Alto |
| Notebooks | Parcialmente estruturados | Médio |
| Código Python (módulos) | Poucos ficheiros; docstrings fracas | Médio |
| Resultados experimentais | Duplicação de conceitos de output | Alto |
| MkDocs / governação | Ausente | Alto |
| Pastas académicas (01–09) | Muitas vazias ou em falta | Médio |

---

## 2. Inventário da estrutura atual

### 2.1 Árvore observada (ficheiros versionados / com conteúdo)

```text
fetal_vein_segmentation/
├── README.md                          # vazio
├── requirements.txt                   # stack completo (CPU+GPU+Jupyter)
├── .gitignore
│
├── 00-common/                         # biblioteca partilhada + bootstrap
│   ├── 01-functions.ipynb … 06-uploading.ipynb
│   ├── 04-metrics.ipynb               # vazio (0 bytes)
│   ├── 07-training-provider.ipynb
│   ├── runtime_paths.py
│   └── bootstrap/
│       ├── __init__.py
│       ├── bootstrap.py
│       ├── config.py
│       └── checks.py
│
├── 01-literature-review/              # diretório existe; sem ficheiros
├── 02-dataset/                        # diretório existe; sem ficheiros
├── 03-preprocessing/                  # referenciado no bootstrap; sem ficheiros visíveis
├── 04-segmentation/                   # pipeline única (implementada)
│   ├── train.py, dataset.py, model.py
│   ├── config.yaml
│   └── outputs/.gitkeep
├── 05-postprocessing/                 # referenciado no bootstrap
├── 06-evaluation/                     # diretório vazio
├── 07-results/                        # diretório vazio
│
├── 10-runtime/                        # runtimes (implementado)
│   ├── entrypoint.sh
│   ├── README.md
│   ├── local-cpu/   (Dockerfile, compose, adapter, config, requirements)
│   ├── local-gpu/   (idem)
│   └── kaggle/      (adapter, config, launch.ipynb, requirements, README)
│
├── 10-docker/                         # deprecado — apenas README de redirecionamento
│
├── scripts/
│   └── gen_notebooks.py               # utilitário de geração (não documentado)
│
└── 99_system/                         # criado nesta fase (só este relatório)
    └── documentation/
        └── audit_report.md
```

### 2.2 Pastas referenciadas no bootstrap mas ausentes no disco

O `ProjectConfig.required_directories` e `checks.py` assumem:

| Pasta | No bootstrap | No disco (auditoria) |
|-------|--------------|----------------------|
| `00-project` | Não referenciada | **Ausente** |
| `08-report` | Não referenciada | **Ausente** |
| `09-presentation` | Não referenciada | **Ausente** |
| `07-results/figures`, `comparisons`, `final-results` | Criadas pelo bootstrap | Vazias se criadas |
| `06-evaluation/metrics`, `tables`, `plots` | Criadas pelo bootstrap | Vazias se criadas |
| `02-dataset/statistics`, `figures` | Criadas pelo bootstrap | Vazias se criadas |

**Conclusão:** o modelo mental do projeto (00–09) está **parcialmente materializado**; várias pastas são *placeholders* criados em runtime pelo bootstrap.

---

## 3. Nomenclatura — inconsistências

### 3.1 Diretórios

| Atual | Convenção alvo | Conflito |
|-------|----------------|----------|
| `00-common` | `00_common` | Hífen vs `snake_case` |
| `01-literature-review` | `01_literature_review` | Hífen + palavra composta |
| `02-dataset` | `02_dataset` | Hífen |
| `04-segmentation` | `04_segmentation` | Hífen |
| `10-runtime` | `10_runtime` (proposto) | Hífen; não listado no exemplo alvo mas necessário |
| `10-docker` | Remover ou `99_system/legacy` | Pasta redundante |
| `local-cpu`, `local-gpu` | `local_cpu`, `local_gpu` | Kebab-case em subpastas de runtime |
| `final-results` (bootstrap) | `final_results` ou `reports` | Hífen dentro de `07-results` |

**Padrão dominante atual:** prefixo numérico + **hífen** (`NN-nome`).  
**Padrão alvo:** prefixo numérico + **underscore** (`NN_nome`).

**Impacto da migração:** dezenas de referências hardcoded em Python, Docker, compose, notebooks, YAML e documentação.

### 3.2 Ficheiros Python

| Atual | Alvo (exemplo governação) | Notas |
|-------|---------------------------|-------|
| `train.py` | `train_model.py` (opcional) | Nome genérico vs descritivo |
| `dataset.py` | `dataset_loader.py` | Idem |
| `adapter.py` | `runtime_adapter.py` | Repetido em 3 runtimes |
| `runtime_paths.py` | OK em `snake_case` | Bom |
| `gen_notebooks.py` | `generate_notebooks.py` ou mover para `99_system` | Fora da estrutura numerada |

### 3.3 Ficheiros Notebook

| Atual | Alvo |
|-------|------|
| `01-functions.ipynb` | `01_functions.ipynb` |
| `07-training-provider.ipynb` | `07_training_provider.ipynb` |
| `launch.ipynb` (kaggle) | `launch_kaggle.ipynb` ou manter em runtime |

### 3.4 Funções e classes (Python)

**Módulos de pipeline / bootstrap (inglês técnico, `snake_case`):**

- `load_pipeline_config`, `resolve_dataset_paths`, `build_model`, `prepare_environment` — alinhados com o alvo.

**Notebooks `00-common` (português, `snake_case`):**

- `analisar_metadados`, `validar_dimensoes`, `garantir_uint8`, etc.

**Conflito de governação:** o documento alvo exemplifica funções em **inglês** (`load_dataset()`), enquanto a biblioteca de notebooks está em **português**. É necessária decisão explícita na Fase 2:

- **Opção A:** inglês em código exportável + português só em markdown de notebooks académicos.
- **Opção B:** português permitido em funções de notebooks; inglês obrigatório em `.py` de pipeline/bootstrap.

### 3.5 Constantes e variáveis de ambiente

| Atual | Alvo |
|-------|------|
| `FETAL_PROVIDER`, `FETAL_OUTPUT_PATH` | Estilo `SCREAMING_SNAKE` OK, mas prefixo `FETAL_` não está na governação |
| `BOOTSTRAP_PROFILE`, `PROJECT_ROOT` | OK |
| Sem módulo `constants.py` | Criar `DEFAULT_BATCH_SIZE`, `OUTPUT_DIRECTORY`, etc. |

### 3.6 Classes

| Atual | Alvo |
|-------|------|
| `DatasetPaths` | OK (`PascalCase`) |
| `ProjectConfig`, `CheckReport` | OK |
| `PairDataset` (interna em `train.py`) | Extrair para `UnetTrainer` / módulo dedicado se MkDocs exigir API estável |

---

## 4. Organização e arquitetura

### 4.1 Pontos fortes

1. **Separação pipeline / runtime** respeitada: treino só em `04-segmentation/train.py`.
2. **Adapters** por ambiente (`local-cpu`, `local-gpu`, `kaggle`) sem duplicar `train_*.py`.
3. **Bootstrap** centralizado com perfis e validações por runtime.
4. **Notebooks `00-common`** com secções markdown em `01-functions` (modelo reutilizável).

### 4.2 Problemas de organização

| Problema | Detalhe |
|----------|---------|
| **Dupla hierarquia de outputs** | Treino grava em `04-segmentation/outputs/`; bootstrap também gere `07-results/` e `06-evaluation/` sem ligação automática |
| **`scripts/` solto na raiz** | Deveria viver em `99_system/scripts` ou `99_system/tools` |
| **`10-docker` fantasma** | Só README; confunde novos utilizadores |
| **`99_system` inexistente** | Toda a governação pedida ainda não tem casa |
| **README raiz vazio** | Sem entrada para o projeto académico |
| **Sem `pyproject.toml`** | Dificulta tooling (ruff, black, mkdocstrings) |
| **Requirements fragmentados** | Raiz + 3 runtimes; risco de drift de versões |
| **Imports frágeis** | Adapters fazem `sys.path.insert` para `00-common` |

### 4.3 Ficheiros redundantes ou de dívida técnica

| Item | Recomendação |
|------|--------------|
| `10-docker/README.md` | Remover pasta após migração documentada |
| `scripts/gen_notebooks.py` | Integrar em tooling de `99_system` ou eliminar após notebooks estáveis |
| `04-metrics.ipynb` vazio | Implementar ou marcar explicitamente como WIP na governação |
| Conteúdo duplicado em `07-training-provider.ipynb` vs funções que deveriam ser `.py` | Extrair módulo `training_provider.py` para MkDocs |

---

## 5. Documentação

### 5.1 Estado atual

| Local | Estado |
|-------|--------|
| `README.md` (raiz) | Vazio |
| `10-runtime/README.md` | Existe; útil |
| `10-runtime/kaggle/README.md` | Existe |
| Docstrings em `.py` | Majoritariamente **uma linha em português**; não Google Style |
| MkDocs | **Ausente** |
| Governação formal | **Ausente** |
| Documentação de API | **Ausente** |

### 5.2 Problemas para MkDocs + mkdocstrings

1. Pacotes Python não são pacotes instaláveis (`00-common` sem `__init__.py` na raiz do pacote).
2. `04-segmentation` importa com `from dataset import ...` (imports relativos ao diretório, não ao pacote).
3. Bootstrap em `00-common/bootstrap` não é importável como `fetal_vein.bootstrap` sem configuração.
4. Funções definidas **dentro de notebooks** não aparecem em mkdocstrings sem extração.
5. Nenhum `mkdocs.yml` nem estrutura `docs/`.

---

## 6. Notebooks Jupyter

### 6.1 Inventário

| Notebook | Células | Estrutura markdown | Docstrings em funções |
|----------|---------|--------------------|------------------------|
| `01-functions.ipynb` | Rica | Títulos + secções | PT, curtas |
| `02-filters.ipynb` | Sim | Similar | PT |
| `03-morphology.ipynb` | Sim | Similar | PT |
| `04-metrics.ipynb` | **Vazio** | N/A | N/A |
| `05-visualization.ipynb` | Sim | Similar | PT |
| `06-uploading.ipynb` | Sim | Similar | PT |
| `07-training-provider.ipynb` | Mínima | Título + lista | Código sem Google Style |
| `10-runtime/kaggle/launch.ipynb` | Mínima | 1 título | Sem secções padronizadas |

### 6.2 Lacunas vs governação pretendida

- Sem template obrigatório (objetivo, pré-requisitos, inputs, outputs, reprodutibilidade).
- Numeração com **hífen** (`01-functions`) vs alvo `01_functions`.
- Mistura **PT/EN** nos títulos (`Training Provider` vs `01 — Funções`).
- Células `!python` no Kaggle — aceitável, mas deve constar na governação de notebooks.
- Sem metadados de experimento (ID, data, runtime, commit).

---

## 7. Código Python — legibilidade e manutenção

### 7.1 Qualidade geral

| Aspeto | Avaliação |
|--------|-----------|
| `from __future__ import annotations` | Consistente nos módulos novos |
| Type hints | Parcial (bom em `runtime_paths`, fraco em `train.py` interno) |
| Docstrings | Não conformes com Google Style EN |
| Comentários de secção | Quase ausentes nos `.py` |
| Classes internas | `PairDataset` dentro de `train()` — dificulta testes e docs |
| Tratamento de erros | Adequado para MVP; pouco logging estruturado |

### 7.2 Acoplamentos críticos para a migração

Todos os seguintes contêm paths literais `00-common`, `04-segmentation`, `10-runtime`:

- `00-common/bootstrap/config.py`, `checks.py`
- `04-segmentation/train.py`
- `10-runtime/*/adapter.py`
- `10-runtime/entrypoint.sh`
- Dockerfiles e `docker-compose.yml`
- `00-common/07-training-provider.ipynb`
- `10-runtime/kaggle/launch.ipynb`

---

## 8. Resultados experimentais

### 8.1 Estrutura atual

| Local | Conteúdo esperado | Estado |
|-------|-------------------|--------|
| `04-segmentation/outputs/checkpoints`, `logs`, `metrics.json` | Pós-treino | `.gitkeep` apenas |
| `07-results/figures`, `comparisons`, `final-results` | Relatório final | Pastas vazias / não criadas |
| `06-evaluation/metrics`, `tables`, `plots` | Avaliação | Vazias |

### 8.2 Conflito com alvo Fase 9

**Alvo:**

```text
07_results/
├── figures/
├── metrics/
├── comparisons/
├── reports/
└── experiments/
```

**Atual (bootstrap):** `final-results` em vez de `reports`; sem `experiments/`; métricas de treino em `04-segmentation/outputs/metrics.json`.

**Recomendação:** definir contrato único:

- `04_segmentation/outputs/` → artefactos **técnicos** do run (checkpoints, logs).
- `07_results/experiments/<exp_id>/` → manifesto + métricas + figuras por experiência.
- Script de **promoção** pós-treino: copiar/sincronizar de segmentation → results.

---

## 9. Runtimes e infraestrutura

| Item | Estado | Nota |
|------|--------|------|
| `local-cpu` / `local-gpu` Docker | Funcional no desenho | Paths com hífen |
| `kaggle` | Adapter + launch | OK |
| Aliases `cpu`/`gpu` | Suportados no bootstrap | Documentar como legado |
| `gen_notebooks.py` | Gera JSON programaticamente | Risco de divergência manual |

---

## 10. Matriz de conflitos entre convenções

| Domínio | Convenção A (atual) | Convenção B (alvo) | Severidade |
|---------|---------------------|---------------------|------------|
| Pastas numeradas | `NN-nome` | `NN_nome` | Crítica |
| Subpastas runtime | `local-cpu` | `local_cpu` | Alta |
| Ficheiros notebook | `01-functions` | `01_functions` | Alta |
| Idioma funções | PT (notebooks) | EN (governação) | Média — decisão necessária |
| Outputs | `04-segmentation/outputs` + `07-results` | `07_results/experiments` | Alta |
| Docstrings | PT one-liner | Google EN | Média |
| Nome projeto pasta | `fetal_vein_segmentation` | OK (`snake_case`) | — |

---

## 11. Riscos da migração (Fase 10)

1. **Quebra de Docker build** se `COPY` paths não forem atualizados em bloco.
2. **OneDrive / Windows** — renomeações em massa podem ser lentas; preferir um script único de migração.
3. **Git history** — renomear tudo de uma vez vs. commits incrementais por domínio.
4. **Notebooks** — referências cruzadas (`06-uploading` → `01-functions`) em markdown.
5. **Kaggle** — paths absolutos `/kaggle/...` independentes da rename local, mas notebooks no repo sim.
6. **Alunos / avaliação** — documentar período de convivência com aliases simbólicos (links ou script `compat_paths`).

---

## 12. Oportunidades (sem complexidade desnecessária)

1. Um único pacote Python `fetal_vein` (ou nome curto) com submódulos `common`, `segmentation`, `runtime`.
2. `07_training_provider.py` extraído do notebook; notebook passa a ser demo.
3. `mkdocs.yml` em `99_system/documentation/mkdocs/` com plugins Material + mkdocstrings.
4. Pre-commit mínimo: verificar nomes de ficheiros + notebook template headers.
5. `experiment_manifest.yaml` por run em `07_results/experiments/`.

---

## 13. Checklist de conformidade (estado atual)

| Requisito futuro | Conforme? |
|------------------|-----------|
| Diretórios `snake_case` | Não |
| Ficheiros `snake_case` | Parcial |
| Google docstrings | Não |
| Templates oficiais | Não |
| MkDocs Material | Não |
| Governação documentada | Não |
| Estrutura `07_results/experiments` | Não |
| Pipeline única de treino | **Sim** |
| Runtimes sem lógica de treino duplicada | **Sim** |
| Bootstrap multi-perfil | **Sim** |

---

## 14. Conclusão da Fase 1

O projeto tem **base arquitetural sólida** (pipeline única + adapters), mas **não está pronto** para documentação automática nem para uma base académica uniforme sem:

1. Migração sistemática `hífen → snake_case` em pastas e ficheiros.
2. Criação de `99_system` com governação e templates.
3. Resolução do modelo de **outputs experimentais**.
4. Decisão **PT vs EN** no código dos notebooks.
5. Extração gradual de código de notebooks para módulos `.py` documentáveis.

**Nenhuma alteração foi feita ao código, notebooks, bootstrap ou runtimes durante esta auditoria.**

---

## 15. Anexos

### A. Ficheiros Python versionados (contagem)

| Área | Ficheiros |
|------|-----------|
| `00-common` | 5 (`runtime_paths` + 4 bootstrap) |
| `04-segmentation` | 3 |
| `10-runtime` | 3 adapters |
| `scripts` | 1 |
| **Total** | **12** |

### B. Referências cruzadas a paths legados

Mínimo **40+ ocorrências** de strings `00-common`, `04-segmentation`, `10-runtime` em código, infra e notebooks (estimativa por grep).

### C. Dependências

- Raiz: ciência de dados + Jupyter + PyTorch + MONAI.
- Runtimes: CPU sem torch; GPU/Kaggle com torch/MONAI.
- **Sem** `mkdocs`, `mkdocstrings`, `ruff`, `black` nas dependências atuais.

---

*Fim do relatório de auditoria — Fase 1.*
