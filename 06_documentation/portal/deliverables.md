# Deliverables

--8<-- "includes/repo_links.md"

Where to find **project outputs**. This page does not reproduce report text, masks, or metric tables.

---

## Written report

| Item | Role | Open |
|------|------|------|
| Report template | Structure for the final written deliverable | [template.docx][report-template] |

Submitted PDF/DOCX (if stored outside the template path) should be referenced in your report cover sheet or submission system.

---

## Evaluation results

| Item | Role | Open |
|------|------|------|
| Results folder | Aggregated pipeline outputs | [04_pipeline_results/][results-dir] |
| Comparison table (CSV) | Cross-experiment metrics (when generated) | [tabela_avaliacao_experiencias.csv][results-csv] |

The evaluation notebook writes the comparison table after segmentation masks exist under `02_dataset/results_*`.

---

## How results are produced

Metrics (Dice, accuracy, precision, recall) and the comparison across Original + PP1–PP5 — with and without morphological post-processing — are computed in [03_evaluation.ipynb][nb-evaluation] (`calculate_metrics`, `pos_process`).

No formulas or metric definitions are duplicated on this site.

---

## Reproducibility (summary)

1. Clone the [repository][repo].
2. Open [README.md][readme] for Colab setup (`requirements.txt`).
3. Follow [03_pipeline/README.md][pipeline-readme] for the official execution order.
4. Use [02_dataset/README.md][dataset-readme] for data layout.

---

## Related

- [Home](../index.md)
- [Implementation](implementation.md)
- [Academic materials](academic.md)
