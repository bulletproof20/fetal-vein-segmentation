# Plano de Migração — Consolidação arquitetural

**Versão:** 2.0 — **executada** (2026-05-29)  
**Relatório:** [architecture_consolidation_report.md](architecture_consolidation_report.md)  
**Uniformização:** **Nível A** — `snake_case` em pastas raiz; runtime em `99_system/01_runtime/`  
**Removido como topo:** `10_runtime`, `10_docker` → infraestrutura em `99_system/`

---

## 1. Objetivos

1. Aplicar nomenclatura `snake_case` em diretórios e ficheiros conforme [migration_map.md](migration_map.md).
2. Manter **funcionalidade** de bootstrap, Docker, pipeline `train.py` e notebooks.
3. Permitir **rollback** via Git em cada onda.
4. Preparar terreno para **MkDocs** (Fase 5) com paths finais.

---

## 2. Pré-condições

| # | Condição |
|---|----------|
| P1 | Working tree limpo (`git status`) |
| P2 | JupyterLab e containers Docker **parados** |
| P3 | Branch dedicada: `refactor/snake-case-migration` |
| P4 | Backup local ou push remoto antes de onda 3 |
| P5 | Fase 5 MkDocs: decidir se corre **antes** ou **depois** da migração (recomendado: **depois**) |

---

## 3. Estratégia geral

### 3.1 Abordagem

- **Ondas sequenciais** com commit por onda (6 commits mínimos).
- **`git mv`** para preservar histórico.
- **Não** deixar pastas legadas e novas em simultâneo no mesmo nível.
- **Aliases de perfil** (`cpu`/`gpu` → `local_cpu`/`local_gpu`) mantidos **1 release** no bootstrap.

### 3.2 O que não fazer

- Renomear metade dos paths num commit e testar (estado inconsistente).
- Renomear `train.py` (proibido por decisão de projeto).
- Criar `src/fetal_vein` nesta migração.
- Alterar lógica de treino nos adapters.

---

## 4. Ondas de migração

### Onda 0 — Preparação (sem rename)

| Passo | Ação | Risco |
|-------|------|-------|
| 0.1 | Criar branch `refactor/snake-case-migration` | Baixo |
| 0.2 | Script `99_system/tools/verify_paths.py` (opcional) — lista paths legados | Baixo |
| 0.3 | Tag Git `pre-snake-case-migration` | Baixo |

**Rollback:** checkout tag.

---

### Onda 1 — Estrutura científica (pastas 00–09)

**Operações:** `git mv` de todas as pastas numeradas exceto `10-runtime`.

| De | Para |
|----|------|
| `00-common` → `00_common` | … |
| `01-literature-review` → `01_literature_review` | … |
| … | … |
| `07-results` → `07_results` | … |

**Suboperações `07_results`:**

```bash
# Após mv 07-results → 07_results
git mv 07_results/final-results 07_results/reports   # se existir
mkdir -p 07_results/metrics 07_results/experiments
mkdir -p 08_report 09_presentation
```

**Criar:** `08_report`, `09_presentation`, opcionalmente `00_project`.

| Métrica | Valor |
|---------|-------|
| Risco | **Médio** — muitos paths default no bootstrap |
| Impacto | Bootstrap falha até onda 2 atualizar `config.py` |
| Duração estimada | 15 min + validação |

**Validação parcial:** pastas existem no disco; **não** executar bootstrap ainda.

**Rollback:** `git revert` do commit ou `git reset --hard` à tag (se não houve commits seguintes).

---

### Onda 2 — Pipeline + common paths no código

**Operações:**

1. Atualizar `00_common/bootstrap/config.py` — todos os paths `02-dataset` → `02_dataset`, etc.
2. Atualizar `00_common/bootstrap/checks.py` — markers, mensagens, lista notebooks.
3. Atualizar `00_common/runtime_paths.py` — deteção `00_common` + `10_runtime`.
4. Atualizar `04_segmentation/dataset.py` — default dataset path.
5. Atualizar `04_segmentation/train.py` — `adapter_map` (paths apenas; ficheiro ainda `adapter.py` se onda 3 não correu).

| Métrica | Valor |
|---------|-------|
| Risco | **Alto** |
| Impacto | Bootstrap e `train.py` dependem disto |
| Teste | `python 00_common/bootstrap/bootstrap.py --no-strict` |

**Rollback:** revert commit onda 2.

---

### Onda 3 — Runtime (crítico Docker)

**Ordem interna:**

1. `git mv 10-runtime 10_runtime`
2. `git mv 10_runtime/local-cpu 10_runtime/local_cpu`
3. `git mv 10_runtime/local-gpu 10_runtime/local_gpu`
4. Atualizar `Dockerfile` (COPY paths), `docker-compose.yml`, `entrypoint.sh`
5. Atualizar `config.yaml` — `provider` e paths relativos
6. `git mv adapter.py → runtime_adapter.py` em cada provider
7. Atualizar referências `adapter.py` → `runtime_adapter.py` em train, entrypoint, launch, checks
8. `git rm -r 10-docker`

| Métrica | Valor |
|---------|-------|
| Risco | **Crítico** |
| Impacto | Build Docker, Kaggle launch, bootstrap runtime checks |
| Teste | `docker compose -f 10_runtime/local_cpu/docker-compose.yml build` |
| Teste | `python 10_runtime/local_cpu/runtime_adapter.py` |

**Rollback:** revert onda 3 inteira; reconstruir imagens Docker.

---

### Onda 4 — Notebooks e training provider

**Operações:**

1. `git mv` dos 7 notebooks em `00_common`
2. Atualizar `%run` e markdown em `06_uploading`, `05_visualization`, `03_morphology`, `01_functions`
3. Extrair (opcional nesta onda) `00_common/training_provider.py` do notebook 07
4. Atualizar `07_training_provider.ipynb` para importar módulo
5. `git mv` `launch.ipynb` → `launch_kaggle.ipynb` (opcional)

| Métrica | Valor |
|---------|-------|
| Risco | **Médio-Alto** |
| Impacto | Fluxo académico Jupyter |
| Teste | Abrir `01_functions.ipynb`, executar `06_uploading` com `%run` |

**Rollback:** revert onda 4.

---

### Onda 5 — Tooling e documentação

**Operações:**

1. `git mv scripts/gen_notebooks.py` → `99_system/tools/generate_notebooks.py`
2. Atualizar referências internas do script
3. Atualizar todos os `.md` em `99_system/documentation` (legado → alvo)
4. Preencher `README.md` raiz com paths novos
5. Atualizar `10_runtime/README.md`, `kaggle/README.md`
6. Gerar `99_system/documentation/migration_report.md` (Fase 11)

| Métrica | Valor |
|---------|-------|
| Risco | **Baixo** |
| Impacto | Documentação apenas |

---

### Onda 6 — Validação final

| Teste | Comando / critério |
|-------|-------------------|
| Bootstrap CPU | `BOOTSTRAP_PROFILE=local_cpu python 00_common/bootstrap/bootstrap.py --no-strict` |
| Adapter CPU | `python 10_runtime/local_cpu/runtime_adapter.py` |
| Train dry-run | `python 04_segmentation/train.py` |
| Docker CPU build | `docker compose -f 10_runtime/local_cpu/docker-compose.yml up --build -d` |
| Grep legado | `rg "00-common|10-runtime|local-cpu" --glob '!99_system/documentation/migration/*'` → 0 no código |

---

## 5. Matriz de risco

| Onda | Risco | Probabilidade | Impacto | Mitigação |
|------|-------|---------------|---------|-----------|
| 0 | Baixo | Baixa | Baixo | Tag Git |
| 1 | Médio | Média | Médio | Commit isolado; não testar bootstrap |
| 2 | Alto | Média | Alto | Testar bootstrap antes de Docker |
| 3 | Crítico | Média | Crítico | Parar containers; um commit; rebuild |
| 4 | Médio-Alto | Média | Médio | Testar `%run` manualmente |
| 5 | Baixo | Baixa | Baixo | Docs-only revert fácil |
| 6 | — | — | — | Gate de merge |

---

## 6. Rollback

### 6.1 Por onda

```bash
git log --oneline -n 10
git revert <commit-hash-onda-N>   # preferível em branch partilhada
# ou
git reset --hard pre-snake-case-migration   # apenas em branch local
```

### 6.2 Rollback completo

1. `git checkout pre-snake-case-migration`
2. Branch nova ou force push (evitar em `main` sem acordo)
3. Remover imagens Docker órfãs: `docker image prune`

### 6.3 Rollback parcial (não recomendado)

Manter `04_segmentation` migrado e `10-runtime` legado **quebra** `train.py` adapter_map — evitar.

---

## 7. Compatibilidade temporária (opcional)

Se necessário convivência de 1 semana:

| Mecanismo | Implementação |
|-----------|---------------|
| Symlink Windows | `mklink /J 00-common 00_common` (dev local) |
| Alias bootstrap | `PROFILE_ALIASES["local-cpu"] = "local_cpu"` já planeado |
| README | Banner «estrutura migrada em DATA» |

**Não** commitar symlinks no Git (Windows/Linux incompatível).

---

## 8. Coordenação com MkDocs (Fase 5)

| Ordem | Vantagem |
|-------|----------|
| **Migração → MkDocs** (recomendado) | `mkdocs.yml` nasce com paths finais |
| MkDocs → Migração | Requer segundo passe no `mkdocs.yml` |

Configuração mkdocstrings sugerida pós-migração:

```yaml
paths:
  - ../../../
  - ../../../00_common
  - ../../../04_segmentation
```

---

## 9. Cronograma sugerido

| Dia | Onda |
|-----|------|
| 1 | 0 + 1 + 2 |
| 2 | 3 (Docker) + testes |
| 3 | 4 + 5 + 6 |

Ajustar conforme disponibilidade; **não** comprimir ondas 2 e 3 no mesmo dia sem testes intermédios.

---

## 10. Critérios de aceitação (Fase 10 concluída)

- [ ] Zero pastas com hífen `NN-nome` na raiz (exceto exceções documentadas)
- [ ] `train.py` inalterado como nome
- [ ] Bootstrap OK em `local_cpu` e `local_gpu` (strict GPU conforme perfil)
- [ ] `docker compose` build CPU e GPU
- [ ] `train.py` dry-run ou treino curto OK
- [ ] Notebooks `%run` funcionais
- [ ] `migration_report.md` publicado
- [ ] `rg` sem paths legados no código executável

---

## 11. Pós-migração (Fase 11)

1. Publicar `migration_report.md` com diff de nomes.
2. Atualizar `naming_conventions.md` — remover coluna «legado».
3. Arquivar pasta `99_system/documentation/migration/` como referência histórica.

---

## 12. Documentos relacionados

- [naming_validation_report.md](naming_validation_report.md)
- [migration_map.md](migration_map.md)
- [../governance/project_governance.md](../governance/project_governance.md)

---

## Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Plano inicial — Fase 3 |
