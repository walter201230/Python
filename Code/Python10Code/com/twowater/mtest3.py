#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):

    name=''

    def __setattr__(self, name, value):
        # 每一次属性赋值时, __setattr__都会被调用，因此不断调用自身导致无限递归了
        # 会造成程序奔溃
        self.name = value


if __name__ == '__main__':
    user = User()
    user.name='两点水'
