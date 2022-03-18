import logging
from typing import Any

from fastapi import APIRouter, Depends
from py2neo import Graph
from sqlalchemy.orm import Session

from app.api import deps
from app.service import graph, linkedin
from app.util.timer import elapsed_timer

router = APIRouter()


logger = logging.getLogger(__name__)


@router.post("/graph/provision", response_model=None)
def provision_graph(
    *,
    db: Session = Depends(deps.get_db),  # noqa: B008
    g: Graph = Depends(deps.get_graph),  # noqa: B008
) -> Any:
    with elapsed_timer() as elapsed:
        # Delete everything in the current graph database.
        g.run("MATCH (n) CALL { WITH n DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS")
        logger.info(f"clean graph took: {elapsed()} sec")

        # Provision everything for the graph database.
        (
            candidates,
            courses,
            educations,
            experiences,
            honors,
            interests,
            languages,
            projects,
            publications,
            recommendations,
            skills,
            volunteers,
        ) = linkedin.candidate.candidate.get_all(db=db)
        logger.info(f"get all candidates from mysql took: {elapsed()} sec")

        graph.candidate.import_all(g=g, models=candidates)
        logger.info(f"import all nodes and relationships took: {elapsed()} sec")
