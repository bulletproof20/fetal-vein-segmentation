# MkDocs — Documentação do projeto

## Instalação

```bash
cd 99_system/05_documentation/05_mkdocs
pip install -r requirements_mkdocs.txt
```

## Sincronizar fontes normativas

Copia markdown de `99_system/documentation/` para `docs/`:

```bash
python sync_source_docs.py
```

## Servir localmente

```bash
mkdocs serve
```

URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Build estático

```bash
mkdocs build
```

Output: `site/`
