# API Reference

Documentação gerada com [mkdocstrings](https://mkdocstrings.github.io/) a partir do código Python.

!!! info "Docstrings em evolução"
    O padrão oficial é **Google Style em inglês**. Módulos podem ainda ter docstrings curtas até à Fase 10.

---

## Pipeline (`04-segmentation`)

| Módulo | Descrição |
|--------|-----------|
| [train](train.md) | Entry point de treino |
| [dataset](dataset.md) | Dataset e carregamento |
| [model](model.md) | Construção do modelo |

---

## Bootstrap (`00-common/bootstrap`)

| Módulo | Descrição |
|--------|-----------|
| [bootstrap](bootstrap.md) | Script principal |
| [config](config.md) | Configuração do projeto |
| [checks](checks.md) | Verificações |

---

## Runtime

| Módulo | Descrição |
|--------|-----------|
| [runtime_paths](runtime_paths.md) | Paths e variáveis `FETAL_*` |
| [adapter](adapter.md) | Adapter local_cpu (exemplo) |

---

## Paths de importação

O `mkdocs.yml` inclui:

```text
../../../04-segmentation
../../../00-common/bootstrap
../../../10-runtime/local-cpu
```
