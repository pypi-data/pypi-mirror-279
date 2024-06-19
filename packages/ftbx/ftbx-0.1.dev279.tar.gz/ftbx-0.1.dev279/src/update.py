"""

    PROJECT: flex_toolbox
    FILENAME: update.py
    AUTHOR: David NAISSE
    DATE: March 3rd, 2024

    DESCRIPTION: update command functions

    TEST STATUS: DOES NOT REQUIRE TESTING
"""

import subprocess

from src.utils import on_shutil_rm_error, update_toolbox_resources


def update_command_func(args):
    """
    Action on update command.

    TEST STATUS: DOES NOT REQUIRE TESTING
    """

    print(f"\nUpdating ftbx to latest version..\n")
    subprocess.run(
        [
            "pip",
            "install",
            "ftbx",
            "--upgrade",
            "--break-system-packages",
            "--quiet",
        ],
        check=True,
    )

    # fetch updated resources
    update_toolbox_resources()
