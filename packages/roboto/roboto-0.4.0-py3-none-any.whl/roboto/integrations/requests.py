import typing

import pydantic


class RegisterS3IntegrationRequest(pydantic.BaseModel):
    account_id: str
    bucket_name: str
    org_id: str


class RegisterS3IntegrationResponse(pydantic.BaseModel):
    iam_role_name: str
    iam_role_policy: dict[str, typing.Any]
    iam_role_trust_relationship: dict[str, typing.Any]
    s3_bucket_cors_policy: list[dict[str, typing.Any]]
