import collections.abc
import typing
import urllib.parse

from ...association import Association
from ...http import RobotoClient
from .operations import (
    AddMessagePathRepresentationRequest,
    AddMessagePathRequest,
    CreateTopicRequest,
    SetDefaultRepresentationRequest,
    UpdateMessagePathRequest,
    UpdateTopicRequest,
)
from .record import (
    MessagePathRecord,
    RepresentationRecord,
    TopicRecord,
)


class Topic:
    __record: TopicRecord
    __roboto_client: RobotoClient

    @classmethod
    def create(
        cls,
        request: CreateTopicRequest,
        caller_org_id: typing.Optional[str] = None,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> "Topic":
        roboto_client = RobotoClient.defaulted(roboto_client)
        response = roboto_client.post(
            "v1/topics",
            data=request,
            caller_org_id=caller_org_id,
        )
        record = response.to_record(TopicRecord)
        return cls(record, roboto_client)

    @classmethod
    def from_name_and_association(
        cls,
        topic_name: str,
        association: Association,
        owner_org_id: typing.Optional[str] = None,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> "Topic":
        roboto_client = RobotoClient.defaulted(roboto_client)
        quoted_topic_name = urllib.parse.quote_plus(topic_name)
        encoded_association = association.url_encode()

        response = roboto_client.get(
            f"v1/topics/association/{encoded_association}/name/{quoted_topic_name}",
            owner_org_id=owner_org_id,
        )
        record = response.to_record(TopicRecord)
        return cls(record, roboto_client)

    @classmethod
    def get_by_association(
        cls,
        association: Association,
        owner_org_id: typing.Optional[str] = None,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> collections.abc.Generator["Topic", None, None]:
        roboto_client = RobotoClient.defaulted(roboto_client)
        encoded_association = association.url_encode()

        page_token: typing.Optional[str] = None
        while True:
            response = roboto_client.get(
                f"v1/topics/association/{encoded_association}",
                owner_org_id=owner_org_id,
                query={"page_token": page_token} if page_token else None,
            )
            paginated_results = response.from_paginated_list(TopicRecord)
            for topic_record in paginated_results.items:
                yield cls(topic_record, roboto_client)
            if paginated_results.next_token:
                page_token = paginated_results.next_token
            else:
                break

    def __init__(
        self,
        record: TopicRecord,
        roboto_client: typing.Optional[RobotoClient] = None,
    ):
        self.__record = record
        self.__roboto_client = RobotoClient.defaulted(roboto_client)

    def __repr__(self) -> str:
        return self.__record.model_dump_json()

    @property
    def association(self) -> Association:
        return self.__record.association

    @property
    def default_representation(self) -> typing.Optional[RepresentationRecord]:
        return self.__record.default_representation

    @property
    def message_paths(self) -> collections.abc.Sequence[MessagePathRecord]:
        return self.__record.message_paths

    @property
    def name(self) -> str:
        return self.__record.topic_name

    @property
    def org_id(self) -> str:
        return self.__record.org_id

    @property
    def record(self) -> TopicRecord:
        return self.__record

    @property
    def url_quoted_name(self) -> str:
        return urllib.parse.quote_plus(self.name)

    def add_message_path(self, request: AddMessagePathRequest) -> MessagePathRecord:
        encoded_association = self.association.url_encode()
        response = self.__roboto_client.post(
            f"v1/topics/association/{encoded_association}/name/{self.url_quoted_name}/message-path",
            data=request,
            owner_org_id=self.org_id,
        )
        message_path_record = response.to_record(MessagePathRecord)
        self.__refresh()
        return message_path_record

    def add_message_path_representation(
        self,
        request: AddMessagePathRepresentationRequest,
    ) -> RepresentationRecord:
        encoded_association = self.association.url_encode()
        response = self.__roboto_client.post(
            f"v1/topics/association/{encoded_association}/name/{self.url_quoted_name}/message-path/representation",
            data=request,
            owner_org_id=self.org_id,
        )
        representation_record = response.to_record(RepresentationRecord)
        self.__refresh()
        return representation_record

    def delete(self) -> None:
        encoded_association = self.association.url_encode()
        self.__roboto_client.delete(
            f"v1/topics/association/{encoded_association}/name/{self.url_quoted_name}",
            owner_org_id=self.org_id,
        )

    def set_default_representation(
        self, request: SetDefaultRepresentationRequest
    ) -> RepresentationRecord:
        encoded_association = self.association.url_encode()
        response = self.__roboto_client.post(
            f"v1/topics/association/{encoded_association}/name/{self.url_quoted_name}/representation",
            data=request,
            owner_org_id=self.org_id,
        )
        representation_record = response.to_record(RepresentationRecord)
        self.__refresh()
        return representation_record

    def update(self, request: UpdateTopicRequest) -> "Topic":
        encoded_association = self.association.url_encode()
        response = self.__roboto_client.put(
            f"v1/topics/association/{encoded_association}/name/{self.url_quoted_name}",
            data=request,
            owner_org_id=self.org_id,
        )
        record = response.to_record(TopicRecord)
        self.__record = record
        return self

    def update_message_path(
        self, request: UpdateMessagePathRequest
    ) -> MessagePathRecord:
        encoded_association = self.association.url_encode()
        response = self.__roboto_client.put(
            f"v1/topics/association/{encoded_association}/name/{self.url_quoted_name}/message-path",
            data=request,
            owner_org_id=self.org_id,
        )
        message_path_record = response.to_record(MessagePathRecord)
        self.__refresh()
        return message_path_record

    def __refresh(self) -> None:
        topic = Topic.from_name_and_association(
            topic_name=self.name,
            association=self.association,
            owner_org_id=self.org_id,
            roboto_client=self.__roboto_client,
        )
        self.__record = topic.record
