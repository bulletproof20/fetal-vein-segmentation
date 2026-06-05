# Design Evolution

**Version:** 4.0

This document describes the evolution of the project architecture throughout the development process and the rationale that led to the final repository structure.

---

## Initial Architectural Concept

During the early stages of the project, the repository was conceived as a highly automated execution framework centred on a unified training entry point.

The initial design emphasised:

* Automated environment validation;
* Runtime abstraction;
* Hardware-independent execution;
* Container-oriented deployment;
* Reusable execution adapters.

The objective was to maximise operational portability and allow experiments to be executed across multiple computational environments while maintaining a consistent workflow.

This exploratory architecture is documented within the design materials preserved under `99_system/`.

---

## Identified Limitations

As the project requirements became more clearly defined, several observations emerged.

The primary objective of the assignment was not the development of an execution framework, but rather the scientific evaluation of image preprocessing techniques, segmentation performance and post-processing strategies.

Consequently, the initial architecture introduced complexity that was not directly aligned with the intended experimental goals.

Specific challenges included:

* Increased implementation overhead;
* Additional abstraction layers unrelated to image analysis;
* Reduced visibility of experimental parameters;
* Greater maintenance effort for comparatively limited scientific benefit.

These observations motivated a redesign focused on experimental reproducibility and methodological transparency.

---

## Architectural Transition

The repository progressively evolved from a software-oriented execution framework into a scientific experimentation platform.

Rather than prioritising runtime abstraction, the revised design focused on:

* Reproducible experimentation;
* Clear separation of processing stages;
* Direct visibility of methodological choices;
* Simplified comparison of preprocessing strategies;
* Transparent presentation of results.

This transition aligned the repository structure more closely with the scientific objectives of the project.

---

## Final Architecture

The final solution adopts a notebook-based scientific workflow organised into three independent processing stages:

```text
Preprocessing
      │
      ▼
Segmentation
      │
      ▼
Evaluation
```

This architecture separates data preparation, model execution and quantitative assessment while preserving traceability throughout the entire experimental process.

The repository structure reflects this workflow:

| Component              | Purpose                                                        |
| ---------------------- | -------------------------------------------------------------- |
| `01_academic/`         | Academic and lecturer-provided material                        |
| `02_dataset/`          | Images, labels, preprocessing outputs and segmentation results |
| `03_pipeline/`         | Scientific workflow implementation                             |
| `04_pipeline_results/` | Aggregated metrics and experimental outputs                    |
| `05_report/`           | Scientific analysis and discussion                             |
| `06_documentation/`    | Technical and governance documentation                         |

---

## Design Rationale

The final architecture was selected because it better supports the scientific objectives of the project.

| Consideration                | Architectural Response                             |
| ---------------------------- | -------------------------------------------------- |
| Experimental reproducibility | Independent and traceable processing stages        |
| Comparative evaluation       | Dedicated datasets for each preprocessing strategy |
| Academic transparency        | Explicit methodology and parameter visibility      |
| Result interpretation        | Clear separation between processing and reporting  |
| Maintainability              | Reduced complexity and simplified workflow         |

---

## Outcome

The architectural evolution reflects a shift from a general-purpose execution framework towards a research-oriented workflow focused on experimentation, evaluation and scientific reporting.

This transition resulted in a repository structure that is more closely aligned with the objectives of the assignment while maintaining reproducibility, transparency and extensibility.

---

## Related Documents

* [System Architecture](system_architecture.md)
* [Data Flow](data_flow.md)
* [Implementation](../portal/implementation.md)
