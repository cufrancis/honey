#!/usr/bin/env python
# coding=utf-8
import sys
sys.path.append("../../../")

from .APIHandler import APIHandler
import api
import utils
import time
import datetime
from bson.objectid import ObjectId
from session import sessionToken
from auth import generator_sessionToken
import tornado.web

class index(APIHandler):

    @api.application_verification
    def post(self):
        """
        POST /users
        user register
        example :
            body: {"username":"llnhhy", "password":"123456", email:"test@test.com"}
        """
        args = utils.body_decode(self.request.body)

        if args.get('username', '') == '' or args.get('password') == '':
            self.write_error("username or password is empty!", 401)
        if self.db.users.find_one({'username':args.get('username')}) is not None:
            self.write_error("username has isset!", 401)

        user = {
            'username':args.get('username', ''),
            'password':args.get('password', ''),
            'email':args.get('email', ''),
            'phone':args.get('phone', ''),
            'age':args.get('age', 18),
            'sex':args.get('sex', ''),
            'created_at':datetime.datetime.utcnow(),
            'updated_at':datetime.datetime.utcnow(),
            # 'sessionToken':args.get('username', 'defaultSessionToken'),
        }
        user_id = self.db.users.insert_one(user).inserted_id

        if user_id is not None:
            # success
            info = self.db.users.find_one({'_id':user_id}, ['created_at', '_id', 'username', 'sessionToken'])
            data = {
                'objectId':str(info.get('_id', '')),
                'sessionToken':info.get('sessionToken', ''),
                # from datetime tuple convert to unix timestamp
                'created_at':time.mktime(info.get('created_at', '').timetuple()),
            }
            # write session token in redis server!
            self.sessionToken.create(user.get('username'))
            self.write_json(data, 201)
        else:
            self.write_error("Some error!, contact administrator.", 401)

class login(APIHandler):
    """
    login
    """
    @api.application_verification
    def post(self):
        args = utils.body_decode(self.request.body)

        user = self.db.users.find_one({'username':args.get('username', ''), 'password':args.get('password')},
                                        projection={'password':False})
        if user is not None:
            user['created_at'] = time.mktime(user.get('created_at', '').timetuple())
            user['updated_at'] = time.mktime(user.get('updated_at', '').timetuple())

            data = {
                'objectId':str(user.get('_id', '')),
                'sessionToken':self.sessionToken.create(user)
            }
            data.update(user)
            # delet _id : object_id

            self.write_json(data)
            print(data)

class user(APIHandler):

    @api.application_verification
    @api.authenticated
    # @tornado.web.authenticated
    def get(self, username):
        # print(self.current_user)
        # print(username)
        del self.current_user['password']
        self.write_json(self.current_user)
