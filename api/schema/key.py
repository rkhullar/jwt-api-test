from ..model.key import PublicKey
from pydantic import BaseModel


class PublicKeyForClient(PublicKey):
    # used in okta oauth jwks uri
    alg: str = 'RS256'
    use: str = 'sig'


class PublicKeysResponse(BaseModel):
    keys: list[PublicKeyForClient]
