from functools import partial
from typing import Any, Iterable, Literal, Optional, Self, Sequence, overload

from pymongo.cursor import CursorType

from .core import BaseDocument


class ReadingMixin(BaseDocument):
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        validate: Literal[False] = False,
        lazy: Literal[False] = False,
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> list[dict[str, Any]]: ...
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        validate: Literal[True] = False,
        lazy: Literal[True] = False,
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> Iterable[Self]: ...
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        validate: Literal[False] = False,
        lazy: Literal[True] = False,
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> Iterable[dict[str, Any]]: ...
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        validate: Literal[True] = False,
        lazy: Literal[False] = False,
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> list[Self]: ...

    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]] = None,
        skip: int = 0,
        limit: int = 0,
        validate: bool = False,
        lazy: bool = False,
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ):
        cursor_type = (
            CursorType.NON_TAILABLE if lazy or limit != 0 else CursorType.EXHAUST
        )
        col = cls.collection(alias=alias)
        cursor = col.find(
            filter=filter,
            projection=projection,
            skip=skip,
            limit=limit,
            sort=sort,
            cursor_type=cursor_type,
        )
        # TODO cache cursor when skip is not None
        validate_doc = cls.model_validate if validate else lambda x: x
        it = (validate_doc(item) for item in cursor)
        return it if lazy else list(it)
