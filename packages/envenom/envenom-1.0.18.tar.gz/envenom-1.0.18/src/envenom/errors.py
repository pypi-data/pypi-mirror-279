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

from dataclasses import dataclass


@dataclass
class ConfigurationError(Exception):
    name: str

    def __str__(self) -> str:
        return f"'{self.name}'"

    def __format__(self, __format_spec: str) -> str:
        match __format_spec:
            case "class":
                return self.__class__.__name__
            case _:
                return f"{self.__class__.__name__}({str(self)})"


class MissingConfiguration(ConfigurationError):
    pass


@dataclass
class InvalidConfiguration(ConfigurationError):
    value: str

    def __str__(self) -> str:
        return f"{super().__str__()}, '{self.value}'"


class ConfigurationFileUnreadable(InvalidConfiguration):
    pass
