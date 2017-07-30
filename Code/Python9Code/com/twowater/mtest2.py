#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class UserInfo(object):
    name = '两点水'


class UserInfo(object):
    def __init__(self, name):
        self.name = name


class UserInfo(object):
    def __init__(self, name, age, account):
        self.name = name
        self._age = age
        self.__account = account
