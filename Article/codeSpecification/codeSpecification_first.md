# 一、简明概述

## 1、编码

* 如无特殊情况, 文件一律使用 UTF-8 编码
* 如无特殊情况, 文件头部必须加入`#-*-coding:utf-8-*-`标识

## 2、代码格式

### 2.1、缩进

* 统一使用 4 个空格进行缩进

### 2.2、行宽

每行代码尽量不超过 80 个字符(在特殊情况下可以略微超过 80 ，但最长不得超过 120)

理由：

* 这在查看 side-by-side 的 diff 时很有帮助
* 方便在控制台下查看代码
* 太长可能是设计有缺陷

### 2.3、引号

简单说，自然语言使用双引号，机器标示使用单引号，因此 __代码里__ 多数应该使用 __单引号__

 * ***自然语言*** **使用双引号** `"..."`  
   例如错误信息；很多情况还是 unicode，使用`u"你好世界"`
 * ***机器标识*** **使用单引号** `'...'`
   例如 dict 里的 key
 * ***正则表达式*** **使用原生的双引号** `r"..."`
 * ***文档字符串 (docstring)*** **使用三个双引号** `"""......"""`

### 2.4、空行

* 模块级函数和类定义之间空两行；
* 类成员函数之间空一行；

```python
class A:

    def __init__(self):
        pass

    def hello(self):
        pass


def main():
    pass   
```

* 可以使用多个空行分隔多组相关的函数
* 函数中可以使用空行分隔出逻辑相关的代码


## 3、import 语句

* import 语句应该分行书写

```python
# 正确的写法
import os
import sys

# 不推荐的写法
import sys,os

# 正确的写法
from subprocess import Popen, PIPE
```
* import语句应该使用 __absolute__ import

```python
# 正确的写法
from foo.bar import Bar

# 不推荐的写法
from ..bar import Bar
```

* import语句应该放在文件头部，置于模块说明及docstring之后，于全局变量之前；
* import语句应该按照顺序排列，每组之间用一个空行分隔

```python
import os
import sys

import msgpack
import zmq

import foo
```

* 导入其他模块的类定义时，可以使用相对导入

```python
from myclass import MyClass
```

* 如果发生命名冲突，则可使用命名空间

```python
import bar
import foo.bar

bar.Bar()
foo.bar.Bar()
```

## 4、空格

* 在二元运算符两边各空一格`[=,-,+=,==,>,in,is not, and]`:

```python
# 正确的写法
i = i + 1
submitted += 1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)

# 不推荐的写法
i=i+1
submitted +=1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

* 函数的参数列表中，`,`之后要有空格

```python
# 正确的写法
def complex(real, imag):
    pass

# 不推荐的写法
def complex(real,imag):
    pass
```

* 函数的参数列表中，默认值等号两边不要添加空格

```python
# 正确的写法
def complex(real, imag=0.0):
    pass

# 不推荐的写法
def complex(real, imag = 0.0):
    pass
```

* 左括号之后，右括号之前不要加多余的空格

```python
# 正确的写法
spam(ham[1], {eggs: 2})

# 不推荐的写法
spam( ham[1], { eggs : 2 } )
```

* 字典对象的左括号之前不要多余的空格

```python
# 正确的写法
dict['key'] = list[index]

# 不推荐的写法
dict ['key'] = list [index]
```

* 不要为对齐赋值语句而使用的额外空格

```python
# 正确的写法
x = 1
y = 2
long_variable = 3

# 不推荐的写法
x             = 1
y             = 2
long_variable = 3
```

## 5、换行

Python 支持括号内的换行。这时有两种情况。

1) 第二行缩进到括号的起始处

```python
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

2) 第二行缩进 4 个空格，适用于起始括号就换行的情形

```python
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

使用反斜杠`\`换行，二元运算符`+` `.`等应出现在行末；长字符串也可以用此法换行

```python
session.query(MyTable).\
        filter_by(id=1).\
        one()

print 'Hello, '\
      '%s %s!' %\
      ('Harry', 'Potter')
```

禁止复合语句，即一行中包含多个语句：

```python
# 正确的写法
do_first()
do_second()
do_third()

# 不推荐的写法
do_first();do_second();do_third();
```

`if/for/while`一定要换行：

```python
# 正确的写法
if foo == 'blah':
    do_blah_thing()

# 不推荐的写法
if foo == 'blah': do_blash_thing()
```

## 6、docstring
docstring 的规范中最其本的两点：

1. 所有的公共模块、函数、类、方法，都应该写 docstring 。私有方法不一定需要，但应该在 def 后提供一个块注释来说明。
2. docstring 的结束"""应该独占一行，除非此 docstring 只有一行。

```python
"""Return a foobar
Optional plotz says to frobnicate the bizbaz first.
"""

"""Oneline docstring"""
```
