"""Tests for schema-aligned YAML fixtures."""

from pathlib import Path

import pytest
from linkml_runtime.loaders import yaml_loader

import reactome_ontology.datamodel.reactome_ontology as reactome_model

DATA_DIR = Path(__file__).parent / "data"
VALID_EXAMPLE_FILES = sorted((DATA_DIR / "valid").glob("*.yaml"))
INVALID_EXAMPLE_FILES = sorted((DATA_DIR / "invalid").glob("*.yaml"))


def _target_class_for(filepath: Path):
    """Resolve the generated datamodel class from the fixture filename."""
    target_class_name = filepath.stem.split("-")[0]
    return getattr(reactome_model, target_class_name)


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath: Path):
    """Valid fixtures should deserialize into the expected generated class."""
    target_class = _target_class_for(filepath)
    obj = yaml_loader.load(str(filepath), target_class=target_class)

    assert obj is not None
    assert isinstance(obj, target_class)


@pytest.mark.parametrize("filepath", INVALID_EXAMPLE_FILES)
def test_invalid_data_files_raise_validation_errors(filepath: Path):
    """Invalid fixtures should fail during LinkML object construction."""
    target_class = _target_class_for(filepath)

    with pytest.raises(ValueError):
        yaml_loader.load(str(filepath), target_class=target_class)
