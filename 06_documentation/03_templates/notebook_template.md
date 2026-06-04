# Template — Jupyter Notebook

**Obrigatório** para todos os notebooks do projeto.  
**Markdown:** português · **Código:** inglês (funções novas)

Copiar secções abaixo como células markdown/code na ordem indicada.

---

## 1. Título e objetivo

```markdown
# NN — Título do notebook

## Objetivo

Descrever em 2–4 frases o propósito deste notebook no trabalho prático.

## Contexto no projeto

- **Módulo:** `00_common` / `06_evaluation` / …
- **Depende de:** `01_functions.ipynb`, dataset em `02_dataset`, …
- **Alimenta:** `04_segmentation`, `07_results`, …
```

---

## 2. Pré-requisitos

```markdown
## Pré-requisitos

| Item | Detalhe |
|------|---------|
| Python | 3.11 |
| Runtime | `local_cpu` / `local_gpu` / `kaggle` |
| Bibliotecas | numpy, … |
| Dados | `02_dataset/images`, `02_dataset/masks` |
```

---

## 3. Inputs e outputs

```markdown
## Inputs

- Caminho do dataset: `02_dataset` ou variável `FETAL_DATASET_PATH`
- Ficheiros de configuração: (se aplicável)

## Outputs esperados

- Figuras em: `07_results/figures/` ou `…/experiments/<exp_id>/figures/`
- Métricas em: (caminho)
- **Não** duplicar artefactos já gerados por `train.py` sem documentar
```

---

## 4. Experimento (se aplicável)

```markdown
## Experimento

| Campo | Valor |
|-------|-------|
| ID | `exp_YYYYMMDD_NNN` |
| Pipeline | `04_segmentation/train.py` |
| Runtime | `local_gpu` |
```

---

## 5. Configuração (célula code)

```python
# ==================================================
# Configuration
# ==================================================

import os
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", Path.cwd())).resolve()
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
```

---

## 6. Implementação

```markdown
## Nome da secção

Descrição em português do que a próxima célula faz.
```

```python
def example_function(image: np.ndarray) -> np.ndarray:
    """
    Short summary in English.

    Args:
        image (np.ndarray):
            Input grayscale or RGB image.

    Returns:
        np.ndarray:
            Processed image.
    """
    return image
```

---

## 7. Treino (apenas orquestração)

Se este notebook iniciar treino:

```markdown
## Execução da pipeline

O treino é executado **apenas** pelo script canónico. Não implementar loops de treino neste notebook.
```

```python
# !python 04_segmentation/train.py
```

---

## 8. Validação

```markdown
## Validação

Smoke test ou visualização mínima para confirmar que os outputs foram gerados.
```

```python
# Example assertion
assert PROJECT_ROOT.exists()
```

---

## 9. Referências (opcional)

```markdown
## Referências

- Autor et al. (ano) — título
- Documentação: [experiment_standards.md](../governance/experiment_standards.md)
```

---

## Checklist final

- [ ] Todas as secções 1–8 preenchidas ou marcadas N/A
- [ ] Markdown em português
- [ ] Funções novas em inglês com Google docstring
- [ ] Sem `train_*` duplicado no notebook
- [ ] Outputs documentados

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
