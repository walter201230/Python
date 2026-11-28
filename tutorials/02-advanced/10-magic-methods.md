# 第 10 章：Python 的 Magic Method

# 前言 #

有时候修改文章，真的修改到想死。真的很耗时间，很烦的。

好吧，每次都是安慰自己，快完结了，快更新完了。

# 目录 #


这一篇的目录如下：

- 一、Python 的 Magic Method
- 二、构造（`__new__`）和初始化（`__init__`）
- 三、属性的访问控制
- 四、对象的描述器
- 五、自定义容器（Container）
- 六、运算符相关的魔术方法
    - 1、比较运算符
    - 2、算术运算符

# 一、Python 的 Magic Method #

在 Python 中，所有以 "__" 双下划线包起来的方法，都统称为"魔术方法"。比如我们接触最多的 `__init__` 。

魔术方法有什么作用呢？

使用这些魔术方法，我们可以构造出优美的代码，将复杂的逻辑封装成简单的方法。

那么一个类中有哪些魔术方法呢？

我们可以使用 Python 内置的方法 `dir()` 来列出类中所有的魔术方法.示例如下：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    pass


if __name__ == '__main__':
    print(dir(User()))
```

输出的结果：

```
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
```

可以看到，一个类的魔术方法还是挺多的，不过我们只需要了解一些常见和常用的魔术方法就好了。





## 先选一种希望对象支持的操作

魔法方法不必一口气背完。假设我们希望用 `len()` 看一份记录有几条，先围绕这个需求写最少的代码：

```python
class Logbook:
    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)


book = Logbook()
print(len(book), bool(book))
book.records.append(15)
print(len(book), bool(book))
```

输出：

```text
0 False
1 True
```

我们只实现了 `__len__`。没有单独定义 `__bool__` 时，对象的真假判断可以使用长度，因此空记录为假，有一条记录时为真。这里的协议对应关系，比记住一串双下划线名称更重要。

自己再加两条记录，检查长度是不是 `3`。然后想一下：如果需求只是保存一组分钟数，普通列表是否已经足够？自定义类的价值应该来自确实需要的行为，而不是为了用上所有魔法方法。

前面的描述器、属性访问等部分可以在需要时反复阅读。初次学到这里，先能说明一种普通操作怎样触发自己定义的方法，再逐步深入。

# 二、构造(`__new__`)和初始化(`__init__`) #

通过之前的学习，我们已经知道定义一个类时，我们经常会通过 `__init__(self)` 的方法在实例化对象的时候，对属性进行设置。

比如下面的例子：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __init__(self, name, age):
        self.name = name;
        self.age = age;

user=User('两点水',23)
```

实际上，创建一个类的过程是分为两步的，一步是创建类的对象，还有一步就是对类进行初始化。

`__new__` 是用来创建类并返回这个类的实例, 而`__init__` 只是将传入的参数来初始化该实例.`__new__` 在创建一个实例的过程中必定会被调用,但 `__init__` 就不一定，比如通过 pickle.load 的方式反序列化一个实例时就不会调用 `__init__` 方法。

![实例的创建与初始化](../assets/diagrams/instance-creation.svg)

`def __new__(cls)` 是在 `def __init__(self)` 方法之前调用的，作用是返回一个实例对象。还有一点需要注意的是：`__new__` 方法总是需要返回该类的一个实例，而 `__init__`  不能返回除了 `None` 的任何值

> 这里还有一个边界：`__new__` 也可以返回其他类型的对象；返回值不是当前类的实例时，不会继续调用当前类的 `__init__`。通常创建当前类实例时，才按前面介绍的两步理解。

具体的示例：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __new__(cls, *args, **kwargs):
        # 打印 __new__方法中的相关信息
        print('调用了 def __new__ 方法')
        print(args)
        # 最后返回父类的方法
        return super(User, cls).__new__(cls)

    def __init__(self, name, age):
        print('调用了 def __init__ 方法')
        self.name = name
        self.age = age


if __name__ == '__main__':
    usr = User('两点水', 23)
```

看看输出的结果：

```txt
调用了 def __new__ 方法
('两点水', 23)
调用了 def __init__ 方法
```

通过打印的结果来看，我们就可以知道一个类创建的过程是怎样的了，先是调用了 `__new__` 方法来创建一个对象，把参数传给 `__init__` 方法进行实例化。

其实在实际开发中，很少会用到 `__new__` 方法，除非你希望能够控制类的创建。通常讲到 `__new__` ，都是牵扯到 `metaclass`(元类)的。

当然当一个对象的生命周期结束的时候，析构函数 `__del__` 方法会被调用。但是这个方法是 Python 自己对对象进行垃圾回收的。

# 三、属性的访问控制 #

之前也有讲到过，Python 没有真正意义上的私有属性。然后这就导致了对 Python 类的封装性比较差。我们有时候会希望 Python 能够定义私有属性，然后提供公共可访问的 get 方法和 set 方法。Python 其实可以通过魔术方法来实现封装。

|方法|说明|
| ---| --- |
|`__getattr__(self, name)`|该方法定义了你试图访问一个不存在的属性时的行为。因此，重载该方法可以实现捕获错误拼写然后进行重定向, 或者对一些废弃的属性进行警告。|
|`__setattr__(self, name, value)`|定义了对属性进行赋值和修改操作时的行为。不管对象的某个属性是否存在,都允许为该属性进行赋值.有一点需要注意，实现 `__setattr__` 时要避免"无限递归"的错误，|
|`__delattr__(self, name)`|`__delattr__` 与 `__setattr__` 很像，只是它定义的是你删除属性时的行为。实现 `__delattr__` 是同时要避免"无限递归"的错误|
|`__getattribute__(self, name)`|`__getattribute__` 定义了你的属性被访问时的行为，相比较，`__getattr__` 只有该属性不存在时才会起作用。因此，在支持 `__getattribute__ `的 Python 版本,调用`__getattr__` 前必定会调用 `__getattribute__``__getattribute__` 同样要避免"无限递归"的错误。|

通过上面的方法表可以知道，在进行属性访问控制定义的时候你可能会很容易的引起一个错误，可以看看下面的示例：

```python
def __setattr__(self, name, value):
    self.name = value
    # 每当属性被赋值的时候， ``__setattr__()`` 会被调用，这样就造成了递归调用。
    # 这意味这会调用 ``self.__setattr__('name', value)`` ，每次方法会调用自己。这样会造成程序崩溃。

def __setattr__(self, name, value):
    # 给类中的属性名分配值
    self.__dict__[name] = value  
    # 定制特有属性
```

上面方法的调用具体示例如下：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __getattr__(self, name):
        print('调用了 __getattr__ 方法')
        return super(User, self).__getattr__(name)

    def __setattr__(self, name, value):
        print('调用了 __setattr__ 方法')
        return super(User, self).__setattr__(name, value)

    def __delattr__(self, name):
        print('调用了 __delattr__ 方法')
        return super(User, self).__delattr__(name)

    def __getattribute__(self, name):
        print('调用了 __getattribute__ 方法')
        return super(User, self).__getattribute__(name)


if __name__ == '__main__':
    user = User()
    # 设置属性值，会调用 __setattr__
    user.attr1 = True
    # 属性存在,只有__getattribute__调用
    user.attr1
    try:
        # 属性不存在, 先调用__getattribute__, 后调用__getattr__
        user.attr2
    except AttributeError:
        pass
    # __delattr__调用
    del user.attr1

```

输出的结果：

```txt
调用了 __setattr__ 方法
调用了 __getattribute__ 方法
调用了 __getattribute__ 方法
调用了 __getattr__ 方法
调用了 __delattr__ 方法
```

# 四、对象的描述器 #

一般来说，一个描述器是一个有“绑定行为”的对象属性 (object attribute)，它的访问控制被描述器协议方法重写。

这些方法是 `__get__()`, `__set__()` , 和 `__delete__()`  。

有这些方法的对象叫做描述器。

默认对属性的访问控制是从对象的字典里面 (`__dict__`) 中获取 (get) , 设置 (set) 和删除 (delete) 。

举例来说， `a.x` 的查找顺序是, `a.__dict__['x']` , 然后 `type(a).__dict__['x']` , 然后找 `type(a)` 的父类 ( 不包括元类 (metaclass) ).如果查找到的值是一个描述器, Python 就会调用描述器的方法来重写默认的控制行为。

这个重写发生在这个查找环节的哪里取决于定义了哪个描述器方法。

注意, 只有在新式类中时描述器才会起作用。在之前的篇节中已经提到新式类和旧式类的，有兴趣可以查看之前的篇节来看看，至于新式类最大的特点就是所有类都继承自 type 或者 object 的类。

在面向对象编程时，如果一个类的属性有相互依赖的关系时，使用描述器来编写代码可以很巧妙的组织逻辑。在 Django 的 ORM 中,models.Model 中的 InterField 等字段, 就是通过描述器来实现功能的。

我们先看下下面的例子：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __init__(self, name='两点水', sex='男'):
        self.sex = sex
        self.name = name

    def __get__(self, obj, objtype):
        print('获取 name 值')
        return self.name

    def __set__(self, obj, val):
        print('设置 name 值')
        self.name = val


class MyClass(object):
    x = User('两点水', '男')
    y = 5


if __name__ == '__main__':
    m = MyClass()
    print(m.x)

    print('\n')

    m.x = '三点水'
    print(m.x)

    print('\n')

    print(m.x)

    print('\n')

    print(m.y)

```

输出的结果如下：

```txt
获取 name 值
两点水


设置 name 值
获取 name 值
三点水


获取 name 值
三点水


5

```

通过这个例子，可以很好的观察到这 `__get__()` 和  `__set__()` 这些方法的调用。

再看一个经典的例子

我们知道，距离既可以用单位"米"表示,也可以用单位"英尺"表示。
现在我们定义一个类来表示距离,它有两个属性: 米和英尺。

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class Meter(object):
    def __init__(self, value=0.0):
        self.value = float(value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = float(value)


class Foot(object):
    def __get__(self, instance, owner):
        return instance.meter * 3.2808

    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808


class Distance(object):
    meter = Meter()
    foot = Foot()


if __name__ == '__main__':
    d = Distance()
    print(d.meter, d.foot)
    d.meter = 1
    print(d.meter, d.foot)
    d.meter = 2
    print(d.meter, d.foot)

```
 
输出的结果：

```txt
0.0 0.0
1.0 3.2808
2.0 6.5616
```

在上面例子中,在还没有对 Distance 的实例赋值前, 我们认为 meter 和 foot 应该是各自类的实例对象, 但是输出却是数值。这是因为 `__get__` 发挥了作用.

我们只是修改了 meter ,并且将其赋值成为 int ，但 foot 也修改了。这是 `__set__` 发挥了作用.

描述器对象 (Meter、Foot) 不能独立存在, 它需要被另一个所有者类 (Distance) 所持有。描述器对象可以访问到其拥有者实例的属性，比如例子中 Foot 的 `instance.meter` 。

# 五、自定义容器（Container） #

经过之前编章的介绍，我们知道在 Python 中，常见的容器类型有: dict, tuple, list, string。其中也提到过可容器和不可变容器的概念。其中 tuple, string 是不可变容器，dict, list 是可变容器。

可变容器和不可变容器的区别在于，不可变容器一旦赋值后，不可对其中的某个元素进行修改。当然具体的介绍，可以看回之前的文章，有图文介绍。

那么这里先提出一个问题，这些数据结构就够我们开发使用吗？

不够的时候，或者说有些特殊的需求不能单单只使用这些基本的容器解决的时候，该怎么办呢？

这个时候就需要自定义容器了，那么具体我们该怎么做呢？

|功能|说明|
|------|------|
|自定义不可变容器类型|需要定义 `__len__` 和 `__getitem__` 方法|
|自定义可变类型容器|在不可变容器类型的基础上增加定义 `__setitem__` 和 `__delitem__` |
|自定义的数据类型需要迭代|需定义 `__iter__` |
|返回自定义容器的长度|需实现 `__len__(self)` |
|自定义容器可以调用 `self[key]` ，如果 key 类型错误，抛出TypeError ，如果没法返回key对应的数值时,该方法应该抛出ValueError|需要实现 `__getitem__(self, key)`|
|当执行 	`self[key] = value` 时|调用是 `__setitem__(self, key, value)`这个方法|
|当执行 `del self[key]` 方法 |其实调用的方法是 `__delitem__(self, key)`|
|当你想你的容器可以执行 `for x in container:` 或者使用 `iter(container)` 时|需要实现 `__iter__(self)` ，该方法返回的是一个迭代器|

来看一下使用上面魔术方法实现 Haskell 语言中的一个数据结构：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class FunctionalList:
    ''' 实现了内置类型list的功能,并丰富了一些其他方法: head, tail, init, last, drop, take'''

    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return FunctionalList(reversed(self.values))

    def append(self, value):
        self.values.append(value)

    def head(self):
        # 获取第一个元素
        return self.values[0]

    def tail(self):
        # 获取第一个元素之后的所有元素
        return self.values[1:]

    def init(self):
        # 获取最后一个元素之前的所有元素
        return self.values[:-1]

    def last(self):
        # 获取最后一个元素
        return self.values[-1]

    def drop(self, n):
        # 获取所有元素，除了前N个
        return self.values[n:]

    def take(self, n):
        # 获取前N个元素
        return self.values[:n]

```

# 六、运算符相关的魔术方法 #


运算符相关的魔术方法实在太多了,j就大概列举下面两类：


## 1、比较运算符 ##

|魔术方法|说明|
|-----|-----|
|`__cmp__(self, other)`|如果该方法返回负数，说明 `self < other`;  返回正数，说明 `self > other`; 返回 0 说明 `self == other `。强烈不推荐来定义 `__cmp__` , 取而代之, 最好分别定义 `__lt__`, `__eq__` 等方法从而实现比较功能。 `__cmp__` 在 Python3 中被废弃了。|
|`__eq__(self, other)`|定义了比较操作符 == 的行为|
|`__ne__(self, other)`|定义了比较操作符 != 的行为|
|`__lt__(self, other)`|定义了比较操作符 < 的行为|
|`__gt__(self, other)`|定义了比较操作符 > 的行为|
|`__le__(self, other)`|定义了比较操作符 <= 的行为|
|`__ge__(self, other)`|定义了比较操作符 >= 的行为|


来看个简单的例子就能理解了：

> 观察下面标为 `num1 != num2` 的打印：花括号中实际仍写着 `num1 == num2`，所以当前代码调用的是 `__eq__`。若要验证不等于，应把该表达式写成 `num1 != num2`，这时会调用 `__ne__`，得到 `True`。

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class Number(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        print('__eq__')
        return self.value == other.value

    def __ne__(self, other):
        print('__ne__')
        return self.value != other.value

    def __lt__(self, other):
        print('__lt__')
        return self.value < other.value

    def __gt__(self, other):
        print('__gt__')
        return self.value > other.value

    def __le__(self, other):
        print('__le__')
        return self.value <= other.value

    def __ge__(self, other):
        print('__ge__')
        return self.value >= other.value


if __name__ == '__main__':
    num1 = Number(2)
    num2 = Number(3)
    print(f'num1 == num2 ? --------> {num1 == num2} \n')
    print(f'num1 != num2 ? --------> {num1 == num2} \n')
    print(f'num1 < num2 ? --------> {num1 < num2} \n')
    print(f'num1 > num2 ? --------> {num1 > num2} \n')
    print(f'num1 <= num2 ? --------> {num1 <= num2} \n')
    print(f'num1 >= num2 ? --------> {num1 >= num2} \n')

```

输出的结果为：

```txt
__eq__
num1 == num2 ? --------> False

__eq__
num1 != num2 ? --------> False

__lt__
num1 < num2 ? --------> True

__gt__
num1 > num2 ? --------> False

__le__
num1 <= num2 ? --------> True

__ge__
num1 >= num2 ? --------> False

```

## 2、算术运算符 ##

|魔术方法|说明|
|-----|-----|
|`__add__(self, other)`|实现了加号运算|
|`__sub__(self, other)`|实现了减号运算|
|`__mul__(self, other)`|实现了乘法运算|
|`__floordiv__(self, other)`|实现了 // 运算符|
|`___div__(self, other)`|实现了/运算符. 该方法在 Python3 中废弃. 原因是 Python3 中，division 默认就是 true division|
|`__truediv__(self, other)`|实现了 true division. Python 3 中 `/` 默认即为 true division，无需再 `from __future__ import division`|
|`__mod__(self, other)`|实现了 % 运算符, 取余运算|
|`__divmod__(self, other)`|实现了 divmod() 內建函数|
|`__pow__(self, other)`|实现了 `**` 操作. N 次方操作|
|`__lshift__(self, other)`|实现了位操作 `<<`|
|`__rshift__(self, other)`|实现了位操作 `>>`|
|`__and__(self, other)`|实现了位操作 `&`|
|`__or__(self, other)`|实现了位操作 `|`|
|`__xor__(self, other)`|实现了位操作 `^`|
