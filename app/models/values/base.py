from typing import TypeVar, Any, Generic

from pydantic import BaseModel, model_validator

VT = TypeVar("VT", bound=Any)


class BaseValueObject(BaseModel, Generic[VT]):
    value: VT

    @classmethod
    def validate(cls):
        ...

    @model_validator(mode='after')
    def validate_value(self) -> None:
        self.validate()
