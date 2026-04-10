from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.7.0"
version = "1.0.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'comments': ['This schema favors ontology-oriented naming for OWL generation; '
                  'source mappings are maintained in separate mapping files.',
                  'Administrative and serialization helper fields are retained for '
                  'round-tripping but may be omitted from OWL export profiles.',
                  'Inverse-style helper relations have been removed from the '
                  'ontology-facing profile in favor of canonical relations.'],
     'default_prefix': 'reactome',
     'default_range': 'string',
     'description': 'A final OWL-oriented LinkML schema for generating a clean '
                    'Reactome ontology. This profile keeps ontology-facing classes '
                    'and properties and removes source-mapping annotations, which '
                    'are maintained in separate mapping files.',
     'id': 'https://w3id.org/reactome-ontology/final',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/licenses/by/4.0/',
     'name': 'reactome_ontology',
     'prefixes': {'BFO': {'prefix_prefix': 'BFO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/BFO_'},
                  'CHEBI': {'prefix_prefix': 'CHEBI',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/CHEBI_'},
                  'GO': {'prefix_prefix': 'GO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/GO_'},
                  'NCBITaxon': {'prefix_prefix': 'NCBITaxon',
                                'prefix_reference': 'http://purl.obolibrary.org/obo/NCBITaxon_'},
                  'RO': {'prefix_prefix': 'RO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/RO_'},
                  'UniProtKB': {'prefix_prefix': 'UniProtKB',
                                'prefix_reference': 'http://purl.uniprot.org/uniprot/'},
                  'biolink': {'prefix_prefix': 'biolink',
                              'prefix_reference': 'https://w3id.org/biolink/vocab/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'orcid': {'prefix_prefix': 'orcid',
                            'prefix_reference': 'https://orcid.org/'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'reactome': {'prefix_prefix': 'reactome',
                               'prefix_reference': 'https://w3id.org/reactome-ontology/'},
                  'reactomeid': {'prefix_prefix': 'reactomeid',
                                 'prefix_reference': 'https://w3id.org/reactome-ontology/id/'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'src/reactome_ontology/schema/reactome_ontology.yaml',
     'title': 'Reactome Ontology Model'} )


class NamedEntity(ConfiguredBaseModel):
    """
    Generic named entity used as a lightweight semantic root for serializable objects.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:NamedEntity',
         'comments': ['Provides reusable identifier, naming, and descriptive slots '
                      'independent of the Reactome-specific hierarchy.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class DatabaseObject(NamedEntity):
    """
    Root class for most Reactome schema objects and the main provenance-bearing superclass.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:DatabaseObject',
         'comments': ['Reactome’s frame-based model uses DatabaseObject as the common '
                      'ancestor for curated graph records.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'created': {'name': 'created', 'required': True},
                        'display_label': {'name': 'display_label', 'required': True},
                        'reactome_db_id': {'name': 'reactome_db_id', 'required': True},
                        'reactome_stable_identifier': {'name': 'reactome_stable_identifier',
                                                       'required': True},
                        'source_schema_class': {'name': 'source_schema_class',
                                                'required': True}}})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class InstanceEdit(DatabaseObject):
    """
    Provenance record describing a curation action such as creation, modification, review, or revision.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:InstanceEdit',
         'comments': ['Typically stores who performed an edit and when the edit '
                      'occurred.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    date: Optional[datetime ] = Field(default=None, description="""Timestamp or date string for the edit activity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['instance_edit']} })
    author: Optional[list[Person]] = Field(default=None, description="""Person or people responsible for the edit activity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['instance_edit']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Publication(DatabaseObject):
    """
    Publication record used as evidence or supporting documentation for curated biology.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:Publication',
         'comments': ['Abstract superclass for specific publication-like records.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class LiteratureReference(Publication):
    """
    Literature citation record, commonly representing a PubMed-indexed paper supporting a Reactome assertion.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:LiteratureReference',
         'comments': ['Used widely to ground events, regulations, and catalyst '
                      'activities in the literature.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    pubmed_id: Optional[str] = Field(default=None, description="""PubMed identifier for a literature reference.""", json_schema_extra = { "linkml_meta": {'comments': ['Stored as string for broad interoperability with exports and '
                      'loaders.'],
         'domain_of': ['literature_reference'],
         'slot_uri': 'reactome:pubmedId'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('pubmed_id')
    def pattern_pubmed_id(cls, v):
        pattern=re.compile(r"^[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid pubmed_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid pubmed_id format: {v}"
            raise ValueError(err_msg)
        return v


class Person(DatabaseObject):
    """
    Person record used primarily for provenance, authorship, and curation attribution.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Person',
         'comments': ['May represent curators, reviewers, or contributors.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    orcid: Optional[str] = Field(default=None, description="""ORCID identifier for a person involved in curation or authorship.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for curator and contributor disambiguation.'],
         'domain_of': ['person'],
         'slot_uri': 'reactome:orcid'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Summation(DatabaseObject):
    """
    Narrative summary record containing prose that explains the biological meaning of an entity or event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Summation',
         'comments': ['Distinct from a formal definition; meant for human reading.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    text: str = Field(default=..., description="""Narrative summary text.""", json_schema_extra = { "linkml_meta": {'domain_of': ['summation']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Event(DatabaseObject):
    """
    Biological occurrence or process unit in Reactome, covering both pathways and reaction-like events.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:Event',
         'comments': ['Event is one of the central abstractions in the Reactome '
                      'model.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Pathway(Event):
    """
    Curated grouping of biologically related events representing a pathway or pathway-like module.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Pathway',
         'comments': ['Pathways can overlap; event membership is not exclusive.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_event': {'name': 'has_event', 'required': True}}})

    has_event: list[Event] = Field(default=..., description="""Membership relation linking a pathway to constituent events.""", json_schema_extra = { "linkml_meta": {'comments': ['Pathways in Reactome are curated groupings of events and can '
                      'overlap with other pathways.'],
         'domain_of': ['pathway'],
         'slot_uri': 'reactome:hasEvent'} })
    has_go_biological_process: Optional[str] = Field(default=None, description="""GO biological process term associated with a Reactome pathway or event.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful as a high-level semantic alignment rather than an exact '
                      'equivalence in all cases.'],
         'domain_of': ['pathway'],
         'slot_uri': 'reactome:hasGoBiologicalProcess'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReactionLikeEvent(Event):
    """
    Event in which physical entities participate as inputs, outputs, regulators, or catalysts in a transformation-like process.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:ReactionLikeEvent',
         'comments': ['Covers canonical reactions as well as black-box and '
                      'polymerization-style event subclasses.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_input: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[CatalystActivity]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[Regulation]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[Event]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[Interaction]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Reaction(ReactionLikeEvent):
    """
    Standard reaction-like event with explicit transformed inputs and outputs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Reaction',
         'comments': ['Best used for relatively well-resolved mechanistic '
                      'conversions.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_input': {'name': 'has_input', 'required': True},
                        'has_output': {'name': 'has_output', 'required': True}}})

    has_input: list[PhysicalEntity] = Field(default=..., description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: list[PhysicalEntity] = Field(default=..., description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[CatalystActivity]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[Regulation]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[Event]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[Interaction]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class BlackBoxEvent(ReactionLikeEvent):
    """
    Reaction-like event included in the pathway model despite incomplete mechanistic detail.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:BlackBoxEvent',
         'comments': ['Useful when biological evidence supports the event but not a '
                      'full molecular mechanism.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_input: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[CatalystActivity]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[Regulation]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[Event]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[Interaction]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Polymerization(ReactionLikeEvent):
    """
    Event representing formation of a polymer from repeated or assembling units.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Polymerization',
         'comments': ['Kept distinct because its participant semantics can differ from '
                      'ordinary reaction balance.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_input: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[CatalystActivity]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[Regulation]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[Event]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[Interaction]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Depolymerization(ReactionLikeEvent):
    """
    Event representing breakdown of a polymer into constituent or smaller units.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Depolymerization',
         'comments': ['Complementary to polymerisation.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_input: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[CatalystActivity]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[Regulation]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[Event]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[PhysicalEntity]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[Interaction]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    release_date: Optional[date] = Field(default=None, description="""Release date associated with a curation or publication cycle.""", json_schema_extra = { "linkml_meta": {'comments': ['Modeled as string to match Reactome exports; can be normalized '
                      'later if needed.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseDate'} })
    release_status: Optional[str] = Field(default=None, description="""Editorial release state of the object in the Reactome release process.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples might include draft-like or released-like status '
                      'labels depending on source exports.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:releaseStatus'} })
    is_inferred: Optional[bool] = Field(default=None, description="""Indicates whether an object was computationally inferred rather than directly curated.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome uses inference especially for orthology-based event '
                      'propagation.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:isInferred'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class PhysicalEntity(DatabaseObject):
    """
    Concrete biological participant whose identity reflects both underlying molecular identity and contextual state.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:PhysicalEntity',
         'comments': ['In Reactome, compartment, modification state, and assembly '
                      'state can distinguish one physical entity from another.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class SimpleEntity(PhysicalEntity):
    """
    Simple molecular entity, typically a small molecule or other non-sequence-based chemical participant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:SimpleEntity',
         'comments': ['Commonly aligned to ChEBI-like reference identities through '
                      'ReferenceMolecule.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_reference_entity': {'name': 'has_reference_entity',
                                                 'range': 'reference_molecule',
                                                 'required': True}}})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ["{'One of the key distinctions in Reactome': 'reference identity "
                      "is separate from stateful physical instantiation.'}"],
         'domain_of': ['simple_entity', 'sequence_entity'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class GenomeEncodedEntity(PhysicalEntity):
    """
    Physical entity whose existence is grounded in a genome-encoded product such as a protein or nucleic acid.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GenomeEncodedEntity',
         'comments': ['Serves as a superclass for accessioned sequence-based '
                      'entities.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class SequenceEntity(GenomeEncodedEntity):
    """
    Sequence-bearing physical entity linked to a stable reference sequence and optionally decorated with residue modifications and subsequence coordinates.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:SequenceEntity',
         'comments': ['Core Reactome pattern for proteins, RNAs, and other accessioned '
                      'biomolecules in specific states.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_reference_entity': {'name': 'has_reference_entity',
                                                 'range': 'reference_sequence',
                                                 'required': True}}})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ["{'One of the key distinctions in Reactome': 'reference identity "
                      "is separate from stateful physical instantiation.'}"],
         'domain_of': ['simple_entity', 'sequence_entity'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    has_modified_residue: Optional[list[AbstractModifiedResidue]] = Field(default=None, description="""Modified residue feature borne by a sequence-based physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports phosphorylation, cleavage, ubiquitination, and related '
                      'residue-level state modeling.'],
         'domain_of': ['sequence_entity'],
         'slot_uri': 'reactome:hasModifiedResidue'} })
    start_coordinate: Optional[int] = Field(default=None, description="""Start coordinate of a subsequence, fragment, or feature-bearing region on a sequence entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for proteolytic fragments, domains, and sequence-trimmed '
                      'entity forms.'],
         'domain_of': ['sequence_entity'],
         'slot_uri': 'reactome:startCoordinate'} })
    end_coordinate: Optional[int] = Field(default=None, description="""End coordinate of a subsequence, fragment, or feature-bearing region on a sequence entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically paired with start_coordinate.'],
         'domain_of': ['sequence_entity'],
         'slot_uri': 'reactome:endCoordinate'} })
    sequence_reference_type: Optional[str] = Field(default=None, description="""Textual qualifier for the kind of referenced sequence or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Included for compatibility with Reactome exports.'],
         'domain_of': ['sequence_entity'],
         'slot_uri': 'reactome:sequenceReferenceType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Complex(PhysicalEntity):
    """
    Physical entity composed of two or more component physical entities assembled into a functional complex.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Complex',
         'comments': ['The complex is treated as an entity distinct from its '
                      'components.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_component': {'name': 'has_component', 'required': True}}})

    has_component: list[PhysicalEntity] = Field(default=..., description="""Component physical entities that make up a complex.""", json_schema_extra = { "linkml_meta": {'comments': ['Complex identity is distinct from component identity in '
                      'Reactome.'],
         'domain_of': ['complex'],
         'slot_uri': 'reactome:hasComponent'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class EntitySet(PhysicalEntity):
    """
    Curated set of physical entities that are treated as functionally interchangeable in a given biological context.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:EntitySet',
         'comments': ['This is a graph object representing a curated set, not merely a '
                      'class extension over its members.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_member': {'name': 'has_member', 'required': True}}})

    has_member: list[PhysicalEntity] = Field(default=..., description="""Members of an entity set representing functionally interchangeable participants.""", json_schema_extra = { "linkml_meta": {'comments': ['Entity sets are curated graph objects, not simply OWL classes '
                      'over their members.'],
         'domain_of': ['entity_set'],
         'slot_uri': 'reactome:hasMember'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class CandidateSet(EntitySet):
    """
    Entity set whose members are candidates for fulfilling a shared biological role.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:CandidateSet',
         'comments': ['Often reflects partial knowledge or broad functional grouping.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_member: list[PhysicalEntity] = Field(default=..., description="""Members of an entity set representing functionally interchangeable participants.""", json_schema_extra = { "linkml_meta": {'comments': ['Entity sets are curated graph objects, not simply OWL classes '
                      'over their members.'],
         'domain_of': ['entity_set'],
         'slot_uri': 'reactome:hasMember'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class DefinedSet(EntitySet):
    """
    Entity set whose members are explicitly curated as the intended interchangeable participants.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:DefinedSet',
         'comments': ['Stronger editorial commitment than a candidate set.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_member: list[PhysicalEntity] = Field(default=..., description="""Members of an entity set representing functionally interchangeable participants.""", json_schema_extra = { "linkml_meta": {'comments': ['Entity sets are curated graph objects, not simply OWL classes '
                      'over their members.'],
         'domain_of': ['entity_set'],
         'slot_uri': 'reactome:hasMember'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Polymer(PhysicalEntity):
    """
    Polymer entity abstracted in terms of one or more repeated units.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Polymer',
         'comments': ['Useful for biological polymers that are not modeled by '
                      'enumerating every monomer instance.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_repeated_unit: Optional[list[PhysicalEntity]] = Field(default=None, description="""Repeated unit composing a polymer entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Used when Reactome models a polymer abstractly in terms of '
                      'repeating constituents.'],
         'domain_of': ['polymer'],
         'slot_uri': 'reactome:hasRepeatedUnit'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Cell(PhysicalEntity):
    """
    Cell or cell-like biological unit treated as a physical participant in an event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Cell',
         'comments': ['Included for cases where cells themselves are modeled as '
                      'interacting biological entities.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class OtherEntity(PhysicalEntity):
    """
    Catch-all physical entity class for biologically relevant participants not covered by more specific subclasses.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:OtherEntity',
         'comments': ['Helps preserve source fidelity when Reactome uses residual '
                      'categorization.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Drug(PhysicalEntity):
    """
    Therapeutic or intervention-oriented physical entity modeled in the Reactome graph.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Drug',
         'comments': ['Drug subclasses distinguish broad molecular kinds of '
                      'therapeutic agents.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ChemicalDrug(Drug):
    """
    Drug represented primarily as a chemical or small-molecule therapeutic agent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ChemicalDrug',
         'comments': ['Often alignable to small-molecule reference identities.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ProteinDrug(Drug):
    """
    Drug represented as a protein therapeutic or protein-derived biologic.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ProteinDrug',
         'comments': ['Includes antibody-like or recombinant protein therapeutics when '
                      'modeled as physical entities.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class RnaDrug(Drug):
    """
    Drug represented as an RNA-based therapeutic agent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:RnaDrug',
         'comments': ['Can cover antisense, siRNA, or related RNA therapeutic '
                      'modalities.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:hasGoCellularComponent'} })
    systematic_name: Optional[str] = Field(default=None, description="""Formal or systematic name for an entity when available.""", json_schema_extra = { "linkml_meta": {'comments': ['Often useful for chemicals, complexes, or sequence-derived '
                      'entities.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:systematicName'} })
    is_in_disease_context: Optional[bool] = Field(default=None, description="""Boolean flag indicating that the represented entity is contextualized to a disease state.""", json_schema_extra = { "linkml_meta": {'comments': ['This is a contextual flag and does not by itself define a '
                      'disease ontology class.'],
         'domain_of': ['physical_entity'],
         'slot_uri': 'reactome:isInDiseaseContext'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceEntity(DatabaseObject):
    """
    Invariant reference identity used to connect multiple contextualized physical entities that share an underlying molecular identity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:ReferenceEntity',
         'comments': ['This is the key abstraction Reactome uses to separate '
                      'contextual state from canonical identity.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_reference_database': {'name': 'has_reference_database',
                                                   'required': True}}})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceSequence(ReferenceEntity):
    """
    Reference identity for a sequence-bearing biomolecule.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceSequence',
         'comments': ['Commonly used for protein, DNA, RNA, and isoform references.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceGeneProduct(ReferenceSequence):
    """
    Reference sequence corresponding to a gene product, typically protein-centric.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceGeneProduct',
         'comments': ['Often alignable to UniProt entries for proteins.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceIsoform(ReferenceSequence):
    """
    Reference sequence representing a specific isoform-level identity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceIsoform',
         'comments': ['Useful when isoform distinction matters biologically.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceDnaSequence(ReferenceSequence):
    """
    Reference identity for a DNA sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceDnaSequence',
         'comments': ['Supports DNA-centric entities in the Reactome schema.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceRnaSequence(ReferenceSequence):
    """
    Reference identity for an RNA sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceRnaSequence',
         'comments': ['Supports transcript and RNA molecule identity modeling.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceMolecule(ReferenceEntity):
    """
    Reference identity for a small molecule, simple chemical, or chemically grounded participant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceMolecule',
         'comments': ['Naturally alignable to ChEBI-like references.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceGroup(ReferenceEntity):
    """
    Grouped reference identity used when an invariant identity is represented at a grouped rather than single-entry level.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceGroup',
         'comments': ['Useful for families or grouped reference semantics in source '
                      'data.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceTherapeutic(ReferenceEntity):
    """
    Reference identity for a therapeutic or intervention-oriented entity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceTherapeutic',
         'comments': ['Supports the reference-layer counterpart of drug-like modeled '
                      'entities.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReferenceDatabase(DatabaseObject):
    """
    Metadata record describing an external database or authority used for identifiers and cross-references.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceDatabase',
         'comments': ['Holds resolver and namespace information for identifier '
                      'interpretation.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    access_url: Optional[str] = Field(default=None, description="""URL template or access URL used to resolve an identifier in a reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Can encode direct or templated resolver behavior.'],
         'domain_of': ['reference_database'],
         'slot_uri': 'reactome:accessUrl'} })
    identifier_prefix: Optional[str] = Field(default=None, description="""Prefix or namespace abbreviation used by a reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for CURIE generation and namespace harmonization.'],
         'domain_of': ['reference_database'],
         'slot_uri': 'reactome:identifierPrefix'} })
    resource_identifier: Optional[str] = Field(default=None, description="""Identifier for the reference resource itself rather than for entries inside it.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports metadata about the authority record for a database.'],
         'domain_of': ['reference_database'],
         'slot_uri': 'reactome:resourceIdentifier'} })
    url: Optional[str] = Field(default=None, description="""General URL associated with an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often used for resource metadata pages or resolver entry '
                      'points.'],
         'domain_of': ['reference_database'],
         'slot_uri': 'reactome:url'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class DatabaseIdentifier(DatabaseObject):
    """
    Cross-reference record that pairs an identifier string with a reference database authority.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:DatabaseIdentifier',
         'comments': ['Useful as a reified identifier object rather than a bare '
                      'literal.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    has_reference_database: Optional[str] = Field(default=None, description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class CatalystActivity(DatabaseObject):
    """
    Reified catalytic assertion connecting a catalyst bearer, a GO molecular function, and one or more catalyzed reaction-like events.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:CatalystActivity',
         'comments': ['This is one of the most semantically important reified node '
                      'types in Reactome.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_catalyst': {'name': 'has_catalyst', 'required': True},
                        'has_go_molecular_function': {'name': 'has_go_molecular_function',
                                                      'required': True}}})

    has_catalyst: str = Field(default=..., description="""Physical entity serving as the bearer of a catalyst activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Used inside reified catalyst activity objects.'],
         'domain_of': ['catalyst_activity'],
         'slot_uri': 'reactome:hasCatalyst'} })
    has_go_molecular_function: str = Field(default=..., description="""GO molecular function term asserted in a catalyst activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome reifies catalysis so the molecular function can be '
                      'attached explicitly.'],
         'domain_of': ['catalyst_activity'],
         'slot_uri': 'reactome:hasGoMolecularFunction'} })
    has_active_unit: Optional[list[PhysicalEntity]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    catalyzes: Optional[list[ReactionLikeEvent]] = Field(default=None, description="""Reaction-like event catalyzed by the given catalyst activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Allows one catalyst activity node to connect molecular function '
                      'and event participation.'],
         'domain_of': ['catalyst_activity'],
         'slot_uri': 'reactome:catalyzes'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Regulation(DatabaseObject):
    """
    Reified regulatory assertion linking a regulator physical entity to a regulated reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:Regulation',
         'comments': ['Reactome models regulation explicitly instead of flattening it '
                      'into a simple binary relation.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'slot_usage': {'has_regulator': {'name': 'has_regulator', 'required': True},
                        'regulates': {'name': 'regulates', 'required': True}}})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[PhysicalEntity]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class PositiveRegulation(Regulation):
    """
    Regulation that increases, enables, or positively influences the occurrence or efficiency of a reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:PositiveRegulation',
         'comments': ['Semantic polarity is explicit at the class level.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[PhysicalEntity]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class NegativeRegulation(Regulation):
    """
    Regulation that decreases, inhibits, or negatively influences the occurrence or efficiency of a reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:NegativeRegulation',
         'comments': ['Semantic polarity is explicit at the class level.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[PhysicalEntity]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Requirement(Regulation):
    """
    Regulation-like assertion indicating that a regulator or participant is required for a reaction-like event to occur.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Requirement',
         'comments': ['Used when necessity is the key biological relation rather than '
                      'positive or negative modulation.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[PhysicalEntity]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Interaction(DatabaseObject):
    """
    Interaction record associated with an event or set of participants.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Interaction',
         'comments': ['Retained as a distinct object to preserve graph fidelity when '
                      'interactions are explicitly modeled.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReactionTypeTerm(DatabaseObject):
    """
    Controlled vocabulary term used to characterize a reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReactionTypeTerm',
         'comments': ['Supports editorial or mechanistic grouping of reaction events.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class AbstractModifiedResidue(DatabaseObject):
    """
    Feature record describing a modified residue or residue-level state on a sequence-bearing entity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:AbstractModifiedResidue',
         'comments': ['Abstract superclass for phosphorylation-like or other residue '
                      'modification records.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class OrganismTaxon(DatabaseObject):
    """
    Organism taxon record representing the organismal context for entities and events.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:OrganismTaxon',
         'comments': ['Often associated with taxonomy identifiers and may correspond '
                      'to NCBI Taxonomy concepts.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    ncbi_taxon_id: Optional[str] = Field(default=None, description="""Taxonomic identifier, typically aligned to the NCBI Taxonomy.""", json_schema_extra = { "linkml_meta": {'comments': ['Often used on species or taxon-like records.'],
         'domain_of': ['organism_taxon', 'taxon'],
         'slot_uri': 'reactome:ncbiTaxonId'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('ncbi_taxon_id')
    def pattern_ncbi_taxon_id(cls, v):
        pattern=re.compile(r"^[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ncbi_taxon_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ncbi_taxon_id format: {v}"
            raise ValueError(err_msg)
        return v


class Taxon(DatabaseObject):
    """
    Taxonomic concept used for taxonomic assignment or metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Taxon',
         'comments': ['Can be used in parallel with or beneath species-oriented '
                      'records.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    ncbi_taxon_id: Optional[str] = Field(default=None, description="""Taxonomic identifier, typically aligned to the NCBI Taxonomy.""", json_schema_extra = { "linkml_meta": {'comments': ['Often used on species or taxon-like records.'],
         'domain_of': ['organism_taxon', 'taxon'],
         'slot_uri': 'reactome:ncbiTaxonId'} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('ncbi_taxon_id')
    def pattern_ncbi_taxon_id(cls, v):
        pattern=re.compile(r"^[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid ncbi_taxon_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid ncbi_taxon_id format: {v}"
            raise ValueError(err_msg)
        return v


class Compartment(DatabaseObject):
    """
    Cellular or subcellular location object used to state where an event occurs or where a physical entity resides.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Compartment',
         'comments': ['Often alignable to GO cellular component terms, though not '
                      'always identical in role.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class Disease(DatabaseObject):
    """
    Disease concept used to contextualize events and entities in pathological settings.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Disease',
         'comments': ['Represents disease context rather than a full disease ontology '
                      'commitment.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class GoMolecularFunctionTerm(DatabaseObject):
    """
    Wrapper object for a GO molecular function term used in Reactome catalysis modeling.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GoMolecularFunctionTerm',
         'comments': ['Particularly important in CatalystActivity.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class GoBiologicalProcessTerm(DatabaseObject):
    """
    Wrapper object for a GO biological process term used for pathway or event alignment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GoBiologicalProcessTerm',
         'comments': ['Useful for crosswalks between Reactome pathways and GO process '
                      'knowledge.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class GoCellularComponentTerm(DatabaseObject):
    """
    Wrapper object for a GO cellular component term used in entity or location annotation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GoCellularComponentTerm',
         'comments': ['Often complements explicit compartment modeling.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final'})

    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome DB_ID values are implementation-oriented identifiers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: str = Field(default=..., description="""Stable public Reactome identifier for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically corresponds to the curated Reactome stable accession '
                      'such as R-HSA-xxxxx.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeStableIdentifier'} })
    source_schema_class: str = Field(default=..., description="""Name of the source Reactome schema class from which the instance derives.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful when preserving frame-schema provenance or '
                      'round-tripping with the original Reactome graph.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:sourceSchemaClass'} })
    display_label: str = Field(default=..., description="""Preferred display label used by Reactome for user-facing presentation.""", json_schema_extra = { "linkml_meta": {'comments': ['Often combines identity and contextual state into a concise '
                      'label.'],
         'domain_of': ['database_object'],
         'is_a': 'name',
         'slot_uri': 'reactome:displayLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: str = Field(default=..., description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Usually points to an InstanceEdit containing editor and date '
                      'metadata.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Unique identifier for an instance in the serialized dataset.""", json_schema_extra = { "linkml_meta": {'comments': ['This may be a local identifier, CURIE, URI, or other '
                      'serialization key.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })


class ReactomeDataset(ConfiguredBaseModel):
    """
    Top-level container for a serialized Reactome dataset excerpt or export package.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['Provides a practical root object for JSON and YAML instance '
                      'data.'],
         'from_schema': 'https://w3id.org/reactome-ontology/final',
         'tree_root': True})

    database_objects: Optional[dict[str, DatabaseObject]] = Field(default=None, description="""Collection of Reactome objects keyed by identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['reactome_dataset']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedEntity.model_rebuild()
DatabaseObject.model_rebuild()
InstanceEdit.model_rebuild()
Publication.model_rebuild()
LiteratureReference.model_rebuild()
Person.model_rebuild()
Summation.model_rebuild()
Event.model_rebuild()
Pathway.model_rebuild()
ReactionLikeEvent.model_rebuild()
Reaction.model_rebuild()
BlackBoxEvent.model_rebuild()
Polymerization.model_rebuild()
Depolymerization.model_rebuild()
PhysicalEntity.model_rebuild()
SimpleEntity.model_rebuild()
GenomeEncodedEntity.model_rebuild()
SequenceEntity.model_rebuild()
Complex.model_rebuild()
EntitySet.model_rebuild()
CandidateSet.model_rebuild()
DefinedSet.model_rebuild()
Polymer.model_rebuild()
Cell.model_rebuild()
OtherEntity.model_rebuild()
Drug.model_rebuild()
ChemicalDrug.model_rebuild()
ProteinDrug.model_rebuild()
RnaDrug.model_rebuild()
ReferenceEntity.model_rebuild()
ReferenceSequence.model_rebuild()
ReferenceGeneProduct.model_rebuild()
ReferenceIsoform.model_rebuild()
ReferenceDnaSequence.model_rebuild()
ReferenceRnaSequence.model_rebuild()
ReferenceMolecule.model_rebuild()
ReferenceGroup.model_rebuild()
ReferenceTherapeutic.model_rebuild()
ReferenceDatabase.model_rebuild()
DatabaseIdentifier.model_rebuild()
CatalystActivity.model_rebuild()
Regulation.model_rebuild()
PositiveRegulation.model_rebuild()
NegativeRegulation.model_rebuild()
Requirement.model_rebuild()
Interaction.model_rebuild()
ReactionTypeTerm.model_rebuild()
AbstractModifiedResidue.model_rebuild()
OrganismTaxon.model_rebuild()
Taxon.model_rebuild()
Compartment.model_rebuild()
Disease.model_rebuild()
GoMolecularFunctionTerm.model_rebuild()
GoBiologicalProcessTerm.model_rebuild()
GoCellularComponentTerm.model_rebuild()
ReactomeDataset.model_rebuild()
