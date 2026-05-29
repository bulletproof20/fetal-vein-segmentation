# Decisão Oficial — Uniformização Nível A

**Data:** 2026-05-29  
**Estado:** aprovado  
**Substitui:** propostas de Nível B na Fase 3.1 (numerção em subpastas internas)

---

## Escopo aprovado (Nível A)

### Incluído

| Área | Regra |
|------|--------|
| Pastas raiz | `00_common` … `10_runtime`, `99_system` — `NN_snake_case`, sem hífens |
| Notebooks `00_common` | `01_functions.ipynb` … `07_training_provider.ipynb` |
| Runtime | `10_runtime/local_cpu`, `local_gpu`, `kaggle` — **sem** `01_local_cpu` |
| Provider IDs | `local_cpu`, `local_gpu`, `kaggle` (YAML/env, sem prefixo numérico) |
| Documentação | `99_system/05_documentation/01_governance` … `05_mkdocs` — pastas numeradas; ficheiros `.md` descritivos |
| Tools | `scripts/` → `99_system/04_tools/` |
| Results (raiz) | `07_results` + subpastas `figures`, `metrics`, `comparisons`, `reports`, `experiments` — **sem** `01_figures` |
| Pipeline | Manter `train.py`, `dataset.py`, `model.py` |
| Adapters | `adapter.py` → `runtime_adapter.py` (Fase 10) |

### Excluído (Nível B — não aplicar)

| Proposta | Estado |
|----------|--------|
| `10_runtime/01_local_cpu/` | **Rejeitado** |
| `07_results/01_figures/` | **Rejeitado** |
| `02_dataset/01_images/` | **Rejeitado** |
| `99_system/01_runtime/` (duplicar `10_runtime`) | **Rejeitado** |
| Mover bootstrap para `99_system` | **Rejeitado** |
| `04_segmentation/01_outputs/` | **Rejeitado** |
| `08_pipeline.ipynb` | **Opcional** — não planeado por defeito |
| Renumerar ficheiros `.md` (`01_project_governance.md`) | **Rejeitado** |

---

## Ordem de execução recomendada

1. **Fase 10** — migração física Nível A (`migration_plan.md`)
2. **Fase 5** — MkDocs com paths finais
3. **Fase 11** — `migration_report.md`

---

## Documentos de referência

- [uniformization_report.md](uniformization_report.md) — análise completa
- [migration_map.md](../../documentation/migration/migration_map.md) — mapa (ignorar linhas Nível B)
- [migration_plan.md](../../documentation/migration/migration_plan.md) — ondas de migração

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 | Aprovação Nível A |
