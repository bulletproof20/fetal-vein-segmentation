# Notebooks — `00_common`

Biblioteca interativa de funções auxiliares. **Markdown em português**; funções novas em **inglês**.

---

## Inventário (alvo Nível A)

| Notebook (alvo) | Estado | Tema |
|-----------------|--------|------|
| `01_functions.ipynb` | Preenchido | Metadados, conversões, ROI |
| `02_filters.ipynb` | Preenchido | Filtros |
| `03_morphology.ipynb` | Preenchido | Morfologia |
| `04_metrics.ipynb` | **Vazio (WIP)** | Métricas |
| `05_visualization.ipynb` | Preenchido | Visualização |
| `06_uploading.ipynb` | Preenchido | Carregamento de dados |
| `07_training_provider.ipynb` | Preenchido | Provider de runtime (sem treino) |

Nomes atuais no disco: `01-functions.ipynb`, etc. (hífen).

---

## Dependências entre notebooks

```text
01_functions ──► 06_uploading (%run)
              └──► 03_morphology (opcional)
              └──► 05_visualization (opcional)
07_training_provider ──► train.py (orquestração apenas)
```

---

## Regras

- Seguir [notebook_template.md](../templates/notebook_template.md)
- **Não** duplicar lógica de `train.py`
- Secções: objetivo, pré-requisitos, inputs, outputs, configuração, implementação, validação

---

## Kaggle

`10-runtime/kaggle/launch.ipynb` — prepara adapter e executa `train.py`.

---

## Ver também

- [Padrões de notebooks](../governance/notebook_standards.md)
- [Training provider](../pipeline/index.md) (conceito)
