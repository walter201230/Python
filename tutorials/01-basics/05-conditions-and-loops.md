# 第 5 章：条件语句和循环语句

# 前言 #

通常都听到别人说，计算机很牛逼，很聪明，其实计算机一点都不聪明，光是你要跟他沟通，都会气 shi 你，聪明的是在写程序的你。

写程序就是跟计算机沟通，告诉它要做什么。

竟然是这样，那么肯定缺少不了一些沟通逻辑。比如你要告诉计算机在什么情况下做什么？或者在哪个时间点做什么？

这都需要用到逻辑判断。这一章节，主要就是说这个。


# 目录 #


条件语句和循环语句

- 一、条件语句
    - 1、什么是条件语句
    - 2、`if` 语句的基本形式
    - 3、`if` 语句多个判断条件的形式
    - 4、`if` 语句多个条件同时判断
    - 5、`if` 嵌套
- 二、循环语句
    - 1、什么是循环语句
    - 2、`for` 循环语句
    - 3、`range()` 函数
    - 4、`While` 循环语句
    - 5、`for` 循环和 `while` 循环的区别
    - 6、嵌套循环
- 三、条件语句和循环语句综合实例
    - 1、打印九九乘法表
    - 2、判断是否是闰年

# 一、条件语句 #


## 1、什么是条件语句 ##


Python 条件语句跟其他语言基本一致的，都是通过一条或多条语句的执行结果（ True 或者 False ）来决定执行的代码块。

Python 程序语言指定任何非 0 和非空（null）值为 True，0 或者 null 为 False。

执行的流程图如下：

![if 条件判断](../assets/diagrams/if-flow.svg)


## 2、if 语句的基本形式 ##

Python 中，if 语句的基本形式如下：

<!-- skip-ci -->
```python
if 判断条件：
    执行语句……
else：
    执行语句……
```

之前的章节也提到过，Python 语言有着严格的缩进要求，因此这里也需要注意缩进，也不要少写了冒号 `:` 。

if 语句的判断条件可以用>（大于）、<(小于)、==（等于）、>=（大于等于）、<=（小于等于）来表示其关系。

例如：

```python
# -*-coding:utf-8-*-

results=59

if results>=60:
    print ('及格')
else :
    print ('不及格')

```

输出的结果为：

```txt
不及格
```

上面也说到，非零数值、非空字符串、非空 list 等，判断为 True，否则为 False。因此也可以这样写：

```python
num = 6
if num :
    print('Hello Python')
```

输出的结果如下：

```
Hello Python
```

可见，把结果打印出来了。

那如果我们把 `num ` 改为空字符串呢？

```python
num = ''
if num :
    print('Hello Python')
```

输出结果什么也没有打印（程序正常结束，没输出 `Hello Python`）。

很明显，空字符串是为 False 的，不符合条件语句，因此不会执行到  `print('Hello Python')`  这段代码。

还有再啰嗦一点，提醒一下，在条件判断代码中的冒号 `:` 后、下一行内容是一定要缩进的。不缩进是会报错的。

<!-- skip-ci -->
```python
num = ''
if num :
print('Hello Python')
```

运行后会报错：

```
  File "/Users/twowater/dev/python/test/com/twowater/test.py", line 4
    print('Hello Python')
        ^
IndentationError: expected an indented block
```

冒号和缩进是一种语法。它会帮助 Python 区分代码之间的层次，理解条件执行的逻辑及先后顺序。



## 3、if 语句多个判断条件的形式 ##

有些时候，我们的判断语句不可能只有两个，有些时候需要多个，比如上面的例子中大于 60 的为及格，那我们还要判断大于 90 的为优秀，在 80 到 90 之间的良好呢？

这时候需要用到 if 语句多个判断条件，

用伪代码来表示：

<!-- skip-ci -->
```python
if 判断条件1:
    执行语句1……
elif 判断条件2:
    执行语句2……
elif 判断条件3:
    执行语句3……
else:
    执行语句4……
```

实例：

```python
# -*-coding:utf-8-*-

results = 89

if results > 90:
    print('优秀')
elif results > 80:
    print('良好')
elif results > 60:
    print ('及格')
else :
    print ('不及格')

```

输出的结果：

```txt
良好
```



## 4、if 语句多个条件同时判断 ##

有时候我们会遇到多个条件的时候该怎么操作呢？

比如说要求 java 和 python 的考试成绩要大于 80 分的时候才算优秀，这时候该怎么做？

这时候我们可以结合 `or` 和  `and` 来使用。

or （或）表示两个条件有一个成立时判断条件成功
 
and （与）表示只有两个条件同时成立的情况下，判断条件才成功。

例如：

```python
# -*-coding:utf-8-*-

java = 86
python = 68

if java > 80 and  python > 80:
    print('优秀')
else :
    print('不优秀')

if ( java >= 80  and java < 90 )  or ( python >= 80 and python < 90):
    print('良好')

```

输出结果：

```txt
不优秀
良好
```

注意：if 有多个条件时可使用括号来区分判断的先后顺序，括号中的判断优先执行，此外 and 和 or 的优先级低于 >（大于）、<（小于）等判断符号，即大于和小于在没有括号的情况下会比与或要优先判断。

## 5、if 嵌套 ##

if 嵌套是指什么呢？

就跟字面意思差不多，指 if 语句中可以嵌套 if 语句。

比如上面说到的例子，也可以用 if 嵌套来写。

```python
java = 86
python = 68

if java > 80:
    if python > 80:
        print('优秀')
    else:
        print('不优秀')
else:
    print('不优秀')
```

输出结果：

```
不优秀
```

当然这只是为了说明 if 条件语句是可以嵌套的。如果是这个需求，我个人还是不太建议这样使用 if 嵌套的，因为这样代码量多了，而且嵌套太多，也不方便阅读代码。



## 6、 Python 3.10+ 的新写法：match / case ##

各位童鞋，如果你用的是 Python 3.10 或者更新的版本，那么除了 `if / elif / else` 之外，还多了一个更直观的家伙—— `match / case`，叫做「结构化模式匹配」（structural pattern matching）。

为什么要专门讲它啊？

我们先看一个需求，假设水哥想根据后台返回的「指令字符串」来做不同的事情：

```python
command = 'start'

if command == 'start':
    print('启动')
elif command == 'stop':
    print('停止')
elif command == 'pause':
    print('暂停')
else:
    print('未知指令')
```

输出的结果：

```
启动
```

这样写没毛病，但是当分支多起来的时候，一长串 `elif` 就显得啰嗦了。我们用 `match / case` 重写一下：

```python
command = 'start'

match command:
    case 'start':
        print('启动')
    case 'stop':
        print('停止')
    case 'pause':
        print('暂停')
    case _:
        print('未知指令')
```

输出的结果：

```
启动
```

这里的 `case _` 就是兜底分支，相当于 `else`，下划线 `_` 是个通配符，匹配任何还没被前面 case 命中的情况。

看到这里，善于思考的你可能会问：那这跟 `switch / case` 不就一样吗？换个语法糖而已嘛。

并不是的， `match / case` 真正的厉害之处，是它能匹配「结构」，不仅仅是「值」。

来看一个序列匹配的例子，假设产品反馈过来一个坐标数据：

```python
point = [10, 20]

match point:
    case [0, 0]:
        print('原点')
    case [x, 0]:
        print(f'在 x 轴上，x = {x}')
    case [0, y]:
        print(f'在 y 轴上，y = {y}')
    case [x, y]:
        print(f'普通点，x = {x}，y = {y}')
    case _:
        print('不是二维坐标')
```

输出的结果：

```
普通点，x = 10，y = 20
```

是不是发现，这里不光匹配到了「这是一个长度为 2 的列表」，还顺手把 `x` 、 `y` 给「解包」出来了，下面分支里直接就能用。

序列里还可以用 `*rest` 来收集剩下的元素：

```python
nums = [1, 2, 3, 4, 5]

match nums:
    case [first, *rest]:
        print(f'第一个：{first}，剩下的：{rest}')
```

输出的结果：

```
第一个：1，剩下的：[2, 3, 4, 5]
```

那么字典呢？

`match / case` 也能匹配字典的「形状」：

```python
response = {'status': 'ok', 'data': [1, 2, 3]}

match response:
    case {'status': 'ok', 'data': data}:
        print(f'成功，拿到数据 {data}')
    case {'status': 'error', 'message': msg}:
        print(f'失败：{msg}')
    case _:
        print('未知响应')
```

输出的结果：

```
成功，拿到数据 [1, 2, 3]
```

更有意思的是，`match / case` 还能跟「类」一起用，配合 `dataclass` 食用，效果更佳：

```python
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


p = Point(0, 5)

match p:
    case Point(x=0, y=0):
        print('原点')
    case Point(x=0, y=y):
        print(f'在 y 轴上，y = {y}')
    case Point(x=x, y=0):
        print(f'在 x 轴上，x = {x}')
    case Point(x=x, y=y):
        print(f'普通点 ({x}, {y})')
```

输出的结果：

```
在 y 轴上，y = 5
```

最后，再介绍一个小特性，叫「守卫条件」（guard），就是在 `case` 后面加一个 `if`：

```python
score = 75

match score:
    case x if x >= 90:
        print('优秀')
    case x if x >= 80:
        print('良好')
    case x if x >= 60:
        print('及格')
    case _:
        print('不及格')
```

输出的结果：

```
及格
```

是不是发现，有了 `match / case` 之后，代码更结构化也更好读了？

这里也啰嗦一句，`match / case` 不是用来取代 `if / elif` 的。简单的「值比较」、「真假判断」，老老实实写 `if` 反而更清楚；只有当你要根据「数据的结构」来分发逻辑的时候，比如解析 JSON、处理 AST、写解释器之类的场景，`match / case` 才能真正发挥威力。

# 二、循环语句 #



## 1、什么是循环语句 ##

一般编程语言都有循环语句，为什么呢？

那就问一下自己，我们弄程序是为了干什么？

那肯定是为了方便我们工作，优化我们的工作效率啊。

而计算机和人类不同，计算机不怕苦也不怕累，也不需要休息，可以一直做。

你要知道，计算机最擅长就是做重复的事情。

所以这时候需要用到循环语句，循环语句允许我们执行一个语句或语句组多次。

循环语句的一般形式如下：

![循环的基本流程](../assets/diagrams/while-flow.svg)


在 Python 提供了 for 循环和 while 循环。

这里又有一个问题了，如果我想让他运行了一百次之后停止，那该怎么做呢？

这时候需要用到一些控制循环的语句：

|循环控制语句|描述|
|------|------|
|break|在语句块执行过程中终止循环，并且跳出整个循环|
|continue|在语句块执行过程中终止当前循环，跳出该次循环，执行下一次循环|
|pass|pass 是空语句，是为了保持程序结构的完整性|

这些控制语句是为了让我们告诉程序什么时候停止，什么时候不运行这次循环。




## 2、 for 循环语句 ##

我们先来看下 for 循环语句。

它的流程图基本如下：


![for 循环遍历序列](../assets/diagrams/for-flow.svg)


基本的语法格式：

<!-- skip-ci -->
```python
for iterating_var in sequence:
   statements(s)
```

那么我们根据他的基本语法格式，随便写个例子测试一下：


```python
for letter in 'Hello 两点水':
    print(letter)
```

输出的结果如下：

```txt
H
e
l
l
o

两
点
水
```

从打印结果来看，它就是把字符串 `Hello 水哥`  一个一个字符的打印出来。

那如果我们把字符串换为字典 dict 呢？

```python
dict = {'一点水': '小学生', '两点水': '初中生', '三点水': '高中生'}

for i in dict:
    print(i)
```

打印结果：

```
一点水
两点水
三点水
```

你会发现只打印了字典 dict 中的每一个 key 值。

很多时候，我都是建议大家学到一个新的知识点，都多去尝试。

你尝试一遍，自己观察出来的结论，好过别人说十遍。

如果你不知道怎么去试？

可以根据我们的例子举一反三，比如上面的 for 循环，试了字符串，字典，那我们之前学的基本数据类型还有什么呢？

不记得可以再返回去看看，可以把所有的基本类型都拿去尝试一下。

比如，你试了之后，会发现整数和浮点数是不可以直接放在 for 循环里面的。

<!-- skip-ci -->
```python
a = 100

b = 0.01

for i in a:
    print(i)

for i in b:
    print(i)
```

运行后会报错：

```
Traceback (most recent call last):
  File "/Users/twowater/dev/python/test/com/twowater/test.py", line 5, in <module>
    for i in a:
TypeError: 'int' object is not iterable
```






## 3、 range() 函数 ##

for 循环还常常和 range() 函数搭配使用的。

如果不知道 range() 函数 , 我们直接通过一段程序来理解。

```python
for i in range(3):
    print(i)
```

打印的结果为：

```
0
1
2
```

可见，打印了  0 到 3 。

使用 range(x) 函数，就可以生成一个从 0 到 x-1 的整数序列。

如果是 `range(a,b)`  函数，你可以生成了一个左闭右开的整数序列。

其实例子中的  `range(3)` 可以写成 `range(0,3)`, 结果是一样的。

其实使用 range() 函数，我们更多是为了把一段代码重复运行 n 次。

这里提个问题，你仔细观察 range()  函数，上面说到的不管是 1 个参数的，还是 2 个参数的都有什么共同的特点？

不知道你们有没有发现，他都是每次递增 1 的。

`range(3)` 就是 0 ，1，2  ，每次递增 1 。

`range(3,6)`  就是 3 ，4 ，5 ，也是每次递增 1 的。

那能不能每次不递增 1 呢？

比如我想递增 2 呢？

在程序的编写中，肯定会遇到这样的需求的。而 python 发展至今，range 函数肯定也会有这种功能。

所以 range 函数还有一个三个参数的。

比如  `range(0,10,2) ` , 它的意思是：从 0 数到 10（不取 10 ），每次间隔为 2 。

```python
for i in range(0, 10, 2):
    print(i)
```

打印的结果为：

```
0
2
4
6
8
```


 
 
 

## 4、While 循环语句 ##

While 循环和 for 循环的作用是一样的。

我们先来看看 While 循环语句的样子。

```python
count = 1
sum1 = 0

while count <= 100:    # 条件语句
    sum1 = sum1 + count    # while 子句
    count = count + 1

print(sum1)
```

程序输出的结果是：

```txt
5050
```

这个例子是计算 1 到 100 所有整数的和。



## 5、for 循环和 whlie 循环的区别 ##

之前也提到过了，如果一种语法能表示一个功能，那没必要弄两种语法来表示。

竟然都是循环，for 循环和 while 循环肯定有他们的区别的。

那什么时候才使用 for 循环和 while 循环呢？

* for 循环主要用在迭代可迭代对象的情况。

* while 循环主要用在需要满足一定条件为真，反复执行的情况。
（死循环+break 退出等情况。）

* 部分情况下，for 循环和 while 循环可以互换使用。

例如：

```python
for i in range(0, 10):
    print(i)


i = 0
while i < 10:
    print(i)
    i = i + 1
```

虽然打印的结果是一样的，但是细细品味你会发现，他们执行的顺序和知道的条件是不同的。



## 6、嵌套循环 ##

循环语句和条件语句一样，都是可以嵌套的。

具体的语法如下：

**for 循环嵌套语法**

<!-- skip-ci -->
```python
for iterating_var in sequence:
   for iterating_var in sequence:
      statements(s)
   statements(s)
```

**while 循环嵌套语法**

<!-- skip-ci -->
```python
while expression:
   while expression:
      statement(s)
   statement(s)
```

除此之外，你也可以在循环体内嵌入其他的循环体，如在 while 循环中可以嵌入 for 循环， 反之，你可以在 for 循环中嵌入 while 循环

比如：

当我们需要判断 sum 大于 1000 的时候，不在相加时，可以用到 break ，退出整个循环。

```python
count = 1
sum = 0
while (count <= 100):
    sum = sum + count
    if ( sum > 1000):  #当 sum 大于 1000 的时候退出循环
        break
    count = count + 1
print(sum)
```

输出的结果：

```txt
1035
```

有时候，我们只想统计 1 到 100 之间的奇数和，那么也就是说当 count 是偶数，也就是双数的时候，我们需要跳出当次的循环，不想加，这时候可以用到 break

```python
count = 1
sum = 0
while (count <= 100):
    if ( count % 2 == 0):  # 双数时跳过输出
        count = count + 1
        continue
    sum = sum + count
    count = count + 1
print(sum)
```

输出的语句：

```txt
2500
```

还有：

```python
for num in range(10,20):  # 迭代 10 到 20 之间的数字
   for i in range(2,num): # 根据因子迭代
      if num%i == 0:      # 确定第一个因子
         j=num/i          # 计算第二个因子
         print (f'{num} 是一个合数')
         break            # 跳出当前循环
   else:                  # 循环的 else 部分
      print (f'{num} 是一个质数')
```

输出的结果：

```txt
10 是一个合数
11 是一个质数
12 是一个合数
13 是一个质数
14 是一个合数
15 是一个合数
16 是一个合数
17 是一个质数
18 是一个合数
19 是一个质数
```


当然，这里还用到了  `for … else`  语句。

其实 for 循环中的语句和普通的没有区别，else 中的语句会在循环正常执行完（即 for 不是通过 break 跳出而中断的）的情况下执行。

当然有 `for … else`  ，也会有   `while … else` 。他们的意思都是一样的。

# 三、条件语句和循环语句综合实例 #

## 1、打印九九乘法表 ##

```python
# -*- coding: UTF-8 -*-

# 打印九九乘法表
for i in range(1, 10):
        for j in range(1, i+1):
            # 使用 f-string 直接在字符串前加 f，大括号里写表达式即可被求值并插入到字符串中
            print(f'{i}x{j}={i*j}\t', end='')
        print()
```

输出的结果:

```txt
1x1=1   
2x1=2   2x2=4   
3x1=3   3x2=6   3x3=9   
4x1=4   4x2=8   4x3=12  4x4=16  
5x1=5   5x2=10  5x3=15  5x4=20  5x5=25  
6x1=6   6x2=12  6x3=18  6x4=24  6x5=30  6x6=36  
7x1=7   7x2=14  7x3=21  7x4=28  7x5=35  7x6=42  7x7=49  
8x1=8   8x2=16  8x3=24  8x4=32  8x5=40  8x6=48  8x7=56  8x8=64  
9x1=9   9x2=18  9x3=27  9x4=36  9x5=45  9x6=54  9x7=63  9x8=72  9x9=81 
```


## 2、判断是否是闰年 ##

<!-- skip-ci -->
```python

# 判断是否是闰年

year = int(input("请输入一个年份: "))
if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
    print(f'{year} 是闰年')
else:
     print(f'{year} 不是闰年')

```





## 先把手工统计步骤写出来

我们准备统计学习时间。记录里可能有 `0`，也可能有录入错误的负数。先约定：零分钟允许保留，负数暂时跳过。那手工会怎么做？从零开始，逐条查看，只把符合要求的记录加进去。

```python
records = [15, 0, 10, -3]
total = 0
valid_count = 0
for minutes in records:
    if minutes < 0:
        continue
    total = total + minutes
    valid_count = valid_count + 1
print(total)
print(valid_count)
```

输出：

```text
25
3
```

别只看总数，沿着循环把每一步的 `minutes`、`total` 和 `valid_count` 写下来。零分钟虽然不增加合计，仍然是一条有效记录，所以有效条数是 `3`。

自己试两种边界：空列表应该得到 `0` 和 `0`；全是负数的列表也一样。如果把判断改成 `minutes <= 0`，合计可能没变，但条数会变。这说明输出中的某一个数字正确，并不等于程序完全符合需求。

这里跳过负数是这个练习的业务约定，不是所有程序都该悄悄跳过错误。学到异常处理时，我们会改成向调用方说明哪里不符合要求。
