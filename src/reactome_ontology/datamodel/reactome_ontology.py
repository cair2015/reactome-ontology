# Auto generated from reactome_ontology.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-09T22:16:40
# Schema: reactome_ontology
#
# id: https://w3id.org/reactome-ontology/final
# description: A final OWL-oriented LinkML schema for generating a clean Reactome ontology. This profile keeps ontology-facing classes and properties and removes source-mapping annotations, which are maintained in separate mapping files.
# license: https://creativecommons.org/licenses/by/4.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import Bool, URI, XSDDate, XSDDateTime

metamodel_version = "1.7.0"
version = "1.0.0"

# Namespaces
BFO = CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_')
CHEBI = CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_')
GO = CurieNamespace('GO', 'http://purl.obolibrary.org/obo/GO_')
NCBITAXON = CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_')
RO = CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_')
UNIPROTKB = CurieNamespace('UniProtKB', 'http://purl.uniprot.org/uniprot/')
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/vocab/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
ORCID = CurieNamespace('orcid', 'https://orcid.org/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
REACTOME = CurieNamespace('reactome', 'https://w3id.org/reactome-ontology/')
REACTOMEID = CurieNamespace('reactomeid', 'https://w3id.org/reactome-ontology/id/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = REACTOME


# Types

# Class references
class NamedEntityId(extended_str):
    pass


class DatabaseObjectId(NamedEntityId):
    pass


class InstanceEditId(DatabaseObjectId):
    pass


class PublicationId(DatabaseObjectId):
    pass


class LiteratureReferenceId(PublicationId):
    pass


class PersonId(DatabaseObjectId):
    pass


class SummationId(DatabaseObjectId):
    pass


class EventId(DatabaseObjectId):
    pass


class PathwayId(EventId):
    pass


class ReactionLikeEventId(EventId):
    pass


class ReactionId(ReactionLikeEventId):
    pass


class BlackBoxEventId(ReactionLikeEventId):
    pass


class PolymerizationId(ReactionLikeEventId):
    pass


class DepolymerizationId(ReactionLikeEventId):
    pass


class PhysicalEntityId(DatabaseObjectId):
    pass


class SimpleEntityId(PhysicalEntityId):
    pass


class GenomeEncodedEntityId(PhysicalEntityId):
    pass


class SequenceEntityId(GenomeEncodedEntityId):
    pass


class ComplexId(PhysicalEntityId):
    pass


class EntitySetId(PhysicalEntityId):
    pass


class CandidateSetId(EntitySetId):
    pass


class DefinedSetId(EntitySetId):
    pass


class PolymerId(PhysicalEntityId):
    pass


class CellId(PhysicalEntityId):
    pass


class OtherEntityId(PhysicalEntityId):
    pass


class DrugId(PhysicalEntityId):
    pass


class ChemicalDrugId(DrugId):
    pass


class ProteinDrugId(DrugId):
    pass


class RnaDrugId(DrugId):
    pass


class ReferenceEntityId(DatabaseObjectId):
    pass


class ReferenceSequenceId(ReferenceEntityId):
    pass


class ReferenceGeneProductId(ReferenceSequenceId):
    pass


class ReferenceIsoformId(ReferenceSequenceId):
    pass


class ReferenceDnaSequenceId(ReferenceSequenceId):
    pass


class ReferenceRnaSequenceId(ReferenceSequenceId):
    pass


class ReferenceMoleculeId(ReferenceEntityId):
    pass


class ReferenceGroupId(ReferenceEntityId):
    pass


class ReferenceTherapeuticId(ReferenceEntityId):
    pass


class ReferenceDatabaseId(DatabaseObjectId):
    pass


class DatabaseIdentifierId(DatabaseObjectId):
    pass


class CatalystActivityId(DatabaseObjectId):
    pass


class RegulationId(DatabaseObjectId):
    pass


class PositiveRegulationId(RegulationId):
    pass


class NegativeRegulationId(RegulationId):
    pass


class RequirementId(RegulationId):
    pass


class InteractionId(DatabaseObjectId):
    pass


class ReactionTypeTermId(DatabaseObjectId):
    pass


class AbstractModifiedResidueId(DatabaseObjectId):
    pass


class OrganismTaxonId(DatabaseObjectId):
    pass


class TaxonId(DatabaseObjectId):
    pass


class CompartmentId(DatabaseObjectId):
    pass


class DiseaseId(DatabaseObjectId):
    pass


class GoMolecularFunctionTermId(DatabaseObjectId):
    pass


class GoBiologicalProcessTermId(DatabaseObjectId):
    pass


class GoCellularComponentTermId(DatabaseObjectId):
    pass


@dataclass(repr=False)
class NamedEntity(YAMLRoot):
    """
    Generic named entity used as a lightweight semantic root for serializable objects.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["NamedEntity"]
    class_class_curie: ClassVar[str] = "reactome:NamedEntity"
    class_name: ClassVar[str] = "named_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.NamedEntity

    id: Union[str, NamedEntityId] = None
    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedEntityId):
            self.id = NamedEntityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatabaseObject(NamedEntity):
    """
    Root class for most Reactome schema objects and the main provenance-bearing superclass.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["DatabaseObject"]
    class_class_curie: ClassVar[str] = "reactome:DatabaseObject"
    class_name: ClassVar[str] = "database_object"
    class_model_uri: ClassVar[URIRef] = REACTOME.DatabaseObject

    id: Union[str, DatabaseObjectId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    definition: Optional[str] = None
    previous_stable_identifier: Optional[str] = None
    modified: Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatabaseObjectId):
            self.id = DatabaseObjectId(self.id)

        if self._is_empty(self.reactome_db_id):
            self.MissingRequiredField("reactome_db_id")
        if not isinstance(self.reactome_db_id, int):
            self.reactome_db_id = int(self.reactome_db_id)

        if self._is_empty(self.reactome_stable_identifier):
            self.MissingRequiredField("reactome_stable_identifier")
        if not isinstance(self.reactome_stable_identifier, str):
            self.reactome_stable_identifier = str(self.reactome_stable_identifier)

        if self._is_empty(self.source_schema_class):
            self.MissingRequiredField("source_schema_class")
        if not isinstance(self.source_schema_class, str):
            self.source_schema_class = str(self.source_schema_class)

        if self._is_empty(self.display_label):
            self.MissingRequiredField("display_label")
        if not isinstance(self.display_label, str):
            self.display_label = str(self.display_label)

        if self._is_empty(self.created):
            self.MissingRequiredField("created")
        if not isinstance(self.created, InstanceEditId):
            self.created = InstanceEditId(self.created)

        if self.definition is not None and not isinstance(self.definition, str):
            self.definition = str(self.definition)

        if self.previous_stable_identifier is not None and not isinstance(self.previous_stable_identifier, str):
            self.previous_stable_identifier = str(self.previous_stable_identifier)

        if not isinstance(self.modified, list):
            self.modified = [self.modified] if self.modified is not None else []
        self.modified = [v if isinstance(v, InstanceEditId) else InstanceEditId(v) for v in self.modified]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class InstanceEdit(DatabaseObject):
    """
    Provenance record describing a curation action such as creation, modification, review, or revision.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["InstanceEdit"]
    class_class_curie: ClassVar[str] = "reactome:InstanceEdit"
    class_name: ClassVar[str] = "instance_edit"
    class_model_uri: ClassVar[URIRef] = REACTOME.InstanceEdit

    id: Union[str, InstanceEditId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    date: Optional[Union[str, XSDDateTime]] = None
    author: Optional[Union[dict[Union[str, PersonId], Union[dict, "Person"]], list[Union[dict, "Person"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, InstanceEditId):
            self.id = InstanceEditId(self.id)

        if self.date is not None and not isinstance(self.date, XSDDateTime):
            self.date = XSDDateTime(self.date)

        self._normalize_inlined_as_list(slot_name="author", slot_type=Person, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Publication(DatabaseObject):
    """
    Publication record used as evidence or supporting documentation for curated biology.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Publication"]
    class_class_curie: ClassVar[str] = "reactome:Publication"
    class_name: ClassVar[str] = "publication"
    class_model_uri: ClassVar[URIRef] = REACTOME.Publication

    id: Union[str, PublicationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

@dataclass(repr=False)
class LiteratureReference(Publication):
    """
    Literature citation record, commonly representing a PubMed-indexed paper supporting a Reactome assertion.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["LiteratureReference"]
    class_class_curie: ClassVar[str] = "reactome:LiteratureReference"
    class_name: ClassVar[str] = "literature_reference"
    class_model_uri: ClassVar[URIRef] = REACTOME.LiteratureReference

    id: Union[str, LiteratureReferenceId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    pubmed_id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LiteratureReferenceId):
            self.id = LiteratureReferenceId(self.id)

        if self.pubmed_id is not None and not isinstance(self.pubmed_id, str):
            self.pubmed_id = str(self.pubmed_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(DatabaseObject):
    """
    Person record used primarily for provenance, authorship, and curation attribution.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Person"]
    class_class_curie: ClassVar[str] = "reactome:Person"
    class_name: ClassVar[str] = "person"
    class_model_uri: ClassVar[URIRef] = REACTOME.Person

    id: Union[str, PersonId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    orcid: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.orcid is not None and not isinstance(self.orcid, URI):
            self.orcid = URI(self.orcid)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Summation(DatabaseObject):
    """
    Narrative summary record containing prose that explains the biological meaning of an entity or event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Summation"]
    class_class_curie: ClassVar[str] = "reactome:Summation"
    class_name: ClassVar[str] = "summation"
    class_model_uri: ClassVar[URIRef] = REACTOME.Summation

    id: Union[str, SummationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    text: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SummationId):
            self.id = SummationId(self.id)

        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Event(DatabaseObject):
    """
    Biological occurrence or process unit in Reactome, covering both pathways and reaction-like events.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Event"]
    class_class_curie: ClassVar[str] = "reactome:Event"
    class_name: ClassVar[str] = "event"
    class_model_uri: ClassVar[URIRef] = REACTOME.Event

    id: Union[str, EventId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], list[Union[str, OrganismTaxonId]]]] = empty_list()
    located_in_compartment: Optional[Union[Union[str, CompartmentId], list[Union[str, CompartmentId]]]] = empty_list()
    has_summation: Optional[Union[str, SummationId]] = None
    has_cross_reference: Optional[Union[Union[str, DatabaseIdentifierId], list[Union[str, DatabaseIdentifierId]]]] = empty_list()
    has_disease_context: Optional[Union[Union[str, DiseaseId], list[Union[str, DiseaseId]]]] = empty_list()
    supported_by: Optional[Union[Union[str, PublicationId], list[Union[str, PublicationId]]]] = empty_list()
    reviewed: Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]] = empty_list()
    revised: Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]] = empty_list()
    release_date: Optional[Union[str, XSDDate]] = None
    release_status: Optional[str] = None
    is_inferred: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        if not isinstance(self.located_in_compartment, list):
            self.located_in_compartment = [self.located_in_compartment] if self.located_in_compartment is not None else []
        self.located_in_compartment = [v if isinstance(v, CompartmentId) else CompartmentId(v) for v in self.located_in_compartment]

        if self.has_summation is not None and not isinstance(self.has_summation, SummationId):
            self.has_summation = SummationId(self.has_summation)

        if not isinstance(self.has_cross_reference, list):
            self.has_cross_reference = [self.has_cross_reference] if self.has_cross_reference is not None else []
        self.has_cross_reference = [v if isinstance(v, DatabaseIdentifierId) else DatabaseIdentifierId(v) for v in self.has_cross_reference]

        if not isinstance(self.has_disease_context, list):
            self.has_disease_context = [self.has_disease_context] if self.has_disease_context is not None else []
        self.has_disease_context = [v if isinstance(v, DiseaseId) else DiseaseId(v) for v in self.has_disease_context]

        if not isinstance(self.supported_by, list):
            self.supported_by = [self.supported_by] if self.supported_by is not None else []
        self.supported_by = [v if isinstance(v, PublicationId) else PublicationId(v) for v in self.supported_by]

        if not isinstance(self.reviewed, list):
            self.reviewed = [self.reviewed] if self.reviewed is not None else []
        self.reviewed = [v if isinstance(v, InstanceEditId) else InstanceEditId(v) for v in self.reviewed]

        if not isinstance(self.revised, list):
            self.revised = [self.revised] if self.revised is not None else []
        self.revised = [v if isinstance(v, InstanceEditId) else InstanceEditId(v) for v in self.revised]

        if self.release_date is not None and not isinstance(self.release_date, XSDDate):
            self.release_date = XSDDate(self.release_date)

        if self.release_status is not None and not isinstance(self.release_status, str):
            self.release_status = str(self.release_status)

        if self.is_inferred is not None and not isinstance(self.is_inferred, Bool):
            self.is_inferred = Bool(self.is_inferred)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Pathway(Event):
    """
    Curated grouping of biologically related events representing a pathway or pathway-like module.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Pathway"]
    class_class_curie: ClassVar[str] = "reactome:Pathway"
    class_name: ClassVar[str] = "pathway"
    class_model_uri: ClassVar[URIRef] = REACTOME.Pathway

    id: Union[str, PathwayId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_event: Union[dict[Union[str, EventId], Union[dict, Event]], list[Union[dict, Event]]] = empty_dict()
    has_go_biological_process: Optional[Union[str, GoBiologicalProcessTermId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathwayId):
            self.id = PathwayId(self.id)

        if self._is_empty(self.has_event):
            self.MissingRequiredField("has_event")
        self._normalize_inlined_as_list(slot_name="has_event", slot_type=Event, key_name="id", keyed=True)

        if self.has_go_biological_process is not None and not isinstance(self.has_go_biological_process, GoBiologicalProcessTermId):
            self.has_go_biological_process = GoBiologicalProcessTermId(self.has_go_biological_process)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReactionLikeEvent(Event):
    """
    Event in which physical entities participate as inputs, outputs, regulators, or catalysts in a transformation-like
    process.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReactionLikeEvent"]
    class_class_curie: ClassVar[str] = "reactome:ReactionLikeEvent"
    class_name: ClassVar[str] = "reaction_like_event"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReactionLikeEvent

    id: Union[str, ReactionLikeEventId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_input: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]]] = empty_dict()
    has_output: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]]] = empty_dict()
    requires_component: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]]] = empty_dict()
    has_catalyst_activity: Optional[Union[dict[Union[str, CatalystActivityId], Union[dict, "CatalystActivity"]], list[Union[dict, "CatalystActivity"]]]] = empty_dict()
    has_regulation: Optional[Union[dict[Union[str, RegulationId], Union[dict, "Regulation"]], list[Union[dict, "Regulation"]]]] = empty_dict()
    preceded_by: Optional[Union[dict[Union[str, EventId], Union[dict, Event]], list[Union[dict, Event]]]] = empty_dict()
    has_interacting_entity_on_other_cell: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]]] = empty_dict()
    has_interaction: Optional[Union[dict[Union[str, InteractionId], Union[dict, "Interaction"]], list[Union[dict, "Interaction"]]]] = empty_dict()
    has_reaction_type: Optional[Union[Union[str, ReactionTypeTermId], list[Union[str, ReactionTypeTermId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="has_input", slot_type=PhysicalEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_output", slot_type=PhysicalEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="requires_component", slot_type=PhysicalEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_catalyst_activity", slot_type=CatalystActivity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_regulation", slot_type=Regulation, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="preceded_by", slot_type=Event, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_interacting_entity_on_other_cell", slot_type=PhysicalEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="has_interaction", slot_type=Interaction, key_name="id", keyed=True)

        if not isinstance(self.has_reaction_type, list):
            self.has_reaction_type = [self.has_reaction_type] if self.has_reaction_type is not None else []
        self.has_reaction_type = [v if isinstance(v, ReactionTypeTermId) else ReactionTypeTermId(v) for v in self.has_reaction_type]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Reaction(ReactionLikeEvent):
    """
    Standard reaction-like event with explicit transformed inputs and outputs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Reaction"]
    class_class_curie: ClassVar[str] = "reactome:Reaction"
    class_name: ClassVar[str] = "reaction"
    class_model_uri: ClassVar[URIRef] = REACTOME.Reaction

    id: Union[str, ReactionId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_input: Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]] = empty_dict()
    has_output: Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReactionId):
            self.id = ReactionId(self.id)

        if self._is_empty(self.has_input):
            self.MissingRequiredField("has_input")
        self._normalize_inlined_as_list(slot_name="has_input", slot_type=PhysicalEntity, key_name="id", keyed=True)

        if self._is_empty(self.has_output):
            self.MissingRequiredField("has_output")
        self._normalize_inlined_as_list(slot_name="has_output", slot_type=PhysicalEntity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BlackBoxEvent(ReactionLikeEvent):
    """
    Reaction-like event included in the pathway model despite incomplete mechanistic detail.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["BlackBoxEvent"]
    class_class_curie: ClassVar[str] = "reactome:BlackBoxEvent"
    class_name: ClassVar[str] = "black_box_event"
    class_model_uri: ClassVar[URIRef] = REACTOME.BlackBoxEvent

    id: Union[str, BlackBoxEventId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BlackBoxEventId):
            self.id = BlackBoxEventId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Polymerization(ReactionLikeEvent):
    """
    Event representing formation of a polymer from repeated or assembling units.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Polymerization"]
    class_class_curie: ClassVar[str] = "reactome:Polymerization"
    class_name: ClassVar[str] = "polymerization"
    class_model_uri: ClassVar[URIRef] = REACTOME.Polymerization

    id: Union[str, PolymerizationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PolymerizationId):
            self.id = PolymerizationId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Depolymerization(ReactionLikeEvent):
    """
    Event representing breakdown of a polymer into constituent or smaller units.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Depolymerization"]
    class_class_curie: ClassVar[str] = "reactome:Depolymerization"
    class_name: ClassVar[str] = "depolymerization"
    class_model_uri: ClassVar[URIRef] = REACTOME.Depolymerization

    id: Union[str, DepolymerizationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DepolymerizationId):
            self.id = DepolymerizationId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhysicalEntity(DatabaseObject):
    """
    Concrete biological participant whose identity reflects both underlying molecular identity and contextual state.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["PhysicalEntity"]
    class_class_curie: ClassVar[str] = "reactome:PhysicalEntity"
    class_name: ClassVar[str] = "physical_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.PhysicalEntity

    id: Union[str, PhysicalEntityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], list[Union[str, OrganismTaxonId]]]] = empty_list()
    located_in_compartment: Optional[Union[Union[str, CompartmentId], list[Union[str, CompartmentId]]]] = empty_list()
    has_cross_reference: Optional[Union[Union[str, DatabaseIdentifierId], list[Union[str, DatabaseIdentifierId]]]] = empty_list()
    has_disease_context: Optional[Union[Union[str, DiseaseId], list[Union[str, DiseaseId]]]] = empty_list()
    has_go_cellular_component: Optional[Union[str, GoCellularComponentTermId]] = None
    systematic_name: Optional[str] = None
    is_in_disease_context: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        if not isinstance(self.located_in_compartment, list):
            self.located_in_compartment = [self.located_in_compartment] if self.located_in_compartment is not None else []
        self.located_in_compartment = [v if isinstance(v, CompartmentId) else CompartmentId(v) for v in self.located_in_compartment]

        if not isinstance(self.has_cross_reference, list):
            self.has_cross_reference = [self.has_cross_reference] if self.has_cross_reference is not None else []
        self.has_cross_reference = [v if isinstance(v, DatabaseIdentifierId) else DatabaseIdentifierId(v) for v in self.has_cross_reference]

        if not isinstance(self.has_disease_context, list):
            self.has_disease_context = [self.has_disease_context] if self.has_disease_context is not None else []
        self.has_disease_context = [v if isinstance(v, DiseaseId) else DiseaseId(v) for v in self.has_disease_context]

        if self.has_go_cellular_component is not None and not isinstance(self.has_go_cellular_component, GoCellularComponentTermId):
            self.has_go_cellular_component = GoCellularComponentTermId(self.has_go_cellular_component)

        if self.systematic_name is not None and not isinstance(self.systematic_name, str):
            self.systematic_name = str(self.systematic_name)

        if self.is_in_disease_context is not None and not isinstance(self.is_in_disease_context, Bool):
            self.is_in_disease_context = Bool(self.is_in_disease_context)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SimpleEntity(PhysicalEntity):
    """
    Simple molecular entity, typically a small molecule or other non-sequence-based chemical participant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["SimpleEntity"]
    class_class_curie: ClassVar[str] = "reactome:SimpleEntity"
    class_name: ClassVar[str] = "simple_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.SimpleEntity

    id: Union[str, SimpleEntityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_entity: Union[str, ReferenceMoleculeId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SimpleEntityId):
            self.id = SimpleEntityId(self.id)

        if self._is_empty(self.has_reference_entity):
            self.MissingRequiredField("has_reference_entity")
        if not isinstance(self.has_reference_entity, ReferenceMoleculeId):
            self.has_reference_entity = ReferenceMoleculeId(self.has_reference_entity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GenomeEncodedEntity(PhysicalEntity):
    """
    Physical entity whose existence is grounded in a genome-encoded product such as a protein or nucleic acid.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["GenomeEncodedEntity"]
    class_class_curie: ClassVar[str] = "reactome:GenomeEncodedEntity"
    class_name: ClassVar[str] = "genome_encoded_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.GenomeEncodedEntity

    id: Union[str, GenomeEncodedEntityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenomeEncodedEntityId):
            self.id = GenomeEncodedEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SequenceEntity(GenomeEncodedEntity):
    """
    Sequence-bearing physical entity linked to a stable reference sequence and optionally decorated with residue
    modifications and subsequence coordinates.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["SequenceEntity"]
    class_class_curie: ClassVar[str] = "reactome:SequenceEntity"
    class_name: ClassVar[str] = "sequence_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.SequenceEntity

    id: Union[str, SequenceEntityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_entity: Union[str, ReferenceSequenceId] = None
    has_modified_residue: Optional[Union[dict[Union[str, AbstractModifiedResidueId], Union[dict, "AbstractModifiedResidue"]], list[Union[dict, "AbstractModifiedResidue"]]]] = empty_dict()
    start_coordinate: Optional[int] = None
    end_coordinate: Optional[int] = None
    sequence_reference_type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SequenceEntityId):
            self.id = SequenceEntityId(self.id)

        if self._is_empty(self.has_reference_entity):
            self.MissingRequiredField("has_reference_entity")
        if not isinstance(self.has_reference_entity, ReferenceSequenceId):
            self.has_reference_entity = ReferenceSequenceId(self.has_reference_entity)

        self._normalize_inlined_as_list(slot_name="has_modified_residue", slot_type=AbstractModifiedResidue, key_name="id", keyed=True)

        if self.start_coordinate is not None and not isinstance(self.start_coordinate, int):
            self.start_coordinate = int(self.start_coordinate)

        if self.end_coordinate is not None and not isinstance(self.end_coordinate, int):
            self.end_coordinate = int(self.end_coordinate)

        if self.sequence_reference_type is not None and not isinstance(self.sequence_reference_type, str):
            self.sequence_reference_type = str(self.sequence_reference_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Complex(PhysicalEntity):
    """
    Physical entity composed of two or more component physical entities assembled into a functional complex.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Complex"]
    class_class_curie: ClassVar[str] = "reactome:Complex"
    class_name: ClassVar[str] = "complex"
    class_model_uri: ClassVar[URIRef] = REACTOME.Complex

    id: Union[str, ComplexId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_component: Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComplexId):
            self.id = ComplexId(self.id)

        if self._is_empty(self.has_component):
            self.MissingRequiredField("has_component")
        self._normalize_inlined_as_list(slot_name="has_component", slot_type=PhysicalEntity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EntitySet(PhysicalEntity):
    """
    Curated set of physical entities that are treated as functionally interchangeable in a given biological context.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["EntitySet"]
    class_class_curie: ClassVar[str] = "reactome:EntitySet"
    class_name: ClassVar[str] = "entity_set"
    class_model_uri: ClassVar[URIRef] = REACTOME.EntitySet

    id: Union[str, EntitySetId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_member: Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntitySetId):
            self.id = EntitySetId(self.id)

        if self._is_empty(self.has_member):
            self.MissingRequiredField("has_member")
        self._normalize_inlined_as_list(slot_name="has_member", slot_type=PhysicalEntity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CandidateSet(EntitySet):
    """
    Entity set whose members are candidates for fulfilling a shared biological role.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["CandidateSet"]
    class_class_curie: ClassVar[str] = "reactome:CandidateSet"
    class_name: ClassVar[str] = "candidate_set"
    class_model_uri: ClassVar[URIRef] = REACTOME.CandidateSet

    id: Union[str, CandidateSetId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_member: Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CandidateSetId):
            self.id = CandidateSetId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DefinedSet(EntitySet):
    """
    Entity set whose members are explicitly curated as the intended interchangeable participants.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["DefinedSet"]
    class_class_curie: ClassVar[str] = "reactome:DefinedSet"
    class_name: ClassVar[str] = "defined_set"
    class_model_uri: ClassVar[URIRef] = REACTOME.DefinedSet

    id: Union[str, DefinedSetId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_member: Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DefinedSetId):
            self.id = DefinedSetId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Polymer(PhysicalEntity):
    """
    Polymer entity abstracted in terms of one or more repeated units.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Polymer"]
    class_class_curie: ClassVar[str] = "reactome:Polymer"
    class_name: ClassVar[str] = "polymer"
    class_model_uri: ClassVar[URIRef] = REACTOME.Polymer

    id: Union[str, PolymerId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_repeated_unit: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PolymerId):
            self.id = PolymerId(self.id)

        self._normalize_inlined_as_list(slot_name="has_repeated_unit", slot_type=PhysicalEntity, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Cell(PhysicalEntity):
    """
    Cell or cell-like biological unit treated as a physical participant in an event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Cell"]
    class_class_curie: ClassVar[str] = "reactome:Cell"
    class_name: ClassVar[str] = "cell"
    class_model_uri: ClassVar[URIRef] = REACTOME.Cell

    id: Union[str, CellId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellId):
            self.id = CellId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OtherEntity(PhysicalEntity):
    """
    Catch-all physical entity class for biologically relevant participants not covered by more specific subclasses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["OtherEntity"]
    class_class_curie: ClassVar[str] = "reactome:OtherEntity"
    class_name: ClassVar[str] = "other_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.OtherEntity

    id: Union[str, OtherEntityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OtherEntityId):
            self.id = OtherEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Drug(PhysicalEntity):
    """
    Therapeutic or intervention-oriented physical entity modeled in the Reactome graph.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Drug"]
    class_class_curie: ClassVar[str] = "reactome:Drug"
    class_name: ClassVar[str] = "drug"
    class_model_uri: ClassVar[URIRef] = REACTOME.Drug

    id: Union[str, DrugId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DrugId):
            self.id = DrugId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ChemicalDrug(Drug):
    """
    Drug represented primarily as a chemical or small-molecule therapeutic agent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ChemicalDrug"]
    class_class_curie: ClassVar[str] = "reactome:ChemicalDrug"
    class_name: ClassVar[str] = "chemical_drug"
    class_model_uri: ClassVar[URIRef] = REACTOME.ChemicalDrug

    id: Union[str, ChemicalDrugId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalDrugId):
            self.id = ChemicalDrugId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProteinDrug(Drug):
    """
    Drug represented as a protein therapeutic or protein-derived biologic.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ProteinDrug"]
    class_class_curie: ClassVar[str] = "reactome:ProteinDrug"
    class_name: ClassVar[str] = "protein_drug"
    class_model_uri: ClassVar[URIRef] = REACTOME.ProteinDrug

    id: Union[str, ProteinDrugId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProteinDrugId):
            self.id = ProteinDrugId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RnaDrug(Drug):
    """
    Drug represented as an RNA-based therapeutic agent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["RnaDrug"]
    class_class_curie: ClassVar[str] = "reactome:RnaDrug"
    class_name: ClassVar[str] = "rna_drug"
    class_model_uri: ClassVar[URIRef] = REACTOME.RnaDrug

    id: Union[str, RnaDrugId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RnaDrugId):
            self.id = RnaDrugId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceEntity(DatabaseObject):
    """
    Invariant reference identity used to connect multiple contextualized physical entities that share an underlying
    molecular identity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceEntity"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceEntity"
    class_name: ClassVar[str] = "reference_entity"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceEntity

    id: Union[str, ReferenceEntityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None
    identifier: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.has_reference_database):
            self.MissingRequiredField("has_reference_database")
        if not isinstance(self.has_reference_database, ReferenceDatabaseId):
            self.has_reference_database = ReferenceDatabaseId(self.has_reference_database)

        if self.identifier is not None and not isinstance(self.identifier, str):
            self.identifier = str(self.identifier)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceSequence(ReferenceEntity):
    """
    Reference identity for a sequence-bearing biomolecule.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceSequence"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceSequence"
    class_name: ClassVar[str] = "reference_sequence"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceSequence

    id: Union[str, ReferenceSequenceId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceSequenceId):
            self.id = ReferenceSequenceId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceGeneProduct(ReferenceSequence):
    """
    Reference sequence corresponding to a gene product, typically protein-centric.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceGeneProduct"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceGeneProduct"
    class_name: ClassVar[str] = "reference_gene_product"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceGeneProduct

    id: Union[str, ReferenceGeneProductId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceGeneProductId):
            self.id = ReferenceGeneProductId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceIsoform(ReferenceSequence):
    """
    Reference sequence representing a specific isoform-level identity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceIsoform"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceIsoform"
    class_name: ClassVar[str] = "reference_isoform"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceIsoform

    id: Union[str, ReferenceIsoformId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceIsoformId):
            self.id = ReferenceIsoformId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceDnaSequence(ReferenceSequence):
    """
    Reference identity for a DNA sequence.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceDnaSequence"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceDnaSequence"
    class_name: ClassVar[str] = "reference_dna_sequence"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceDnaSequence

    id: Union[str, ReferenceDnaSequenceId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceDnaSequenceId):
            self.id = ReferenceDnaSequenceId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceRnaSequence(ReferenceSequence):
    """
    Reference identity for an RNA sequence.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceRnaSequence"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceRnaSequence"
    class_name: ClassVar[str] = "reference_rna_sequence"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceRnaSequence

    id: Union[str, ReferenceRnaSequenceId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceRnaSequenceId):
            self.id = ReferenceRnaSequenceId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceMolecule(ReferenceEntity):
    """
    Reference identity for a small molecule, simple chemical, or chemically grounded participant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceMolecule"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceMolecule"
    class_name: ClassVar[str] = "reference_molecule"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceMolecule

    id: Union[str, ReferenceMoleculeId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceMoleculeId):
            self.id = ReferenceMoleculeId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceGroup(ReferenceEntity):
    """
    Grouped reference identity used when an invariant identity is represented at a grouped rather than single-entry
    level.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceGroup"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceGroup"
    class_name: ClassVar[str] = "reference_group"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceGroup

    id: Union[str, ReferenceGroupId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceGroupId):
            self.id = ReferenceGroupId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceTherapeutic(ReferenceEntity):
    """
    Reference identity for a therapeutic or intervention-oriented entity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceTherapeutic"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceTherapeutic"
    class_name: ClassVar[str] = "reference_therapeutic"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceTherapeutic

    id: Union[str, ReferenceTherapeuticId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_reference_database: Union[str, ReferenceDatabaseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceTherapeuticId):
            self.id = ReferenceTherapeuticId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceDatabase(DatabaseObject):
    """
    Metadata record describing an external database or authority used for identifiers and cross-references.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReferenceDatabase"]
    class_class_curie: ClassVar[str] = "reactome:ReferenceDatabase"
    class_name: ClassVar[str] = "reference_database"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReferenceDatabase

    id: Union[str, ReferenceDatabaseId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    access_url: Optional[Union[str, URI]] = None
    identifier_prefix: Optional[str] = None
    resource_identifier: Optional[str] = None
    url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceDatabaseId):
            self.id = ReferenceDatabaseId(self.id)

        if self.access_url is not None and not isinstance(self.access_url, URI):
            self.access_url = URI(self.access_url)

        if self.identifier_prefix is not None and not isinstance(self.identifier_prefix, str):
            self.identifier_prefix = str(self.identifier_prefix)

        if self.resource_identifier is not None and not isinstance(self.resource_identifier, str):
            self.resource_identifier = str(self.resource_identifier)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatabaseIdentifier(DatabaseObject):
    """
    Cross-reference record that pairs an identifier string with a reference database authority.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["DatabaseIdentifier"]
    class_class_curie: ClassVar[str] = "reactome:DatabaseIdentifier"
    class_name: ClassVar[str] = "database_identifier"
    class_model_uri: ClassVar[URIRef] = REACTOME.DatabaseIdentifier

    id: Union[str, DatabaseIdentifierId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    identifier: Optional[str] = None
    has_reference_database: Optional[Union[str, ReferenceDatabaseId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatabaseIdentifierId):
            self.id = DatabaseIdentifierId(self.id)

        if self.identifier is not None and not isinstance(self.identifier, str):
            self.identifier = str(self.identifier)

        if self.has_reference_database is not None and not isinstance(self.has_reference_database, ReferenceDatabaseId):
            self.has_reference_database = ReferenceDatabaseId(self.has_reference_database)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CatalystActivity(DatabaseObject):
    """
    Reified catalytic assertion connecting a catalyst bearer, a GO molecular function, and one or more catalyzed
    reaction-like events.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["CatalystActivity"]
    class_class_curie: ClassVar[str] = "reactome:CatalystActivity"
    class_name: ClassVar[str] = "catalyst_activity"
    class_model_uri: ClassVar[URIRef] = REACTOME.CatalystActivity

    id: Union[str, CatalystActivityId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_catalyst: Union[str, PhysicalEntityId] = None
    has_go_molecular_function: Union[str, GoMolecularFunctionTermId] = None
    has_active_unit: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]] = empty_dict()
    catalyzes: Optional[Union[dict[Union[str, ReactionLikeEventId], Union[dict, ReactionLikeEvent]], list[Union[dict, ReactionLikeEvent]]]] = empty_dict()
    supported_by: Optional[Union[Union[str, PublicationId], list[Union[str, PublicationId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CatalystActivityId):
            self.id = CatalystActivityId(self.id)

        if self._is_empty(self.has_catalyst):
            self.MissingRequiredField("has_catalyst")
        if not isinstance(self.has_catalyst, PhysicalEntityId):
            self.has_catalyst = PhysicalEntityId(self.has_catalyst)

        if self._is_empty(self.has_go_molecular_function):
            self.MissingRequiredField("has_go_molecular_function")
        if not isinstance(self.has_go_molecular_function, GoMolecularFunctionTermId):
            self.has_go_molecular_function = GoMolecularFunctionTermId(self.has_go_molecular_function)

        self._normalize_inlined_as_list(slot_name="has_active_unit", slot_type=PhysicalEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="catalyzes", slot_type=ReactionLikeEvent, key_name="id", keyed=True)

        if not isinstance(self.supported_by, list):
            self.supported_by = [self.supported_by] if self.supported_by is not None else []
        self.supported_by = [v if isinstance(v, PublicationId) else PublicationId(v) for v in self.supported_by]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Regulation(DatabaseObject):
    """
    Reified regulatory assertion linking a regulator physical entity to a regulated reaction-like event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Regulation"]
    class_class_curie: ClassVar[str] = "reactome:Regulation"
    class_name: ClassVar[str] = "regulation"
    class_model_uri: ClassVar[URIRef] = REACTOME.Regulation

    id: Union[str, RegulationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_regulator: Union[str, PhysicalEntityId] = None
    regulates: Union[str, ReactionLikeEventId] = None
    has_active_unit: Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]] = empty_dict()
    supported_by: Optional[Union[Union[str, PublicationId], list[Union[str, PublicationId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.has_regulator):
            self.MissingRequiredField("has_regulator")
        if not isinstance(self.has_regulator, PhysicalEntityId):
            self.has_regulator = PhysicalEntityId(self.has_regulator)

        if self._is_empty(self.regulates):
            self.MissingRequiredField("regulates")
        if not isinstance(self.regulates, ReactionLikeEventId):
            self.regulates = ReactionLikeEventId(self.regulates)

        self._normalize_inlined_as_list(slot_name="has_active_unit", slot_type=PhysicalEntity, key_name="id", keyed=True)

        if not isinstance(self.supported_by, list):
            self.supported_by = [self.supported_by] if self.supported_by is not None else []
        self.supported_by = [v if isinstance(v, PublicationId) else PublicationId(v) for v in self.supported_by]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PositiveRegulation(Regulation):
    """
    Regulation that increases, enables, or positively influences the occurrence or efficiency of a reaction-like event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["PositiveRegulation"]
    class_class_curie: ClassVar[str] = "reactome:PositiveRegulation"
    class_name: ClassVar[str] = "positive_regulation"
    class_model_uri: ClassVar[URIRef] = REACTOME.PositiveRegulation

    id: Union[str, PositiveRegulationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_regulator: Union[str, PhysicalEntityId] = None
    regulates: Union[str, ReactionLikeEventId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PositiveRegulationId):
            self.id = PositiveRegulationId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NegativeRegulation(Regulation):
    """
    Regulation that decreases, inhibits, or negatively influences the occurrence or efficiency of a reaction-like
    event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["NegativeRegulation"]
    class_class_curie: ClassVar[str] = "reactome:NegativeRegulation"
    class_name: ClassVar[str] = "negative_regulation"
    class_model_uri: ClassVar[URIRef] = REACTOME.NegativeRegulation

    id: Union[str, NegativeRegulationId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_regulator: Union[str, PhysicalEntityId] = None
    regulates: Union[str, ReactionLikeEventId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NegativeRegulationId):
            self.id = NegativeRegulationId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Requirement(Regulation):
    """
    Regulation-like assertion indicating that a regulator or participant is required for a reaction-like event to
    occur.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Requirement"]
    class_class_curie: ClassVar[str] = "reactome:Requirement"
    class_name: ClassVar[str] = "requirement"
    class_model_uri: ClassVar[URIRef] = REACTOME.Requirement

    id: Union[str, RequirementId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    has_regulator: Union[str, PhysicalEntityId] = None
    regulates: Union[str, ReactionLikeEventId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RequirementId):
            self.id = RequirementId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Interaction(DatabaseObject):
    """
    Interaction record associated with an event or set of participants.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Interaction"]
    class_class_curie: ClassVar[str] = "reactome:Interaction"
    class_name: ClassVar[str] = "interaction"
    class_model_uri: ClassVar[URIRef] = REACTOME.Interaction

    id: Union[str, InteractionId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, InteractionId):
            self.id = InteractionId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReactionTypeTerm(DatabaseObject):
    """
    Controlled vocabulary term used to characterize a reaction-like event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReactionTypeTerm"]
    class_class_curie: ClassVar[str] = "reactome:ReactionTypeTerm"
    class_name: ClassVar[str] = "reaction_type_term"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReactionTypeTerm

    id: Union[str, ReactionTypeTermId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReactionTypeTermId):
            self.id = ReactionTypeTermId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AbstractModifiedResidue(DatabaseObject):
    """
    Feature record describing a modified residue or residue-level state on a sequence-bearing entity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["AbstractModifiedResidue"]
    class_class_curie: ClassVar[str] = "reactome:AbstractModifiedResidue"
    class_name: ClassVar[str] = "abstract_modified_residue"
    class_model_uri: ClassVar[URIRef] = REACTOME.AbstractModifiedResidue

    id: Union[str, AbstractModifiedResidueId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AbstractModifiedResidueId):
            self.id = AbstractModifiedResidueId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OrganismTaxon(DatabaseObject):
    """
    Organism taxon record representing the organismal context for entities and events.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["OrganismTaxon"]
    class_class_curie: ClassVar[str] = "reactome:OrganismTaxon"
    class_name: ClassVar[str] = "organism_taxon"
    class_model_uri: ClassVar[URIRef] = REACTOME.OrganismTaxon

    id: Union[str, OrganismTaxonId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    ncbi_taxon_id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganismTaxonId):
            self.id = OrganismTaxonId(self.id)

        if self.ncbi_taxon_id is not None and not isinstance(self.ncbi_taxon_id, str):
            self.ncbi_taxon_id = str(self.ncbi_taxon_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Taxon(DatabaseObject):
    """
    Taxonomic concept used for taxonomic assignment or metadata.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Taxon"]
    class_class_curie: ClassVar[str] = "reactome:Taxon"
    class_name: ClassVar[str] = "taxon"
    class_model_uri: ClassVar[URIRef] = REACTOME.Taxon

    id: Union[str, TaxonId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None
    ncbi_taxon_id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TaxonId):
            self.id = TaxonId(self.id)

        if self.ncbi_taxon_id is not None and not isinstance(self.ncbi_taxon_id, str):
            self.ncbi_taxon_id = str(self.ncbi_taxon_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Compartment(DatabaseObject):
    """
    Cellular or subcellular location object used to state where an event occurs or where a physical entity resides.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Compartment"]
    class_class_curie: ClassVar[str] = "reactome:Compartment"
    class_name: ClassVar[str] = "compartment"
    class_model_uri: ClassVar[URIRef] = REACTOME.Compartment

    id: Union[str, CompartmentId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CompartmentId):
            self.id = CompartmentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Disease(DatabaseObject):
    """
    Disease concept used to contextualize events and entities in pathological settings.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["Disease"]
    class_class_curie: ClassVar[str] = "reactome:Disease"
    class_name: ClassVar[str] = "disease"
    class_model_uri: ClassVar[URIRef] = REACTOME.Disease

    id: Union[str, DiseaseId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseId):
            self.id = DiseaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GoMolecularFunctionTerm(DatabaseObject):
    """
    Wrapper object for a GO molecular function term used in Reactome catalysis modeling.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["GoMolecularFunctionTerm"]
    class_class_curie: ClassVar[str] = "reactome:GoMolecularFunctionTerm"
    class_name: ClassVar[str] = "go_molecular_function_term"
    class_model_uri: ClassVar[URIRef] = REACTOME.GoMolecularFunctionTerm

    id: Union[str, GoMolecularFunctionTermId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GoMolecularFunctionTermId):
            self.id = GoMolecularFunctionTermId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GoBiologicalProcessTerm(DatabaseObject):
    """
    Wrapper object for a GO biological process term used for pathway or event alignment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["GoBiologicalProcessTerm"]
    class_class_curie: ClassVar[str] = "reactome:GoBiologicalProcessTerm"
    class_name: ClassVar[str] = "go_biological_process_term"
    class_model_uri: ClassVar[URIRef] = REACTOME.GoBiologicalProcessTerm

    id: Union[str, GoBiologicalProcessTermId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GoBiologicalProcessTermId):
            self.id = GoBiologicalProcessTermId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GoCellularComponentTerm(DatabaseObject):
    """
    Wrapper object for a GO cellular component term used in entity or location annotation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["GoCellularComponentTerm"]
    class_class_curie: ClassVar[str] = "reactome:GoCellularComponentTerm"
    class_name: ClassVar[str] = "go_cellular_component_term"
    class_model_uri: ClassVar[URIRef] = REACTOME.GoCellularComponentTerm

    id: Union[str, GoCellularComponentTermId] = None
    reactome_db_id: int = None
    reactome_stable_identifier: str = None
    source_schema_class: str = None
    display_label: str = None
    created: Union[str, InstanceEditId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GoCellularComponentTermId):
            self.id = GoCellularComponentTermId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReactomeDataset(YAMLRoot):
    """
    Top-level container for a serialized Reactome dataset excerpt or export package.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = REACTOME["ReactomeDataset"]
    class_class_curie: ClassVar[str] = "reactome:ReactomeDataset"
    class_name: ClassVar[str] = "reactome_dataset"
    class_model_uri: ClassVar[URIRef] = REACTOME.ReactomeDataset

    database_objects: Optional[Union[dict[Union[str, DatabaseObjectId], Union[dict, DatabaseObject]], list[Union[dict, DatabaseObject]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_dict(slot_name="database_objects", slot_type=DatabaseObject, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DCTERMS.identifier, name="id", curie=DCTERMS.curie('identifier'),
                   model_uri=REACTOME.id, domain=None, range=URIRef)

slots.category = Slot(uri=REACTOME.category, name="category", curie=REACTOME.curie('category'),
                   model_uri=REACTOME.category, domain=None, range=Optional[str])

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=REACTOME.name, domain=None, range=Optional[str])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=REACTOME.description, domain=None, range=Optional[str])

slots.reactome_db_id = Slot(uri=REACTOME.reactomeDbId, name="reactome_db_id", curie=REACTOME.curie('reactomeDbId'),
                   model_uri=REACTOME.reactome_db_id, domain=None, range=Optional[int])

slots.reactome_stable_identifier = Slot(uri=REACTOME.reactomeStableIdentifier, name="reactome_stable_identifier", curie=REACTOME.curie('reactomeStableIdentifier'),
                   model_uri=REACTOME.reactome_stable_identifier, domain=None, range=Optional[str])

slots.source_schema_class = Slot(uri=REACTOME.sourceSchemaClass, name="source_schema_class", curie=REACTOME.curie('sourceSchemaClass'),
                   model_uri=REACTOME.source_schema_class, domain=None, range=Optional[str])

slots.display_label = Slot(uri=REACTOME.displayLabel, name="display_label", curie=REACTOME.curie('displayLabel'),
                   model_uri=REACTOME.display_label, domain=None, range=Optional[str])

slots.definition = Slot(uri=REACTOME.definition, name="definition", curie=REACTOME.curie('definition'),
                   model_uri=REACTOME.definition, domain=None, range=Optional[str])

slots.systematic_name = Slot(uri=REACTOME.systematicName, name="systematic_name", curie=REACTOME.curie('systematicName'),
                   model_uri=REACTOME.systematic_name, domain=None, range=Optional[str])

slots.release_date = Slot(uri=REACTOME.releaseDate, name="release_date", curie=REACTOME.curie('releaseDate'),
                   model_uri=REACTOME.release_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.release_status = Slot(uri=REACTOME.releaseStatus, name="release_status", curie=REACTOME.curie('releaseStatus'),
                   model_uri=REACTOME.release_status, domain=None, range=Optional[str])

slots.is_inferred = Slot(uri=REACTOME.isInferred, name="is_inferred", curie=REACTOME.curie('isInferred'),
                   model_uri=REACTOME.is_inferred, domain=None, range=Optional[Union[bool, Bool]])

slots.is_in_disease_context = Slot(uri=REACTOME.isInDiseaseContext, name="is_in_disease_context", curie=REACTOME.curie('isInDiseaseContext'),
                   model_uri=REACTOME.is_in_disease_context, domain=None, range=Optional[Union[bool, Bool]])

slots.created = Slot(uri=REACTOME.created, name="created", curie=REACTOME.curie('created'),
                   model_uri=REACTOME.created, domain=None, range=Optional[Union[str, InstanceEditId]])

slots.modified = Slot(uri=REACTOME.modified, name="modified", curie=REACTOME.curie('modified'),
                   model_uri=REACTOME.modified, domain=None, range=Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]])

slots.reviewed = Slot(uri=REACTOME.reviewed, name="reviewed", curie=REACTOME.curie('reviewed'),
                   model_uri=REACTOME.reviewed, domain=None, range=Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]])

slots.revised = Slot(uri=REACTOME.revised, name="revised", curie=REACTOME.curie('revised'),
                   model_uri=REACTOME.revised, domain=None, range=Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]])

slots.authored = Slot(uri=REACTOME.authored, name="authored", curie=REACTOME.curie('authored'),
                   model_uri=REACTOME.authored, domain=None, range=Optional[Union[Union[str, InstanceEditId], list[Union[str, InstanceEditId]]]])

slots.in_taxon = Slot(uri=REACTOME.inTaxon, name="in_taxon", curie=REACTOME.curie('inTaxon'),
                   model_uri=REACTOME.in_taxon, domain=None, range=Optional[Union[Union[str, OrganismTaxonId], list[Union[str, OrganismTaxonId]]]])

slots.located_in_compartment = Slot(uri=REACTOME.locatedInCompartment, name="located_in_compartment", curie=REACTOME.curie('locatedInCompartment'),
                   model_uri=REACTOME.located_in_compartment, domain=None, range=Optional[Union[Union[str, CompartmentId], list[Union[str, CompartmentId]]]])

slots.has_summation = Slot(uri=REACTOME.hasSummation, name="has_summation", curie=REACTOME.curie('hasSummation'),
                   model_uri=REACTOME.has_summation, domain=None, range=Optional[Union[str, SummationId]])

slots.supported_by = Slot(uri=REACTOME.supportedBy, name="supported_by", curie=REACTOME.curie('supportedBy'),
                   model_uri=REACTOME.supported_by, domain=None, range=Optional[Union[Union[str, PublicationId], list[Union[str, PublicationId]]]])

slots.has_cross_reference = Slot(uri=REACTOME.hasCrossReference, name="has_cross_reference", curie=REACTOME.curie('hasCrossReference'),
                   model_uri=REACTOME.has_cross_reference, domain=None, range=Optional[Union[Union[str, DatabaseIdentifierId], list[Union[str, DatabaseIdentifierId]]]])

slots.has_disease_context = Slot(uri=REACTOME.hasDiseaseContext, name="has_disease_context", curie=REACTOME.curie('hasDiseaseContext'),
                   model_uri=REACTOME.has_disease_context, domain=None, range=Optional[Union[Union[str, DiseaseId], list[Union[str, DiseaseId]]]])

slots.has_go_biological_process = Slot(uri=REACTOME.hasGoBiologicalProcess, name="has_go_biological_process", curie=REACTOME.curie('hasGoBiologicalProcess'),
                   model_uri=REACTOME.has_go_biological_process, domain=None, range=Optional[Union[str, GoBiologicalProcessTermId]])

slots.has_go_cellular_component = Slot(uri=REACTOME.hasGoCellularComponent, name="has_go_cellular_component", curie=REACTOME.curie('hasGoCellularComponent'),
                   model_uri=REACTOME.has_go_cellular_component, domain=None, range=Optional[Union[str, GoCellularComponentTermId]])

slots.has_go_molecular_function = Slot(uri=REACTOME.hasGoMolecularFunction, name="has_go_molecular_function", curie=REACTOME.curie('hasGoMolecularFunction'),
                   model_uri=REACTOME.has_go_molecular_function, domain=None, range=Optional[Union[str, GoMolecularFunctionTermId]])

slots.has_event = Slot(uri=REACTOME.hasEvent, name="has_event", curie=REACTOME.curie('hasEvent'),
                   model_uri=REACTOME.has_event, domain=None, range=Optional[Union[dict[Union[str, EventId], Union[dict, Event]], list[Union[dict, Event]]]])

slots.preceded_by = Slot(uri=REACTOME.precededBy, name="preceded_by", curie=REACTOME.curie('precededBy'),
                   model_uri=REACTOME.preceded_by, domain=None, range=Optional[Union[dict[Union[str, EventId], Union[dict, Event]], list[Union[dict, Event]]]])

slots.has_input = Slot(uri=REACTOME.hasInput, name="has_input", curie=REACTOME.curie('hasInput'),
                   model_uri=REACTOME.has_input, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_output = Slot(uri=REACTOME.hasOutput, name="has_output", curie=REACTOME.curie('hasOutput'),
                   model_uri=REACTOME.has_output, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.requires_component = Slot(uri=REACTOME.requiresComponent, name="requires_component", curie=REACTOME.curie('requiresComponent'),
                   model_uri=REACTOME.requires_component, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_catalyst_activity = Slot(uri=REACTOME.hasCatalystActivity, name="has_catalyst_activity", curie=REACTOME.curie('hasCatalystActivity'),
                   model_uri=REACTOME.has_catalyst_activity, domain=None, range=Optional[Union[dict[Union[str, CatalystActivityId], Union[dict, CatalystActivity]], list[Union[dict, CatalystActivity]]]])

slots.has_regulation = Slot(uri=REACTOME.hasRegulation, name="has_regulation", curie=REACTOME.curie('hasRegulation'),
                   model_uri=REACTOME.has_regulation, domain=None, range=Optional[Union[dict[Union[str, RegulationId], Union[dict, Regulation]], list[Union[dict, Regulation]]]])

slots.has_interacting_entity_on_other_cell = Slot(uri=REACTOME.hasInteractingEntityOnOtherCell, name="has_interacting_entity_on_other_cell", curie=REACTOME.curie('hasInteractingEntityOnOtherCell'),
                   model_uri=REACTOME.has_interacting_entity_on_other_cell, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_interaction = Slot(uri=REACTOME.hasInteraction, name="has_interaction", curie=REACTOME.curie('hasInteraction'),
                   model_uri=REACTOME.has_interaction, domain=None, range=Optional[Union[dict[Union[str, InteractionId], Union[dict, Interaction]], list[Union[dict, Interaction]]]])

slots.has_reaction_type = Slot(uri=REACTOME.hasReactionType, name="has_reaction_type", curie=REACTOME.curie('hasReactionType'),
                   model_uri=REACTOME.has_reaction_type, domain=None, range=Optional[Union[Union[str, ReactionTypeTermId], list[Union[str, ReactionTypeTermId]]]])

slots.has_reference_entity = Slot(uri=REACTOME.hasReferenceEntity, name="has_reference_entity", curie=REACTOME.curie('hasReferenceEntity'),
                   model_uri=REACTOME.has_reference_entity, domain=None, range=Optional[Union[str, ReferenceEntityId]])

slots.has_modified_residue = Slot(uri=REACTOME.hasModifiedResidue, name="has_modified_residue", curie=REACTOME.curie('hasModifiedResidue'),
                   model_uri=REACTOME.has_modified_residue, domain=None, range=Optional[Union[dict[Union[str, AbstractModifiedResidueId], Union[dict, AbstractModifiedResidue]], list[Union[dict, AbstractModifiedResidue]]]])

slots.start_coordinate = Slot(uri=REACTOME.startCoordinate, name="start_coordinate", curie=REACTOME.curie('startCoordinate'),
                   model_uri=REACTOME.start_coordinate, domain=None, range=Optional[int])

slots.end_coordinate = Slot(uri=REACTOME.endCoordinate, name="end_coordinate", curie=REACTOME.curie('endCoordinate'),
                   model_uri=REACTOME.end_coordinate, domain=None, range=Optional[int])

slots.sequence_reference_type = Slot(uri=REACTOME.sequenceReferenceType, name="sequence_reference_type", curie=REACTOME.curie('sequenceReferenceType'),
                   model_uri=REACTOME.sequence_reference_type, domain=None, range=Optional[str])

slots.has_component = Slot(uri=REACTOME.hasComponent, name="has_component", curie=REACTOME.curie('hasComponent'),
                   model_uri=REACTOME.has_component, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_member = Slot(uri=REACTOME.hasMember, name="has_member", curie=REACTOME.curie('hasMember'),
                   model_uri=REACTOME.has_member, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_repeated_unit = Slot(uri=REACTOME.hasRepeatedUnit, name="has_repeated_unit", curie=REACTOME.curie('hasRepeatedUnit'),
                   model_uri=REACTOME.has_repeated_unit, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_regulator = Slot(uri=REACTOME.hasRegulator, name="has_regulator", curie=REACTOME.curie('hasRegulator'),
                   model_uri=REACTOME.has_regulator, domain=None, range=Optional[Union[str, PhysicalEntityId]])

slots.regulates = Slot(uri=REACTOME.regulates, name="regulates", curie=REACTOME.curie('regulates'),
                   model_uri=REACTOME.regulates, domain=None, range=Optional[Union[str, ReactionLikeEventId]])

slots.has_active_unit = Slot(uri=REACTOME.hasActiveUnit, name="has_active_unit", curie=REACTOME.curie('hasActiveUnit'),
                   model_uri=REACTOME.has_active_unit, domain=None, range=Optional[Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]]])

slots.has_catalyst = Slot(uri=REACTOME.hasCatalyst, name="has_catalyst", curie=REACTOME.curie('hasCatalyst'),
                   model_uri=REACTOME.has_catalyst, domain=None, range=Optional[Union[str, PhysicalEntityId]])

slots.catalyzes = Slot(uri=REACTOME.catalyzes, name="catalyzes", curie=REACTOME.curie('catalyzes'),
                   model_uri=REACTOME.catalyzes, domain=None, range=Optional[Union[dict[Union[str, ReactionLikeEventId], Union[dict, ReactionLikeEvent]], list[Union[dict, ReactionLikeEvent]]]])

slots.has_reference_database = Slot(uri=REACTOME.hasReferenceDatabase, name="has_reference_database", curie=REACTOME.curie('hasReferenceDatabase'),
                   model_uri=REACTOME.has_reference_database, domain=None, range=Optional[Union[str, ReferenceDatabaseId]])

slots.identifier = Slot(uri=REACTOME.identifier, name="identifier", curie=REACTOME.curie('identifier'),
                   model_uri=REACTOME.identifier, domain=None, range=Optional[str])

slots.access_url = Slot(uri=REACTOME.accessUrl, name="access_url", curie=REACTOME.curie('accessUrl'),
                   model_uri=REACTOME.access_url, domain=None, range=Optional[Union[str, URI]])

slots.identifier_prefix = Slot(uri=REACTOME.identifierPrefix, name="identifier_prefix", curie=REACTOME.curie('identifierPrefix'),
                   model_uri=REACTOME.identifier_prefix, domain=None, range=Optional[str])

slots.resource_identifier = Slot(uri=REACTOME.resourceIdentifier, name="resource_identifier", curie=REACTOME.curie('resourceIdentifier'),
                   model_uri=REACTOME.resource_identifier, domain=None, range=Optional[str])

slots.url = Slot(uri=REACTOME.url, name="url", curie=REACTOME.curie('url'),
                   model_uri=REACTOME.url, domain=None, range=Optional[Union[str, URI]])

slots.pubmed_id = Slot(uri=REACTOME.pubmedId, name="pubmed_id", curie=REACTOME.curie('pubmedId'),
                   model_uri=REACTOME.pubmed_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[0-9]+$'))

slots.orcid = Slot(uri=REACTOME.orcid, name="orcid", curie=REACTOME.curie('orcid'),
                   model_uri=REACTOME.orcid, domain=None, range=Optional[Union[str, URI]])

slots.ncbi_taxon_id = Slot(uri=REACTOME.ncbiTaxonId, name="ncbi_taxon_id", curie=REACTOME.curie('ncbiTaxonId'),
                   model_uri=REACTOME.ncbi_taxon_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[0-9]+$'))

slots.previous_stable_identifier = Slot(uri=REACTOME.previousStableIdentifier, name="previous_stable_identifier", curie=REACTOME.curie('previousStableIdentifier'),
                   model_uri=REACTOME.previous_stable_identifier, domain=None, range=Optional[str])

slots.instanceEdit__date = Slot(uri=REACTOME.date, name="instanceEdit__date", curie=REACTOME.curie('date'),
                   model_uri=REACTOME.instanceEdit__date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.instanceEdit__author = Slot(uri=REACTOME.author, name="instanceEdit__author", curie=REACTOME.curie('author'),
                   model_uri=REACTOME.instanceEdit__author, domain=None, range=Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]])

slots.summation__text = Slot(uri=REACTOME.text, name="summation__text", curie=REACTOME.curie('text'),
                   model_uri=REACTOME.summation__text, domain=None, range=str)

slots.reactomeDataset__database_objects = Slot(uri=REACTOME.database_objects, name="reactomeDataset__database_objects", curie=REACTOME.curie('database_objects'),
                   model_uri=REACTOME.reactomeDataset__database_objects, domain=None, range=Optional[Union[dict[Union[str, DatabaseObjectId], Union[dict, DatabaseObject]], list[Union[dict, DatabaseObject]]]])

slots.database_object_reactome_db_id = Slot(uri=REACTOME.reactomeDbId, name="database_object_reactome_db_id", curie=REACTOME.curie('reactomeDbId'),
                   model_uri=REACTOME.database_object_reactome_db_id, domain=DatabaseObject, range=int)

slots.database_object_reactome_stable_identifier = Slot(uri=REACTOME.reactomeStableIdentifier, name="database_object_reactome_stable_identifier", curie=REACTOME.curie('reactomeStableIdentifier'),
                   model_uri=REACTOME.database_object_reactome_stable_identifier, domain=DatabaseObject, range=str)

slots.database_object_source_schema_class = Slot(uri=REACTOME.sourceSchemaClass, name="database_object_source_schema_class", curie=REACTOME.curie('sourceSchemaClass'),
                   model_uri=REACTOME.database_object_source_schema_class, domain=DatabaseObject, range=str)

slots.database_object_display_label = Slot(uri=REACTOME.displayLabel, name="database_object_display_label", curie=REACTOME.curie('displayLabel'),
                   model_uri=REACTOME.database_object_display_label, domain=DatabaseObject, range=str)

slots.database_object_created = Slot(uri=REACTOME.created, name="database_object_created", curie=REACTOME.curie('created'),
                   model_uri=REACTOME.database_object_created, domain=DatabaseObject, range=Union[str, InstanceEditId])

slots.pathway_has_event = Slot(uri=REACTOME.hasEvent, name="pathway_has_event", curie=REACTOME.curie('hasEvent'),
                   model_uri=REACTOME.pathway_has_event, domain=Pathway, range=Union[dict[Union[str, EventId], Union[dict, Event]], list[Union[dict, Event]]])

slots.reaction_has_input = Slot(uri=REACTOME.hasInput, name="reaction_has_input", curie=REACTOME.curie('hasInput'),
                   model_uri=REACTOME.reaction_has_input, domain=Reaction, range=Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]])

slots.reaction_has_output = Slot(uri=REACTOME.hasOutput, name="reaction_has_output", curie=REACTOME.curie('hasOutput'),
                   model_uri=REACTOME.reaction_has_output, domain=Reaction, range=Union[dict[Union[str, PhysicalEntityId], Union[dict, "PhysicalEntity"]], list[Union[dict, "PhysicalEntity"]]])

slots.simple_entity_has_reference_entity = Slot(uri=REACTOME.hasReferenceEntity, name="simple_entity_has_reference_entity", curie=REACTOME.curie('hasReferenceEntity'),
                   model_uri=REACTOME.simple_entity_has_reference_entity, domain=SimpleEntity, range=Union[str, ReferenceMoleculeId])

slots.sequence_entity_has_reference_entity = Slot(uri=REACTOME.hasReferenceEntity, name="sequence_entity_has_reference_entity", curie=REACTOME.curie('hasReferenceEntity'),
                   model_uri=REACTOME.sequence_entity_has_reference_entity, domain=SequenceEntity, range=Union[str, ReferenceSequenceId])

slots.complex_has_component = Slot(uri=REACTOME.hasComponent, name="complex_has_component", curie=REACTOME.curie('hasComponent'),
                   model_uri=REACTOME.complex_has_component, domain=Complex, range=Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]])

slots.entity_set_has_member = Slot(uri=REACTOME.hasMember, name="entity_set_has_member", curie=REACTOME.curie('hasMember'),
                   model_uri=REACTOME.entity_set_has_member, domain=EntitySet, range=Union[dict[Union[str, PhysicalEntityId], Union[dict, PhysicalEntity]], list[Union[dict, PhysicalEntity]]])

slots.reference_entity_has_reference_database = Slot(uri=REACTOME.hasReferenceDatabase, name="reference_entity_has_reference_database", curie=REACTOME.curie('hasReferenceDatabase'),
                   model_uri=REACTOME.reference_entity_has_reference_database, domain=ReferenceEntity, range=Union[str, ReferenceDatabaseId])

slots.catalyst_activity_has_catalyst = Slot(uri=REACTOME.hasCatalyst, name="catalyst_activity_has_catalyst", curie=REACTOME.curie('hasCatalyst'),
                   model_uri=REACTOME.catalyst_activity_has_catalyst, domain=CatalystActivity, range=Union[str, PhysicalEntityId])

slots.catalyst_activity_has_go_molecular_function = Slot(uri=REACTOME.hasGoMolecularFunction, name="catalyst_activity_has_go_molecular_function", curie=REACTOME.curie('hasGoMolecularFunction'),
                   model_uri=REACTOME.catalyst_activity_has_go_molecular_function, domain=CatalystActivity, range=Union[str, GoMolecularFunctionTermId])

slots.regulation_has_regulator = Slot(uri=REACTOME.hasRegulator, name="regulation_has_regulator", curie=REACTOME.curie('hasRegulator'),
                   model_uri=REACTOME.regulation_has_regulator, domain=Regulation, range=Union[str, PhysicalEntityId])

slots.regulation_regulates = Slot(uri=REACTOME.regulates, name="regulation_regulates", curie=REACTOME.curie('regulates'),
                   model_uri=REACTOME.regulation_regulates, domain=Regulation, range=Union[str, ReactionLikeEventId])
