#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User1(object):
    pass


class User2(User1):
    pass


class User3(User2):
    pass


if __name__ == '__main__':
    user1 = User1()
    user2 = User2()
    user3 = User3()
    # isinstance()就可以告诉我们，一个对象是否是某种类型
    print(isinstance(user3, User2))
    print(isinstance(user3, User1))
    print(isinstance(user3, User3))
    # 基本类型也可以用isinstance()判断
    print(isinstance('两点水', str))
    print(isinstance(347073565, int))
    print(isinstance(347073565, str))
