from typing import Optional

from pydantic import BaseModel


class CreateNameSpaceRequestSchema(BaseModel):
    name: str


class CreateNameSpaceResponseSchema(BaseModel):
    name: str
    message: Optional[str] = "Successfully created NameSpace"