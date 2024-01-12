from typing import Optional
from spacy.tokens import Doc

from src.models.entity_database import EntityDatabase
from src.models.entity_mention import EntityMention
from src.models.article import Article


class HyperlinksOnlyLinker:
    LINKER_IDENTIFIER = "Hyperlinks Only"

    def __init__(self, entity_db: EntityDatabase):
        self.entity_db = entity_db
        self.model = None

    def link_entities(self, article: Article, doc: Optional[Doc] = None):
        entity_mentions = []
        for span, target in article.hyperlinks:
            entity_id = self.entity_db.link2id(target)
            if entity_id:
                entity_mention = EntityMention(span=span,
                                               recognized_by=self.LINKER_IDENTIFIER,
                                               entity_id=entity_id,
                                               linked_by=self.LINKER_IDENTIFIER,
                                               candidates={entity_id})
                entity_mentions.append(entity_mention)
        article.add_entity_mentions(entity_mentions)
