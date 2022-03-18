from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Project

NODE_LABEL = "Project"


class ProjectNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Project) -> None:
        self.node = Node(
            NODE_LABEL,
            title=obj_in.title,
        )
        tx.create(self.node)


project_node = ProjectNode()
