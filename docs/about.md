# About Reactome Ontology

`reactome-ontology` is a LinkML-based project for representing key parts of the Reactome data model in a cleaner, ontology-oriented form.

The goal is not to mirror every implementation detail of the operational Reactome source schema. Instead, this project focuses on preserving the concepts, relationships, and identifiers that are most useful for ontology development, documentation, validation, and downstream semantic integration.

## Why This Project Exists

Reactome is a powerful biological pathway knowledgebase, but its source-facing data structures are designed for curation and system operation rather than ontology-facing exchange. This project creates a profile that is easier to:

- understand as a conceptual model
- validate as structured data
- document automatically
- align with ontology terms and URIs
- export into generated Python and semantic artifacts

## What Is In Scope

The schema includes ontology-relevant classes and relationships for:

- Reactome database objects
- biological events such as pathways and reactions
- physical entities and reference entities
- provenance objects such as instance edits and people
- supporting terms, identifiers, and cross-references

It also preserves selected administrative and serialization-oriented fields that are helpful for round-tripping, validation, and traceability.

## How The Project Is Organized

The repository is built around a single primary schema source:

`src/reactome_ontology/schema/reactome_ontology.yaml`

From that schema, the project generates:

- schema reference documentation
- Python dataclasses
- Pydantic models
- published schema artifacts for documentation and distribution

Additional mapping files document how the ontology-facing schema relates back to the original Reactome source model.

## Documentation Workflow

This documentation site is generated with MkDocs, and schema reference pages are generated from the LinkML schema.

Common commands:

```bash
just gen-doc
just gen-project
just test
```

These commands regenerate documentation and project artifacts, and validate example data and schema behavior.

## Intended Use

This project is useful for anyone who wants to work with Reactome content in a form that is more ontology-friendly than the original operational schema, including:

- ontology engineers
- knowledge graph builders
- data modelers
- Python developers working with generated LinkML models

## Source And Publishing

The Markdown files in `docs/` are the source for this documentation site. Generated schema pages are written into `docs/elements/`, and the published site is deployed through GitHub Pages.
