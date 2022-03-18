from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.model.linkedin.candidate import Candidate
from app.service.linkedin.candidate import candidate

router = APIRouter()


@router.get("/candidates", response_model=List[Candidate])
def get_linkedin_candidates(*, db: Session = Depends(deps.get_db)) -> Any:  # noqa: B008
    (
        candidates,
        _courses,
        _educations,
        _experiences,
        _honors,
        _interests,
        _languages,
        _projects,
        _publications,
        _recommendations,
        _skills,
        _volunteers,
    ) = candidate.get_all(db=db)
    return candidates[:10]  # Only return first 10
