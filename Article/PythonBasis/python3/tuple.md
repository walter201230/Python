# 二、tuple（元组） #

## 1、什么是元组 （tuple） ##

上一节刚说了一个有序列表 List ，现在说另一种有序列表叫元组：tuple 。

tuple 和 List 非常类似，但是 tuple 一旦初始化就不能修改。
也就是说元组（tuple）是不可变的，那么不可变是指什么意思呢？

元组（tuple） 不可变是指当你创建了 tuple 时候，它就不能改变了，也就是说它也没有 append()，insert() 这样的方法，但它也有获取某个索引值的方法，但是不能赋值。

那么为什么要有 tuple 呢？

那是因为 tuple 是不可变的，所以代码更安全。

所以建议能用 tuple 代替 list 就尽量用 tuple 。



## 2、怎样创建元组（tuple） ##

元组创建很简单，只需要在括号中添加元素，并使用逗号隔开即可。

```python
tuple1=('两点水','twowter','liangdianshui',123,456)
tuple2='两点水','twowter','liangdianshui',123,456
```

创建空元组

```python
tuple3=()
```

元组中只包含一个元素时，需要在元素后面添加逗号

```python
tuple4=(123,)
```

如果不加逗号，创建出来的就不是 元组（tuple），而是指 ```123``` 这个数了。


这是因为括号 () 既可以表示元组（tuple），又可以表示数学公式中的小括号，这就产生了歧义。

所以如果只有一个元素时，你不加逗号，计算机就根本没法识别你是要进行整数或者小数运算还是表示元组。

因此，Python 规定，这种情况下，按小括号进行计算，计算结果自然是 ```123``` ，而如果你要表示元组的时候，就需要加个逗号。

具体看下图 tuple4 和 tuple5 的输出值

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-093847.jpg)







## 3、如何访问元组（tuple） ##

元组下标索引也是从 0 开始，元组（tuple）可以使用下标索引来访问元组中的值。

```python
#-*-coding:utf-8-*-

tuple1=('两点水','twowter','liangdianshui',123,456)
tuple2='两点水','twowter','liangdianshui',123,456

print(tuple1[1])
print(tuple2[0])
```

输出的结果：

![访问 tuple](http://upload-images.jianshu.io/upload_images/2136918-edfb7c9ebc7d5ab0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





## 4、修改元组 （tuple） ##

可能看到这个小标题有人会疑问，上面不是花了一大段来说 tuple 是不可变的吗？

这里怎么又来修改 tuple （元组） 了。

那是因为元组中的元素值是不允许修改的，但我们可以对元组进行连接组合，还有通过修改其他列表的值从而影响 tuple 的值。

具体看下面的这个例子：

```python
#-*-coding:utf-8-*-
list1=[123,456]
tuple1=('两点水','twowater','liangdianshui',list1)
print(tuple1)
list1[0]=789
list1[1]=100
print(tuple1)
```

输出的结果：
```
('两点水', 'twowater', 'liangdianshui', [123, 456])
('两点水', 'twowater', 'liangdianshui', [789, 100])
```


可以看到，两次输出的 tuple 值是变了的。我们看看 tuple1 的存储是怎样的。


![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-%E4%BF%AE%E6%94%B9tuple%E6%B5%81%E7%A8%8B%E5%9B%BE.png)


可以看到，tuple1 有四个元素，最后一个元素是一个 List ，List 列表里有两个元素。

当我们把 List 列表中的两个元素 `124` 和 `456` 修改为 `789` 和 `100` 的时候，从输出来的 tuple1 的值来看，好像确实是改变了。

但其实变的不是 tuple 的元素，而是 list 的元素。

tuple 一开始指向的 list 并没有改成别的 list，所以，tuple 所谓的“不变”是说，tuple 的每个元素，指向永远不变。注意是 tupe1 中的第四个元素还是指向原来的 list ，是没有变的，我们修改的只是列表 List 里面的元素。



## 5、删除 tuple （元组） ##

tuple 元组中的元素值是不允许删除的，但我们可以使用 del 语句来删除整个元组

```python
#-*-coding:utf-8-*-

tuple1=('两点水','twowter','liangdianshui',[123,456])
print(tuple1)
del tuple1
```

## 6、tuple （元组）运算符 ##

与字符串一样，元组之间可以使用 `+` 号和 `*` 号进行运算。这就意味着他们可以组合和复制，运算后会生成一个新的元组。

|Python 表达式|结果|描述|
|-----------|-----|-----|
|len((1, 2, 3))|3|计算元素个数|
|(1, 2, 3) + (4, 5, 6)|(1, 2, 3, 4, 5, 6)|连接|
|('Hi!',) * 4|('Hi!', 'Hi!', 'Hi!', 'Hi!')|复制|
|3 in (1, 2, 3)|True|元素是否存在|
|for x in (1, 2, 3):  print(x)|1 2 3|迭代|

## 7、元组内置函数 ##

|方法|描述|
|----|----|
|len(tuple)|计算元组元素个数|
|max(tuple)|返回元组中元素最大值|
|min(tuple)|返回元组中元素最小值|
|tuple(seq)|将列表转换为元组|


## 8、实例 ##

最后跟列表一样，来一个实例，大家也可以多尝试，去把元组的各种玩法玩一遍。

```python
name1 = ('一点水', '两点水', '三点水', '四点水', '五点水')

name2 = ('1点水', '2点水', '3点水', '4点水', '5点水')

list1 = [1, 2, 3, 4, 5]

# 计算元素个数
print(len(name1))
# 连接,两个元组相加
print(name1 + name2)
# 复制元组
print(name1 * 2)
# 元素是否存在 (name1 这个元组中是否含有一点水这个元素)
print('一点水' in name1)
# 元素的最大值
print(max(name2))
# 元素的最小值
print(min(name2))
# 将列表转换为元组
print(tuple(list1))
```

输出的结果如下：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-101523.png)








