#!/usr/bin/env python
# coding=utf-8

# 路由表

import Handler.IndexHandler as Index
import Handler.UserHandler as User

urls = [
    (r'/', Index.index),
    (r'/users', User.index),
    (r'/login', User.login),
    (r'/users/(.*)', User.user),
]
