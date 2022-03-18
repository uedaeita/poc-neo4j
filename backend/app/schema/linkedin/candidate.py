from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declared_attr

from app.db.base_class import Base

if TYPE_CHECKING:
    pass


class Candidate(Base):  # type: ignore
    @declared_attr
    def __tablename__(cls) -> str:
        return "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    recruiter_id = Column(String, nullable=True)
    resume = Column(JSON, nullable=True)
    obs = Column(String, nullable=True)
    current_company_id = Column(Integer, nullable=True)
    invite_date = Column(TIMESTAMP, nullable=True)
    can_recommend = Column(Boolean, nullable=False)
    created = Column(TIMESTAMP, default=datetime.utcnow)
    updated = Column(TIMESTAMP, nullable=False)
