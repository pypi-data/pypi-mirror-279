#!/usr/bin/env python
"""
Transforms database URLs into shell environment variables.
"""
import click


@click.command()
@click.argument("database_url")
@click.option("--prefix", default="PG")
@click.option("--export", is_flag=True)
@click.option("--engine", is_flag=True)
@click.option("--host-key", default="HOST")
@click.option("--port-key", default="PORT")
@click.option("--user-key", default="USER")
@click.option("--password-key", default="PASSWORD")
@click.option("--database-key", default="DATABASE")
def main(database_url, prefix, export, engine, host_key, port_key, user_key, password_key, database_key):
    from urllib.parse import urlparse

    def to_envs(url):
        result = [
            (host_key, url.hostname),
            (port_key, url.port),
            (user_key, url.username),
            (password_key, url.password),
            (database_key, url.path[1:]),
        ]
        if engine:
            result.insert(0, ("ENGINE", url.scheme))
        return tuple(result)

    if export:
        prefix = f"export {prefix}"

    urlparse(database_url)

    for k, v in to_envs(urlparse(database_url)):
        if not v:
            continue
        print(f"{prefix}{k}={v}")


if __name__ == "__main__":
    main.main()
