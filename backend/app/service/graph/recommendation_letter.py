import csv
import logging
from tempfile import NamedTemporaryFile
from typing import List, Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.core.config import Settings
from app.graph.recommendation_letter_node import NODE_LABEL, recommendation_letter_node
from app.model.linkedin.candidate import Recommendation as RecommendationModel
from app.service.aws import s3

logger = logging.getLogger(__name__)


class RecommendationLetter:
    def create_all(self, g: Graph, models: List[RecommendationModel]) -> None:
        tx = g.begin()

        uniq_keys: List[str] = []
        for m in models:
            if m.name not in uniq_keys:
                uniq_keys.append(m.name)
                recommendation_letter_node.create_node(tx, obj_in=m)

        g.commit(tx)

    def import_all(self, g: Graph, models: List[RecommendationModel]) -> None:
        headers = [["Id", "Name", "Headline", "Comment", "UserLink", "Photo"]]
        rows = [
            [i + 1, m.name, m.headline, m.comment, m.user_link, m.photo]
            for i, m in enumerate(models)
        ]
        tmpfile = NamedTemporaryFile(delete=False)
        try:
            with open(tmpfile.name, "w") as file:
                writer = csv.writer(file)
                writer.writerows(headers + rows)
            with open(tmpfile.name, "rb") as file:
                s3.upload_fileobj(
                    file, bucket="xaion-neo4j-csv", key="recommendation_letters.csv"
                )
        finally:
            tmpfile.close()
        query = f"""
        LOAD CSV WITH HEADERS FROM '{Settings.S3_ENDPOINT}/xaion-neo4j-csv/recommendation_letters.csv' AS row
        WITH row WHERE row.Id IS NOT NULL AND row.Name IS NOT NULL
        MERGE (n:{NODE_LABEL} {{recommendationLetterId: row.Id, name: row.Name, headline: row.Headline, comment: row.Comment, userLink: row.UserLink, photo: row.Photo}})
        """
        g.run(query)

    def find(self, g: Graph, name: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, name=name).first()


recommendation_letter = RecommendationLetter()
