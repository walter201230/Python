#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __init__(self, name):
        self.name = name

    def printUser(self):
        print('Hello !' + self.name)


class UserVip(User):
    def printUser(self):
        print('Hello ! 尊敬的Vip用户：' + self.name)


class UserGeneral(User):
    def printUser(self):
        print('Hello ! 尊敬的用户：' + self.name)


def printUserInfo(user):
    user.printUser()


if __name__ == '__main__':
    userVip = UserVip('两点水')
    printUserInfo(userVip)
    userGeneral = UserGeneral('水水水')
    printUserInfo(userGeneral)
