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

On each build, `06_documentation/hooks/copy_repo_assets.py` mirrors key repository artefacts (PDFs, notebooks, CSV files, figures) into `06_documentation/repo_files/` so portal pages can link to them with site-relative paths. The folder is named `repo_files/` (not `assets/`) to avoid colliding with MkDocs Material theme assets.

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
| `06_documentation/index.md` | Reviewer home page |
| `06_documentation/portal/` | Academic / implementation / deliverables indexes |
| `06_documentation/hooks/copy_repo_assets.py` | Pre-build asset mirror into `assets/` |

Use **direct Markdown links** in portal pages (`[label](../repo_files/…)` or `[label](page.md)`). Do not use reference-style links (`[text][ref]`).

The site indexes repository artefacts; notebook and governance content remain authoritative in their source folders.
