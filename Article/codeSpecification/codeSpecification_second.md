# 二、注释

## 1、注释

### 1.1、块注释
“#”号后空一格，段落件用空行分开（同样需要“#”号）

```python
# 块注释
# 块注释
#
# 块注释
# 块注释
```

### 1.2、行注释
至少使用两个空格和语句分开，注意不要使用无意义的注释

```python
# 正确的写法
x = x + 1  # 边框加粗一个像素

# 不推荐的写法(无意义的注释)
x = x + 1 # x加1
```

### 1.3、建议

* 在代码的关键部分(或比较复杂的地方), 能写注释的要尽量写注释

* 比较重要的注释段, 使用多个等号隔开, 可以更加醒目, 突出重要性

```python
app = create_app(name, options)


# =====================================
# 请勿在此处添加 get post等app路由行为 !!!
# =====================================


if __name__ == '__main__':
    app.run()
```

## 2、文档注释（Docstring）
作为文档的Docstring一般出现在模块头部、函数和类的头部，这样在python中可以通过对象的\_\_doc\_\_对象获取文档.
编辑器和IDE也可以根据Docstring给出自动提示.

* 文档注释以 """ 开头和结尾, 首行不换行, 如有多行, 末行必需换行, 以下是Google的docstring风格示例

```python
# -*- coding: utf-8 -*-
"""Example docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.
"""
```

* 不要在文档注释复制函数定义原型, 而是具体描述其具体内容, 解释具体参数和返回值等

```python
#  不推荐的写法(不要写函数原型等废话)
def function(a, b):
    """function(a, b) -> list"""
    ... ...


#  正确的写法
def function(a, b):
    """计算并返回a到b范围内数据的平均值"""
    ... ...
```

* 对函数参数、返回值等的说明采用numpy标准, 如下所示

```python
def func(arg1, arg2):
    """在这里写函数的一句话总结(如: 计算平均值).

    这里是具体描述.

    参数
    ----------
    arg1 : int
        arg1的具体描述
    arg2 : int
        arg2的具体描述

    返回值
    -------
    int
        返回值的具体描述

    参看
    --------
    otherfunc : 其它关联函数等...

    示例
    --------
    示例使用doctest格式, 在`>>>`后的代码可以被文档测试工具作为测试用例自动运行

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    """
```


* 文档注释不限于中英文, 但不要中英文混用

* 文档注释不是越长越好, 通常一两句话能把情况说清楚即可

* 模块、公有类、公有方法, 能写文档注释的, 应该尽量写文档注释


