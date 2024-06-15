import subprocess

import typer
from .util import exec
import serverctl.util as util
import time
from .config import SERVERS_DIR, Config, Server, SERVICE_DAEMON_FILE

UPDATE_INTERVAL = 60  # seconds

app = typer.Typer()


@app.command(help="Install the serverctl daemon service")
def install():
    util.start_systemd_service("serverctl", SERVICE_DAEMON_FILE)
    print(f"✅ Installed serverctl daemon")


@app.command(help="Uninstall the serverctl daemon service")
def uninstall():
    util.stop_systemd_service("serverctl")
    print(f"✅ Uninstalled serverctl daemon")


@app.command(help="Get the status of the serverctl daemon service")
def status():
    util.get_systemd_service_status("serverctl")


@app.command(help="Restart the serverctl daemon service")
def restart():
    util.restart_systemd_service("serverctl")


def __update_server(name: str, server: Server):
    cwd = SERVERS_DIR / name
    exec("git", "remote", "update", cwd=cwd, check=True)
    out = subprocess.check_output(["git", "status", "-uno"], cwd=cwd).decode()
    if not "Your branch is up to date" in out:
        print(f"🔄 Updating server {name}")
        try:
            util.stop_server(name)
            util.update_repo(SERVERS_DIR / name)
            util.start_server(name)
        except Exception as e:
            print(f"❌ Failed to update server {name}: {e}")


@app.command(help="Start the serverctl daemon in foreground")
def start():
    while True:
        config = Config.load()
        for name, server in config.server.items():
            if server.auto_update:
                __update_server(name, server)
        time.sleep(UPDATE_INTERVAL)
