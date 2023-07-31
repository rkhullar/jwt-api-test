from pydantic import BaseModel
from typing import Literal


class PublicKey(BaseModel):
    kty: Literal['RSA']
    e: str
    kid: str
    n: str


class PrivateKey(PublicKey):
    d: str
    p: str
    q: str
    dp: str
    dq: str
    qi: str
    pem: str

    @property
    def public_key(self) -> PublicKey:
        return PublicKey(kty=self.kty, e=self.e, kid=self.kid, n=self.n)
