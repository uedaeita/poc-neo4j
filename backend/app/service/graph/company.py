import csv
import logging
from tempfile import NamedTemporaryFile
from typing import List, Optional

from py2neo import Graph, Node
from py2neo.matching import NodeMatcher

from app.core.config import Settings
from app.graph.company_node import NODE_LABEL, company_node
from app.model.linkedin.candidate import Experience as ExperienceModel
from app.service.aws import s3

logger = logging.getLogger(__name__)


class Company:
    def create_all(self, g: Graph, models: List[ExperienceModel]) -> None:
        tx = g.begin()

        uniq_keys: List[str] = []
        for m in models:
            if m.company not in uniq_keys:
                uniq_keys.append(m.company)
                company_node.create_node(tx, obj_in=m)

        g.commit(tx)

    def import_all(self, g: Graph, models: List[ExperienceModel]) -> None:
        headers = [["Id", "Name"]]
        rows = [[i + 1, m.company] for i, m in enumerate(models)][:10]
        tmpfile = NamedTemporaryFile(delete=False)
        try:
            with open(tmpfile.name, "w") as file:
                writer = csv.writer(file)
                writer.writerows(headers + rows)
            with open(tmpfile.name, "rb") as file:
                s3.upload_fileobj(file, bucket="xaion-neo4j-csv", key="companies.csv")
        finally:
            tmpfile.close()
        query = f"""
        LOAD CSV WITH HEADERS FROM '{Settings.S3_ENDPOINT}/xaion-neo4j-csv/companies.csv' AS row
        WITH row WHERE row.Id IS NOT NULL AND row.Name IS NOT NULL
        MERGE (n:{NODE_LABEL} {{companyId: row.Id, name: row.Name}})
        """
        g.run(query)

    def find(self, g: Graph, name: str) -> Optional[Node]:
        nodes = NodeMatcher(g)
        return nodes.match(NODE_LABEL, name=name).first()


company = Company()
