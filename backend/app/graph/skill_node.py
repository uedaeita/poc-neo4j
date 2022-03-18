from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Skill

NODE_LABEL = "Skill"


class SkillNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Skill) -> None:
        self.node = Node(
            NODE_LABEL,
            name=obj_in.name,
        )
        tx.create(self.node)


skill_node = SkillNode()
