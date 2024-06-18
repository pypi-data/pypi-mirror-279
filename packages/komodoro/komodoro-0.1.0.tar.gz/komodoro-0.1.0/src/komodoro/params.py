from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar
from typing_extensions import Annotated


@dataclass
class Field:
    type_: type[Any]
    name: str


class Param: ...


class PathParam(Param): ...


class QueryParam(Param): ...


class HeaderParam(Param): ...


AnyType = TypeVar("AnyType")
if TYPE_CHECKING:
    Body = Annotated[AnyType, ...]
else:

    class Body:
        def __class_getitem__(cls, item: AnyType) -> AnyType:
            return Annotated[item, cls()]


T = TypeVar("T")
Path = Annotated[T, PathParam()]
Query = Annotated[T, QueryParam()]
Header = Annotated[T, HeaderParam()]

Body[int]
