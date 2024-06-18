from os import getenv
from typing import Any, Iterator, get_args

from datek_app_utils.env_config.bool_type import _Bool
from datek_app_utils.env_config.errors import InstantiationForbiddenError


class Variable:
    def __init__(self, type_: type = str, default_value=...):
        type_args = get_args(type_)
        type_ = type_args[0] if type_args else type_
        self._type = _Bool if type_ is bool else type_
        self._default_value = default_value

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, type_=None):
        return self.value

    @property
    def default_value(self) -> Any:
        return self._default_value

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def value(self) -> Any:
        if (value := getenv(self._name)) is not None:
            casted_val = self._type(value)
            return bool(casted_val) if self._type is _Bool else casted_val

        if self._default_value is not ...:
            return self._default_value


class ConfigMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        for key, type_ in namespace.get("__annotations__", {}).items():
            namespace[key] = Variable(type_, namespace.get(key, ...))

        for base in bases:
            if not isinstance(base, ConfigMeta):
                continue

            for variable in base:
                namespace[variable.name] = variable

        return super().__new__(mcs, name, bases, namespace)

    def __iter__(cls) -> Iterator[Variable]:
        return (value for value in cls.__dict__.values() if isinstance(value, Variable))


class BaseConfig(metaclass=ConfigMeta):
    def __new__(cls, *args, **kwargs):
        raise InstantiationForbiddenError
