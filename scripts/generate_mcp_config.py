"""Print a client-neutral local MCP stdio configuration; never change user settings."""
import json
from pathlib import Path
import sys


def build_config(python_executable=None):
    root = Path(__file__).resolve().parents[1]
    interpreter = Path(python_executable or sys.executable).resolve()
    return {
        "mcpServers": {
            "advanced-hwp": {
                "command": str(interpreter),
                "args": [str(root / "advanced_hwp_server.py")],
            }
        }
    }


if __name__ == "__main__":
    print(json.dumps(build_config(), ensure_ascii=False, indent=2))
