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

from collections.abc import Callable, Iterable
from dataclasses import Field, dataclass, field
from typing import Any, Type, TypeVar

from envenom.entries import Entry, EntryWithDefault, OptionalEntry, RequiredEntry
from envenom.vars import Var


def __default_parser(v: str) -> str:
    """
    This is technically not strictly needed and could be inlined in Var code.
    But the nice bonus is that doing it this way we coerce the default return type
    to `str` if the user does not specify any parser.
    """
    return v


# Why so much 'type: ignore' around here?
#
# It's a hard truth to accept, but dataclasses are lying to us.
#
# When the `field` function is called it creates a Field[T] object, but it tells
# us that it really returns a T (or sometimes None), I swear, pretty please.
#
# Because we're exposing a similar interface and hooking into this exact layer,
# we therefore need to:
#   1) ignore the return value from `field`; it's a lie anyway
#   2) lie to our consumers on the API side just like `field` would, except of
#      course we supply three versions of the `field` function, so we need
#      to lie on all three fronts.


T = TypeVar("T")


def config(
    namespace: Iterable[str] | str | None = None,
) -> Callable[[Type[T]], Type[T]]:
    def wrapper(cls: Type[T]) -> Type[T]:
        var: Var[Any]
        new_fields: dict[str, Field[Any]] = {
            name: field(
                init=False,
                repr=True,
                hash=True,
                metadata={
                    "type": cls.__annotations__[name],
                    "var": (var := entry.get_var(name, namespace)),
                },
                default_factory=var.get,  # type: ignore (1)
            )
            for name, entry in cls.__dict__.items()
            if isinstance(entry, Entry) and name in cls.__annotations__
        }

        for name, entry in new_fields.items():
            setattr(cls, name, entry)

        return dataclass(frozen=True, eq=True)(cls)

    return wrapper


def subconfig(factory: Callable[[], T]) -> T:
    return field(default_factory=factory)


def optional(
    parser: Callable[[str], T] = __default_parser, *, file: bool = True
) -> T | None:
    return OptionalEntry(parser=parser, file=file)  # type: ignore (2)


def with_default(
    parser: Callable[[str], T] = __default_parser,
    *,
    default: Callable[[], T] | T,
    file: bool = True,
) -> T:
    return EntryWithDefault(
        parser=parser,
        file=file,
        default=default,  # type: ignore (2)
    )


def required(parser: Callable[[str], T] = __default_parser, *, file: bool = True) -> T:
    return RequiredEntry(parser=parser, file=file)  # type: ignore (2)
