#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

# 设定一个常量
a = '两点水|twowater|liangdianshui|草根程序员|ReadingWithU'

# 判断是否有 “两点水” 这个字符串，使用 PY 自带函数

print('a 是否含有“两点水”这个字符串：{0}'.format(a.index('两点水') > -1))
print('a 是否含有“两点水”这个字符串：{0}'.format('两点水' in a))

# 正则表达式

findall = re.findall('两点水', a)
print(findall)

if len(findall) > 0:
    print('a 含有“两点水”这个字符串')
else:
    print('a 不含有“两点水”这个字符串')

# 选择 a 里面的所有小写英文字母

re_findall = re.findall('[a-z]', a)

print(re_findall)
