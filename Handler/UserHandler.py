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
# from session import sessionToken, session
# from auth import generator_sessionToken
import tornado.web
import auth

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
            'emailVerified':False,
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
            self.sessionToken.create(info)
            self.write_json(data, 201)
        else:
            self.write_error("Some error!, contact administrator.", 401)

    @api.application_verification
    def get(self):
        """
        Get all user information
        """
        users = self.db.users.find({})

        # for k in len(users):
        #     print(k)
        result = list()
        for user in users:
            user['_id'] = str(user['_id'])
            user['created_at'] = time.mktime(user.get('created_at', '').timetuple()),
            user['updated_at'] = time.mktime(user.get('updated_at', '').timetuple()),

            result.append(user)

        self.write_json(data={'result':result})
        print(result)

    @api.application_verification
    @api.authenticated
    def put(self, username):
        """
        Update user information
        """
        if self.current_user.get('username') != username:
            self.write_error('Forbidden', status_code=403)

        args = utils.body_decode(self.request.body)
        args['updated_at'] = datetime.datetime.utcnow()

        from pymongo import ReturnDocument
        user = self.db.users.find_one_and_update(
                {'username':self.current_user['username']},
                {'$set':args},
                return_document=ReturnDocument.AFTER
                )
        self.write_json({'updated_at':time.mktime(user.get('updated_at', '').timetuple())})


class login(APIHandler):
    """
    login
    """
    @api.application_verification
    # @auth.account_lock
    def post(self):
        args = utils.body_decode(self.request.body)

        user = self.db.users.find_one({'username':args.get('username', ''), 'password':args.get('password')},
                                        projection={'password':False})
        # print(args)
        if user is not None:
            user['created_at'] = time.mktime(user.get('created_at', '').timetuple())
            user['updated_at'] = time.mktime(user.get('updated_at', '').timetuple())

            data = {
                'objectId':str(user.get('_id', '')),
                'sessionToken':self.sessionToken.create(user)
            }
            data.update(user)
            # delet _id : object_id
            del data['_id']
            # delete failed login log
            key = 'failed_'+args.get('username')
            self.session.dels(key)

            self.write_json(data)
        else:
            # 如果在 15 分钟内，同一个用户登录失败的次数大于 6 次，该用户账户即被云端暂时锁定
            key = 'failed_'+args.get('username')
            result = self.session.get(key)
            if result is not None and int(result) >= 6:
                self.write_error("Account lock!")

            self.session.incr(key, 1)
            if self.session.ttl(key) is None:
                self.session.expire(key, 900) # 900 seconds == 15 minutes
            self.write_error("password or username error", 401)

class updatePassword(APIHandler):

    @api.application_verification
    @api.authenticated
    def put(self, username):
        args = utils.body_decode(self.request.body)
        # print(username)
        if self.current_user.get('username') != username:
            self.write_error('Forbidden', status_code=403)

        if self.current_user.get('password') != args.get('old_password'):
            self.write_error(msg='old password is error')

        from pymongo import ReturnDocument
        user = self.db.users.find_one_and_update(
                {'username':username},
                {'$set':{'password':args.get('new_password')}},
                return_document=AFTER
                )

        user['created_at'] = time.mktime(user.get('created_at', '').timetuple())
        user['updated_at'] = time.mktime(user.get('updated_at', '').timetuple())

        data = {
            'objectId':str(user.get('_id', '')),
            'sessionToken':self.sessionToken.create(user)
        }
        data.update(user)
        # delet _id : object_id
        del data['_id']
        self.write_json(data, msg="update successful!")


class user(APIHandler):

    @api.application_verification
    @api.authenticated
    def get(self, username):
        """
        Get user information
        """
        user = self.db.users.find_one({'username':str(username)}, projection={'password':False})

        if user is None:
            self.write_error(msg = 'username is empty!', status_code=404)

        user['created_at'] = time.mktime(user.get('created_at', '').timetuple())
        user['updated_at'] = time.mktime(user.get('updated_at', '').timetuple())

        data = {
            'objectId':str(user.get('_id', '')),
            'sessionToken':self.sessionToken.create(user)
        }
        data.update(user)
        # delet _id : object_id
        del data['_id']

        self.write_json(data)

class refreshSessionToken(APIHandler):

    @api.application_verification
    @api.authenticated
    def put(self, username):
        # update sessionToken
        print(username)
        """
        1. generator new sessionToken
        2. store in redis and set expire time
        3. return data to result
        """
        user = self.db.users.find_one({'username':username}, projection={'password':False})
        # self.sessionToken.create(user)
        # print(user)
        print(user)

        user['created_at'] = time.mktime(user.get('created_at', '').timetuple())
        user['updated_at'] = time.mktime(user.get('updated_at', '').timetuple())

        data = {
            'objectId':str(user.get('_id', '')),
            'sessionToken':self.sessionToken.update(user)
        }
        data.update(user)
        # delet _id : object_id
        del data['_id']

        self.write_json(data)

class emailVerified(APIHandler):

    @api.application_verification
    @api.authenticated
    def post(self):
        args = utils.body_decode(self.request.body)
        user = self.db.users.find_one({'email':args.get('email', '')}, projection={'password':False})
        # print(user)
        if user is None:
            self.write_error(msg="email is empty!")
        if user.get('emailVerified') is True:
            self.write_error(msg="This email is Verified!")

        # print("No check")
        if self.VerifiedEmail.send(user):
            self.write_json(msg="send email success.")
        else:
            self.write_error(msg="send email error.")
        self.write_json(msg="")
            # self.emailVerified.create(user)

    def get(self, emailVerifiedCode):
        email = self.email_verified.find(emailVerifiedCode)
        # print(email)

        if email is False or email == '':
            self.write_error("emailVerifiedCode Error!", status_code=404)

        from pymongo import ReturnDocument
        user = self.db.users.find_one_and_update(
                    {'email':email},
                    update={'$set': {'emailVerified':True}},
                    return_document=ReturnDocument.AFTER
                    )
        # print(user)
        self.email_verified.delete(emailVerifiedCode)

        self.write_json("Verify email successful!")

class requestPasswordReset(APIHandler):

    @api.application_verification
    @api.authenticated
    def post(self):
        args = utils.body_decode(self.request.body)

        user = self.db.users.find_one({'email':args.get('email', '')}, projection={'password':False})
        if user is None:
            self.write_error("cannot find user!")

        emailResetPassword = utils.emailResetPassword()
        if emailResetPassword.send(user):
            self.write_json("send resetPassword successful")
        else:
            self.write_error("send resetPassword error...")

    # def get(self, code):
    #     emailResetPassword = utils.emailResetPassword()
    #     email = emailResetPassword.find(code)
    #
    #     if email is False or email == '':
    #         self.write_error("Reset password code Error!", status_code=404)
    #
    #     user = self.db.users.find_one({'email':email})
    #
    #     # print(user)
    #     self.emailResetPassword.delete(code)
    #
    #     self.write_json("Verify email successful!")
