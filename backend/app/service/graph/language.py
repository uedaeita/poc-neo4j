import csv
import logging
from tempfile import NamedTemporaryFile
from typing import List, Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.core.config import Settings
from app.graph.language_node import NODE_LABEL, language_node
from app.model.linkedin.candidate import Language as LanguageModel
from app.service.aws import s3

logger = logging.getLogger(__name__)


class Language:
    def create_all(self, g: Graph, models: List[LanguageModel]) -> None:
        tx = g.begin()

        uniq_keys: List[str] = []
        for m in models:
            if m.name not in uniq_keys:
                uniq_keys.append(m.name)
                language_node.create_node(tx, obj_in=m)

        g.commit(tx)

    def import_all(self, g: Graph, models: List[LanguageModel]) -> None:
        headers = [["Id", "Name"]]
        rows = [[i + 1, m.name] for i, m in enumerate(models)]
        tmpfile = NamedTemporaryFile(delete=False)
        try:
            with open(tmpfile.name, "w") as file:
                writer = csv.writer(file)
                writer.writerows(headers + rows)
            with open(tmpfile.name, "rb") as file:
                s3.upload_fileobj(file, bucket="xaion-neo4j-csv", key="languages.csv")
        finally:
            tmpfile.close()
        query = f"""
        LOAD CSV WITH HEADERS FROM '{Settings.S3_ENDPOINT}/xaion-neo4j-csv/languages.csv' AS row
        WITH row WHERE row.Id IS NOT NULL AND row.Name IS NOT NULL
        MERGE (n:{NODE_LABEL} {{languageId: row.Id, name: row.Name}})
        """
        g.run(query)

    def find(self, g: Graph, name: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, name=name).first()


language = Language()
