import logging

from py2neo import Graph

from app.graph import relationship
from app.graph.candidate_node import NODE_LABEL
from app.graph.company_node import NODE_LABEL as COMPANY_NODE_LABEL
from app.graph.course_node import NODE_LABEL as COURSE_NODE_LABEL
from app.graph.honor_node import NODE_LABEL as HONOR_NODE_LABEL
from app.graph.job_node import NODE_LABEL as JOB_NODE_LABEL
from app.graph.language_node import NODE_LABEL as LANGUAGE_NODE_LABEL
from app.graph.project_node import NODE_LABEL as PROJECT_NODE_LABEL
from app.graph.publication_node import NODE_LABEL as PUBLICATION_NODE_LABEL
from app.graph.recommendation_letter_node import (
    NODE_LABEL as RECOMMENDATION_LETTER_NODE_LABEL,
)
from app.graph.school_node import NODE_LABEL as SCHOOL_NODE_LABEL
from app.graph.skill_node import NODE_LABEL as SKILL_NODE_LABEL
from app.graph.volunteer_organization_node import (
    NODE_LABEL as VOLUNTEER_ORGANIZATION_NODE_LABEL,
)
from app.model.csv import CandidateImportCsv, CsvStruct
from app.model.linkedin.candidate import Candidate as CandidateModel
from app.model.linkedin.candidate import (
    Course,
    Education,
    Experience,
    Honor,
    Language,
    Project,
    Publication,
    Recommendation,
    Skill,
    Volunteer,
)
from app.service import graph
from app.util.string import clean_str
from app.util.timer import elapsed_timer

logger = logging.getLogger(__name__)


CSV_FILE_NAME = "candidate.csv"
CSV_NAME_CAND_COMPANY_REL = "candidate_company_relationship.csv"
CSV_NAME_CAND_COURSE_REL = "candidate_course_relationship.csv"
CSV_NAME_CAND_HONOR_REL = "candidate_honor_relationship.csv"
CSV_NAME_CAND_JOB_REL = "candidate_job_relationship.csv"
CSV_NAME_CAND_LANGUAGE_REL = "candidate_language_relationship.csv"
CSV_NAME_CAND_PROJECT_REL = "candidate_project_relationship.csv"
CSV_NAME_CAND_PUBLICATION_REL = "candidate_publication_relationship.csv"
CSV_NAME_CAND_REC_LETTER_REL = "candidate_recommendation_letter_relationship.csv"
CSV_NAME_CAND_SCHOOL_REL = "candidate_school_relationship.csv"
CSV_NAME_CAND_SKILL_REL = "candidate_skill_relationship.csv"
CSV_NAME_CAND_VOLUNTEER_ORG_REL = "candidate_volunteer_organization_relationship.csv"


class Candidate:
    def __init__(self):
        self.csv = CandidateImportCsv(
            filename=CSV_FILE_NAME,
            headers=[
                "UserId",
                "Name",
                "RecruiterId",
                "Obs",
                "InviteDate",
                "CompanyCurrent",
                "CompanyBeginDate",
                "CompanyEndDate",
                "CompanyEmployeeStatus",
                "CompanyTitle",
                "CompanyLocation",
                "CompanyDescription",
            ],
            rows=[],
            company_relationship=CsvStruct(
                filename=CSV_NAME_CAND_COMPANY_REL,
                headers=[
                    "CandidateName",
                    "CompanyName",
                    "Current",
                    "BeginDate",
                    "EndDate",
                    "EmployeeStatus",
                    "Title",
                    "Location",
                    "Description",
                ],
                rows=[],
            ),
            course_relationship=CsvStruct(
                filename=CSV_NAME_CAND_COURSE_REL,
                headers=["CandidateName", "CourseTitle"],
                rows=[],
            ),
            honor_relationship=CsvStruct(
                filename=CSV_NAME_CAND_HONOR_REL,
                headers=["CandidateName", "HonorTitle", "Date"],
                rows=[],
            ),
            job_relationship=CsvStruct(
                filename=CSV_NAME_CAND_JOB_REL,
                headers=[
                    "CandidateName",
                    "JobTitle",
                    "CompanyName",
                    "BeginDate",
                    "EndDate",
                ],
                rows=[],
            ),
            language_relationship=CsvStruct(
                filename=CSV_NAME_CAND_LANGUAGE_REL,
                headers=["CandidateName", "LanguageName", "Proficiency"],
                rows=[],
            ),
            project_relationship=CsvStruct(
                filename=CSV_NAME_CAND_PROJECT_REL,
                headers=[
                    "CandidateName",
                    "ProjectTitle",
                    "BeginDate",
                    "EndDate",
                    "Description",
                ],
                rows=[],
            ),
            publication_relationship=CsvStruct(
                filename=CSV_NAME_CAND_PUBLICATION_REL,
                headers=["CandidateName", "PublicationTitle", "Date"],
                rows=[],
            ),
            recommendation_letter_relationship=CsvStruct(
                filename=CSV_NAME_CAND_REC_LETTER_REL,
                headers=["CandidateName", "RecommendationLetterName"],
                rows=[],
            ),
            school_relationship=CsvStruct(
                filename=CSV_NAME_CAND_SCHOOL_REL,
                headers=[
                    "CandidateName",
                    "SchoolName",
                    "BeginDate",
                    "EndDate",
                    "Degree",
                    "Course",
                    "Description",
                ],
                rows=[],
            ),
            skill_relationship=CsvStruct(
                filename=CSV_NAME_CAND_SKILL_REL,
                headers=["CandidateName", "SkillName"],
                rows=[],
            ),
            volunteer_organization_relationship=CsvStruct(
                filename=CSV_NAME_CAND_VOLUNTEER_ORG_REL,
                headers=[
                    "CandidateName",
                    "VolunteerOrganizationName",
                    "BeginDate",
                    "EndDate",
                    "Role",
                    "Description",
                    "Cause",
                ],
                rows=[],
            ),
        )

    def append_csv_row(self, model: CandidateModel) -> None:
        self.csv.rows.append(
            [
                model.user_id,
                model.name,
                model.recruiter_id,
                model.obs,
                model.invite_date,
            ]
        )

    def append_csv_company_rel_row(
        self, from_model: CandidateModel, to_model: Experience
    ) -> None:
        self.csv.company_relationship.rows.append(
            [
                from_model.name,
                to_model.company,
                to_model.current,
                to_model.begin_date,
                to_model.end_date,
                to_model.employee_status,
                to_model.title,
                clean_str(to_model.location),
                clean_str(to_model.description),
            ]
        )

    def append_csv_course_rel_row(
        self, from_model: CandidateModel, to_model: Course
    ) -> None:
        self.csv.course_relationship.rows.append([from_model.name, to_model.title])

    def append_csv_honor_rel_row(
        self, from_model: CandidateModel, to_model: Honor
    ) -> None:
        self.csv.honor_relationship.rows.append(
            [from_model.name, to_model.title, to_model.date]
        )

    def append_csv_job_rel_row(
        self, from_model: CandidateModel, to_model: Experience
    ) -> None:
        self.csv.honor_relationship.rows.append(
            [
                from_model.name,
                to_model.title,
                to_model.company,
                to_model.begin_date,
                to_model.end_date,
            ]
        )

    def append_csv_language_rel_row(
        self, from_model: CandidateModel, to_model: Language
    ) -> None:
        self.csv.language_relationship.rows.append(
            [
                from_model.name,
                to_model.name,
                to_model.proficiency,
            ]
        )

    def append_csv_project_rel_row(
        self, from_model: CandidateModel, to_model: Project
    ) -> None:
        self.csv.project_relationship.rows.append(
            [
                from_model.name,
                to_model.title,
                to_model.begin_date,
                to_model.end_date,
                clean_str(to_model.description),
            ]
        )

    def append_csv_publication_rel_row(
        self, from_model: CandidateModel, to_model: Publication
    ) -> None:
        self.csv.publication_relationship.rows.append(
            [
                from_model.name,
                to_model.title,
                to_model.date,
            ]
        )

    def append_csv_rec_letter_rel_row(
        self, from_model: CandidateModel, to_model: Recommendation
    ) -> None:
        self.csv.recommendation_letter_relationship.rows.append(
            [
                from_model.name,
                to_model.name,
            ]
        )

    def append_csv_school_rel_row(
        self, from_model: CandidateModel, to_model: Education
    ) -> None:
        self.csv.school_relationship.rows.append(
            [
                from_model.name,
                to_model.school,
                to_model.begin_date,
                to_model.end_date,
                to_model.degree,
                to_model.course,
                clean_str(to_model.description),
            ]
        )

    def append_csv_skill_rel_row(
        self, from_model: CandidateModel, to_model: Skill
    ) -> None:
        self.csv.skill_relationship.rows.append(
            [
                from_model.name,
                to_model.name,
            ]
        )

    def append_csv_volunteer_org_rel_row(
        self, from_model: CandidateModel, to_model: Volunteer
    ) -> None:
        self.csv.volunteer_organization_relationship.rows.append(
            [
                from_model.name,
                to_model.organization,
                to_model.begin_date,
                to_model.end_date,
                to_model.role,
                clean_str(to_model.description),
                to_model.cause,
            ]
        )

    def import_csv(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(key=CSV_FILE_NAME)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MERGE (n:{NODE_LABEL} {{name: row.Name}})
            ON CREATE
                SET
                    n.userId = row.UserId,
                    n.recruiterId = row.RecruiterId,
                    n.obs = row.Obs,
                    n.inviteDate = row.InviteDate
            ON MATCH
                SET
                    n.userId = row.UserId,
                    n.recruiterId = row.RecruiterId,
                    n.obs = row.Obs,
                    n.inviteDate = row.InviteDate
            """
            g.run(query)
            logger.info(f"import csv took: {elapsed()} sec")

    def import_csv_company_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_COMPANY_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (company:{COMPANY_NODE_LABEL} {{name: row.CompanyName}})
            CREATE (candidate)-[
                :{relationship.WorksFor.__name__} {{
                    current: row.Current,
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    employeeStatus: row.EmployeeStatus,
                    title: row.Title,
                    location: row.Location,
                    description: row.Description
                }}
            ]->(company)
            """
            g.run(query)
            logger.info(f"company_rel:import csv took: {elapsed()} sec")

    def import_csv_course_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_COURSE_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (course:{COURSE_NODE_LABEL} {{title: row.CourseTitle}})
            CREATE (candidate)-[
                :{relationship.Takes.__name__}
            ]->(course)
            """
            g.run(query)
            logger.info(f"course_rel:import csv took: {elapsed()} sec")

    def import_csv_honor_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_HONOR_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (honor:{HONOR_NODE_LABEL} {{title: row.HonorTitle}})
            CREATE (candidate)-[
                :{relationship.AwardedFor.__name__} {{
                    date: row.Date
                }}
            ]->(honor)
            """
            g.run(query)
            logger.info(f"honor_rel:import csv took: {elapsed()} sec")

    def import_csv_job_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_JOB_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (job:{JOB_NODE_LABEL} {{title: row.JobTitle}})
            CREATE (candidate)-[
                :{relationship.WorksAs.__name__} {{
                    companyName: row.CompanyName,
                    beginDate: row.BeginDate,
                    endDate: row.EndDate
                }}
            ]->(job)
            """
            g.run(query)
            logger.info(f"job_rel:import csv took: {elapsed()} sec")

    def import_csv_language_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_LANGUAGE_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (language:{LANGUAGE_NODE_LABEL} {{name: row.LanguageName}})
            CREATE (candidate)-[
                :{relationship.Speaks.__name__} {{
                    proficiency: row.Proficiency
                }}
            ]->(language)
            """
            g.run(query)
            logger.info(f"language_rel:import csv took: {elapsed()} sec")

    def import_csv_project_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_PROJECT_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (project:{PROJECT_NODE_LABEL} {{title: row.ProjectTitle}})
            CREATE (candidate)-[
                :{relationship.ParticipatesIn.__name__} {{
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    description: row.Description
                }}
            ]->(project)
            """
            g.run(query)
            logger.info(f"project_rel:import csv took: {elapsed()} sec")

    def import_csv_publication_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_PUBLICATION_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (publication:{PUBLICATION_NODE_LABEL} {{title: row.PublicationTitle}})
            CREATE (candidate)-[
                :{relationship.Published.__name__} {{
                    date: row.Date
                }}
            ]->(publication)
            """
            g.run(query)
            logger.info(f"publication_rel:import csv took: {elapsed()} sec")

    def import_csv_rec_letter_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_REC_LETTER_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (recommendationLetter:{RECOMMENDATION_LETTER_NODE_LABEL} {{
                name: row.RecommendationLetterName
            }})
            CREATE (candidate)-[
                :{relationship.Received.__name__}
            ]->(recommendationLetter)
            """
            g.run(query)
            logger.info(f"recommendation_letter_rel:import csv took: {elapsed()} sec")

    def import_csv_school_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_SCHOOL_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (school:{SCHOOL_NODE_LABEL} {{name: row.SchoolName}})
            CREATE (candidate)-[
                :{relationship.BelongsTo.__name__} {{
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    degree: row.Degree,
                    course: row.Course,
                    description: row.Description
                }}
            ]->(school)
            """
            g.run(query)
            logger.info(f"school_rel:import csv took: {elapsed()} sec")

    def import_csv_skill_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_SKILL_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (skill:{SKILL_NODE_LABEL} {{name: row.SkillName}})
            CREATE (candidate)-[
                :{relationship.Possesses.__name__}
            ]->(skill)
            """
            g.run(query)
            logger.info(f"skill_rel:import csv took: {elapsed()} sec")

    def import_csv_volunteer_org_rel(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(CSV_NAME_CAND_VOLUNTEER_ORG_REL)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (volunteerOrganization:{VOLUNTEER_ORGANIZATION_NODE_LABEL} {{
                name: row.VolunteerOrganizationName
            }})
            CREATE (candidate)-[
                :{relationship.ParticipatesIn.__name__} {{
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    role: row.Role,
                    description: row.Description,
                    cause: row.Cause
                }}
            ]->(volunteerOrganization)
            """
            g.run(query)
            logger.info(f"volunteer_organization_rel:import csv took: {elapsed()} sec")

    def create_constraint(self, g: Graph) -> None:
        g.schema.create_uniqueness_constraint(COMPANY_NODE_LABEL, "name")
        g.schema.create_uniqueness_constraint(COURSE_NODE_LABEL, "title")
        g.schema.create_uniqueness_constraint(HONOR_NODE_LABEL, "title")
        g.schema.create_uniqueness_constraint(JOB_NODE_LABEL, "title")
        g.schema.create_uniqueness_constraint(LANGUAGE_NODE_LABEL, "name")
        g.schema.create_uniqueness_constraint(PROJECT_NODE_LABEL, "title")
        g.schema.create_uniqueness_constraint(PUBLICATION_NODE_LABEL, "title")
        g.schema.create_uniqueness_constraint(RECOMMENDATION_LETTER_NODE_LABEL, "name")
        g.schema.create_uniqueness_constraint(SCHOOL_NODE_LABEL, "name")
        g.schema.create_uniqueness_constraint(SKILL_NODE_LABEL, "name")
        g.schema.create_uniqueness_constraint(VOLUNTEER_ORGANIZATION_NODE_LABEL, "name")
        g.schema.create_uniqueness_constraint(NODE_LABEL, "name")


candidate = Candidate()
