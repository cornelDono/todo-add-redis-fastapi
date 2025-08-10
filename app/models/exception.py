from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return 'Application Error occurred'


@dataclass(frozen=True, eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return f'Text is empty'