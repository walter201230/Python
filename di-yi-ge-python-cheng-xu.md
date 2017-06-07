# 前言 #

最近开始学习 Python ，故把学习的知识点作个总结归纳。

# 一、Python 简介 #

Python 是著名的“龟叔” Guido van Rossum 在 1989 年圣诞节期间，为了打发无聊的圣诞节而编写的一个编程语言。牛人就是牛人，为了打发无聊时间竟然写了一个这么牛皮的编程语言。

现在，全世界差不多有 600 多种编程语言，但流行的编程语言也就那么 20 来种。不知道你有没有听说过 TIOBE 排行榜。

这是 2017 年 2 月编程语言排行榜 TOP20 榜单：

![2 月编程语言排行榜 TOP20 榜单.png](http://upload-images.jianshu.io/upload_images/2136918-1a4dfdbd699c8b62.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还有就是 Top 10 编程语言 TIOBE 指数走势：

![Top 10 编程语言 TIOBE 指数走势.png](http://upload-images.jianshu.io/upload_images/2136918-2714dba010ea5d75.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

总的来说，这几种编程语言各有千秋，但不难看出，最近几年 Python 的发展非常的快，特别最近流行的机器学习，数据分析，更让 python 快速的发展起来。

Python 是高级编程语言，它有一个特点就是能快速的开发。Python 为我们提供了非常完善的基础代码库，覆盖了网络、文件、GUI、数据库、文本等大量内容，被形象地称作“内置电池（batteries included）”。用 Python 开发，许多功能不必从零编写，直接使用现成的即可。而且 Python 还能开发网站，多大型网站就是用 Python 开发的，例如 YouTube、Instagram，还有国内的豆瓣。很多大公司，包括 Google、Yahoo 等，甚至 NASA（美国航空航天局）都大量地使用 Python。

当然，任何编程语言有有点，也有缺点，Python 也不例外。那么 Python 有哪些缺点呢？

第一个缺点就是运行速度慢，和C程序相比非常慢，因为Python是解释型语言，你的代码在执行时会一行一行地翻译成CPU能理解的机器码，这个翻译过程非常耗时，所以很慢。而C程序是运行前直接编译成CPU能执行的机器码，所以非常快。

第二个缺点就是代码不能加密。如果要发布你的 Python 程序，实际上就是发布源代码。像 JAVA , C 这些编译型的语言，都没有这个问题，而解释型的语言，则必须把源码发布出去。

# 二、Python 的安装 #

因为 Python 是跨平台的，它可以运行在 Windows、Mac 和各种 Linux/Unix 系统上。目前，Python 有两个版本，一个是 2.x 版，一个是 3.x版，这两个版本是不兼容的。本草根安装的是 3.6.1 版本的。

至于在哪里下载，本草根建议最好直接官网下载啦，随时下载下来的都是最新版本。官网地址：[https://www.python.org/](https://www.python.org/)

本草根是 windows 系统，下载完后，直接安装，不过这里记得勾上Add Python 3.6 to PATH，然后点 “Install Now” 即可完成安装。如果没有勾上这个，就必须要自己配置环境变量了，至于如何配置，跟 JAVA 的差不多，具体可以 Google 一下。

![Python安装.png](http://upload-images.jianshu.io/upload_images/2136918-2bf6591f0a12e80b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

安装完成后，打开命令提示符窗口，敲入 python 后，出现下面的情况，证明 Python 安装成功了。你看到提示符 >>> 就表示我们已经在 Python交互式环境中了，可以输入任何 Python 代码，回车后会立刻得到执行结果。

![运行python.png](http://upload-images.jianshu.io/upload_images/2136918-817c22f802e8cfce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 三、第一个 Python 程序 #

Python 的代码使用文本编辑器就可以写了，本草根使用 [Sublime Text](http://www.sublimetext.com/)，第一个 Python 程序当然是 Hello Python 啦，把这句话打印出来。

注意 print 前面不要有任何空格，最后保存下来，可以看到，Python 保存后是一个以 .py 为后缀的文件。

![HelloPython.png](http://upload-images.jianshu.io/upload_images/2136918-f0ec1b2c06d1ab18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


最后就可以打开命令行窗口，把当前目录切换到 HelloPython.py 所在目录，就可以运行这个程序了，下面就是运行的结果。


![运行第一个Python程序.png](http://upload-images.jianshu.io/upload_images/2136918-b7eb043853df29bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


当然，如果你是使用  [Sublime Text](http://www.sublimetext.com/) ，并且在安装 Python 的时候配置好了环境变量，直接按 Ctrl + B 就可以运行了，运行结果如下：

![Sublime运行Python.png](http://upload-images.jianshu.io/upload_images/2136918-a771a2fa1e4c03bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




