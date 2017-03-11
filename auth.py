#!/usr/bin/env python
# coding=utf-8

import functools

def generator_sessionToken(string):
    """
    generator session token
    """
    return 'sessionToken_'+string

def account_lock(method):
    """
    account Lock
    6 times
    lock 15 minutes
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kw):
        

        return method(self, *args, **kw)

    return wrapper
