from typing import List

from pydantic import BaseModel


class CsvStruct(BaseModel):  # type: ignore
    filename: str
    headers: List[str]
    rows: List[str]


class CandidateImportCsv(CsvStruct):
    company_relationship: CsvStruct
    course_relationship: CsvStruct
    honor_relationship: CsvStruct
    job_relationship: CsvStruct
    language_relationship: CsvStruct
    project_relationship: CsvStruct
    publication_relationship: CsvStruct
    rec_letter_relationship: CsvStruct
    school_relationship: CsvStruct
    skill_relationship: CsvStruct
    volunteer_org_relationship: CsvStruct
