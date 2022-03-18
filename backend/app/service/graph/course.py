import csv
import logging
from tempfile import NamedTemporaryFile
from typing import List, Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.core.config import Settings
from app.graph.course_node import NODE_LABEL, course_node
from app.model.linkedin.candidate import Course as CourseModel
from app.service.aws import s3

logger = logging.getLogger(__name__)


class Course:
    def create_all(self, g: Graph, models: List[CourseModel]) -> None:
        tx = g.begin()

        uniq_keys: List[str] = []
        for m in models:
            if m.title not in uniq_keys:
                uniq_keys.append(m.title)
                course_node.create_node(tx, obj_in=m)

        g.commit(tx)

    def import_all(self, g: Graph, models: List[CourseModel]) -> None:
        headers = [["Id", "Title"]]
        rows = [[i + 1, m.title] for i, m in enumerate(models)]
        tmpfile = NamedTemporaryFile(delete=False)
        try:
            with open(tmpfile.name, "w") as file:
                writer = csv.writer(file)
                writer.writerows(headers + rows)
            with open(tmpfile.name, "rb") as file:
                s3.upload_fileobj(file, bucket="xaion-neo4j-csv", key="courses.csv")
        finally:
            tmpfile.close()

        query = f"""
        LOAD CSV WITH HEADERS FROM '{Settings.S3_ENDPOINT}/xaion-neo4j-csv/courses.csv' AS row
        WITH row WHERE row.Id IS NOT NULL AND row.Title IS NOT NULL
        MERGE (n:{NODE_LABEL} {{courseId: row.Id, title: row.Title}})
        """
        g.run(query)

    def find(self, g: Graph, title: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, title=title).first()


course = Course()
