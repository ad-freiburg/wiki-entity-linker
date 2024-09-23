from typing import Dict, Set

import pickle
import logging

import elevant.helpers.entity_database_reader
from elevant import settings


logger = logging.getLogger("main." + __name__.split(".")[-1])


class EntityDatabaseReader(elevant.helpers.entity_database_reader.EntityDatabaseReader):
    @staticmethod
    def get_title_synonyms() -> Dict[str, Set[str]]:
        filename = settings.TITLE_SYNONYMS_FILE
        logger.info("Loading title synonyms from %s ..." % filename)
        with open(filename, "rb") as f:
            title_synonyms = pickle.load(f)
        logger.info("-> %d title synonyms loaded." % len(title_synonyms))
        return title_synonyms

    @staticmethod
    def get_akronyms() -> Dict[str, Set[str]]:
        filename = settings.AKRONYMS_FILE
        logger.info("Loading akronyms from %s ..." % filename)
        with open(filename, "rb") as f:
            akronyms = pickle.load(f)
        logger.info("-> %d akronyms loaded." % len(akronyms))
        return akronyms
