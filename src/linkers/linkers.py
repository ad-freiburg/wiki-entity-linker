from enum import Enum


class Linkers(Enum):
    REFINED = "refined"
    REL = "rel"
    TAGME = "tagme"
    WAT = "wat"
    DBPEDIA_SPOTLIGHT = "dbpedia-spotlight"
    BASELINE = "baseline"
    SPACY = "spacy"
    TRAINED_MODEL = "trained_model"
    POPULAR_ENTITIES = "popular-entities"
    POS_PRIOR = "pos-prior"
    NONE = "none"


class HyperlinkLinkers(Enum):
    HYPERLINKS_ONLY = "hyperlinks-only"
    HYPERLINK_REFERENCE = "hyperlink-reference"


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
