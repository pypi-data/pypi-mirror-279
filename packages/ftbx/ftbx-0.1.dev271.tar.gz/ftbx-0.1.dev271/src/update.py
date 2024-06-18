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
import git


def update_command_func(args):
    """
    Action on update command.

    TEST STATUS: DOES NOT REQUIRE TESTING
    """

    try:
        print(f"\nUpdating ftbx to latest version..\n")
        subprocess.run(
            ["pip", "install", "ftbx", "--upgrade", "--break-system-packages", "--quiet"],
            check=True,
        )
        
        subprocess.run(
            ["pip", "show", "ftbx"],
            check=True
        )

        print(f"\nNow trying to update resources from bitbucket (flex-icons, templates..): \n")
        git.Repo.clone_from(
            "git@bitbucket.org:ooyalaflex/flex-toolbox.git",
            os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox"),
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
            os.path.join(
                os.path.expanduser("~"), ".ftbx", "flex-toolbox", "templates"
            ),
            os.path.join(os.path.expanduser("~"), ".ftbx", "templates"),
            dirs_exist_ok=True,
        )
        print(f"templates have been updated successfully ('~/.ftbx/templates/').\n ")

        # variables
        shutil.copy(
            os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox", "variables.yml"),
            os.path.join(os.path.expanduser("~"), ".ftbx"),
        )

        # delete temp repo
        shutil.rmtree(os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox"))

    except subprocess.CalledProcessError as error:
        print(error)
