#!/usr/bin/env python
# coding=utf-8

import json
from tornado.web import Finish
import tornado.web
from db import db

class APIHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.set_header('Content-Type', 'text/json')
        self.set_header('Server', 'Tornado')
        self.set_header('Connection','keep-alive')
        self.db = db


        # if self.settings.get('allow_remote_access'):
        #     self.access_control_allow()

    def write_json(self, data, status_code=200, msg='success.'):
        self.set_header('Cache-Control', "no-cache")
        self.set_status(status_code)

        self.write(json.dumps({
            'meta':status_code,
            'data':data,
            'msg':msg,
        }))
        raise Finish()

    def write_error(self, msg, status_code=200):
        self.write_json(data='', status_code=status_code, msg=msg)

    # def application_verification(self):
    def application_verification(self, headers):
        # 验证appid 与appkey
        appid = headers.get('X-LC-Id', '')
        appkey = headers.get('X-LC-Key', '')

        if appid == '' or appkey == '':
            self.write_error(msg="Unauthorized.", status_code=401)
        #
        data = db.application.find_one({"appId":appid, "appKey":appkey}, "_id")
        if data is not None:
            return True
