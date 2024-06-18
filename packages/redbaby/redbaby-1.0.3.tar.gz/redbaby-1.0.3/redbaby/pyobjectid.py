from typing import Any

from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # left to right evaluation on the schemas below
        from_json_validation = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]
        )
        from_python_validation = core_schema.union_schema(
            [core_schema.is_instance_schema(ObjectId), from_json_validation]
        )
        # we only want to stringify the ObjectId when serializing to json
        serializer = core_schema.plain_serializer_function_ser_schema(
            str, when_used="json"
        )
        pydantic_core_schema = core_schema.json_or_python_schema(
            json_schema=from_json_validation,
            python_schema=from_python_validation,
            serialization=serializer,
        )
        return pydantic_core_schema

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError(f"'{value}' is not a valid bson.ObjectId.")

        return ObjectId(value)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())
