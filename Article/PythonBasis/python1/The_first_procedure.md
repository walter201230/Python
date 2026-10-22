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
