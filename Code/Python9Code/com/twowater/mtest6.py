#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class UserInfo(object):
    lv = 5

    def __init__(self, name, age, account):
        self.name = name
        self._age = age
        self.__account = account

    def get_account(self):
        return self.__account

    @classmethod
    def get_name(cls):
        return cls.lv

    @property
    def get_age(self):
        return self._age


class UserInfo2(UserInfo):
    def __init__(self, name, age, account, sex):
        super(UserInfo2, self).__init__(name, age, account)
        self.sex = sex;


if __name__ == '__main__':
    userInfo2 = UserInfo2('两点水', 23, 347073565, '男');
    # 打印所有属性
    print(dir(userInfo2))
    # 打印构造函数中的属性
    print(userInfo2.__dict__)
    print(UserInfo2.get_name())
