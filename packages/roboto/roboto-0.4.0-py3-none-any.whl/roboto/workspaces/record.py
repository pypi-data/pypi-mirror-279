import datetime
from typing import Any

import pydantic


class WorkspaceRecord(pydantic.BaseModel):
    workspace_id: str
    org_id: str
    config: dict[str, Any]
    created: datetime.datetime
    created_by: str
