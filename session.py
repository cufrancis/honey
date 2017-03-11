#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from auth import generator_sessionToken

class SessionManager(object):
    def __init__(self, host='localhost', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.Redis(connection_pool=self.pool)

class Session(object):
    SessionManager = SessionManager().r

    def isInside(self):
        pass

    def smembers(self, key):
        tmp = self.SessionManager.smembers(key)
        result = []
        for k in tmp:
            result.append(int(bytes.decode(k)))

        return result

    def set(self, key, value, px=False, nx=False):
        result = self.SessionManager.set(key, value, px, nx)
        # if outtime != 0:
        #     self.SessionManager.expire(key, outtime)

        return result

    def hset(self, key, field, value):
        try:
            result = self.SessionManager.hset(key, field, value)
            return result
        except:
            return 0

    def hget(self, key, field, convert=True):
        result = self.SessionManager.hget(key, field)

        if convert:
            try:
                return bytes.decode(result)
            except:
                return None

    def get(self, key, convert=True):
        if convert:
            try:
                result = self.SessionManager.get(key)
                return bytes.decode(result)
            except:
                return None

    def zrevrange(self, name, start, end, withscores=False):
        tmps = self.SessionManager.zrevrange(name, start, end, withscores)
        result = []
        for key in tmps:
            result.append(int(bytes.decode(key)))

        return result

    def exists(self, name):
        return self.SessionManager.exists(name)

    def flushdb(self):
        pass
        #return self.r.flushdb()

    def _bytes2str(self, byte, doit=True):
        if not isinstance(byte, bytes):
            return byte

        if doit:
            return bytes.decode(byte)
        else:
            return byte

# session = Session(host = 'localhost', port = 6379)

class sessionToken(Session):

    def generator_token(self, data):
        key = data.get('username', '') + str(data.get('_id'))

        return key

    # @classmethod
    def create(self, data):
        """
        create session token
        """
        # return self.hset(key='sessionToken', field=field, value=value)
        # field = generator_sessionToken(value)
        # key = data.get('username', '') + str(data.get('_id'))
        key = self.generator_token(data)
        result = self.set(key=key, value=data.get('username'))

        return key if result else False

    def find(self, key):
        """
        return
        """
        # key = self.generator_token()
        # result = self.get(field)
        print(self.exists(key))

        if self.exists(key) is False:
            return None
        else:
            return self.get(key)
            # result = self.get(field)

        # return field
