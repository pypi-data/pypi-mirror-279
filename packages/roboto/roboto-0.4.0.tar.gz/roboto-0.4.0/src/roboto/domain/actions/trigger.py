import collections.abc
import datetime
import typing

from ...exceptions import RobotoConflictException
from ...http import RobotoClient
from ...query import (
    ConditionType,
    QuerySpecification,
)
from .action import Action
from .invocation import Invocation
from .invocation_operations import (
    CreateInvocationRequest,
)
from .invocation_record import (
    InvocationDataSource,
    InvocationSource,
)
from .trigger_operations import (
    CreateTriggerRequest,
    UpdateTriggerRequest,
)
from .trigger_record import (
    TriggerForEachPrimitive,
    TriggerRecord,
)


class Trigger:
    __record: TriggerRecord
    __roboto_client: RobotoClient

    @classmethod
    def create(
        cls,
        request: CreateTriggerRequest,
        caller_org_id: typing.Optional[str] = None,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> "Trigger":
        """
        Invoke an action on every new dataset (or every new dataset file) that meets some acceptance criteria.
        """
        roboto_client = RobotoClient.defaulted(roboto_client)
        response = roboto_client.post(
            "v1/triggers",
            data=request,
            caller_org_id=caller_org_id,
        )
        record = response.to_record(TriggerRecord)
        return cls(record, roboto_client)

    @classmethod
    def from_name(
        cls,
        name: str,
        owner_org_id: typing.Optional[str] = None,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> "Trigger":
        roboto_client = RobotoClient.defaulted(roboto_client)
        response = roboto_client.get(
            f"v1/triggers/{name}",
            owner_org_id=owner_org_id,
        )
        record = response.to_record(TriggerRecord)
        return cls(record, roboto_client)

    @classmethod
    def query(
        cls,
        spec: typing.Optional[QuerySpecification] = None,
        owner_org_id: typing.Optional[str] = None,
        roboto_client: typing.Optional[RobotoClient] = None,
    ) -> collections.abc.Generator["Trigger", None, None]:
        roboto_client = RobotoClient.defaulted(roboto_client)
        spec = spec or QuerySpecification()

        while True:
            response = roboto_client.post(
                "v1/triggers/query",
                data=spec,
                owner_org_id=owner_org_id,
                idempotent=True,
            )
            paginated_results = response.from_paginated_list(TriggerRecord)
            for record in paginated_results.items:
                yield cls(record, roboto_client)
            if paginated_results.next_token:
                spec.after = paginated_results.next_token
            else:
                break

    def __init__(
        self,
        record: TriggerRecord,
        roboto_client: typing.Optional[RobotoClient] = None,
    ):
        self.__record = record
        self.__roboto_client = RobotoClient.defaulted(roboto_client)

    def __repr__(self) -> str:
        return self.__record.model_dump_json()

    @property
    def condition(self) -> typing.Optional[ConditionType]:
        return self.__record.condition

    @property
    def created(self) -> datetime.datetime:
        return self.__record.created

    @property
    def created_by(self) -> str:
        return self.__record.created_by

    @property
    def enabled(self) -> bool:
        return self.__record.enabled

    @property
    def for_each(self) -> TriggerForEachPrimitive:
        return self.__record.for_each

    @property
    def name(self):
        return self.__record.name

    @property
    def modified(self) -> datetime.datetime:
        return self.__record.modified

    @property
    def modified_by(self) -> str:
        return self.__record.modified_by

    @property
    def org_id(self):
        return self.__record.org_id

    @property
    def record(self) -> TriggerRecord:
        return self.__record

    @property
    def service_user_id(self) -> typing.Optional[str]:
        return self.__record.service_user_id

    def delete(self):
        self.__roboto_client.delete(
            f"v1/triggers/{self.name}",
            owner_org_id=self.org_id,
        )

    def get_action(self) -> Action:
        return Action.from_name(
            self.__record.action.name,
            digest=self.__record.action.digest,
            owner_org_id=self.__record.action.owner,
            roboto_client=self.__roboto_client,
        )

    def invoke(
        self,
        data_source: InvocationDataSource,
        idempotency_id: typing.Optional[str] = None,
        input_data_override: typing.Optional[list[str]] = None,
    ) -> typing.Optional[Invocation]:
        create_invocation_request = CreateInvocationRequest(
            compute_requirement_overrides=self.__record.compute_requirement_overrides,
            container_parameter_overrides=self.__record.container_parameter_overrides,
            data_source_id=data_source.data_source_id,
            data_source_type=data_source.data_source_type,
            input_data=input_data_override or self.__record.required_inputs,
            idempotency_id=idempotency_id,
            invocation_source=InvocationSource.Trigger,
            invocation_source_id=self.__record.name,
            parameter_values=self.__record.parameter_values,
            timeout=self.__record.timeout,
        )
        try:
            return self.get_action().invoke(
                request=create_invocation_request,
                caller_org_id=self.__record.org_id,
            )
        except RobotoConflictException:
            # Return None if there was an existing invocation with the same idempotency ID
            return None

    def to_dict(self) -> dict[str, typing.Any]:
        return self.__record.model_dump(mode="json")

    def update(
        self,
        request: UpdateTriggerRequest,
    ) -> "Trigger":
        response = self.__roboto_client.put(
            f"v1/triggers/{self.name}",
            data=request,
            owner_org_id=self.org_id,
        )
        record = response.to_record(TriggerRecord)
        self.__record = record
        return self
