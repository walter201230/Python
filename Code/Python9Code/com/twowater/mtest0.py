#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class Test:
    def prt(self):
        print(self)
        print(self.__class__)

t = Test()
t.prt()