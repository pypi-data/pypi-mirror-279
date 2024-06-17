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


def as_boolean(v: str) -> bool:
    """
    This handles one of the most basic conversions in a sensible manner.
    `bool`, unlike `int`, will not do the right thing, so here's a convenience function.

    `t`, `true`, `y`, `yes`, `1`, `+`, `✓` will evaluate to `True`.

    `f`, `false`, `n`, `no`, `0`, `-`, `✗` will evaluate to `False`.

    The parser is case-insensitive.
    """
    normalized = v.lower()
    if normalized in {"t", "true", "y", "yes", "1", "+", "✓"}:
        return True
    if normalized in {"f", "false", "n", "no", "0", "-", "✗"}:
        return False
    raise ValueError(v)
