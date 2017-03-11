#!/usr/bin/env python
# coding=utf-8

from .APIHandler import APIHandler
import api
import tornado.web

class index(APIHandler):

    @api.application_verification
    def get(self):
        self.write_json(status_code=404,data={
            'users_list':'http://localhost:8888/users',
        })
