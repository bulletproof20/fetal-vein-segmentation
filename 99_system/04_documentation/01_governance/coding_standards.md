# Padrões de Código Python

**Versão:** 1.0  
**Idioma do código:** inglês  
**Docstrings:** Google Style (inglês)

---

## 1. Âmbito

Aplica-se a todos os ficheiros `.py` em:

- `00_common/` (incluindo `bootstrap/`)
- `04_segmentation/`
- `10_runtime/*/`
- `99_system/tools/` (quando existir)

**Não** aplica regras de estrutura de células a notebooks — ver [notebook_standards.md](notebook_standards.md).

---

## 2. Estilo e formatação

| Aspeto | Regra |
|--------|-------|
| PEP 8 | Base obrigatória |
| Comprimento de linha | 88–100 caracteres (preferir 88 se formatador automático) |
| Imports | `stdlib` → terceiros → locais; uma linha em branco entre grupos |
| `from __future__ import annotations` | Obrigatório em módulos novos |
| Type hints | Obrigatórios em funções públicas |
| f-strings | Preferidas para formatação |

---

## 3. Nomenclatura

Ver [naming_conventions.md](naming_conventions.md).

```python
# Good
def load_dataset(dataset_path: Path) -> dict[str, Any]:
    ...

class DatasetLoader:
    ...

DEFAULT_BATCH_SIZE = 2
```

```python
# Avoid in new code
def analisar_metadados(img):  # legacy notebook-only; do not copy to .py modules
    ...
```

---

## 4. Docstrings (Google Style)

Todas as funções e classes **públicas** devem ter docstring em inglês.

Ver template: [../templates/python_function_template.md](../templates/python_function_template.md).

Regras:

- Primeira linha: resumo imperativo («Load dataset from disk.»).
- `Args`, `Returns`, `Raises` quando aplicável.
- Sem repetir o nome da função no início.

---

## 5. Comentários

### 5.1 Comentários de secção

Em módulos longos (>150 linhas ou >5 blocos lógicos):

```python
# ==================================================
# Dataset Loading
# ==================================================
```

### 5.2 Comentários inline

Explicam **porquê**, não **o quê**:

```python
# Normalize to [0, 1] before MONAI loss
array = array / 255.0
```

Evitar:

```python
# increment i
i += 1
```

---

## 6. Estrutura de módulos

Ordem recomendada:

1. Docstring de módulo (opcional, uma linha)
2. `from __future__ import annotations`
3. Imports
4. Constantes
5. Classes
6. Funções públicas
7. Funções privadas (`_prefix`)
8. `if __name__ == "__main__":`

---

## 7. Imports e layout (sem `src/fetal_vein`)

Decisão aprovada: **não** usar pacote instalável `src/fetal_vein`.

### 7.1 Pipeline `04_segmentation`

Imports locais entre módulos da mesma pasta:

```python
from dataset import resolve_dataset_paths
from model import build_model
```

### 7.2 Runtimes

Adapters podem adicionar `00_common` ao `sys.path` **apenas** no entrypoint/adapter, não na pipeline.

### 7.3 Bootstrap

Executado com `00_common/bootstrap` no `sys.path` (como script) ou após migração com caminho documentado.

---

## 8. Configuração

| Tipo | Formato | Local |
|------|---------|-------|
| Pipeline | YAML | `04_segmentation/config.yaml` |
| Runtime | YAML | `10_runtime/<provider>/config.yaml` |
| Constantes Python | `.py` opcional | `00_common/constants.py` (futuro) |

Não hardcodar paths absolutos exceto deteção Kaggle (`/kaggle/input`).

---

## 9. Variáveis de ambiente

Prefixo do projeto: `FETAL_` para runtime/pipeline; `BOOTSTRAP_` para bootstrap.

| Variável | Uso |
|----------|-----|
| `PROJECT_ROOT` | Raiz do repositório |
| `FETAL_DATASET_PATH` | Dataset |
| `FETAL_OUTPUT_PATH` | Outputs de treino |
| `FETAL_DEVICE` | `cpu` ou `cuda` |
| `FETAL_PROVIDER` | `local_cpu`, `local_gpu`, `kaggle` |
| `BOOTSTRAP_PROFILE` | Perfil de validação |

---

## 10. Erros e logging

- Usar exceções específicas (`FileNotFoundError`, `RuntimeError` com mensagem clara).
- `print()` aceitável em scripts CLI (`train.py`, bootstrap); preferir `logging` em módulos reutilizáveis futuros.
- Mensagens de erro para utilizador: podem ser em português no bootstrap; inglês na pipeline técnica.

---

## 11. Testes (futuro)

Quando existirem, em `99_system/tests/`:

- Nomes: `test_<module>_<behavior>.py`
- Funções: `test_returns_empty_list_when_dataset_missing`

---

## 12. Proibições

| Proibido | Motivo |
|----------|--------|
| Lógica de treino em `10_runtime` | Separação pipeline/runtime |
| Secrets em código | Usar env / Kaggle secrets |
| `import *` | Legibilidade |
| Código morto comentado em bloco | Usar git history |

---

## 13. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação — Fase 2 |
