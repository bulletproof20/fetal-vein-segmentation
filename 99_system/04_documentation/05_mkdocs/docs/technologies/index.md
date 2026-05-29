# Stack Tecnológica

Resumo das tecnologias do projeto. Documentação alargada em [architecture/technology_stack.md](../architecture/technology_stack.md).

---

## Linguagem e ambiente

| Tecnologia | Versão / notas | Uso no projeto |
|------------|----------------|----------------|
| **Python** | 3.11 | Pipeline, bootstrap, adapters, notebooks |
| **Jupyter** | JupyterLab 4.x | Exploração em `00-common`; Docker CPU/GPU |
| **Git** | — | Versionamento; GitHub para entrega |

---

## Imagem e ciência de dados

| Tecnologia | Uso |
|------------|-----|
| **NumPy** | Arrays, pré-processamento |
| **SciPy** | Operações científicas |
| **pandas** | Tabelas e estatísticas |
| **Matplotlib** | Visualização |
| **Pillow** | I/O de imagens |
| **scikit-image** | Processamento de imagem |
| **PyYAML** | Configuração pipeline e runtime |

*Excluído por decisão de projeto:* OpenCV, seaborn, scikit-learn.

---

## Deep learning

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **PyTorch** | ≥ 2.4.1 | Treino, CUDA |
| **MONAI** | 1.5.x | UNet em `model.py` |
| **TorchMetrics** | ≥ 1.4 | Métricas (expansão futura) |

Imagem Docker GPU: `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime`.

---

## Infraestrutura de execução

| Tecnologia | Uso |
|------------|-----|
| **Docker** | Ambientes `local_cpu` e `local_gpu` |
| **Docker Compose** | Orquestração por runtime |
| **NVIDIA Container Toolkit** | GPU local |
| **Kaggle Notebooks** | Runtime cloud com GPU |

---

## Documentação

| Tecnologia | Uso |
|------------|-----|
| **MkDocs** | Site estático desta documentação |
| **Material for MkDocs** | Tema e navegação |
| **mkdocstrings** | API a partir de docstrings Python |

---

## GitHub

| Aspeto | Uso previsto |
|--------|--------------|
| Repositório remoto | Entrega e backup |
| GitHub Actions | Opcional — `99_system/03_automation` (futuro) |
| GitHub Pages | Opcional — deploy de `mkdocs build` |

---

## Matriz runtime × stack

| Capability | local_cpu | local_gpu | kaggle |
|------------|-----------|-----------|--------|
| JupyterLab | Sim | Sim | Plataforma |
| PyTorch | Opcional (WARN) | Sim | Sim |
| MONAI | Opcional (WARN) | Sim | Sim |
| CUDA | Não | Sim | Sim |
| Docker | Sim | Sim | N/A |

---

## Ver também

- [Runtimes](../runtimes/index.md)
- [Bootstrap](../bootstrap/index.md)
- [Pipeline](../pipeline/index.md)
- [API Reference](../api/index.md)
