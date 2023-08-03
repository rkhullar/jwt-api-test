from pydantic import BaseModel, model_validator


class DiscoveryMetadata(BaseModel):
    issuer: str
    jwks_uri: str


class SignMetadata(BaseModel):
    duration: int | None = None
    expiration: int | None = None
    issued_at: int | None = None
    audience: str = 'api://default'

    @model_validator(mode='after')
    def check_timestamps(self):
        iat, exp, dur = map(bool, [self.issued_at, self.expiration, self.duration])
        if not (dur or exp):
            self.duration, dur = 5, True

        if not dur ^ exp:
            raise ValueError('duration and expiration are mutually exclusive')


class SignData(BaseModel):
    data: dict
    metadata: SignMetadata = SignMetadata(duration=3600)


if __name__ == '__main__':
    payload = {
        'data': {},
        'metadata': {}
    }
    request = SignData.model_validate(payload)
    print(request)
