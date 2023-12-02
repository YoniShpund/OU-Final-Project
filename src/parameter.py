from enum import Enum


class ParameterType(Enum):
    LOCAL_PARAM = 1
    LOCAL_CONST = 2
    KEYWORD = 3


class Parameter():
    def __init__(self, name: str, type: ParameterType) -> None:
        self._name = name
        self._type = type

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def __str__(self) -> str:
        return f"{__name__} {self.name} - {self.type}"
