
## Virtualenv

### 介绍

在使用 `Python` 开发的过程中，工程一多，难免会碰到不同的工程依赖不同版本的库的问题；亦或者是在开发过程中不想让物理环境里充斥各种各样的库，引发未来的依赖灾难。

因此，我们需要对于不同的工程使用不同的虚拟环境来保持开发环境以及宿主环境的清洁。而 `virtualenv`就是一个可以帮助我们管理不同 `Python` 环境的绝好工具。`virtualenv` 可以在系统中建立多个不同并且相互不干扰的虚拟环境。

### 安装

```
 pip3 install virtualenv
```

这样就成功了

### 使用

#### 创建

假如我们想要用`scrapy`去爬取某个网站的信息，我们不想再宿主环境总安装scrapy以及requests这些包，那我们就可以使用virtualenv了。

假设我们把这个虚拟环境放在`~/workspaces/project_env/spider/`目录下

```
 virtualenv ~/workspaces/project_env/spider/
```

这样虚拟环境就创建好了，我们可以看到在这个目录下油三个目录被建立

*   bin：包含一些在这个虚拟环境中可用的命令，以及开启虚拟环境的脚本 `activate`
*   include：包含虚拟环境中的头文件，包括 `Python` 的头文件
*   lib：这里面就是一些依赖库

#### 激活

```
 source ~/workspaces/project_env/spider/bin/activate
```

此时我们就已经在虚拟环境中了

可以安装一下requests这个模块

```
 pip install requests
```

可以看到很快就成功

#### 退出虚拟环境

```
 deactivate
```

## virtualenvwrapper

### 介绍

我们刚才了解了`virtualenv`，我觉得比较麻烦，每次开启虚拟环境之前要去虚拟环境所在目录下的 `bin` 目录下 `source`一下 `activate`，这就需要我们记住每个虚拟环境所在的目录。

一种可行的解决方案是，将所有的虚拟环境目录全都集中起来，比如放到 `~/virtualenvs/`，并对不同的虚拟环境使用不同的目录来管理。`virtualenvwrapper` 正是这样做的。并且，它还省去了每次开启虚拟环境时候的 `source` 操作，使得虚拟环境更加好用。

### 安装

```
 pip install virtualwrapper
```

这样我们就安装好了可以管理虚拟环境的神器

### 使用

#### 配置

首先需要对`virtualenvwrapper`进行配置:

*   需要指定一个环境变量，叫做`WORKON_HOME`，它是用来存放各种虚拟环境目录的目录
*   需要export vitualenvwrapper这个模块存放的位置
*   需要运行一下它的初始化工具 `virtualenvwrapper.sh`，可通过`which virtualenvwrapper.sh`查看位置，我的在`/usr/local/bin/`

由于每次都需要执行这两步操作，我们可以将其写入终端的配置文件中。

如果使用 `bash`，则添加到 `~/.bashrc` 中

如果使用 `zsh`，则添加到 `~/.zshrc` 中

这样每次启动终端的时候都会自动运行，终端启动之后 `virtualenvwrapper` 就可以用啦

```
 export WORKON_HOME='~/Workspaces/Envs'

 export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3

 source /usr/local/bin/virtualenvwrapper.sh
```


**创建虚拟机**

```
mkvirtualenv env
```

创建虚拟环境完成后，会自动切换到创建的虚拟环境中

当然也可以指定虚拟机的 python 版本

```
mkvirtualenv env -p C:\python27\python.exe
```

**列出虚拟环境列表**

```
workon 或者 lsvirtualenv
```

**启动/切换虚拟环境**

使用 workon [virtual-name] 即可切换到对应的虚拟环境

```
workon [虚拟环境名称]
```


**删除虚拟环境**

```
rmvirtualenv [虚拟环境名称]
```

**离开虚拟环境，和 virutalenv 一样的命令**

```
deactivate
```
