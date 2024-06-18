import collections.abc
import http
import http.client
import json
import random
import typing
import urllib.error
import urllib.parse
import urllib.request
import urllib.response

import pydantic
import tenacity.wait

from ..serde import safe_dict_drill
from .response import PaginatedList

RetryWaitFn = typing.Callable[
    [tenacity.RetryCallState, typing.Optional[BaseException]], float
]

T = typing.TypeVar("T", bound=pydantic.BaseModel)


class HttpResponse:
    __response: urllib.response.addinfourl

    def __init__(self, response: urllib.response.addinfourl) -> None:
        super().__init__()
        self.__response = response

    @property
    def readable_response(self) -> urllib.response.addinfourl:
        return self.__response

    @property
    def status(self) -> http.HTTPStatus:
        status_code = self.__response.status
        if status_code is None:
            raise RuntimeError("Response has no status code")
        return http.HTTPStatus(int(status_code))

    @property
    def headers(self) -> typing.Optional[dict[str, str]]:
        return dict(self.__response.headers.items())

    def from_paginated_list(self, record_type: typing.Type[T]) -> PaginatedList[T]:
        unmarshalled = self.from_json(json_path=["data"])
        return PaginatedList(
            items=[record_type.model_validate(item) for item in unmarshalled["items"]],
            next_token=unmarshalled["next_token"],
        )

    def to_record(self, record_type: typing.Type[T]) -> T:
        return record_type.model_validate(self.from_json(json_path=["data"]))

    def to_record_list(
        self, record_type: typing.Type[T]
    ) -> collections.abc.Sequence[T]:
        return [
            record_type.model_validate(item)
            for item in self.from_json(json_path=["data"])
        ]

    def from_json(self, json_path: typing.Optional[list[str]] = None) -> typing.Any:
        with self.__response:
            unmarsalled = json.loads(self.__response.read().decode("utf-8"))
            if json_path is None:
                return unmarsalled

            return safe_dict_drill(unmarsalled, json_path)

    def from_string(self):
        with self.__response:
            return self.__response.read().decode("utf-8")


def default_retry_wait_ms(
    retry_state: tenacity.RetryCallState, _exc: typing.Optional[BaseException]
) -> float:
    """
    Returns sleep time in ms using exponential backoff with full jitter, as described in:
    https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    """
    base = 500
    cap = 30_000

    exponential_wait = min(cap, pow(2, retry_state.attempt_number) * base)
    jittered = random.uniform(0, exponential_wait)
    return jittered


class HttpRequest:
    url: str
    method: str
    headers: dict
    retry_wait: RetryWaitFn
    data: typing.Any = None
    idempotent: bool = False

    def __init__(
        self,
        url: str,
        method: str = "GET",
        headers: typing.Optional[dict[str, str]] = None,
        data: typing.Any = None,
        retry_wait: typing.Optional[RetryWaitFn] = None,
        idempotent: bool = False,
    ):
        self.url = url
        self.method = method
        self.headers = headers if headers is not None else {}
        self.data = data
        self.retry_wait = (
            retry_wait if retry_wait is not None else default_retry_wait_ms
        )
        self.idempotent = idempotent

        if isinstance(self.data, pydantic.BaseModel) or isinstance(self.data, dict):
            self.headers["Content-Type"] = "application/json"

    def __repr__(self) -> str:
        return (
            f"HttpRequest("
            f"url={self.url}, "
            f"method={self.method}, "
            f"headers={self.headers}, "
            f"data={self.data}, "
            f"idempotent={self.idempotent}"
            ")"
        )

    @property
    def body(self) -> typing.Optional[bytes]:
        if self.data is None:
            return None

        if isinstance(self.data, bytes):
            return self.data

        if isinstance(self.data, str):
            return self.data.encode("utf-8")

        if isinstance(self.data, pydantic.BaseModel):
            return self.data.model_dump_json(exclude_unset=True).encode("utf-8")

        return json.dumps(self.data).encode("utf-8")

    @property
    def hostname(self) -> str:
        parsed_url = urllib.parse.urlparse(self.url)
        return (
            parsed_url.hostname
            if parsed_url.hostname is not None
            else parsed_url.netloc
        )

    def append_headers(self, headers: dict[str, str]) -> None:
        self.headers.update(headers)


HttpRequestDecorator = typing.Callable[[HttpRequest], HttpRequest]
