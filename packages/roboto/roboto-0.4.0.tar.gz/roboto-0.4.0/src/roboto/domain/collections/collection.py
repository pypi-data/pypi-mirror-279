import collections.abc
import typing
from typing import Optional

from roboto.query import QuerySpecification

from ...auth import (
    EditAccessRequest,
    GetAccessResponse,
)
from ...http import RobotoClient
from .operations import (
    CreateCollectionRequest,
    UpdateCollectionRequest,
)
from .record import (
    CollectionChangeRecord,
    CollectionContentMode,
    CollectionRecord,
)


class Collection:
    __record: CollectionRecord
    __roboto_client: RobotoClient

    @classmethod
    def from_id(
        cls,
        collection_id: str,
        version: Optional[int] = None,
        content_mode: CollectionContentMode = CollectionContentMode.Full,
        roboto_client: typing.Optional["RobotoClient"] = None,
    ) -> "Collection":
        roboto_client = RobotoClient.defaulted(roboto_client)

        query: dict[str, typing.Any] = {"content_mode": content_mode.value}

        if version is not None:
            query["version"] = version

        record = roboto_client.get(
            f"v1/collections/id/{collection_id}", query=query
        ).to_record(CollectionRecord)

        return cls(record=record, roboto_client=roboto_client)

    @classmethod
    def create(
        cls,
        request: CreateCollectionRequest,
        roboto_client: typing.Optional["RobotoClient"] = None,
        caller_org_id: Optional[str] = None,
    ) -> "Collection":
        roboto_client = RobotoClient.defaulted(roboto_client)

        record = roboto_client.post(
            "v1/collections/create", data=request, caller_org_id=caller_org_id
        ).to_record(CollectionRecord)

        return cls(record=record, roboto_client=roboto_client)

    @classmethod
    def list_all(
        cls,
        roboto_client: typing.Optional["RobotoClient"] = None,
        owner_org_id: Optional[str] = None,
        content_mode: CollectionContentMode = CollectionContentMode.SummaryOnly,
    ) -> collections.abc.Generator["Collection", None, None]:
        roboto_client = RobotoClient.defaulted(roboto_client)

        spec = QuerySpecification()
        query_params = {"content_mode": content_mode.value}

        while True:
            paginated_result = roboto_client.post(
                "v1/collections/search",
                query=query_params,
                data=spec.model_dump(mode="json"),
                owner_org_id=owner_org_id,
                idempotent=True,
            ).from_paginated_list(CollectionRecord)

            for record in paginated_result.items:
                yield cls(record=record, roboto_client=roboto_client)
            if paginated_result.next_token:
                spec.after = paginated_result.next_token
            else:
                break

    def __init__(
        self,
        record: CollectionRecord,
        roboto_client: typing.Optional["RobotoClient"] = None,
    ):
        self.__record = record
        self.__roboto_client = RobotoClient.defaulted(roboto_client)

    def __repr__(self) -> str:
        return self.__record.model_dump_json()

    @property
    def collection_id(self) -> str:
        return self.__record.collection_id

    @property
    def record(self) -> CollectionRecord:
        return self.__record

    def changes(
        self, from_version: Optional[int] = None, to_version: Optional[int] = None
    ) -> collections.abc.Generator["CollectionChangeRecord", None, None]:
        query: dict[str, typing.Any] = {}

        if from_version:
            query["from_version"] = from_version

        if to_version:
            query["to_version"] = to_version

        # Currently this only returns a single page
        paginated_results = self.__roboto_client.get(
            f"v1/collections/id/{self.collection_id}/changes", query=query
        ).from_paginated_list(CollectionChangeRecord)

        for record in paginated_results.items:
            yield record

    def delete(self):
        self.__roboto_client.delete(f"v1/collections/id/{self.collection_id}")

    def get_access(self) -> GetAccessResponse:
        return self.__roboto_client.get(
            f"v1/collections/{self.collection_id}/access"
        ).to_record(GetAccessResponse)

    def edit_access(self, edit: EditAccessRequest) -> GetAccessResponse:
        return self.__roboto_client.put(
            f"v1/collections/{self.collection_id}/access", data=edit
        ).to_record(GetAccessResponse)

    def update(self, request: UpdateCollectionRequest) -> "Collection":
        self.__record = self.__roboto_client.put(
            f"v1/collections/id/{self.collection_id}", data=request
        ).to_record(CollectionRecord)

        return self
