import typing

import pydantic


class CreateTokenRequest(pydantic.BaseModel):
    expiry_days: int = pydantic.Field(
        description="Number of days until the token expires"
    )
    name: str = pydantic.Field(description="A human-readable name for this token.")
    description: typing.Optional[str] = pydantic.Field(
        default=None, description="An optional longer description for this token."
    )
