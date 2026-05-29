# Fetal Vein Segmentation

Trabalho prático — **Imagem Biomédica** (IPCA). Segmentação da veia umbilical fetal em ecografia.

## Princípio arquitetural

- **Uma única pipeline de treino:** `04_segmentation/train.py`
- **Runtimes** (`99_system/01_runtime/`) apenas preparam ambiente e variáveis — sem duplicar lógica de treino
- **Bootstrap:** `99_system/02_bootstrap/`

## Estrutura (resumo)

```text
00_common … 09_presentation   # pipeline científica e entregáveis
99_system/                    # infraestrutura
```

Ver `99_system/04_documentation/04_migration/architecture_consolidation_report.md` para o mapa completo.

## Início rápido

```bash
python 99_system/02_bootstrap/bootstrap.py --no-strict
python 99_system/01_runtime/local_cpu/adapter.py
python 04_segmentation/train.py
```

Documentação: `99_system/README.md`
