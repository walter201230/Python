# 第 6 章：函数

# 前言 #

函数这个章节内容有点多，对于新手，也有些不好理解。建议各位多看几篇，多敲几次代码。

# 目录 #


函数

- 一、Python 自定义函数的基本步骤
    - 1、什么是函数
    - 2、怎么自定义函数
- 二、函数返回值
- 三、函数的参数
    - 1、函数的参数类型
    - 2、默认参数
    - 3、关键字参数（位置参数）
    - 4、不定长参数
    - 5、只接受关键字参数
- 四、函数传值问题
- 五、匿名函数

# 一、Python 自定义函数的基本步骤 #




## 1、什么是函数 ##

函数，其实我们一开始学 Python 的时候就接触过。

不过我们使用的大多数都是 Python 的内置函数。

比如基本每个章节都会出现的 `print()`  函数。

而现在，我们主要学习的是自定义函数。

**各位有没有想过为什么需要函数呢？**

如果要想回答这个问题，我们需要先了解函数是什么？

函数就是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。

没错，函数其实就是把代码抽象出来的代码段。

那为什么要抽象出来呢？

**方便我们使用，方便我们重复使用。**

**函数的本质就是我们把一些数据喂给函数，让他内部消化，然后吐出你想要的东西，至于他怎么消化的，我们不需要知道，它内部解决。**

怎么理解这句话呢？

举个例子，好比每次用到的 print 函数，我们都知道这个函数的作用是可以把我们的数据输出到控制台，让我们看到。所以 `print('水哥')` , 我们想打印 `水哥` 出来，就把 `水哥` 这个数据喂给  `print` 函数，然后他就直接把结果打印到控制台上了。







## 2、怎么自定义函数 ##

怎么自定义函数？

要知道怎么定义函数，就要知道函数的组成部分是怎样的。

<!-- skip-ci -->
```python
def 函数名(参数1，参数2....参数n):
    函数体
    return 语句
```

这就是 Python 函数的组成部分。

所以自定义函数，基本有以下规则步骤：

* 函数代码块以 def 关键词开头，后接函数标识符名称和圆括号()
* 任何传入参数和自变量必须放在圆括号中间。圆括号之间可以用于定义参数
* 函数的第一行语句可以选择性地使用文档字符串（用于存放函数说明）
* 函数内容以冒号起始，并且缩进
* return [表达式] 结束函数，选择性地返回一个值给调用方。不带表达式的 return 相当于返回 None。

语法示例：

```python
def functionname( parameters ):
   "函数_文档字符串"
   function_suite
   return [expression]
```

实例：

1. def 定义一个函数，给定一个函数名 sum 
2. 声明两个参数 num1 和 num2
3. 函数的第一行语句进行函数说明：两数之和
4. 最终 return 语句结束函数，并返回两数之和

```python
def sum(num1,num2):
	"两数之和"
	return num1+num2

# 调用函数
print(sum(5,6))
```

输出结果：

```python
11
```

# 二、函数返回值 #

通过上面的学习，可以知道通过 return [表达式] 语句用于退出函数，选择性地向调用方返回一个表达式。

**不带参数值的 return 语句返回 None。**

具体示例：

```python
# -*- coding: UTF-8 -*-

def sum(num1,num2):
	# 两数之和
	if not (isinstance (num1,(int ,float)) and isinstance (num2,(int ,float))):
		raise TypeError('参数类型错误')
	return num1+num2

print(sum(1,2))
```

返回结果：

```txt
3
```

这个示例，还通过内置函数`isinstance()`进行数据类型检查，检查调用函数时参数是否是整形和浮点型。如果参数类型不对，会报错，提示 `参数类型错误`,如图：

<!-- skip-ci -->
```python
# -*- coding: UTF-8 -*-

def sum(num1,num2):
	# 两数之和
	if not (isinstance (num1,(int ,float)) and isinstance (num2,(int ,float))):
		raise TypeError('参数类型错误')
	return num1+num2

print(sum('11',2))
```

报错信息：

```
Traceback (most recent call last):
  File "C:\Users\Administrator\Desktop\Python\test.py", line 9, in <module>
    print(sum('11',2))
  File "C:\Users\Administrator\Desktop\Python\test.py", line 6, in sum
    raise TypeError('参数类型错误')
TypeError: 参数类型错误
```

当然，函数也可以返回多个值，具体实例如下：

```python
# -*- coding: UTF-8 -*-

def  division ( num1, num2 ):
	# 求商与余数
         a = num1 % num2
         b = (num1-a) / num2
         return b , a

num1 , num2 = division(9,4)
tuple1 = division(9,4)

print (num1,num2)
print (tuple1)
```

输出的值：

```txt
2.0 1
(2.0, 1)
```

认真观察就可以发现，尽管从第一个输出值来看，返回了多个值，实际上是先创建了一个元组然后返回的。

回忆一下，元组是可以直接用逗号来创建的，观察例子中的 ruturn ，可以发现实际上我们使用的是逗号来生成一个元组。

Python 语言中的函数返回值可以是多个，而其他语言都不行，这是Python 相比其他语言的简便和灵活之处。

**Python 一次接受多个返回值的数据类型就是元组。**

不知道此刻你还记不记得元组的相关知识，如果不记得，建议现在立刻写几个例子回忆一下，比如如何获取元组的第一个元素出来。

# 三、函数的参数 #




## 1、函数的参数类型 ##

设置与传递参数是函数的重点，而 Python 的函数对参数的支持非常的灵活。

主要的参数类型有：默认参数、关键字参数（位置参数）、不定长参数。

下面我们将一一了解这几种参数。




## 2、默认参数 ##

有时候，我们自定义的函数中，如果调用的时候没有设置参数，需要给个默认值，这时候就需要用到默认值参数了。

默认参数，只要在构造函数参数的时候，给参数赋值就可以了

例如：


```python
# -*- coding: UTF-8 -*-

def print_user_info( name , age , sex = '男' ):
    # 打印用户信息
    print(f'昵称：{name}' , end = ' ')
    print(f'年龄：{age}' , end = ' ')
    print(f'性别：{sex}')
    return;

# 调用 print_user_info 函数

print_user_info( '两点水' , 18 , '女')
print_user_info( '三点水' , 25 )
```

输出结果：

```txt
昵称：两点水 年龄：18 性别：女
昵称：三点水 年龄：25 性别：男
```

从输出结果可以看到，当你设置了默认参数的时候，在调用函数的时候，不传该参数，就会使用默认值。

但是这里需要注意的一点是：**只有在形参表末尾的那些参数可以有默认参数值**，也就是说你不能在声明函数形参的时候，先声明有默认值的形参而后声明没有默认值的形参。

这是因为赋给形参的值是根据位置而赋值的。例如，def func(a, b=1) 是有效的，但是 def func(a=1, b) 是 无效 的。 

默认值参数就这样结束了吗？

还没有的，细想一下，如果参数中是一个可修改的容器比如一个 list （列表）或者 dict （字典），那么我们使用什么来作为默认值呢？

我们可以使用 None 作为默认值。就像下面这个例子一样：

```python
# 如果 b 是一个 list ，可以使用 None 作为默认值
def print_info( a , b = None ):
    if b is None :
        b=[]
    return;
```

认真看下例子，会不会有这样的疑问呢？在参数中我们直接 `b=[]` 不就行了吗？

也就是写成下面这个样子：

```python
def print_info( a , b = [] ):
    return;
```
对不对呢？

运行一下也没发现错误啊，可以这样写吗？

这里需要特别注意的一点：**默认参数的值是不可变的对象，比如None、True、False、数字或字符串**，如果你像上面的那样操作，当默认值在其他地方被修改后你将会遇到各种麻烦。

这些修改会影响到下次调用这个函数时的默认值。

示例如下：

```python
# -*- coding: UTF-8 -*-

def print_info( a , b = [] ):
    print(b)
    return b ;

result = print_info(1)

result.append('error')

print_info(2)
```

输出的结果：

```txt
[]
['error']
```

认真观察，你会发现第二次输出的值根本不是你想要的，因此切忌不能这样操作。


还有一点，有时候我就是不想要默认值啊，只是想单单判断默认参数有没有值传递进来，那该怎么办？

我们可以这样做：

```python
_no_value =object()

def print_info( a , b = _no_value ):
    if b is _no_value :
        print('b 没有赋值')
    return;
```

这里的 `object` 是 python 中所有类的基类。 你可以创建 `object` 类的实例，但是这些实例没什么实际用处，因为它并没有任何有用的方法， 也没有任何实例数据(因为它没有任何的实例字典，你甚至都不能设置任何属性值)。 你唯一能做的就是测试同一性。也正好利用这个特性，来判断是否有值输入。




## 3、关键字参数（位置参数） ##

一般情况下，我们需要给函数传参的时候，是要按顺序来的，如果不对应顺序，就会传错值。

不过在 Python 中，可以通过参数名来给函数传递参数，而不用关心参数列表定义时的顺序，这被称之为关键字参数。

使用关键参数有两个优势 ：

* 由于我们不必担心参数的顺序，使用函数变得更加简单了。

* 假设其他参数都有默认值，我们可以只给我们想要的那些参数赋值

具体看例子：

```python
# -*- coding: UTF-8 -*-

def print_user_info( name ,  age  , sex = '男' ):
    # 打印用户信息
    print(f'昵称：{name}' , end = ' ')
    print(f'年龄：{age}' , end = ' ')
    print(f'性别：{sex}')
    return;

# 调用 print_user_info 函数

print_user_info( name = '两点水' ,age = 18 , sex = '女')
print_user_info( name = '两点水' ,sex = '女', age = 18 )

```

输出的值：

```txt
昵称：两点水 年龄：18 性别：女
昵称：两点水 年龄：18 性别：女
```





## 4、不定长参数 ##

或许有些时候，我们在设计函数的时候，我们有时候无法确定传入的参数个数。

那么我们就可以使用不定长参数。

Python 提供了一种元组的方式来接受没有直接定义的参数。这种方式在参数前边加星号 `*` 。

如果在函数调用时没有指定参数，它就是一个空元组。我们也可以不向函数传递未命名的变量。

例如：

```python
# -*- coding: UTF-8 -*-

def print_user_info( name ,  age  , sex = '男' , * hobby):
    # 打印用户信息
    print(f'昵称：{name}' , end = ' ')
    print(f'年龄：{age}' , end = ' ')
    print(f'性别：{sex}' ,end = ' ' )
    print(f'爱好：{hobby}')
    return;

# 调用 print_user_info 函数
print_user_info( '两点水' ,18 , '女', '打篮球','打羽毛球','跑步')

```

输出的结果：

<!-- skip-ci -->
```python
昵称：两点水 年龄：18 性别：女 爱好：('打篮球', '打羽毛球', '跑步')
```

通过输出的结果可以知道，`*hobby`是可变参数，且 hobby 其实就是一个 tuple （元祖）


可变长参数也支持关键字参数（位置参数），没有被定义的关键参数会被放到一个字典里。

这种方式即是在参数前边加 `**`,更改上面的示例如下：


```python
# -*- coding: UTF-8 -*-

def print_user_info( name ,  age  , sex = '男' , ** hobby ):
    # 打印用户信息
    print(f'昵称：{name}' , end = ' ')
    print(f'年龄：{age}' , end = ' ')
    print(f'性别：{sex}' ,end = ' ' )
    print(f'爱好：{hobby}')
    return;

# 调用 print_user_info 函数
print_user_info( name = '两点水' , age = 18 , sex = '女', hobby = ('打篮球','打羽毛球','跑步'))

```

输出的结果：

```txt
昵称：两点水 年龄：18 性别：女 爱好：{'hobby': ('打篮球', '打羽毛球', '跑步')}	
```

通过对比上面的例子和这个例子，可以知道，`*hobby`是可变参数，且 hobby其实就是一个 tuple （元祖），`**hobby`是关键字参数，且 hobby 就是一个 dict （字典）



## 5、只接受关键字参数 ##

关键字参数使用起来简单，不容易参数出错，那么有些时候，我们定义的函数希望某些参数强制使用关键字参数传递，这时候该怎么办呢？

将强制关键字参数放到某个`*`参数或者单个`*`后面就能达到这种效果,比如：

```python
# -*- coding: UTF-8 -*-

def print_user_info( name , *, age  , sex = '男' ):
    # 打印用户信息
    print(f'昵称：{name}' , end = ' ')
    print(f'年龄：{age}' , end = ' ')
    print(f'性别：{sex}')
    return;

# 调用 print_user_info 函数
print_user_info( name = '两点水' ,age = 18 , sex = '女' )

# 这种写法会报错，因为 age ，sex 这两个参数强制使用关键字参数
#print_user_info( '两点水' , 18 , '女' )
print_user_info('两点水',age='22',sex='男')
```

通过例子可以看，如果 `age` , `sex` 不使用关键字参数是会报错的。

很多情况下，使用强制关键字参数会比使用位置参数表意更加清晰，程序也更加具有可读性。使用强制关键字参数也会比使用 `**kw` 参数更好且强制关键字参数在一些更高级场合同样也很有用。



## 6、 Python 3.10+ 的类型注解写法 ##

各位童鞋，看了上面这么多种参数，大家有没有想过一个问题：函数光看名字和参数列表，我们其实并不知道每个参数到底是什么类型？

比如下面这个函数，你能一眼看出 `name` 是字符串、 `age` 是整数吗？

```python
def print_user_info(name, age, sex='男'):
    print(f'昵称：{name} 年龄：{age} 性别：{sex}')
```

调用的人很可能传错类型，传了一个 list 进去也不会报错，运行到一半才出问题。这时候，类型注解（type hint）就派上用场了。

我们先看最基本的写法：

```python
def print_user_info(name: str, age: int, sex: str = '男') -> None:
    print(f'昵称：{name} 年龄：{age} 性别：{sex}')


print_user_info('两点水', 18, '女')
```

输出的结果：

```
昵称：两点水 年龄：18 性别：女
```

参数后面的 `: str` 、`: int` ，以及箭头 `-> None` 都是类型注解。注意，Python 自己运行的时候 **不会** 强制检查这些注解——你硬传一个 list 也不会立刻报错。注解的真正用处，是给你和你的同事（还有 IDE、 mypy、 pyright 这些静态检查工具）看的，让代码更易读、更易维护。

那么遇到「这个参数可能是 None」的情况怎么办呢？

在 Python 3.10 之前，要写 `Optional[str]` ：

```python
from typing import Optional


def find_user(name: str) -> Optional[str]:
    # 没找到就返回 None
    if name == '两点水':
        return '131456780002'
    return None


print(find_user('两点水'))
print(find_user('六点水'))
```

输出的结果：

```
131456780002
None
```

这样写没毛病，但是要专门 `import` 一个东西，有点啰嗦。Python 3.10 之后，可以直接用 `|` 表示「或」（PEP 604）：

```python
def find_user(name: str) -> str | None:
    if name == '两点水':
        return '131456780002'
    return None


print(find_user('两点水'))
print(find_user('六点水'))
```

输出的结果：

```
131456780002
None
```

是不是干净多了？ `str | None` 直接读出来就是「字符串或者 None」，不再需要 `Optional` 这个名字。

那么 list、 dict 这种容器类型呢？

在 Python 3.9 之前要从 `typing` 导入大写的 `List` 、 `Dict` ：

```python
from typing import List, Dict


def get_users() -> List[str]:
    return ['一点水', '两点水', '三点水']


def get_phones() -> Dict[str, str]:
    return {'两点水': '131456780002'}


print(get_users())
print(get_phones())
```

而从 Python 3.9 开始（PEP 585），可以直接用内置的小写 `list` 、 `dict` 当类型注解：

```python
def get_users() -> list[str]:
    return ['一点水', '两点水', '三点水']


def get_phones() -> dict[str, str]:
    return {'两点水': '131456780002'}


print(get_users())
print(get_phones())
```

输出的结果都是：

```
['一点水', '两点水', '三点水']
{'两点水': '131456780002'}
```

这下连 `from typing import ...` 都省了，更简洁。

类型注解还可以用在「类」上面，比较常见的场景就是搭配 `dataclass` ：

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
    sex: str = '男'


u = User('两点水', 18, '女')
print(u)
```

输出的结果：

```
User(name='两点水', age=18, sex='女')
```

`dataclass` 是个非常好用的东西，等到后面讲面向对象的时候，咱们再展开聊。

> Python 3.12+ ：`type` 关键字定义类型别名

最后再提一个 Python 3.12 的新东西（PEP 695）。如果你写了一个特别长的复合类型，每次都重复写不优雅，可以用 `type` 关键字给它起个别名：

<!-- skip-ci -->
```python
type UserId = int | str
type PhoneBook = dict[str, str]


def find_phone(book: PhoneBook, name: str) -> str | None:
    return book.get(name)


book: PhoneBook = {'两点水': '131456780002'}
print(find_phone(book, '两点水'))
```

输出的结果：

```
131456780002
```

这里 `UserId` 和 `PhoneBook` 就是「类型别名」，跟变量赋值长得很像，但意思是「这是一个类型」。

类型注解的世界其实远不止这些，还有泛型、协议（Protocol）、 `TypeVar` 等等更高级的玩法，咱们这本书后面会专门拿出一章来讲，这里各位先掌握上面这几种最常用的就够日常写代码用了。

# 四、函数传值问题 #

先看一个例子：

```python
# -*- coding: UTF-8 -*-
def chagne_number( b ):
    b = 1000

b = 1
chagne_number(b)
print( b )
```

最后输出的结果为：

```txt
1
```

先看看运行的结果？

想一下为什么打印的结果是 1 ，而不是 1000 ？

其实把问题归根结底就是，为什么通过函数 `chagne_number` 没有更改到 b 的值？

这个问题很多编程语言都会讲到，原理解释也是差不多的。

这里主要是函数参数的传递中，传递的是类型对象，之前也介绍了 Python 中基本的数据类型等。而这些类型对象可以分为可更改类型和不可更改的类型

**在 Python 中，字符串，整形，浮点型，tuple 是不可更改的对象，而 list ， dict 等是可以更改的对象。**

例如：

**不可更改的类型**：变量赋值 `a = 1`，其实就是生成一个整形对象 1 ，然后变量 a 指向 1，当 `a = 1000` 其实就是再生成一个整形对象 1000，然后改变 a 的指向，不再指向整形对象 1 ，而是指向 1000，最后 1 会被丢弃

**可更改的类型**：变量赋值 `a = [1,2,3,4,5,6]` ，就是生成一个对象 list ，list 里面有 6 个元素，而变量 a 指向 list ，`a[2] = 5`则是将 list a 的第三个元素值更改,这里跟上面是不同的，并不是将 a 重新指向，而是直接修改 list 中的元素值。

不可更改的类型（变量重新指向）：

![变量重新指向](../assets/diagrams/variable-rebinding.svg)

可更改的类型（直接修改对象内部元素）：

![列表原地修改](../assets/diagrams/list-mutation.svg)

这也将影响到函数中参数的传递了：

**不可更改的类型**：类似 c++ 的值传递，如 整数、字符串、元组。如fun（a），传递的只是 a 的值，没有影响 a 对象本身。比如在 fun（a）内部修改 a 的值，只是修改另一个复制的对象，不会影响 a 本身。

**可更改的类型**：类似 c++ 的引用传递，如 列表，字典。如 fun（a），则是将 a 真正的传过去，修改后 fun 外部的 a 也会受影响

因此，在一开始的例子中，`b = 1`,创建了一个整形对象 1 ，变量 b 指向了这个对象，然后通过函数 chagne_number 时，按传值的方式复制了变量 b ，传递的只是 b 的值，并没有影响到 b 的本身。具体可以看下修改后的实例，通过打印的结果更好的理解。

```python
# -*- coding: UTF-8 -*-
def chagne_number( b ):
    print(f'函数中一开始 b 的值：{b}')
    b = 1000
    print(f'函数中 b 赋值后的值：{b}')


b = 1
chagne_number( b )
print(f'最后输出 b 的值：{b}')


```

打印的结果：

```txt
函数中一开始 b 的值：1
函数中 b 赋值后的值：1000
最后输出 b 的值：1
```

当然，如果参数中的是可更改的类型，那么调用了这个函数后，原来的值也会被更改，具体实例如下：

```python
# -*- coding: UTF-8 -*-

def chagne_list( b ):
    print(f'函数中一开始 b 的值：{b}')
    b.append(1000)
    print(f'函数中 b 赋值后的值：{b}')


b = [1,2,3,4,5]
chagne_list( b )
print(f'最后输出 b 的值：{b}')
```

输出的结果：

```txt
函数中一开始 b 的值：[1, 2, 3, 4, 5]
函数中 b 赋值后的值：[1, 2, 3, 4, 5, 1000]
最后输出 b 的值：[1, 2, 3, 4, 5, 1000]
```



## 一样是列表，为什么有时改了，有时没改

各位先别急着往下看，我们再试一个问题：如果传进去的是列表，在函数里给参数重新赋值，外面的列表也一定会变吗？

先猜一下下面两次打印的结果，再运行代码：

```python
def replace_items(items):
    items = [1000]


def append_item(items):
    items.append(1000)


numbers = [1, 2]
replace_items(numbers)
print(numbers)
append_item(numbers)
print(numbers)
```

输出：

```text
[1, 2]
[1, 2, 1000]
```

是不是发现，传进去的明明都是同一个列表，两次操作的结果却不一样？

原因要回到前面讲过的变量指向。在调用函数时，参数名 `items` 和外面的 `numbers` 指向同一个列表。`items = [1000]` 是让函数里的 `items` 指向另一个列表，外面的 `numbers` 没有跟着改。`items.append(1000)` 则没有改变指向，而是往原来的列表里增加了一个元素，所以外面也看到了变化。

理解前面的传参类比时，要注意一个边界：Python 的参数传递不会因为对象能不能修改而切换机制，也不会在传入整数时自动复制一个对象。参数名绑定到传入的对象；实际操作是重新绑定名称，还是修改对象，才决定了这里的区别。可以对照 [Python 官方 FAQ](https://docs.python.org/zh-cn/3.13/faq/programming.html#how-do-i-write-a-function-with-output-parameters-call-by-reference) 理解。

自己再改一下：把 `numbers` 的初始值换成空列表，两次输出应该是什么？先写下答案，再运行。应该依次得到 `[]` 和 `[1000]`，理由还是一样的。

## 默认的列表为什么会记住上一次调用

参数那一节提到过，默认值要小心使用列表。这个建议不是说 Python 的语法不允许，而是默认值在定义函数时求值一次，后续省略这个参数的调用会共用它。

我们还用记录学习时间这个小需求来试一下：

```python
def record_minutes(minutes, records=[]):
    records.append(minutes)
    return records


print(record_minutes(5))
print(record_minutes(10))
```

输出：

```text
[5]
[5, 10]
```

如果我们的需求是每次调用都新建一份记录，那么第二次出现 `5` 就不符合预期了。可以这样写：

```python
def record_minutes(minutes, records=None):
    if records is None:
        records = []
    records.append(minutes)
    return records


print(record_minutes(5))
print(record_minutes(10))
```

输出：

```text
[5]
[10]
```

`None` 在这里表示调用方没有提供记录列表，于是函数自己创建一份。如果调用方主动传入同一个列表，记录仍然会累加。自己试一下：创建 `records = []`，分别调用 `record_minutes(5, records)` 和 `record_minutes(10, records)`，最后打印 `records`，结果应该是 `[5, 10]`。这次共享是我们明确选择的。

阅读 [官方教程的默认参数说明](https://docs.python.org/zh-cn/3.13/tutorial/controlflow.html#default-argument-values) 时，可以带着一个问题去找答案：默认值究竟是在什么时候产生的？先找这个信息，再回头解释上面的两组输出。

## 打印出来了，为什么还拿到 None

最后再分清楚一个经常混在一起的问题。函数把结果打印到屏幕，和把结果返回给调用方，是两件事。

```python
def show_minutes(minutes):
    print(minutes)


def get_minutes(minutes):
    return minutes


shown = show_minutes(15)
saved = get_minutes(15)
print(shown)
print(saved)
```

输出：

```text
15
None
15
```

第一行是 `show_minutes` 自己打印的。它没有写 `return`，所以 `shown` 得到的是 `None`。`get_minutes` 则把 `15` 返回给了调用方，由外面的 `print(saved)` 打印出来。

到这里，各位可以自己写一个 `total_minutes(first, second)`：返回两次学习时间的和，函数内部不打印。用 `total_minutes(5, 10)`、`total_minutes(0, 0)` 和 `total_minutes(12, 3)` 验证，结果应该分别是 `15`、`0` 和 `15`。如果你能解释打印与返回的区别，并独立完成这三个调用，这一部分才算真正用起来了。

# 补充：函数里的变量，外面看得见吗？

上一节「函数传值问题」里，函数里写了 `b = 1000` ，外面的 `b` 却还是 1。这一节换个角度，从「变量在哪儿能用」说说这件事。

先看一个例子：

<!-- skip-ci -->
```python
def add_cost(cost):
    total = 0
    total = total + cost
    return total


print(add_cost(12.5))
print(total)
```

第一行打印出了 `12.5` ，接着报错，最后一行是：

```
NameError: name 'total' is not defined
```

`total` 明明在函数里定义过，外面怎么找不到？

因为在函数里面创建的变量，叫**局部变量**，只在这个函数里面能用。函数一结束，它就没了。外面想要函数算出来的结果，就得靠 `return` 交出来，就像 `print(add_cost(12.5))` 那样。

反过来，写在所有函数外面的变量，叫**全局变量**。函数里面可以直接读它：

```python
budget = 50


def within_budget(cost):
    return cost <= budget


print(within_budget(30))
print(within_budget(80))
```

输出的结果：

```
True
False
```

能读，那能不能改呢？试试在函数里给全局变量加钱：

<!-- skip-ci -->
```python
total = 0


def add(cost):
    total = total + cost


add(12.5)
```

报错信息的最后一行是：

```
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
```

意思是：没法访问局部变量 `total` ，它还没有值。

为什么呢？只要函数里有给 `total` 赋值的语句，Python 就认定这个 `total` 是函数自己的局部变量，和外面那个没关系了。可执行 `total + cost` 的时候，局部的 `total` 还没有值，就报错了。

回头再看上一节的例子，道理是一样的：函数里的 `b = 1000` ，只是给函数自己的局部变量 `b` 赋了值，外面的 `b` 当然不会变。

那想在函数里累加，该怎么办？最好的办法是：**用参数把值传进去，用 `return` 把结果交出来**：

```python
def add(total, cost):
    return total + cost


total = 0
total = add(total, 12.5)
total = add(total, 25)
print(total)
```

输出的结果：

```
37.5
```

函数只管算，不碰外面的变量；外面拿到结果，自己决定存到哪儿。这样的函数，拿到哪儿都能用，也不容易出错。

其实，Python 还有一个关键字 `global` ，写在函数里，就能直接改外面的变量：

```python
total = 0


def add(cost):
    global total
    total = total + cost


add(12.5)
add(25)
print(total)
```

输出的结果：

```
37.5
```

能用是能用，可函数和外面的变量就这么缠在了一起：读函数的时候，得去外面找 `total` 是哪儿来的；外面的 `total` 被谁改了，也很难查。所以一般能用参数和返回值解决的，就别用 `global` 。第 15 章讲闭包的时候，还会再见到它。

自己试一试：把下面代码里的 `count = count + 1` 改成 `return count + 1` 的写法，让它能正确数出一共调用了几次。

```python
count = 0


def visit(count):
    count = count + 1


visit(count)
visit(count)
print(count)
```

现在它打印的是 `0` ，想一想为什么。

# 五、匿名函数 #

有没有想过定义一个很短的回调函数，但又不想用 `def` 的形式去写一个那么长的函数，那么有没有快捷方式呢？

答案是有的。

python 使用 lambda 来创建匿名函数，也就是不再使用 def 语句这样标准的形式定义一个函数。

匿名函数主要有以下特点：

* lambda 只是一个表达式，函数体比 def 简单很多。
* lambda 的主体是一个表达式，而不是一个代码块。仅仅能在 lambda 表达式中封装有限的逻辑进去。
* lambda 函数拥有自己的命名空间，且不能访问自有参数列表之外或全局命名空间里的参数。

**基本语法**

<!-- skip-ci -->
```python
lambda [arg1 [,arg2,.....argn]]:expression
```

示例：

```python
# -*- coding: UTF-8 -*-

sum = lambda num1 , num2 : num1 + num2;

print( sum( 1 , 2 ) )

```

输出的结果：

```txt
3
```

注意：**尽管 lambda 表达式允许你定义简单函数，但是它的使用是有限制的。 你只能指定单个表达式，它的值就是最后的返回值。也就是说不能包含其他的语言特性了， 包括多个语句、条件表达式、迭代以及异常处理等等。**

匿名函数中，有一个特别需要注意的问题，比如，把上面的例子改一下：

```python
# -*- coding: UTF-8 -*-

num2 = 100
sum1 = lambda num1 : num1 + num2 ;

num2 = 10000
sum2 = lambda num1 : num1 + num2 ;

print( sum1( 1 ) )
print( sum2( 1 ) )
```

你会认为输出什么呢？第一个输出是 101，第二个是 10001，结果不是的，输出的结果是这样：

```txt
10001
10001
```

**这主要在于 lambda 表达式中的 num2 是一个自由变量，在运行时绑定值，而不是定义时就绑定，这跟函数的默认值参数定义是不同的。所以建议还是遇到这种情况还是使用第一种解法。**
