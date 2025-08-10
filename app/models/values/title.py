from models.exception import EmptyTextException
from models.values.base import BaseValueObject


class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()