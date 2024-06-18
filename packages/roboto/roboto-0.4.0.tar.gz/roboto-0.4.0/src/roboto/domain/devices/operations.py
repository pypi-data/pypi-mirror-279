import typing

import pydantic


class CreateDeviceRequest(pydantic.BaseModel):
    device_id: str = pydantic.Field(
        description="A user-provided identifier for a device, which is unique within that device's org."
    )
    org_id: typing.Optional[str] = pydantic.Field(
        description="The org to which this device belongs.", default=None
    )
