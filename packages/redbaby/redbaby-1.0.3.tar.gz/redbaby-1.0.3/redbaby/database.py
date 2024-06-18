from typing import Optional, TypedDict

from pymongo import MongoClient
from pymongo.database import Database


class MongoConnection(TypedDict):
    db_name: str
    uri: str


class DB:
    connections: dict[str, MongoConnection] = {}
    clients: dict[str, MongoClient] = {}

    @classmethod
    def get(
        cls,
        db_name: Optional[str] = None,
        suffix: Optional[str] = None,
        alias: str = "default",
    ) -> Database:
        if db_name is None:
            db_name = cls.get_conn(alias)["db_name"]
        if suffix:
            db_name = f"{db_name}-{suffix}"
        return cls.get_client(alias)[db_name]

    @classmethod
    def get_client(cls, alias: str = "default") -> MongoClient:
        return cls.clients[alias]

    @classmethod
    def add_client(cls, alias: str = "default") -> MongoClient:
        cls.clients[alias] = MongoClient(host=cls.get_conn(alias)["uri"], fsync=True)

    @classmethod
    def get_conn(cls, alias: str = "default") -> MongoConnection:
        return cls.connections[alias]

    @classmethod
    def add_conn(
        cls,
        db_name: str,
        uri: str,
        alias: str = "default",
        start_client: bool = True,
    ):
        cls.connections[alias] = MongoConnection(db_name=db_name, uri=uri)
        if start_client:
            cls.add_client(alias)


DB.add_conn(
    db_name="redbaby",
    uri="mongodb://localhost:27017",
    start_client=False,
)
