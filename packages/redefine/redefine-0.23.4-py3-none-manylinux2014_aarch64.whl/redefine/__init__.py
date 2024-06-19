"this module contains the function that will run when the command is typed in the cli"

import os
import pathlib
import subprocess
import sys

INSTALLER_BINARY = "redefine_installer"


def _get_binary_name() -> str:
    if sys.platform.lower() == "win32":
        return f"{INSTALLER_BINARY}.exe"
    return INSTALLER_BINARY


def execute_from_cmd() -> int:
    try:
        redefine_installer_dir = pathlib.Path(__file__).parent.resolve()
        redefine_installer_abs_path = os.path.join(
            redefine_installer_dir, _get_binary_name()
        )
        if not os.path.exists(redefine_installer_abs_path):
            print("Redefine Installation Error: Redefine not running")
            return 0
    except Exception as ex:
        print(ex)
        return 0

    cmd = [redefine_installer_abs_path]
    cmd.extend(sys.argv[1:])

    result = subprocess.run(" ".join(cmd), shell=True, check=False)
    if (
        "session_check" in sys.argv
        or "--exit-code" in sys.argv
        or "predict" in sys.argv
    ):
        return result.returncode
    return 0
