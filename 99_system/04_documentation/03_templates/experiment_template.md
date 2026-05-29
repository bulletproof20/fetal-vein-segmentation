# Template — Experiência Experimental

Criar uma pasta por experiência:

```text
07_results/experiments/exp_YYYYMMDD_NNN/
```

Ver [experiment_standards.md](../governance/experiment_standards.md).

---

## 1. Identificação

| Campo | Valor |
|-------|-------|
| **experiment_id** | `exp_20260529_001` |
| **Título** | Baseline UNet — 5 épocas |
| **Estado** | planned \| running \| completed \| failed \| archived |
| **Criado em** | 2026-05-29 |

---

## 2. manifest.yaml

Copiar e preencher:

```yaml 
experiment_id: exp_20260529_001
created_at: "2026-05-29T14:30:00Z"
provider: local_gpu
pipeline: 04_segmentation/train.py
dataset_path: ./02_dataset
output_path: ./04_segmentation/outputs
device: cuda
git_commit: null
notes: "Describe hypothesis and changes vs previous run."

hyperparameters:
  epochs: 5
  batch_size: 2
  learning_rate: 0.0001

metrics_summary:
  status: completed
  final_train_loss: null
  final_val_loss: null
```

---

## 3. Estrutura de ficheiros

```text
exp_20260529_001/
├── manifest.yaml           # obrigatório
├── metrics.json            # cópia ou derivado de train output
├── config_snapshot.yaml    # cópia de 04_segmentation/config.yaml no momento do run
├── checkpoints/
│   └── last.pt
├── logs/
└── figures/
    └── loss_curve.png      # opcional
```

---

## 4. Procedimento

1. Executar adapter do runtime (se necessário).
2. Executar `python 04_segmentation/train.py`.
3. Verificar `04_segmentation/outputs/metrics.json`.
4. Copiar artefactos para `07_results/experiments/<exp_id>/`.
5. Atualizar `manifest.yaml` com métricas finais e `git_commit`.
6. Registar figuras em `figures/`.

---

## 5. Registo no relatório académico

No `08_report`, citar:

> Experiência `exp_20260529_001` (provider `local_gpu`, UNet MONAI, 5 épocas) — ver `07_results/experiments/exp_20260529_001/`.

---

## 6. Comparação com outra experiência

```text
07_results/comparisons/exp_20260529_001_vs_002/
├── comparison_table.csv
└── notes.md
```

---

## Checklist

- [ ] `experiment_id` único
- [ ] `manifest.yaml` completo
- [ ] `config_snapshot.yaml` guardado
- [ ] Checkpoint referenciado no manifesto
- [ ] Estado atualizado para `completed` ou `failed`

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
