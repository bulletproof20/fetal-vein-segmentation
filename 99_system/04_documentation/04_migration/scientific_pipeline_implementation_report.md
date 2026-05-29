# Relatório — Implementação do núcleo científico

**Data:** 2026-05-29  
**Âmbito:** `04_segmentation` + ajustes mínimos de paths em `99_system/01_runtime` (sem alteração de estrutura de diretórios)

## Resumo

O núcleo científico foi alinhado com a referência da docente (`FetalVeinSegmentationUS.ipynb`), corrigindo fragilidades metodológicas (normalização da label) e mantendo `train.py` como **único ponto de treino**.

## Ficheiros modificados

| Ficheiro | Alteração |
|----------|-----------|
| `04_segmentation/dataset.py` | `labels/` oficial, fallback `masks/`, binarização GT, split YAML, logs |
| `04_segmentation/config.yaml` | Hiperparâmetros científicos completos |
| `04_segmentation/model.py` | UNet 5 níveis (256), validação strides/canais |
| `04_segmentation/train.py` | Refatoração: DiceLoss, DiceMetric, cosine, best/last, teste, export, avaliação |
| `99_system/01_runtime/local_cpu/config.yaml` | `masks_dir` → `labels` |
| `99_system/01_runtime/local_gpu/config.yaml` | idem |
| `99_system/01_runtime/kaggle/config.yaml` | idem |
| `99_system/01_runtime/kaggle/adapter.py` | Fallback `labels/` em `/kaggle/input` |
| `99_system/01_runtime/runtime_paths.py` | Default `labels`, fallback `masks` |
| `99_system/02_bootstrap/config.py` | Default GT `labels` |
| `99_system/02_bootstrap/checks.py` | Mensagens `labels/` |

## Requisitos implementados (checklist)

1. **Dataset / GT** — `labels/` prioritário; fallback; falha explícita se &lt; min_samples  
2. **Binarização** — só imagem normalizada; label `{0,1}`  
3. **Split** — train/val/test via YAML (`counts` 110/20/resto por defeito)  
4. **DiceLoss** — MONAI, sigmoid + squared_pred + smooth  
5. **DiceMetric** — validação por época  
6. **Checkpoints** — `best.pt` (melhor Dice val), `last.pt`  
7. **CosineAnnealingLR** — configurável  
8. **config.yaml** — estrutura expandida  
9. **UNet** — canais `[16,32,64,128,256]`  
10. **train.py** — funções `train_epoch`, `validate`, `run_test`, `save_checkpoint`, `export_predictions`  
11. **Inferência** — teste com `best.pt`  
12. **Export** — `outputs/predictions/*.png`  
13. **Avaliação** — `06_evaluation/{metrics,plots,tables}` + espelho em `07_results/metrics`  
14. **Kaggle** — paths `labels/` nos YAML/adapters  
15. **Reprodutibilidade** — `set_determinism` + seeds  

## Execução

```bash
# Local (após adapter ou env)
python 99_system/01_runtime/local_gpu/adapter.py
python 04_segmentation/train.py

# Kaggle
# launch.ipynb → adapter → train.py → sync_outputs
```

## Riscos remanescentes

- Treino 150 épocas requer GPU (Kaggle recomendado).  
- Dataset Kaggle deve publicar `images/` + `labels/`.  
- `torch.load(..., weights_only=False)` — necessário para checkpoints completos.  
- Primeira execução longa; testar com `training.epochs: 2` no YAML para smoke test.

## Arquitetura

Nenhuma pasta criada ou movida. Runtimes sem lógica de treino duplicada.
