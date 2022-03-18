from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Recommendation

NODE_LABEL = "RecommendationLetter"


class RecommendationLetterNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Recommendation) -> None:
        self.node = Node(
            NODE_LABEL,
            name=obj_in.name,
            headline=obj_in.headline,
            comment=obj_in.comment,
            user_link=obj_in.user_link,
            photo=obj_in.photo,
        )
        tx.create(self.node)


recommendation_letter_node = RecommendationLetterNode()
