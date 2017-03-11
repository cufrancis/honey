#!/usr/bin/env python
# coding=utf-8

# 路由表

import Handler.IndexHandler as Index
import Handler.UserHandler as User

urls = [
    (r'/', Index.index), # 404 index
    (r'/users', User.index),
    (r'/login', User.login),
    (r'/users/(.*)/refreshSessionToken', User.refreshSessionToken),
    (r'/users/(.*)', User.user),
    # (r'/usersByMobilePhone', User.usersByMobilePhone),

]
