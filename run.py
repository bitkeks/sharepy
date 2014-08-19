#!/usr/bin/python
# -*- coding: utf-8 -*-

from sharepy.application import app
from sharepy.database import database_init
from sharepy.filehandling import check_permissions

if __name__ == "__main__":
    database_init(_remove=1)
    check_permissions()
    app.run()
