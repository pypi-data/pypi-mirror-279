from redbaby.behaviors import ObjectIdMixin, ReadingMixin


class SomeDoc(ReadingMixin, ObjectIdMixin):
    attr: int

    @classmethod
    def collection_name(cls) -> str:
        return "some_doc"


def test_find():
    # setup
    SomeDoc.collection().insert_many([{"attr": 1}, {"attr": 2}, {"attr": 3}])
    # given
    filter = {"attr": 2}
    skip = 0
    limit = 1
    validate = True
    lazy = False
    sort = [("attr", 1)]

    # when
    result = SomeDoc.find(
        filter=filter,
        skip=skip,
        limit=limit,
        validate=validate,
        lazy=lazy,
        sort=sort,
    )

    # then
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], SomeDoc)
    assert result[0].attr == 2
    # cleanup
    SomeDoc.collection().delete_many({"attr": {"$in": [1, 2, 3]}})


def test_find_project():
    # setup
    SomeDoc.collection().insert_many([{"attr": 1}, {"attr": 2}, {"attr": 3}])
    # given
    filter = {"attr": 2}
    projection = {"attr": 0}
    limit = 1
    validate = False
    lazy = False
    # when
    result = SomeDoc.find(
        filter=filter,
        projection=projection,
        limit=limit,
        validate=validate,
        lazy=lazy,
    )

    # then
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert "attr" not in result[0]
    assert "_id" in result[0]
    # cleanup
    SomeDoc.collection().delete_many({"attr": {"$in": [1, 2, 3]}})
