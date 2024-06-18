#  Copyright (c) 2023 Roboto Technologies, Inc.

import datetime
import enum
import typing

import pydantic

from ..users import UserRecord


class OrgStatus(str, enum.Enum):
    Provisioning = "provisioning"
    Active = "active"
    Deprovisioning = "de-provisioning"


class OrgTier(str, enum.Enum):
    free = "free"
    premium = "premium"


class OrgRecord(pydantic.BaseModel):
    org_id: str
    name: str
    tier: OrgTier
    status: OrgStatus
    created: datetime.datetime
    created_by: typing.Optional[str] = None


class OrgRoleName(str, enum.Enum):
    user = "user"
    admin = "admin"
    owner = "owner"


class OrgUserRecord(pydantic.BaseModel):
    user: UserRecord
    org: OrgRecord
    roles: list[OrgRoleName]


class OrgInviteRecord(pydantic.BaseModel):
    invite_id: str
    user_id: str
    invited_by: UserRecord
    org: OrgRecord
