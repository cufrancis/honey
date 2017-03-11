#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from db import db

class Model(object):
    pass

class User(object):

    def __init__(self):
        self.db = db
