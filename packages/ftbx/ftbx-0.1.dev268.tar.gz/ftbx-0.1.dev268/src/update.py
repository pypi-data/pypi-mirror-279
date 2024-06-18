"""

    PROJECT: flex_toolbox
    FILENAME: update.py
    AUTHOR: David NAISSE
    DATE: March 3rd, 2024

    DESCRIPTION: update command functions

    TEST STATUS: DOES NOT REQUIRE TESTING
"""

import subprocess


def update_command_func(args):
    """
    Action on update command.

    TEST STATUS: DOES NOT REQUIRE TESTING
    """

    try:
        subprocess.run(
            [
                'pip',
                'install',
                'ftbx',
                '--upgrade',
                '--break-system-packages'
            ],
            check=True
        )
    except subprocess.CalledProcessError as error:
        print(error)
