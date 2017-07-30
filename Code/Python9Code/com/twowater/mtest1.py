#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 旧式类
class OldClass:
    def __init__(self, account, name):
        self.account = account;
        self.name = name;


# 新式类
class NewClass(object):
    def __init__(self, account, name):
        self.account = account;
        self.name = name;


if __name__ == '__main__':
    old_class = OldClass(111111, 'OldClass')
    print(old_class)
    print(type(old_class))
    print(dir(old_class))
    print('\n')
    new_class=NewClass(222222,'NewClass')
    print(new_class)
    print(type(new_class))
    print(dir(new_class))
