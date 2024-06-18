from typing import Any

import pydantic


class CreateWorkspaceRequest(pydantic.BaseModel):
    # Config is an opaque JSON object handled by VizConfig.ts on the frontend
    config: dict[str, Any]
