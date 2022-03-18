from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Publication

NODE_LABEL = "Publication"


class PublicationNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Publication) -> None:
        self.node = Node(
            NODE_LABEL,
            title=obj_in.title,
            link=obj_in.link,
            description=obj_in.description,
            publisher=obj_in.publisher,
        )
        tx.create(self.node)


publication_node = PublicationNode()
