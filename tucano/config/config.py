from dataclasses import dataclass
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


@dataclass
class GlobalConfiguration:
    workspace_file: str = 'workspace.yaml'
    project_root = get_project_root()


config = GlobalConfiguration()
