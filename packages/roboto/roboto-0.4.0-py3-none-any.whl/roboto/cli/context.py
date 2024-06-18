import typing

from ..http import HttpClient, RobotoClient
from .feature_flags import RobotoFeatureFlags


class CLIContext:
    __roboto_service_base_url: typing.Optional[str]
    __http: typing.Optional[HttpClient]
    extensions: dict[str, typing.Any]
    feature_flags: RobotoFeatureFlags
    roboto_client: RobotoClient

    @property
    def roboto_service_base_url(self) -> str:
        if self.__roboto_service_base_url is None:
            raise ValueError("roboto_service_base_url is unset")

        return self.__roboto_service_base_url

    @roboto_service_base_url.setter
    def roboto_service_base_url(self, roboto_service_base_url: str) -> None:
        self.__roboto_service_base_url = roboto_service_base_url

    @property
    def http_client(self) -> HttpClient:
        # Necessary since http is lazy set after parsing args
        if self.__http is None:
            raise ValueError("Unset HTTP client!")

        return self.__http

    @http_client.setter
    def http_client(self, http: HttpClient) -> None:
        self.__http = http
