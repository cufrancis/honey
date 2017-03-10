#!/usr/bin/env python
# coding=utf-8

from pymongo import MongoClient

class Db(object):

    def __init__(self, url='localhost', port=27017, database='honey'):
        client = MongoClient(url, port)
        self.db = client[database]




# from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017/')


# db = client.qamyself
db = Db().db

# print(db.users)

# info = {
#     'username':'llnhhy',
#     'age':'22',
#     'sex':'male',
#     'password':'00000000',
# }
# users = db.users
# count = users.find({'age':'22'}).count()
# if count > 0:
#     print("Have")
    # print(user['username'])
# user_id = users.insert_one(info).inserted_id
# print(user_id)

# print(users.find_one({'username':'llnhhy'}))
