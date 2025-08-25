from typing import Optional

from pydantic import BaseModel


class CreateNameSpaceRequestSchema(BaseModel):
    name: str


class CreateNameSpaceResponseSchema(BaseModel):
    name: str
    message: Optional[str] = "Successfully created NameSpace"


class DeleteNameSpaceRequestSchema(BaseModel):
    name: str


class DeleteNameSpaceResponseSchema(BaseModel):
    is_deleted: bool
    message: Optional[str] = "Successfully deleted NameSpace"