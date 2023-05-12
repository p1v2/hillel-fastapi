import json
from typing import Annotated, Optional

from app.routers.books import router as books

from fastapi import FastAPI, Response, Header, Cookie, UploadFile, Request

app = FastAPI()
app.include_router(
    router=books,
)


# @app.middleware("http")
# async def check_basic_auth(request: Request, call_next):
#     if not request.headers.get("authorization"):
#         return Response(status_code=401, content=json.dumps({"message": "Unauthorized"}))
#     if request.headers.get("authorization") != "Bearer 123":
#         return Response(status_code=403, content=json.dumps({"message": "Forbidden"}))
#
#     return await call_next(request)


@app.get("/")
async def echo(message: str = "Hello World"):
    return {"message": message}


# @app.get("/{message}")
# async def echo_with_url_param(message: str, name: str):
#     return {"message": f"{message} {name}"}


@app.get("/user_agent")
async def get_user_agent(user_agent: Annotated[Optional[str], Header()] = None):
    return {"user_agent": user_agent}


# Getting params from cookies
@app.get("/cookie")
async def get_cookie_or_default(
    tracking: Optional[str] = Cookie(default=None),
):
    response_content = json.dumps({"tracking": tracking})
    response = Response(content=response_content)

    # Set tracking cookies
    response.set_cookie(key="tracking", value="yes")
    return response


# Upload file
@app.post("/upload")
async def upload_file(file: UploadFile):
    return {"size": len(await file.read())}

