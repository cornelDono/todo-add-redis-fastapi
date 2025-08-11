from enum import StrEnum


class ToDoStatus(StrEnum):
    ToDo = "To Do"
    InProgress = "In Progress"
    Done = "Done"


class NameSpace(StrEnum):
    Name = "namespace"