"""

    PROJECT: flex_toolbox
    FILENAME: update.py
    AUTHOR: David NAISSE
    DATE: March 3rd, 2024

    DESCRIPTION: update command functions

    TEST STATUS: DOES NOT REQUIRE TESTING
"""

import subprocess
import os
import shutil

from src.utils import on_shutil_rm_error


def update_command_func(args):
    """
    Action on update command.

    TEST STATUS: DOES NOT REQUIRE TESTING
    """

    try:
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

        print("#" * os.get_terminal_size().columns)
        subprocess.run(["pip", "show", "ftbx"], check=True)
        print("#" * os.get_terminal_size().columns)

        print(
            f"\nNow trying to update resources from bitbucket (flex-icons, templates..): \n"
        )
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "git@bitbucket.org:ooyalaflex/flex-toolbox.git",
                os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox"),
            ],
            check=True,
        )

        # flex-icons
        shutil.copytree(
            os.path.join(
                os.path.expanduser("~"), ".ftbx", "flex-toolbox", "flex-icons"
            ),
            os.path.join(os.path.expanduser("~"), ".ftbx", "flex-icons"),
            dirs_exist_ok=True,
        )
        print(f"\nflex-icons have been updated successfully ('~/.ftbx/flex-icons/'). ")

        # templates
        shutil.copytree(
            os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox", "templates"),
            os.path.join(os.path.expanduser("~"), ".ftbx", "templates"),
            dirs_exist_ok=True,
        )
        print(f"templates have been updated successfully ('~/.ftbx/templates/').\n ")

        # delete temp repo
        shutil.rmtree(
            os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox"),
            onexc=on_shutil_rm_error,
        )

    except subprocess.CalledProcessError as error:
        print(error)
