import logging
from typing import Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.graph.course_node import NODE_LABEL
from app.model.csv import CsvStruct
from app.model.linkedin.candidate import Course as CourseModel
from app.service import graph
from app.util.string import clean_str
from app.util.timer import elapsed_timer

logger = logging.getLogger(__name__)


CSV_FILE_NAME = "course.csv"


class Course:
    def __init__(self):
        self.csv = CsvStruct(
            filename=CSV_FILE_NAME,
            headers=["Title"],
            rows=[],
        )

    def append_csv_row(self, model: CourseModel) -> None:
        self.csv.rows.append(
            [
                clean_str(model.title),
            ]
        )

    def create_constraint(self, g: Graph) -> None:
        g.schema.create_uniqueness_constraint(NODE_LABEL, "title")

    def import_csv(self, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(key=CSV_FILE_NAME)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MERGE (n:{NODE_LABEL} {{title: row.Title}})
            """
            g.run(query)
            logger.info(f"import csv took: {elapsed()} sec")

    def find(self, g: Graph, title: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, title=title).first()


course = Course()
