# Publishing documentation (MkDocs + GitHub Pages)

## Prerequisites

```bash
pip install -r requirements-mkdocs.txt
```

## Local build

```bash
mkdocs build --strict
```

Output: `site/` (gitignored).

## Deploy

```bash
mkdocs gh-deploy
```

Pushes the built site to `gh-pages`. Run **once** per release to avoid cancelled GitHub Pages workflow runs.

## How content is included

| MkDocs page | Repository source |
|-------------|-------------------|
| State of the Art | `01_academic/02_literature/state_of_the_art.md` |
| Dataset overview | `02_dataset/README.md` |
| Dataset licence | `01_academic/03_dataset_documentation/licence.md` |
| Scientific pipeline | `03_pipeline/README.md` |

Markdown is included with `pymdownx.snippets`. PDFs, notebooks, and CSV files link to the GitHub repository (not mirrored copies).

## Configuration

| File | Role |
|------|------|
| `mkdocs.yml` | Site and navigation (repository root) |
| `06_documentation/` | Documentation source (`docs_dir`) |
