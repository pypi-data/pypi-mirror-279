import os
import sys
from typing import Dict, Optional
import subprocess
from shutil import which
import fcntl

from serverctl.config import SERVICE_FILE, LOCK_FILE


def exec(
    prog: str | os.PathLike,
    *args: str | os.PathLike | None,
    cwd: str | os.PathLike = ".",
    env: Optional[Dict[str, str]] = None,
    check: bool = False,
    dump: bool = False,
):
    """Run a command and return the status."""
    cmd: list[str] = [str(prog), *(str(arg) for arg in args if arg is not None)]
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE if not dump else None,
        stderr=subprocess.PIPE if not dump else None,
    )
    if check and result.returncode:
        sys.stderr.buffer.write(result.stderr)
        sys.stderr.buffer.flush()
        sys.exit(result.returncode)
    return result.returncode


def update_repo(cwd: os.PathLike):
    exec("git", "reset", "--hard", "HEAD", cwd=cwd, check=True)
    exec("git", "pull", cwd=cwd, check=True)


def start_systemd_service(name: str, file: os.PathLike):
    exec("systemctl", "--user", "link", file, check=True)
    exec("systemctl", "--user", "daemon-reload", check=True)
    exec("systemctl", "--user", "restart", name, check=True)
    exec("systemctl", "--user", "enable", name, check=True)
    exec("loginctl", "enable-linger", os.getlogin(), check=True)


def stop_systemd_service(name: str, disable=True, check=True):
    exec("systemctl", "--user", "stop", name, check=check)
    if disable:
        exec("systemctl", "--user", "disable", name, check=check)


def systemd_service_is_active(name: str):
    return os.system(f"systemctl --user --quiet is-active {name}") == 0


def get_systemd_service_status(name: str):
    exec("systemctl", "--user", "status", name, dump=True)


def restart_systemd_service(name: str):
    exec("systemctl", "--user", "restart", name, check=True)


def start_server(name: str):
    start_systemd_service(f"serverctl@{name}", SERVICE_FILE)


def restart_server(name: str):
    restart_systemd_service(f"serverctl@{name}")


def stop_server(name: str, disable=True, check=True):
    stop_systemd_service(f"serverctl@{name}", disable, check)


def get_server_status(name: str):
    get_systemd_service_status(f"serverctl@{name}")


def server_is_active(name: str):
    return systemd_service_is_active(f"serverctl@{name}")


def editor_exists():
    return (
        "EDITOR" in os.environ
        or "VISUAL" in os.environ
        or which("nano")
        or which("vim")
    )


def get_editor():
    return (
        os.environ.get("EDITOR")
        or os.environ.get("VISUAL")
        or which("vim")
        or which("nano")
    )


class UpdateLock:
    def __enter__(self):
        self.file = open(LOCK_FILE, "w+")
        fcntl.flock(self.file, fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        fcntl.flock(self.file, fcntl.LOCK_UN)
        self.file.close()


def exclusive(f):
    def wrapper(*args, **kwargs):
        with UpdateLock():
            return f(*args, **kwargs)

    return wrapper
