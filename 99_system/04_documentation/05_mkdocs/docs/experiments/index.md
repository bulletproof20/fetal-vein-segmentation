# Experiências e Resultados

Governação em [experiment_standards.md](../governance/experiment_standards.md).

---

## Duas zonas de outputs

| Zona | Path (alvo) | Conteúdo |
|------|-------------|----------|
| Técnico (run) | `04_segmentation/outputs/` | Checkpoints, logs, `metrics.json` |
| Académico (citável) | `07_results/experiments/<exp_id>/` | Manifesto, figuras, cópia de métricas |

---

## Estrutura `07_results` (Nível A)

```text
07_results/
├── figures/
├── metrics/
├── comparisons/
├── reports/          # ex: final-results
└── experiments/
    └── exp_YYYYMMDD_NNN/
        ├── manifest.yaml
        ├── metrics.json
        ├── config_snapshot.yaml
        ├── checkpoints/
        ├── logs/
        └── figures/
```

---

## Identificador

Formato: `exp_YYYYMMDD_NNN` (ex.: `exp_20260529_001`).

---

## Promoção pós-treino

Fluxo futuro (Fase 10+):

1. `python 04_segmentation/train.py`
2. Script de promoção → `07_results/experiments/<exp_id>/`
3. Preencher `manifest.yaml`

---

## Template

[experiment_template.md](../templates/experiment_template.md)
