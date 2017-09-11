#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import enum


class User(enum.IntEnum):
    Twowater = 98
    Liangdianshui = 30
    Tom = 12


try:
    print('\n'.join(s.name for s in sorted(User)))
except TypeError as err:
    print(' Error : {}'.format(err))
