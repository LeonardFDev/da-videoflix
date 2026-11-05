import subprocess
import sys
import os

try:
    subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Docker is not running or not installed!")
    sys.exit(1)
    

os.environ["DEBUGPY_ENABLED"] = "1"

subprocess.run(
    ["docker", "compose", "up", "-d", "--force-recreate", "web"],
    check=True
)