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
version = "1.1.0"


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
                  'Version 1.1.0 changes vs 1.0.0:',
                  '  - id slot: range changed from string to uriorcurie; pattern '
                  'added; construction strategy documented per class',
                  '  - ReactomeClassEnum added to document concrete class labels '
                  'used in serialized instances',
                  '  - reactome_stable_identifier: key:true added for UNIQUE '
                  'constraint generation',
                  '  - All slots with range pointing to a class: inlined:false '
                  'added explicitly',
                  '  - inlined_as_list removed from slots that are now '
                  'inlined:false (mutually exclusive)',
                  '  - New slots: synonym',
                  '  - authored slot moved to event class (was missing from event '
                  'slot list)',
                  '  - drug class: has_reference_entity slot added with '
                  'required:true, range:reference_therapeutic',
                  '  - Prefixes added: Ensembl, DOID',
                  '  - category slot added to database_object slots list',
                  '  - reactome_stable_identifier required:true removed from '
                  'database_object (absent on supporting nodes)'],
     'default_prefix': 'reactome',
     'default_range': 'string',
     'description': 'The Reactome Ontology Model provides a more ontology-oriented '
                    'and reusable representation of core parts of the Reactome '
                    'data model. Using LinkML as the source schema, it describes '
                    'entities, events, provenance, and related reference objects '
                    'in a consistent and structured way. The model covers '
                    'pathways, reactions, physical entities, regulatory '
                    'relationships, and supporting metadata through clearly '
                    'defined classes, slots, and ranges. This supports validation, '
                    'documentation generation, ontology export, and downstream '
                    'integration. Its goal is to provide a clear and interoperable '
                    'foundation for publishing and working with Reactome knowledge '
                    'in ontology-friendly formats.',
     'id': 'https://w3id.org/reactome-ontology',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/licenses/by/4.0/',
     'name': 'reactome_ontology',
     'prefixes': {'BFO': {'prefix_prefix': 'BFO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/BFO_'},
                  'CHEBI': {'prefix_prefix': 'CHEBI',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/CHEBI_'},
                  'DOID': {'prefix_prefix': 'DOID',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/DOID_'},
                  'Ensembl': {'prefix_prefix': 'Ensembl',
                              'prefix_reference': 'http://identifiers.org/ensembl/'},
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

class ReactomeClassEnum(str, Enum):
    """
    Closed enumeration of all concrete (non-abstract) Reactome class names used as values for the category discriminator slot.
    """
    Pathway = "Pathway"
    """
    Curated grouping of biologically related events.
    """
    Reaction = "Reaction"
    """
    Standard reaction-like event with balanced inputs and outputs.
    """
    BlackBoxEvent = "BlackBoxEvent"
    """
    Reaction-like event with incomplete mechanistic detail.
    """
    Polymerization = "Polymerization"
    """
    Polymer-forming reaction-like event.
    """
    Depolymerization = "Depolymerization"
    """
    Polymer-breaking reaction-like event.
    """
    SimpleEntity = "SimpleEntity"
    """
    Small molecule or non-sequence-based chemical participant.
    """
    GenomeEncodedEntity = "GenomeEncodedEntity"
    """
    Genome-encoded entity whose sequence is unknown.
    """
    SequenceEntity = "SequenceEntity"
    """
    Sequence-bearing physical entity with accession and optional modifications.
    """
    Protein = "Protein"
    """
    Protein physical entity linked to a reference gene product.
    """
    Complex = "Complex"
    """
    Multi-component physical entity.
    """
    DefinedSet = "DefinedSet"
    """
    Explicitly curated set of interchangeable physical entities.
    """
    CandidateSet = "CandidateSet"
    """
    Candidate set of physical entities fulfilling a shared role.
    """
    Polymer = "Polymer"
    """
    Polymer physical entity defined by repeated units.
    """
    Cell = "Cell"
    """
    Cell or cell-like biological unit.
    """
    OtherEntity = "OtherEntity"
    """
    Catch-all physical entity not covered by more specific subclasses.
    """
    Drug = "Drug"
    """
    Therapeutic physical entity.
    """
    ChemicalDrug = "ChemicalDrug"
    """
    Small-molecule therapeutic.
    """
    ProteinDrug = "ProteinDrug"
    """
    Protein-derived therapeutic.
    """
    RnaDrug = "RnaDrug"
    """
    RNA-based therapeutic.
    """
    ReferenceGeneProduct = "ReferenceGeneProduct"
    """
    Gene product reference identity, typically UniProt-backed.
    """
    ReferenceIsoform = "ReferenceIsoform"
    """
    Isoform-level reference identity.
    """
    ReferenceDnaSequence = "ReferenceDnaSequence"
    """
    DNA sequence reference identity.
    """
    ReferenceRnaSequence = "ReferenceRnaSequence"
    """
    RNA sequence reference identity.
    """
    ReferenceMolecule = "ReferenceMolecule"
    """
    Small-molecule reference identity, typically ChEBI-backed.
    """
    ReferenceGroup = "ReferenceGroup"
    """
    Grouped reference identity.
    """
    ReferenceTherapeutic = "ReferenceTherapeutic"
    """
    Therapeutic reference identity.
    """
    ReferenceDatabase = "ReferenceDatabase"
    """
    External database authority record.
    """
    DatabaseIdentifier = "DatabaseIdentifier"
    """
    Cross-reference identifier record.
    """
    CatalystActivity = "CatalystActivity"
    """
    Reified catalytic assertion.
    """
    PositiveRegulation = "PositiveRegulation"
    """
    Positive regulatory assertion.
    """
    NegativeRegulation = "NegativeRegulation"
    """
    Negative regulatory assertion.
    """
    Requirement = "Requirement"
    """
    Requirement-style regulatory assertion.
    """
    Interaction = "Interaction"
    """
    Interaction record.
    """
    AbstractModifiedResidue = "AbstractModifiedResidue"
    """
    Modified residue feature on a sequence entity.
    """
    OrganismTaxon = "OrganismTaxon"
    """
    Organism taxon record.
    """
    Taxon = "Taxon"
    """
    Taxonomic concept record.
    """
    Compartment = "Compartment"
    """
    Cellular compartment record.
    """
    Disease = "Disease"
    """
    Disease context record.
    """
    GoMolecularFunctionTerm = "GoMolecularFunctionTerm"
    """
    GO molecular function term wrapper.
    """
    GoBiologicalProcessTerm = "GoBiologicalProcessTerm"
    """
    GO biological process term wrapper.
    """
    GoCellularComponentTerm = "GoCellularComponentTerm"
    """
    GO cellular component term wrapper.
    """
    InstanceEdit = "InstanceEdit"
    """
    Provenance edit record.
    """
    LiteratureReference = "LiteratureReference"
    """
    Literature citation record.
    """
    Person = "Person"
    """
    Person record for provenance attribution.
    """
    Summation = "Summation"
    """
    Narrative summary record.
    """



class NamedEntity(ConfiguredBaseModel):
    """
    Generic named entity used as a lightweight semantic root for serializable objects.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:NamedEntity',
         'comments': ['Provides reusable identifier, naming, and descriptive slots '
                      'independent of the Reactome-specific hierarchy.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class DatabaseObject(NamedEntity):
    """
    Root class for most Reactome schema objects and the main provenance-bearing superclass.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:DatabaseObject',
         'comments': ["Reactome's frame-based model uses DatabaseObject as the common "
                      'ancestor for curated graph records.',
                      'id is constructed per class; see the id slot comments for the '
                      'full strategy.'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'display_label': {'name': 'display_label', 'required': True},
                        'reactome_db_id': {'name': 'reactome_db_id', 'required': True},
                        'source_schema_class': {'name': 'source_schema_class',
                                                'required': True}}})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class InstanceEdit(DatabaseObject):
    """
    Provenance record describing a curation action such as creation, modification, review, or revision.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:InstanceEdit',
         'comments': ['Typically stores who performed an edit and when the edit '
                      'occurred.',
                      'id construction: reactome:ie/{reactomeDbId}, e.g. '
                      'reactome:ie/54321',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    date: Optional[datetime ] = Field(default=None, description="""Timestamp or date string for the edit activity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['instance_edit']} })
    author: Optional[list[str]] = Field(default=None, description="""Person or people responsible for the edit activity.""", json_schema_extra = { "linkml_meta": {'domain_of': ['instance_edit']} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Publication(DatabaseObject):
    """
    Publication record used as evidence or supporting documentation for curated biology.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:Publication',
         'comments': ['Abstract superclass for specific publication-like records.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class LiteratureReference(Publication):
    """
    Literature citation record, commonly representing a PubMed-indexed paper supporting a Reactome assertion.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:LiteratureReference',
         'comments': ['Used widely to ground events, regulations, and catalyst '
                      'activities in the literature.',
                      'id construction: reactome:lit/{reactomeDbId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    pubmed_id: Optional[str] = Field(default=None, description="""PubMed identifier for a literature reference.""", json_schema_extra = { "linkml_meta": {'comments': ['Stored as string for broad interoperability with exports and '
                      'loaders.'],
         'domain_of': ['literature_reference'],
         'slot_uri': 'reactome:pubmedId'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
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

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Person(DatabaseObject):
    """
    Person record used primarily for provenance, authorship, and curation attribution.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Person',
         'comments': ['May represent curators, reviewers, or contributors.',
                      'id construction: orcid:{orcidId} when available; otherwise '
                      'reactome:person/{reactomeDbId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    orcid: Optional[str] = Field(default=None, description="""ORCID identifier for a person involved in curation or authorship.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for curator and contributor disambiguation.'],
         'domain_of': ['person'],
         'slot_uri': 'reactome:orcid'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Summation(DatabaseObject):
    """
    Narrative summary record containing prose that explains the biological meaning of an entity or event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Summation',
         'comments': ['Distinct from a formal definition; meant for human reading.',
                      'id construction: reactome:sum/{reactomeDbId}',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    text: str = Field(default=..., description="""Narrative summary text.""", json_schema_extra = { "linkml_meta": {'domain_of': ['summation']} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Event(DatabaseObject):
    """
    Biological occurrence or process unit in Reactome, covering both pathways and reaction-like events.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:Event',
         'comments': ['Event is one of the central abstractions in the Reactome model.',
                      'id construction for all Event subclasses: reactome:{stId}, e.g. '
                      'reactome:R-HSA-983169'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Pathway(Event):
    """
    Curated grouping of biologically related events representing a pathway or pathway-like module.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Pathway',
         'comments': ['Pathways can overlap; event membership is not exclusive.',
                      'id construction: reactome:{stId}, e.g. reactome:R-HSA-983169'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_event': {'name': 'has_event', 'required': True}}})

    has_event: list[str] = Field(default=..., description="""Membership relation linking a pathway to constituent events.""", json_schema_extra = { "linkml_meta": {'comments': ['Pathways in Reactome are curated groupings of events and can '
                      'overlap with other pathways.',
                      'inlined:false so that events are stored as references, not '
                      'embedded objects.'],
         'domain_of': ['pathway'],
         'slot_uri': 'reactome:hasEvent'} })
    has_go_biological_process: Optional[str] = Field(default=None, description="""GO biological process term associated with a Reactome pathway or event.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful as a high-level semantic alignment rather than an exact '
                      'equivalence in all cases.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['pathway'],
         'slot_uri': 'reactome:hasGoBiologicalProcess'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReactionLikeEvent(Event):
    """
    Event in which physical entities participate as inputs, outputs, regulators, or catalysts in a transformation-like process.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:ReactionLikeEvent',
         'comments': ['Covers canonical reactions as well as black-box and '
                      'polymerization-style event subclasses.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_input: Optional[list[str]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[str]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[str]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[str]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[str]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[str]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.',
                      'inverse_of follows_event (derived); only one direction is '
                      'stored.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[str]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[str]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Reaction(ReactionLikeEvent):
    """
    Standard reaction-like event with explicit transformed inputs and outputs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Reaction',
         'comments': ['Best used for relatively well-resolved mechanistic conversions.',
                      'id construction: reactome:{stId}, e.g. reactome:R-HSA-1218823'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_input': {'name': 'has_input',
                                      'range': 'physical_entity',
                                      'required': True},
                        'has_output': {'name': 'has_output',
                                       'range': 'physical_entity',
                                       'required': True}}})

    has_input: list[str] = Field(default=..., description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: list[str] = Field(default=..., description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[str]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[str]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[str]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[str]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.',
                      'inverse_of follows_event (derived); only one direction is '
                      'stored.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[str]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[str]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class BlackBoxEvent(ReactionLikeEvent):
    """
    Reaction-like event included in the pathway model despite incomplete mechanistic detail.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:BlackBoxEvent',
         'comments': ['Useful when biological evidence supports the event but not a '
                      'full molecular mechanism.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_input: Optional[list[str]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[str]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[str]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[str]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[str]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[str]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.',
                      'inverse_of follows_event (derived); only one direction is '
                      'stored.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[str]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[str]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Polymerization(ReactionLikeEvent):
    """
    Event representing formation of a polymer from repeated or assembling units.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Polymerization',
         'comments': ['Kept distinct because its participant semantics can differ from '
                      'ordinary reaction balance.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_input: Optional[list[str]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[str]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[str]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[str]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[str]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[str]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.',
                      'inverse_of follows_event (derived); only one direction is '
                      'stored.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[str]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[str]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Depolymerization(ReactionLikeEvent):
    """
    Event representing breakdown of a polymer into constituent or smaller units.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Depolymerization',
         'comments': ['Complementary to polymerisation.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_input: Optional[list[str]] = Field(default=None, description="""Physical entity consumed, transformed, or otherwise used as an input to a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Inputs need not always be fully consumed in a strict '
                      'stoichiometric sense across all event subclasses.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInput'} })
    has_output: Optional[list[str]] = Field(default=None, description="""Physical entity produced by a reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['Output identity often reflects new compartment, modification '
                      'state, or assembly state.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasOutput'} })
    requires_component: Optional[list[str]] = Field(default=None, description="""Physical entity required for a reaction-like event but not modeled as a transforming input.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for contextual cofactors, platform components, or '
                      'required participants.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:requiresComponent'} })
    has_catalyst_activity: Optional[list[str]] = Field(default=None, description="""Catalyst activity associated with the reaction-like event.""", json_schema_extra = { "linkml_meta": {'comments': ['A central Reactome modeling pattern that preserves GO molecular '
                      'function and active-unit context.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasCatalystActivity'} })
    has_regulation: Optional[list[str]] = Field(default=None, description="""Reified regulation assertion attached to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports positive, negative, and requirement-style regulatory '
                      'semantics.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasRegulation'} })
    preceded_by: Optional[list[str]] = Field(default=None, description="""Event that occurs before the current event in a curated process sequence.""", json_schema_extra = { "linkml_meta": {'comments': ['Encodes partial ordering rather than necessarily strict '
                      'temporal or causal completeness.',
                      'inverse_of follows_event (derived); only one direction is '
                      'stored.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:precededBy'} })
    has_interacting_entity_on_other_cell: Optional[list[str]] = Field(default=None, description="""Physical entity located on another interacting cell in intercellular biology.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for immune, adhesion, and receptor-ligand interaction '
                      'contexts.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteractingEntityOnOtherCell'} })
    has_interaction: Optional[list[str]] = Field(default=None, description="""Associated interaction object linked to an event.""", json_schema_extra = { "linkml_meta": {'comments': ['Preserves interaction-level detail when Reactome models such '
                      'assertions explicitly.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasInteraction'} })
    has_reaction_type: Optional[list[str]] = Field(default=None, description="""Controlled reaction type annotation describing the mechanistic or editorial type of a reaction.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for grouping reaction-like events into broad mechanistic '
                      'categories.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['reaction_like_event'],
         'slot_uri': 'reactome:hasReactionType'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_summation: Optional[str] = Field(default=None, description="""Narrative summary object explaining the biology of an event or entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from formal definition; usually prose intended for '
                      'readers.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:hasSummation'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    reviewed: Optional[list[str]] = Field(default=None, description="""Provenance links to formal review actions on the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Distinct from simple modification in Reactome curation '
                      'workflows.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:reviewed'} })
    revised: Optional[list[str]] = Field(default=None, description="""Provenance links to explicit revision actions after prior curation or review.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful for tracking editorial iteration.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:revised'} })
    authored: Optional[list[str]] = Field(default=None, description="""Provenance links capturing authoring actions for the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Included to support richer editorial provenance when present in '
                      'exports.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event'],
         'slot_uri': 'reactome:authored'} })
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class PhysicalEntity(DatabaseObject):
    """
    Concrete biological participant whose identity reflects both underlying molecular identity and contextual state.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:PhysicalEntity',
         'comments': ['In Reactome, compartment, modification state, and assembly '
                      'state can distinguish one physical entity from another.',
                      'id construction for all PhysicalEntity subclasses: '
                      'reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class SimpleEntity(PhysicalEntity):
    """
    Simple molecular entity, typically a small molecule or other non-sequence-based chemical participant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:SimpleEntity',
         'comments': ['Commonly aligned to ChEBI-like reference identities through '
                      'ReferenceMolecule.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_reference_entity': {'name': 'has_reference_entity',
                                                 'range': 'reference_molecule',
                                                 'required': True}}})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class GenomeEncodedEntity(PhysicalEntity):
    """
    Physical entity whose existence is grounded in a genome-encoded product such as a protein or nucleic acid.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GenomeEncodedEntity',
         'comments': ['Serves as a superclass for accessioned sequence-based entities.',
                      'No referenceEntity slot; sequence is unknown for bare '
                      'GenomeEncodedEntity instances.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class SequenceEntity(GenomeEncodedEntity):
    """
    Sequence-bearing physical entity linked to a stable reference sequence and optionally decorated with residue modifications and subsequence coordinates.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:SequenceEntity',
         'comments': ['Core Reactome pattern for proteins, RNAs, and other accessioned '
                      'biomolecules in specific states.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_reference_entity': {'name': 'has_reference_entity',
                                                 'range': 'reference_sequence',
                                                 'required': True}}})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    has_modified_residue: Optional[list[str]] = Field(default=None, description="""Modified residue feature borne by a sequence-based physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports phosphorylation, cleavage, ubiquitination, and related '
                      'residue-level state modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
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
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Protein(SequenceEntity):
    """
    Protein physical entity linked to a reference gene product and optionally decorated with modifications and subsequence features.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Protein',
         'comments': ['The most common type of sequence entity in Reactome.',
                      'id construction: reactome:{stId}, e.g. reactome:R-HSA-199420'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_reference_entity': {'name': 'has_reference_entity',
                                                 'range': 'reference_gene_product',
                                                 'required': True}}})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    has_modified_residue: Optional[list[str]] = Field(default=None, description="""Modified residue feature borne by a sequence-based physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Supports phosphorylation, cleavage, ubiquitination, and related '
                      'residue-level state modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
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
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Complex(PhysicalEntity):
    """
    Physical entity composed of two or more component physical entities assembled into a functional complex.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Complex',
         'comments': ['The complex is treated as an entity distinct from its '
                      'components.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_component': {'name': 'has_component', 'required': True}}})

    has_component: list[str] = Field(default=..., description="""Component physical entities that make up a complex.""", json_schema_extra = { "linkml_meta": {'comments': ['Complex identity is distinct from component identity in '
                      'Reactome.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['complex'],
         'slot_uri': 'reactome:hasComponent'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class EntitySet(PhysicalEntity):
    """
    Curated set of physical entities that are treated as functionally interchangeable in a given biological context.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:EntitySet',
         'comments': ['This is a graph object representing a curated set, not merely a '
                      'class extension over its members.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_member': {'name': 'has_member', 'required': True}}})

    has_member: list[str] = Field(default=..., description="""Members of an entity set representing functionally interchangeable participants.""", json_schema_extra = { "linkml_meta": {'comments': ['Entity sets are curated graph objects, not simply OWL classes '
                      'over their members.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['entity_set'],
         'slot_uri': 'reactome:hasMember'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateSet(EntitySet):
    """
    Entity set whose members are candidates for fulfilling a shared biological role.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:CandidateSet',
         'comments': ['Often reflects partial knowledge or broad functional grouping.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_member: list[str] = Field(default=..., description="""Members of an entity set representing functionally interchangeable participants.""", json_schema_extra = { "linkml_meta": {'comments': ['Entity sets are curated graph objects, not simply OWL classes '
                      'over their members.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['entity_set'],
         'slot_uri': 'reactome:hasMember'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class DefinedSet(EntitySet):
    """
    Entity set whose members are explicitly curated as the intended interchangeable participants.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:DefinedSet',
         'comments': ['Stronger editorial commitment than a candidate set.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_member: list[str] = Field(default=..., description="""Members of an entity set representing functionally interchangeable participants.""", json_schema_extra = { "linkml_meta": {'comments': ['Entity sets are curated graph objects, not simply OWL classes '
                      'over their members.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['entity_set'],
         'slot_uri': 'reactome:hasMember'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Polymer(PhysicalEntity):
    """
    Polymer entity abstracted in terms of one or more repeated units.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Polymer',
         'comments': ['Useful for biological polymers that are not modeled by '
                      'enumerating every monomer instance.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_repeated_unit: Optional[list[str]] = Field(default=None, description="""Repeated unit composing a polymer entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Used when Reactome models a polymer abstractly in terms of '
                      'repeating constituents.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['polymer'],
         'slot_uri': 'reactome:hasRepeatedUnit'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Cell(PhysicalEntity):
    """
    Cell or cell-like biological unit treated as a physical participant in an event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Cell',
         'comments': ['Included for cases where cells themselves are modeled as '
                      'interacting biological entities.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class OtherEntity(PhysicalEntity):
    """
    Catch-all physical entity class for biologically relevant participants not covered by more specific subclasses.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:OtherEntity',
         'comments': ['Helps preserve source fidelity when Reactome uses residual '
                      'categorization.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Drug(PhysicalEntity):
    """
    Therapeutic or intervention-oriented physical entity modeled in the Reactome graph.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Drug',
         'comments': ['Drug subclasses distinguish broad molecular kinds of '
                      'therapeutic agents.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_reference_entity': {'name': 'has_reference_entity',
                                                 'range': 'reference_therapeutic',
                                                 'required': True}}})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ChemicalDrug(Drug):
    """
    Drug represented primarily as a chemical or small-molecule therapeutic agent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ChemicalDrug',
         'comments': ['Often alignable to small-molecule reference identities.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ProteinDrug(Drug):
    """
    Drug represented as a protein therapeutic or protein-derived biologic.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ProteinDrug',
         'comments': ['Includes antibody-like or recombinant protein therapeutics when '
                      'modeled as physical entities.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class RnaDrug(Drug):
    """
    Drug represented as an RNA-based therapeutic agent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:RnaDrug',
         'comments': ['Can cover antisense, siRNA, or related RNA therapeutic '
                      'modalities.',
                      'id construction: reactome:{stId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_entity: str = Field(default=..., description="""Invariant reference identity underlying a contextualized physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['One of the key distinctions in Reactome; reference identity is '
                      'separate from stateful physical instantiation.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['simple_entity', 'sequence_entity', 'drug'],
         'slot_uri': 'reactome:hasReferenceEntity'} })
    in_taxon: Optional[list[str]] = Field(default=None, description="""Taxon in which the object, event, or entity is asserted to occur or be defined.""", json_schema_extra = { "linkml_meta": {'comments': ['For events this denotes the organism context; for entities it '
                      'denotes the biological source organism.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:inTaxon'} })
    located_in_compartment: Optional[list[str]] = Field(default=None, description="""Compartment in which an entity resides or an event occurs.""", json_schema_extra = { "linkml_meta": {'comments': ['In Reactome, compartment is identity-relevant for many physical '
                      'entities.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:locatedInCompartment'} })
    has_cross_reference: Optional[list[str]] = Field(default=None, description="""External cross-reference to another database or controlled resource.""", json_schema_extra = { "linkml_meta": {'comments': ['Used for interoperating with identifiers from GO, ChEBI, '
                      'UniProt, Ensembl, and related resources.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasCrossReference'} })
    has_disease_context: Optional[list[str]] = Field(default=None, description="""Disease context associated with an event or physical entity.""", json_schema_extra = { "linkml_meta": {'comments': ['Represents contextual disease association rather than broad '
                      'etiologic modeling.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'physical_entity'],
         'slot_uri': 'reactome:hasDiseaseContext'} })
    has_go_cellular_component: Optional[str] = Field(default=None, description="""GO cellular component term associated with a physical entity or event context.""", json_schema_extra = { "linkml_meta": {'comments': ['Often complements the explicit compartment modeling in '
                      'Reactome.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceEntity(DatabaseObject):
    """
    Invariant reference identity used to connect multiple contextualized physical entities that share an underlying molecular identity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:ReferenceEntity',
         'comments': ['This is the key abstraction Reactome uses to separate '
                      'contextual state from canonical identity.',
                      'id construction varies by subclass; see individual class '
                      'comments.'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_reference_database': {'name': 'has_reference_database',
                                                   'required': True}}})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceSequence(ReferenceEntity):
    """
    Reference identity for a sequence-bearing biomolecule.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceSequence',
         'comments': ['Commonly used for protein, DNA, RNA, and isoform references.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceGeneProduct(ReferenceSequence):
    """
    Reference sequence corresponding to a gene product, typically protein-centric.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceGeneProduct',
         'comments': ['Often alignable to UniProt entries for proteins.',
                      'id construction: UniProtKB:{identifier}, e.g. UniProtKB:P60484'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceIsoform(ReferenceSequence):
    """
    Reference sequence representing a specific isoform-level identity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceIsoform',
         'comments': ['Useful when isoform distinction matters biologically.',
                      'id construction: UniProtKB:{variantIdentifier}, e.g. '
                      'UniProtKB:P60484-2'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceDnaSequence(ReferenceSequence):
    """
    Reference identity for a DNA sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceDnaSequence',
         'comments': ['Supports DNA-centric entities in the Reactome schema.',
                      'id construction: Ensembl:{identifier}, e.g. '
                      'Ensembl:ENSG00000141510'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceRnaSequence(ReferenceSequence):
    """
    Reference identity for an RNA sequence.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceRnaSequence',
         'comments': ['Supports transcript and RNA molecule identity modeling.',
                      'id construction: Ensembl:{identifier}, e.g. '
                      'Ensembl:ENST00000269305'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceMolecule(ReferenceEntity):
    """
    Reference identity for a small molecule, simple chemical, or chemically grounded participant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceMolecule',
         'comments': ['Naturally alignable to ChEBI-like references.',
                      'id construction: CHEBI:{identifier}, e.g. CHEBI:15422'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceGroup(ReferenceEntity):
    """
    Grouped reference identity used when an invariant identity is represented at a grouped rather than single-entry level.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceGroup',
         'comments': ['Useful for families or grouped reference semantics in source '
                      'data.',
                      'id construction: reactome:refgroup/{reactomeDbId} (no standard '
                      'external DB)'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceTherapeutic(ReferenceEntity):
    """
    Reference identity for a therapeutic or intervention-oriented entity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceTherapeutic',
         'comments': ['Supports the reference-layer counterpart of drug-like modeled '
                      'entities.',
                      'id construction: reactome:refther/{reactomeDbId} (no single '
                      'standard external DB)'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_reference_database: str = Field(default=..., description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReferenceDatabase(DatabaseObject):
    """
    Metadata record describing an external database or authority used for identifiers and cross-references.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReferenceDatabase',
         'comments': ['Holds resolver and namespace information for identifier '
                      'interpretation.',
                      'id construction: reactome:db/{displayName}, e.g. '
                      'reactome:db/UniProt',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

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
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class DatabaseIdentifier(DatabaseObject):
    """
    Cross-reference record that pairs an identifier string with a reference database authority.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:DatabaseIdentifier',
         'comments': ['Useful as a reified identifier object rather than a bare '
                      'literal.',
                      'id construction: reactome:xref/{reactomeDbId}',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    identifier: Optional[str] = Field(default=None, description="""Identifier string assigned by an external reference database.""", json_schema_extra = { "linkml_meta": {'comments': ['Examples include UniProt accessions, ChEBI identifiers, or GO '
                      'term identifiers.',
                      'This is the raw accession string; the full CURIE form is stored '
                      'in the id slot.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:identifier'} })
    has_reference_database: Optional[str] = Field(default=None, description="""Reference database authority associated with a reference entity or database identifier.""", json_schema_extra = { "linkml_meta": {'comments': ['Provides the namespace and interpretation context for an '
                      'identifier.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['reference_entity', 'database_identifier'],
         'slot_uri': 'reactome:hasReferenceDatabase'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class CatalystActivity(DatabaseObject):
    """
    Reified catalytic assertion connecting a catalyst bearer, a GO molecular function, and one or more catalyzed reaction-like events.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:CatalystActivity',
         'comments': ['This is one of the most semantically important reified node '
                      'types in Reactome.',
                      'id construction: reactome:ca/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_catalyst': {'name': 'has_catalyst', 'required': True},
                        'has_go_molecular_function': {'name': 'has_go_molecular_function',
                                                      'required': True}}})

    has_catalyst: str = Field(default=..., description="""Physical entity serving as the bearer of a catalyst activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Used inside reified catalyst activity objects.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['catalyst_activity'],
         'slot_uri': 'reactome:hasCatalyst'} })
    has_go_molecular_function: str = Field(default=..., description="""GO molecular function term asserted in a catalyst activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome reifies catalysis so the molecular function can be '
                      'attached explicitly.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['catalyst_activity'],
         'slot_uri': 'reactome:hasGoMolecularFunction'} })
    has_active_unit: Optional[list[str]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    catalyzes: Optional[list[str]] = Field(default=None, description="""Reaction-like event catalyzed by the given catalyst activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Allows one catalyst activity node to connect molecular function '
                      'and event participation.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['catalyst_activity'],
         'slot_uri': 'reactome:catalyzes'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Regulation(DatabaseObject):
    """
    Reified regulatory assertion linking a regulator physical entity to a regulated reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'reactome:Regulation',
         'comments': ['Reactome models regulation explicitly instead of flattening it '
                      'into a simple binary relation.',
                      'id construction for all Regulation subclasses: '
                      'reactome:reg/{reactomeDbId}',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology',
         'slot_usage': {'has_regulator': {'name': 'has_regulator', 'required': True},
                        'regulates': {'name': 'regulates', 'required': True}}})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[str]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class PositiveRegulation(Regulation):
    """
    Regulation that increases, enables, or positively influences the occurrence or efficiency of a reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:PositiveRegulation',
         'comments': ['Semantic polarity is explicit at the class level.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[str]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class NegativeRegulation(Regulation):
    """
    Regulation that decreases, inhibits, or negatively influences the occurrence or efficiency of a reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:NegativeRegulation',
         'comments': ['Semantic polarity is explicit at the class level.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[str]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Requirement(Regulation):
    """
    Regulation-like assertion indicating that a regulator or participant is required for a reaction-like event to occur.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Requirement',
         'comments': ['Used when necessity is the key biological relation rather than '
                      'positive or negative modulation.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    has_regulator: str = Field(default=..., description="""Physical entity that exerts regulatory influence on a regulated event.""", json_schema_extra = { "linkml_meta": {'comments': ['May be a protein, complex, small molecule, set, or other '
                      'physical entity.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:hasRegulator'} })
    regulates: str = Field(default=..., description="""Reaction-like event that is the target of regulation.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept explicit through reified regulation nodes rather than '
                      'flattened triples.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge.'],
         'domain_of': ['regulation'],
         'slot_uri': 'reactome:regulates'} })
    has_active_unit: Optional[list[str]] = Field(default=None, description="""Subunit, domain-bearing fragment, or active molecular portion responsible for catalytic or regulatory activity.""", json_schema_extra = { "linkml_meta": {'comments': ['Reactome can attach active-unit detail to catalyst activities '
                      'and regulation objects.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:hasActiveUnit'} })
    supported_by: Optional[list[str]] = Field(default=None, description="""Publication supporting the existence, mechanism, or curation of the object.""", json_schema_extra = { "linkml_meta": {'comments': ['Often points to PubMed-backed literature references.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['event', 'catalyst_activity', 'regulation'],
         'slot_uri': 'reactome:supportedBy'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Interaction(DatabaseObject):
    """
    Interaction record associated with an event or set of participants.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Interaction',
         'comments': ['Retained as a distinct object to preserve graph fidelity when '
                      'interactions are explicitly modeled.',
                      'id construction: reactome:int/{reactomeDbId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReactionTypeTerm(DatabaseObject):
    """
    Controlled vocabulary term used to characterize a reaction-like event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:ReactionTypeTerm',
         'comments': ['Supports editorial or mechanistic grouping of reaction events.',
                      'id construction: reactome:rxntype/{reactomeDbId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class AbstractModifiedResidue(DatabaseObject):
    """
    Feature record describing a modified residue or residue-level state on a sequence-bearing entity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:AbstractModifiedResidue',
         'comments': ['Abstract superclass for phosphorylation-like or other residue '
                      'modification records.',
                      'id construction: reactome:mod/{reactomeDbId}',
                      'No stId exists for this class; reactome_stable_identifier is '
                      'absent.'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class OrganismTaxon(DatabaseObject):
    """
    Organism taxon record representing the organismal context for entities and events.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:OrganismTaxon',
         'comments': ['Often associated with taxonomy identifiers and may correspond '
                      'to NCBI Taxonomy concepts.',
                      'id construction: NCBITaxon:{ncbiTaxonId}, e.g. NCBITaxon:9606'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    ncbi_taxon_id: Optional[str] = Field(default=None, description="""Taxonomic identifier aligned to the NCBI Taxonomy.""", json_schema_extra = { "linkml_meta": {'comments': ['Used on OrganismTaxon and Taxon records.',
                      'The id slot on these nodes is constructed as '
                      'NCBITaxon:{ncbi_taxon_id}.'],
         'domain_of': ['organism_taxon', 'taxon'],
         'slot_uri': 'reactome:ncbiTaxonId'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
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

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Taxon(DatabaseObject):
    """
    Taxonomic concept used for taxonomic assignment or metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Taxon',
         'comments': ['Can be used in parallel with or beneath species-oriented '
                      'records.',
                      'id construction: NCBITaxon:{ncbiTaxonId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    ncbi_taxon_id: Optional[str] = Field(default=None, description="""Taxonomic identifier aligned to the NCBI Taxonomy.""", json_schema_extra = { "linkml_meta": {'comments': ['Used on OrganismTaxon and Taxon records.',
                      'The id slot on these nodes is constructed as '
                      'NCBITaxon:{ncbi_taxon_id}.'],
         'domain_of': ['organism_taxon', 'taxon'],
         'slot_uri': 'reactome:ncbiTaxonId'} })
    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
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

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Compartment(DatabaseObject):
    """
    Cellular or subcellular location object used to state where an event occurs or where a physical entity resides.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Compartment',
         'comments': ['Often alignable to GO cellular component terms.',
                      'id construction: GO:{goIdentifier}, e.g. GO:0005737 for '
                      'cytosol'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Disease(DatabaseObject):
    """
    Disease concept used to contextualize events and entities in pathological settings.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:Disease',
         'comments': ['Represents disease context rather than a full disease ontology '
                      'commitment.',
                      'id construction: DOID:{identifier} where available, e.g. '
                      'DOID:162; otherwise reactome:disease/{reactomeDbId}'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class GoMolecularFunctionTerm(DatabaseObject):
    """
    Wrapper object for a GO molecular function term used in Reactome catalysis modeling.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GoMolecularFunctionTerm',
         'comments': ['Particularly important in CatalystActivity.',
                      'id construction: GO:{identifier}, e.g. GO:0004672'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class GoBiologicalProcessTerm(DatabaseObject):
    """
    Wrapper object for a GO biological process term used for pathway or event alignment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GoBiologicalProcessTerm',
         'comments': ['Useful for crosswalks between Reactome pathways and GO process '
                      'knowledge.',
                      'id construction: GO:{identifier}, e.g. GO:0008150'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class GoCellularComponentTerm(DatabaseObject):
    """
    Wrapper object for a GO cellular component term used in entity or location annotation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'reactome:GoCellularComponentTerm',
         'comments': ['Often complements explicit compartment modeling.',
                      'id construction: GO:{identifier}, e.g. GO:0005737'],
         'from_schema': 'https://w3id.org/reactome-ontology'})

    category: Optional[str] = Field(default=None, description="""Concrete class discriminator used in serialized instances.""", json_schema_extra = { "linkml_meta": {'comments': ["Must remain range:string. LinkML's pythongen requires the "
                      'designates_type slot to carry a plain string class name and '
                      'does not support an enum range here.',
                      'The ReactomeClassEnum in this schema documents the closed '
                      'vocabulary of valid values and is used by JSON Schema and OWL '
                      'generators, but cannot be referenced directly by this slot '
                      'without breaking gen-python.',
                      'Valid values are the permissible_values keys of '
                      'ReactomeClassEnum, e.g. Pathway, Reaction, '
                      'EntityWithAccessionedSequence, CatalystActivity, etc.'],
         'domain_of': ['database_object']} })
    reactome_db_id: int = Field(default=..., description="""Internal Reactome database identifier assigned to a database object.""", json_schema_extra = { "linkml_meta": {'comments': ['Kept for provenance and round-tripping only; never used as a '
                      'foreign key in this ontology schema.',
                      'Reactome DB_ID values are implementation-oriented integers '
                      'rather than stable public identifiers.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:reactomeDbId'} })
    reactome_stable_identifier: Optional[str] = Field(default=None, description="""Stable public Reactome identifier for an object, where one exists.""", json_schema_extra = { "linkml_meta": {'comments': ['Typically the R-HSA-xxxxx accession assigned to curated '
                      'biological objects.',
                      'Present on Events, PhysicalEntities, and ReferenceEntities; '
                      'absent on supporting nodes such as CatalystActivity, '
                      'InstanceEdit, and Summation.',
                      'Not marked key:true because LinkML only permits one identifier '
                      'per class hierarchy (id already serves that role). Downstream '
                      'generators (SQL DDL, Neo4j Cypher) should add a UNIQUE '
                      'constraint / index on this column independently, using the '
                      'source_schema_class or class label to scope it to classes where '
                      'it is populated.'],
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
    synonym: Optional[list[str]] = Field(default=None, description="""Alternative names or synonyms for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['For Reactome DatabaseObject records, this can capture '
                      'additional values from the source name list after the first '
                      'value is used as the primary name.'],
         'domain_of': ['database_object'],
         'slot_uri': 'skos:altLabel'} })
    definition: Optional[str] = Field(default=None, description="""Curated textual definition that states what the object is.""", json_schema_extra = { "linkml_meta": {'comments': ['Intended for conceptual definitions rather than narrative '
                      'summaries.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:definition'} })
    previous_stable_identifier: Optional[str] = Field(default=None, description="""Deprecated or previous stable Reactome identifier retained for traceability.""", json_schema_extra = { "linkml_meta": {'comments': ['Useful during migration, identifier replacement, and legacy '
                      'resolution.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:previousStableIdentifier'} })
    created: Optional[str] = Field(default=None, description="""Provenance link to the curation event that originally created the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Points to an InstanceEdit node containing editor and date '
                      'metadata.',
                      'inlined:false ensures generators emit a foreign key or graph '
                      'edge, not an embedded object.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:created'} })
    modified: Optional[list[str]] = Field(default=None, description="""Provenance links to subsequent modifications of the object record.""", json_schema_extra = { "linkml_meta": {'comments': ['Multiple modifications are common across curation history.',
                      'inlined:false ensures generators emit foreign keys or graph '
                      'edges.'],
         'domain_of': ['database_object'],
         'slot_uri': 'reactome:modified'} })
    id: str = Field(default=..., description="""Primary stable identifier for an instance, stored as a CURIE or URI.""", json_schema_extra = { "linkml_meta": {'comments': ['Construction strategy varies by class (see class-level comments '
                      'for details).',
                      'Biological objects (Event, PhysicalEntity subclasses): '
                      'reactome:{stId}, e.g. reactome:R-HSA-983169',
                      'ReferenceGeneProduct / ReferenceIsoform: UniProtKB:{accession}, '
                      'e.g. UniProtKB:P60484',
                      'ReferenceDnaSequence / ReferenceRnaSequence: '
                      'Ensembl:{accession}',
                      'ReferenceMolecule: CHEBI:{id}, e.g. CHEBI:15422',
                      'OrganismTaxon / Taxon: NCBITaxon:{taxId}, e.g. NCBITaxon:9606',
                      'GO term wrappers and Compartment: GO:{id}, e.g. GO:0005737',
                      'Disease: DOID:{id} where available, e.g. DOID:162',
                      'Supporting nodes without stId (CatalystActivity, Regulation, '
                      'InstanceEdit, Summation, ReferenceDatabase, '
                      'ReferenceTherapeutic, ReferenceGroup): '
                      'reactome:{classPrefix}/{reactomeDbId}, e.g. '
                      'reactome:ca/1218822, reactome:ie/54321'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:identifier'} })
    name: Optional[str] = Field(default=None, description="""Human-readable primary label for an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Generic reusable naming slot for schema-wide use.',
                      'When the source Reactome name field is multivalued, the first '
                      'value is promoted here as the primary ontology label.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'rdfs:label'} })
    description: Optional[str] = Field(default=None, description="""Free-text textual description of an object.""", json_schema_extra = { "linkml_meta": {'comments': ['Can hold editorial notes, plain-language explanations, or short '
                      'summaries.'],
         'domain_of': ['named_entity'],
         'slot_uri': 'dcterms:description'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.+-]*:.+")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ReactomeDataset(ConfiguredBaseModel):
    """
    Top-level container for a serialized Reactome dataset excerpt or export package.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['Provides a practical root object for JSON and YAML instance '
                      'data.'],
         'from_schema': 'https://w3id.org/reactome-ontology',
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
Protein.model_rebuild()
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
