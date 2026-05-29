# Runtimes

Ambientes de execução em `10-runtime/` (alvo: `10_runtime/`). **Não contêm lógica de treino.**

---

## Providers (Nível A)

| Provider | Pasta (alvo) | Device | Infra |
|----------|--------------|--------|-------|
| `local_cpu` | `10_runtime/local_cpu` | CPU | Docker `python:3.11-slim` |
| `local_gpu` | `10_runtime/local_gpu` | CUDA | Docker PyTorch CUDA 12.1 |
| `kaggle` | `10_runtime/kaggle` | CUDA | Kaggle Notebooks |

---

## Fluxo canónico

```bash
python 10-runtime/local-gpu/adapter.py    # preparar ambiente
python 04-segmentation/train.py           # pipeline única
```

No Kaggle: ver `launch.ipynb` em `10-runtime/kaggle/`.

---

## Adapter (alvo: `runtime_adapter.py`)

| Função | Descrição |
|--------|-----------|
| `prepare_environment()` | Define `FETAL_*` e cria outputs |
| `resolve_paths_runtime()` | Lê `config.yaml` |
| `validate_runtime()` | Pré-condições |
| `check_cuda()` | GPU — obrigatório em local_gpu/kaggle |
| `sync_outputs()` | Kaggle — copia para `/kaggle/working/output` |

---

## Configuração (`config.yaml`)

```yaml
provider: local_gpu
dataset_path: ./02_dataset
output_path: ./04_segmentation/outputs
device: cuda
```

---

## Docker

```bash
# CPU (paths atuais até Fase 10)
docker compose -f 10-runtime/local-cpu/docker-compose.yml up --build

# GPU
docker compose -f 10-runtime/local-gpu/docker-compose.yml up --build
```

---

## Ver também

- [Arquitetura de runtime](../architecture/runtime_architecture.md)
- [Bootstrap](../bootstrap/index.md)
- [API adapter](../api/adapter.md)
