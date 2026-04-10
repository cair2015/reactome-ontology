# Schema Directory

This directory contains the ontology-first LinkML schema for this project together with mapping files that relate it to the upstream Reactome LinkML schema.

## Files

- `reactome_ontology.yaml`: the primary ontology-oriented LinkML schema maintained in this repository
- `reactome_ontology_mapping.md`: a human-readable mapping from this schema to the upstream Reactome schema
- `reactome_ontology_mapping.tsv`: a tabular version of the mapping for spreadsheet use, QA, and future automation

## Reference Schema

The upstream Reactome LinkML schema is available at:

- https://github.com/reactome/reactome-schemas/blob/main/schema.yaml

That upstream schema appears aligned with the current Reactome Neo4j-facing data model and serves as the main external reference point for this repository.

## How To Use These Files

- Use `reactome_ontology.yaml` as the source of truth for the ontology-first model in this project.
- Use the mapping files to verify how ontology-facing classes and slots correspond to the upstream Reactome schema.
- Use the upstream Reactome schema as a reference when checking alignment with the Reactome source model or when mapping this ontology model back to the Neo4j-oriented schema.
