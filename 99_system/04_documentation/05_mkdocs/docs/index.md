# Fetal Vein Segmentation

Documentação central do trabalho prático de **segmentação da veia umbilical fetal** (Imagem Biomédica — IPCA).

---

## Princípio arquitetural

```text
Mesmo código · Mesmo dataset · Mesmo output · Mesma estrutura
Diferente ambiente de execução
```

A pipeline científica vive em `04-segmentation/` (alvo pós-migração: `04_segmentation/`).  
Os runtimes em `10-runtime/` apenas preparam o ambiente.

---

## Estado do projeto

| Fase | Estado |
|------|--------|
| Governação e templates | Concluída |
| Validação nomenclatura (Nível A) | Aprovada |
| MkDocs (esta plataforma) | Em utilização |
| Migração física (Fase 10) | Pendente |

!!! note "Paths no site"
    Enquanto a Fase 10 não for executada, os paths no repositório usam **hífens** (`00-common`, `10-runtime`).  
    A documentação descreve o **alvo Nível A** (`00_common`, `10_runtime`).

---

## Navegação rápida

| Secção | Conteúdo |
|--------|----------|
| [Governação](governance/index.md) | Regras normativas do projeto |
| [Arquitetura](architecture/index.md) | Sistema, runtime, fluxo de dados |
| [Estrutura do projeto](project_structure/index.md) | Pastas e responsabilidades |
| [Tecnologias](technologies/index.md) | Stack técnica |
| [Runtimes](runtimes/index.md) | local_cpu, local_gpu, kaggle |
| [Pipeline](pipeline/index.md) | `train.py` e módulos |
| [API](api/index.md) | Referência Python (mkdocstrings) |
| [Migração](migration/index.md) | Planos Fase 3 / 10 |

---

## Comandos úteis

```bash
cd 99_system/05_documentation/05_mkdocs
pip install -r requirements_mkdocs.txt
python sync_source_docs.py
mkdocs serve
```

URL local: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
