import csv
import logging
import math
from tempfile import NamedTemporaryFile

from py2neo import Graph

from app.core.config import Settings
from app.graph.candidate_node import NODE_LABEL as CANDIDATE_NODE_LABEL
from app.graph.skill_node import NODE_LABEL as SKILL_NODE_LABEL
from app.model.csv import CsvStruct
from app.service.aws import s3

logger = logging.getLogger(__name__)

CSV_BUCKET = "xaion-neo4j-csv"
BUCKET_LOCATION = (
    f"{Settings.S3_ENDPOINT}/{CSV_BUCKET}"
    if Settings.S3_ENDPOINT
    else s3.client._endpoint.host.replace("https://", f"https://{CSV_BUCKET}.")
)
LIMIT = 100_000
ROWS_PER_TX = 10_000


class Schema:
    def delete_all_nodes(self, g: Graph) -> None:
        # FIXME: Delete posseses relationships first due to the amount.
        query = f"""
        MATCH (:{CANDIDATE_NODE_LABEL})-[r:POSSESSES]-(:{SKILL_NODE_LABEL})
        RETURN COUNT(r)
        """
        rel_count = g.run(query).data()[0].get("COUNT(r)", 0)
        r = math.ceil(rel_count / LIMIT)
        for _ in range(0, r):
            query = f"""
            MATCH (:{CANDIDATE_NODE_LABEL})-[r:POSSESSES]-(:{SKILL_NODE_LABEL})
            WITH r LIMIT {LIMIT} DELETE r
            """
            g.run(query)

        first_node = g.nodes.match().limit(1).first()
        start_id = first_node.identity if first_node else 0
        r = math.ceil(len(g.nodes) / LIMIT)
        for i in range(1, r + 1):
            until_id = start_id + LIMIT * i
            query = f"""
            MATCH (n) WHERE id(n) < {until_id}
            CALL {{ WITH n DETACH DELETE n }}
            IN TRANSACTIONS OF {ROWS_PER_TX} ROWS
            """
            res = g.run(query)
            res.stats()

    def delete_all_constraints(self, g: Graph) -> None:
        constraints = g.run("CALL db.constraints() YIELD name RETURN name").data()
        for constraint in constraints:
            g.run(f"DROP CONSTRAINT {constraint['name']}")

    def upload_csv_to_s3(self, cs: CsvStruct):
        tmpfile = NamedTemporaryFile(delete=False)
        try:
            with open(tmpfile.name, "w") as file:
                writer = csv.writer(file, doublequote=False, escapechar="\\")
                writer.writerows([cs.headers, *cs.rows])
            with open(tmpfile.name, "rb") as file:
                s3.upload_fileobj(file, bucket=CSV_BUCKET, key=cs.filename)
            logger.info(f"uploaded {cs.filename} (rows: {len(cs.rows)}).")
        except Exception as e:
            logger.error(e)
        finally:
            tmpfile.close()

    def get_bucket_url(self, key: str) -> str:
        return f"{BUCKET_LOCATION}/{key}"


schema = Schema()
