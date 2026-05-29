# 99_system — Infraestrutura do projeto

Toda a infraestrutura (runtime, bootstrap, ferramentas, documentação, contexto académico) vive aqui. A pipeline científica está nas pastas numeradas `00_common` … `09_presentation` na raiz do repositório.

## Estrutura

| Pasta | Função |
|-------|--------|
| `01_runtime/` | Adapters (`local_cpu`, `local_gpu`, `kaggle`), Docker, `entrypoint.sh` |
| `02_bootstrap/` | Validação e preparação do ambiente |
| `03_tools/` | Scripts de manutenção, sync MkDocs, migração |
| `04_documentation/` | Governação, arquitetura, templates, migração, MkDocs |
| `05_academic_context/` | Material UC (não usado pelo código) |

## Comandos rápidos

```bash
python 99_system/02_bootstrap/bootstrap.py --no-strict
python 99_system/01_runtime/local_cpu/adapter.py
python 04_segmentation/train.py
```

## Documentação (MkDocs)

```bash
cd 99_system/04_documentation/05_mkdocs
pip install -r requirements_mkdocs.txt
python ../../03_tools/sync_source_docs.py
mkdocs serve
```

Relatório de consolidação: `04_documentation/04_migration/architecture_consolidation_report.md`
