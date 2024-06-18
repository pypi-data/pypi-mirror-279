from functools import cached_property

from pydantic import BaseModel, computed_field

from ..hashing import HashDigest, get_hash
from ..utils import cat


class HashIdMixin(BaseModel):

    @computed_field(alias="_id", repr=True)
    @cached_property
    def id(self) -> HashDigest:
        return get_hash(cat(*self.hashable_fields()))

    def hashable_fields(self) -> list[str]:
        raise NotImplementedError
