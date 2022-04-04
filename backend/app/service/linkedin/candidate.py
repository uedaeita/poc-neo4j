import logging
import math
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.model.linkedin.candidate import Candidate as CandidateModel
from app.model.linkedin.candidate import (
    Course,
    Education,
    Experience,
    Honor,
    Interest,
    Language,
    Project,
    Publication,
    Recommendation,
    Resume,
    Skill,
    Volunteer,
)
from app.schema.linkedin.candidate import Candidate as CandidateSchema

logger = logging.getLogger(__name__)

PER_PAGE = 100000


class Candidate:
    def get_all(self, db: Session) -> List[CandidateModel]:
        total_count = self.get_count(db=db)
        total_pages = math.ceil(total_count / PER_PAGE)

        ress: List[CandidateSchema] = []
        for i in range(0, total_pages):
            ress.extend(
                db.query(CandidateSchema)
                .filter(CandidateSchema.id > PER_PAGE * i)
                .limit(PER_PAGE)
            )

        candidates: List[CandidateModel] = []
        for res in ress:
            resume: Optional[Resume] = None
            if res.resume:
                courses = [
                    Course(title=i) if isinstance(i, str) else Course(**i)
                    for i in res.resume.get("courses", [])
                ]
                educations = [Education(**i) for i in res.resume.get("educations", [])]
                experiences = [
                    Experience(**i) for i in res.resume.get("experiences", [])
                ]
                honors = [Honor(**i) for i in res.resume.get("honors", [])]
                interests = [Interest(**i) for i in res.resume.get("interests", [])]
                languages = [
                    Language(name=i) if isinstance(i, str) else Language(**i)
                    for i in res.resume.get("languages", [])
                ]
                projects = [Project(**i) for i in res.resume.get("projects", [])]
                publications = [
                    Publication(**i) for i in res.resume.get("publications", [])
                ]
                recommendations = [
                    Recommendation(**i) for i in res.resume.get("recommendations", [])
                ]
                skills = [Skill(**i) for i in res.resume.get("skills", [])]
                volunteers = [Volunteer(**i) for i in res.resume.get("volunteers", [])]

                resume = Resume(
                    recruiter_id=res.resume.get("recruiter_id"),
                    location=res.resume.get("location"),
                    volunteers=volunteers,
                    summary=res.resume.get("summary"),
                    honors=honors,
                    photo_file=res.resume.get("photo_file"),
                    origin=res.resume.get("origin"),
                    skills=skills,
                    name=res.resume.get("name"),
                    educations=educations,
                    recommendations=recommendations,
                    experiences=experiences,
                    normalize_location_en=res.resume.get("normalize_location_en"),
                    open_talk=res.resume.get("open_talk"),
                    linkedin_url=res.resume.get("linkedin_url"),
                    courses=courses,
                    projects=projects,
                    photo=res.resume.get("photo"),
                    publications=publications,
                    headline=res.resume.get("headline"),
                    normalize_location_jp=res.resume.get("normalize_location_jp"),
                    languages=languages,
                    interests=interests,
                )
            candidate = CandidateModel(
                id=res.id,
                name=res.name,
                user_id=res.user_id,
                recruiter_id=res.recruiter_id,
                resume=resume,
                obs=res.obs,
                current_company_id=res.current_company_id,
                invite_date=res.invite_date,
                can_recommend=res.can_recommend,
                created=res.created,
                updated=res.updated,
            )
            candidates.append(candidate)

        return candidates

    def get_count(self, db: Session) -> int:
        return db.query(func.count(CandidateSchema.id)).scalar()


candidate = Candidate()
