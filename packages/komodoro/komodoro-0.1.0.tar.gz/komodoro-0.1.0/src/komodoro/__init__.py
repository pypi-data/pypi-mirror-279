from typing import Awaitable, Callable
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel
from typing_extensions import get_args, get_origin, get_type_hints
from typing import Annotated

from komodoro.params import PathParam


Endpoint = Callable[..., Awaitable[BaseModel | Response]]


class Komodoro:
    def populate(self):
        def decorator(endpoint: Endpoint) -> Callable[[Request], Awaitable[Response]]:
            annotations = get_type_hints(endpoint, include_extras=True)
            request_key = None
            path_params: dict[str, PathParam] = {}

            for key, value in annotations.items():
                if key == "return":
                    continue
                if value == Request:
                    request_key = key
                origin = get_origin(value)
                if origin == Annotated:
                    args = get_args(value)
                    for arg in args:
                        if isinstance(arg, PathParam):
                            path_params[key] = arg

            async def wrapper(request: Request) -> Response:
                params = {}
                if request_key:
                    params[request_key] = request
                if path_params:
                    for key in path_params:
                        value = request.path_params.get(key)
                        # TODO: Handle validation.
                        params[key] = value
                model = await endpoint(**params)
                if isinstance(model, Response):
                    return model
                return Response(content=model.model_dump_json(), media_type="application/json")

            return wrapper

        return decorator


_default = Komodoro()
populate = _default.populate
