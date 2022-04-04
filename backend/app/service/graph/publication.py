import logging
from typing import Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.graph.publication_node import NODE_LABEL
from app.model.csv import CsvStruct
from app.model.linkedin.candidate import Publication as PublicationModel
from app.service.graph import schema
from app.util.string import clean_str
from app.util.timer import elapsed_timer

logger = logging.getLogger(__name__)

CSV_FILE_NAME = "publication.csv"


class Publication:
    def __init__(self):
        self.csv = CsvStruct(
            filename=CSV_FILE_NAME,
            headers=["Title", "Link", "Description", "Publisher"],
            rows=[],
        )

    def append_csv_row(self, model: PublicationModel) -> None:
        if not model.title:
            return

        self.csv.rows.append(
            [
                model.title,
                model.link,
                clean_str(model.description),
                model.publisher,
            ]
        )

    def import_csv(cls, g: Graph) -> None:
        with elapsed_timer() as elapsed:
            csv_url = schema.get_bucket_url(key=CSV_FILE_NAME)
            query = f"""
            USING PERIODIC COMMIT 10000
            LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
            MERGE (n:{NODE_LABEL} {{title: row.Title}})
            ON CREATE
                SET
                    n.link = row.Link,
                    n.description = row.Description,
                    n.publisher = row.Publisher
            ON MATCH
                SET
                    n.link = row.Link,
                    n.description = row.Description,
                    n.publisher = row.Publisher
            """
            g.run(query)
            logger.info(f"import csv took: {elapsed()} sec")

    def find(self, g: Graph, title: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, title=title).first()


publication = Publication()
