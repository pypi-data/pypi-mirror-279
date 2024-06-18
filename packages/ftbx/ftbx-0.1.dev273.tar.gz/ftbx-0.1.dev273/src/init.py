"""

    PROJECT: flex_toolbox
    FILENAME: init.py
    AUTHOR: David NAISSE
    DATE: December 15, 2023

    DESCRIPTION: init command functions

    TEST STATUS: FULLY TESTED
"""

import os
import platform
import subprocess
import shutil
import git


def init_command_func(args):
    """
    Action on init command.

    TEST STATUS: FULLY TESTED

    :param args:
    :return:
    """

    # get os
    user_os = platform.system()
    print(f"\nOS: {user_os.upper()}\n")

    # create dotfolder
    os.makedirs(os.path.join(os.path.expanduser("~"), ".ftbx"), exist_ok=True)
    print(f"Directory '.ftbx' has been created successfully. \n")

    try:

        print(f"Now trying to fetch resources from bitbucket (flex-icons, templates..): \n")
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
            os.path.join(os.path.expanduser("~"), ".ftbx", "flex-toolbox", "templates"),
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
