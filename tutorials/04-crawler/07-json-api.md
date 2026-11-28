# 爬虫第 7 章：数据藏在接口里

# 前言

前几章抓的，都是直接写在 HTML 里的数据。可是现在的网站，很多内容并不在一开始发回来的 HTML 里。那它们是怎么来的呢？网页先打开一个空架子，再由网页里的 JavaScript 去另一个地址把数据要过来，填进页面。

遇到这种情况，`requests` 拿到的就只有那个空架子。很多童鞋第一次遇到时，都会一头雾水：浏览器里明明看得到，程序怎么就是取不到呢？

先别急着发愁，这往往是好事。为什么这么说呢？因为数据既然是从「另一个地址」要过来的，那个地址发回来的多半是 JSON，比 HTML 干净得多。只要找到它，直接请求它，连解析 HTML 的功夫都省了。这种专门发数据的地址，叫**接口**（API）。

所以这一章，咱们就去找这些藏在背后的接口：先用开发者工具的「网络」面板，看看网页都要了哪些数据，再用 `requests` 直接去要。

**学这一章之前**，需要先学完 [爬虫课第 6 章](06-pagination-and-politeness.md) ，会翻页，也会控制请求的节奏。另外，还要记得第 2 章讲过的 `response.json()` 。

# 目录

这一章会学到：

- 一、网页上有，requests 里没有——JavaScript 后来填的数据
- 二、在开发者工具里找接口——「网络」面板
- 三、直接请求接口——拿回来就是数据
- 四、分页的接口——顺着 `next` 一直取
- 五、常见坑
- 六、自己查一次文档——把嵌套的数据打印得好读一点
- 七、小结与回看

学完这一章，你能找到网页背后的数据接口，用几个请求就把整个书店的数据完整取下来。

# 一、网页上有，requests 里没有

先来看一个例子。在浏览器里打开两点书店的 [新书速递](https://learn-py.org/lab/bookstore/new/) ，能看到 8 本新书。那么，用学过的办法，能不能把它们取下来呢？试一试：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/new/').text
soup = BeautifulSoup(html, 'html.parser')
print(len(soup.select('li.new-book')))
print(soup.select_one('#new-books').get_text())
```

输出的结果：

```
0
正在加载……
```

结果一本都没取到，书单的位置上只有一句「正在加载……」。浏览器里明明看得到，这是怎么回事呢？

第 3 章说过，开发者工具「元素」面板里看到的，是运行完 JavaScript 以后的网页。而 `requests` 拿到的，是网站最初发回来的 HTML。这一页的书单，就是 JavaScript 后来才填进去的，所以 `requests` 拿到的 HTML 里还没有它。

那么，JavaScript 又是从哪儿拿到书单的呢？其实答案就写在 HTML 里。把 `<script>` 那一段找出来，打印前 60 个字符看看：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/new/').text
soup = BeautifulSoup(html, 'html.parser')
print(soup.select_one('script').get_text().strip()[:60])
```

输出的结果：

```
fetch('https://learn-py.org/lab/bookstore/api/new.json')
  .then((res) => res.js
```

这里的 `fetch()` ，是 JavaScript 里发请求的函数。也就是说，网页打开以后，它又去请求了 `https://learn-py.org/lab/bookstore/api/new.json` ，拿到 JSON，再把书单填进页面。

在这个例子里，一眼就能看出来。可真实网站的 JavaScript 往往有成千上万行，还被压缩成了一团，很难这样找。那该怎么办呢？更通用的办法，是去开发者工具的「网络」面板里看，下一节就来试试。

# 二、在开发者工具里找接口

为什么说「网络」面板（Network）更通用呢？因为它会记下网页打开过程中发出的**每一个请求**：HTML、图片、样式，还有 JavaScript 要数据的请求。不管 JavaScript 写成什么样，只要它去要了数据，这里就有记录。

下面就在新书速递页上试一试：

1. 打开开发者工具，切到「网络」面板。
2. 刷新网页。面板里会列出一串请求。
3. 在面板上方的筛选按钮里点「Fetch/XHR」，只看 JavaScript 发出的请求。列表里剩下一个 `new.json` 。
4. 点开它。在右边的「标头」（Headers）里，能看到完整的地址。在「预览」（Preview）或「响应」（Response）里，就是它发回来的数据：一个 `books` 列表，每本书有 `id` 、`title` 、`price` 。

这个例子筛完只剩一个请求，很好找。可真实的网站，一刷新就是一大串请求，该怎么找呢？有几个诀窍：

- 先筛 **Fetch/XHR** ，大部分数据请求都在这里。
- 不知道是哪个，就一个一个点开「预览」看，哪个里面有你要的数据，就是它。
- 在网页上翻页、搜索、点「加载更多」的时候，盯着「网络」面板，看看又多出了哪些请求，往往就能找到翻页的接口和参数。

找到接口以后，先别急着写代码，在浏览器里直接打开它的地址看看，比如 [new.json](https://learn-py.org/lab/bookstore/api/new.json) 。要是能直接看到 JSON，说明它不需要别的条件，用 `requests.get()` 就能拿到。

除了新书的接口，两点书店还有两个接口，后面几节会用到：

| 接口 | 发回什么 |
|---|---|
| `https://learn-py.org/lab/bookstore/api/page-1.json` 到 `page-6.json` | 每一页的 20 本书，以及下一页接口的地址 |
| `https://learn-py.org/lab/bookstore/api/books/编号.json` | 一本书的全部信息 |

其中第二个，第 2 章其实已经用过了。

接口都找到了，下一节就用 `requests` 直接去要数据。

# 三、直接请求接口

接口的地址找到了，剩下的就简单了：直接请求它，再用 `.json()` 把发回来的 JSON 变成 Python 的数据：

<!-- skip-ci -->
```python
import requests

data = requests.get('https://learn-py.org/lab/bookstore/api/new.json').json()
print(type(data), list(data.keys()))
for book in data['books']:
    print(book['id'], book['title'], book['price'])
```

输出的结果：

```
<class 'dict'> ['books']
10 留白的秘密 63.6
27 一步步做小工具 58.6
33 运河千年 71.4
72 迟到的来信 42.2
84 字体的力量 82.5
103 海洋的故事 38.5
30 图标的秘密 47.3
57 小熊找朋友 44.1
```

新书的编号、书名和价格，一下子就全拿到了。和前几章从 HTML 里抠数据比一比，省事在哪儿呢？

- 不用 BeautifulSoup，也不用写选择器。
- 价格本来就是数字 `63.6` ，不用去掉 `¥` 再转换。
- 网站改了页面的样子，只要接口不变，代码就不用改。

再看输出的第一行。拿到接口的数据，第一件事是先看清它的结构：最外层是什么类型，有哪些键，列表里的每一项又长什么样。`type()` 和 `keys()` 就是用来做这个的。从输出可以看到，最外层是一个字典，里面只有一个键 `books` 。

还有一点要留意：接口发回来的数据，和网页上显示的不一定完全一样。比如新书速递页上，价格显示成 `¥63.60` ，接口里却是 `63.6` 。再比如，网页上只显示书名和价格，详情接口里却有页数、出版年份和简介。看到接口里有、网页上没有的字段，不妨也拿下来，说不定以后用得上。

下面先做一道练习，自己请求新书接口，找出最便宜的是哪本。

# 四、分页的接口

新书没几本，一个请求就取完了。那全部图书呢？它的接口是分页的。按上一节说的，拿到数据先看结构。下面就取第 1 页看看：

<!-- skip-ci -->
```python
import requests

data = requests.get('https://learn-py.org/lab/bookstore/api/page-1.json').json()
print(data['page'], data['total_pages'], data['next'])
print(len(data['books']))
print(data['books'][2])
```

输出的结果：

```
1 6 https://learn-py.org/lab/bookstore/api/page-2.json
20
{'id': 3, 'title': '早起养花', 'author': '林子墨', 'category': '生活', 'price': 56.2, 'rating': None, 'reviews': 0, 'stock': 47, 'pages': 310, 'year': 2014}
```

可以看到，接口里除了 20 本书，还有三个字段：现在是第几页、一共几页，以及下一页接口的地址 `next` 。最后一页的 `next` 是 JSON 里的 `null` ，到了 Python 里就是 `None` 。

是不是很眼熟？这和第 6 章顺着「下一页」翻网页一模一样，只是这回的「下一页」写在了 JSON 里。所以代码的写法也差不多：只要 `url` 不是 `None` ，就接着取。全部取完以后，再数一数有几本没有评分，看看最贵的是哪本：

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
print(sum(1 for book in books if book['rating'] is None), '本没有评分')
print(max(books, key=lambda book: book['price'])['title'])
```

输出的结果：

```
120
11 本没有评分
实战做小工具
```

只用了 6 个请求，120 本书的全部字段就都拿到了，而且都是干干净净的数字和 `None` 。要是用取网页的办法，得先取 6 个列表页，再取 120 个详情页，还要一个一个地清洗。两边一比，差别就很明显了。

代码里还有两处写法，是基础课学过的，这里提一下：

- `books.extend(列表)` 把另一个列表里的元素都加进来，基础课第 3 章讲过。
- `max(books, key=...)` 按价格找出最贵的一本。`lambda` 是基础课第 6 章讲的匿名函数。

看到这里就明白了：写爬虫的第一步，往往不是写选择器，而是先打开「网络」面板，看看有没有现成的接口。

下面有两道练习：一道顺着 `next` 取完整个书店，另一道按编号去取新书的详细信息。

# 五、常见坑

接口用起来确实省事，不过也有几个坑，一不留神就会踩到。

## 1、对着网页调用 json()

先看一段代码，它请求的是第 9 页的接口：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/api/page-9.json')
print(response.status_code)
print(response.json())
```

先打印出 `404` ，接着报错，最后一行是：

```
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

为什么会这样呢？因为第 9 页的接口根本不存在，网站发回来的是一个「找不到网页」的 HTML 页面。拿 HTML 当 JSON 来解析，第 1 行第 1 个字符就对不上了，这就是报错里 `line 1 column 1` 的意思。

所以，调用 `json()` 之前，也要先看看状态码。拿不准的话，再看看响应头里的 `content-type` 是不是 `application/json` 。

## 2、只取了第一页

接口一次往往只给一部分数据，比如只给 20 条。要是拿到第一页，就以为是全部，数据就少了一大截。所以拿到接口的数据，先找找有没有 `next` 、`total_pages` 、`has_more` 这类字段，看看是不是分了页。

## 3、按网页上的样子去处理接口的数据

前面清洗过网页上的价格和星星。那接口里的价格和评分，也要这样处理吗？取第 1 本书看看：

<!-- skip-ci -->
```python
import requests

book = requests.get('https://learn-py.org/lab/bookstore/api/books/1.json').json()
print(book['price'] * 2)
print(book['rating'])
```

输出的结果：

```
208.8
4.7
```

价格直接乘以 2 就算出来了，评分打印出来是 4.7。可见，接口里的价格本来就是数字，评分是带小数的平均分，和网页上的「¥104.40」「★★★★★」完全是两回事。要是还照着网页的样子去 `replace('¥', '')` ，就会报错，因为数字没有 `replace()` 方法。所以处理之前，先 `print()` 出来，看看数据实际的样子。

## 4、接口也要守规矩

最后这个坑，不在代码上。接口不是「后门」，第 1 章立下的规矩，对接口一样管用：robots.txt 不让抓的地址，接口也不该去抓。接口返回得再快，请求之间也要停一停。有的接口要登录、要密钥才能用，那是网站不想公开给所有人，就别去想办法绕过。

# 六、自己查一次文档

上一节说过，处理接口的数据之前，先打印出来看看。可接口发回来的数据，常常是字典套列表、列表又套字典。直接 `print()` 出来是一长行，很难看清结构。比如第 6 页的接口，只看前 120 个字符：

<!-- skip-ci -->
```python
import requests

book = requests.get('https://learn-py.org/lab/bookstore/api/page-6.json').json()
print(str(book)[:120])
```

输出的结果：

```
{'page': 6, 'total_pages': 6, 'next': None, 'books': [{'id': 101, 'title': '看懂保险', 'author': '秦南风', 'category': '经济', 'p
```

才看了前 120 个字符，就已经挤成一团了。有没有办法打印得好读一点呢？Python 自带一个 `pprint` 模块，名字的意思是 pretty print，也就是「好看地打印」。去查一查文档：[pprint --- 数据美化输出](https://docs.python.org/zh-cn/3/library/pprint.html) 。

文档里有两个函数：[pprint.pp()](https://docs.python.org/zh-cn/3/library/pprint.html#pprint.pp) 和 `pprint.pprint()` 。它们有什么区别呢？看说明：`pp()` 打印对象的格式化表示形式，可以在交互式解释器里代替 `print()` ，用来检查对象的值。`pprint()` 和它一样，只是默认会把字典的键排好序。

`pp()` 的参数里，有两个正好用得上，可以控制打印出来的样子：

- `width` ：每一行最多多少个字符，超过了就换行。
- `depth` ：最多展开几层，更深的部分用 `...` 代替。

试一试。先只展开两层，看清整体的结构：

<!-- skip-ci -->
```python
from pprint import pp

import requests

data = requests.get('https://learn-py.org/lab/bookstore/api/page-6.json').json()
pp(data, depth=2)
```

输出的结果：

```
{'page': 6,
 'total_pages': 6,
 'next': None,
 'books': [{...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...},
           {...}]}
```

这回一眼就看清了：最外层有四个键，其中 `books` 是一个有 20 项的列表，每一项又是一个字典。因为只展开两层，这些字典都显示成了 `{...}` 。整体结构清楚了，再单独看看其中一本，用 `width` 把每一行设成最多 60 个字符：

<!-- skip-ci -->
```python
from pprint import pp

import requests

data = requests.get('https://learn-py.org/lab/bookstore/api/page-6.json').json()
pp(data['books'][0], width=60)
```

输出的结果：

```
{'id': 101,
 'title': '看懂保险',
 'author': '秦南风',
 'category': '经济',
 'price': 63.1,
 'rating': 5,
 'reviews': 1,
 'stock': 29,
 'pages': 467,
 'year': 2018}
```

每个键占一行，一本书有哪些字段，一目了然。

最后还要提醒一句：文档网址里的 `3` ，指的是最新版的 Python。参数表里有的参数比较新，说明里会标出它是哪个版本加上的。网页里运行的是 Python 3.12，所以用到某个参数报错时，先看看它是不是更新的版本才有的。

# 七、小结与回看

这一章，咱们从新书速递页上那份「取不到的书单」出发，一路找到了数据真正的来处：网页背后的接口。回头梳理一下，学到了这几件事：

- 网页上看得到、`requests` 却取不到，多半是因为数据是 JavaScript 后来从**接口**要过来的。
- 在开发者工具的「网络」面板里筛「Fetch/XHR」，一个个点开「预览」，就能找到接口。找到以后，先在浏览器里直接打开接口地址试一试。
- 直接请求接口，`json()` 拿回来就是字典和列表，不用写选择器，也不用清洗。
- 分页的接口顺着 `next` 取，和翻网页是同一个套路。
- 常见的坑：调用 `json()` 之前，先看状态码。接口的数据，要按它实际的样子处理。接口也要守规矩。
- 层次多的数据，用 `pprint.pp()` 打印：`depth` 控制展开几层，`width` 控制每行多宽。

哪里卡住了，就回去看一看：

- `response.json()` 和状态码：爬虫课第 2 章
- 顺着「下一页」翻页：爬虫课第 6 章
- 字典套列表的数据：第 3、4 章

现在，整个书店的数据都能取下来了。可是还有一个问题：程序一结束，这些数据就没了。下次想用，难道还要重新取一遍吗？下一章，咱们就把取到的数据存下来：存成 csv、json，还要认识一个新朋友——Python 自带的小数据库 sqlite3。
