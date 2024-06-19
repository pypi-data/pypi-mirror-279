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

from fastapi import FastAPI
from fastapi.routing import APIRoute

from envenom import config, with_default
from envenom.parsers import as_boolean


@config()
class FastAPICfg:
    static_docs: bool = with_default(as_boolean, default=True)
    interactive_docs: bool = with_default(as_boolean, default=False)


@dataclass
class IndexResponse:
    pass


async def get_index() -> IndexResponse:
    return IndexResponse()


cfg = FastAPICfg()
app = FastAPI(
    redoc_url="/redoc" if cfg.static_docs else None,
    docs_url="/docs" if cfg.interactive_docs else None,
    routes=[
        APIRoute("/", get_index, methods={"GET"}),
    ],
)
