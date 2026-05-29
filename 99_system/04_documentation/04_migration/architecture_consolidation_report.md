# Architecture Consolidation Report

**Data:** 2026-05-29  
**Estado:** Concluída (estrutura final para desenvolvimento científico)

## Resumo

Consolidação definitiva da arquitetura: pipeline científica em `00_common` … `09_presentation`; infraestrutura centralizada em `99_system/`; remoção conceptual de `10_runtime` e `10_docker` como pastas de topo.

## Estrutura final

```text
fetal_vein_segmentation/
├── 00_common/
├── 01_literature_review/
├── 02_dataset/
├── 03_preprocessing/
├── 04_segmentation/          # train.py — pipeline única
├── 05_postprocessing/
├── 06_evaluation/
├── 07_results/
├── 08_report/
├── 09_presentation/
├── 99_system/
│   ├── 01_runtime/
│   │   ├── local_cpu/
│   │   ├── local_gpu/
│   │   ├── kaggle/
│   │   ├── docker/
│   │   ├── entrypoint.sh
│   │   └── runtime_paths.py
│   ├── 02_bootstrap/
│   ├── 03_tools/
│   ├── 04_documentation/
│   │   ├── 01_governance/
│   │   ├── 02_architecture/
│   │   ├── 03_templates/
│   │   ├── 04_migration/
│   │   └── 05_mkdocs/
│   └── 05_academic_context/
│       ├── 01_assignment/
│       ├── 02_worksheets/
│       └── 03_course_material/
├── LICENSE
├── README.md
└── requirements.txt
```

## Movimentos principais

| Origem | Destino |
|--------|---------|
| `00-common/` | `00_common/` |
| `00-common/bootstrap/` | `99_system/02_bootstrap/` |
| `00-common/runtime_paths.py` | `99_system/01_runtime/runtime_paths.py` |
| `10-runtime/*` | `99_system/01_runtime/` (`local-cpu` → `local_cpu`, etc.) |
| `10-docker/*` | `99_system/01_runtime/docker/` |
| `scripts/*` | `99_system/03_tools/` |
| `99_system/documentation/` | `99_system/04_documentation/01_*` … |
| `99_system/05_documentation/05_mkdocs/` | `99_system/04_documentation/05_mkdocs/` |
| Worksheets UC (externo) | `99_system/05_academic_context/02_worksheets/` |

## Referências atualizadas (código)

- `99_system/02_bootstrap/config.py`, `checks.py`
- `99_system/01_runtime/runtime_paths.py`, `entrypoint.sh`, adapters
- `04_segmentation/train.py`, `dataset.py`
- Dockerfiles / `docker-compose.yml` (contexto = raiz do repo)
- Notebooks `00_common`, `kaggle/launch.ipynb`
- `99_system/03_tools/sync_source_docs.py`, `gen_notebooks.py`

## MkDocs

- Caminho canónico: `99_system/04_documentation/05_mkdocs/`
- Sync: `python 99_system/03_tools/sync_source_docs.py`
- Serve: `cd 99_system/04_documentation/05_mkdocs && pip install -r requirements_mkdocs.txt && python ../../03_tools/sync_source_docs.py && mkdocs serve`
- Nova navegação: **Academic Context** (Assignment, Worksheets, Course Material)

## Comandos operacionais

```bash
# Bootstrap (host)
python 99_system/02_bootstrap/bootstrap.py --no-strict

# Adapter CPU
python 99_system/01_runtime/local_cpu/adapter.py

# Treino
python 04_segmentation/train.py

# Docker CPU (na raiz do repo)
docker compose -f 99_system/01_runtime/local_cpu/docker-compose.yml up --build
```

## Impactos / pendências

1. **Pastas legadas vazias** (`10-runtime/`, `10-docker/`, `scripts/`) podem persistir no OneDrive por bloqueio de permissões — estão no `.gitignore`; apagar manualmente quando o sync permitir.
2. **`99_system/05_documentation/`** — duplicado legado; usar apenas `04_documentation/`.
3. **Worksheets** — copiar para `02_worksheets/` se a pasta externa existir; não são dependência do código.
4. **Assignment / course material** — READMEs criados; preencher com PDFs oficiais da UC.

## Próximo foco

Desenvolvimento exclusivo da pipeline científica: dataset → pré-processamento → segmentação → pós-processamento → avaliação → resultados → relatório → apresentação.
