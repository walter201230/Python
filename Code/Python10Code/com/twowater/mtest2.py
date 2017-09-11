#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __new__(cls, *args, **kwargs):
        # 打印 __new__方法中的相关信息
        print('调用了 def __new__ 方法')
        print(args)
        # 最后返回父类的方法
        return super(User, cls).__new__(cls)

    def __init__(self, name, age):
        print('调用了 def __init__ 方法')
        self.name = name
        self.age = age


if __name__ == '__main__':
    usr = User('两点水', 23)
