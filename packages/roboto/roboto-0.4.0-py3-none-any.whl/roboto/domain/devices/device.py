import collections.abc
import typing

from ...exceptions import (
    RobotoNotImplementedException,
)
from ...http import RobotoClient
from ..tokens import Token
from .operations import CreateDeviceRequest
from .record import DeviceRecord


class Device:
    """
    A device is a non-human entity which can interact with Roboto on behalf of a specific organization.
    Each device is identified by a device_id, which is unique among all devices in the organization to which it belongs.

    The most typical device is a robot which uploads its log data to Roboto, either directly from its on-board software
    stack, or indirectly through an automatic upload station or human-in-the-loop upload process. Its device ID
    may be a string that represents its serial number in a scheme native to its organization.

    A dedicated uploader station which connects to many different robots and uploads data on their behalf could also
    be modeled as a device.

    API access tokens can be allocated for devices, and these tokens can be used to authenticate Roboto requests made
    on behalf of a device.
    """

    __roboto_client: RobotoClient
    __record: DeviceRecord

    # Class methods + Constructor

    @classmethod
    def create(
        cls,
        request: CreateDeviceRequest,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> "Device":
        """
        Registers a device with Roboto.

        Args:
            request: User-specified fields for the to-be-created device record
            roboto_client: Common parameters required to construct any Device object

        Returns:
            A Device object representing the newly-created device
        """
        roboto_client = RobotoClient.defaulted(roboto_client)
        record = roboto_client.post(
            "v1/devices/create", caller_org_id=request.org_id, data=request
        ).to_record(DeviceRecord)
        return cls(record=record, roboto_client=roboto_client)

    @classmethod
    def for_org(
        cls, org_id: str, roboto_client: typing.Optional[RobotoClient] = None
    ) -> collections.abc.Generator["Device", None, None]:
        """
        List all devices registered for a given org.

        Args:
            org_id: The org to list devices for
            roboto_client: Common parameters required to construct any Device object

        Returns:
            A generator of Device objects. For orgs with a large number of devices, this may involve multiple service
            calls, and the generator will yield results as they become available.
        """
        roboto_client = RobotoClient.defaulted(roboto_client)

        next_token: typing.Optional[str] = None
        while True:
            query_params: dict[str, typing.Any] = {}
            if next_token:
                query_params["page_token"] = str(next_token)

            results = roboto_client.get(
                f"v1/devices/org/{org_id}",
                query=query_params,
            ).from_paginated_list(DeviceRecord)

            for item in results.items:
                yield cls(record=item, roboto_client=roboto_client)

            next_token = results.next_token
            if not next_token:
                break

    @classmethod
    def from_id(
        cls,
        device_id: str,
        roboto_client: typing.Optional[RobotoClient] = None,
        org_id: typing.Optional[str] = None,
    ) -> "Device":
        """
        Args:
            device_id: The device ID to look up. See :func:`Device.device_id` for more details.
            roboto_client: Common parameters required to construct any Device object
            org_id: The org to which the device belongs.
                If not specified by a caller who only belongs to one org, will default to the org_id of that org.
                If not specified by a caller who belongs to multiple orgs, will raise an exception.

        Returns:
            A Device object representing the specified device

        Raises:
            RobotoNotFoundException: If the specified device is not registered with Roboto
        """
        roboto_client = RobotoClient.defaulted(roboto_client)
        record = roboto_client.get(
            f"v1/devices/id/{device_id}",
            owner_org_id=org_id,
        ).to_record(DeviceRecord)
        return cls(record=record, roboto_client=roboto_client)

    def __init__(
        self, record: DeviceRecord, roboto_client: typing.Optional[RobotoClient] = None
    ):
        self.__roboto_client = RobotoClient.defaulted(roboto_client)
        self.__record = record

    def __repr__(self) -> str:
        return self.__record.model_dump_json()

    @property
    def device_id(self) -> str:
        """
        This device's ID. Device ID is a user-provided identifier for a device, which is unique within the
        device's org.
        """
        return self.__record.device_id

    @property
    def org_id(self) -> str:
        """
        The ID of the org to which this device belongs.
        """
        return self.__record.org_id

    @property
    def record(self) -> DeviceRecord:
        """
        The underlying DeviceRecord object which represents this device. This is often used as the wire representation
        of a device during API requests, and is subject to evolve over time. You should not program against this
        if avoidable.
        """
        return self.__record

    def create_token(self) -> Token:
        """
        Stub API - Not Yet Implemented

        Raises:
            RobotoNotImplementedException: Always, because it's not implemented
        """
        raise RobotoNotImplementedException("Cannot create tokens for device.")

    def delete(self) -> None:
        """
        Deletes this device.
        """
        self.__roboto_client.delete(
            f"v1/devices/id/{self.device_id}", owner_org_id=self.org_id
        )

    def tokens(self) -> collections.abc.Generator[Token, None, None]:
        """
        Stub API - Not Yet Implemented

        Raises:
            RobotoNotImplementedException: Always, because it's not implemented
        """
        raise RobotoNotImplementedException("Cannot get tokens for device.")
