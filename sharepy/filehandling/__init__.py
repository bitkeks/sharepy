#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
All file handling related code:
* Checking file system permissions
* Lookup file information
* Moving files from upload to storage
* Removing files
"""

from collections import namedtuple
import os
from sharepy.config import FILES_UPLOADDIR, FILES_STORAGEDIR
from sharepy.database import get_userfiles


def check_permissions():
    """Check if folders exist and if they are read-writeable.
    Should be used in the startup script to check the configured paths.
    """
    for d in (FILES_UPLOADDIR, FILES_STORAGEDIR):
        if not os.path.exists(d):
            exit(u"Directory {} does not exist!".format(d))

        if not (os.access(d, os.R_OK) and os.access(d, os.W_OK)):
            exit(u"Cannot use directory {}. Wrong permissions!".format(d))


def check_storagefile_exist():
    pass


def create_useruploaddir(username):
    """Create a users upload dir if it does not exist.
    """
    userdir = os.path.join(FILES_UPLOADDIR, username)
    if not os.path.exists(userdir):
        os.mkdir(userdir, 0700)


def get_unregistered_files(username):
    """Get all files from a users upload dir.
    """
    userdir = os.path.join(FILES_UPLOADDIR, username)
    files = []
    file_tuple = namedtuple('userfile', 'path name size')
    for f in os.listdir(userdir):
        file_path = os.path.join(userdir, f)
        if os.path.isfile(file_path):
            files.append(file_tuple(file_path, f, os.lstat(file_path).st_size))

    return files


def get_filesize_byte(username, filename):
    """Get the size of an uploaded file in bytes.
    """
    file_path = os.path.join(FILES_UPLOADDIR, username, filename)
    return os.lstat(file_path).st_size

