# Padrões de Jupyter Notebooks

**Versão:** 1.0  
**Markdown:** português  
**Código nas células:** inglês (funções novas)

---

## 1. Âmbito

Notebooks em:

- `00_common/*.ipynb`
- `10_runtime/kaggle/launch.ipynb` (e futuros notebooks de runtime)
- Notebooks exploratórios em `01_literature_review` … `06_evaluation` (quando existirem)

Template obrigatório: [../templates/notebook_template.md](../templates/notebook_template.md).

---

## 2. Nomenclatura de ficheiros

`NN_topic.ipynb` em `snake_case` — ver [naming_conventions.md](naming_conventions.md).

Exemplo: `01_functions.ipynb`, `07_training_provider.ipynb`.

---

## 3. Estrutura obrigatória de células

Ordem recomendada (ajustar com `# N/A` se não aplicável):

| # | Secção | Tipo | Conteúdo |
|---|--------|------|----------|
| 1 | Título e objetivo | Markdown PT | O que o notebook faz |
| 2 | Contexto no projeto | Markdown PT | Onde encaixa no pipeline |
| 3 | Pré-requisitos | Markdown PT | Bibliotecas, notebooks anteriores |
| 4 | Inputs | Markdown PT | Dados, paths, variáveis de ambiente |
| 5 | Outputs esperados | Markdown PT | Ficheiros, figuras, métricas |
| 6 | Configuração | Code | Imports, constantes, seeds |
| 7 | Implementação | Code + Markdown | Secções por tema |
| 8 | Validação / smoke test | Code | Assert ou visualização mínima |
| 9 | Referências | Markdown PT | Links, papers (opcional) |

---

## 4. Markdown (português)

### 4.1 Títulos

```markdown
# 01 — Funções auxiliares

Utilitários reutilizáveis para metadados, validação e conversões.
```

- Nível 1: uma vez por notebook.
- Níveis 2–3: secções de implementação.
- Evitar níveis 4+ excessivos.

### 4.2 Listas e ênfase

- Listas para pré-requisitos e outputs.
- **Negrito** para termos definidos na primeira ocorrência.
- `` `código` `` para paths, funções e variáveis.

---

## 5. Células de código

### 5.1 Idioma

| Elemento | Idioma |
|----------|--------|
| Nomes de funções novas | Inglês |
| Docstrings em funções | Inglês (Google Style) |
| Comentários inline | Inglês (técnicos) |
| Strings de log/print para relatório | Português aceite |

### 5.2 Organização

- Uma responsabilidade principal por célula quando possível.
- Funções relacionadas na mesma célula se forem curtas (<30 linhas).
- Evitar células com centenas de linhas — dividir por secção markdown.

### 5.3 Imports

Primeira célula de código após «Configuração»:

```python
import numpy as np
# third-party
# local (avoid sys.path hacks in notebooks; use documented PROJECT_ROOT)
```

---

## 6. Notebooks sem lógica de treino

`07_training_provider` e equivalentes:

- Apenas orquestração de runtime (`get_provider`, `export_dataset`, …).
- Execução de treino: **sempre** delegar a `04_segmentation/train.py` numa célula separada com comentário explícito.

```python
# Training is executed only via the canonical pipeline (do not duplicate training logic here).
# !python 04_segmentation/train.py
```

---

## 7. Reprodutibilidade

Cada notebook deve declarar:

| Campo | Onde |
|-------|------|
| `random seed` | Célula configuração |
| Versão Python / runtime | Markdown pré-requisitos |
| Dataset path | Markdown inputs (`02_dataset` ou env) |

---

## 8. Metadados de experimento (opcional mas recomendado)

Para notebooks que geram resultados:

```markdown
## Experimento

| Campo | Valor |
|-------|-------|
| ID | `exp_20260529_001` |
| Runtime | `local_gpu` |
| Pipeline | `04_segmentation/train.py` |
```

Alinhar com [experiment_standards.md](experiment_standards.md).

---

## 9. Outputs e commits

- Não commitar outputs pesados dentro do notebook (clear outputs antes de commit se política do grupo o exigir).
- Figuras exportadas para `07_results/` ou subpastas de módulo, não embutidas como único artefacto.

---

## 10. Notebooks vazios ou WIP

`04_metrics.ipynb` e similares:

- Primeira célula markdown com estado **WIP** e data prevista.
- Não deixar ficheiro 0 bytes sem documentação.

---

## 11. Kernel e dependências

- Documentar no README do runtime ou em `technology_stack.md` se GPU é necessária.
- Kaggle: referenciar `10_runtime/kaggle/requirements.txt`.

---

## 12. Checklist antes de entregar

- [ ] Template de secções preenchido
- [ ] Título e objetivo em português
- [ ] Funções novas em inglês com docstring
- [ ] Sem lógica de treino duplicada
- [ ] Inputs/outputs documentados
- [ ] Smoke test ou validação mínima

---

## 13. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação — Fase 2 |
