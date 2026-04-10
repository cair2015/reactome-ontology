# Examples

This folder holds generated example outputs derived from the YAML fixtures in [tests/data](../tests/data/).

When you run `just test`, the `linkml-run-examples` step reads the schema-aligned fixtures in `tests/data/valid` and `tests/data/invalid` and writes converted outputs into `examples/output/`.

The `output/` directory is intentionally git-ignored because it can be regenerated at any time.
