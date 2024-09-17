from fastapi import APIRouter, Request, Response
from starlette_context import context

from ...lib.log import LoggingFormat, setup_logger
from ...ai.open_ai import OpenAIHandler

setup_logger(fmt=LoggingFormat.JSON, level="DEBUG")
router = APIRouter(prefix="/v1", tags=["review"])

@router.post("/review")
async def github(request: Request):
    data = request.json()
    api_key = data.get("api_key", "")
    if not api_key:
        return Response(content={"error":"Error key"}, status_code=401)
    base_url = data.get("base_url", "BASE_URL") #default open ai
    model = data.get("model")
    content = data.get("content")
    system = data.get("system")
    open_ai = OpenAIHandler(api_key=api_key, base_url=base_url)
    resp, finish_reason = open_ai.chat_completion(model=model, system=system, user="admin", messages=content)
    #Call git comment
    return resp, finish_reason #Will change to return success or fail when git commit

