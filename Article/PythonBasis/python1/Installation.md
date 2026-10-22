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
 





