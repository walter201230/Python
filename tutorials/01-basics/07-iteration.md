# 第 7 章：迭代器和生成器

# 前言 #

这篇内容挺多的，而且比内容不好理解。或许新手看完后，还会一脸懵逼，不过这是正常的，如果你看完后，是迷糊的，那么建议你继续学习后面的内容，等学完，再回来看几次。

注：这也是我第二次修改内容没有改过的章节。

# 目录 #


迭代器和生成器

- 一、迭代
- 二、Python 迭代器
- 三、list 生成式（列表生成式）
    - 1、创建 list 的方式
    - 2、list 生成式的创建
- 四、生成器
    - 1、为什么需要生成器
    - 2、生成器的创建
    - 3、遍历生成器的元素
    - 4、以函数的形式实现生成器
    - 5、打印杨辉三角
- 五、迭代器和生成器综合例子
    - 1、反向迭代
    - 2、同时迭代多个序列

# 一、迭代 #

什么叫做迭代？

比如在 Java 中，我们通过 List 集合的下标来遍历 List 集合中的元素，在 Python 中，给定一个 list 或 tuple，我们可以通过 for 循环来遍历这个 list 或 tuple ，这种遍历就是迭代。

可是，Python 的 `for` 循环抽象程度要高于 Java 的 `for` 循环的，为什么这么说呢？因为 Python 的 `for` 循环不仅可以用在 list 或tuple 上，还可以作用在其他可迭代对象上。

也就是说，只要是可迭代的对象，无论有没有下标，都是可以迭代的。

比如：

```python

# -*- coding: UTF-8 -*-

# 1、for 循环迭代字符串
for char in 'liangdianshui' :
    print ( char , end = ' ' )

print('\n')

# 2、for 循环迭代 list
list1 = [1,2,3,4,5]
for num1 in list1 :
    print ( num1 , end = ' ' )

print('\n')

# 3、for 循环也可以迭代 dict （字典）
dict1 = {'name':'两点水','age':'23','sex':'男'}

for key in dict1 :    # 迭代 dict 中的 key
    print ( key , end = ' ' )

print('\n')

for value in dict1.values() :   # 迭代 dict 中的 value
	print ( value , end = ' ' )

print ('\n')

# 如果 list 里面一个元素有两个变量，也是很容易迭代的
for x , y in [ (1,'a') , (2,'b') , (3,'c') ] :
	print ( x , y )

```

输出的结果如下：

```txt
l i a n g d i a n s h u i 

1 2 3 4 5 

name age sex 

两点水 23 男 

1 a
2 b
3 c
```

# 二、Python 迭代器 #

上面简单的介绍了一下迭代，迭代是 Python 最强大的功能之一，是访问集合元素的一种方式。现在正式进入主题：迭代器，迭代器是一个可以记住遍历的位置的对象。

迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。

迭代器只能往前不会后退。

迭代器有两个基本的方法：iter() 和 next(),且字符串，列表或元组对象都可用于创建迭代器，迭代器对象可以使用常规 for 语句进行遍历，也可以使用 next() 函数来遍历。

具体的实例：

```python
# 1、字符创创建迭代器对象
str1 = 'liangdianshui'
iter1 = iter ( str1 )

# 2、list对象创建迭代器
list1 = [1,2,3,4]
iter2 = iter ( list1 )

# 3、tuple(元祖) 对象创建迭代器
tuple1 = ( 1,2,3,4 )
iter3 = iter ( tuple1 )

# for 循环遍历迭代器对象
for x in iter1 :
    print ( x , end = ' ' )

print('\n------------------------')
 
# next() 函数遍历迭代器
while True :
    try :
        print ( next ( iter3 ) )
    except StopIteration :
        break

```

最后输出的结果：

```txt
l i a n g d i a n s h u i 
------------------------
1
2
3
4
```

# 三、list 生成式（列表生成式） #


## 1、创建 list 的方式 ##

之前经过我们的学习，都知道如何创建一个 list ，可是有些情况，用赋值的形式创建一个 list 太麻烦了，特别是有规律的 list ，一个一个的写，一个一个赋值，太麻烦了。比如要生成一个有 30 个元素的 list ，里面的元素为 1 - 30 。我们可以这样写：

```python
# -*- coding: UTF-8 -*-

list1=list ( range (1,31) )
print(list1)
```

输出的结果：

```txt
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
```

这个其实在之前也有提到过，打印九九乘法表，用这个方法其实就几句代码就可以了，具体可以看之前的这个章节：[条件语句和循环语句综合实例](05-conditions-and-loops.md)

但是，如果用到 list 生成式，可以一句代码就生成九九乘法表了。

你没听错，就是一句代码。

具体实现：

```python
print('\n'.join([' '.join (f'{x}x{y}={x*y:2d}'  for x in range(1,y+1)) for y in range(1,10)]))
```

最后输出的结果：

```txt
1x1= 1
1x2= 2 2x2= 4
1x3= 3 2x3= 6 3x3= 9
1x4= 4 2x4= 8 3x4=12 4x4=16
1x5= 5 2x5=10 3x5=15 4x5=20 5x5=25
1x6= 6 2x6=12 3x6=18 4x6=24 5x6=30 6x6=36
1x7= 7 2x7=14 3x7=21 4x7=28 5x7=35 6x7=42 7x7=49
1x8= 8 2x8=16 3x8=24 4x8=32 5x8=40 6x8=48 7x8=56 8x8=64
1x9= 9 2x9=18 3x9=27 4x9=36 5x9=45 6x9=54 7x9=63 8x9=72 9x9=81
```

不过，这里我们先要了解如何创建 list 生成式

## 2、list 生成式的创建 ##

首先，list 生成式的语法为：

<!-- skip-ci -->
```python
[expr for iter_var in iterable] 
[expr for iter_var in iterable if cond_expr]
```

第一种语法：首先迭代 iterable 里所有内容，每一次迭代，都把 iterable 里相应内容放到iter_var 中，再在表达式中应用该 iter_var 的内容，最后用表达式的计算值生成一个列表。

第二种语法：加入了判断语句，只有满足条件的内容才把 iterable 里相应内容放到 iter_var 中，再在表达式中应用该 iter_var 的内容，最后用表达式的计算值生成一个列表。

其实不难理解的，因为是 list 生成式，因此肯定是用 [] 括起来的，然后里面的语句是把要生成的元素放在前面，后面加 for 循环语句或者 for 循环语句和判断语句。

例子：

```python
# -*- coding: UTF-8 -*-
list1=[x * x for x in range(1, 11)]
print(list1)
```

输出的结果：

```txt
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

可以看到，就是把要生成的元素 x * x 放到前面，后面跟 for 循环，就可以把 list 创建出来。那么 for 循环后面有 if 的形式呢？又该如何理解：

```python
# -*- coding: UTF-8 -*-
list1= [x * x for x in range(1, 11) if x % 2 == 0]
print(list1)
```

输出的结果：

```txt
[4, 16, 36, 64, 100]
```

这个例子是为了求 1 到 10 中偶数的平方根，上面也说到， `x * x` 是要生成的元素，后面那部分其实就是在 for 循环中嵌套了一个 if 判断语句。

那么有了这个知识点，我们也可以猜想出，for 循环里面也嵌套 for 循环。具体示例：

```python
# -*- coding: UTF-8 -*-
list1= [(x+1,y+1) for x in range(3) for y in range(5)] 
print(list1)
```

输出的结果：

```txt
[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]
```

其实知道了 list 生成式是怎样组合的，就不难理解这个东西了。因为 list 生成式只是把之前学习的知识点进行了组合，换成了一种更简洁的写法而已。

# 四、生成器 #

## 1、为什么需要生成器 ##

通过上面的学习，可以知道列表生成式，我们可以直接创建一个列表。

但是，受到内存限制，列表容量肯定是有限的。而且，创建一个包含 1000 万个元素的列表，不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。

**所以，如果列表元素可以按照某种算法推算出来，那我们是否可以在循环的过程中不断推算出后续的元素呢？**

这样就不必创建完整的 list，从而节省大量的空间。

**在 Python 中，这种一边循环一边计算的机制，称为生成器：generator。**

在 Python 中，使用了 yield 的函数被称为生成器（generator）。

跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。

在调用生成器运行的过程中，每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回 yield 的值。并在下一次执行 next()方法时从当前位置继续运行。

那么如何创建一个生成器呢？


## 2、生成器的创建 ##

最简单最简单的方法就是把一个列表生成式的 `[]` 改成 `()`

```python
# -*- coding: UTF-8 -*-
gen= (x * x for x in range(10))
print(gen)
```

输出的结果：

```txt
<generator object <genexpr> at 0x0000000002734A40>
```

创建 List 和 generator 的区别仅在于最外层的 `[]` 和 `()` 。

但是生成器并不真正创建数字列表， 而是返回一个生成器，这个生成器在每次计算出一个条目后，把这个条目“产生” ( yield ) 出来。

生成器表达式使用了“惰性计算” ( lazy evaluation，也有翻译为“延迟求值”，我以为这种按需调用 call by need 的方式翻译为惰性更好一些)，只有在检索时才被赋值（ evaluated ），所以在列表比较长的情况下使用内存上更有效。


那么竟然知道了如何创建一个生成器，那么怎么查看里面的元素呢？

## 3、遍历生成器的元素 ##

按我们的思维，遍历用 for 循环，对了，我们可以试试：

```python
# -*- coding: UTF-8 -*-
gen= (x * x for x in range(10))

for num  in  gen :
	print(num)
```

没错，直接这样就可以遍历出来了。当然，上面也提到了迭代器，那么用 next() 可以遍历吗？当然也是可以的。


## 4、以函数的形式实现生成器 ##

上面也提到，创建生成器最简单最简单的方法就是把一个列表生成式的 `[]` 改成 `()`。为啥突然来个以函数的形式来创建呢？

其实生成器也是一种迭代器，但是你只能对其迭代一次。

这是因为它们并没有把所有的值存在内存中，而是在运行时生成值。你通过遍历来使用它们，要么用一个“for”循环，要么将它们传递给任意可以进行迭代的函数和结构。

而且实际运用中，大多数的生成器都是通过函数来实现的。那么我们该如何通过函数来创建呢？

先不急，来看下这个例子：

```python
# -*- coding: UTF-8 -*-
def my_function():
    for i in range(10):
        print ( i )

my_function()
```

输出的结果：

```txt
0
1
2
3
4
5
6
7
8
9
```

如果我们需要把它变成生成器，我们只需要把 `print ( i )` 改为 `yield i` 就可以了，具体看下修改后的例子：

```python
# -*- coding: UTF-8 -*-
def my_function():
    for i in range(10):
        yield i

print(my_function())
```

输出的结果：

```txt
<generator object my_function at 0x0000000002534A40>
```

但是，这个例子非常不适合使用生成器，发挥不出生成器的特点，生成器的最好的应用应该是：你不想同一时间将所有计算出来的大量结果集分配到内存当中，特别是结果集里还包含循环。因为这样会耗很大的资源。

比如下面是一个计算斐波那契数列的生成器：

<!-- skip-ci -->
```python
# -*- coding: UTF-8 -*-
def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b

# 引用函数
for x in fibon(1000000):
    print(x , end = ' ')
```

运行的效果（输出会一直滚动打印斐波那契数列，前几项是这样的）：

```
1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 ...
```

你看，运行一个这么大的参数，也不会说有卡死的状态，因为这种方式不会使用太大的资源。这里，最难理解的就是 generator 和函数的执行流程不一样。函数是顺序执行，遇到 return 语句或者最后一行函数语句就返回。而变成 generator 的函数，在每次调用 next() 的时候执行，遇到 yield语句返回，再次执行时从上次返回的 yield 语句处继续执行。

比如这个例子：

```python
# -*- coding: UTF-8 -*-
def odd():
    print ( 'step 1' )
    yield ( 1 )
    print ( 'step 2' )
    yield ( 3 )
    print ( 'step 3' )
    yield ( 5 )

o = odd()
print( next( o ) )
print( next( o ) )
print( next( o ) )
```

输出的结果：

```txt
step 1
1
step 2
3
step 3
5
```

可以看到，odd 不是普通函数，而是 generator，在执行过程中，遇到 yield 就中断，下次又继续执行。执行 3 次 yield 后，已经没有 yield 可以执行了，如果你继续打印 `print( next( o ) ) ` ,就会报错的。所以通常在 generator 函数中都要对错误进行捕获。

## 5、打印杨辉三角 ##

通过学习了生成器，我们可以直接利用生成器的知识点来打印杨辉三角：

```python
# -*- coding: UTF-8 -*-
def triangles( n ):         # 杨辉三角形
    L = [1]
    while True:
        yield L
        L.append(0)
        L = [ L [ i -1 ] + L [ i ] for i in range (len(L))]

n= 0
for t in triangles( 10 ):   # 直接修改函数名即可运行
    print(t)
    n = n + 1
    if n == 10:
        break
```

输出的结果为：

```txt
[1]
[1, 1]
[1, 2, 1]
[1, 3, 3, 1]
[1, 4, 6, 4, 1]
[1, 5, 10, 10, 5, 1]
[1, 6, 15, 20, 15, 6, 1]
[1, 7, 21, 35, 35, 21, 7, 1]
[1, 8, 28, 56, 70, 56, 28, 8, 1]
[1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
```





## 为什么第二次遍历什么都没有

前面看过生成器以后，再用学习时间试一次。先预测这三次输出，尤其是最后一次：

```python
def valid_minutes(records):
    for minutes in records:
        if minutes >= 0:
            yield minutes


source = valid_minutes([15, 0, 10])
print(next(source))
print(list(source))
print(list(source))
```

输出：

```text
15
[0, 10]
[]
```

第一次 `next()` 已经取走一个值。随后 `list(source)` 继续往后取，把剩下的值取完。最后仍然是同一个生成器，它不会自动回到开头。

如果要重新遍历，可以再次调用 `valid_minutes(...)` 建立新的生成器；如果要多次使用一份已经算出的结果，可以根据数据量和用途，先把它保存成列表。这两种选择要由实际需求决定。

自己把输入改成 `[-3, 0, 5]`，三次输出应该是 `0`、`[5]` 和 `[]`。如果输入为空，直接 `next(source)` 会抛出 `StopIteration`；可以试 `next(source, '没有记录')`，观察自己是否确实需要这个默认结果。不要把「可迭代」理解成「每次遍历都会自动重新开始」。

# 五、迭代器和生成器综合例子 #

因为迭代器和生成器基本是互通的，因此有些知识点需要综合在一起

## 1、反向迭代 ##

反向迭代，应该也是常有的需求了，比如从一开始迭代的例子里，有个输出 list 的元素，从 1 到 5 的

```python
list1 = [1,2,3,4,5]
for num1 in list1 :
    print ( num1 , end = ' ' )
```

那么我们从 5 到 1 呢？这也很简单， Python 中有内置的函数 `reversed()`

```python
list1 = [1,2,3,4,5]
for num1 in reversed(list1) :
    print ( num1 , end = ' ' )
```

方向迭代很简单，可是要注意一点就是：**反向迭代仅仅当对象的大小可预先确定或者对象实现了 `__reversed__()` 的特殊方法时才能生效。 如果两者都不符合，那你必须先将对象转换为一个列表才行**

其实很多时候我们可以通过在自定义类上实现 `__reversed__()` 方法来实现反向迭代。不过有些知识点在之前的篇节中还没有提到，不过可以相应的看下，有编程基础的，学完上面的知识点应该也能理解的。

```python
# -*- coding: UTF-8 -*-

class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
    	# Forward iterator
        n = self.start
        while n > 0:
            yield n
            n -= 1

    def __reversed__(self):
    	# Reverse iterator
        n = 1
        while n <= self.start:
            yield n
            n += 1

for rr in reversed(Countdown(30)):
    print(rr)
for rr in Countdown(30):
    print(rr)
```

输出的结果是 1 到 30 然后 30 到 1 ，分别是顺序打印和倒序打印

## 2、同时迭代多个序列 ##

你想同时迭代多个序列，每次分别从一个序列中取一个元素。你遇到过这样的需求吗？

为了同时迭代多个序列，使用 zip() 函数，具体示例：

```python
# -*- coding: UTF-8 -*-

names = ['laingdianshui', 'twowater', '两点水']
ages = [18, 19, 20]
for name, age in zip(names, ages):
     print(name,age)
```

输出的结果：

```txt
laingdianshui 18
twowater 19
两点水 20
```

其实 zip(a, b) 会生成一个可返回元组 (x, y) 的迭代器，其中 x 来自 a，y 来自 b。 一旦其中某个序列到底结尾，迭代宣告结束。 因此迭代长度跟参数中最短序列长度一致。注意理解这句话喔，也就是说如果 a ， b 的长度不一致的话，以最短的为标准，遍历完后就结束。

利用 `zip()` 函数，我们还可把一个 key 列表和一个 value 列表生成一个 dict （字典）,如下：

```python
# -*- coding: UTF-8 -*-

names = ['laingdianshui', 'twowater', '两点水']
ages = [18, 19, 20]

dict1= dict(zip(names,ages))

print(dict1)

```


输出如下结果：

```python
{'laingdianshui': 18, 'twowater': 19, '两点水': 20}
```

这里提一下， `zip()` 是可以接受多于两个的序列的参数，不仅仅是两个。
