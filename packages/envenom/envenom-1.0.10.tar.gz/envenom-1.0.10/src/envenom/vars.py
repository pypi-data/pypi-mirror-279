# `envenom` - an elegant application configurator for the more civilized age
# Copyright (C) 2024-  Artur Ciesielski <artur.ciesielski@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
from abc import ABCMeta
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar, Generic, TypeAlias, TypeVar

from envenom.errors import (
    ConfigurationFileUnreadable,
    InvalidConfiguration,
    MissingConfiguration,
)

T = TypeVar("T")

Namespace: TypeAlias = Iterable[str] | str

DefaultType: TypeAlias = Callable[[], T] | T
ParserType: TypeAlias = Callable[[str], T]


def get_env_var_value(name: str) -> str | None:
    return os.environ.get(name)


def get_file_var_value(name: str) -> str | None:
    with open(name, "r") as f:
        return f.read().strip() or None


def get_combined_var_value(env: str, file: str) -> str | None:
    return get_file_var_value(file) or get_env_var_value(env)


@dataclass
class Var(Generic[T], metaclass=ABCMeta):
    name: str
    namespace: Namespace | None = field(default=None)
    parser: ParserType[T] = field(repr=False, kw_only=True)
    file: bool = field(repr=False, kw_only=True, default=True)

    env_name_pattern: ClassVar[re.Pattern[str]] = re.compile("[^0-9a-zA-Z_]+")

    def get(self) -> T | None:
        if (v := self.get_raw_value()) is None:
            return None

        try:
            return self.parser(v)
        except ValueError as e:
            raise InvalidConfiguration(self.env_name, v) from e

    def get_raw_value(self) -> str | None:
        if self.file:
            if (file := get_env_var_value(self.file_env_name)) is not None:
                try:
                    return get_combined_var_value(self.env_name, file)
                except IOError as e:
                    raise ConfigurationFileUnreadable(self.env_name, file) from e

        return get_env_var_value(self.env_name)

    @cached_property
    def normalized_namespace(self) -> str | None:
        if self.namespace is None:
            return None

        if isinstance(self.namespace, str):
            namespace = (self.namespace,)
        else:
            namespace = self.namespace

        return "__".join(
            map(lambda s: re.sub(self.env_name_pattern, "_", s).upper(), namespace)
        )

    @cached_property
    def namespace_prefix(self) -> str:
        return (
            f"{self.normalized_namespace}__"
            if self.normalized_namespace is not None
            else ""
        )

    @cached_property
    def normalized_name(self) -> str:
        return re.sub(self.env_name_pattern, "_", self.name).upper()

    @cached_property
    def env_name(self) -> str:
        return f"{self.namespace_prefix}{self.normalized_name}"

    @cached_property
    def file_env_name(self) -> str:
        return f"{self.env_name}__FILE"


class OptionalVar(Var[T]):
    pass


@dataclass
class VarWithDefault(Generic[T], Var[T]):
    default: DefaultType[T] = field(repr=False, kw_only=True)

    def get(self) -> T:
        return (value) if (value := super().get()) is not None else self.get_default()

    def get_default(self) -> T:
        return self.default if not callable(self.default) else self.default()


class RequiredVar(Var[T]):
    def get(self) -> T:
        if (value := super().get()) is None:
            raise MissingConfiguration(self.env_name)
        return value
