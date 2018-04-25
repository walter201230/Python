 ![一个完整的初学者指南Django  - 第2部分](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/featured.jpg)


 ![Python 3.6.2](https://img.shields.io/badge/python-3.6.2-brightgreen.svg) ![Django 1.11.4](https://img.shields.io/badge/django-1.11.4-brightgreen.svg)


#### 介绍


欢迎来到 Django 教程的第二部分！在上一课中，我们安装了项目所需要的一切软件，希望你们在学习这篇文章之前，安装了 Python 3.6，并且在虚拟环境中运行Django 1.11。因为，在本篇文章中，我们将继续在这个项目中编写我们的代码。


在这一篇文章中，可能不会有太多的代码操作，主要是讨论分析项目。在下一篇中，我们就开始学习 Django 的基础知识，包括模型（models），管理后台（admin），视图（views），模板（templates）和 路由（URL）。


在这里，还是跟第一篇一样，建议大家多动手。

* * *

#### 论坛项目


每个人的学习习惯都是不同的，不知道你们是怎样的，就我个人而言，通过看实例和一些代码片段，可以让我学的更多，学的更快。但是，有些时候当我们看到 `Class A`和`Class B` ，或者是 `foo(bar)` 这样的例子的时候，我们是很难理解这些概念的。


所以在我们进入模型（models），创建视图（views） 这些有趣的代码实操之前，我们还是需要花点时间，简单的讨论一下我们将怎样设计，开发这个项目。


但是如果你已经有 web 开发经验的，而且觉得讲的太细了，那么你可以快速的浏览一下，然后进入到 【模型（models）】那一块中。

如果你对 Web 开发并不熟悉，那么我强烈建议你认真阅读下去。这里会介绍 web 应用程序开发的建模和设计，因为对于 web 开发来说，敲代码只是其中的一部分，模型的设计也是很重要的。


![火箭科学](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/Pixton_Comic_Rocket_Science.png)


##### 用例图


我们的项目本身是一个论坛系统，整个项目来说就是维护几个【论坛板块（boards）】 ，然后在每个板块里面，用户可以通过创建【主题（Topic）】并且在主题中讨论。


一般情况下，只有管理员才能创建【论坛板块（boards）】，那么在用户这方面，我们就需要分为普通用户和管理员用户了，而且他们拥有的权限是不同的，管理员用户可以创建 【论坛板块（boards）】，【主题（Topic）】以及讨论回复，而普通用户只能发布【主题（Topic）】以及讨论回复。具体每个用户角色的功能分配如下图：



> 图1：Web Board 核心功能的用例图


![用例图](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/use-case-diagram.png)



##### 类图


从上面的用例图中，我们可以开始思考我们项目中的**实体类**有哪些了。这些实体是我们要创建的模型，它与我们的 Django 应用非常密切。


如果要实现上面我们说到的论坛，那么我们至少需要以下的几个模型：**Board**，**Topic**，**Post**和**User**。

* **Board** : 版块
* **Topic** : 主题
* **Post** : 帖子（用户评论与回复）
* **User** : 用户


> 图2：Web Board 类图


![基本类图](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/basic-class-diagram.png)


上面我们只是说了需要有几个模型，并没有提到模型与模型之间是怎么关联的。


通过上面的图片我们可以知道，主题（Topic）与版块（Board） 之间是有关联的，就好比我们需要知道这个主题（Topic） 是属于哪一个版块的（Board），因此我们需要一个字段，也就是可以通过外键爱关联它们。


同样的，一个帖子（Post） 也是需要确定它是那个主题的，当然，用户和主题（Topic）和帖子（Post） 之间也是有联系的，因为我们需要确认是谁发的帖子，是谁回复评论了内容。


竟然知道了模型之间的联系了，那么我们也必须要考虑这些模型应该存放哪些信息。就目前而言，我们的模型可以设计成这样：


> 图3：类（模型）之间关系的类图


![类图](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram.png)



这个类图强调的是模型之间的关系，当然最后这些线条和箭头都会用字段来进行表示。

**Board（版块模型）** ：Board 中有 **name** 和 **description** 这两个字段，name 是唯一的，主要是为了避免两个名称重复。description 则是用于描述把这个版块来用干什么的。


**Topic（主题模型）** ：subject 表示主题内容，last_update 用来定义话题的排序，starter 用来识别谁发起的话题，board 用于指定它属于哪个版块


**Post（帖子模型）** ： message 字段，用于存储回复的内容，created_at 创建的时间，在排序时候用（最先发表的帖子排最前面），updated_at 更新时间，告诉用户是否更新了内容，同时，还需要有对应的 User 模型的引用，Post 由谁创建的和谁更新的。


**User（用户模型）** ：这里有 username ，password，email 和 is_superuser 四个字段。


这里值得注意的是，我们在 Django 应用中，不需要创建 User 用户模型，因为在 Django 的 contrib 中已经内置了 User 模型，我们可以直接拿来使用，就没必要重新创建了。


认真观察的童鞋应该看到了，上面的模型关系图中，模型与模型之间的对应关系有数字 1，0..* 等等的字段，这是代表什么意思呢？


如下图，`1` 代表一个 Topic 必须与一个  Board 相关联，`0..*` 代表 Board 下面可能会有多个和 0 个 Topic ，也就是一对多的关系。


![类图板和主题协会](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram-board-topic.png)


这里也是一样，`1` 代表一个 Post 只有一个  Topic ，`1..*` 代表一个 Topic 下面可能会有 1 个和多个个 Post ，也就是说，一个主题最少一个一个帖子。



![类图主题和帖子关联](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram-topic-post.png)


`1` 代表一个 Topic 有且至于一个  User ，`0..*` 代表一个 User（用户） 可能拥有多个 Topic ，也可能没有。


![类图主题和用户关联](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram-topic-user.png)


Post（帖子） 和 User（用户）的关系也是类似，一个 Post 必须有一个 User ，而一个 User 可能没有也可能有多个 Post。这里的 Post ，用户发布了之后是可以进行修改的，也就是更新（updated_by），当然如果又被修改，updated_by 就是为空了。


![类图邮政和用户协会](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram-post-user.png)一


当然，如果你觉得上面的图看起来很复杂，那么你也可以不需要强调模型与模型之间的关系，直接强调字段就可以了，如下图：


> 图4：强调类（模型）属性（字段）的类图


![类图属性](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram-attributes.png)


其实这种表达图和前面那个显示箭头和线的表达图，要表达的内容是一样的。不过使用这种表达方式可能更符合 Django  Modles API 的设计。


好了，现在已经够 UML 了！为了绘制本节介绍的图表，我使用的是 [StarUML](http://staruml.io/) 工具。


##### 原型图


花了一些时间来设计我们的程序模型，后面我们也需要设计一下我们的网页原型图。只有这样，才能更好的让我们清楚的知道自己将要干什么？


![线框漫画](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/Pixton_Comic_Wireframes.png)



首先，是我们的主页，在主页中，我们会显示我们所有的版块：


> 图5：主页显示所有的版块信息


![线框板](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/wireframe-boards.png)


同样的，当用户点进了版块信息，进入到版块页面，那么版块页面也将显示该版块下的所有主题：


>图6：版块下的所有主题信息

![线框主题](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/wireframe-topics.png)


通过观察图片，细心的你，可能会发现，用户在这个页面有两条可以走的路线。第一条就是点击 “new topic” 来创建新的主题，第二条就是点击已经存在的主题进入相关的主题进行讨论回复。



“new topic” 的界面如下 ：


![线框新主题](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/wireframe-new-topic.png)


而，进入了相关的主题后，应该显示具体的帖子信息和用户的一些回复信息：


![线框帖子](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/wireframe-posts.png)



如果用户点击 “Reply” 的按钮，他们将看到下面的页面，并以相反的顺序（最新的第一个）对帖子进行显示：

![线框回复](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/wireframe-reply.png)


那么这些图是用什么来绘制的呢？你可以使用 [draw.io](https://draw.io/) ，而且他是完全免费的。


* * *

#### 模型（Models）


上一部分，设计了我们 Web 应用的数据库还有界面原型设计。在模型（Models）这一部分中，我们将在 Django 中创建我们数据库的模型类：**Board** ，**Topic** 和 **Post** 。


这里是不是有个疑问，明明我们设计数据库的时候是有 **User** 的，为什么我们不用创建它的模型类呢？是不是写漏了？


并不是，那是因为 **User** 这个模型类，已经内置在 Django 应用程序中的，**User** 模型就在 **django.contrib.auth** 中。在 settings.py 中，`INSTALLED_APPS` 就配置了**django.contrib.auth**。


好了，现在我们将根据我们上面设计的数据库模型来完成我们项目 **boards** 下的 models.py 文件中的所有操作。


> **boards/models.py**

```python
from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')
```

可以看到，创建的所有模型类，**Board** ， **Topic** 和 **Post** 都是 **django.db.models.Model** 的子类，它们都将会转化成数据表。而 **django.db.models.Field** 的子类（Django 内置的核心类）的实例都会转化为数据表中的列。


上面可以看到的 `CharField`，`DateTimeField` 等，都是 **django.db.models.Field** 的子类，在 Django 项目中都可以直接使用它们。


在这里，我们仅仅使用了 `CharField`，`TextField`，`DateTimeField`，和 `ForeignKey` 字段来定义我们的模型（Models） 。当然，在 Django 中，不仅仅只是提供了这些字段，还提供了更多，更广泛的选择来代表不同类型的数据，比如还有：`IntegerField`，`BooleanField`， `DecimalField`。我们会根据不同的需求来使用它们。	
 

有些字段是需要参数的，就好比 `CharField` ，我们都设定了一个 `max_length` , 设置一个最大长度。当我们设定了这个字段后，就会作用于数据的。


在 `Board` 模型（Model）中，在 `name` 字段中，我们也设置了参数 `unique=True`，顾名思义，这是为了在数据库中，保证该字段的唯一性。


在 `Post` 模型中，`created_at` 字段有一个可选参数，`auto_now_add` 设置为 `True`。这是为了指明 Django 在创建 `Post` 对象的时候，`created_at` 使用的是当前的日期和时间。


创建模型与模型之间关系的其中一种方法就是使用 `ForeignKey` 字段，使用这个字段，会自动创建模型与模型之间的联系，而且会在数据库中也创建它们的关系。使用 `ForeignKey` 会有一个参数，来表明他与那个模型之间的联系。 例如：


在 `Topic` 模型中，`models.ForeignKey(Board, related_name='topics')`，第一个参数是代表关联的表格（主表），在默认情况下，外键存储的是主表的主键（Primary Key）。第二个参数 `related_name` 是定义一个名称，用于反向查询的。Django 会自动创建这种反向关系。 虽然 `related_name` 是可选参数，但是如果我们不为它设置一个名称的，Django 会默认生成名称 `(class_name)_set` 。例如，在 `Board` 模型中，`Topic` 实例将在该 `topic_set` 属性下可用。而我们只是将其重新命名为`topics`，使用起来更加自然。


在 `Post` 模型中，`updated_by` 字段设置`related_name='+'`。这指示 Django 我们不需要这种反向关系。


下面这张图可以很好地看到设计图和源码之间的比较，其中绿线就表示了我们是如何处理反向关系的。


![类图模型定义](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/class-diagram-django-models.png)


可能到这一步，你会问：“主键呢？”好像我们都没有定义主键啊。对，如果我们没有为模型（Models）指定主键，那么 Django 会自动生成它。


##### 迁移模型（Migrating the Models）


到这一步，我们要开始告诉 Django 如何创建数据库，这样方便我们更好的使用。


打开**终端** ，激活虚拟环境，进入到 **manage.py** 文件所在的文件夹，然后运行以下命令：


```
python manage.py makemigrations
```

这时，你会看到这样的输出信息：


```
Migrations for 'boards':
  boards/migrations/0001_initial.py
    - Create model Board
    - Create model Post
    - Create model Topic
    - Add field topic to post
    - Add field updated_by to post
```


此时，Django 在 **boards / migrations** 目录内创建了一个名为**0001_initial.py** 的文件。它代表了我们应用程序模型的当前状态。在下一步中，Django 将使用该文件来创建表和列。


迁移文件被翻译成 SQL 语句。如果您熟悉 SQL，则可以运行以下命令来检查将在数据库中执行的 SQL 指令：

```
python manage.py sqlmigrate boards 0001
```


如果你不熟悉 SQL，也不用担心。在本系列教程中，我们不会直接使用 SQL。所有的工作都将使用 Django ORM 来完成，它是一个与数据库进行通信的抽象层。

好了，下一步我们将把我们的迁移文件应用到我们的数据库中：


```
python manage.py migrate</code>
```


输出应该是这样的：

```
Operations to perform:
  Apply all migrations: admin, auth, boards, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying boards.0001_initial... OK
  Applying sessions.0001_initial... OK
```



因为这是我们第一次迁移数据库，所以该 `migrate` 命令还应用了 Django contrib 应用中现有的迁移文件，这些文件列于 `settings.py` 中的 `INSTALLED_APPS` 。


而 `Applying boards.0001_initial... OK` 就是指我们在上一步中生成的迁移文件。


好了，此时！我们的数据库已经可以使用了。


![SQLite的](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/Pixton_Comic_SQLite.png)


> **注意：** 需要注意的是 **SQLite** 是一个数据库。SQLite 被许多公司用于成千上万的产品，如所有 Android 和 iOS 设备，所有主要的 Web 浏览器，Windows 10，MacOS 等。
>
> 当然，它也不是适合所有的应用场景。SQLite 不能与 MySQL，PostgreSQL 或 Oracle 等数据库进行比较。大容量网站，密集型的应用程序，大数据集，高并发性，这些使用使用 SQLite 可能会导致很多问题。
>
> 在我们开发的项目中，我们将使用 SQLite ，因为它很方便，我们不需要安装其他任何东西。当我们将项目部署到生产环境时，我们将切换到 PostgreSQL 。因为这对于简单的网站是不错的选择。但这里有一点要注意，对于复杂的网站，建议在开发和生产中使用相同的数据库。


##### Models API


使用 Python 开发的一个重要优点是交互式 shell。我几乎一直都在使用它。这是一个可以快速尝试和测试实验的方法。

你可以使用 **manage.py** 加载我们的项目来启动 Python shell ：

启动命令：

```
python manage.py shell
```

可以看到这样的输出：

```
Python 3.6.2 (default, Jul 17 2017, 16:44:45)
[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```


在我们使用 `python manage.py shell` 之外，我们也可以将项目添加到`sys.path`并加载 Django。这意味着我们可以在项目中导入我们的模型(models) 和任何其他资源。

我们从导入 **Board** 类开始：

```
from boards.models import Board
```

如果我们需要创建 **Board** 对象，我们可以执行以下操作：

```
board = Board(name='Django', description='This is a board about Django.')
```

此时我们只是创建了这个对象，并没有保存到数据库的，因此我们可以调用 `save` 方法，将这个对象保存在数据库中。


```
board.save()
```

该 `save` 方法 ，在创建对象和更新对象中都可以使用，这里 Django 会创建一个新的对象，因为 **Board** 实例是没有 **id** 这个字段的，因此保存后，Django 会自动设置一个 ID ：


```
board.id
1
```


其他的字段你也可以当作属性来访问就好了，比如：

```
board.name
'Django'
```

```
board.description
'This is a board about Django.'
```


要更新一个值，我们可以这样做：


```
board.description = 'Django discussion board.'
board.save()
```


每个 Django 模型 (Models) 都带有一个特殊的属性; 我们称之为 **Model Manager（模型管理器）**。我们可以通过 Python 属性 `objects` 来访问它。它主要用于在数据库中执行查询。例如，我们可以使用它来直接创建一个新的**Board** 对象：

```
board = Board.objects.create(name='Python', description='General discussion about Python.')
```

```
board.id
2
```

```
board.name
'Python'
```

所以，结合之前的操作，我们现在有两个 boards 对象。我们可以使用`objects` 列出数据库中所有现有的 boards ：


```
Board.objects.all()
<QuerySet [<Board: Board object>, <Board: Board object>]>
```


结果是一个 **QuerySet** 。稍后我们会进一步了解它。基本上，它是来自数据库的对象列表。通过输出结果，可以看到我们有两个对象，但我们只能读取 **Board对象** 。这是因为我们没有在 **Board** 模型中定义 `__str__` 方法。


该 `__str__` 方法是一个对象的字符串表示。我们可以使用 Board 的名称来表示它。


首先，退出交互式控制台：


```
exit()
```


现在编辑 **boards** 应用程序中的 **models.py** 文件：


```
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```


让我们再次尝试查询。再次打开交互式控制台：


```
from boards.models import Board

Board.objects.all()
<QuerySet [<Board: Django>, <Board: Python>]>
```


仔细对比上面的，看下区别？

可以看到上面那个是 object ，而这里是我们定义的字符串。


我们可以将这个 **QuerySet** 看作一个列表。假设我们想遍历它并打印每个 Board（版块） 的描述：


```
boards_list = Board.objects.all()
for board in boards_list:
    print(board.description)
```


结果是：


```
Django discussion board.
General discussion about Python.
```


当然，我们也可以使用 **Model Manager（模型管理器）** 来查询数据库，如果查询其中的一个，我们可以使用 `get` 的方法：


```
django_board = Board.objects.get(id=1)

django_board.name
'Django'
```

当然我们要小心这种情况，因为很容易发生内存溢出的。比如我们试图去查询一个不存在的对象，就好比我们数据库只有两个 Board 对象，如果你查询 `id=3`，那么它会引发一个异常：


```
board = Board.objects.get(id=3)

boards.models.DoesNotExist: Board matching query does not exist.
```

当然，在 `get` 方法中，参数可以是该模型下的字段，最好是使用唯一的标识字段。否则会返回多个对象，会导致异常的。


```
Board.objects.get(name='Django')
<Board: Django>
```


请注意，查询是区分大小写的，小写 “django” 是不匹配的：


```
Board.objects.get(name='django')
boards.models.DoesNotExist: Board matching query does not exist.
```


##### 模型操作摘要

下面的表格是我们在本章节中学到的方法和操作。代码示例使用 **Board** 模型作为参考示例。大写的 **Board** 代表类，小写的 **board** 是指 **Board** 的实例对象。


| 描述 | 代码示例 |
| --- | --- |
| 创建一个对象并没有保存 | `board = Board()` |
| 保存一个对象（创建或更新） | `board.save()` |
| 在数据库中创建并保存一个对象 | `Board.objects.create(name='...', description='...')` |
| 列出所有对象 | `Board.objects.all()` |
| 获取由字段标识的单个对象 | `Board.objects.get(id=1)` |


在下一节中，我们将开始编写视图并在 HTML 页面中显示我们的版块页面。


* * *

#### Views, Templates 和静态文件


回顾一下，我们之前做的。我们已经可以在应用程序的主页上显示 ”Hello ，World！“ 的界面了。


> **MyProject/urls.py**

```
from django.conf.urls import url
from django.contrib import admin

from boards import views

urlpatterns = [
    url(r'^/code>, views.home, name='home'),
    url(r'^admin/', admin.site.urls),
]
```

> **boards/views.py**

```
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, World!')
```

好了，现在我们需要修改这个主页，如果你不记得我们的主页要做成什么样子，可以看看之前我们已经设计好的原型界面图。我们在主页上，要做的是在表格中显示一些版块的名单和其他的一些信息。


首先我们要做的是：导入 **Board** 模型，然后获取所有的存在的版块（boards）信息


> **boards/views.py**


```
from django.http import HttpResponse
from .models import Board

def home(request):
    boards = Board.objects.all()
    boards_names = list()

    for board in boards:
        boards_names.append(board.name)

    response_html = '<br>'.join(boards_names)

    return HttpResponse(response_html)
```



然后我们运行，就会看到这个简单的 HTML 页面：



![主页HttpResponse](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/boards-homepage-httpresponse.png)


但是，一般情况下，我们是不会通过这种方式去渲染 HTML ，在 **views.py** 中，我们只需要获取 **boards** 的集合，至于 HTML 渲染那部分的代码，我们应该在 Django 的 templates 目录下完成。


##### Django 模板引擎设置

竟然我们要将 **views.py** 里渲染 HTML 的代码分离，那么我们首先要在 **baords** 的同目录下，创建一个名为 **templates** 的文件夹。


```
myproject/
 |-- myproject/
 |    |-- boards/
 |    |-- myproject/
 |    |-- templates/   <-- here!
 |    +-- manage.py
 +-- venv/
```

在我们创建的 **templates** 文件夹中，我们创建一个名为 **home.html** 的 HTML 文件

> **templates/home.html**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Boards</title>
  </head>
  <body>
    <h1>Boards</h1>

    {% for board in boards %}
      {{ board.name }} <br>
    {% endfor %}

  </body>
</html>
```

**home.html** 的文件内容如上面的一样，是一些原始的 HTML 标签代码和 Django 语言上的代码：`{% for ... in ... %}` ，`{{ variable }}`。上面的代码中展示了如何使用 for 循环遍历 list 对象。

到此，我们的 HTML 页面已经完成了，可是我们还没有告诉 Django 在哪里能找到我们应用中的 `templates` 文件夹里的 HTML。


首先，我们在 Django 中绑定一下我们的 `templates` ,打开我们 ** myproject** 项目中的 **settings.py** 文件，搜索 `TEMPLATES` 变量然后在 `DIRS`设置 ：`os.path.join(BASE_DIR, 'templates')`

具体如下：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

这样设计就好比相当于在你的项目中的完整路径下，在加上 "/templates"

那是不是跟我们预想的一样呢？我们可以通过 python shell 进行调试：

```
python manage.py shell
```

```
from django.conf import settings

settings.BASE_DIR
'/Users/vitorfs/Development/myproject'

import os

os.path.join(settings.BASE_DIR, 'templates')
'/Users/vitorfs/Development/myproject/templates'
```


可以看到，目录就是指向我们在上面创建的 **templates** 文件夹

此时，我们只是绑定了 **templates** 文件夹的路径，Django 并没有绑定我们 **home.html** ，我们可以在 **views.py** 中绑定：

```
from django.shortcuts import render
from .models import Board

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
```



运行后，HTML 的页面是这样的：


![主板渲染](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/boards-homepage-render.png)

我们可以改进HTML模板来代替使用表格：

> **templates/home.html**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Boards</title>
  </head>
  <body>
    <h1>Boards</h1>

    <table border="1">
      <thead>
        <tr>
          <th>Board</th>
          <th>Posts</th>
          <th>Topics</th>
          <th>Last Post</th>
        </tr>
      </thead>
      <tbody>
        {% for board in boards %}
          <tr>
            <td>
              {{ board.name }}<br>
              <small style="color: #888">{{ board.description }}</small>
            </td>
            <td>0</td>
            <td>0</td>
            <td></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </body>
</html>
```


![主板渲染](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/boards-homepage-render-2.png)


##### 测试主页


![测试漫画](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/Pixton_Comic_Testing.png)

测试这部分会在这系列教程中会不断的重复探讨。


现在让我们来写第一个测试，首先在应用程序 **boards** 中找到 **tests.py** 

> **boards/tests.py** 

```
from django.core.urlresolvers import reverse
from django.test import TestCase

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
```

这是一个非常简单的测试用例，但非常的有用。我们在测试的是响应状态码，如果是 200 意味着成功。


我们可以在控制台中检查响应码：

![回应200](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/test-homepage-view-status-code-200.png)


如果出现未捕获的异常，语法错误或其他任何情况，Django 会返回状态代码**500**，这意味着**服务器错误**。现在，想象我们的应用程序有 100 个界面（view）。如果我们为所有视图（view）编写了这个简单的测试，只需一个命令，我们就可以测试所有视图是否返回成功代码，这样用户就不会在任何地方看到任何错误消息。如果没有自动化测试，我们需要逐一检查每个页面。

要执行 Django 的测试套件：

```
python manage.py test
```

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.041s

OK
Destroying test database for alias 'default'...
```

现在我们可以测试 Django 是否为请求的 URL 返回了正确的视图函数。这也是一个有用的测试，因为随着开发的进展，您会发现 **urls.py** 模块可能变得非常庞大而复杂。URL 配置全部是关于解析正则表达式的。有些情况下我们有一个非常宽容的URL，所以 Django 最终可能返回错误的视图函数。

以下是我们如何做到的：

> **boards/tests.py**

```
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import home

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
```



在第二个测试中，我们正在使用 `resolve` 功能。Django 使用它来将请求的 URL与 **urls.py** 模块中列出的 URL 列表进行匹配。该测试将确保使用 `/`根 URL ，是否返回主视图（home view）。

再次测试：

```
python manage.py test
```

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.027s

OK
Destroying test database for alias 'default'...
```


要查看有关测试执行的更多详细信息，请将 **verbosity** 设置为更高级别：

```
python manage.py test --verbosity=2
```

```
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, boards, contenttypes, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying boards.0001_initial... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_home_url_resolves_home_view (boards.tests.HomeTests) ... ok
test_home_view_status_code (boards.tests.HomeTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.017s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```

详细程度决定了将要打印到控制台的通知和调试信息量; 0 是无输出，1 是正常输出，2 是详细输出。

##### 静态文件设置

静态文件是指 CSS，JavaScript，字体，图像或者是我们用来组成用户界面的任何其他资源。

事实上，Django 不提供这些文件。但在开发过程中，我们又会用到，因此 Django 提供了一些功能来帮助我们管理静态文件。这些功能可在配置文件（settings.py）中 `INSTALLED_APPS` 里的 **django.contrib.staticfiles** 。

有了这么多的前端组件库，我们没有理由继续渲染基本的 HTML 。我们可以轻松地将Bootstrap 4 添加到我们的项目中。Bootstrap 是一个用 HTML，CSS 和JavaScript 开发的开源工具包。

在项目根目录中，除**boards**，**templates** 和 **myproject** 文件夹外，我们还需要创建一个名为 **static** 的文件夹，并在 **static** 文件夹内创建另一个名为 **css** 文件夹：

```
myproject/
 |-- myproject/
 |    |-- boards/
 |    |-- myproject/
 |    |-- templates/
 |    |-- static/       <-- here
 |    |    +-- css/     <-- and here
 |    +-- manage.py
 +-- venv/
```

到 [getbootstrap.com](https://getbootstrap.com/docs/4.0/getting-started/download/#compiled-css-and-js) 下载最新版本：

![Bootstrap下载](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/bootstrap-download.png)

下载 **Compiled CSS and JS** 的版本。

解压从 Bootstrap 网站下载的 **bootstrap-4.0.0-beta-dist.zip** 文件，将文件 **css / bootstrap.min.css** 复制到我们项目的css文件夹中：

```
myproject/
 |-- myproject/
 |    |-- boards/
 |    |-- myproject/
 |    |-- templates/
 |    |-- static/
 |    |    +-- css/
 |    |         +-- bootstrap.min.css    <-- here
 |    +-- manage.py
 +-- venv/
```

还是一样的问题，我们需要将 Django 中的 **settings.py** 里配置一下静态文件的目录。在 `STATIC_URL` 添加以下内容： 

```
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```


这里可以回忆一下，`TEMPLATES` 配置目录的路径，操作是差不多的。


现在我们必须在模板中加载静态文件（Bootstrap CSS文件）：

> **templates/home.html**

```
{% load static %}<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Boards</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
  </head>
  <body>
    <!-- body suppressed for brevity ... -->
  </body>
</html>
```



首先，我们在 html 的开头加载静态文件：`{% load static %}`


`{% static %}` 是用于告诉资源文件存在的路径，在这是，`{% static 'css/bootstrap.min.css' %}` 就会返回 **/static/css/bootstrap.min.css** ，相当于 **http://127.0.0.1:8000/static/css/bootstrap.min.css**


这个 `{% static %}` 标签将会和 **settings.py** 的 `STATIC_URL` 组成最终的 URL。怎么理解这句话呢？

例如，我们在静态文件托管在 **https://static.example.com/** ，然后我们设置了这个属性：`STATIC_URL=https://static.example.com/`，然后 `{% static 'css/bootstrap.min.css' %}` 返回的是 ：**https://static.example.com/css/bootstrap.min.css**。


如果还不能理解，放心，你现在只需要了解和记住相关的过程就行了，后面正式开发上线的时候，会继续开展这部分的内容。


刷新页面 **127.0.0.1:8000** 我们可以看到它是这个样子的：

![Boards主页Bootstrap](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/boards-homepage-bootstrap.png)

现在我们可以编辑模板，以利用Bootstrap CSS：

现在我们可以利用 Bootstrap CSS 来编辑我们的模板页面了：



```
{% load static %}<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Boards</title>
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
  </head>
  <body>
    <div class="container">
      <ol class="breadcrumb my-4">
        <li class="breadcrumb-item active">Boards</li>
      </ol>
      <table class="table">
        <thead class="thead-inverse">
          <tr>
            <th>Board</th>
            <th>Posts</th>
            <th>Topics</th>
            <th>Last Post</th>
          </tr>
        </thead>
        <tbody>
          {% for board in boards %}
            <tr>
              <td>
                {{ board.name }}
                <small class="text-muted d-block">{{ board.description }}</small>
              </td>
              <td class="align-middle">0</td>
              <td class="align-middle">0</td>
              <td></td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </body>
</html>
```



修改后变成这样子：

![Boards主页Bootstrap](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/boards-homepage-bootstrap-2.png)


到目前为止，我们使用交互式控制台（`python manage.py shell`）添加新的版块（board）。但是这样很不方便，因此我们需要一个更好的方式来做这个。在下一节中，我们将为网站管理员实施一个管理界面来管理它。

* * *

#### Django Admin简介

当我们开始一个新项目时，Django 在 `INSTALLED_APPS` 中已经配置了 **Django Admin** 。

![Django Admin漫画](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/Pixton_Comic_Django_Admin.png)

Django Admin 的一个很好的用例就是，在博客中，它可以被作者用来编写和发布文章。另一个例子是电子商务网站，工作人员可以创建，编辑，删除产品。

目前，我们将配置 Django Admin 来维护我们的应用程序的版块模块。

我们首先创建一个管理员帐户：

```
python manage.py createsuperuser
```

按照说明操作：

```
Username (leave blank to use 'vitorfs'): admin
Email address: admin@example.com
Password:
Password (again):
Superuser created successfully.
```

现在在浏览器中打开 URL：**http://127.0.0.1:8000/admin/**

![Django管理员登录](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/django-admin-login.png)

输入 **用户名** 和 **密码** ：

![Django Admin](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/django-admin.png)


在这里，它已经配置了一些功能，我们也可以添加**用户**和**组**来管理权限。


那么我们如何在这个管理后台中管理版块（Board）里面的内容呢？

其实很简单，在 **board** 目录下，**admin.py** 中添加以下代码：


> **boards/admin.py**

```
from django.contrib import admin
from .models import Board

admin.site.register(Board)
```


保存以下，然后刷新网页：

![Django管理委员会](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/django-admin-boards.png)

点击 **Boards** 链接就能查看现有版块列表：

![Django管理委员会名单](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/django-admin-boards-list.png)

我们可以通过点击 **Add Board** 按钮添加一个新的版块：

![Django管理委员会添加](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/django-admin-boards-add.png)

点击 **SAVE** 按钮：

![Django管理委员会名单](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/django-admin-boards-list-2.png)

我们可以检查一切是否正常，打开 **http://127.0.0.1:8000** URL：

![董事会主页](https://simpleisbetterthancomplex.com/media/series/beginners-guide/1.11/part-2/boards-homepage-bootstrap-3.png)

* * *

#### 结论

在本教程中，我们探讨了许多新概念。我们为我们的项目定义了一些要求，创建了第一个模型，迁移了数据库，开始玩 Models API。我们创建了第一个视图并编写了一些单元测试。我们还配置了 Django 模板引擎，静态文件，并将 Bootstrap 4 库添加到项目中。最后，我们简要介绍了 Django Admin 界面。


该项目的源代码在 GitHub 上,你可以在下面的链接中找到本章节的代码：

[https://github.com/sibtc/django-beginners-guide/tree/v0.2-lw](https://github.com/sibtc/django-beginners-guide/tree/v0.2-lw)