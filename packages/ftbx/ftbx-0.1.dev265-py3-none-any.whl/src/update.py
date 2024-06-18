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


def update_command_func(args):
    """
    Action on update command.

    TEST STATUS: DOES NOT REQUIRE TESTING
    """

    FTBX = os.environ.get('FTBX')
    assert FTBX, "Cannot find environment variable FTBX. Please check your config or run ftbx init if you haven't yet. "

    try:
        subprocess.run(
            [
                'git',
                '--git-dir=' + os.path.join(FTBX, '.git'),
                '--work-tree=' + FTBX,
                'pull',
                'origin',
                'master'
            ],
            check=True
        )
    except subprocess.CalledProcessError as error:
        print(error)
