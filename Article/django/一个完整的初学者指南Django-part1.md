>源自：https://simpleisbetterthancomplex.com/series/2017/09/04/a-complete-beginners-guide-to-django-part-1.html

### 一个完整的初学者指南Django - 第1部分

 ![一个完整的初学者指南Django  - 第1部分](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/featured.jpg)


 ![Python 3.6.2](https://img.shields.io/badge/python-3.6.2-brightgreen.svg) ![Django 1.11.4](https://img.shields.io/badge/django-1.11.4-brightgreen.svg)


#### 介绍

![欢迎班](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/Pixton_Comic_Welcome_Class.png)


今天我将开始一个关于 Django 基础知识的新系列教程。这是一个完整的 Django 初学者指南。材料分为七个部分。我们将从安装，开发环境准备，模型，视图，模板，URL 到更高级主题（如迁移，测试和部署）来探索所有基本概念。


我想做一些不同的事情。一个教程，易于遵循，信息丰富和有趣的阅读。因此我想出了在文章中创建一些漫画的想法来说明一些概念和场景。希望你喜欢这种阅读方式！


但在我们开始之前......


我想通过孔夫子的名言来开始我们的课程：

> 我听见了，我就忘了
> 
> 我看见了，我就记得了
> 
> 我去做了，我就理解了

![孔子名言](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/Pixton_Comic_Confucius_Quote.png)

所以，一定要动手！不要只阅读教程。让我们一起来实操，这样你将通过做和练会学习到更多的知识。

* * *

#### 为什么选择 Django？


Django 是一个用 Python 编写的 Web 框架。这个 Web 框架支持动态网站，应用程序和服务开发。它提供了一组工具和功能，可解决许多与 Web 开发相关的常见问题，例如安全功能，数据库访问，会话，模板处理，URL 路由，国际化，本地化等等。


使用诸如 Django 之类的 Web 框架，能使我们能够以标准化的方式快速开发安全可靠的Web 应用程序，从而无需重新开发。


那么，Django 有什么特别之处呢？

对于初学者来说，这是一个 Python Web 开源框架，这意味着您可以从各种各样的开源库中受益。在[python软件资料库(pypi)](https://pypi.python.org/pypi) 中托管了超过 **11.6万** 个的包（按照 2017 年 9 月 6 日的数据）。如果你需要解决一个特定问题的时候，可能已经有相关的库给你使用。

Django 是用 Python 编写的最流行的 Web 框架之一。它可以提供各种功能，例如用于开发和测试的独立 Web 服务器，缓存，中间件系统，ORM，模板引擎，表单处理，基于 Python 单元测试工具的接口。Django 还附带了电池，提供内置应用程序，如认证系统，具有自动生成`CRUD`(增删改除)操作页面的管理界面，生成订阅文档（RSS / Atom），站点地图等。甚至在 Django 中建立了一个地理信息系统（GIS）框架。

而且 Django 的开发得到了 [Django软件基金会的](https://www.djangoproject.com/foundation/)支持，并且由 JetBrains 和 Instagram 等公司赞助。Django 到目前为止，已经持续开发维护超过12年了，这足以证明它是一个成熟，可靠和安全的 Web 框架。

##### 谁在使用Django？

为什么要知道谁在使用 Django 呢？

因为这能很好的让我们了解和知道它能做些什么？

在使用 Django 的最大网站中，有：[Instagram](https://instagram.com/)， [Disqus](https://disqus.com/)，[Mozilla](https://www.mozilla.org/)， [Bitbucket](https://bitbucket.org/)，[Last.fm](https://www.last.fm/)， [National Geographic](http://www.nationalgeographic.com/)。

当然，远远不止上面列举的这些，你可以看下 [Django Sites](https://www.djangosites.org/) 数据库，它们提供了超过 **5000** 个 Django 支持的 Web站点的列表。

顺便说一下，去年在 Django Under The Hood 2016 大会上，Django 核心开发人员Carl Meyer 和 Instagram 员工就[如何在规模上使用Django](https://www.youtube.com/watch?v=lx5WQjXLlq8) 以及它如何支持其增长展开了一次演讲。这是一个长达一个小时的谈话，如果你有兴趣的话，可以去了解下。


* * *

#### 安装

如果我们想开始使用 Django ，那么我们需要安装一些应用程序，包括安装 **Python**，**Virtualenv** 和 **Django**。

![基本设置](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/Pixton_Comic_Basic_Setup.png)


一开始，强烈建议使用虚拟环境，虽然不是强制性的，可是这对于初学者来说，是一个很好的开端.


在使用 Django 开发 Web 站点或 Web 项目时，必须安装外部库以支持开发是非常常见的。使用虚拟环境，您开发的每个项目都会有其独立的环境。所以依赖关系不会发生冲突。它还允许您维护在不同 Django 版本上运行的本地计算机项目。


##### 安装Python 3.6.2

我们想要做的第一件事是安装最新的  Python 发行版，它是 **Python 3.6.2**。至少在我写这篇教程的时候是这样。如果有更新的版本，请与它一起使用。接下来的步骤应该保持大致相同。

我们将使用 Python 3，因为最重要的 Python 库已经移植到 Python 3，并且下一个主要的 Django 版本（2.x）不再支持 Python 2。所以 Python 3 是很有必要的。

在 Mac 中，最好的安装方法就是 [Homebrew](https://brew.sh/)。如果您还没有在Mac 上安装它，请在 **终端** 运行以下命令：

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

如果您没有安装**命令行工具`(Command Line Tools)`**，则 Homebrew 安装可能需要更长一点时间。但它会自动处理，所以不用担心。请坐下来等到安装完成。

当您看到以下消息时，您会知道安装何时完成：


```
==> Installation successful!

==> Homebrew has enabled anonymous aggregate user behaviour analytics.
Read the analytics documentation (and how to opt-out) here:
  https://docs.brew.sh/Analytics.html

==> Next steps:
- Run `brew help` to get started
- Further documentation:
    https://docs.brew.sh
```

请运行以下命令来安装Python 3：

```
brew install python3
```


由于 macOS 已经安装了Python 2，所以在安装 Python 3 之后，您将可以使用这两个版本。

要运行 Python 2，请使用`python`终端中的命令。对于 Python 3，请`python3`改用。

我们可以通过在终端中输入来测试安装：

```
python3 --version
Python 3.6.2
```

![macOS测试Python 3](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/mac/test-python.png)

到此时，Python 已经安装完成了。进入下一步：虚拟环境！

##### 安装 Virtualenv

接下来这一步，我们将通过 **pip**(一个管理和安装Python包的工具)来安装**Virtualenv**。


请注意，Homebrew 已经为您的 Python 3.6.2 安装了 `pip3`。

在终端中，执行下面的命令：

```
sudo pip3 install virtualenv
```

![pip3安装virtualenv](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/mac/pip-virtualenv.png)


到目前为止，我们执行的操作都是在系统环境下的。不过，从这一刻起，我们安装的所有东西，包括 Django 本身，都将安装在虚拟环境中。


你可以这样想像一下：对于每个 diango 项目，我们都会为它创建一个虚拟环境。这就好比每个 Django 项目都是一个独立的沙盒，你可以在这个沙盒里随意的玩，安装软件包，卸载软件包，不管怎么对系统环境都不会有任何影响，也不会对其他项目有影响。


我个人喜欢在我的电脑上创建一个 **Development** 的文件夹，然后在这个文件夹下存放我的所有项目。当然，你也可以根据下面的步骤来创建你个人的目录。


通常，我会在我的 **Development** 文件夹中创建一个项目名称的新文件夹。竟然这是我们的第一个项目，就直接将项目名称起为 **myproject**。

```
mkdir myproject
cd myproject
```

![创建myproject文件夹](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/mac/myproject.png)


该文件夹将存储与 Django 项目相关的所有文件，包括其虚拟环境。

接下来，我们将开始创建我们第一个虚拟环境和安装 Django。

在 **myproject** 文件夹中，我们创建一个基于 python 3 的虚拟环境。

```
virtualenv venv -p python3
```

![VIRTUALENV](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/mac/venv.png)

如上图所示，我们的虚拟环境已创建完成。那么我们将如何使用它呢？


当然，我们先开启虚拟环境啦，可以通过以下命令来激活一下虚拟环境：


 ```
 source venv/bin/activate
 ```

如果你在命令行的前面看到 **（venv）**，就说明，虚拟环境激活成功，现在已经进入到虚拟环境里面了。如下图所示：


![Virtualenv激活](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/mac/activate.png)


那么这里面到底发生了什么呢？


其实这里我们首先创建了名为 **venv** 的特殊文件夹，这个文件夹里面有 python 的副本，当我们激活 **venv** 环境之后，运行 `Python` 命令时，它使用的是存储在 **venv** 里面 `Python` 环境 ，而不是我们装在操作系统上的。


如果在该环境下，我们使用 **PIP** 安装 python 软件包，比如 Django ，那么它是被安装在 **venv** 的虚拟环境上的。


这里有一点需要注意的，当我们启动了 **venv** 这个虚拟环境后，我们使用命令 `python` 就能调用 python 3.6.2 ，而且也仅仅使用 `pip`（而不是`pip3`）来安装软件包。


那么如果我们想退出 **venv** 虚拟环境，该如何操作呢？

只要运行以下命令就可以：

```
deactivate
```

不过，现在我们先不退出虚拟环境 **venv** ，保持着虚拟环境的激活状态，开始下一步操作。




##### 安装Django 1.11.4

现在我们来安装以下 Django 1.11.4 ，因为我们已经开启了虚拟环境 **venv** ，因此，这操作会非常的简单。我们将运行下面的命令来安装 Django ：

```
pip install django
```

![pip安装django](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/mac/pip-django.png)


安装成功了，现在一切都准备就绪了！


![结束安装](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/Pixton_Comic_End_Installation.png)

* * *

#### 开始一个新项目

要开始一个新的 Django项目，运行下面的命令：

到目前为止，我们终于可以开始一个新的 Django 项目了，运行下面的命令，创建一个 Django 项目：

```
django-admin startproject myproject
```

命令行工具 **django-admin** 会在安装 Django 的时候一起安装的。


当我们运行了上面的命令之后，系统就会自动的为 Django 项目生成基础的文件。


我们可以打开 **myproject** 目录，可以看到具体的文件结构如下所示：


```
myproject/                  <-- higher level folder
 |-- myproject/             <-- django project folder
 |    |-- myproject/
 |    |    |-- __init__.py
 |    |    |-- settings.py
 |    |    |-- urls.py
 |    |    |-- wsgi.py
 |    +-- manage.py
 +-- venv/                  <-- virtual environment folder
```


可以看到，一个初始 Django 的项目由五个文件组成：


*   **manage.py**：**django-admin** 是命令行工具的快捷方式。它用于运行与我们项目相关的管理命令。我们将使用它来运行开发服务器，运行测试，创建迁移等等。
*   **__init__.py**：这个空文件告诉 Python 这个文件夹是一个 Python 包。
*   **settings.py**：这个文件包含了所有的项目配置。我们会一直使用到这个文件。
*   **urls.py**：这个文件负责映射我们项目中的路由和路径。例如，如果您想在 URL `/about/` 中显示某些内容，则必须先将其映射到此处。
*   **wsgi.py**：该文件是用于部署简单的网关接口。现在我们暂时不用关心它的内容。



Django 自带有一个简单的 Web 服务器。在开发过程中非常方便，所以我们不需要安装其他任何软件即可以在本地运行项目。我们可以通过执行命令来运行它：

```
python manage.py runserver
```


现在在 Web 浏览器中打开以下 URL：**http://127.0.0.1:8000**，您应该看到以下页面：


![有效！](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/it-worked.png)


这里提醒一点，如果你需要停止服务器，可以 `Control + C` 点击停止开发服务器。

* * *

#### Django 的应用


在 Django 哲学中，我们有两个重要的概念：

*   **app**：是一个可以执行某些操作的 Web 应用程序。一个应用程序通常由一组 models(数据库表)，views(视图)，templates(模板)，tests(测试) 组成。
*   **project**：是配置和应用程序的集合。一个项目可以由多个应用程序或一个应用程序组成。

请注意，如果没有一个 project，你就无法运行 Django 应用程序。像博客这样的简单网站可以完全在单个应用程序中编写，例如可以将其命名为 blog或 weblog。

![Django应用程序](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/Pixton_Comic_Django_Apps.png)


当然这是组织源代码的一种方式，现在刚入门，判断确定什么是不是应用程序这些还不太重要。包括如何组织代码等，现在都不是担心这些问题的时候。现在，首先让我们先熟悉了解 Django 的 API 和基础知识。

好了，为了更好的了解，我们先来创建一个简单的论坛项目，那么我们要创建一个应用程序，首先要进入到 **manage.py** 文件所在的目录并执行以下命令：

```
django-admin startapp boards
```


请注意，这次我们使用了命令 **startapp**。

这会给我们以下的目录结构：

```
myproject/
 |-- myproject/
 |    |-- boards/                <-- our new django app!
 |    |    |-- migrations/
 |    |    |    +-- __init__.py
 |    |    |-- __init__.py
 |    |    |-- admin.py
 |    |    |-- apps.py
 |    |    |-- models.py
 |    |    |-- tests.py
 |    |    +-- views.py
 |    |-- myproject/
 |    |    |-- __init__.py
 |    |    |-- settings.py
 |    |    |-- urls.py
 |    |    |-- wsgi.py
 |    +-- manage.py
 +-- venv/
```


所以，我们先来看看每个文件的功能：

*   **migrations /**：在这个文件夹中，Django 会存储一些文件以跟踪您在 **models.py** 文件中创建的更改，目的是为了保持数据库和 **models.py** 同步。
*   **admin.py**：这是 Django应用程序一个名为 **Django Admin** 的内置配置文件。
*   **apps.py**：这是应用程序本身的配置文件。
*   **models.py**：这里是我们定义 Web 应用程序实体的地方。models  由 Django 自动转换为数据库表。
*   **tests.py**：该文件用于为应用程序编写单元测试。
*   **views.py**：这是我们处理Web应用程序请求(request)/响应(resopnse)周期的文件。

现在我们创建了我们的第一个应用程序，让我们来配置一下项目以便启用这个应用程序。


为此，请打开**settings.py**并尝试查找`INSTALLED_APPS`变量：

**settings.py**

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

正如你所看到的，Django 已经安装了6个内置的应用程序。它们提供大多数Web应用程序所需的常用功能，如身份验证，会话，静态文件管理（图像，JavaScript，CSS等）等。

我们将会在本系列教程中探索这些应用程序。但现在，先不管它们，只需将我们的应用程序 boards 添加到 `INSTALLED_APPS` 列表即可：

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'boards',
]
```

使用上个漫画中的正方形和圆形的比喻，黄色圆圈将成为我们的 **boards** 应用程序，而 **django.contrib.admin**，**django.contrib.auth** 等将成为红色圆圈。

* * *

#### Hello, World!


现在我们先来写一个我们的第一个 **视图（view）** ，那么，现在我们来看看该如何使用 Django 来创建一个新的页面吧。


打开 **boards** 应用程序中的 **views.py** 文件，并添加下面的代码：

**views.py**

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, World!')
```

**视图（view）** 是接收 `HttpRequest` 对象并返回 `HttpResponse`对象的 Python 函数。接收 request 作为参数并返回 response 作为结果。这个过程是需要我们记住的。


因此，就像我们上面的代码，我们定义了一个简单的视图，命名为 `home` ，然后我们简单的返回了一个字符串 **Hello，World！**


那么我们直接运行就可以了吗？

并不是的，我们还没有告诉 Django 什么时候调用这个 **视图（view）** 呢？这就需要我们在 **urls.py** 文件中完成：


**urls.py**

```Python
from django.conf.urls import url
from django.contrib import admin

from boards import views

urlpatterns = [
    url(r'^/code>, views.home, name='home'),
    url(r'^admin/', admin.site.urls),
]
```


如果您将上面的代码段与您的 **urls.py** 文件进行比较，您会注意到我添加了以下的代码：`url(r'^$', views.home, name='home')` 并使用我们的应用程序 **boards** 中导入了 **views** 模块。`from boards import views`

可能这里大家还是会有很多疑问，不过先这样做，在后面我们会详细探讨这些概念。

但是现在，Django 使用**正则表达式**来匹配请求的URL。对于我们的 **home** 视图，我使用的是`^$`正则表达式，它将匹配空白路径，这是主页（此URL：**http://127.0.0.1:8000**）。如果我想匹配URL **http://127.0.0.1:8000/homepage/**，那么我们 url 的正则表达式就应该这样写：`url(r'^homepage/$', views.home, name='home')`。

运行项目，让我们看看会发生什么：

```
python manage.py runserver
```


在 Web 浏览器中，打开 http://127.0.0.1:8000 ：


![你好，世界！](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-1/hello-world.png)


这样我们就看到了我们刚刚创建的第一个界面了。

* * *

#### 总结

这是本系列教程的第一部分。在本教程中，我们学习了如何安装最新的 Python 版本以及如何设置开发环境。我们还介绍了虚拟环境，并开始了我们第一个 Django 项目，并已创建了我们的初始应用程序。

我希望你喜欢第一部分！第二部将涉及模型，视图，模板和网址。我们将一起探索所有的Django 基础知识！

就这样我们可以保持在同一页面上，我在 GitHub 上提供了源代码。项目的当前状态可以在发布**release tag v0.1-lw**下找到。下面的链接将带你到正确的地方：

[https://github.com/sibtc/django-beginners-guide/tree/v0.1-lw](https://github.com/sibtc/django-beginners-guide/tree/v0.1-lw)
