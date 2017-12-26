#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

a = 'pythonpythonpython'

# 组

findall = re.findall('(python){3}', a)
print(findall)


