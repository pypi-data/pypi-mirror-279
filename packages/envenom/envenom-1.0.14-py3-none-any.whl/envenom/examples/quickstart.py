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

# flake8: noqa

from functools import cached_property

from envenom import config, optional, required, subconfig, with_default
from envenom.parsers import as_boolean


@config(namespace=("myapp", "postgres"))
class DbCfg:
    host: str = required()
    port: int = with_default(int, default=5432)
    database: str = required()
    username: str | None = optional()
    password: str | None = optional()
    connection_timeout: int | None = optional(int)
    sslmode_require: bool = with_default(as_boolean, default=False)

    @cached_property
    def connection_string(self) -> str:
        auth = ""
        if self.username:
            auth += self.username
        if self.password:
            auth += f":{self.password}"
        if auth:
            auth += "@"

        query: dict[str, str] = {}
        if self.connection_timeout:
            query["timeout"] = str(self.connection_timeout)
        if self.sslmode_require:
            query["sslmode"] = "require"

        if query_string := "&".join((f"{key}={value}" for key, value in query.items())):
            query_string = f"?{query_string}"

        return (
            f"postgresql+psycopg://{auth}{self.host}:{self.port}"
            f"/{self.database}{query_string}"
        )


@config(namespace="myapp")
class AppCfg:
    secret_key: str = required()

    db: DbCfg = subconfig(DbCfg)


if __name__ == "__main__":
    cfg = AppCfg()

    # fmt: off
    print(f"myapp/secret_key: {repr(cfg.secret_key)} {type(cfg.secret_key)}")
    print(f"myapp/db/host: {repr(cfg.db.host)} {type(cfg.db.host)}")
    print(f"myapp/db/port: {repr(cfg.db.port)} {type(cfg.db.port)}")
    print(f"myapp/db/database: {repr(cfg.db.database)} {type(cfg.db.database)}")
    print(f"myapp/db/username: {repr(cfg.db.username)} {type(cfg.db.username)}")
    print(f"myapp/db/password: {repr(cfg.db.password)} {type(cfg.db.password)}")
    print(f"myapp/db/connection_timeout: {repr(cfg.db.connection_timeout)} {type(cfg.db.connection_timeout)}")
    print(f"myapp/db/sslmode_require: {repr(cfg.db.sslmode_require)} {type(cfg.db.sslmode_require)}")
    print(f"myapp/db/connection_string: {repr(cfg.db.connection_string)} {type(cfg.db.connection_string)}")
    # fmt: on
