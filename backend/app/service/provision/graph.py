import logging

from py2neo import Graph
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.graph.connection import GraphLocal
from app.service import graph, linkedin
from app.service.graph import schema
from app.util.timer import elapsed_timer

logger = logging.getLogger(__name__)


def provision(db: Session, g: Graph) -> None:
    with elapsed_timer() as elapsed:
        schema.delete_all_nodes(g)
        schema.delete_all_constraints(g=g)
        logger.info(f"clean graph took: {elapsed()} sec")

    with elapsed_timer() as elapsed:
        candidates = linkedin.candidate.candidate.get_all(db=db)
        logger.info(f"get mysql {len(candidates)} candidates took: {elapsed()} sec")

    with elapsed_timer() as elapsed:
        candidate_service = graph.candidate
        company_service = graph.company
        course_service = graph.course
        honor_service = graph.honor
        job_service = graph.job
        language_service = graph.language
        project_service = graph.project
        publication_service = graph.publication
        rec_letter_service = graph.recommendation_letter
        school_service = graph.school
        skill_service = graph.skill
        volunteer_org_service = graph.volunteer_organization

        for m in candidates:
            if not m.name:
                continue
            candidate_service.append_csv_row(model=m)

            if not m.resume:
                continue
            for e in m.resume.experiences:
                if e.company:
                    company_service.append_csv_row(model=e)
                    candidate_service.append_csv_company_rel_row(
                        from_model=m, to_model=e
                    )
                if e.title:
                    job_service.append_csv_row(model=e)
                    candidate_service.append_csv_job_rel_row(from_model=m, to_model=e)
            for c in m.resume.courses:
                if c.title:
                    course_service.append_csv_row(model=c)
                    candidate_service.append_csv_course_rel_row(
                        from_model=m, to_model=c
                    )
            for h in m.resume.honors:
                if h.title:
                    honor_service.append_csv_row(model=h)
                    candidate_service.append_csv_honor_rel_row(from_model=m, to_model=h)
            for lang in m.resume.languages:
                if lang.name:
                    language_service.append_csv_row(model=lang)
                    candidate_service.append_csv_language_rel_row(
                        from_model=m, to_model=lang
                    )
            for p in m.resume.projects:
                if p.title:
                    project_service.append_csv_row(model=p)
                    candidate_service.append_csv_project_rel_row(
                        from_model=m, to_model=p
                    )
            for p in m.resume.publications:
                if p.title:
                    publication_service.append_csv_row(model=p)
                    candidate_service.append_csv_publication_rel_row(
                        from_model=m, to_model=p
                    )
            for r in m.resume.recommendations:
                if r.name:
                    rec_letter_service.append_csv_row(model=r)
                    candidate_service.append_csv_rec_letter_rel_row(
                        from_model=m, to_model=r
                    )
            for e in m.resume.educations:
                if e.school:
                    school_service.append_csv_row(model=e)
                    candidate_service.append_csv_school_rel_row(
                        from_model=m, to_model=e
                    )
            for s in m.resume.skills:
                if s.name:
                    skill_service.append_csv_row(model=s)
                    candidate_service.append_csv_skill_rel_row(from_model=m, to_model=s)
            for v in m.resume.volunteers:
                if v.organization:
                    volunteer_org_service.append_csv_row(model=v)
                    candidate_service.append_csv_volunteer_org_rel_row(
                        from_model=m, to_model=v
                    )
        logger.info(f"create csv rows took: {elapsed()} sec")

    with elapsed_timer() as elapsed:
        schema.upload_csv_to_s3(csv_struct=company_service.csv)
        schema.upload_csv_to_s3(csv_struct=course_service.csv)
        schema.upload_csv_to_s3(csv_struct=honor_service.csv)
        schema.upload_csv_to_s3(csv_struct=job_service.csv)
        schema.upload_csv_to_s3(csv_struct=language_service.csv)
        schema.upload_csv_to_s3(csv_struct=project_service.csv)
        schema.upload_csv_to_s3(csv_struct=publication_service.csv)
        schema.upload_csv_to_s3(csv_struct=rec_letter_service.csv)
        schema.upload_csv_to_s3(csv_struct=skill_service.csv)
        schema.upload_csv_to_s3(csv_struct=school_service.csv)
        schema.upload_csv_to_s3(csv_struct=volunteer_org_service.csv)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.company_relationship)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.course_relationship)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.honor_relationship)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.job_relationship)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.language_relationship)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.project_relationship)
        schema.upload_csv_to_s3(
            csv_struct=candidate_service.csv.publication_relationship
        )
        schema.upload_csv_to_s3(
            csv_struct=candidate_service.csv.recommendation_letter_relationship
        )
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.school_relationship)
        schema.upload_csv_to_s3(csv_struct=candidate_service.csv.skill_relationship)
        schema.upload_csv_to_s3(
            csv_struct=candidate_service.csv.volunteer_organization_relationship
        )
        logger.info(f"upload csv took: {elapsed()} sec")

    with elapsed_timer() as elapsed:
        candidate_service.create_constraint(g=g)
        logger.info(f"create constraints took: {elapsed()} sec")

    with elapsed_timer() as elapsed:
        company_service.import_csv(g=g)
        course_service.import_csv(g=g)
        honor_service.import_csv(g=g)
        job_service.import_csv(g=g)
        language_service.import_csv(g=g)
        project_service.import_csv(g=g)
        publication_service.import_csv(g=g)
        rec_letter_service.import_csv(g=g)
        school_service.import_csv(g=g)
        skill_service.import_csv(g=g)
        volunteer_org_service.import_csv(g=g)
        candidate_service.import_csv(g=g)
        candidate_service.import_csv_company_rel(g=g)
        candidate_service.import_csv_course_rel(g=g)
        candidate_service.import_csv_honor_rel(g=g)
        candidate_service.import_csv_job_rel(g=g)
        candidate_service.import_csv_language_rel(g=g)
        candidate_service.import_csv_project_rel(g=g)
        candidate_service.import_csv_publication_rel(g=g)
        candidate_service.import_csv_rec_letter_rel(g=g)
        candidate_service.import_csv_school_rel(g=g)
        candidate_service.import_csv_skill_rel(g=g)
        candidate_service.import_csv_volunteer_org_rel(g=g)
        logger.info(f"import graph took: {elapsed()} sec")


if __name__ == "__main__":
    logger.info("provision start.")

    db = SessionLocal()
    g = GraphLocal()
    provision(db=db, g=g)

    logger.info("provision end.")
