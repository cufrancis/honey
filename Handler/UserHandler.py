#!/usr/bin/env python
# coding=utf-8

from .APIHandler import APIHandler
import api

class index(APIHandler):

    @api.application_verification
    def get(self):
        self.write_json()
