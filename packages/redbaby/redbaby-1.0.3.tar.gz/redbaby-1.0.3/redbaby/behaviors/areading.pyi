from typing import Any, Iterable, Literal, Optional, Self, Sequence, overload

from .core import BaseDocument

class ReadingMixin(BaseDocument):
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]],
        skip: Optional[int],
        limit: Optional[int],
        validate: Literal[True],
        lazy: Literal[True],
        sort: Optional[Sequence[tuple[str, int]]],
        alias: str = "default",
    ) -> Iterable[Self]: ...
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]],
        skip: Optional[int],
        limit: Optional[int],
        validate: Literal[False],
        lazy: Literal[True],
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> Iterable[dict[str, Any]]: ...
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]],
        skip: Optional[int],
        limit: Optional[int],
        validate: Literal[False],
        lazy: Literal[False],
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> Sequence[dict[str, Any]]: ...
    @overload
    @classmethod
    def find(
        cls,
        filter: dict[str, Any],
        projection: Optional[dict[str, int | bool]],
        skip: Optional[int],
        limit: Optional[int],
        validate: Literal[True],
        lazy: Literal[False],
        sort: Optional[Sequence[tuple[str, int]]] = None,
        alias: str = "default",
    ) -> Sequence[Self]: ...
