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

import enum
import os
import pprint
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Self
from unittest.mock import patch
from uuid import UUID, uuid4

from envenom import config, optional, required, subconfig, with_default
from envenom.parsers import as_boolean

# some custom classes with different structure and behavior


@dataclass
class CallMe:
    # CallMe is callable, so we need to wrap it in a closure
    # to ensure the instance will get injected when defining the field

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __call__(self, *_: Any, **__: Any) -> Self:
        raise RuntimeError("this is not the desired result!")


class ExitCode(enum.IntEnum):
    OK = 0
    MISSING_CONFIG = 1
    INVALID_CONFIG = 2
    CONFIG_FILE_UNREADABLE = 3


class LaunchCode(enum.StrEnum):
    OK = enum.auto()
    LAUNCHPAD_OBSTRUCTED = enum.auto()
    NOT_ENOUGH_FUEL = enum.auto()
    OVERRIDDEN_BY_POTUSPL = enum.auto()


@dataclass
class BoxedInt:
    value: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(int(s))


# and our config section


@config(namespace="ns1")
class BoxedIntsCfg:
    some_boxed_int_1: BoxedInt = with_default(BoxedInt.from_str, default=BoxedInt(2137))
    some_boxed_int_2: BoxedInt = required(BoxedInt.from_str)


@config(namespace=("ns1", "sub-ns1"))
class NamespacedCfg:
    some_int: int | None = optional(int)
    some_int_enum: ExitCode | None = optional(lambda c: ExitCode(int(c)))
    some_str_enum: LaunchCode | None = optional(LaunchCode)


@config()
class NonNamespacedCfg:
    some_str: str | None = optional()
    some_uuid_1: UUID = with_default(UUID, default=uuid4)
    some_uuid_2: UUID = with_default(UUID, default=uuid4)


@dataclass
class FrameworkCfg:
    is_month_number_odd: bool = field(
        default_factory=lambda: date.today().month % 2 == 0
    )
    feature_flag: bool = True
    boxed_ints: BoxedIntsCfg = subconfig(BoxedIntsCfg)


@config(namespace="ns1")
class ApplicationCfg:
    some_str: str = required()
    some_bool: bool = required(as_boolean)
    good_time: CallMe = with_default(lambda _: CallMe(), default=lambda: CallMe())
    namespaced_subconfig: NamespacedCfg = subconfig(NamespacedCfg)
    non_namespaced_subconfig: NonNamespacedCfg = subconfig(NonNamespacedCfg)
    framework_config: FrameworkCfg = subconfig(FrameworkCfg)


# run it

if __name__ == "__main__":
    env = {
        # no namespace
        "SOME_UUID_1": "9f4d52c5-6a9c-47ed-9cee-7dbbf0e17499",
        # namespace ns1
        "NS1__SOME_BOXED_INT_2": "420",
        "NS1__SOME_STR": "pythagoras",
        "NS1__SOME_BOOL": "TruE",
        # namespace ns1/subns1
        "NS1__SUB_NS1__SOME_INT": "69",
        "NS1__SUB_NS1__SOME_INT_ENUM": "0",
        "NS1__SUB_NS1__SOME_STR_ENUM": "overridden_by_potuspl",
    }
    with patch.dict(os.environ, env):
        pprint.pprint(ApplicationCfg())
