from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Experience

NODE_LABEL = "Company"


class CompanyNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Experience) -> None:
        self.node = Node(
            NODE_LABEL,
            name=obj_in.company,
        )
        tx.create(self.node)


company_node = CompanyNode()
