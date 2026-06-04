# Padrões de Experiências e Resultados

**Versão:** 1.0

---

## 1. Objetivo

Definir como os **resultados experimentais** são organizados, nomeados e promovidos desde a pipeline de treino até ao relatório académico, sem duplicar lógica nem perder rastreabilidade.

---

## 2. Separação de responsabilidades

| Zona | Conteúdo | Ciclo de vida |
|------|----------|---------------|
| `04_segmentation/outputs/` | Artefactos **técnicos** do run (checkpoints, logs, `metrics.json`) | Por execução de `train.py` |
| `07_results/experiments/<exp_id>/` | Experiência **documentada** (manifesto, métricas, figuras) | Persistente, citável no relatório |
| `07_results/reports/` | Sínteses e tabelas finais | Entrega académica |
| `06_evaluation/` | Avaliação comparativa entre métodos | Análise |

---

## 3. Identificador de experiência

Formato:

```text
exp_YYYYMMDD_NNN
```

Exemplo: `exp_20260529_001`

| Componente | Regra |
|------------|-------|
| Prefixo | `exp_` fixo |
| Data | UTC ou local (documentar no manifesto) |
| Sequência | `001`, `002`, … por dia |

---

## 4. Estrutura de pasta (alvo)

```text
07_results/
├── figures/              # figuras gerais não ligadas a uma exp
├── metrics/              # agregados entre experiências
├── comparisons/          # comparações lado a lado
├── reports/              # relatórios finais (ex-PDFs, markdown export)
└── experiments/
    └── exp_20260529_001/
        ├── manifest.yaml
        ├── metrics.json
        ├── config_snapshot.yaml
        ├── checkpoints/
        │   └── last.pt
        ├── logs/
        └── figures/
```

Template: [../templates/experiment_template.md](../templates/experiment_template.md).

---

## 5. Ficheiro `manifest.yaml`

Campos obrigatórios:

```yaml
experiment_id: exp_20260529_001
created_at: "2026-05-29T14:30:00Z"
provider: local_gpu          # local_cpu | local_gpu | kaggle
pipeline: 04_segmentation/train.py
dataset_path: ./02_dataset
device: cuda
git_commit: abc1234          # opcional mas recomendado
notes: "Baseline UNet 5 epochs"
```

Campos opcionais:

```yaml
hyperparameters:
  epochs: 5
  batch_size: 2
  learning_rate: 0.0001
metrics_summary:
  final_train_loss: 0.012
  final_val_loss: 0.018
```

---

## 6. Promoção pós-treino

Fluxo normativo (implementação futura em `99_system/tools/` ou módulo `00_common`):

1. Executar `train.py` → gera `04_segmentation/outputs/`.
2. Executar promoção (script) → copia/sincroniza para `07_results/experiments/<exp_id>/`.
3. Preencher `manifest.yaml`.
4. Registar figuras em `figures/`.

**Não** editar manualmente checkpoints sem atualizar o manifesto.

---

## 7. Métricas

| Ficheiro | Origem | Uso |
|----------|--------|-----|
| `04_segmentation/outputs/metrics.json` | `train.py` | Debug e run técnico |
| `07_results/experiments/<id>/metrics.json` | Cópia ou transformação | Citação no relatório |

Formato JSON: manter chaves em `snake_case` inglês (`train_loss`, `val_loss`, `status`).

---

## 8. Figuras

- Nomes: `snake_case` descritivos — `loss_curve.png`, `sample_prediction_01.png`.
- Resolução e formato documentados no notebook que gera a figura.
- Armazenar em `experiments/<id>/figures/`, não apenas inline no notebook.

---

## 9. Comparações

`07_results/comparisons/`:

```text
comparisons/
└── exp_20260529_001_vs_002/
    ├── comparison_table.csv
    └── overlay_metrics.json
```

---

## 10. Relatórios académicos

`07_results/reports/` e `08_report/`:

- O relatório final **referencia** `experiment_id`, não paths absolutos locais.
- Tabelas exportadas também em `07_results/reports/`.

---

## 11. Integração com notebooks

Notebooks devem declarar o `experiment_id` na secção «Experimento» (ver [notebook_standards.md](notebook_standards.md)).

---

## 12. Git e dados grandes

| Artefacto | Git |
|-----------|-----|
| `manifest.yaml`, `metrics.json` | Sim |
| Checkpoints `.pt` | Opcional — preferir `.gitignore` + armazenamento externo |
| Dataset | Não — apenas estrutura de pastas |

Atualizar `.gitignore` na Fase 10 se necessário.

---

## 13. Estados de experiência

| Estado | Descrição |
|--------|-----------|
| `planned` | Manifesto criado, treino não executado |
| `running` | Treino em curso |
| `completed` | Métricas e checkpoints finais |
| `failed` | Erro documentado no manifesto |
| `archived` | Não usado em comparações ativas |

---

## 14. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação — Fase 2 |
