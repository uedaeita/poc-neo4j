import csv
import logging
from tempfile import NamedTemporaryFile
from typing import List, Optional

from py2neo import Graph

from app.core.config import Settings
from app.graph.candidate_node import NODE_LABEL, candidate_node
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
    Interest,
    Language,
    Project,
    Publication,
    Recommendation,
    Skill,
    Volunteer,
)
from app.service import graph
from app.service.aws import s3
from app.util.timer import elapsed_timer

logger = logging.getLogger(__name__)


BUCKET_NAME = "xaion-neo4j-csv"
BUCKET_LOCATION = (
    f"{Settings.S3_ENDPOINT}/{BUCKET_NAME}"
    if Settings.S3_ENDPOINT
    else s3.client._endpoint.host.replace("https://", f"https://{BUCKET_NAME}.")
)


class Candidate:
    def create_all(
        self,
        g: Graph,
        candidates: List[CandidateModel],
        courses: List[Course],
        educations: List[Education],
        experiences: List[Experience],
        honors: List[Honor],
        interests: List[Interest],
        languages: List[Language],
        projects: List[Project],
        publications: List[Publication],
        recommendations: List[Recommendation],
        skills: List[Skill],
        volunteers: List[Volunteer],
    ) -> None:
        # create all candidates with relationships
        tx = g.begin()
        for candidate in candidates:
            candidate_node.create_node(tx, obj_in=candidate)
            for i in candidate.resume.experiences:
                to_node = graph.company.find(g=g, name=i.company)
                if to_node:
                    candidate_node.connect_company(tx, to_node=to_node, obj_in=i)
                to_node = graph.job.find(g=g, title=i.title)
                if to_node:
                    candidate_node.connect_job(tx, to_node=to_node, obj_in=i)
            for i in candidate.resume.courses:
                to_node = graph.course.find(g=g, title=i.title)
                if to_node:
                    candidate_node.connect_course(tx, to_node=to_node)
            for i in candidate.resume.honors:
                to_node = graph.honor.find(g=g, title=i.title)
                if to_node:
                    candidate_node.connect_honor(tx, to_node=to_node, obj_in=i)
            for i in candidate.resume.projects:
                to_node = graph.project.find(g=g, title=i.title)
                if to_node:
                    candidate_node.connect_project(tx, to_node=to_node, obj_in=i)
            for i in candidate.resume.publications:
                to_node = graph.publication.find(g=g, title=i.title)
                if to_node:
                    candidate_node.connect_publication(tx, to_node=to_node, obj_in=i)
            for i in candidate.resume.recommendations:
                to_node = graph.recommendation_letter.find(g=g, name=i.name)
                if to_node:
                    candidate_node.connect_recommendation_letter(tx, to_node=to_node)
            for i in candidate.resume.educations:
                to_node = graph.school.find(g=g, name=i.school)
                if to_node:
                    candidate_node.connect_school(tx, to_node=to_node, obj_in=i)
            for i in candidate.resume.skills:
                to_node = graph.skill.find(g=g, name=i.name)
                if to_node:
                    candidate_node.connect_skill(tx, to_node=to_node)
            for i in candidate.resume.volunteers:
                to_node = graph.volunteer_organization.find(g=g, name=i.organization)
                if to_node:
                    candidate_node.connect_volunteer_organization(
                        tx, to_node=to_node, obj_in=i
                    )
            for i in candidate.resume.languages:
                to_node = graph.language.find(g=g, name=i.name)
                if to_node:
                    candidate_node.connect_language(tx=tx, to_node=to_node, obj_in=i)
        g.commit(tx)

    def import_all(self, g: Graph, models: List[CandidateModel]) -> None:
        with elapsed_timer() as elapsed:
            candidate_obj = CandidateImportCsv(
                filename="candidate.csv",
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
                    filename="candidate_company_relationship.csv",
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
                    filename="candidate_course_relationship.csv",
                    headers=["CandidateName", "CourseTitle"],
                    rows=[],
                ),
                honor_relationship=CsvStruct(
                    filename="candidate_honor_relationship.csv",
                    headers=["CandidateName", "HonorTitle", "Date"],
                    rows=[],
                ),
                job_relationship=CsvStruct(
                    filename="candidate_job_relationship.csv",
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
                    filename="candidate_language_relationship.csv",
                    headers=["CandidateName", "LanguageName", "Proficiency"],
                    rows=[],
                ),
                project_relationship=CsvStruct(
                    filename="candidate_project_relationship.csv",
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
                    filename="candidate_publication_relationship.csv",
                    headers=["CandidateName", "PublicationTitle", "Date"],
                    rows=[],
                ),
                recommendation_letter_relationship=CsvStruct(
                    filename="candidate_recommendation_letter_relationship.csv",
                    headers=["CandidateName", "RecommendationLetterName"],
                    rows=[],
                ),
                school_relationship=CsvStruct(
                    filename="candidate_school_relationship.csv",
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
                    filename="candidate_skill_relationship.csv",
                    headers=["CandidateName", "SkillName"],
                    rows=[],
                ),
                volunteer_organization_relationship=CsvStruct(
                    filename="candidate_volunteer_organization_relationship.csv",
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
            company_obj = CsvStruct(
                filename="company.csv",
                headers=["Name"],
                rows=[],
            )
            course_obj = CsvStruct(
                filename="course.csv",
                headers=["Title"],
                rows=[],
            )
            honor_obj = CsvStruct(
                filename="honor.csv",
                headers=["Title", "Issuer"],
                rows=[],
            )
            job_obj = CsvStruct(
                filename="job.csv",
                headers=["Title"],
                rows=[],
            )
            language_obj = CsvStruct(
                filename="language.csv",
                headers=["Name"],
                rows=[],
            )
            project_obj = CsvStruct(
                filename="project.csv",
                headers=["Title"],
                rows=[],
            )
            publication_obj = CsvStruct(
                filename="publication.csv",
                headers=["Title", "Link", "Description", "Publisher"],
                rows=[],
            )
            recommendation_letter_obj = CsvStruct(
                filename="recommendation_letter.csv",
                headers=["Name", "Headline", "Comment", "UserLink", "Photo"],
                rows=[],
            )
            school_obj = CsvStruct(
                filename="school.csv",
                headers=["Name"],
                rows=[],
            )
            skill_obj = CsvStruct(
                filename="skill.csv",
                headers=["Name"],
                rows=[],
            )
            volunteer_organization_obj = CsvStruct(
                filename="volunteer_organization.csv",
                headers=["Name"],
                rows=[],
            )
            for m in models:
                if not m.name:
                    continue

                candidate_obj.rows.append(
                    [m.user_id, m.name, m.recruiter_id, m.obs, m.invite_date]
                )
                if not m.resume:
                    continue
                for e in m.resume.experiences:
                    if e.company:
                        company_obj.rows.append([e.company])
                        candidate_obj.company_relationship.rows.append(
                            [
                                m.name,
                                e.company,
                                e.current,
                                e.begin_date,
                                e.end_date,
                                e.employee_status,
                                e.title,
                                self.__format_str(e.location),
                                self.__format_str(e.description),
                            ]
                        )
                    if e.title:
                        job_obj.rows.append([e.title])
                        candidate_obj.job_relationship.rows.append(
                            [m.name, e.title, e.company, e.begin_date, e.end_date]
                        )
                for c in m.resume.courses:
                    if c.title:
                        course_obj.rows.append([c.title])
                        candidate_obj.course_relationship.rows.append([m.name, c.title])
                for h in m.resume.honors:
                    if h.title:
                        honor_obj.rows.append([h.title, h.issuer])
                        candidate_obj.honor_relationship.rows.append(
                            [m.name, h.title, h.date]
                        )
                for lang in m.resume.languages:
                    if lang.name:
                        language_obj.rows.append([lang.name])
                        candidate_obj.language_relationship.rows.append(
                            [m.name, lang.name, lang.proficiency]
                        )
                for p in m.resume.projects:
                    if p.title:
                        project_obj.rows.append([p.title])
                        candidate_obj.project_relationship.rows.append(
                            [
                                m.name,
                                p.title,
                                p.begin_date,
                                p.end_date,
                                self.__format_str(p.description),
                            ]
                        )
                for p in m.resume.publications:
                    if p.title:
                        publication_obj.rows.append(
                            [
                                p.title,
                                p.link,
                                self.__format_str(p.description),
                                p.publisher,
                            ]
                        )
                        candidate_obj.publication_relationship.rows.append(
                            [m.name, p.title, p.date]
                        )
                for r in m.resume.recommendations:
                    if r.name:
                        recommendation_letter_obj.rows.append(
                            [
                                r.name,
                                r.headline,
                                self.__format_str(r.comment),
                                r.user_link,
                                r.photo,
                            ]
                        )
                        candidate_obj.recommendation_letter_relationship.rows.append(
                            [m.name, r.name]
                        )
                for e in m.resume.educations:
                    if e.school:
                        school_obj.rows.append([e.school])
                        candidate_obj.school_relationship.rows.append(
                            [
                                m.name,
                                e.school,
                                e.begin_date,
                                e.end_date,
                                e.degree,
                                e.course,
                                self.__format_str(e.description),
                            ]
                        )
                for s in m.resume.skills:
                    if s.name:
                        skill_obj.rows.append([s.name])
                        candidate_obj.skill_relationship.rows.append([m.name, s.name])
                for v in m.resume.volunteers:
                    if v.organization:
                        volunteer_organization_obj.rows.append([v.organization])
                        candidate_obj.volunteer_organization_relationship.rows.append(
                            [
                                m.name,
                                v.organization,
                                v.begin_date,
                                v.end_date,
                                v.role,
                                self.__format_str(v.description),
                                v.cause,
                            ]
                        )
            logger.info(f"create import objects took: {elapsed()} sec")

            csv_struct = company_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{COMPANY_NODE_LABEL} {{name: row.Name}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} companies took: {elapsed()} sec")

            csv_struct = course_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{COURSE_NODE_LABEL} {{title: row.Title}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} courses took: {elapsed()} sec")

            csv_struct = honor_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{HONOR_NODE_LABEL} {{title: row.Title}})
            ON MATCH SET
                n.issuer = row.Issuer
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} honors took: {elapsed()} sec")

            csv_struct = job_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{JOB_NODE_LABEL} {{title: row.Title}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} jobs took: {elapsed()} sec")

            csv_struct = language_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{LANGUAGE_NODE_LABEL} {{name: row.Name}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} languages took: {elapsed()} sec")

            csv_struct = project_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{PROJECT_NODE_LABEL} {{title: row.Title}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} projects took: {elapsed()} sec")

            csv_struct = publication_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{PUBLICATION_NODE_LABEL} {{title: row.Title}})
            ON MATCH
                SET
                    n.link = row.Link,
                    n.description = row.Description,
                    n.publisher = row.Publisher
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} publications took: {elapsed()} sec")

            csv_struct = recommendation_letter_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{RECOMMENDATION_LETTER_NODE_LABEL} {{name: row.Name}})
            ON MATCH
                SET
                    n.headline = row.Headline,
                    n.comment = row.Comment,
                    n.userLink = row.UserLink,
                    n.photo = row.Photo
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} recommendation letters took: {elapsed()} sec")

            csv_struct = school_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{SCHOOL_NODE_LABEL} {{name: row.Name}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} schools took: {elapsed()} sec")

            csv_struct = skill_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{SKILL_NODE_LABEL} {{name: row.Name}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} skills took: {elapsed()} sec")

            csv_struct = volunteer_organization_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{VOLUNTEER_ORGANIZATION_NODE_LABEL} {{name: row.Name}})
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} volunteer organizations took: {elapsed()} sec")

            csv_struct = candidate_obj
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MERGE (n:{NODE_LABEL} {{name: row.Name}})
            ON MATCH
                SET
                    n.userId = row.UserId,
                    n.recruiterId = row.RecruiterId,
                    n.obs = row.Obs,
                    n.inviteDate = row.InviteDate
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(f"import {count} candidates took: {elapsed()} sec")

            csv_struct = candidate_obj.company_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (company:{COMPANY_NODE_LABEL} {{name: row.CompanyName}})
            CREATE (candidate)-[
                :WORKS_FOR {{
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
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-company relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.course_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (course:{COURSE_NODE_LABEL} {{title: row.CourseTitle}})
            CREATE (candidate)-[:TAKES]->(course)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-course relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.honor_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (honor:{HONOR_NODE_LABEL} {{title: row.HonorTitle}})
            CREATE (candidate)-[:AWARDED_FOR {{date: row.Date}}]->(honor)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-honor relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.job_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (job:{JOB_NODE_LABEL} {{title: row.JobTitle}})
            CREATE (candidate)-[
                :WORKS_AS {{
                    companyName: row.CompanyName,
                    beginDate: row.BeginDate,
                    endDate: row.EndDate
                }}
            ]->(job)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-job relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.language_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (language:{LANGUAGE_NODE_LABEL} {{name: row.LanguageName}})
            CREATE (candidate)-[:SPEAKS {{proficiency: row.Proficiency}}]->(language)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-language relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.project_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (project:{PROJECT_NODE_LABEL} {{title: row.ProjectTitle}})
            CREATE (candidate)-[
                :PARTICIPATES_IN {{
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    description: row.Description
                }}
            ]->(project)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-project relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.publication_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (publication:{PUBLICATION_NODE_LABEL} {{title: row.PublicationTitle}})
            CREATE (candidate)-[:PUBLISHED {{date: row.Date}}]->(publication)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-publication relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.recommendation_letter_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (recommendationLetter:{RECOMMENDATION_LETTER_NODE_LABEL} {{
                name: row.RecommendationLetterName
            }})
            CREATE (candidate)-[:RECEIVED]->(recommendationLetter)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-recommendation letter relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.school_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (school:{SCHOOL_NODE_LABEL} {{name: row.SchoolName}})
            CREATE (candidate)-[
                :BELONGS_TO {{
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    degree: row.Degree,
                    course: row.Course,
                    description: row.Description
                }}
            ]->(school)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-school relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.skill_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (skill:{SKILL_NODE_LABEL} {{name: row.SkillName}})
            CREATE (candidate)-[:POSSESSES]->(skill)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-skill relationships took: {elapsed()} sec"
            )

            csv_struct = candidate_obj.volunteer_organization_relationship
            self.__upload_csv(csv_struct=csv_struct)
            csv_location = f"{BUCKET_LOCATION}/{csv_struct.filename}"
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_location}' AS row
            MATCH (candidate:{NODE_LABEL} {{name: row.CandidateName}})
            MATCH (volunteerOrganization:{VOLUNTEER_ORGANIZATION_NODE_LABEL} {{
                name: row.VolunteerOrganizationName
            }})
            CREATE (candidate)-[
                :PARTICIPATES_IN {{
                    beginDate: row.BeginDate,
                    endDate: row.EndDate,
                    role: row.Role,
                    description: row.Description,
                    cause: row.Cause
                }}
            ]->(volunteerOrganization)
            """
            g.run(query)
            count = len(csv_struct.rows)
            logger.info(
                f"import {count} candidate-volunteer organization relationships took: {elapsed()} sec"
            )

    def __upload_csv(self, csv_struct: CsvStruct):
        tmpfile = NamedTemporaryFile(delete=False)
        try:
            with open(tmpfile.name, "w") as file:
                writer = csv.writer(file)
                writer.writerows([csv_struct.headers, *csv_struct.rows])
            with open(tmpfile.name, "rb") as file:
                s3.upload_fileobj(file, bucket=BUCKET_NAME, key=csv_struct.filename)
        finally:
            tmpfile.close()

    def __format_str(self, s: Optional[str]) -> Optional[str]:
        if not s:
            return None
        return s.rstrip("\\")


candidate = Candidate()
