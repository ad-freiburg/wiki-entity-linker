from enum import Enum


class Linkers(Enum):
    BASELINE = "baseline"
    SPACY = "spacy"
    TAGME = "tagme"
    TRAINED_MODEL = "trained_model"
    BERT_MODEL = "bert-model"
    POPULAR_ENTITIES = "popular-entities"
    POS_PRIOR = "pos-prior"
    DBPEDIA_SPOTLIGHT = "dbpedia-spotlight"
    NONE = "none"


class LinkLinkers(Enum):
    LINK_LINKER = "link-linker"
    LINK_TEXT_LINKER = "link-text-linker"


class CoreferenceLinkers(Enum):
    NEURALCOREF = "neuralcoref"
    ENTITY = "entity"
    STANFORD = "stanford"
    XRENNER = "xrenner"
    WEXEA = "wexea"


class PredictionFormats(Enum):
    NIF = "nif"
    SIMPLE_JSONL = "simple-jsonl"
    AMBIVERSE = "ambiverse"
    WIKIFIER = "wikifier"
    WEXEA = "wexea"
    EPGEL = "epgel"
