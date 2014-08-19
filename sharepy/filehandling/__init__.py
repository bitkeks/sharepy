#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
All file handling related code:
* Checking file system permissions
* Lookup file information
* Moving files from upload to storage
* Removing files
"""

import os
from sharepy.config import FILES_UPLOADDIR, FILES_STORAGEDIR


def check_permissions():
    """Check if folders exist and if they are read-writeable.
    Should be used in the startup script to check the configured paths.
    """
    for d in (FILES_UPLOADDIR, FILES_STORAGEDIR):
        if not os.path.exists(d):
            exit(u"Directory {} does not exist!".format(d))

        if not (os.access(d, os.R_OK) and os.access(d, os.W_OK)):
            exit(u"Cannot use directory {}. Wrong permissions!".format(d))


def create_useruploaddir(username):
    """Create a users upload dir if it does not exist.
    """
    userdir = os.path.join(FILES_UPLOADDIR, username)
    if not os.path.exists(userdir):
        os.mkdir(userdir, 0700)
