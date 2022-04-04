import logging
from typing import Any

from fastapi import APIRouter, Depends
from py2neo import Graph
from sqlalchemy.orm import Session

from app.api import deps
from app.service.provision import graph
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
        graph.provision(db=db, g=g)
        logger.info(f"provision took {elapsed()} sec")
