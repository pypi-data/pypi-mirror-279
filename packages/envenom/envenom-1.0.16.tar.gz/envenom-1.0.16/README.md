<!-- `envenom` - an elegant application configurator for the more civilized age
Copyright (C) 2024-  Artur Ciesielski <artur.ciesielski@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. -->

# envenom

[![pipeline status](https://gitlab.com/arcanery/python/envenom/badges/main/pipeline.svg)](https://gitlab.com/arcanery/python/envenom/-/commits/main)
[![coverage report](https://gitlab.com/arcanery/python/envenom/badges/main/coverage.svg)](https://gitlab.com/arcanery/python/envenom/-/commits/main)
[![latest release](https://gitlab.com/arcanery/python/envenom/-/badges/release.svg)](https://gitlab.com/arcanery/python/envenom/-/releases)

## Introduction

`envenom` is an elegant application configurator for the more civilized age.

`envenom` is written with simplicity and type safety in mind. It allows
you to express your application configuration declaratively in a dataclass-like
format while providing your application with type information about each entry,
its nullability and default values.

`envenom` is designed for modern usecases, allowing for pulling configuration from
environment variables or files for more sophisticated deployments on platforms
like Kubernetes.

## How it works

An `envenom` config class looks like a regular Python dataclass - because it is one.

The `config` decorator creates a new dataclass by converting the config fields into
their `dataclass` equivalents providing the relevant dataclass field parameters.

This also means it's 100% compatible with dataclasses. You can:
- use a config class as a property of a regular dataclass
- use a regular dataclass as a property of a config class
- declare static or dynamic fields using standard dataclass syntax
- use the `InitVar`/`__post_init__` method for delayed initialization of fields
- use methods, `classmethod`s, `staticmethod`s, and properties

`envenom` will automatically fetch the environment variable values to populate the
dataclass fields (optionally running a parser so that the field is automatically
converted to a desired type). This works out of the box with all types trivially
convertible from `str`, like `Enum` and `UUID`, and with any object type that can be
instantiated easily from a single string (any function `(str,) -> T` will work as a
parser).

If using a static type checker the type deduction system will correctly identify most
mistakes if you declare fields, parsers or default values with mismatched types. There
are certain exceptions, for example `T` will always satisfy type bounds `T | None`.

The `with_default` field variant accepts both objects and callables `() -> T`
to produce the default value if required. Care is required if trying to instantiate
callable objects.

`envenom` also offers reading variable contents from file by specifying an environment
variable with the suffix `__FILE` which contains the path to a file with the respective
secret. This aims to facilitate a common deploy pattern where secrets are mounted as
files (especially prevalent with Kubernetes).

All interaction with the environment is case-sensitive - we'll convert everything to
uppercase, and since `_` is a common separator within environment variable names we use
`_` to replace any and all nonsensical characters, then use `__` to separate namespaces.
Therefore a field `"var"` in namespaces `("ns-1", "ns2")` will be mapped to
`NS_1__NS2__VAR`.

## Usage

### Quickstart guide

Install `envenom` with `python -m pip install envenom`.

```python
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

    print(f"myapp/secret_key: {repr(cfg.secret_key)} {type(cfg.secret_key)}")
    print(f"myapp/db/host: {repr(cfg.db.host)} {type(cfg.db.host)}")
    print(f"myapp/db/port: {repr(cfg.db.port)} {type(cfg.db.port)}")
    print(f"myapp/db/database: {repr(cfg.db.database)} {type(cfg.db.database)}")
    print(f"myapp/db/username: {repr(cfg.db.username)} {type(cfg.db.username)}")
    print(f"myapp/db/password: {repr(cfg.db.password)} {type(cfg.db.password)}")
    print(f"myapp/db/connection_timeout: {repr(cfg.db.connection_timeout)} {type(cfg.db.connection_timeout)}")
    print(f"myapp/db/sslmode_require: {repr(cfg.db.sslmode_require)} {type(cfg.db.sslmode_require)}")
    print(f"myapp/db/connection_string: {repr(cfg.db.connection_string)} {type(cfg.db.connection_string)}")
```

Run the example with `python -m envenom.examples.quickstart`:

```
Traceback (most recent call last):
    ...
    raise MissingConfiguration(self.env_name)
envenom.errors.MissingConfiguration: 'MYAPP__SECRET_KEY'
```

Run the example again with environment set:

```bash
MYAPP__SECRET_KEY='}uZ?uvJdKDM+$2[$dR)).n4q1SX!A$0u{(+D$PVB' \
MYAPP__POSTGRES__HOST='postgres' \
MYAPP__POSTGRES__DATABASE='database-name' \
MYAPP__POSTGRES__USERNAME='user' \
MYAPP__POSTGRES__SSLMODE_REQUIRE='t' \
MYAPP__POSTGRES__CONNECTION_TIMEOUT='15' \
python -m envenom.examples.quickstart
```

```bash
myapp/secret_key: '}uZ?uvJdKDM+$2[$dR)).n4q1SX!A$0u{(+D$PVB' <class 'str'>
myapp/db/host: 'postgres' <class 'str'>
myapp/db/port: 5432 <class 'int'>
myapp/db/database: 'database-name' <class 'str'>
myapp/db/username: 'user' <class 'str'>
myapp/db/password: None <class 'NoneType'>
myapp/db/connection_timeout: 15 <class 'int'>
myapp/db/sslmode_require: True <class 'bool'>
myapp/db/connection_string: 'postgresql+psycopg://user@postgres:5432/database-name?sslmode=require&timeout=15' <class 'str'>
```

### Next steps

See the [documentation](https://arcanery.gitlab.io/python/envenom/) for more info
and examples of advanced usage.
