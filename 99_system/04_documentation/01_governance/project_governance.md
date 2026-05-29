# Governação do Projeto

**Projeto:** Segmentação da veia umbilical fetal (`fetal_vein_segmentation`)  
**Versão:** 1.0  
**Estado:** normativo — Fase 2 (sem migração física aplicada)

---

## 1. Propósito

Este documento define a **governação global** do repositório académico: papéis das pastas, princípios arquiteturais, zonas de responsabilidade e regras de evolução.

É a **fonte oficial** para decisões de estrutura, documentação e qualidade. Documentos complementares:

| Documento | Conteúdo |
|-----------|----------|
| [coding_standards.md](coding_standards.md) | Código Python |
| [notebook_standards.md](notebook_standards.md) | Jupyter Notebooks |
| [documentation_standards.md](documentation_standards.md) | MkDocs e Markdown |
| [naming_conventions.md](naming_conventions.md) | Nomes de pastas e ficheiros |
| [experiment_standards.md](experiment_standards.md) | Resultados experimentais |
| [../architecture/system_architecture.md](../architecture/system_architecture.md) | Arquitetura de sistema |
| [../architecture/runtime_architecture.md](../architecture/runtime_architecture.md) | Runtimes |
| [../architecture/data_flow.md](../architecture/data_flow.md) | Fluxo de dados |
| [../architecture/technology_stack.md](../architecture/technology_stack.md) | Stack tecnológica |

---

## 2. Decisões aprovadas (baseline)

| ID | Decisão |
|----|---------|
| D1 | **Código Python em inglês** (identificadores, docstrings, comentários técnicos). |
| D2 | **Markdown dos notebooks em português** (títulos, secções, explicações). |
| D3 | Manter o ficheiro **`train.py`** na pipeline de segmentação. |
| D4 | **Não** criar pacote `src/fetal_vein` — módulos permanecem no layout numerado do repositório. |
| D5 | Migrar toda a estrutura para **`snake_case`** (pastas e ficheiros). |
| D6 | **`99_system`** é a zona única de infraestrutura, governação e tooling. |
| D7 | Pipeline científica **única**; runtimes **apenas** preparam ambiente. |

---

## 3. Princípio arquitetural central

```text
Mesmo código · Mesmo dataset · Mesmo output · Mesma estrutura
Diferente ambiente de execução
```

- A lógica de treino existe **uma vez** em `04_segmentation/` (alvo pós-migração; atualmente `04-segmentation/`).
- Os runtimes em `10_runtime/` (alvo) **não** duplicam treino, modelo ou dataset loaders dedicados por ambiente.
- Execução canónica: `python 04_segmentation/train.py` (caminho atual até à Fase 10).

---

## 4. Mapa de zonas do repositório

### 4.1 Zona científica (00–09)

| Pasta (alvo) | Responsabilidade |
|--------------|------------------|
| `00_common` | Biblioteca partilhada, bootstrap, utilitários |
| `01_literature_review` | Revisão bibliográfica |
| `02_dataset` | Dados brutos (images, masks) |
| `03_preprocessing` | Pré-processamento e outputs |
| `04_segmentation` | **Pipeline única** de treino (`train.py`, `dataset.py`, `model.py`) |
| `05_postprocessing` | Pós-processamento |
| `06_evaluation` | Métricas, tabelas, gráficos de avaliação |
| `07_results` | Resultados finais e experiências |
| `08_report` | Relatório académico |
| `09_presentation` | Apresentação |

### 4.2 Zona de execução

| Pasta (alvo) | Responsabilidade |
|--------------|------------------|
| `10_runtime` | Ambientes: `local_cpu`, `local_gpu`, `kaggle` — Docker, adapters, configs |

### 4.3 Zona de infraestrutura

| Pasta | Responsabilidade |
|-------|------------------|
| `99_system` | Governação, templates, MkDocs, scripts de migração, auditoria, CI local |

**Proibido** colocar lógica de treino ou notebooks científicos principais dentro de `99_system`.

---

## 5. Papéis e responsabilidades

| Componente | Dono lógico | Pode conter treino? |
|------------|-------------|---------------------|
| `04_segmentation/train.py` | Pipeline | Sim (único ponto) |
| `10_runtime/*/adapter.py` | Runtime | Não |
| `00_common/*.ipynb` | Biblioteca | Não (funções auxiliares) |
| `00_common/bootstrap/` | Infraestrutura | Não (validação) |
| `99_system/` | Infraestrutura | Não |

---

## 6. Fluxo de trabalho recomendado

1. Preparar dados em `02_dataset`.
2. Explorar e pré-processar com notebooks em `00_common` e pastas 03–06.
3. Escolher runtime (`local_cpu`, `local_gpu`, `kaggle`).
4. Executar adapter → `train.py` → outputs.
5. Promover resultados para `07_results/experiments/<exp_id>/` (ver [experiment_standards.md](experiment_standards.md)).
6. Documentar no relatório (`08_report`) e apresentação (`09_presentation`).

---

## 7. Controlo de alterações

### 7.1 Alterações que exigem atualização de governação

- Novo runtime (ex.: RunPod, AWS).
- Novo módulo de pipeline.
- Mudança no contrato de outputs experimentais.
- Alteração de convenção de nomenclatura.

### 7.2 Alterações proibidas sem revisão

- `train_gpu.py`, `model_kaggle.py`, ou equivalentes nos runtimes.
- Paths de output diferentes por runtime sem variável de ambiente documentada.
- Código de treino copiado para notebooks de `00_common`.

---

## 8. Qualidade mínima

- Bootstrap deve passar no perfil do runtime antes de treinos longos.
- Notebooks seguem [notebook_standards.md](notebook_standards.md).
- Código Python segue [coding_standards.md](coding_standards.md).
- Documentação pública via MkDocs segue [documentation_standards.md](documentation_standards.md).

---

## 9. Migração pendente (Fase 10)

Até à migração física, o repositório pode usar nomes legados com hífen (`00-common`, `10-runtime`). A governação descreve o **estado alvo**. O mapa de renomeação será aplicado numa única fase controlada com relatório em `99_system/documentation/migration_report.md`.

---

## 10. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação — Fase 2 |
