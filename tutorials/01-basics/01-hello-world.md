# 第 1 章：第一个 Python 程序

# 前言 #

每个编程语言的学习，第一个程序都是先向世界问好，Python 也不例外，这节我们先写下第一个 Python 程序 —— Hello World 。

# 目录 #


- 一、Python 简介
- 二、Python 的安装
- 三、第一个 Python 程序
- 四、集成开发环境（IDE）：PyCharm

# 一、Python 简介 #

Python 是著名的“龟叔” Guido van Rossum 在 1989 年圣诞节期间，为了打发无聊的圣诞节而编写的一个编程语言。牛人就是牛人，为了打发无聊时间竟然写了一个这么牛皮的编程语言。

现在，全世界差不多有 600 多种编程语言，但流行的编程语言也就那么 20 来种。不知道你有没有听说过 TIOBE 排行榜。

这是 2017 年 2 月编程语言排行榜 TOP20 榜单：

| Feb 2017 | Feb 2016 | Change | Programming Language | Ratings | Change |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 |  | Java | 16.676% | -4.47% |
| 2 | 2 |  | C | 8.445% | -7.15% |
| 3 | 3 |  | C++ | 5.429% | -1.48% |
| 4 | 4 |  | C# | 4.902% | +0.50% |
| 5 | 5 |  | Python | 4.043% | -0.14% |
| 6 | 6 |  | PHP | 3.072% | +0.30% |
| 7 | 9 | ↑ | JavaScript | 2.872% | +0.67% |
| 8 | 7 | ↓ | Visual Basic .NET | 2.824% | +0.37% |
| 9 | 10 | ↑ | Delphi/Object Pascal | 2.479% | +0.32% |
| 10 | 8 | ↓ | Perl | 2.171% | -0.08% |
| 11 | 11 |  | Ruby | 2.153% | +0.10% |
| 12 | 16 | ↑↑ | Swift | 2.125% | +0.75% |
| 13 | 13 |  | Assembly language | 2.107% | +0.28% |
| 14 | 38 | ↑↑ | Go | 2.105% | +1.81% |
| 15 | 17 | ↑ | R | 1.922% | +0.73% |
| 16 | 12 | ↓↓ | Visual Basic | 1.875% | +0.02% |
| 17 | 18 | ↑ | MATLAB | 1.723% | +0.63% |
| 18 | 19 | ↑ | PL/SQL | 1.549% | +0.49% |
| 19 | 14 | ↓↓ | Objective-C | 1.536% | +0.13% |
| 20 | 23 | ↑ | Scratch | 1.500% | +0.71% |

还有就是 Top 10 编程语言 TIOBE 指数走势：

> TIOBE Programming Community Index（数据来源：[www.tiobe.com](https://www.tiobe.com/tiobe-index/)）从 2002 年到 2017 年的走势显示：Java 长期处于 15% ~ 25% 的高位，与 C 语言交替领跑；C 语言整体呈缓慢下行趋势；C++ 从 15% 一路下滑到 5% 左右；Python、PHP、JavaScript、C# 等长期在 2% ~ 10% 区间内此起彼伏；而 Perl、Visual Basic .NET、Delphi/Object Pascal 等则逐渐式微。

总的来说，这几种编程语言各有千秋，但不难看出，最近几年 Python 的发展非常的快，特别最近流行的机器学习，数据分析，更让 python 快速的发展起来。

Python 是高级编程语言，它有一个特点就是能快速的开发。Python 为我们提供了非常完善的基础代码库，覆盖了网络、文件、GUI、数据库、文本等大量内容，被形象地称作“内置电池（batteries included）”。用 Python 开发，许多功能不必从零编写，直接使用现成的即可。而且 Python 还能开发网站，多大型网站就是用 Python 开发的，例如 YouTube、Instagram，还有国内的豆瓣。很多大公司，包括 Google、Yahoo 等，甚至 NASA（美国航空航天局）都大量地使用 Python。

当然，任何编程语言有有点，也有缺点，Python 也不例外。那么 Python 有哪些缺点呢？

第一个缺点就是运行速度慢，和C程序相比非常慢，因为Python是解释型语言，你的代码在执行时会一行一行地翻译成CPU能理解的机器码，这个翻译过程非常耗时，所以很慢。而C程序是运行前直接编译成CPU能执行的机器码，所以非常快。

第二个缺点就是代码不能加密。如果要发布你的 Python 程序，实际上就是发布源代码。像 JAVA , C 这些编译型的语言，都没有这个问题，而解释型的语言，则必须把源码发布出去。

# 二、Python 的安装 #

> 下面的截图和命令以 Python 3.6／3.7 为例，当前安装界面可能不同。准备后续练习时，请从 [Python 官方下载页](https://www.python.org/downloads/) 选择仍受维护的 Python 3，并核对各章标明的最低版本；安装完成后用 `python3 --version`（Windows 也可用 `py --version`）确认实际运行的解释器。路径应以自己的安装位置为准。

因为 Python 是跨平台的，它可以运行在 Windows、Mac 和各种 Linux/Unix 系统上。目前，Python 有两个版本，一个是 2.x 版，一个是 3.x版，这两个版本是不兼容的。本草根安装的是 3.6.1 版本的。

至于在哪里下载，草根我建议大家最好直接官网下载，随时下载下来的都是最新版本。官网地址：[https://www.python.org/](https://www.python.org/)

## 1、windows 系统下安装配置 ##

如果是 windows 系统，下载完后，直接安装，不过这里记得勾上Add Python 3.6 to PATH，然后点 「Install Now」 即可完成安装。

这里要注意了，记得把「Add Python 3.6 to Path」勾上，勾上之后就不需要自己配置环境变量了，如果没勾上，就要自己手动配置。

在 「Install Python 3.6.1 (64-bit)」 安装向导中，你会看到两个安装选项：

- 「Install Now」：使用默认设置安装，默认路径是 `C:\Users\Administrator\AppData\Local\Programs\Python\Python36`，会自带 IDLE 、pip 和文档，并创建快捷方式和文件关联。
- 「Customize installation」：自定义安装路径和功能。

无论选哪个，安装界面下方都有两个勾选框，一个是「Install launcher for all users (recommended)」，另一个就是「Add Python 3.6 to PATH」 。**勾上这个就不用自己配置环境变量了**，所以这一步千万别忘。

如果你一时手快，忘记了勾上 「Add Python 3.6 to Path」，那也不要紧，只需要手动配置一下环境变量就好了。

在命令提示框中 cmd  上输入 ：

```
path=%path%;C:\Python 
```

特别特别注意： `C:\Python` 是 Python 的安装目录，如果你的安装目录是其他地方，就得填上你对应的目录。

安装完成后，打开命令提示符窗口，敲入 python 后，出现下面的情况，证明 Python 安装成功了。

```
C:\Users\Administrator>python
Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

而你看到提示符 `>>>` 就表示我们已经在 Python 交互式环境中了，可以输入任何 Python 代码，回车后会立刻得到执行结果。


## 2、Mac 系统下安装配置 ##

MAC 系统一般都自带有 Python2.x 版本的环境，不过现在都不用 2.x 的版本了，所以建议你在 https://www.python.org/downloads/mac-osx/ 上下载最新版安装。

安装完成之后，如何配置环境变量呢？

先查看当前环境变量：

``` 
echo $PATH
```

然后打开 ``` ~/.bash_profile(没有请新建) ```

``` 
vi ~/.bash_profile
``` 

我装的是 Python3.7 ，Python 执行路径为：`/Library/Frameworks/Python. Framework/Versions/3.7/bin` 。于是写入

```
export PATH="/Library/Frameworks/Python. Framework/Versions/3.7/bin:$PATH"
```

写入后 `~/.bash_profile` 文件大致是下面这个样子（以草根本机的配置为例）：

```bash
# Setting PATH for Python 3.6
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"
export PATH
```

最后保存退出，激活运行一下文件：

```
source ~/.bash_profile
```

# 三、第一个 Python 程序 #

好了，说了那么多，现在我们可以来写一下第一个 Python 程序了。

一开始写 Python 程序，个人不太建议用专门的工具来写，不方便熟悉语法，所以这里我先用 [Sublime Text](http://www.sublimetext.com/) 来写，后期可以改为用 PyCharm 。

第一个 Python 程序当然是打印 Hello Python 啦。

如果你没编程经验，什么都不懂，没关系，第一个 Python 程序，只要跟着做，留下个印象，尝试一下就好。

新建一个文件，命名为 `HelloPython.py` , 注意，这里是以 `.py` 为后缀的文件。

然后打开文件，输入 `print('Hello Python')`


```python
print('Hello Python')
```


最后就可以打开命令行窗口，把当前目录切换到 HelloPython.py 所在目录，就可以运行这个程序了，下面就是运行的结果。


```
C:\Users\Administrator>cd C:\Users\Administrator\Desktop\Python

C:\Users\Administrator\Desktop\Python>python HelloPython.py
Hello Python

C:\Users\Administrator\Desktop\Python>
```


当然，如果你是使用  [Sublime Text](http://www.sublimetext.com/) ，并且在安装 Python 的时候配置好了环境变量，直接按 Ctrl + B 就可以运行了，运行结果如下：

这里要注意，记得在 Sublime Text 右下角的语法选择那里，选择 `Python` ，否则按 Ctrl + B 是没法正确执行的。运行后在编辑器底部的输出窗口就能看到结果：

```
Hello Python
[Finished in 0.5s]
```




## 第一行跑通以后，再改一小步

前面的程序已经能打印文字了。各位先自己写下想看到的两行结果，再把下面的文字改成自己的版本：

```python
print('今天开始学 Python')
print('先完成一个能运行的小例子')
```

输出：

```text
今天开始学 Python
先完成一个能运行的小例子
```

这次先只改引号里面的文字，运行后核对是不是两行。接着故意少写一个右括号，再运行一次，观察报错。读报错时先找错误类型和代码位置，不要马上把整段代码删掉重写。把括号补回来，再次运行，确认问题消失。这就是一次很小、但完整的「改动、观察、修复」。

这里的引号和括号是 Python 语法，使用英文半角符号；引号里面是我们要显示的文字，可以写中文。输出中的中文标点不会因为是全角就变成语法错误。

浏览器里运行能让我们先专心看代码。等你要做本地文件或命令行练习时，再按安装章节准备环境。先选一个能运行程序的编辑器即可，不需要为了第一行代码把所有编辑器都装一遍。

# 四、集成开发环境（IDE）: PyCharm #

我本人一直是建议在学习周期使用文本编辑器或者是[Sublime Text](http://www.sublimetext.com/) 这个工具来写 Python 程序的，因为这样有利于我们了解整个流程。

当然，如果你有一定的编程基础，是可以使用集成的开发环境的，这样可以提高效率。这时，你可以选择 PyCharm ，PyCharm 是由 JetBrains 打造的一款 Python IDE，支持 macOS、 Windows、 Linux 系统。

PyCharm 下载地址 : [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)
