from enum import Enum


class Linkers(Enum):
    REFINED = "refined"
    REL = "rel"
    GPT = "gpt"
    TAGME = "tagme"
    WAT = "wat"
    DBPEDIA_SPOTLIGHT = "dbpedia-spotlight"
    BABELFY = "babelfy"
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
    # NEURALCOREF = "neuralcoref"  # Neuralcoref is outdated, see ELEVANT Github issue #5
    FASTCOREF = "fastcoref"
    ENTITY = "entity"
    STANFORD = "stanford"
    WEXEA = "wexea"
    # XRENNER = "xrenner"  # Xrenner has a dependency conflict with REL (flair)


class APILinkers(Enum):
    NIF_API = "nif-api"


class PredictionFormats(Enum):
    NIF = "nif"
    SIMPLE_JSONL = "simple-jsonl"
    AMBIVERSE = "ambiverse"
    WIKIFIER = "wikifier"
    WEXEA = "wexea"
    EPGEL = "epgel"
