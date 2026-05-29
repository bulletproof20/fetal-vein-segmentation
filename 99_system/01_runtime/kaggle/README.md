# Runtime Kaggle

Este runtime **não contém lógica de treino**. Apenas prepara o ambiente Kaggle e delega para a pipeline única.

## Fluxo

1. Adicionar dataset Kaggle (ex.: `fetal-vein`) com `images/` e `masks/`.
2. Copiar o repositório para o notebook ou usar `launch.ipynb`.
3. Instalar dependências: `pip install -r 10-runtime/kaggle/requirements.txt`
4. Executar:

```bash
python 10-runtime/kaggle/adapter.py
python 04-segmentation/train.py
python -c "from importlib.util import spec_from_file_location, module_from_spec; ..."
```

Ou usar as células de `launch.ipynb`.

## Outputs

A pipeline grava sempre em `04-segmentation/outputs/` (ou o caminho definido em `config.yaml`).

O adapter copia resultados para `/kaggle/working/output` via `sync_outputs()` para download no Kaggle.

## Variáveis

| Variável | Descrição |
|----------|-----------|
| `FETAL_PROVIDER` | `kaggle` |
| `FETAL_DATASET_PATH` | Caminho do dataset de input |
| `FETAL_OUTPUT_PATH` | Destino dos artefactos de treino |
