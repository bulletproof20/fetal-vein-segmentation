# Publishing documentation (MkDocs + GitHub Pages)

This file describes how to build and publish the site from `06_documentation/` without changing the scientific pipeline.

## Prerequisites

```bash
pip install -r requirements-mkdocs.txt
```

## Local build

```bash
mkdocs build
```

Output directory: `site/` (ignored by Git).

## Deploy to GitHub Pages

1. Uncomment and set `site_url` and `repo_url` in the root `mkdocs.yml` to match your GitHub repository.
2. From the repository root:

```bash
mkdocs gh-deploy
```

This pushes the built site to the `gh-pages` branch. Enable **GitHub Pages** in the repository settings (source: `gh-pages` branch, `/` root).

## Configuration

| File | Role |
|------|------|
| `mkdocs.yml` | Site configuration and navigation (repository root) |
| `requirements-mkdocs.txt` | MkDocs dependencies only |
| `06_documentation/index.md` | Site home and authoritative link matrix |

The site links to repository sources (README, notebooks, dataset README) instead of duplicating their content.
