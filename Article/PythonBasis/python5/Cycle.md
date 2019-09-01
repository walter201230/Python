# 二、循环语句 #

一般编程语言都有循环语句，循环语句允许我们执行一个语句或语句组多次。

循环语句的一般形式如下：

![python循环语句](http://upload-images.jianshu.io/upload_images/2136918-eaaae2fbfec3330f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Python 提供了 for 循环和 while 循环，当然还有一些控制循环的语句：

|循环控制语句|描述|
|------|------|
|break|在语句块执行过程中终止循环，并且跳出整个循环|
|continue|在语句块执行过程中终止当前循环，跳出该次循环，执行下一次循环|
|pass|pass 是空语句，是为了保持程序结构的完整性|


## 1、While 循环语句 ##


```python
count = 1
sum = 0
while (count <= 100):
    sum = sum + count
    count = count + 1
print(sum)
```

输出的结果：

```txt
5050
```

当然 while 语句时还有另外两个重要的命令 continue，break 来跳过循环，continue 用于跳过该次循环，break 则是用于退出循环

比如，上面的例子是计算 1 到 100 所有整数的和，当我们需要判断 sum 大于 1000 的时候，不在相加时，可以用到 break ，退出整个循环

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

在 Python 的 while 循环中，还可以使用 else 语句，while … else 在循环条件为 false 时执行 else 语句块

比如：

```python
count = 0
while count < 5:
   print (count)
   count = count + 1
else:
   print (count)
```

输出的结果：

```txt
0
1
2
3
4
5
```

## 2、 for 循环语句 ##

 for循环可以遍历任何序列的项目，如一个列表或者一个字符串

它的流程图基本如下：


![for循环的流程图](http://upload-images.jianshu.io/upload_images/2136918-a0728c1c488238af?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

基本的语法格式：

```python
for iterating_var in sequence:
   statements(s)
```

实例：

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

有 while … else 语句，当然也有 for … else  语句啦，for 中的语句和普通的没有区别，else 中的语句会在循环正常执行完（即 for 不是通过 break 跳出而中断的）的情况下执行，while … else 也是一样。

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

## 3、嵌套循环 ##

Python 语言允许在一个循环体里面嵌入另一个循环。上面的实例也是使用了嵌套循环的，这里就不给出实例了。

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
