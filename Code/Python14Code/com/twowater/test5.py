#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

a = '347073565'

# 边界匹配符

findall = re.findall('\d{6}565$', a)

print(findall)
