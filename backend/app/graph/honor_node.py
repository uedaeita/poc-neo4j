from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Honor

NODE_LABEL = "Honor"


class HonorNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Honor) -> None:
        self.node = Node(
            NODE_LABEL,
            issuer=obj_in.issuer,
            title=obj_in.title,
        )
        tx.create(self.node)


honor_node = HonorNode()
