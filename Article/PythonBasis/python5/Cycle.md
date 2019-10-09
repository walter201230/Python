# 二、循环语句 #



## 1、什么是循环语句 ##

一般编程语言都有循环语句，为什么呢？

那就问一下自己，我们弄程序是为了干什么？

那肯定是为了方便我们工作，优化我们的工作效率啊。

而计算机和人类不同，计算机不怕苦也不怕累，也不需要休息，可以一直做。

你要知道，计算机最擅长就是做重复的事情。

所以这时候需要用到循环语句，循环语句允许我们执行一个语句或语句组多次。

循环语句的一般形式如下：

![python循环语句](http://upload-images.jianshu.io/upload_images/2136918-eaaae2fbfec3330f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


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


![for循环的流程图](http://upload-images.jianshu.io/upload_images/2136918-a0728c1c488238af?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


基本的语法格式：

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

从打印结果来看，它就是把字符串 `Hello 两点水`  一个一个字符的打印出来。

那如果我们把字符串换为字典 dict 呢？

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-094741.png)

你会发现只打印了字典 dict 中的每一个 key 值。

很多时候，我都是建议大家学到一个新的知识点，都多去尝试。

你尝试一遍，自己观察出来的结论，好过别人说十遍。

如果你不知道怎么去试？

可以根据我们的例子举一反三，比如上面的 for 循环，试了字符串，字典，那我们之前学的基本数据类型还有什么呢？

不记得可以再返回去看看，可以把所有的基本类型都拿去尝试一下。

比如，你试了之后，会发现整数和浮点数是不可以直接放在 for 循环里面的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-095313.png)






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

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-09-065854.png)


 
 
 

## 4、While 循环语句 ##

While 循环和 for 循环的作用是一样的。

我们先来看看 While 循环语句的样子。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-083137.png)

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

```python
for iterating_var in sequence:
   for iterating_var in sequence:
      statements(s)
   statements(s)
```

**while 循环嵌套语法**

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
         print ('%d 是一个合数' % num)
         break            # 跳出当前循环
   else:                  # 循环的 else 部分
      print ('%d 是一个质数' % num)
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


