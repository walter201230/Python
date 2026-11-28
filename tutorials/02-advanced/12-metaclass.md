# 第 12 章：元类

# 前言 #

Python 界的领袖 Tim Peters 说的：

> 元类就是深度的魔法，99% 的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。


所以，这篇文章，认真阅读一遍就好了。

# 目录 #


这一篇的目录如下：

- 一、Python 中类也是对象
- 二、使用 type() 动态创建类
- 三、什么是元类
- 四、自定义元类
- 五、使用元类

# 一、Python 中类也是对象 #

在了解元类之前，我们先进一步理解 Python 中的类，在大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段。在 Python 中这一点也是一样的。

这点在学习类的章节也强调过了，下面可以通过例子回忆一下：

```python
class ObjectCreator(object):
    pass


mObject = ObjectCreator()
print(mObject)
```

输出结果：

```
<__main__.ObjectCreator object at 0x00000000023EE048>
```

但是，Python 中的类有一点跟大多数的编程语言不同，在 Python 中，可以把类理解成也是一种对象。对的，这里没有写错，就是对象。

为什么呢？

因为只要使用关键字 `class` ，Python 解释器在执行的时候就会创建一个对象。

如：

```python
class ObjectCreator(object):
    pass
```

当程序运行这段代码的时候，就会在内存中创建一个对象，名字就是ObjectCreator。这个对象（类）自身拥有创建对象（类实例）的能力，而这就是为什么它是一个类的原因。

但是，它的本质仍然是一个对象，于是我们可以对它做如下的操作：

```python
class ObjectCreator(object):
    pass


def echo(ob):
    print(ob)


mObject = ObjectCreator()
print(mObject)

# 可以直接打印一个类，因为它其实也是一个对象
print(ObjectCreator)
# 可以直接把一个类作为参数传给函数（注意这里是类，是没有实例化的）
echo(ObjectCreator)
# 也可以直接把类赋值给一个变量
objectCreator = ObjectCreator
print(objectCreator)
```

输出的结果如下：

```
<__main__.ObjectCreator object at 0x000000000240E358>
<class '__main__.ObjectCreator'>
<class '__main__.ObjectCreator'>
<class '__main__.ObjectCreator'>
```

# 二、使用 `type()` 动态创建类 #

因为类也是对象，所以我们可以在程序运行的时候创建类。

Python 是动态语言。

**动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的。**

在之前，我们先了了解下 `type()` 函数。


首先我们新建一个 `hello.py` 的模块，然后定义一个 Hello 的 class ，

```python
class Hello(object):
    def hello(self, name='Py'):
        print('Hello,', name)
```

然后在另一个模块中引用 hello 模块，并输出相应的信息。

其中 `type()` 函数的作用是可以查看一个类型和变量的类型。

<!-- skip-ci -->
```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from com.twowater.hello import Hello

h = Hello()
h.hello()

print(type(Hello))
print(type(h))

```

输出的结果是怎样的呢？

```
Hello, Py
<class 'type'>
<class 'com.twowater.hello.Hello'>
```

上面也提到过，`type()` 函数可以查看一个类型或变量的类型，`Hello` 是一个 `class` ，它的类型就是 `type` ，而 `h` 是一个实例，它的类型就是 `com.twowater.hello.Hello`。

前面的 `com.twowater` 是我的包名，`hello` 模块在该包名下。

在这里还要细想一下，上面的例子中，我们使用 `type()` 函数查看一个类型或者变量的类型。

其中查看了一个 `Hello` class 的类型，打印的结果是： `<class 'type'>` 。

**其实 	`type()` 函数不仅可以返回一个对象的类型，也可以创建出新的类型。**

class 的定义是运行时动态创建的，而创建 class 的方法就是使用 `type()` 函数。

比如我们可以通过 `type()` 函数创建出上面例子中的 `Hello` 类，具体看下面的代码：

```python
# -*- coding: UTF-8 -*-

def printHello(self, name='Py'):
    # 定义一个打印 Hello 的函数
    print('Hello,', name)


# 创建一个 Hello 类
Hello = type('Hello', (object,), dict(hello=printHello))

# 实例化 Hello 类
h = Hello()
# 调用 Hello 类的方法
h.hello()
# 查看 Hello class 的类型
print(type(Hello))
# 查看实例 h 的类型
print(type(h))

```

输出的结果如下：

```
Hello, Py
<class 'type'>
<class '__main__.Hello'>
```

在这里，需先了解下通过 `type()` 函数创建 class 对象的参数说明：

1、class 的名称，比如例子中的起名为 `Hello`

2、继承的父类集合，注意 Python 支持多重继承，如果只有一个父类，tuple 要使用单元素写法；例子中继承 object 类，因为是单元素的 tuple ，所以写成 `(object,)`

3、class 的方法名称与函数绑定；例子中将函数 `printHello` 绑定在方法名 `hello` 中

具体的模式如下：

<!-- skip-ci -->
```python
type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
```

好了，了解完具体的参数使用之外，我们看看输出的结果，可以看到，通过 `type()` 函数创建的类和直接写 class 是完全一样的。

这是因为Python 解释器遇到 class 定义时，仅仅是扫描一下 class 定义的语法，然后调用 `type()` 函数创建出 class 的。

不过一般的情况下，我们都是使用 `class ***...` 的方法来定义类的，不过 `type()` 函数也可以让我们创建出类来。

也就是说，动态语言本身支持运行期动态创建类，这和静态语言有非常大的不同，要在静态语言运行期创建类，必须构造源代码字符串再调用编译器，或者借助一些工具生成字节码实现，本质上都是动态编译，会非常复杂。

**可以看到，在 Python 中，类也是对象，你可以动态的创建类。**

其实这也就是当你使用关键字 class 时 Python 在幕后做的事情，而这就是通过元类来实现的。

# 三、什么是元类 #

通过上面的介绍，终于模模糊糊的带到元类这里来了。可是我们到现在还不知道元类是什么鬼东西。

我们创建类的时候，大多数是为了创建类的实例对象。

那么元类呢？

**元类就是用来创建类的。也可以换个理解方式就是：元类就是类的类。**

通过上面 `type()` 函数的介绍，我们知道可以通过 `type()` 函数创建类：

```python	
MyClass = type('MyClass', (), {})
```

**实际上 `type()` 函数是一个元类。**

`type()` 就是 Python 在背后用来创建所有类的元类。

那么现在我们也可以猜到一下为什么 `type()` 函数是 type 而不是 Type呢？

这可能是为了和 str 保持一致性，str 是用来创建字符串对象的类，而 int 是用来创建整数对象的类。

type 就是创建类对象的类。

你可以通过检查 `__class__` 属性来看到这一点。

Python 中所有的东西，注意喔，这里是说所有的东西，他们都是对象。

这包括整数、字符串、函数以及类。它们全部都是对象，而且它们都是从一个类创建而来。

```python
# 整形
age = 23
print(age.__class__)
# 字符串
name = '两点水'
print(name.__class__)


# 函数
def fu():
    pass


print(fu.__class__)


# 实例
class eat(object):
    pass


mEat = eat()

print(mEat.__class__)
```

输出的结果如下：

```
<class 'int'>
<class 'str'>
<class 'function'>
<class '__main__.eat'>
```

可以看到，上面的所有东西，也就是所有对象都是通过类来创建的，那么我们可能会好奇，`__class__` 的 `__class__` 会是什么呢？

**换个说法就是，创建这些类的类是什么呢？**

我们可以继续在上面的代码基础上新增下面的代码：

<!-- skip-ci -->
```python
print(age.__class__.__class__)
print(name.__class__.__class__)
print(fu.__class__.__class__)
print(mEat.__class__.__class__)
```

输出的结果如下：

```
<class 'type'>
<class 'type'>
<class 'type'>
<class 'type'>
```

认真观察，再理清一下，上面输出的结果是我们把整形 `age` ,字符创 `name` ,函数 `fu` 和对象实例 `mEat` 里  `__class__` 的 `__class__` 打印出来的结果。

也可以说是他们类的类打印结果。发现打印出来的 class 都是 type 。

一开始也提到了，元类就是类的类。

也就是元类就是负责创建类的一种东西。

你也可以理解为，元类就是负责生成类的。

**而 type 就是内建的元类。也就是 Python 自带的元类。**




## 先分清对象与类，再看创建类的工具

这一章容易让人绕进去，因为我们不只在创建实例，还在讨论类本身。先用三个判断把关系摆出来：

```python
StudyRecord = type('StudyRecord', (), {'category': '学习记录'})
record = StudyRecord()
print(type(record) is StudyRecord)
print(type(StudyRecord) is type)
print(record.category)
```

输出：

```text
True
True
学习记录
```

第一行创建一个类，第二行再用这个类创建实例。`type(record)` 观察实例属于什么类，`type(StudyRecord)` 则继续观察类本身的类型。在这个普通例子里，类由 `type` 创建。

自己用 `class StudyRecord:` 写出对应版本，给它同样的 `category`，再比较这三个结果。先把两种创建方式的对应位置看明白，再回看自定义元类在创建过程中的作用。

元类属于进阶内容。初次学习如果暂时用不上，可以完成关系对照后继续后面的课程，带着「创建一个类时还能做什么」这个问题回来。它不是完成普通函数、脚本和综合项目的前提。

# 四、自定义元类 #

到现在，我们已经知道元类是什么鬼东西了。

那么，从始至终我们还不知道元类到底有啥用。

只是了解了一下元类。

在了解它有啥用的时候，我们先来了解下怎么自定义元类。

因为只有了解了怎么自定义才能更好的理解它的作用。

首先我们来了解下 `__metaclass__` 属性

metaclass，直译为元类，简单的解释就是：

当我们定义了类以后，就可以根据这个类创建出实例，所以：先定义类，然后创建实例。

但是如果我们想创建出类呢？

那就必须根据metaclass创建出类，所以：先定义metaclass，然后创建类。

连接起来就是：先定义metaclass，就可以创建类，最后创建实例。

所以，metaclass 允许你创建类或者修改类。

换句话说，你可以把类看成是 metaclass 创建出来的“实例”。

<!-- skip-ci -->
```python
class MyObject(object):
    __metaclass__ = something…
[…]
```

如果是这样写的话，Python 就会用元类来创建类 MyObject。

当你写下 `class MyObject(object)`，但是类对象 MyObject 还没有在内存中创建。P

ython 会在类的定义中寻找 `__metaclass__` 属性，如果找到了，Python 就会用它来创建类 MyObject，如果没有找到，就会用内建的 type 函数来创建这个类。如果还不怎么理解，看下下面的流程图：

![Python 3 的元类选择](../assets/diagrams/metaclass-selection.svg)


再举个实例：

<!-- skip-ci -->
```python
class Foo(Bar):
    pass
```

它的判断流程是怎样的呢？

首先判断 Foo 中是否有 `__metaclass__` 这个属性？如果有，Python 会在内存中通过 `__metaclass__` 创建一个名字为 Foo 的类对象（注意，这里是类对象）。如果 Python 没有找到`__metaclass__` ，它会继续在 Bar（父类）中寻找`__metaclass__` 属性，并尝试做和前面同样的操作。如果 Python在任何父类中都找不到 `__metaclass__` ，它就会在模块层次中去寻找 `__metaclass__` ，并尝试做同样的操作。如果还是找不到` ` `__metaclass__` ,Python 就会用内置的 type 来创建这个类对象。

其实 `__metaclass__` 就是定义了 class 的行为。类似于 class 定义了 instance 的行为，metaclass 则定义了 class 的行为。可以说，class 是 metaclass 的 instance。


现在，我们基本了解了 `__metaclass__` 属性，但是，也没讲过如何使用这个属性，或者说这个属性可以放些什么？

答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到 type 或者子类化 type 的东东都可以。

**元类的主要目的就是为了当创建类时能够自动地改变类。**

通常，你会为API 做这样的事情，你希望可以创建符合当前上下文的类。假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定`__metaclass__` 。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。

幸运的是，`__metaclass__` 实际上可以被任意调用，它并不需要是一个正式的类。所以，我们这里就先以一个简单的函数作为例子开始。

```python
# 元类会自动将你通常传给‘type’的参数作为自己的参数传入
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #  选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
```


<!-- skip-ci -->
```python
# 将它们转为大写形式
uppercase_attr = dict((name.upper(), value) for name, value in attrs)
 
# 通过'type'来做类对象的创建
return type(future_class_name, future_class_parents, uppercase_attr)
 
__metaclass__ = upper_attr  
#  这会作用到这个模块中的所有类
 
class Foo(object):
    # 我们也可以只在这里定义__metaclass__，这样就只会作用于这个类中
    bar = 'bip'
```

<!-- skip-ci -->
```python
print hasattr(Foo, 'bar')
# 输出: False
print hasattr(Foo, 'BAR')
# 输出:True
 
f = Foo()
print f.BAR
# 输出:'bip'
```

用 class 当做元类的做法：

```python
# 请记住，'type'实际上是一个类，就像'str'和'int'一样
# 所以，你可以从type继承
class UpperAttrMetaClass(type):
    # __new__ 是在__init__之前被调用的特殊方法
    # __new__是用来创建对象并返回之的方法
    # 而__init__只是用来将传入的参数初始化给对象
    # 你很少用到__new__，除非你希望能够控制对象的创建
    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type(future_class_name, future_class_parents, uppercase_attr)

```

但是，这种方式其实不是 OOP。我们直接调用了 type，而且我们没有改写父类的 `__new__` 方法。现在让我们这样去处理:

```python

class UpperAttrMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
 
        # 复用type.__new__方法
        # 这就是基本的OOP编程，没什么魔法
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)
```

你可能已经注意到了有个额外的参数 `upperattr_metaclass` ，这并没有什么特别的。类方法的第一个参数总是表示当前的实例，就像在普通的类方法中的 self 参数一样。当然了，为了清晰起见，这里的名字我起的比较长。但是就像 self 一样，所有的参数都有它们的传统名称。因此，在真实的产品代码中一个元类应该是像这样的：

<!-- skip-ci -->
```python
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
        uppercase_attr  = dict((name.upper(), value) for name, value in attrs)
        return type.__new__(cls, name, bases, uppercase_attr)

```

如果使用 super 方法的话，我们还可以使它变得更清晰一些，这会缓解继承（是的，你可以拥有元类，从元类继承，从 type 继承）

```python
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)
```

通常我们都会使用元类去做一些晦涩的事情，依赖于自省，控制继承等等。确实，用元类来搞些“黑暗魔法”是特别有用的，因而会搞出些复杂的东西来。但就元类本身而言，它们其实是很简单的：

* 拦截类的创建
* 修改类
* 返回修改之后的类

# 五、使用元类 #

终于到了使用元类了，可是一般来说，我们根本就用不上它，就像Python 界的领袖 Tim Peters 说的：

> 元类就是深度的魔法，99% 的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。

元类的主要用途是创建 API。一个典型的例子是 Django ORM。它允许你像这样定义：

<!-- skip-ci -->
```python
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

但是如果你这样做的话：

<!-- skip-ci -->
```python
guy  = Person(name='bob', age='35')
print guy.age
```

这并不会返回一个 IntegerField 对象，而是会返回一个 int，甚至可以直接从数据库中取出数据。

这是有可能的，因为 models.Model 定义了 `__metaclass__` ， 并且使用了一些魔法能够将你刚刚定义的简单的Person类转变成对数据库的一个复杂 hook。

Django 框架将这些看起来很复杂的东西通过暴露出一个简单的使用元类的 API 将其化简，通过这个 API 重新创建代码，在背后完成真正的工作。

Python 中的一切都是对象，它们要么是类的实例，要么是元类的实例，除了 type。type 实际上是它自己的元类，在纯 Python 环境中这可不是你能够做到的，这是通过在实现层面耍一些小手段做到的。

参考：

[https://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python](https://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python)
