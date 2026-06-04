# Template — Função Python

**Estilo:** Google docstrings em inglês.

---

## Função simples

```python
def load_dataset(dataset_path: str) -> dict[str, Any]:
    """
    Load dataset from disk.

    Args:
        dataset_path (str):
            Dataset root directory.

    Returns:
        dict[str, Any]:
            Dataset metadata including sample count and paths.

    Raises:
        FileNotFoundError:
            If dataset does not exist.
    """
```

---

## Função sem retorno

```python
def apply_runtime_env(paths: ResolvedRuntimePaths) -> None:
    """
    Publish environment variables for the canonical training pipeline.

    Args:
        paths (ResolvedRuntimePaths):
            Resolved runtime paths from config.yaml.
    """
```

---

## Função com múltiplos raises

```python
def build_model(cfg: dict[str, Any]) -> Any:
    """
    Build MONAI UNet from pipeline configuration.

    Args:
        cfg (dict[str, Any]):
            Pipeline config dictionary (model section).

    Returns:
        torch.nn.Module:
            Initialized UNet model.

    Raises:
        RuntimeError:
            If MONAI or PyTorch is not installed.
        KeyError:
            If required model keys are missing from cfg.
    """
```

---

## Propriedades e métodos de classe

```python
class DatasetLoader:
    """Load and iterate paired image-mask samples."""

    def __init__(self, images_dir: Path, masks_dir: Path) -> None:
        """
        Initialize the loader.

        Args:
            images_dir (Path):
                Directory containing input images.
            masks_dir (Path):
                Directory containing mask images.
        """
```

---

## Regras

- Primeira linha: verbo no imperativo («Load», «Build», «Validate»).
- Tipos nos `Args` alinhados com type hints.
- Não documentar `Returns` se a função retorna `None` (usar docstring curta sem secção Returns).

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
