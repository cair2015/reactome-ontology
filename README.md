# Reactome Ontology

`reactome-ontology` is an ontology-first [LinkML](https://linkml.io/linkml/) project for representing key parts of the Reactome data model as a cleaner ontology-oriented schema.

The repository centers on a curated LinkML schema that:

- keeps ontology-facing classes and slots from the Reactome model
- separates source-schema mapping details into dedicated mapping files
- generates Python dataclasses, Pydantic models, documentation, and ontology artifacts from a single schema source

The current primary schema is [`src/reactome_ontology/schema/reactome_ontology.yaml`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/schema/reactome_ontology.yaml).

## What This Repository Contains

- [`src/reactome_ontology/schema/reactome_ontology.yaml`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/schema/reactome_ontology.yaml): the main LinkML schema
- [`src/reactome_ontology/schema/reactome_ontology_mapping.md`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/schema/reactome_ontology_mapping.md): human-readable mapping from ontology terms to the Reactome source schema
- [`src/reactome_ontology/schema/reactome_ontology_mapping.tsv`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/schema/reactome_ontology_mapping.tsv): tabular version of the same mapping
- [`src/reactome_ontology/datamodel/reactome_ontology.py`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/datamodel/reactome_ontology.py): generated Python datamodel
- [`src/reactome_ontology/datamodel/reactome_ontology_pydantic.py`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/datamodel/reactome_ontology_pydantic.py): generated Pydantic datamodel
- [`ontology/`](https://github.com/cair2015/reactome-ontology/tree/main/ontology): ontology exports and related alignment artifacts
- [`docs/`](https://github.com/cair2015/reactome-ontology/tree/main/docs): MkDocs source for published documentation
- [`tests/data/`](https://github.com/cair2015/reactome-ontology/tree/main/tests/data): example YAML instances used for validation tests

## Project Goal

Reactome is a rich pathway knowledgebase, but its operational source schema is not always ideal as an ontology-facing exchange model. This project reshapes that source into a LinkML profile that is easier to:

- align with ontology terms and URIs
- validate as structured data
- export into downstream semantic artifacts
- use from Python applications

## Installation

This project uses `uv` for dependency management and `just` for common development tasks.

### Prerequisites

- Python 3.11+
- `uv`
- `just`

### Set Up The Environment

```bash
uv sync --group dev
```

## Common Commands

The repository is configured through [`config.public.mk`](https://github.com/cair2015/reactome-ontology/blob/main/config.public.mk), which points the generators at the schema in `src/reactome_ontology/schema`.

### Generate Project Artifacts

```bash
just gen-project
```

This regenerates project outputs from the LinkML schema, including:

- Python dataclasses in `src/reactome_ontology/datamodel`
- Pydantic models in `src/reactome_ontology/datamodel`
- additional generated outputs under `project/`

### Generate Documentation

```bash
just gen-doc
```

This updates:

- generated schema documentation in `docs/elements/`
- the distributed merged schema in `docs/schema/`

### Build Everything Needed For The Local Docs Site

```bash
just site
```

### Run Tests

```bash
just test
```

This runs schema generation checks, Python tests, and example-data validation.

## Using The Python Datamodel

After installing dependencies, you can import the generated classes directly:

```python
from reactome_ontology.datamodel.reactome_ontology import Pathway, Person

pathway = Pathway(id="R-HSA-EXAMPLE", name="Example pathway")
person = Person(id="person-1", name="Curator Name")
```

The generated models come from the LinkML schema, so schema edits should generally be followed by regeneration with `just gen-project`.

## Example Data And Validation

Example instances live in [`tests/data/valid`](https://github.com/cair2015/reactome-ontology/tree/main/tests/data/valid) and [`tests/data/invalid`](https://github.com/cair2015/reactome-ontology/tree/main/tests/data/invalid). The test suite loads valid examples against the generated Python classes to confirm the datamodel remains usable.

## Documentation

- Project docs source: [`docs/`](https://github.com/cair2015/reactome-ontology/tree/main/docs)
- MkDocs config: [`mkdocs.yml`](https://github.com/cair2015/reactome-ontology/blob/main/mkdocs.yml)
- Published ontology-model docs: [https://cair2015.github.io/reactome-ontology/](https://cair2015.github.io/reactome-ontology/)

To serve docs locally:

```bash
just testdoc
```

## Repository Structure

```text
.
├── src/reactome_ontology/
│   ├── datamodel/         # generated Python models
│   └── schema/            # LinkML schema and mapping files
├── docs/                  # MkDocs content
├── ontology/              # ontology exports and related assets
├── tests/                 # tests and example data
├── justfile               # project automation
└── pyproject.toml         # package metadata and dependencies
```

## Development Notes

- Treat [`src/reactome_ontology/schema/reactome_ontology.yaml`](https://github.com/cair2015/reactome-ontology/blob/main/src/reactome_ontology/schema/reactome_ontology.yaml) as the source of truth.
- Generated Python files in [`src/reactome_ontology/datamodel/`](https://github.com/cair2015/reactome-ontology/tree/main/src/reactome_ontology/datamodel) should be regenerated, not hand-edited.
- Mapping files in [`src/reactome_ontology/schema/`](https://github.com/cair2015/reactome-ontology/tree/main/src/reactome_ontology/schema) capture correspondence back to the original Reactome schema.

## License

This project is distributed under the MIT License. See [`LICENSE`](https://github.com/cair2015/reactome-ontology/blob/main/LICENSE).
