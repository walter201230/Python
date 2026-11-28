# 第 8 章：面向对象

# 前言 #


之前的文章都是使用 [Sublime Text](http://www.sublimetext.com/) 来编写 Python 的，主要是为了更好地熟悉和了解 Python；从这章开始，改用 PyCharm 了。前面 [集成开发环境（IDE）：PyCharm](01-hello-world.md) 一节已经介绍过 PyCharm 的安装和使用，需要的话可以回看。


这篇内容非常的重要，也是我用了很多时间写的。基本上把以前写的东西都重新改了一遍。里面的代码都是我一个一个的敲的，图片也是我一个一个制作的。




# 目录 #

- 面向对象的概念
- 类的定义和调用
- 类方法
- 修改和增加类属性
- 类和对象
- 初始化函数
- 类的继承
- 类的多态
- 类的访问控制

# 一、面向对象的概念 #



## 1、面向对象的两个基本概念 ##

编程语言中，一般有两种编程思维，面向过程和面向对象。

面向过程，看重的是解决问题的过程。

这好比我们解决日常生活问题差不多，分析解决问题的步骤，然后一步一步的解决。

而面向对象是一种抽象，抽象是指用分类的眼光去看世界的一种方法。

Python 就是一门面向对象的语言, 

如果你学过 Java ，就知道 Java 的编程思想就是：万事万物皆对象。Python 也不例外，在解决实际问题的过程中，可以把构成问题事务分解成各个对象。

面向对象都有两个基本的概念，分别是类和对象。

* **类**

用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。

* **对象**

通过类定义的数据结构实例





## 2、面向对象的三大特性 ##

面向对象的编程语言，也有三大特性，继承，多态和封装性。

* **继承**

即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。

例如：一个 Dog 类型的对象派生自 Animal 类，这是模拟"是一个（is-a）"关系（例图，Dog 是一个 Animal ）。

* **多态**

它是指对不同类型的变量进行相同的操作，它会根据对象（或类）类型的不同而表现出不同的行为。

* **封装性**

“封装”就是将抽象得到的数据和行为（或功能）相结合，形成一个有机的整体（即类）；封装的目的是增强安全性和简化编程，使用者不必了解具体的实现细节，而只是要通过外部接口，一特定的访问权限来使用类的成员。


**如果你是初次接触面向对象的编程语言，看到这里还一脸懵逼，不要紧，这是正常的。下面我们会通过大量的例子逐步了解 Python 的面向对象的知识。**

# 二、类的定义和调用 #



## 1、怎么理解类？ ##

类是什么？

个人认为理解类，最简单的方式就是：类是一个变量和函数的集合。

可以看下下面的这张图。

![类的结构](../assets/diagrams/class-structure.svg)

这张图很好的诠释了类，就是把变量和函数包装在一起。

当然我们包装也不是毫无目的的包装，我们会把同性质的包装在一个类里，这样就方便我们重复使用。

所以学到现在，你会发现很多编程的设计，都是为了我们能偷懒，重复使用。






## 2、怎么定义类 ##

知道了类是什么样子的，我们接下来就要学习怎么去定义类了。

类定义语法格式如下：

<!-- skip-ci -->
```python
class ClassName():
    <statement-1>
    .
    .
    .
    <statement-N>
```

可以看到，我们是用 `class` 语句来自定义一个类的，其实这就好比我们是用 `def` 语句来定义一个函数一样。

竟然说类是变量和方法的集合包，那么我们来创建一个类。

```python
class ClassA():
    var1 = 100
    var2 = 0.01
    var3 = '两点水'

    def fun1():
        print('我是 fun1')

    def fun2():
        print('我是 fun1')

    def fun3():
        print('我是 fun1')
```

你看，上面我们就定义了一个类，类名叫做 `ClassA` , 类里面的变量我们称之为属性，那么就是这个类里面有 3 个属性，分别是 `var1` , `var2` 和 `var3` 。除此之外，类里面还有 3 个类方法 `fun1()` , `fun2()` 和 `fun3()` 。





## 3、怎么调用类属性和类方法 ##


我们定义了类之后，那么我们怎么调用类里面的属性和方法呢？

直接看下图：

**类属性和方法的调用**

- 类里面的变量叫 [属性] —— 调用格式：`类.变量`
- 类里面的函数叫 [方法] —— 调用格式：`类.函数()`

这里就不文字解释了（注：做图也不容易啊，只有写过技术文章才知道，这系列文章，多耗时）

好了，知道怎么调用之后，我们尝试一下：


```python
class ClassA():
    var1 = 100
    var2 = 0.01
    var3 = '两点水'

    def fun1():
        print('我是 fun1')

    def fun2():
        print('我是 fun1')

    def fun3():
        print('我是 fun1')


print(ClassA.var1)
print(ClassA.var2)
print(ClassA.var3)
ClassA.fun1()
ClassA.fun2()
ClassA.fun3()
```

输出结果如下：

```
100
0.01
两点水
我是 fun1
我是 fun1
我是 fun1
```

# 三、类方法 #


## 1、类方法如何调用类属性 ##

通过上面我们已经会定义类了，那么这里讲一下在同一个类里，类方法如何调用类属性的。

直接看个例子吧：


```python
class ClassA():
    var1 = '两点水'

    @classmethod
    def fun1(cls):
        print('我是 fun1' + cls.var1)


ClassA.fun1()
```

输出结果如下：

```
我是 fun1两点水
```

注意看，在类方法上面多了个 `@classmethod` ，这是干嘛用的呢？

这是用于声明下面的函数是类函数。其实从名字就很好理解了。

class 就是类，method 就是方法。

那是不是一定需要注明这个呢？

答案是是的。

如果你没使用，是会报错的。


<!-- skip-ci -->
```python
class ClassA():
    var1 = '两点水'

    def fun1(cls):
        print('我是 fun1' + cls.var1)


ClassA.fun1()
```

报错如下：

```
Traceback (most recent call last):
  File "/Users/twowater/dev/python/test/com/twowater/test.py", line 10, in <module>
    ClassA.fun1()
TypeError: fun1() missing 1 required positional argument: 'cls'
```

如果没有声明是类方法，方法参数中就没有 `cls` , 就没法通过 `cls` 获取到类属性。

因此类方法，想要调用类属性，需要以下步骤： 

* 在方法上面，用 `@classmethod` 声明该方法是类方法。只有声明了是类方法，才能使用类属性
* 类方法想要使用类属性，在第一个参数中，需要写上 `cls` ,  cls 是 class 的缩写，其实意思就是把这个类作为参数，传给自己，这样就可以使用类属性了。
* 类属性的使用方式就是 `cls.变量名`


记住喔，无论是 `@classmethod` 还是 `cls` ,都是不能省去的。

省了都会报错。





## 2、类方法传参 ##

上面我们学习了类方法如何调用类属性，那么类方法如何传参呢？

其实很简单，跟普通的函数一样，直接增加参数就好了。

这个就直接上例子了：

```python
class ClassA():
    var1 = '两点水'

    @classmethod
    def fun1(cls, age):  # 定义了个 age 参数
        print('我是 fun1' + cls.var1)
        print('年龄： ' + str(age))


ClassA.fun1(18)  # 多了个参数
```

打印的结果：

```
我是 fun1两点水
年龄： 18
```

# 四、修改和增加类属性 #


## 1、从内部增加和修改类属性 ##

来，我们先来温习一下类的结构。

![类的结构](../assets/diagrams/class-structure.svg)

看着这个结构，提一个问题，如何修改类属性，也就是类里面的变量？

从类结构来看，我们可以猜测，从类方法来修改，也就是从类内部来修改和增加类属性。

看下具体的实例：

<!-- skip-ci -->
```python
class ClassA():
    var1 = '两点水'

    @classmethod
    def fun1(cls):
        print('原来的 var1 值为： ' + cls.var1)
        cls.var1 = input('请输入修改 var1 的值： ')
        print('修改后 var1 值为： ' + cls.var1)
        cls.var2 = input('新增类属性 var2 ，请为它赋值为： ')
        print('修改后 var2 值为： ' + cls.var2)


ClassA.fun1()
```

输出结果如下（绿色字的为我输入的值）：

```
原来的 var1 值为： 两点水
请输入修改 var1 的值： 三点水
修改后 var1 值为： 三点水
新增类属性 var2 ，请为它赋值为： 四点水
修改后 var2 值为： 四点水
```

这里还是强调一下，例子还是要自己多写，不要只看，自己运行， 看效果。多想。




## 2、从外部增加和修改类属性 ##

我们刚刚看了通过类方法来修改类的属性，这时我们看下从外部如何修改和增加类属性。

例子如下：

<!-- skip-ci -->
```python
class ClassA():
    var1 = '两点水'

    @classmethod
    def fun1(cls):
        print('var1 值为： ' + cls.var1)


ClassA.fun1()
ClassA.var1 = input('请输入修改 var1 的值： ')
ClassA.fun1()

ClassA.var2 = input('请输入新增属性 var2 的值： ')
print(ClassA.var2)
```

输出结果如下：

```
var1 值为： 两点水
请输入修改 var1 的值： 三点水
var1 值为： 三点水
请输入新增属性 var2 的值： 四点水
四点水
```

# 五、类和对象 #




## 1、类和对象之间的关系 ##

这部分内容主要讲类和对象，我们先来说说类和对象之间的关系。

**类是对象的模板**

我们得先有了类，才能制作出对象。

类就相对于工厂里面的模具，对象就是根据模具制造出来的产品。

**从模具变成产品的过程，我们就称为类的实例化。**

**类实例化之后，就变成对象了。也就是相当于例子中的产品。**





## 2、类的实例化 ##

这里强调一下，类的实例化和直接使用类的格式是不一样的。

之前我们就学过，直接使用类格式是这样的：

```python
class ClassA():
    var1 = '两点水'

    @classmethod
    def fun1(cls):
        print('var1 值为：' + cls.var1)


ClassA.fun1()
```

而类的实例化是怎样的呢？

是这样的，可以仔细对比一下，类的实例化和直接使用类的格式有什么不同？

```python
class ClassA(object):  # 这个可以先不管，是关于继承的，后面会说到
    var1 = '两点水'

    def fun1(self):  # 没有了 @classmethod ，cls 变成了 self
        print('var1 值为： ' + self.var1)


# 实例化，并且使用
a = ClassA()
# 实例化之后，使用它里面的方法
a.fun1()
# 或者是使用它里面的属性
print(a.var1)
```

输出的结果：

```
var1 值为： 两点水
两点水
```


主要的不同点有：

* 类方法里面没有了 `@classmethod` 声明了，不用声明他是类方法
* 类方法里面的参数 `cls` 改为  `self`
* 类的使用，变成了先通过 `实例名 = 类()` 的方式实例化对象，为类创建一个实例，然后再使用 `实例名.函数()` 的方式调用对应的方法 ，使用 `实例名.变量名` 的方法调用类的属性


这里说明一下，类方法的参数为什么 `cls` 改为  `self` ？

其实这并不是说一定要写这个，你改为什么字母，什么名字都可以。 

不妨试一下：

```python
class ClassA(object):
    var1 = '两点水'

    def fun1(aaaaaaaa):  # self 改为 aaaaaaaa 了
        print('var1 值为： ' + aaaaaaaa.var1)


# 实例化
a = ClassA()
# 实例化之后，使用它里面的方法
a.fun1()
# 或者是使用它里面的属性
print(a.var1)
```

输出结果：

```
var1 值为： 两点水
两点水
```

你看，把 `self` 改为 `aaaaaaaa` 还是可以一样运行的。

只不过使用  `cls` 和 `self` 是我们的编程习惯，这也是我们的编程规范。

因为 cls 是 class 的缩写，代表这类 ， 而 self 代表这对象的意思。

所以啊，这里我们实例化对象的时候，就使用 self 。

**而且 self 是所有类方法位于首位、默认的特殊参数。**

除此之外，在这里，还要强调一个概念，当你把类实例化之后，里面的属性和方法，就不叫类属性和类方法了，改为叫实例属性和实例方法，也可以叫对象属性和对象方法。

为什么要这样强调呢？

**因为一个类是可以创造出多个实例对象出来的。**

你看下面的例子：

```python
class ClassA(object):
    var1 = '两点水'

    def fun1(self):
        print('var1 值为： ' + self.var1)


# 实例化
a = ClassA()
# 实例化之后，使用它里面的方法
a.fun1()
# 或者是使用它里面的属性
print(a.var1)


# 实例化
b = ClassA()
# 实例化之后，使用它里面的方法
b.fun1()
# 或者是使用它里面的属性
print(b.var1)
```

输出结果：

```
var1 值为： 两点水
两点水
var1 值为： 两点水
两点水
```

我不仅能用这个类创建 a 对象，还能创建 b 对象





## 3、实例属性和类属性 ##

一个类可以实例化多个对象出来。

![从类到实例](../assets/diagrams/class-instances.svg)

根据这个图，我们探究一下实例对象的属性和类属性之间有什么关系呢？

**先提出第一个问题，如果类属性改变了，实例属性会不会跟着改变呢？**

还是跟以前一样，提出了问题，我们直接用程序来验证就好。

看程序：


```python
class ClassA(object):
    var1 = '两点水'

    def fun1(self):
        print('var1 值为： ' + self.var1)


# 实例化
a = ClassA()
# 或者是使用它里面的属性
print(a.var1)

# 改变类属性
ClassA.var1 = '三点水'
# 重新打印实例化对象 a 的属性
print(a.var1)
```

输出结果：

```
两点水
三点水
```


从程序运行的结果来看，**类属性改变了，实例属性会跟着改变。**

这很好理解，因为我们的实例对象就是根据类来复制出来的，类属性改变了，实例对象的属性也会跟着改变。

**那么相反，如果实例属性改变了，类属性会改变吗？**

答案当然是不能啦。因为每个实例都是单独的个体，不能影响到类的。

具体我们做下实验：


```python
class ClassA(object):
    var1 = '两点水'

    def fun1(self):
        print('var1 值为： ' + self.var1)


# 实例化
a = ClassA()
# 或者是使用它里面的属性
print(a.var1)

# 修改实例化的属性只
a.var1 = '三点水'
# 打印修改后实例化的属性值
print(a.var1)

# 打印类的属性值
print(ClassA.var1)
```

输出结果：

```
两点水
三点水
两点水
```

可以看到，**不管实例对象怎么修改属性值，对类的属性还是没有影响的。**




## 4、实例方法和类方法 ##

那这里跟上面一样，还是提出同样的问题。

**如果类方法改变了，实例方法会不会跟着改变呢？**

看下下面的例子：

```python
class ClassA(object):
    var1 = '两点水'

    def fun1(self):
        print('关注十年不更新一次的公众号： ReadingWithU')


# 实例化
a = ClassA()
# 或者是使用它里面的方法
a.fun1()


# 修改类方法
# 1. 先要定义一个新函数
def newFun1(self):
    print('加我个人微信号： thinktoday2019 交个好友？ ')


# 2. 用新的函数替代老的函数，也就是「重写类方法」
ClassA.fun1 = newFun1

# 再次调用实例的方法
a.fun1()
```

输出结果：

```
关注十年不更新一次的公众号： ReadingWithU
加我个人微信号： thinktoday2019 交个好友？ 
```

这里建议我的例子，各位都要仔细看一下，自己重新敲一遍。相信为什么要这么做，这么证明。

还是那句话多想，多敲。

回归正题，从运行的结果来看，类方法改变了，实例方法也是会跟着改变的。

在这个例子中，我们需要改变类方法，就用到了**类的重写**。

我们使用了  `类.原始函数 = 新函数`  就完了类的重写了。

要注意的是，这里的赋值是在替换方法，并不是调用函数。所以是不能加上括号的，也就是 `类.原始函数() = 新函数()` 这个写法是不对的。


**那么如果实例方法改变了，类方法会改变吗？**

如果这个问题我们需要验证的话，是不是要重写实例的方法，然后观察结果，看看类方法有没有改变，这样就能得出结果了。


可是我们是不能重写实例方法。

你看，会直接报错。

<!-- skip-ci -->
```python
class ClassA(object):
    var1 = '两点水'

    def fun1(self):
        print('关注十年不更新一次的公众号： ReadingWithU')


# 实例化
a = ClassA()
# 使用它里面的方法
a.fun1()


# 1. 先要定义一个新函数
def newFun1(self):
    print('加我个人微信号： thinktoday2019 交个好友？ ')


# 2. 实例方法替换新函数
a.fun1 = newFun1

# 再次调用实例的方法
a.fun1()
```

报错如下：

```
关注十年不更新一次的公众号： ReadingWithU
Traceback (most recent call last):
  File "/Users/twowater/dev/python/test/com/twowater/test.py", line 24, in <module>
    a.fun1()
TypeError: newFun1() missing 1 required positional argument: 'self'
```
















## 两份记录各存在哪里

前面讲了类与对象，接着把学习时间做成一个很小的类。各位先找出哪些数据属于每一份记录，哪些说明可以由整个类共用。

```python
class StudyRecord:
    category = '学习记录'

    def __init__(self, subject):
        self.subject = subject
        self.minutes = 0

    def add(self, minutes):
        self.minutes = self.minutes + minutes

    @classmethod
    def get_category(cls):
        return cls.category


python_record = StudyRecord('Python')
reading_record = StudyRecord('读书')
python_record.add(15)
print(python_record.minutes)
print(reading_record.minutes)
print(StudyRecord.get_category())
```

输出：

```text
15
0
学习记录
```

`self.minutes` 是每个实例自己的属性，所以增加 Python 的记录，不会改变读书的记录。`category` 是定义在类上的属性，这里由实例共同读取。

类里定义的方法还需要区分类型：这里的 `add(self, ...)` 是实例方法，接收实例；使用 `@classmethod` 的 `get_category(cls)` 才是接收类的类方法。`self`、`cls` 是约定名称，普通实例方法、类方法和静态方法也并非都以 `self` 开头。

自己让两份记录分别增加 `5` 分钟，应该得到 `20` 和 `5`。然后增加一个备注列表，分别试试在 `__init__` 中写 `self.notes = []`，以及在类上写 `notes = []`，用 `append()` 观察共享数据的区别。双下划线名称主要涉及名称改写，不是阻止所有外部访问的权限系统，不能把它当成保存秘密的安全边界。

# 六、初始化函数 #



## 1、什么是初始化函数 ##

初始化函数的意思是，当你创建一个实例的时候，这个函数就会被调用。

比如：

```python
class ClassA(object):

    def __init__(self):
        print('实例化成功')


# 实例化
a = ClassA()
```

输出结果如下（没有调用 `init` 方法，实例化后直接打印出来的）：

```
实例化成功
```

当代码在执行 `a = ClassA()` 的语句时，就自动调用了 `__init__(self)` 函数。

**而这个 `__init__(self)`  函数就是初始化函数，也叫构造函数。**

初始化函数的写法是固定的格式：中间是 `init`，意思是初始化，然后前后都要有【两个下划线】，然后 `__init__()` 的括号中，第一个参数一定要写上 `self`，不然会报错。

构造函数（初始化函数）格式如下：

<!-- skip-ci -->
```python
def __init__(self,[...):
```


初始化函数一样可以传递参数的，例如：

```python
class ClassA(object):

    def __init__(self, str):
        print('实例化成功')
        print(str)


# 实例化
a = ClassA('加我个人微信号： thinktoday2019 交个好友？ ')
```

输出结果：

```
实例化成功
加我个人微信号： thinktoday2019 交个好友？ 
```




## 2、析构函数 ##

竟然一个在创建的时候，会调用构造函数，那么理所当然，这个当一个类销毁的时候，就会调用析构函数。

析构函数语法如下：

<!-- skip-ci -->
```python
def __del__(self,[...):
```

看下具体的示例：


```python
class ClassA(object):

    def __init__(self):
        print('实例化成功')

    def __del__(self):
        print('实例化销毁了')


a = ClassA()
del a  # 调用这个方法能销毁对象
```

输出结果：

```
实例化成功
实例化销毁了
```



## 3、Python 定义类的历史遗留问题 ##

Python  在版本的迭代中，有一个关于类的历史遗留问题，就是新式类和旧式类的问题，具体先看以下的代码：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 旧式类
class OldClass:
    pass

# 新式类
class NewClass(object):
    pass

```

可以看到，这里使用了两者中不同的方式定义类，可以看到最大的不同就是，新式类继承了`object` 类，在 Python2 中，我们定义类的时候最好定义新式类，当然在 Python3 中不存在这个问题了，因为 Python3 中所有类都是新式类。

那么新式类和旧式类有什么区别呢？

运行下下面的那段代码：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 旧式类
class OldClass:
    def __init__(self, account, name):
        self.account = account
        self.name = name


# 新式类
class NewClass(object):
    def __init__(self, account, name):
        self.account = account
        self.name = name


if __name__ == '__main__':
    old_class = OldClass(111111, 'OldClass')
    print(old_class)
    print(type(old_class))
    print(dir(old_class))
    print('\n')
    new_class = NewClass(222222, 'NewClass')
    print(new_class)
    print(type(new_class))
    print(dir(new_class))

```

这是 python 2.7 运行的结果：

```
/Users/twowater/dev/python/test/venv/bin/python /Users/twowater/dev/python/test/com/twowater/test.py
<__main__.OldClass instance at 0x109a50560>
<type 'instance'>
['__doc__', '__init__', '__module__', 'account', 'name']


<__main__.NewClass object at 0x109a4b150>
<class '__main__.NewClass'>
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'account', 'name']

Process finished with exit code 0

```

这是 Python 3.6 运行的结果：

```
/usr/local/bin/python3.6 /Users/twowater/dev/python/test/com/twowater/test.py
<__main__.OldClass object at 0x1038ba630>
<class '__main__.OldClass'>
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'account', 'name']


<__main__.NewClass object at 0x103e3c9e8>
<class '__main__.NewClass'>
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'account', 'name']

Process finished with exit code 0

```


仔细观察输出的结果，对比一下，就能观察出来，注意喔，Pyhton3 中输出的结果是一模一样的，因为Python3 中没有新式类旧式类的问题。

# 七、类的继承 #

## 1、定义类的继承 ##

说到继承，你一定会联想到继承你老爸的家产之类的。

类的继承也是一样。

比如有一个旧类，是可以算平均数的。然后这时候有一个新类，也要用到算平均数，那么这时候我们就可以使用继承的方式。新类继承旧类，这样子新类也就有这个功能了。

通常情况下，我们叫旧类为父类，新类为子类。


首先我们来看下类的继承的基本语法：

<!-- skip-ci -->
```python
class ClassName(BaseClassName):
    <statement-1>
    .
    .
    .
    <statement-N>
```

在定义类的时候，可以在括号里写继承的类，如果不用继承类的时候，也要写继承 object 类，因为在 Python 中 object 类是一切类的父类。

当然上面的是单继承，Python 也是支持多继承的，具体的语法如下：

<!-- skip-ci -->
```python
class ClassName(Base1,Base2,Base3):
    <statement-1>
    .
    .
    .
    <statement-N>
```

多继承有一点需要注意的：若是父类中有相同的方法名，而在子类使用时未指定，python 在圆括号中父类的顺序，从左至右搜索 ， 即方法在子类中未找到时，从左到右查找父类中是否包含方法。

那么继承的子类可以干什么呢？

继承的子类的好处：
* 会继承父类的属性和方法
* 可以自己定义，覆盖父类的属性和方法

## 2、调用父类的方法 ##

一个类继承了父类后，可以直接调用父类的方法的，比如下面的例子，`UserInfo2` 继承自父类 `UserInfo` ，可以直接调用父类的  `get_account` 方法。

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class UserInfo(object):
    lv = 5

    def __init__(self, name, age, account):
        self.name = name
        self._age = age
        self.__account = account

    def get_account(self):
        return self.__account


class UserInfo2(UserInfo):
    pass


if __name__ == '__main__':
    userInfo2 = UserInfo2('两点水', 23, 347073565);
    print(userInfo2.get_account())

```

## 3、父类方法的重写 ##

当然，也可以重写父类的方法。

示例：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class UserInfo(object):
    lv = 5

    def __init__(self, name, age, account):
        self.name = name
        self._age = age
        self.__account = account

    def get_account(self):
        return self.__account

    @classmethod
    def get_name(cls):
        return cls.lv

    @property
    def get_age(self):
        return self._age


class UserInfo2(UserInfo):
    def __init__(self, name, age, account, sex):
        super(UserInfo2, self).__init__(name, age, account)
        self.sex = sex;


if __name__ == '__main__':
    userInfo2 = UserInfo2('两点水', 23, 347073565, '男');
    # 打印所有属性
    print(dir(userInfo2))
    # 打印构造函数中的属性
    print(userInfo2.__dict__)
    print(UserInfo2.get_name())

```

最后打印的结果：

```
['_UserInfo__account', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', ...]
{'name': '两点水', '_age': 23, '_UserInfo__account': 347073565, 'sex': '男'}
5
```

这里就是重写了父类的构造函数。


## 4、子类的类型判断 ##

对于 class 的继承关系来说，有些时候我们需要判断 class 的类型，该怎么办呢？

可以使用 `isinstance()` 函数,

一个例子就能看懂 `isinstance()` 函数的用法了。

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User1(object):
    pass


class User2(User1):
    pass


class User3(User2):
    pass


if __name__ == '__main__':
    user1 = User1()
    user2 = User2()
    user3 = User3()
    # isinstance()就可以告诉我们，一个对象是否是某种类型
    print(isinstance(user3, User2))
    print(isinstance(user3, User1))
    print(isinstance(user3, User3))
    # 基本类型也可以用isinstance()判断
    print(isinstance('两点水', str))
    print(isinstance(347073565, int))
    print(isinstance(347073565, str))

```

输出的结果如下：

```txt
True
True
True
True
True
False
```

可以看到 `isinstance()` 不仅可以告诉我们，一个对象是否是某种类型，也可以用于基本类型的判断。

# 八、类的多态 #

多态的概念其实不难理解，它是指对不同类型的变量进行相同的操作，它会根据对象（或类）类型的不同而表现出不同的行为。

事实上，我们经常用到多态的性质，比如：

```
>>> 1 + 2
3
>>> 'a' + 'b'
'ab'
```

可以看到，我们对两个整数进行 + 操作，会返回它们的和，对两个字符进行相同的 + 操作，会返回拼接后的字符串。

也就是说，不同类型的对象对同一消息会作出不同的响应。


看下面的实例，来了解多态：


```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class User(object):
    def __init__(self, name):
        self.name = name

    def printUser(self):
        print('Hello !' + self.name)


class UserVip(User):
    def printUser(self):
        print('Hello ! 尊敬的Vip用户：' + self.name)


class UserGeneral(User):
    def printUser(self):
        print('Hello ! 尊敬的用户：' + self.name)


def printUserInfo(user):
    user.printUser()


if __name__ == '__main__':
    userVip = UserVip('两点水')
    printUserInfo(userVip)
    userGeneral = UserGeneral('水水水')
    printUserInfo(userGeneral)

```

输出的结果:

```txt
Hello ! 尊敬的Vip用户：两点水
Hello ! 尊敬的用户：水水水
```

可以看到，userVip 和 userGeneral 是两个不同的对象，对它们调用 printUserInfo 方法，它们会自动调用实际类型的 printUser 方法，作出不同的响应。这就是多态的魅力。

要注意喔，有了继承，才有了多态，也会有不同类的对象对同一消息会作出不同的相应。

# 九、类的访问控制 #


## 1、类属性的访问控制 ##

在 Java 中，有 public （公共）属性 和 private （私有）属性，这可以对属性进行访问控制。

那么在 Python 中有没有属性的访问控制呢？

一般情况下，我们会使用 `__private_attrs` 两个下划线开头，声明该属性为私有，不能在类地外部被使用或直接访问。在类内部的方法中使用时 `self.__private_attrs`。

为什么只能说一般情况下呢？

因为实际上， Python 中是没有提供私有属性等功能的。

但是 Python 对属性的访问控制是靠程序员自觉的。为什么这么说呢？

看看下面的示例：

```python
class UserInfo(object):
    def __init__(self, name, age, account):
        self.name = name        # 可以公开访问
        self._age = age         # 私有属性，可是我们想访问还是可以访问到的，这个不是 Python 语法上的规定，只是编程规范
        self.__account = account  # 这里两个下划线的属性，在创建这个类的时候，是不可以直接访问到两个下划线的属性的，但是，它又不是真正的私有属性，依然有办法可以访问
```

仔细看图片，为什么说双下划线不是真正的私有属性呢？我们看下下面的例子，用下面的例子来验证：

```python

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class UserInfo(object):
    def __init__(self, name, age, account):
        self.name = name
        self._age = age
        self.__account = account

    def get_account(self):
        return self.__account


if __name__ == '__main__':
    userInfo = UserInfo('两点水', 23, 347073565);
    # 打印所有属性
    print(dir(userInfo))
    # 打印构造函数中的属性
    print(userInfo.__dict__)
    print(userInfo.get_account())
    # 用于验证双下划线是否是真正的私有属性
    print(userInfo._UserInfo__account)


```

输出的结果如下图：

```
['_UserInfo__account', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', ...]
{'name': '两点水', '_age': 23, '_UserInfo__account': 347073565}
347073565
347073565
```

通过打印的所有属性和构造函数中的属性可以发现，我们定义的属性只是 `__account` ，发现打印中的属性把这个名字改了，变为 `_UserInfo__account` 了；而最后一行，可以直接打印双下划线的属性，证明它并不是真正的私有属性。




## 2、类专有的方法 ##

一个类创建的时候，就会包含一些方法，主要有以下方法：

类的专有方法：

| 方法 | 说明 |
| ------| ------ |
|`__init__` |构造函数，在生成对象时调用|
|`__del__ `| 析构函数，释放对象时使用|
|`__repr__ `| 打印，转换|
|`__setitem__ `| 按照索引赋值|
|`__getitem__`| 按照索引获取值|
|`__len__`| 获得长度|
|`__cmp__`| 比较运算|
|`__call__`| 函数调用|
|`__add__`| 加运算|
|`__sub__`| 减运算|
|`__mul__`|乘运算|
|`__div__`| 除运算|
|`__mod__`| 求余运算|
|`__pow__`|乘方|

当然有些时候我们需要获取类的相关信息，我们可以使用如下的方法：

* `type(obj)`：来获取对象的相应类型；
* `isinstance(obj, type)`：判断对象是否为指定的 type 类型的实例；
* `hasattr(obj, attr)`：判断对象是否具有指定属性/方法；
* `getattr(obj, attr[, default])` 获取属性/方法的值, 要是没有对应的属性则返回 default 值（前提是设置了 default），否则会抛出 AttributeError 异常；
* `setattr(obj, attr, value)`：设定该属性/方法的值，类似于 obj.attr=value；
* `dir(obj)`：可以获取相应对象的所有属性和方法名的列表：



## 3、方法的访问控制 ##

其实我们也可以把方法看成是类的属性的，那么方法的访问控制也是跟属性是一样的，也是没有实质上的私有方法。一切都是靠程序员自觉遵守 Python 的编程规范。

示例如下，具体规则也是跟属性一样的，

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class User(object):
    def upgrade(self):
        pass

    def _buy_equipment(self):
        pass

    def __pk(self):
        pass

```
