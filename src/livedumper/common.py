"Common functions that may be used everywhere"

from __future__ import print_function

import os
import sys
from distutils.util import strtobool


def yes_no_query(question):
    """Ask the user *question* for 'yes' or 'no'; ask again until user
    inputs a valid option.

    Returns:
    'True' if user answered 'y', 'yes', 't', 'true', 'on' or '1'.
    'False' if user answered 'n', 'no', 'f', 'false', 'off' or '0'.
    """

    print("{} (y/n)".format(question), end=" "),
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            print("Please respond with 'y' or 'n'.")


def ask_overwrite(dest):
    """Check if file *dest* exists. If 'True', asks if the user wants
    to overwrite it (just remove the file for later overwrite).
    """

    msg = "File '{}' already exists. Overwrite file?".format(dest)
    if os.path.exists(dest):
        if yes_no_query(msg):
            os.remove(dest)
        else:
            sys.exit("Cancelling operation...")
