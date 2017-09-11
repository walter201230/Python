#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from enum import Enum


class User(Enum):
    Twowater = 98
    Liangdianshui = 30
    Tom = 12


Twowater = User.Twowater
Liangdianshui = User.Liangdianshui

print(Twowater == Liangdianshui, Twowater == User.Twowater)
print(Twowater is Liangdianshui, Twowater is User.Twowater)

try:
    print('\n'.join('  ' + s.name for s in sorted(User)))
except TypeError as err:
    print(' Error : {}'.format(err))
