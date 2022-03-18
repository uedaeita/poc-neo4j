from typing import Generator

from app.db.session import SessionLocal
from app.graph.connection import GraphLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_graph() -> Generator:
    graph = GraphLocal()
    yield graph
