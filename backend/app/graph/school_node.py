from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Education

NODE_LABEL = "School"


class SchoolNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Education) -> None:
        self.node = Node(
            NODE_LABEL,
            name=obj_in.school,
        )
        tx.create(self.node)


school_node = SchoolNode()
