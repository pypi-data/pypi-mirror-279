from pydantic import BaseModel
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.requests import Request

from komodoro import populate
from komodoro.params import Path


@populate()
async def homepage(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Hello, world!")


class Model(BaseModel):
    name: str
    age: int


@populate()
async def homepage2(request: Request) -> Model:
    return Model(name="John", age=42)


@populate()
async def homepage3() -> Model:
    return Model(name="John", age=42)


@populate()
async def path_params(name: Path[str]) -> Model:
    return Model(name=name, age=42)


app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/2", homepage2),
        Route("/3", homepage3),
        Route("/path/{name}", path_params),
    ]
)
