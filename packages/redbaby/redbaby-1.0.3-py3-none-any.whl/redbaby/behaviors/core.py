import logging
from typing import Any, Optional

from pydantic import BaseModel
from pymongo import IndexModel
from pymongo.collection import Collection

from ..database import DB


class BaseDocument(BaseModel):

    def bson(self) -> dict[str, Any]:
        obj = self.model_dump(by_alias=True, mode="python")
        return obj

    @classmethod
    def collection_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def collection(
        cls,
        db_name: Optional[str] = None,
        suffix: Optional[str] = None,
        alias: str = "default",
    ) -> Collection:
        return DB.get(db_name, suffix, alias)[cls.collection_name()]

    @classmethod
    def indexes(cls) -> list[IndexModel]:
        return []

    @classmethod
    def create_indexes(cls, alias: str = "default"):
        idx = cls.indexes()
        if not idx:
            logging.warning(f"No indexes for '{cls.collection_name()}'.")
            return
        cls.collection(alias=alias).create_indexes(idx)
