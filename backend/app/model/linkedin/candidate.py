from datetime import datetime
from typing import List, Optional

from fastapi_camelcase import CamelModel


class Course(CamelModel):  # type: ignore
    title: Optional[str]
    name: Optional[str]


class Education(CamelModel):  # type: ignore
    school: Optional[str]
    datespan: Optional[str]
    groups: Optional[str]
    degree: Optional[str]
    course: Optional[str]
    begin_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    logo: Optional[str]


class Experience(CamelModel):  # type: ignore
    description: Optional[str]
    current: Optional[bool]
    company_string_id: Optional[str]
    company_number_id: Optional[str]
    company_id: Optional[str]
    end_date: Optional[str]
    company: Optional[str]
    employee_status: Optional[str]
    title: Optional[str]
    logo: Optional[str]
    datespan: Optional[str]
    location: Optional[str]
    begin_date: Optional[str]
    # industry_value: Optional[str]
    # employee_size_value: Optional[str]
    # integration_company_id: Optional[str]


class Honor(CamelModel):  # type: ignore
    title: Optional[str]
    description: Optional[str]
    issuer: Optional[str]
    date: Optional[str]


class Interest(CamelModel):  # type: ignore
    image: Optional[str]
    name: Optional[str]
    link: Optional[str]


class Language(CamelModel):  # type: ignore
    name: Optional[str]
    proficiency: Optional[str]


class Project(CamelModel):  # type: ignore
    begin_date: Optional[str]
    title: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    datespan: Optional[str]


class Publication(CamelModel):  # type: ignore
    link: Optional[str]
    title: Optional[str]
    description: Optional[str]
    publisher: Optional[str]
    date: Optional[str]


class Recommendation(CamelModel):  # type: ignore
    headline: Optional[str]
    comment: Optional[str]
    name: Optional[str]
    user_link: Optional[str]
    photo: Optional[str]


class Skill(CamelModel):  # type: ignore
    name: Optional[str]


class Volunteer(CamelModel):  # type: ignore
    datespan: Optional[str]
    organization: Optional[str]
    role: Optional[str]
    begin_date: Optional[str]
    description: Optional[str]
    end_date: Optional[str]
    logo: Optional[str]
    cause: Optional[str]


class Resume(CamelModel):  # type: ignore
    recruiter_id: Optional[str]
    location: Optional[str]
    volunteers: Optional[List[Volunteer]]
    summary: Optional[str]
    honors: Optional[List[Honor]]
    photo_file: Optional[str]
    origin: Optional[str]
    skills: Optional[List[Skill]]
    name: Optional[str]
    educations: Optional[List[Education]]
    recommendations: Optional[List[Recommendation]]
    experiences: Optional[List[Experience]]
    normalize_location_en: Optional[str]
    open_talk: Optional[int]
    linkedin_url: Optional[str]
    courses: Optional[List[Course]]
    projects: Optional[List[Project]]
    photo: Optional[str]
    publications: Optional[List[Publication]]
    headline: Optional[str]
    normalize_location_jp: Optional[str]
    languages: Optional[List[Language]]
    interests: Optional[List[Interest]]
    # updated: Optional[str]
    # platform: Optional[str]
    # wantedly_url: Optional[str]
    # twitter_url: Optional[str]
    # facebook_active: bool
    # twitter_active: bool
    # github_active: bool
    # email: Optional[str]
    # facebook_url: Optional[str]
    # github_url: Optional[str]
    # last_sender: Optional[str]
    # facebook_header_text: Optional[str]
    # twitter_header_text: Optional[str]
    # user_id: Optional[str]


class Candidate(CamelModel):  # type: ignore
    id: int
    name: str
    user_id: str
    recruiter_id: Optional[str]
    resume: Optional[Resume]
    obs: Optional[str]
    current_company_id: Optional[int]
    invite_date: Optional[datetime]
    can_recommend: bool
    created: datetime
    updated: datetime
