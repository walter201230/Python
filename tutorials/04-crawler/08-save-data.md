# 爬虫第 8 章：存下来：csv、json 与 sqlite3

# 前言

学到上一章，书店的 120 本书已经能完整地取下来了。可是这些数据，只活在程序运行的那一会儿。程序一结束，它们就全没了，下次想用，还得重新抓一遍。

重新抓一遍有什么不好呢？它不光浪费自己的时间，也在浪费别人网站的资源。所以，爬虫的最后一步是**存储**：把取到的数据存下来，以后要用，直接读文件就行。

那存成什么呢？实战 5 已经学过 csv 和 json，这一章就把它们用在抓下来的数据上。另外，还要再认识一位新朋友：**sqlite3**，它是 Python 自带的一个小数据库。数据一多，要按条件筛选、要分组统计的时候，它比 csv 文件好用得多。

很多童鞋一听「数据库」，就觉得很高深。其实 sqlite3 就是一个文件，不用安装，也不用启动什么服务。真正要学的，是一种叫 SQL 的查询语言。不过别担心，这一章只用到其中最常用的四五句，多看几遍就熟了。

**学这一章之前**，需要先学完 [爬虫课第 7 章](07-json-api.md) ，会从接口取回整个书店的数据。另外，还要熟悉 [实战 5](../01-basics/09b-practice-5-files-csv-json.md) 里 csv 和 json 的读写。

# 目录

这一章会学到：

- 一、为什么要存下来——别让数据跟着程序一起消失
- 二、存成 csv 和 json——各有各的用处
- 三、存进数据库——sqlite3 和建表、插入
- 四、用 SQL 查数据——筛选、排序、分组统计
- 五、常见坑
- 六、自己查一次文档——用字典直接插入
- 七、小结与回看

学完这一章，你能把抓到的数据存成 csv、json 和 sqlite3 数据库，并用 SQL 从数据库里查出想要的结果。

# 一、为什么要存下来

要存数据，先得有数据。咱们先用上一章的办法，从接口取回全部图书。后面几节，都从这一步开始：

<!-- skip-ci -->
```python
import time
from urllib.parse import urljoin

import requests

url = 'https://learn-py.org/lab/bookstore/api/page-1.json'
books = []
while url:
    data = requests.get(url).json()
    books.extend(data['books'])
    url = urljoin(url, data['next']) if data['next'] else None
    time.sleep(0.2)
print(len(books))
print(list(books[0].keys()))
```

输出的结果：

```
120
['id', 'title', 'author', 'category', 'price', 'rating', 'reviews', 'stock', 'pages', 'year']
```

一共 120 本书，每本有 10 个字段。数据拿到了，为什么还要特意存下来呢？存下来有这么几个好处：

- **不用重复抓**：分析数据的时候，代码可能要改十几遍。要是每改一次，都重新请求一遍网站，既慢，又打扰别人。
- **留下证据**：网站的数据会变，今天的价格，明天可能就改了。存下来的，就是当时的样子。
- **交给别的程序用**：存成 csv，Excel 就能打开。到了数据分析课，pandas 一行就能把它读进来。

那么，存成什么格式好呢？这要看用途：

| 格式 | 适合 |
|---|---|
| csv | 一行一条、每条字段都一样的表格数据；要给 Excel、pandas 用 |
| json | 有嵌套的数据，比如一本书带着好几条评论；要原样保留数字、`None` |
| sqlite3 数据库 | 数据多，经常要按条件筛选、排序、分组统计；要一点一点往里加 |

下一节，先从学过的 csv 和 json 开始。

# 二、存成 csv 和 json

先说 csv。每本书的字段都一样，排起来正好是一张表，所以用 `csv.DictWriter` 存最方便。表头的字段名，直接从第一本书的键里拿。存完以后，再读回来看看：

<!-- skip-ci -->
```python
import csv

import requests

books = requests.get('https://learn-py.org/lab/bookstore/api/page-1.json').json()['books']
with open('my_books.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(books[0].keys()))
    writer.writeheader()
    writer.writerows(books)

with open('my_books.csv', encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
print(len(rows))
print(rows[2])
```

输出的结果：

```
20
{'id': '3', 'title': '早起养花', 'author': '林子墨', 'category': '生活', 'price': '56.2', 'rating': '', 'reviews': '0', 'stock': '47', 'pages': '310', 'year': '2014'}
```

这里只存了第一页的 20 本，好让例子短一点。读回来以后，有两件事要留意，实战 5 都说过：

- 所有的值都变成了字符串，比如 `'56.2'` 、`'47'` ，用的时候要自己转换。
- 没有评分的 `None` ，存进 csv 以后，变成了空字符串 `''` 。

这两件事，换成 json 就都不是问题了。同样存完再读回来看看：

<!-- skip-ci -->
```python
import json

import requests

books = requests.get('https://learn-py.org/lab/bookstore/api/page-1.json').json()['books']
with open('my_books.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

with open('my_books.json', encoding='utf-8') as f:
    loaded = json.load(f)
print(loaded[2])
```

输出的结果：

```
{'id': 3, 'title': '早起养花', 'author': '林子墨', 'category': '生活', 'price': 56.2, 'rating': None, 'reviews': 0, 'stock': 47, 'pages': 310, 'year': 2014}
```

和 csv 读回来的那一行对比一下：这回数字还是数字，`None` 也还是 `None` 。

还有两点要说明。在网页里运行时，这些文件存在浏览器临时准备的地方，刷新页面就没了。在自己电脑上运行，它们就存在代码文件的旁边。另外，要是 csv 是给 Excel 打开的，记得把编码换成 `'utf-8-sig'` 。

下面先做一道练习，把一页书存进 csv，再读回来数一数。

# 三、存进数据库

csv 和 json 都会存了，再来认识前言里说的那位新朋友。**sqlite3** 是 Python 自带的数据库模块。一个数据库就是一个文件，里面可以有好几张**表**。每张表和 csv 一样，一行是一条记录，每一列是一个字段。

和数据库打交道，要用一种专门的语言：**SQL**。下面这段代码，建了一张表，插入两本书，再把它们查出来。先看完整的一段，再一句一句地解释：

```python
import os
import sqlite3

if os.path.exists('bookstore.db'):
    os.remove('bookstore.db')

conn = sqlite3.connect('bookstore.db')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, category TEXT, price REAL, stock INTEGER)')
conn.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?)', (1, '轻松玩转自动化', '编程', 104.4, 55))
conn.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?)', (3, '早起养花', '生活', 56.2, 47))
conn.commit()

for row in conn.execute('SELECT id, title, price FROM books'):
    print(row)
conn.close()
```

输出的结果：

```
(1, '轻松玩转自动化', 104.4)
(3, '早起养花', 56.2)
```

代码不长，可新东西不少。按顺序来看：

- 开头先删掉旧的数据库文件，这样每次运行都从空的开始。在自己电脑上，真正存数据的程序可不会这么做。
- `sqlite3.connect('bookstore.db')` ：打开数据库文件，没有就新建一个，得到一个**连接**。
- `CREATE TABLE books (...)` ：建一张叫 `books` 的表。括号里是每一列的名字和类型：`INTEGER` 整数、`TEXT` 文字、`REAL` 小数。`PRIMARY KEY` 表示 `id` 是每本书独一无二的编号。
- `INSERT INTO books VALUES (?, ?, ?, ?, ?)` ：插入一行。值不直接写进 SQL，而是用 `?` 占位，再用一个元组按顺序交给它。为什么要这样，第五节「常见坑」里会讲。
- `conn.commit()` ：**提交**，真正把改动存进文件。
- `SELECT id, title, price FROM books` ：从 `books` 表里取出这三列。结果可以用 `for` 一行一行地取，每一行是一个元组。
- `conn.close()` ：用完关掉连接。

两本书，一条一条地插还行。可要是 120 本书也一条一条地插，就太慢了。这时候可以用 `executemany()` ，一次插入很多行，正好把接口拿到的 120 本书都存进去：

<!-- skip-ci -->
```python
import os
import sqlite3
import time
from urllib.parse import urljoin

import requests

url = 'https://learn-py.org/lab/bookstore/api/page-1.json'
books = []
while url:
    data = requests.get(url).json()
    books.extend(data['books'])
    url = urljoin(url, data['next']) if data['next'] else None
    time.sleep(0.2)

if os.path.exists('bookstore.db'):
    os.remove('bookstore.db')
conn = sqlite3.connect('bookstore.db')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, category TEXT, price REAL, rating REAL, stock INTEGER, year INTEGER)')
rows = [(b['id'], b['title'], b['author'], b['category'], b['price'], b['rating'], b['stock'], b['year']) for b in books]
conn.executemany('INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?)', rows)
conn.commit()
print(conn.execute('SELECT COUNT(*) FROM books').fetchone())
conn.close()
```

输出的结果：

```
(120,)
```

120 本书都存进去了。最后那句 `SELECT COUNT(*) FROM books` ，是数一数表里有几行。`fetchone()` 取出第一行结果，所以输出是一个只有一个元素的元组。

还有一点：有的书没有评分，`rating` 是 `None` 。Python 的 `None` 存进数据库，会变成 SQL 里的 `NULL` ，读出来又变回 `None` 。

数据存进去了，又该怎么查呢？下一节就来学几句最常用的 SQL。

# 四、用 SQL 查数据

数据存进数据库，最大的好处就是查起来方便。这一节的例子，都在 `:memory:` 数据库里做。它不存文件，只放在内存里，程序一结束就没了，拿来做练习正合适。

下面先建好表，插入全部 120 本书，再换着花样查三次：缺货的书、最贵的三本，以及每类的数量和平均价格：

<!-- skip-ci -->
```python
import sqlite3
import time
from urllib.parse import urljoin

import requests

url = 'https://learn-py.org/lab/bookstore/api/page-1.json'
books = []
while url:
    data = requests.get(url).json()
    books.extend(data['books'])
    url = urljoin(url, data['next']) if data['next'] else None
    time.sleep(0.2)

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, category TEXT, price REAL, rating REAL, stock INTEGER)')
conn.executemany('INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)',
                 [(b['id'], b['title'], b['category'], b['price'], b['rating'], b['stock']) for b in books])

print('-- 缺货的书')
for row in conn.execute('SELECT id, title FROM books WHERE stock = 0 ORDER BY id LIMIT 3'):
    print(row)

print('-- 最贵的三本')
for row in conn.execute('SELECT title, price FROM books ORDER BY price DESC LIMIT 3'):
    print(row)

print('-- 每类的数量和平均价格')
for row in conn.execute('SELECT category, COUNT(*), ROUND(AVG(price), 2) FROM books GROUP BY category ORDER BY AVG(price) DESC'):
    print(row)
```

输出的结果：

```
-- 缺货的书
(19, '从零开始学数据分析')
(26, '古城千年')
(33, '运河千年')
-- 最贵的三本
('实战做小工具', 117.2)
('实战学数据分析', 112.3)
('光影的力量', 107.7)
-- 每类的数量和平均价格
('编程', 15, 79.82)
('设计', 15, 78.37)
('科普', 15, 64.55)
('历史', 15, 59.78)
('经济', 15, 56.51)
('小说', 15, 45.93)
('生活', 15, 44.47)
('童书', 15, 35.99)
```

这三句 SQL 里，用到了好几个新写法。一个一个拆开来看：

| 写法 | 意思 |
|---|---|
| `WHERE stock = 0` | 只要满足条件的行，相当于 `if` |
| `ORDER BY price DESC` | 按价格排序，`DESC` 是从大到小，不写就是从小到大 |
| `LIMIT 3` | 只要前 3 行 |
| `GROUP BY category` | 按类别分组，每组算一次 |
| `COUNT(*)` 、`AVG(price)` 、`ROUND(x, 2)` | 数行数、求平均、保留两位小数 |

这些写法拼在一起的时候，顺序是固定的：`SELECT 要哪些列 FROM 哪张表 WHERE 条件 GROUP BY 分组 ORDER BY 排序 LIMIT 几行` 。记住这个骨架，就够用了。

有的童鞋可能会想：这些统计，用 Python 的循环和字典不也能做吗？能做，可要写十几行。而 SQL 一句话就说清楚了。以后到了数据分析课，pandas 做的也是这些事，到时候你会发现，很多地方都和 SQL 一一对应。

最后再说一点。上一节插入数据时，值是用 `?` 占位的。按条件查的时候，条件里的值也同样用 `?` 占位。比如找出价格低于 60 元的书：

```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE books (title TEXT, price REAL)')
conn.executemany('INSERT INTO books VALUES (?, ?)', [('轻松玩转自动化', 104.4), ('早起养花', 56.2), ('书院笔记', 52.5)])
limit = 60
for row in conn.execute('SELECT title FROM books WHERE price < ? ORDER BY price', (limit,)):
    print(row[0])
```

输出的结果：

```
书院笔记
早起养花
```

注意代码里的 `(limit,)` 。它是只有一个元素的元组，末尾的逗号不能少，基础课第 3 章讲元组时说过。

下面先做一道练习，自己写两句 SQL，查一查高分的好书。

# 五、常见坑

存数据的办法都学完了。不过真动手存的时候，下面这几个坑很容易踩到，有的连报错都没有。

## 1、忘了 commit

先看一段代码：建一张表，插入一行，关掉，再重新打开数一数：

```python
import os
import sqlite3

if os.path.exists('demo.db'):
    os.remove('demo.db')
conn = sqlite3.connect('demo.db')
conn.execute('CREATE TABLE t (x INTEGER)')
conn.execute('INSERT INTO t VALUES (1)')
conn.close()

conn = sqlite3.connect('demo.db')
print(conn.execute('SELECT COUNT(*) FROM t').fetchone())
```

输出的结果：

```
(0,)
```

明明插入了一行，重新打开数据库一看，却一行都没有。为什么呢？因为插入、修改、删除以后，要 `conn.commit()` 才会真正写进文件。这段代码没提交就关掉了，改动也就丢了。更麻烦的是，它还不会报错。

## 2、用 f-string 拼 SQL

下面这段代码，用 f-string 把书名拼进了 SQL 里：

<!-- skip-ci -->
```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE books (title TEXT)')
title = "Python's Book"
conn.execute(f"INSERT INTO books VALUES ('{title}')")
```

报错信息的最后一行是：

```
sqlite3.OperationalError: near "s": syntax error
```

问题出在书名里的那个单引号上。书名拼进 SQL 以后，它里面的单引号提前把字符串结束了，后面的 `s Book'` 就成了一堆看不懂的语法。

报错还算好的。更危险的是，如果拼进去的值来自别人，对方可以故意写一段 SQL 进去，改掉你的查询，这叫 **SQL 注入**。所以，SQL 里的值一律用 `?` 占位，交给 `execute()` 的第二个参数，sqlite3 会替你处理好引号：

```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE books (title TEXT)')
conn.execute('INSERT INTO books VALUES (?)', ("Python's Book",))
print(conn.execute('SELECT title FROM books').fetchone()[0])
```

输出的结果：

```
Python's Book
```

带单引号的书名，这回原样存进去了。

## 3、程序跑了两遍，数据存了两份

爬虫经常要重新跑。要是每跑一遍，就 `INSERT` 一遍，同一本书就存了好几份。怎么避免呢？给 `id` 设成 `PRIMARY KEY` ，再用 `INSERT OR REPLACE` 。这样同一个 `id` 的书，就会被新数据替换，而不是多出一行。下面用循环模拟跑了两遍，第二遍的价格多了 1 元：

```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, price REAL)')
for run in range(2):
    conn.execute('INSERT OR REPLACE INTO books VALUES (?, ?)', (1, 104.4 + run))
print(conn.execute('SELECT * FROM books').fetchall())
```

输出的结果：

```
[(1, 105.4)]
```

跑了两遍，表里还是只有一行，价格也换成了第二遍的新值。

## 4、csv 里的空值读回来是空字符串

第二节已经看到了：存进 csv 的 `None` ，读回来是 `''` 。这会有什么问题呢？空字符串交给 `float()` ，是会报错的。所以转换数字之前，要先判断一下。存 csv 的时候，心里就要有数：哪些字段可能是空的，读回来又该怎么处理。

# 六、自己查一次文档

回头看看第三节插入数据的代码，有个地方挺麻烦。插入之前，要先把每本书的字典，按列的顺序拆成一个元组：`(b['id'], b['title'], ...)` 。字段一多，顺序就很容易写错。那么，能不能直接把字典交给 sqlite3 呢？

带着这个问题，去查一查 sqlite3 的文档：[如何在 SQL 查询中使用占位符来绑定值](https://docs.python.org/zh-cn/3/library/sqlite3.html#sqlite3-placeholders) 。

文档一开头，先警告了一句：别用 Python 的字符串操作来拼 SQL，容易受到 SQL 注入攻击。这正是上一节的第 2 个坑。

接着往下看，文档说 SQL 语句可以用两种占位符：

- **问号风格**：`?` ，参数是一个序列，比如元组，长度要和问号的个数一样。咱们一直用的就是这种。
- **命名风格**：`:名字` ，参数是一个字典，要包含所有用到的名字，多出来的键会被忽略。

注意最后那半句：「多出来的键会被忽略」。这句话太有用了。为什么呢？因为接口拿回来的字典，键比表里的列还多。既然多出来的键会被忽略，那就可以把字典直接交进去。试一试，表里只建三列：

<!-- skip-ci -->
```python
import sqlite3

import requests

books = requests.get('https://learn-py.org/lab/bookstore/api/page-1.json').json()['books']
conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, price REAL)')
conn.executemany('INSERT INTO books VALUES (:id, :title, :price)', books)
print(conn.execute('SELECT COUNT(*), MAX(price) FROM books').fetchone())
print(conn.execute('SELECT * FROM books WHERE id = :id', {'id': 3}).fetchone())
```

输出的结果：

```
(20, 112.3)
(3, '早起养花', 56.2)
```

第一页的 20 本书都插进去了。`:id` 、`:title` 、`:price` 会按名字，从每个字典里取值，而 `author` 、`stock` 这些多出来的键，都被忽略了。查询的时候也一样，条件里用 `:id` ，再配一个字典就行。这样一来，不用再操心顺序，代码也好读多了。

文档后面还有一节，也值得一看：[如何使用连接上下文管理器](https://docs.python.org/zh-cn/3/library/sqlite3.html#sqlite3-connection-context-manager) 。还记得上一节的第 1 个坑，忘了 `commit()` 吗？这一节正好用得上。文档说，连接对象可以放在 `with` 语句里，`with` 里的代码没出错，就会自动提交。这样就不怕忘了 `commit()` 了：

```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE t (x INTEGER)')
with conn:
    conn.execute('INSERT INTO t VALUES (?)', (1,))
print(conn.execute('SELECT COUNT(*) FROM t').fetchone())
```

输出的结果：

```
(1,)
```

不过要注意：`with conn:` 只管提交，不会关闭连接，用完还是要 `conn.close()` 。`with` 背后的原理，基础课第 21 章再讲。

下面先做一道练习，用命名占位符把字典直接插进表里，再分组统计一下。

# 七、小结与回看

这一章，咱们把取到的数据存了下来：先存成 csv 和 json，再存进 sqlite3 数据库，还用 SQL 查了查。爬虫的最后一步「存储」，也学会了。回头梳理一下，学到了这几件事：

- 存下来，就不用重复抓，也能交给 Excel、pandas 用。
- 表格一样的数据存 csv，但读回来全是字符串，`None` 也变成了 `''` 。要保留数字和 `None` ，就存 json。
- sqlite3：`connect()` 打开数据库，`CREATE TABLE` 建表，`INSERT INTO` 插入，`executemany()` 批量插入，`commit()` 提交，`SELECT` 查询，`close()` 关闭。
- SQL 查询的骨架：`SELECT 列 FROM 表 WHERE 条件 GROUP BY 分组 ORDER BY 排序 LIMIT 几行` 。
- SQL 里的值一律用占位符：问号风格 `?` 配元组，命名风格 `:名字` 配字典，多出来的键会被忽略。
- 常见的坑：忘了 `commit()` ；用 f-string 拼 SQL；重复运行存了好几份，要用 `PRIMARY KEY` 加 `INSERT OR REPLACE` 。
- `with conn:` 能让改动自动提交。

哪里卡住了，就回去看一看：

- csv、json 的读写：实战 5
- 元组：第 3 章
- 从接口取回全部图书：爬虫课第 7 章

到这里，获取、解析、提取、存储，爬虫的四步就都学完了。不过，这些本事都是一章一章分开练的。下一章是综合项目：把这几章的本事串起来，写一个完整的书店爬虫，从列表页、详情页一路抓到底，存成数据分析课要用的 `books.csv` 。
