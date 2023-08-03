from pydantic import BaseModel

from ..model.key import PublicKey


class PublicKeyForClient(PublicKey):
    # used in okta oauth jwks uri
    alg: str = 'RS256'
    use: str = 'sig'


class PublicKeysResponse(BaseModel):
    keys: list[PublicKeyForClient]
