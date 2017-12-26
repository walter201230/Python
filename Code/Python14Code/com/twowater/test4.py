#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

a = 'java*&39android##@@python'

# 数量词

findall = re.findall('[a-z]{4,7}', a)
print(findall)

# 贪婪与非贪婪

re_findall = re.findall('[a-z]{4,7}?', a)
print(re_findall)
