#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class UserInfo(object):
    lv = 5

    def __init__(self, name, age, account):
        self.name = name
        self._age = age
        self.__account = account

    def get_account(self):
        return self.__account


class UserInfo2(UserInfo):
    pass


if __name__ == '__main__':
    userInfo2 = UserInfo2('两点水', 23, 347073565);
    print(userInfo2.get_account())

