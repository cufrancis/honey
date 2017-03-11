#!/usr/bin/env python
# coding=utf-8

import sys
sys.path.append("../../../")

from db import db

class User(object):

    def __init__(self):
        self.db = db

    def find_one(self):
        pass
