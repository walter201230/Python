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

    @classmethod
    def get_name(cls):
        return cls.lv

    @property
    def get_age(self):
        return self._age


if __name__ == '__main__':
    userInfo = UserInfo('两点水', 23, 347073565);
    # 打印所有属性
    print(dir(userInfo))
    # 打印构造函数中的属性
    print(userInfo.__dict__)
    # 直接使用类名类调用，而不是某个对象
    print(UserInfo.lv)
    # 像访问属性一样调用方法（注意看get_age是没有括号的）
    print(userInfo.get_age)
