from fastapi import APIRouter

from app.api.v1.endpoint import candidates, graph

api_router = APIRouter()

api_router.include_router(candidates.router, prefix="/linkedin", tags=["candidates"])
api_router.include_router(graph.router, prefix="/neo4j", tags=["graph"])
