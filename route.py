#!/usr/bin/env python
# coding=utf-8

# 路由表

import Handler.IndexHandler as Index
import Handler.UserHandler as User

urls = [
    (r'/', Index.index), # 404 index
    (r'/users', User.index),
    (r'/users/(.*)/updatePassword', User.updatePassword),
    (r'/users/(.*)', User.user),
    (r'/users/(.*)/refreshSessionToken', User.refreshSessionToken),
    (r'/login', User.login),
    (r'/emailVerified/(.*)', User.emailVerified),
    (r'/emailVerified', User.emailVerified),
    # (r'/usersByMobilePhone', User.usersByMobilePhone),
    # unstable
    # (r'/requestPasswordReset/(.*)', User.requestPasswordReset),
    # (r'/requestPasswordReset', User.requestPasswordReset),

]
