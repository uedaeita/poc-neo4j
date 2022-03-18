from typing import Optional

from py2neo import Node, Transaction

from app.graph.relationship import (
    AwardedFor,
    BelongsTo,
    IsInterestedIn,
    ParticipatesIn,
    Possesses,
    Published,
    Received,
    Speaks,
    Takes,
    WorksAs,
    WorksFor,
)
from app.model.linkedin.candidate import (
    Candidate,
    Education,
    Experience,
    Honor,
    Language,
    Project,
    Publication,
    Volunteer,
)

NODE_LABEL = "Candidate"


class CandidateNode:
    def __init__(self, node: Optional[Node] = None):
        self.node = node

    def create_node(self, tx: Transaction, obj_in: Candidate) -> None:
        self.node = Node(
            NODE_LABEL,
            id=obj_in.user_id,
            name=obj_in.name,
            recruiter_id=obj_in.recruiter_id,
            obs=obj_in.obs,
            invite_date=obj_in.invite_date,
        )
        tx.create(self.node)

    def connect_company(
        self, tx: Transaction, to_node: Node, obj_in: Experience
    ) -> None:
        r = WorksFor(
            self.node,
            to_node,
            current=obj_in.current,
            begin_date=obj_in.begin_date,
            end_date=obj_in.end_date,
            employee_status=obj_in.employee_status,
            title=obj_in.title,
            location=obj_in.location,
            description=obj_in.description,
        )
        tx.create(r)

    def connect_course(self, tx: Transaction, to_node: Node) -> None:
        r = Takes(
            self.node,
            to_node,
        )
        tx.create(r)

    def connect_language(
        self, tx: Transaction, to_node: Node, obj_in: Language
    ) -> None:
        r = Speaks(
            self.node,
            to_node,
            proficiency=obj_in.proficiency,
        )
        tx.create(r)

    def connect_honor(self, tx: Transaction, to_node: Node, obj_in: Honor) -> None:
        r = AwardedFor(self.node, to_node, date=obj_in.date)
        tx.create(r)

    def connect_interest(self, tx: Transaction, to_node: Node) -> None:
        r = IsInterestedIn(
            self.node,
            to_node,
        )
        tx.create(r)

    def connect_job(self, tx: Transaction, to_node: Node, obj_in: Experience) -> None:
        r = WorksAs(
            self.node,
            to_node,
            company=obj_in.company,
            begin_date=obj_in.begin_date,
            end_date=obj_in.end_date,
        )
        tx.create(r)

    def connect_project(self, tx: Transaction, to_node: Node, obj_in: Project) -> None:
        r = ParticipatesIn(
            self.node,
            to_node,
        )
        tx.create(r)

    def connect_publication(
        self, tx: Transaction, to_node: Node, obj_in: Publication
    ) -> None:
        r = Published(
            self.node,
            to_node,
            date=obj_in.date,
        )
        tx.create(r)

    def connect_recommendation_letter(self, tx: Transaction, to_node: Node) -> None:
        r = Received(
            self.node,
            to_node,
        )
        tx.create(r)

    def connect_school(self, tx: Transaction, to_node: Node, obj_in: Education) -> None:
        r = BelongsTo(
            self.node,
            to_node,
            begin_date=obj_in.begin_date,
            end_date=obj_in.end_date,
            degree=obj_in.degree,
            course=obj_in.course,
            description=obj_in.description,
        )
        tx.create(r)

    def connect_skill(self, tx: Transaction, to_node: Node) -> None:
        r = Possesses(
            self.node,
            to_node,
        )
        tx.create(r)

    def connect_volunteer_organization(
        self, tx: Transaction, to_node: Node, obj_in: Volunteer
    ) -> None:
        r = ParticipatesIn(
            self.node,
            to_node,
            begin_date=obj_in.begin_date,
            end_date=obj_in.end_date,
            role=obj_in.role,
            description=obj_in.description,
            cause=obj_in.cause,
        )
        tx.create(r)


candidate_node = CandidateNode()
