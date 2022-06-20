from enum import Enum


class Linkers(Enum):
    BASELINE = "baseline"
    SPACY = "spacy"
    EXPLOSION = "explosion"
    TAGME = "tagme"
    TRAINED_MODEL = "trained_model"
    BERT_MODEL = "bert_model"
    POPULAR_ENTITIES = "popular_entities"
    POS_PRIOR = "pos_prior"
    DBPEDIA_SPOTLIGHT = "dbpedia_spotlight"
    NONE = "none"


class LinkLinkers(Enum):
    LINK_LINKER = "link-linker"
    LINK_TEXT_LINKER = "link-text-linker"


class CoreferenceLinkers(Enum):
    NEURALCOREF = "neuralcoref"
    ENTITY = "entity"
    STANFORD = "stanford"
    XRENNER = "xrenner"
    HOBBS = "hobbs"
    WEXEA = "wexea"


class PredictionFormats(Enum):
    NIF = "nif"
    SIMPLE_JSONL = "simple_jsonl"
    AMBIVERSE = "ambiverse"
    WIKIFIER = "wikifier"
    WEXEA = "wexea"
