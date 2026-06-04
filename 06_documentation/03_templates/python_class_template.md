# Template — Classe Python

**Estilo:** Google docstrings em inglês; `PascalCase` para nomes de classe.

---

## Dataclass

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatasetPaths:
    """
  Represent resolved dataset directory paths.

  Attributes:
      images_dir (Path):
          Directory containing input images.
      masks_dir (Path):
          Directory containing mask images.
      extensions (tuple[str, ...]):
          Allowed file extensions for pairing.
  """

    images_dir: Path
    masks_dir: Path
    extensions: tuple[str, ...]
```

---

## Classe com comportamento

```python
class RuntimeAdapter:
    """
    Prepare and validate execution environment for a single provider.

    This class does not implement training logic. It only sets environment
    variables consumed by ``04_segmentation/train.py``.
    """

    def __init__(self, config_path: Path, project_root: Path) -> None:
        """
        Initialize the adapter.

        Args:
            config_path (Path):
                Path to runtime config.yaml.
            project_root (Path):
                Repository root directory.
        """
        self._config_path = config_path
        self._project_root = project_root

    def prepare_environment(self) -> ResolvedRuntimePaths:
        """
        Create output directories and publish FETAL_* variables.

        Returns:
            ResolvedRuntimePaths:
                Resolved paths after applying configuration.
        """
        ...
```

---

## Enum

```python
from enum import Enum


class Level(str, Enum):
    """Bootstrap check severity level."""

    OK = "OK"
    WARN = "WARN"
    FAIL = "FAIL"
```

---

## Checklist

- [ ] Docstring de classe descreve responsabilidade única
- [ ] Métodos públicos com docstrings completas
- [ ] Métodos privados com `_prefix`; docstring opcional

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
