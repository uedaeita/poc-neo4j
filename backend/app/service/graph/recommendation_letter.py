import logging
from typing import Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.graph.recommendation_letter_node import NODE_LABEL
from app.model.csv import CsvStruct
from app.model.linkedin.candidate import Recommendation as RecommendationModel
from app.service import graph
from app.util.string import clean_str
from app.util.timer import elapsed_timer

logger = logging.getLogger(__name__)

CSV_FILE_NAME = "recommendation_letter.csv"


class RecommendationLetter:
    def __init__(self):
        self.csv = CsvStruct(
            filename=CSV_FILE_NAME,
            headers=["Name", "Headline", "Comment", "UserLink", "Photo"],
            rows=[],
        )

    def append_csv_row(self, model: RecommendationModel) -> None:
        self.csv.rows.append(
            [
                clean_str(model.name),
                clean_str(model.headline),
                clean_str(model.comment),
                model.user_link,
                model.photo,
            ]
        )

    def create_constraint(self, g: Graph) -> None:
        g.schema.create_uniqueness_constraint(NODE_LABEL, "name")

    def import_csv(cls, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = graph.schema.get_bucket_url(key=CSV_FILE_NAME)
            query = f"""
            USING PERIODIC COMMIT 5000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MERGE (n:{NODE_LABEL} {{name: row.Name}})
            ON CREATE
                SET
                    n.headline = row.Headline,
                    n.comment = row.Comment,
                    n.userLink = row.UserLink,
                    n.photo = row.Photo
            ON MATCH
                SET
                    n.headline = row.Headline,
                    n.comment = row.Comment,
                    n.userLink = row.UserLink,
                    n.photo = row.Photo
            """
            g.run(query)
            logger.info(f"import csv took: {elapsed()} sec")

    def find(self, g: Graph, name: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, name=name).first()


recommendation_letter = RecommendationLetter()
