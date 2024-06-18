import json
import logging
import pathlib
from typing import Optional

import pydantic

logger = logging.getLogger()


class RobotoFeatureFlags(pydantic.BaseModel):
    # Place additional flags here as needed
    placeholder_flag: Optional[bool] = True


def get_flags_config(
    roboto_config_dir: Optional[pathlib.Path] = None,
) -> RobotoFeatureFlags:
    if roboto_config_dir is None:
        roboto_config_dir = pathlib.Path.home() / ".roboto"

    config_file = roboto_config_dir / "feature_flags.json"

    if not config_file.is_file():
        return RobotoFeatureFlags()

    try:
        with open(config_file, "r") as f:
            contents = json.loads(f.read())
            return RobotoFeatureFlags(**contents)
    except (json.decoder.JSONDecodeError, pydantic.ValidationError) as e:
        logger.warning("Malformed feature flags file, ignoring: %s", str(e))
        return RobotoFeatureFlags()
