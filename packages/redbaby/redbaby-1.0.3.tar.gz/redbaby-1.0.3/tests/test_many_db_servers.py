from redbaby.behaviors.core import BaseDocument
from redbaby.database import DB


class MyDoc(BaseDocument):
    attr: int

    @classmethod
    def collection_name(cls) -> str:
        return "my_doc"


def test_many_db_servers():
    # given
    DB.add_conn("db2", "mongodb://localhost:27017", alias="db2")
    DB.add_conn("db3", "mongodb://localhost:27017", alias="db3")
    # when
    MyDoc.collection(alias="db2").insert_one({"attr": 2})
    MyDoc.collection(alias="db3").insert_one({"attr": 3})
    # then
    db2_res = MyDoc.collection(alias="db2").find_one()
    db3_res = MyDoc.collection(alias="db3").find_one()
    assert db2_res is not None
    assert db2_res["attr"] == 2
    assert db3_res is not None
    assert db3_res["attr"] == 3
    # cleanup
    MyDoc.collection(alias="db2").delete_one({"attr": 2})
    MyDoc.collection(alias="db3").delete_one({"attr": 3})
