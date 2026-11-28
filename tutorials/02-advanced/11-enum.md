# 第 11 章：枚举类

# 前言 #

2019年10月14日16:59:38 看了一下，还有五个章节就修改完基础部分了。

干就完事了。

# 目录 #


这一篇的目录如下：

- 一、枚举类的使用
- 二、Enum 的源码
- 三、自定义类型的枚举
- 四、枚举的比较

# 一、枚举类的使用 #

实际开发中，我们离不开定义常量，当我们需要定义常量时，其中一个办法是用大写变量通过整数来定义，例如月份：

```python
JAN = 1
FEB = 2
MAR = 3
...
NOV = 11
DEC = 12
```

当然这样做简单快捷，缺点是类型是 `int` ，并且仍然是变量。

那有没有什么好的方法呢？

这时候我们定义一个 class 类型，每个常量都是 class 里面唯一的实例。

正好 Python 提供了 Enum 类来实现这个功能如下：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

# 遍历枚举类型
for name, member in Month.__members__.items():
    print(name, '---------', member, '----------', member.value)

# 直接引用一个常量
print('\n', Month.Jan)

```

输出的结果如下：


```
Jan --------- Month.Jan --------- 1
Feb --------- Month.Feb --------- 2
Mar --------- Month.Mar --------- 3
Apr --------- Month.Apr --------- 4
May --------- Month.May --------- 5
Jun --------- Month.Jun --------- 6
Jul --------- Month.Jul --------- 7
Aug --------- Month.Aug --------- 8
Sep --------- Month.Sep --------- 9
Oct --------- Month.Oct --------- 10
Nov --------- Month.Nov --------- 11
Dec --------- Month.Dec --------- 12

 Month.Jan
```

我们使用 `Enum` 来定义了一个枚举类。

上面的代码，我们创建了一个有关月份的枚举类型 Month ，这里要注意的是构造参数，第一个参数 Month 表示的是该枚举类的类名，第二个 tuple 参数，表示的是枚举类的值；当然，枚举类通过 `__members__` 遍历它的所有成员的方法。

注意的一点是 ， `member.value` 是自动赋给成员的 `int` 类型的常量，默认是从 1 开始的。

**而且 Enum 的成员均为单例（Singleton），并且不可实例化，不可更改**





## 状态的名字和状态的值

我们想给学习任务标上「待学习」或「已完成」。用枚举把允许的状态列清楚，再分开观察成员名和值：

```python
from enum import Enum


class StudyState(Enum):
    TODO = '待学习'
    DONE = '已完成'


print(StudyState.TODO.name)
print(StudyState.TODO.value)
print(StudyState('已完成') is StudyState.DONE)
```

输出：

```text
TODO
待学习
True
```

`TODO` 是成员的名称，`'待学习'` 是这里给它安排的值。`StudyState('已完成')` 按值寻找成员，不是在创建一个任意内容的新状态。

自己试试一个没有定义过的值，观察 `ValueError`；再比较 `StudyState.TODO == '待学习'`，结果为 `False`，因为这里的普通 `Enum` 成员和它的字符串值不是同一个东西。不同枚举类型的比较规则要看对应类型，不从这个例子推导所有枚举都和字符串一样。

本章的源码分析可以帮助理解实现，但完成一个状态选择的小需求后再回看，通常更容易知道自己在追哪一段逻辑。

# 二、Enum 的源码 #

通过上面的实例可以知道通过 `__members__`  可以遍历枚举类的所有成员。

那有没有想过为什么呢？

当你看到那段代码的时候，有没有想过为什么通过  `__members__`  就能遍历枚举类型的所有成员出来？


我们可以先来大致看看 Enum 的源码是如何实现的；

Enum 在模块 enum.py 中，先来看看 Enum 类的片段

<!-- skip-ci -->
```python
class Enum(metaclass=EnumMeta):
    """Generic enumeration.
    Derive from this class to define new enumerations.
    """
```

可以看到，Enum 是继承元类 EnumMeta 的；再看看 EnumMeta 的相关片段

```python
class EnumMeta(type):
    """Metaclass for Enum"""
    @property
    def __members__(cls):
        """Returns a mapping of member name->value.
        This mapping lists all enum members, including aliases. Note that this
        is a read-only view of the internal mapping.
        """
        return MappingProxyType(cls._member_map_)
```

首先 `__members__` 方法返回的是一个包含一个 Dict 既 Map 的 MappingProxyType，并且通过 @property 将方法 `__members__(cls)` 的访问方式改变为了变量的的形式，那么就可以直接通过 `__members__` 来进行访问了

# 三、自定义类型的枚举 #

但有些时候我们需要控制枚举的类型，那么我们可以 Enum 派生出自定义类来满足这种需要。通过修改上面的例子：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from enum import Enum, unique

Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))


# @unique 装饰器可以帮助我们检查保证没有重复值
@unique
class Month(Enum):
    Jan = 'January'
    Feb = 'February'
    Mar = 'March'
    Apr = 'April'
    May = 'May'
    Jun = 'June'
    Jul = 'July'
    Aug = 'August'
    Sep = 'September '
    Oct = 'October'
    Nov = 'November'
    Dec = 'December'


if __name__ == '__main__':
    print(Month.Jan, '----------',
          Month.Jan.name, '----------', Month.Jan.value)
    for name, member in Month.__members__.items():
        print(name, '----------', member, '----------', member.value)

```


输出的结果如下：

```
Month.Jan ---------- Jan ---------- January
Jan ---------- Month.Jan ---------- January
Feb ---------- Month.Feb ---------- February
Mar ---------- Month.Mar ---------- March
Apr ---------- Month.Apr ---------- April
May ---------- Month.May ---------- May
Jun ---------- Month.Jun ---------- June
Jul ---------- Month.Jul ---------- July
Aug ---------- Month.Aug ---------- August
Sep ---------- Month.Sep ---------- September
Oct ---------- Month.Oct ---------- October
Nov ---------- Month.Nov ---------- November
Dec ---------- Month.Dec ---------- December
```



通过上面的例子，可以知道枚举模块定义了具有迭代 (interator) 和比较(comparison) 功能的枚举类型。 它可以用来为值创建明确定义的符号，而不是使用具体的整数或字符串。

# 四、枚举的比较 #

因为枚举成员不是有序的，所以它们只支持通过标识(identity) 和相等性 (equality) 进行比较。下面来看看 `==` 和 `is` 的使用：

```python

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
    print(f' Error : {err}')

```

输出的结果：

```txt

False True
False True
 Error : '<' not supported between instances of 'User' and 'User'

```

可以看看最后的输出结果，报了个异常，那是因为大于和小于比较运算符引发 TypeError 异常。也就是 `Enum` 类的枚举是不支持大小运算符的比较的。

那么能不能让枚举类进行大小的比较呢？

当然是可以的，使用 IntEnum 类进行枚举，就支持比较功能。

```python
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
    print(f' Error : {err}')


```

看看输出的结果：

```txt
Tom
Liangdianshui
Twowater
```

通过输出的结果可以看到，枚举类的成员通过其值得大小进行了排序。也就是说可以进行大小的比较。
