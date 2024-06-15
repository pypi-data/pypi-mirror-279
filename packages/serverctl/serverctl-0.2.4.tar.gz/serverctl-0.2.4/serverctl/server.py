import os
from pathlib import Path
import subprocess
from .util import exec
import serverctl.util as util
from .config import CONFIG, Server, Git, SERVERS_DIR, CONFIG_FILE
import rich


def cleanup_servers():
    # Get all running servers
    result = subprocess.check_output(
        ["systemctl", "--user", "list-units", "--type=service"]
    )
    lines = [l.strip() for l in result.decode().splitlines()]
    servers = [l.split()[0] for l in lines if l.startswith("serverctl@")]
    server_names = [s.split("@")[1].split(".service")[0] for s in servers]
    servers_to_stop = [s for s in server_names if s not in CONFIG.server]
    if len(servers_to_stop) == 0:
        return
    # Stop all running servers that are not in the config
    for name in server_names:
        if name not in CONFIG.server:
            try:
                util.stop_server(name)
            except Exception as e:
                print(f"❌ Failed to stop server {name}: {e}")
            try:
                # Remove git repo
                exec("rm", "-rf", SERVERS_DIR / name, check=True)
            except Exception as e:
                print(f"❌ Failed to delete server {name}: {e}")
            print(f"🧹 Removed stale server: {name}")


def init_server(name: str, server: Server):
    git = server.git if not isinstance(server.git, str) else Git(url=server.git)
    if not git:
        # No git repo to clone
        return
    if not (SERVERS_DIR / name).exists():
        rec_args = ["--recursive"] if git.recursive else []
        branch_args = ["--branch", git.branch] if git.branch else []
        cwd = SERVERS_DIR
        gitflags = [*branch_args, *rec_args]
        exec("git", "clone", git.url, name, *gitflags, cwd=cwd, check=True, dump=True)
    exec("git", "fetch", cwd=SERVERS_DIR / name, check=True)
    if git.branch:
        exec("git", "checkout", git.branch, cwd=SERVERS_DIR / name, check=True)
    if not (SERVERS_DIR / name).exists():
        exit(f"❌ Error cloning repository {name}")


def clean_server(name: str, config: Server):
    try:
        if not config.clean:
            return
        exec(
            "bash",
            "-l",
            "-c",
            config.clean,
            cwd=SERVERS_DIR / name,
            check=True,
            dump=True,
        )
    except Exception as e:
        exit(f"❌ Error cleaning server {name}: {e}")


def build_server(name: str, config: Server):
    try:
        if not config.build:
            return
        exec(
            "bash",
            "-l",
            "-c",
            config.build,
            cwd=SERVERS_DIR / name,
            check=True,
            dump=True,
        )
    except Exception as e:
        exit(f"❌ Error building server {name}: {e}")


def start_server(name: str, clean: bool, update: bool, log=True):
    server = CONFIG.server.get(name)
    if server is None:
        exit(f"❌ Server {name} not found in config")
    try:
        # 1. Stop server if running
        util.stop_server(name, disable=False, check=False)
        # 2. Clone repo if not exists
        init_server(name, server)
        # 3. Clean server
        if clean:
            clean_server(name, server)
        # 4. Update server
        if update and server.git:
            util.update_repo(SERVERS_DIR / name)
        # 5. Build if needed
        if server.build:
            build_server(name, server)
        # 6. Start service
        util.start_server(name)
    except Exception as e:
        exit(f"❌ Error starting server {name}: {e}")
    if log:
        print(f"✅ Server {name} started")


def stop_server(name: str):
    server = CONFIG.server.get(name)
    if server is None:
        exit(f"❌ Server {name} not found in config")
    try:
        util.stop_server(name)
    except Exception as e:
        exit(f"❌ Error stopping server {name}: {e}")
    print(f"✅ Server {name} stopped")


def restart_server(name: str):
    util.restart_server(name)
    print(f"✅ Server {name} restarted")


def start_all_servers(clean: bool, update: bool):
    for name in CONFIG.server:
        start_server(name, clean, update)


def stop_all_servers():
    for name in CONFIG.server:
        stop_server(name)


def update_server(name: str):
    server = CONFIG.server.get(name)
    print(f"🔄 Updating server {name}...")
    if server is None:
        exit(f"❌ Server {name} not found in config")
    try:
        if not server.git:
            util.update_repo(SERVERS_DIR / name)
        start_server(name, clean=True, update=True, log=False)
    except Exception as e:
        exit(f"❌ Error updating server {name}: {e}")
    print(f"✅ Server {name} updated")


def show_server_status(name: str):
    util.get_server_status(name)


def show_all_server_status():
    for name, server in CONFIG.server.items():
        auto = "[italic](auto-update)[/italic]" if server.auto_update else ""
        status = (
            "🟢 [green]ACTIVE[/green]"
            if util.server_is_active(name)
            else "🔴 [red]INACTIVE[/red]"
        )
        rich.print(f"[bold]{name}[/bold]: {status} {auto}")


def edit_config_file():
    editor = util.get_editor()
    if not editor:
        exit("❌ No text editor found. Please open the file manually: {CONFIG_FILE}")
    os.system(f"{editor} {CONFIG_FILE}")


def run_server(name: str):
    server = CONFIG.server.get(name)
    if server is None:
        exit(f"❌ Server {name} not found in config")
    try:
        print(f"🟢 Starting server {name} ...")
        os.environ.update(server.env)
        env = {k: v for k, v in os.environ.items() if v is not None}
        if server.cwd:
            cwd_s = os.path.expandvars(os.path.expanduser(server.cwd))
            cwd = Path(cwd_s)
        else:
            cwd = SERVERS_DIR / name
        cwd.mkdir(exist_ok=True, parents=True)
        exec("bash", "-l", "-c", server.run, cwd=cwd, env=env, dump=True, check=True)
    except Exception as e:
        exit(f"❌ Error running server {name}: {e}")
