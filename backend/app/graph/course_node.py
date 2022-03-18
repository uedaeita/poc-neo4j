from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Course

NODE_LABEL = "Course"


class CourseNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Course) -> None:
        self.node = Node(
            NODE_LABEL,
            title=obj_in.title,
        )
        tx.create(self.node)


course_node = CourseNode()
