import enum
import typing

import pydantic
import pydantic_settings

ROBOTO_ENV_VAR_PREFIX = "ROBOTO_"


class RobotoEnvKey(str, enum.Enum):
    ActionParametersFile = f"{ROBOTO_ENV_VAR_PREFIX}ACTION_PARAMETERS_FILE"
    ActionTimeout = f"{ROBOTO_ENV_VAR_PREFIX}ACTION_TIMEOUT"
    BearerToken = f"{ROBOTO_ENV_VAR_PREFIX}BEARER_TOKEN"
    DatasetMetadataChangesetFile = (
        f"{ROBOTO_ENV_VAR_PREFIX}DATASET_METADATA_CHANGESET_FILE"
    )
    DatasetId = f"{ROBOTO_ENV_VAR_PREFIX}DATASET_ID"
    FileMetadataChangesetFile = f"{ROBOTO_ENV_VAR_PREFIX}FILE_METADATA_CHANGESET_FILE"
    InputDir = f"{ROBOTO_ENV_VAR_PREFIX}INPUT_DIR"
    InvocationId = f"{ROBOTO_ENV_VAR_PREFIX}INVOCATION_ID"
    OrgId = f"{ROBOTO_ENV_VAR_PREFIX}ORG_ID"
    OutputDir = f"{ROBOTO_ENV_VAR_PREFIX}OUTPUT_DIR"
    RobotoEnv = f"{ROBOTO_ENV_VAR_PREFIX}ENV"
    RobotoServiceUrl = f"{ROBOTO_ENV_VAR_PREFIX}SERVICE_URL"
    """Deprecated, use RobotoServiceEndpoint instead. Left here until 0.3.3 is released so we can migrate
    existing actions to use the new env var."""
    RobotoServiceEndpoint = f"{ROBOTO_ENV_VAR_PREFIX}SERVICE_ENDPOINT"

    @staticmethod
    def for_parameter(param_name: str) -> str:
        return f"{ROBOTO_ENV_VAR_PREFIX}PARAM_{param_name}"


# You'll notice that the alias values here are duplicates of the RobotoEnvKey values. This is not ideal, but is
# necessary for type checking, because the value of alias needs to be a string literal and not a de-referenced variable.
# Even using f-strings will break the type checking.
class RobotoEnv(pydantic_settings.BaseSettings):
    action_parameters_file: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_ACTION_PARAMETERS_FILE"
    )

    action_timeout: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_ACTION_TIMEOUT"
    )

    bearer_token: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_BEARER_TOKEN"
    )

    dataset_id: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_DATASET_ID"
    )

    dataset_metadata_changeset_file: typing.Optional[str] = pydantic.Field(
        default=None,
        alias="ROBOTO_DATASET_METADATA_CHANGESET_FILE",
    )

    file_metadata_changeset_file: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_FILE_METADATA_CHANGESET_FILE"
    )

    input_dir: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_INPUT_DIR"
    )

    invocation_id: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_INVOCATION_ID"
    )

    org_id: typing.Optional[str] = pydantic.Field(default=None, alias="ROBOTO_ORG_ID")

    output_dir: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_OUTPUT_DIR"
    )

    roboto_env: typing.Optional[str] = pydantic.Field(default=None, alias="ROBOTO_ENV")

    roboto_service_url: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_SERVICE_URL"
    )
    """Deprecated, use roboto_service_endpoint instead. Left here until 0.3.3 is released so we can migrate
    existing actions to use the new env var."""

    roboto_service_endpoint: typing.Optional[str] = pydantic.Field(
        default=None, alias="ROBOTO_SERVICE_ENDPOINT"
    )
    """A Roboto Service API endpoint to send requests to, typically https://api.roboto.ai"""


default_env = RobotoEnv()
