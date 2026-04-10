# Example Data For `reactome_ontology`

This folder contains small YAML fixtures for testing the generated Reactome LinkML datamodel.

- `valid/` contains examples that should load successfully.
- `invalid/` contains examples that should fail because they omit required schema content.

Fixture filenames follow the pattern `ClassName-###.yaml`. The class name is derived from the part before the first `-`, and the tests use that to select the generated Python class to load.
