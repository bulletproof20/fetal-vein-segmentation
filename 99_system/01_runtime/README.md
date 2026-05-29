# Runtime — Ambientes de execução

Separação entre **pipeline científica** (`04_segmentation/train.py`) e **runtime** (este diretório).

## Providers

| Provider | Uso |
|----------|-----|
| `local_cpu` | Desenvolvimento local / Jupyter (CPU) |
| `local_gpu` | CUDA + MONAI |
| `kaggle` | Kaggle Notebooks |

## Comandos

```bash
python 99_system/01_runtime/local_cpu/adapter.py
python 04_segmentation/train.py

docker compose -f 99_system/01_runtime/local_cpu/docker-compose.yml up --build
```

`entrypoint.sh` é usado pelas imagens Docker e invoca o adapter + `99_system/02_bootstrap/bootstrap.py`.
