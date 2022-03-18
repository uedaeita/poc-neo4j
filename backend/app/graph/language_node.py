from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Language

NODE_LABEL = "Language"


class LanguageNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Language) -> None:
        self.node = Node(
            NODE_LABEL,
            name=obj_in.name,
        )
        tx.create(self.node)


language_node = LanguageNode()
