# 二、print() 函数 #

这里先说一下 `print()` 函数，如果你是新手，可能对函数不太了解，没关系，在这里你只要了解它的组成部分和作用就可以了，后面函数这一块会详细说明的。

`print()` 函数由两部分构成 ：

1.  指令：print
2. 指令的执行对象，在 print 后面的括号里的内容

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-17-074454.png)

而 `print()` 函数的作用是让计算机把你给它的指令结果，显示在屏幕的终端上。这里的指令就是你在 `print()` 函数里的内容。

比如在上一章节中，我们的第一个 Python 程序，打印 `print('Hello Python')`

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-17-080241.png)

它的执行流程如下：

1. 向解释器发出指令，打印 'Hello Python' 
2. 解析器把代码解释为计算器能读懂的机器语言
3. 计算机执行完后就打印结果

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-17-083751.png)

可能这里有人会问，为什么要加单引号，直接  `print(Hello Python)` 不行吗？

如果你写代码过程中，有这样的疑问，直接写一下代码，自己验证一下是最好的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-17-094034.png)

显然，去掉单引号后，运行结果标红了（报错），证明这是不可以的。

主要是因为这不符合 Python 的语法规则，去掉单引号后， Python 解释器根本没法看懂你写的是什么。

所以就报 ` SyntaxError: invalid syntax` 的错误，意思是：语法错误。说明你的语句不合规则。
















