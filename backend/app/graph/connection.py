from py2neo import Graph

from app.core.config import Settings


def GraphLocal() -> Graph:
    return Graph(
        Settings.NEO4J_ENDPOINT,
        auth=(
            Settings.NEO4J_USER,
            Settings.NEO4J_PASSWORD,
        ),
    )
