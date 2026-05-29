# Pipeline de Segmentação

Localização: `04-segmentation/` (alvo: `04_segmentation/`).

**Único ponto de treino do projeto:** `train.py`.

---

## Módulos

| Ficheiro | Responsabilidade |
|----------|------------------|
| `train.py` | Loop de treino, checkpoints, `metrics.json` |
| `dataset.py` | Pares imagem/máscara, carregamento |
| `model.py` | `build_model()` — UNet MONAI |
| `config.yaml` | Épocas, batch, arquitetura |

---

## Outputs

```text
04-segmentation/outputs/
├── checkpoints/last.pt
├── logs/
└── metrics.json
```

Variável de ambiente: `FETAL_OUTPUT_PATH`.

---

## Execução

```bash
# Com adapter (recomendado)
python 10-runtime/local-gpu/adapter.py
python 04-segmentation/train.py
```

`train.py` pode invocar o adapter automaticamente se `FETAL_PROVIDER` não estiver definido.

---

## Dry-run

Sem pares no dataset, `train.py` termina com `status: dry_run` em `metrics.json` — útil para validar runtime.

---

## API

- [train](../api/train.md)
- [dataset](../api/dataset.md)
- [model](../api/model.md)
