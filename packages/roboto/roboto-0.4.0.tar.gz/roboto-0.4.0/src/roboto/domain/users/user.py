import typing
from typing import Any, Optional

from roboto.notifications import (
    NotificationChannel,
    NotificationType,
)

from ...http import RobotoClient, roboto_headers
from .operations import (
    CreateUserRequest,
    UpdateUserRequest,
)
from .record import UserRecord


class User:
    __record: UserRecord
    __roboto_client: RobotoClient

    @classmethod
    def create(
        cls,
        request: CreateUserRequest,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> "User":
        roboto_client = RobotoClient.defaulted(roboto_client)
        record = roboto_client.post("v1/users", data=request).to_record(UserRecord)
        return cls(record, roboto_client)

    @classmethod
    def for_self(cls, roboto_client: typing.Optional[RobotoClient] = None) -> "User":
        roboto_client = RobotoClient.defaulted(roboto_client)
        record = roboto_client.get("v1/users").to_record(UserRecord)
        return cls(record=record, roboto_client=roboto_client)

    @classmethod
    def from_id(
        cls, user_id: str, roboto_client: typing.Optional[RobotoClient] = None
    ) -> "User":
        roboto_client = RobotoClient.defaulted(roboto_client)
        record = roboto_client.get(f"v1/users/id/{user_id}").to_record(UserRecord)
        return cls(record=record, roboto_client=roboto_client)

    def __init__(
        self, record: UserRecord, roboto_client: typing.Optional[RobotoClient] = None
    ):
        self.__record = record
        self.__roboto_client = RobotoClient.defaulted(roboto_client)

    def __repr__(self) -> str:
        return self.__record.model_dump_json()

    @property
    def user_id(self) -> str:
        return self.__record.user_id

    @property
    def name(self) -> Optional[str]:
        return self.__record.name

    @property
    def record(self) -> UserRecord:
        return self.__record

    def delete(self) -> None:
        self.__roboto_client.delete(
            "v1/users", headers=roboto_headers(user_id=self.user_id)
        )

    def to_dict(self) -> dict[str, Any]:
        return self.__record.model_dump(mode="json")

    def update(
        self,
        name: Optional[str] = None,
        picture_url: Optional[str] = None,
        notification_channels_enabled: Optional[dict[NotificationChannel, bool]] = None,
        notification_types_enabled: Optional[dict[NotificationType, bool]] = None,
    ) -> "User":
        request = UpdateUserRequest(
            name=name,
            picture_url=picture_url,
            notification_channels_enabled=notification_channels_enabled,
            notification_types_enabled=notification_types_enabled,
        )
        self.__record = self.__roboto_client.put(
            "v1/users", headers=roboto_headers(user_id=self.user_id), data=request
        ).to_record(UserRecord)
        return self
