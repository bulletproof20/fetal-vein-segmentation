# Bootstrap

Validação e preparação do ambiente em `00-common/bootstrap/` (alvo: `00_common/bootstrap/`).

---

## Entry point

```bash
python 00-common/bootstrap/bootstrap.py
```

Opções: `--no-strict`, `--require-gpu`, `--skip-dirs`.

---

## Perfis (`BOOTSTRAP_PROFILE`)

| Perfil (alvo) | Strict default | GPU stack |
|---------------|----------------|-----------|
| `local_cpu` | Não | WARN se em falta |
| `local_gpu` | Sim | FAIL se em falta |
| `kaggle` | Sim | FAIL se em falta |

Aliases legados: `cpu` → `local_cpu`, `gpu` → `local_gpu`.

---

## Verificações principais

1. Estrutura de pastas (`00-common`, `10-runtime`, `04-segmentation`, `02-dataset`)
2. Runtimes e adapters
3. Pipeline de segmentação
4. Dataset (imagens/máscaras)
5. Permissões de escrita em outputs
6. Dependências Python por perfil
7. JupyterLab (perfil local)
8. Notebooks `00-common`

---

## Módulos

| Ficheiro | Função |
|----------|--------|
| `bootstrap.py` | Orquestração |
| `config.py` | `ProjectConfig`, paths |
| `checks.py` | Verificações individuais |

---

## Integração Docker

`10-runtime/entrypoint.sh` executa o adapter e depois `bootstrap.py` antes do JupyterLab.

---

## API

- [bootstrap](../api/bootstrap.md)
- [config](../api/config.md)
- [checks](../api/checks.md)
