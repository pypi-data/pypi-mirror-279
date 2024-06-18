from typing import Annotated

from crypteia import Multibasing, Multihashing, ToBytes, compose
from pydantic import Field

get_hash = compose(ToBytes(), Multihashing("sha3-224"), Multibasing("base58btc"))

# sha3-224 is a 28-byte hash, which is 42 characters in base58btc
# the sha3-224 identifier (0x17) is 5d when encoded in base58btc
# base58btc encoding prepends a z to the string

HashDigest = Annotated[str, Field(pattern=r"z5d[1-9A-HJ-NP-Za-km-z]{39}")]
