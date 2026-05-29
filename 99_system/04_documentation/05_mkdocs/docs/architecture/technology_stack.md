# Stack Tecnológica

**Versão:** 1.0

---

## 1. Resumo

| Camada | Tecnologias |
|--------|-------------|
| Linguagem | Python 3.11 |
| Notebooks | JupyterLab 4.x |
| Imagem clássica | NumPy, SciPy, scikit-image, Pillow, Matplotlib |
| Deep learning | PyTorch ≥2.4.1, MONAI 1.5.x, TorchMetrics |
| Configuração | YAML (PyYAML) |
| Contentores | Docker, Docker Compose |
| Cloud | Kaggle Notebooks (GPU) |
| Documentação (alvo) | MkDocs Material, mkdocstrings |
| Controlo de versões | Git |

**Excluído por decisão de projeto:** OpenCV, seaborn, scikit-learn (onde aplicável ao TP).

---

## 2. Python e ambiente

| Componente | Versão / notas |
|------------|----------------|
| Python | 3.11 (imagens Docker e desenvolvimento local) |
| pip | Atualizado no build Docker |

### 2.1 Ficheiros de dependências

| Ficheiro | Âmbito |
|----------|--------|
| `requirements.txt` (raiz) | Desenvolvimento local completo |
| `10_runtime/local_cpu/requirements.txt` | CPU + Jupyter (sem torch) |
| `10_runtime/local_gpu/requirements.txt` | GPU + Jupyter + MONAI |
| `10_runtime/kaggle/requirements.txt` | Kaggle kernel |

Risco: **drift** entre ficheiros — governação recomenda tabela de versões pinada em `99_system` (futuro).

---

## 3. Deep learning

| Biblioteca | Função no projeto |
|------------|-------------------|
| PyTorch | Tensores, training loop, CUDA |
| MONAI | UNet (`monai.networks.nets.UNet`) |
| TorchMetrics | Métricas (reservado para expansão) |

### 3.1 Imagens base Docker

| Runtime | Imagem |
|---------|--------|
| `local_cpu` | `python:3.11-slim-bookworm` |
| `local_gpu` | `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime` |

### 3.2 Requisitos GPU

- NVIDIA Container Toolkit (Docker local).
- CUDA disponível no Kaggle para perfil `kaggle`.

---

## 4. Jupyter

| Pacote | Uso |
|--------|-----|
| JupyterLab | Ambiente interativo nos Docker |
| ipywidgets | UI em notebooks |
| notebook | Compatibilidade |

Porta default: `8888`, token configurável via `JUPYTER_TOKEN`.

---

## 5. Infraestrutura

| Ferramenta | Uso |
|------------|-----|
| Docker | `local_cpu`, `local_gpu` |
| Docker Compose | Orquestração por runtime |
| Bash | `entrypoint.sh` |
| Git | Versionamento |

---

## 6. Documentação (Fase 5 — planeado)

| Ferramenta | Função |
|------------|--------|
| MkDocs | Site estático |
| Material for MkDocs | Tema |
| mkdocstrings | API a partir de docstrings Google Style |

Dependências a adicionar em `99_system/documentation/mkdocs/requirements-docs.txt` (futuro).

---

## 7. Bootstrap

Módulos em `00_common/bootstrap/`:

- Validação de estrutura de pastas
- Imports de dependências por perfil
- Validação de adapters
- Verificação CUDA/MONAI condicional

Executável: `python 00_common/bootstrap/bootstrap.py`.

---

## 8. Armazenamento e formatos

| Tipo | Formato |
|------|---------|
| Imagens | PNG, JPEG, TIFF, BMP |
| Máscaras | Idem |
| Checkpoints | PyTorch `.pt` |
| Métricas | JSON |
| Config | YAML |
| Manifesto de experiência | YAML |

---

## 9. Matriz runtime × stack

| Capability | local_cpu | local_gpu | kaggle |
|------------|-----------|-----------|--------|
| JupyterLab | Sim | Sim | Sim (platform) |
| PyTorch | Não (WARN) | Sim | Sim |
| MONAI | Não (WARN) | Sim | Sim |
| CUDA | Não | Sim | Sim |
| Docker | Sim | Sim | N/A |

---

## 10. Ferramentas de desenvolvimento (futuro)

Recomendadas em `99_system` — não obrigatórias na Fase 2:

| Ferramenta | Função |
|------------|--------|
| ruff | Lint |
| black | Formatação |
| pre-commit | Hooks |

---

## 11. Documentos relacionados

- [runtime_architecture.md](runtime_architecture.md)
- [../governance/coding_standards.md](../governance/coding_standards.md)

---

## 12. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação — Fase 2 |
