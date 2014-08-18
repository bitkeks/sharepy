#!/usr/bin/python
# -*- coding: utf-8 -*-

from passlib.hash import sha512_crypt


def hash_password(password):
    """Hash a clear text password before saving it in the database.
    """
    return sha512_crypt.encrypt(password)


def verify_password(password, hashstring):
    """Verify a password from a string and a salted hash.
    Passlib handles the salt for us.
    """
    return sha512_crypt.verify(password, hashstring)
