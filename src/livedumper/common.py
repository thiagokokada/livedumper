"Common functions that may be used everywhere"

import os
import sys
from distutils.util import strtobool

def yes_no_query(question):
    sys.stdout.write('{} (y/n) '.format(question)),
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            print("Please respond with 'y' or 'n'.")

def ask_overwrite(dest):
    msg = "File '{}' already exists. Overwrite file?".format(dest)
    if os.path.exists(dest):
        if yes_no_query(msg):
            os.remove(dest)
        else:
            sys.exit('Cancelling operation...')
