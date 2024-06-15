from dataclasses import dataclass, field
import tosholi
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "serverctl"
CONFIG_FILE = CONFIG_DIR / "config.toml"

LOCAL_SHARE_DIR = Path.home() / ".local" / "share" / "serverctl"
SERVERS_DIR = LOCAL_SHARE_DIR / "servers"
LOGS_DIR = LOCAL_SHARE_DIR / "logs"
LOCK_FILE = LOCAL_SHARE_DIR / "lock"

SERVICE_FILE = Path(__file__).parent.parent / "serverctl@.service"
SERVICE_DAEMON_FILE = Path(__file__).parent.parent / "serverctl.service"

CONFIG_DIR.mkdir(exist_ok=True, parents=True)
SERVERS_DIR.mkdir(exist_ok=True, parents=True)
LOGS_DIR.mkdir(exist_ok=True, parents=True)

if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text(
        (Path(__file__).parent.parent / "config.template.toml").read_text()
    )


@dataclass
class Git:
    url: str
    branch: str | None = None
    recursive: bool = False


@dataclass
class Server:
    run: str
    """The command to run the server"""

    cwd: str | None = None
    """The working directory to run the server in"""

    git: str | Git | None = None
    """The git repository to clone and update the server from"""

    env: dict[str, str] = field(default_factory=dict)
    """The environment variables to set before running the server"""

    build: str | None = None
    """The command to build the server"""

    clean: str | None = None
    """The command to clean the server"""

    auto_update: bool = False
    """Whether to update the server automatically on remote changes"""


@dataclass
class Config:
    server: dict[str, Server] = field(default_factory=dict)

    @staticmethod
    def load():
        if not CONFIG_FILE.exists():
            return Config()
        with open(CONFIG_FILE, "rb") as f:
            config = tosholi.load(Config, f)  # type: ignore
        return config


CONFIG = Config.load()
