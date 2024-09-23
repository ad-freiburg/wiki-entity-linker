from enum import Enum
from typing import Dict, Set,Optional, Any

import logging

import elevant.models.entity_database

from wiki_entity_linker.helpers.entity_database_reader import EntityDatabaseReader

logger = logging.getLogger("main." + __name__.split(".")[-1])


class MappingName(Enum):
    WIKIDATA_ALIASES = "wikidata_aliases"
    FAMILY_NAME_ALIASES = "family_name_aliases"
    LINK_ALIASES = "link_aliases"
    TITLE_SYNONYMS = "title_synonyms"
    AKRONYMS = "akronyms"
    SITELINKS = "sitelinks"
    ENTITIES = "entities"
    WIKIPEDIA_WIKIDATA = "wikipedia_wikidata"
    REDIRECTS = "redirects"
    LINK_FREQUENCIES = "link_frequencies"
    NAMES = "names"
    GENDER = "gender"
    COREFERENCE_TYPES = "coreference_types"
    LANGUAGES = "languages"
    DEMONYMS = "demonyms"
    WIKIPEDIA_ID_WIKIPEDIA_TITLE = "wikipedia_id_wikipedia_title"
    NAME_TO_ENTITY_ID = "name_to_entity_id"
    ENTITY_ID_TO_ALIAS = "entity_id_to_alias"
    ENTITY_ID_TO_FAMILY_NAME = "entity_id_to_family_name"
    ENTITY_ID_TO_LINK_ALIAS = "entity_id_to_link_alias"
    HYPERLINK_TO_MOST_POPULAR_CANDIDATES = "hyperlink_alias_to_most_popular_candidates"


class LoadingType(Enum):
    FULL = "full"
    RELEVANT_ENTITIES = "relevant_entities"
    RESTRICTED = "restricted"


class LoadedInfo:
    def __init__(self, loading_type: LoadingType, info: Optional[Any] = None):
        self.loading_type = loading_type
        self.info = info


class EntityDatabase(elevant.models.entity_database.EntityDatabase):
    def __init__(self):
        super().__init__()
        self.given_names = {}
        self.given_names: Dict[str, str]
        self.title_synonyms = {}
        self.title_synonyms: Dict[str, Set[str]]
        self.akronyms = {}
        self.akronyms: Dict[str, Set[str]]

    def load_title_synonyms(self):
        title_synonym_to_entities = EntityDatabaseReader.get_title_synonyms()
        for synonym, entity_set in title_synonym_to_entities.items():
            for entity_title in entity_set:
                entity_id = self.link2id(entity_title)
                if entity_id is not None:
                    if entity_id not in self.title_synonyms:
                        self.title_synonyms[entity_id] = set()
                    self.title_synonyms[entity_id].add(synonym)

    def is_title_synonyms_loaded(self) -> bool:
        return len(self.title_synonyms) > 0

    def load_akronyms(self):
        akronym_to_entities = EntityDatabaseReader.get_akronyms()
        for akronym, entity_set in akronym_to_entities.items():
            for entity_title in entity_set:
                entity_id = self.link2id(entity_title)
                if entity_id is not None:
                    if entity_id not in self.akronyms:
                        self.akronyms[entity_id] = set()
                    self.akronyms[entity_id].add(akronym)

    def is_akronyms_loaded(self) -> bool:
        return len(self.akronyms) > 0

    def get_entity_aliases(self, entity_id: str) -> Optional[Set[str]]:
        aliases = set()
        if entity_id in self.entity_name_db:
            # self.entity_name_db values are strings, not dicts as for the other entity to alias mappings.
            aliases.add(self.entity_name_db[entity_id])
        if entity_id in self.entity_to_aliases_db:
            aliases = aliases.union(self.entity_to_aliases_db[entity_id])
        if entity_id in self.entity_to_family_name:
            aliases.add(self.entity_to_family_name[entity_id])
        if entity_id in self.entity_to_link_alias:
            aliases = aliases.union(self.entity_to_link_alias[entity_id])
        if entity_id in self.title_synonyms:
            aliases = aliases.union(self.title_synonyms[entity_id])
        if entity_id in self.akronyms:
            aliases = aliases.union(self.akronyms[entity_id])
        return aliases

    def load_names(self):
        logger.info("Loading family and given names into entity database ...")
        for entity_id, name in EntityDatabaseReader.read_human_names():
            if " " in name:
                given_name = name.split()[0]
                if len(given_name) > 1:
                    self.given_names[entity_id] = given_name
        logger.info("-> Family and given names loaded.")

    def is_names_loaded(self) -> bool:
        return len(self.given_names) > 0

    def has_given_name(self, entity_id: str) -> bool:
        if len(self.given_names) == 0:
            logger.warning("Tried to access first names mapping but first name mapping was not loaded.")
        if entity_id in self.given_names:
            return True
        return False

    def get_given_name(self, entity_id: str) -> str:
        return self.given_names[entity_id]
