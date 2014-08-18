# SharePy

Flask webapplication usable to send uploaded files via token link.

## Installation

Set up a config.py file with a SECRET_KEY.

## Uploading files

The first idea is to collect locally existing 'unregistered' files from a users folder and convert it to a 'registered' storage object.

1. The user uploads a file to /opt/sharepy/users/<login>
2. The frontend shows the new file and gives possibility to register the file
3. Registering moves the file to another internal folder, renamed as the calculated hashstring
4. The file object can then be shared by the user, with one-time tokens, statistics etc.

A newer version of a file is then again to be registered, so there will be no confusion.
