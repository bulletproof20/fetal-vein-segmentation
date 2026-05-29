# Template — Documento Markdown

Use para novos documentos em `99_system/documentation/`, relatórios ou READMEs técnicos.

---

## Cabeçalho

```markdown
# Título do documento

**Versão:** 1.0  
**Autor:** Nome (opcional)  
**Estado:** rascunho | normativo | arquivado

---

## 1. Propósito

Uma ou duas frases sobre o objetivo do documento.

## 2. Âmbito

O que está incluído e excluído.

## 3. Conteúdo principal

### 3.1 Subsecção

Texto, tabelas, listas.

| Coluna A | Coluna B |
|----------|----------|
| valor    | valor    |

### 3.2 Exemplo de código

```python
def example() -> None:
    pass
```

## 4. Documentos relacionados

- [project_governance.md](../governance/project_governance.md)
- [system_architecture.md](../architecture/system_architecture.md)

## 5. Revisão

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | YYYY-MM-DD | Criação |
```

---

## Regras

- Português (PT-PT) para documentação de governação e arquitetura.
- Links relativos entre ficheiros em `99_system/documentation/`.
- Diagramas: preferir Mermaid em blocos ` ```mermaid `.
- Uma ideia principal por secção de nível 2.

---

## Revisão

| Versão | Data |
|--------|------|
| 1.0 | 2026-05-29 |
