from typing import Optional

from py2neo import Node, Transaction

from app.model.linkedin.candidate import Volunteer

NODE_LABEL = "VolunteerOrganization"


class VolunteerOrganizationNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Volunteer) -> None:
        self.node = Node(
            NODE_LABEL,
            name=obj_in.organization,
        )
        tx.create(self.node)


volunteer_organization_node = VolunteerOrganizationNode()
