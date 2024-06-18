import pydantic

from .record import CommentEntityType


class CreateCommentRequest(pydantic.BaseModel):
    entity_type: CommentEntityType
    entity_id: str
    comment_text: str


class UpdateCommentRequest(pydantic.BaseModel):
    comment_text: str
