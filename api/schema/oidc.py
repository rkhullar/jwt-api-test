from typing import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from pydantic.types import conint

# seconds between 1 minute and 24 hours
DurationType = conint(multiple_of=60, ge=60, le=86400)


def validate_data_to_sign(data: dict):
    reserved_claims = ['iss', 'aud', 'iat', 'exp']
    for claim in reserved_claims:
        if claim in data:
            raise ValueError(f'reserved claims not allowed: {reserved_claims}')
    return data


SigningDataPayload = Annotated[dict, AfterValidator(validate_data_to_sign)]


class DiscoveryMetadata(BaseModel):
    issuer: str
    jwks_uri: str


class SignMetadata(BaseModel):
    duration: DurationType = 3600
    audience: str = 'api://default'


class SignData(BaseModel):
    data: SigningDataPayload
    metadata: SignMetadata = SignMetadata(duration=3600)


class SignDataResponse(BaseModel):
    access_token: str


if __name__ == '__main__':
    payload = {
        'data': {},
        'metadata': {
            'duration': 15 * 60,
            'audience': 'test'
        }
    }
    request = SignData.model_validate(payload)
    # print(request)


    # test default metadata doesn't overlap
    # a = SignData(data={'t': 1})
    # b = SignData(data={'t': 2})
    # b.metadata.duration = 4
    # print(a, b)
