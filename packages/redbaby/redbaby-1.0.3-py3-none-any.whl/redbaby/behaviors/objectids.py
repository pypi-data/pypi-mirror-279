from pydantic import BaseModel, Field

from ..pyobjectid import PyObjectId


class ObjectIdMixin(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
