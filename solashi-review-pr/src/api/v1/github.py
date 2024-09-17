from fastapi import APIRouter
from starlette_context import context

from ...lib.log import LoggingFormat, setup_logger

setup_logger(fmt=LoggingFormat.JSON, level="DEBUG")
router = APIRouter(prefix="/v1", tags=["github"])

@router.post("/github")
async def github():
    return {"message": "Hello review github"}

