from enum import Enum


class EnumHandler(Enum):
    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def keys(cls):
        return cls._member_names_

    @classmethod
    def values(cls):
        return list(cls._value2member_map_.keys())

    @classmethod
    def items(cls):
        return list(cls)
