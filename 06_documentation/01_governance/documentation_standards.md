# Padrões de Documentação

**Versão:** 1.0  
**Motor:** MkDocs Material + mkdocstrings (Fase 5)

---

## 1. Objetivo

Gerar documentação **automática e navegável** a partir de:

- Markdown em `99_system/documentation/`
- Docstrings Google Style nos módulos `.py`
- Diagramas e páginas de arquitetura

---

## 2. Localização de ficheiros

| Tipo | Local |
|------|-------|
| Governação | `99_system/documentation/governance/` |
| Arquitetura | `99_system/documentation/architecture/` |
| Templates | `99_system/documentation/templates/` |
| Config MkDocs | `99_system/documentation/mkdocs/mkdocs.yml` (Fase 5) |
| Site gerado | `99_system/documentation/site/` (gitignore) |
| Auditoria / migração | `99_system/documentation/audit_report.md`, `migration_report.md` |

**Raiz do repositório:** `README.md` curto com links para documentação MkDocs.

---

## 3. Idioma

| Conteúdo | Idioma |
|----------|--------|
| Governação e arquitetura | Português |
| Docstrings (API) | Inglês |
| README técnico de runtime | Português ou inglês (consistente por pasta) |
| Notebooks (markdown) | Português |

---

## 4. MkDocs Material

### 4.1 Estrutura de navegação (alvo)

```text
Início
├── Visão geral
├── Arquitetura
│   ├── Sistema
│   ├── Runtime
│   ├── Fluxo de dados
│   └── Stack
├── Governação
├── Pipeline (04_segmentation)
├── Runtimes (10_runtime)
└── API Reference (mkdocstrings)
```

### 4.2 Plugins

| Plugin | Função |
|--------|--------|
| `material` | Tema e navegação |
| `mkdocstrings` | API a partir de docstrings |
| `search` | Pesquisa integrada |

### 4.3 Configuração mkdocstrings

- Handler: `python`
- Estilo: `google`
- Paths de import: raiz do repo + `00_common`, `04_segmentation`, `10_runtime` (após migração snake_case)

---

## 5. Formato Markdown

- ATX headings (`#`, `##`).
- Tabelas para decisões e comparações.
- Blocos de código com linguagem indicada.
- Links relativos entre documentos de governação.
- Evitar HTML inline desnecessário.

Template: [../templates/markdown_document_template.md](../templates/markdown_document_template.md).

---

## 6. Documentação de API

### 6.1 O que documentar

| Módulo | Prioridade |
|--------|------------|
| `04_segmentation/*` | Alta |
| `00_common/runtime_paths.py` | Alta |
| `00_common/bootstrap/*` | Média |
| `10_runtime/*/adapter.py` | Média |
| Funções só em notebooks | Baixa — extrair para `.py` quando estável |

### 6.2 O que não documentar em API pública

- Funções privadas `_internal` (podem aparecer com opção `members: false` por módulo).
- Scripts one-off em `99_system/tools/`.

---

## 7. Diagramas

- Fluxos: Mermaid em `architecture/data_flow.md`.
- Diagramas complexos: preferir Mermaid no Markdown para versionar com git.

---

## 8. Versionamento e revisão

Cada documento normativo inclui tabela «Revisão» no rodapé.

Alterações de governação: incrementar versão menor (1.0 → 1.1).

---

## 9. Publicação

### 9.1 Local

```bash
cd 99_system/documentation/mkdocs
mkdocs serve
```

### 9.2 CI (futuro)

- Build em push para `main`
- Artefacto `site/` ou GitHub Pages

---

## 10. Relação com código legado

Até à Fase 10, a documentação pode referenciar paths legados (`00-common`) com nota «será renomeado para `00_common`».

Após migração, atualizar links num único commit de documentação.

---

## 11. Checklist de página nova

- [ ] Título e propósito na primeira secção
- [ ] Links para documentos relacionados
- [ ] Tabela de revisão
- [ ] Inclusão em `mkdocs.yml` (quando existir)
- [ ] Ortografia PT-PT consistente

---

## 12. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-05-29 | Criação — Fase 2 |
