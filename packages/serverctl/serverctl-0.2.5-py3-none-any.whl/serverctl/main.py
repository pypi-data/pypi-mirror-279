import os
from typing import Optional
import typer
from typing_extensions import Annotated

from . import server
from . import daemon
from .util import editor_exists, UpdateLock
import serverctl.util as util

app = typer.Typer(pretty_exceptions_enable=False, add_completion=False)
app.add_typer(daemon.app, name="daemon")


@app.command(help="Start a server")
def start(name: str, clean: bool = False, update: bool = False):
    with UpdateLock():
        server.cleanup_servers()
        server.start_server(name, clean, update)


@app.command(help="Stop a server")
def stop(name: str):
    with UpdateLock():
        server.cleanup_servers()
        server.stop_server(name)


@app.command(help="Restart a server without cleaning, rebuilding or updating")
def restart(name: str):
    with UpdateLock():
        server.cleanup_servers()
        server.restart_server(name)


@app.command(name="start-all", help="Start all servers")
def start_all(clean: bool = False, update: bool = False):
    with UpdateLock():
        server.cleanup_servers()
        server.start_all_servers(clean, update)


@app.command(name="stop-all", help="Stop all servers")
def stop_all():
    with UpdateLock():
        server.cleanup_servers()
        server.stop_all_servers()


@app.command(help="Update a server")
def update(name: str):
    with UpdateLock():
        server.cleanup_servers()
        server.update_server(name)


@app.command(help="Get the status of a server")
def status(
    name: Annotated[
        Optional[str],
        typer.Argument(
            help="The name of the server. Lists the status for all servers by default."
        ),
    ] = None
):
    with UpdateLock():
        server.cleanup_servers()
    if name is None or name.strip() == "":
        server.show_all_server_status()
    else:
        server.show_server_status(name)


if editor_exists():

    @app.command(help="Edit the config file")
    def edit():
        server.edit_config_file()


@app.command(name="run", help="Run a server")
def run(name: str):
    with UpdateLock():
        server.cleanup_servers()
    server.run_server(name)


@app.command(name="sweep", help="Cleanup live servers that are not in the config")
def sweep():
    with UpdateLock():
        server.cleanup_servers()


def main():
    app()
