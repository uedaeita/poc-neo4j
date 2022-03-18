import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import Settings

logging.basicConfig(level=getattr(logging, Settings.LOG_LEVEL))

app = FastAPI(title="PoC Neo4j")


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> Any:
    error_message = f"Unexpected error occurred: {exc}"
    return JSONResponse(status_code=500, content={"detail": error_message})


@app.get("/")
def health_check() -> Dict[str, str]:
    return {"version": "1.0.0"}


app.include_router(api_router, prefix="/api")
