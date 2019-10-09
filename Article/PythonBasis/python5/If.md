# 一、条件语句 #


## 1、什么是条件语句 ##


Python 条件语句跟其他语言基本一致的，都是通过一条或多条语句的执行结果（ True 或者 False ）来决定执行的代码块。

Python 程序语言指定任何非 0 和非空（null）值为 True，0 或者 null 为 False。

执行的流程图如下：

![if语句流程图](http://upload-images.jianshu.io/upload_images/2136918-4ee2486190450a1a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 2、if 语句的基本形式 ##

Python 中，if 语句的基本形式如下：

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

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-072713.png)

可见，把结果打印出来了。

那如果我们把 `num ` 改为空字符串呢？

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-072941.png)

很明显，空字符串是为 False 的，不符合条件语句，因此不会执行到  `print('Hello Python')`  这段代码。

还有再啰嗦一点，提醒一下，在条件判断代码中的冒号 `:` 后、下一行内容是一定要缩进的。不缩进是会报错的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-073432.png)

冒号和缩进是一种语法。它会帮助 Python 区分代码之间的层次，理解条件执行的逻辑及先后顺序。



## 3、if 语句多个判断条件的形式 ##

有些时候，我们的判断语句不可能只有两个，有些时候需要多个，比如上面的例子中大于 60 的为及格，那我们还要判断大于 90 的为优秀，在 80 到 90 之间的良好呢？

这时候需要用到 if 语句多个判断条件，

用伪代码来表示：

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

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-09-07-080557.png)

当然这只是为了说明 if 条件语句是可以嵌套的。如果是这个需求，我个人还是不太建议这样使用 if 嵌套的，因为这样代码量多了，而且嵌套太多，也不方便阅读代码。





