# Template — Módulo Python

Use este template ao criar um novo ficheiro `.py`.  
**Idioma:** inglês (código e docstrings).  
**Convenções:** [coding_standards.md](../governance/coding_standards.md).

---

## Estrutura

```python
"""One-line summary of the module purpose."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# ==================================================
# Constants
# ==================================================

DEFAULT_BATCH_SIZE = 2
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", Path.cwd())).resolve()


# ==================================================
# Public API
# ==================================================

def example_public_function(path: Path) -> dict[str, Any]:
    """
    Short imperative summary.

    Args:
        path (Path):
            Description of the argument.

    Returns:
        dict[str, Any]:
            Description of the return value.

    Raises:
        FileNotFoundError:
            When the path does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    return {"status": "ok"}


# ==================================================
# Private helpers
# ==================================================

def _example_private_helper() -> None:
    """Internal helper — not part of public API."""
    pass


if __name__ == "__main__":
    print(example_public_function(PROJECT_ROOT))
```

---

## Checklist

- [ ] `from __future__ import annotations`
- [ ] Type hints em funções públicas
- [ ] Google docstring em funções/classes públicas
- [ ] Sem lógica de treino fora de `04_segmentation/train.py`
- [ ] Paths via env ou `runtime_paths`, não hardcoded por cloud

---

## Revisão do template

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
