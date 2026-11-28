# 爬虫第 2 章：一次请求发生了什么

# 前言

上一章，咱们用三行代码就取回了一个网页。`requests.get()` 用起来很简单，可它背后到底发生了什么，咱们还没有细看。

有的童鞋可能会想：能取回来不就行了，为什么还要弄清楚这些？因为写爬虫的时候，问题多半就出在这里。比如网址拼错了一个字符，状态码不是 200 却没发现，拿回来的不是网页而是一段数据，或者中文变成了乱码……

不知道各位童鞋有没有这种体会：程序一跑不通，就只会盯着自己的代码看。其实很多时候，答案就写在网站发回来的响应里，只要你知道去哪儿找。

所以这一章，咱们把一次请求从头到尾拆开来看：网址由哪几部分组成，程序发出去的是什么，网站发回来的又有些什么。

**学这一章之前**，需要先学完 [爬虫课第 1 章](01-crawler-intro.md) ，会用 `requests.get()` 取回网页、看状态码。

# 目录

这一章会学到：

- 一、网址由哪几部分组成——用 `urlparse()` 把网址拆开
- 二、请求和响应——程序发出去什么，网站发回来什么
- 三、状态码——200、404 之外，还有哪些
- 四、拿回来的不一定是网页——JSON 数据和 `response.json()`
- 五、查询参数——`params` 帮你拼网址
- 六、常见坑
- 七、自己查一次文档——每个状态码叫什么名字
- 八、小结与回看

学完这一章，你能看懂一次请求的来龙去脉，取回网页以后知道先检查什么、去哪儿找问题。

# 一、网址由哪几部分组成

拆开一次请求，先从最熟悉的网址说起。下面是一个完整的网址：

```
https://learn-py.org/lab/bookstore/page/2/?sort=price#top
```

别看它是一整串，其实是由好几段拼起来的。怎么看出是哪几段呢？Python 自带的 `urllib.parse` 模块，就能把它拆开：

```python
from urllib.parse import urlparse

parts = urlparse('https://learn-py.org/lab/bookstore/page/2/?sort=price#top')
print(parts.scheme)
print(parts.netloc)
print(parts.path)
print(parts.query)
print(parts.fragment)
```

输出的结果：

```
https
learn-py.org
https://learn-py.org/lab/bookstore/page/2/
sort=price
top
```

拆出来一共五段。每一段是什么，对照下面这张表，一段一段地看：

| 部分 | 例子 | 是什么 |
|---|---|---|
| `scheme` | `https` | 协议，也就是怎么跟网站说话。`https` 是加密过的，比 `http` 安全 |
| `netloc` | `learn-py.org` | 域名，网站在哪儿 |
| `path` | `https://learn-py.org/lab/bookstore/page/2/` | 路径，要网站上的哪个网页 |
| `query` | `sort=price` | 查询参数，`?` 后面的部分，给网站附带的要求，比如按价格排序 |
| `fragment` | `top` | 锚点，`#` 后面的部分，只在浏览器里用来跳到页面的某个位置，不会发给网站 |

这五段里，写爬虫时最常打交道的，是**路径**和**查询参数**。

先说路径。两点书店的列表页，就是靠路径来分页的：第 2 页是 `https://learn-py.org/lab/bookstore/page/2/` ，第 3 页是 `https://learn-py.org/lab/bookstore/page/3/` 。看出了这个规律，就能用循环把每一页的网址拼出来。上一章连着取好几页，用的就是这个办法。

再说查询参数。上面的例子里只有一个参数，其实查询参数可以有好几个，用 `&` 连起来。要把它们一个一个分开，可以用同一个模块里的 `parse_qs()` ，它能把查询参数拆成字典：

```python
from urllib.parse import parse_qs

print(parse_qs('page=2&sort=price&tag=编程'))
```

输出的结果：

```
{'page': ['2'], 'sort': ['price'], 'tag': ['编程']}
```

细心的童鞋会发现，每个值都装在了一个列表里，连只有一个值的 `page` 也是这样。为什么要这样呢？因为同一个参数可以出现好几次，比如 `tag=编程&tag=小说` ，这时候一个值就装不下了。

下面先做一道练习，用 `urlparse()` 和 `parse_qs()` 自己拆一个网址。

# 二、请求和响应

网址弄清楚了，接下来看看程序拿着网址去找网站的时候，双方是怎么一来一回的。

程序和网站之间说话的规矩，叫 **HTTP**。按这个规矩，一次对话分成两半：

- **请求**（request）：程序发给网站的。里面有请求方法（取网页用 `GET` ）、网址，以及一些附加信息，叫**请求头**（headers）。
- **响应**（response）：网站发回来的。里面有状态码、**响应头**，以及正文，也就是网页本身。

`requests.get()` 返回的响应对象，已经把这些都装好了。咱们先来看响应这一半：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/books/1/')
print(response.url)
print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)
```

输出的结果：

```
https://learn-py.org/lab/bookstore/books/1/
200
text/html; charset=utf-8
utf-8
```

状态码上一章就认识了，另外三样是新的：

- `response.url` ：实际取到的网址。
- `response.headers` ：响应头，用起来像一个字典。其中 `content-type` 说明正文是什么类型：`text/html` 是网页，`charset=utf-8` 是文字的编码。
- `response.encoding` ：`requests` 根据 `content-type` 里的 `charset` ，决定用什么编码把正文变成字符串。

响应里最要紧的是正文。上一章用的是 `response.text` ，其实正文有两种取法：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/books/1/')
print(type(response.content))
print(type(response.text))
print(response.content[:15])
```

输出的结果：

```
<class 'bytes'>
<class 'str'>
b'<!doctype html>'
```

从输出就能看出两者的区别。`response.content` 是 `bytes` ，也就是网站发回来的原始字节，所以打印出来，前面多了一个 `b` 。`response.text` 是 `str` ，是按 `encoding` 解码好的字符串。

那平时该用哪一个呢？处理网页，用 `text` ；下载图片、压缩包这类不是文字的东西，用 `content` 。

响应这一半看完了，那请求这一半呢？程序发出去的东西，其实也查得到：`response.request` 记着程序发出去的请求。

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/')
print(response.request.method)
print(response.request.url)
```

输出的结果：

```
GET
https://learn-py.org/lab/bookstore/
```

可以看到，取网页用的请求方法是 `GET` ，网址也和咱们给的一样。以后提交表单、登录的时候，还会用到另一种方法 `POST` ，第 11 章再讲。

响应里的这几样东西，拿到手以后最先要看的，是状态码。上一章只见过两种，下一节就来看看，状态码还有哪些。

# 三、状态码

状态码都是三位数。记的时候不用一个一个地死记，先看第一位数字，它表示这个状态码属于哪一大类：

| 开头 | 意思 | 常见的 |
|---|---|---|
| 2 | 成功 | `200` 要到了 |
| 3 | 换个地方 | `301` 、`302` 网页搬家了，`requests` 会自动跟过去 |
| 4 | 你这边的问题 | `404` 没有这个网页，`403` 不让你看，`429` 请求太频繁了 |
| 5 | 网站那边的问题 | `500` 网站内部出错，`503` 网站暂时忙不过来 |

这几类里，写爬虫最要留意的是 `4` 开头的。为什么呢？因为 `403` 和 `429` 往往是网站在说「你请求得太多太快了」。这时候该做的是停下来，而不是换个法子接着请求，这也正是上一章说的「出了错就停」。

知道了状态码有哪些，接下来看看在代码里怎么检查。上一章是这么写的：`if response.status_code != 200` 。可每次都这么写，有点啰嗦。其实响应对象有个 `ok` 属性，状态码小于 400 时，它就是 `True` ：

<!-- skip-ci -->
```python
import requests

for url in ['https://learn-py.org/lab/bookstore/', 'https://learn-py.org/lab/bookstore/books/999/']:
    response = requests.get(url)
    print(response.status_code, response.ok)
```

输出的结果：

```
200 True
404 False
```

首页取到了，`ok` 是 `True` ；编号 999 的书不存在，`ok` 就是 `False` 。

不过，`ok` 只是告诉你成没成功，接下来怎么办，还得你自己写 `if` 。还有一种做法更干脆：一出错就直接报错，让程序停下来。这要用到 `raise_for_status()` ：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/books/999/')
response.raise_for_status()
print('这一行不会执行')
```

在自己电脑上运行，报错信息的最后一行是：

```
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://learn-py.org/lab/bookstore/books/999/
```

要是在网页里运行，会发现 `Not Found` 那里是空的。这是因为，这段说明文字是网站随状态码一起发回来的，浏览器转交给网页里的代码时，没有把它带上。不过状态码 `404` 是一样的，所以看状态码就够了。

那么，`raise_for_status()` 到底什么时候报错呢？状态码是 4 或 5 开头时，它就抛出 `HTTPError` ；状态码正常时，它什么都不做。所以它适合「出错了，后面就没必要再干了」的情况。要是想出错时换个办法处理，就要用 `try` / `except` 把它接住，这个基础课第 19 章会讲。

下面先做一道练习，看清楚几个网址各自拿回来的是什么。

# 四、拿回来的不一定是网页

前面取回来的，都是给人看的网页。可网站发回来的，不一定都是网页。比如两点书店，除了给人看的网页，还准备了给程序用的数据：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/api/books/1.json')
print(response.headers['content-type'])
print(response.text)
```

输出的结果：

```
application/json
{
  "id": 1,
  "title": "轻松玩转自动化",
  "author": "陈星河",
  "category": "编程",
  "price": 104.4,
  "rating": 4.7,
  "reviews": 13,
  "stock": 55,
  "pages": 220,
  "year": 2016,
  "description": "《轻松玩转自动化》是一本编程类的小书，2016 年出版。"
}

```

先看第一行，`content-type` 是 `application/json` ，说明这回的正文不是网页，而是 JSON。再看下面的正文，是不是很眼熟？没错，实战 5 用 `json.load()` 读过 JSON 文件，就是这个样子。

那么，怎么把它变成 Python 能用的数据呢？响应对象自带一个 `json()` 方法，能直接把正文变成 Python 的字典或列表：

<!-- skip-ci -->
```python
import requests

book = requests.get('https://learn-py.org/lab/bookstore/api/books/1.json').json()
print(type(book))
print(book['title'], book['price'])
```

输出的结果：

```
<class 'dict'>
轻松玩转自动化 104.4
```

拿到的是一个字典，想要哪一项，就用键去取，比从网页里一点一点地抠数据省事多了。其实很多网站的数据，就是这样从接口里来的，第 7 章会专门讲怎么找到它们。

下面先做一道练习，从接口里取几本书的信息。

# 五、查询参数

第一节说过，查询参数是网址里 `?` 后面的部分。很多网站就是用它来翻页、搜索、排序的，比如 `?page=2&sort=price` 。可网址里带的参数一多，自己用 f-string 拼起来，就容易漏写 `&` 或者 `=` 。

有没有省事的办法呢？`requests.get()` 有个 `params` 参数。把参数写成字典交给它，网址就由它来拼：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/', params={'page': 2, 'sort': 'price'})
print(response.url)
```

输出的结果：

```
https://learn-py.org/lab/bookstore/?page=2&sort=price
```

字典里的两项，变成了网址里的 `page=2` 和 `sort=price` ，中间的 `?` 和 `&` 也都替你加好了。

这还不算完。要是参数里有中文、空格这类不能直接放进网址的字符，它也会自动转换好：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/', params={'tag': '编程 入门'})
print(response.url)
```

输出的结果：

```
https://learn-py.org/lab/bookstore/?tag=%E7%BC%96%E7%A8%8B+%E5%85%A5%E9%97%A8
```

仔细看，中文变成了 `%E7%BC%96` 这样的一串，空格变成了 `+` 。这种转换，叫 **URL 编码**。为什么要转呢？因为网址里只能放一部分英文字符，其他字符都要这样转一下，网站收到以后，再把它们转回来。

不过，有一点要说明：两点书店是一个纯静态的网站，它不看查询参数，带不带 `?page=2` ，返回的都是首页。它分页靠的是路径 `/page/2/` ，这在第一节已经见过了。所以这里只是让你看看 `params` 怎么拼网址。真实网站里，参数的名字和用法各不相同，用之前要先在浏览器里点一点，看看网址是怎么变的。

# 六、常见坑

一次请求的来龙去脉拆完了。下面这几个坑，写爬虫时很容易碰上。

## 1、没看状态码，就去处理网页

先去取编号 999 的书。这本书并不存在，那拿回来的内容是不是空的呢？

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/books/999/')
print(len(response.text) > 0)
print(response.status_code)
```

输出的结果：

```
True
404
```

并不是空的。书明明没有，可 `response.text` 照样有内容，那是网站的「找不到网页」页面。要是不看状态码就往下处理，程序会在一个错误页面里找书名，找不到，你还以为是自己的代码写错了。

所以拿到响应以后，**先看状态码**，再处理内容。

## 2、中文变成了乱码

第二节说过，`requests` 是根据响应头里的 `charset` 来决定编码的。那要是网站在响应头里没写 `charset` 呢？这时候，`requests` 会按 `ISO-8859-1` 这种只认西文的编码来解码，中文就成了乱码。咱们用一段文字来模拟一下：

```python
text = '两点书店'
garbled = text.encode('utf-8').decode('iso-8859-1')
print(garbled)
print(garbled.encode('iso-8859-1').decode('utf-8'))
```

输出的结果：

```
ä¸¤ç¹ä¹¦åº
两点书店
```

第一行，就是乱码的样子；第二行按原路转回去，又变回了「两点书店」。所以以后看到这种「ä¸¤ç」开头的怪字符，八成就是 UTF-8 被当成了 ISO-8859-1。

那在爬虫里该怎么办呢？解决办法是在取 `text` 之前，先告诉 `requests` 正确的编码：

<!-- skip-ci -->
```python
response.encoding = 'utf-8'
print(response.text)
```

两点书店的响应头写清了 `charset=utf-8` ，所以不会出这个问题。等到第 10 章抓别的网站时，要是遇到了乱码，就先看看 `response.encoding` 是什么。

## 3、在网页里改不了 User-Agent

第二节说过，请求里还带着一些附加信息，叫请求头。请求头里有一项叫 `User-Agent` ，说明发请求的是什么程序。`requests` 允许你自己来设：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/', headers={'User-Agent': 'my-crawler/1.0'})
print(response.status_code)
```

输出的结果：

```
200
```

在自己电脑上，这个请求头会原样发出去。可是在网页里，请求是浏览器代发的，而浏览器不让网页里的代码改 `User-Agent` ，所以这一项会被悄悄忽略。这就是为什么第 1 章说的「说明自己是谁」，要到第 10 章回到自己电脑上才做得到。

## 4、网址末尾少了斜杠

看下面这两个网址：`https://learn-py.org/lab/bookstore/books/1/` 和 `https://learn-py.org/lab/bookstore/books/1` ，它们只差末尾一个 `/` 。可就这么一个字符，不同的网站处理起来却不一样：有的当成同一个网页，有的会先让你跳转一次，有的直接返回 404。所以复制网址的时候，要原样照抄，别自作主张地增减斜杠。

# 七、自己查一次文档

第三节那张状态码表，只列了最常见的几个。要是遇到一个没见过的，比如 `429` ，怎么知道它到底是什么意思呢？

答案就在 Python 自带的 `http` 模块里，它有一份完整的状态码清单。先去官方文档看看：[http.HTTPStatus](https://docs.python.org/zh-cn/3/library/http.html#http.HTTPStatus) 。

文档说，`HTTPStatus` 是一个枚举类，每个状态码都有自己的名字。往下翻，「HTTP 状态码」表格把它们全都列了出来：代码、枚举名，还有出自哪份规范。比如 `404` 对应的是 `NOT_FOUND` 。

表格看明白了，再用代码查一下，看看和文档对不对得上：

```python
from http import HTTPStatus

for code in [200, 301, 404, 429, 503]:
    status = HTTPStatus(code)
    print(code, status.name, status.phrase)
```

输出的结果：

```
200 OK OK
301 MOVED_PERMANENTLY Moved Permanently
404 NOT_FOUND Not Found
429 TOO_MANY_REQUESTS Too Many Requests
503 SERVICE_UNAVAILABLE Service Unavailable
```

每个状态码后面，打印出了两样东西：

- `name` 是枚举名，全大写，单词之间用下划线连接。
- `phrase` 是给人看的短语。第三节里 `raise_for_status()` 报错时说的 `Not Found` ，就是它。

再看 `429 Too Many Requests` ，意思是请求太多了，这正是第 1 章说的「网站嫌你太快」。

查到的名字，还能派上别的用场：`HTTPStatus` 可以直接拿来和状态码比较，代码读起来更清楚：

<!-- skip-ci -->
```python
from http import HTTPStatus

import requests

response = requests.get('https://learn-py.org/lab/bookstore/')
print(response.status_code == HTTPStatus.OK)
```

输出的结果：

```
True
```

`HTTPStatus.OK` 就是 `200` 。写成名字，读代码的人一眼就知道是什么意思，不用再去记数字。

# 八、小结与回看

这一章，咱们把取网页背后的一次请求，从头到尾拆开来看了一遍。回头梳理一下，学到了这几件事：

- 网址分为协议、域名、路径、查询参数和锚点。`urlparse()` 拆网址，`parse_qs()` 拆查询参数。
- 程序发出**请求**：方法（取网页用 `GET` ）、网址、请求头；网站发回**响应**：状态码、响应头、正文。
- `response.headers['content-type']` 说明正文的类型和编码；`response.text` 是解码好的字符串，`response.content` 是原始字节。
- 状态码看第一位：2 开头是成功，3 开头是换地方，4 开头是你这边的问题，5 开头是网站那边的问题。`response.ok` 、`raise_for_status()` 能帮你检查。
- 正文是 JSON 时，用 `response.json()` 直接变成字典或列表。
- 查询参数写成字典交给 `params` ，`requests` 会拼好网址、转好编码。
- 遇到没见过的状态码，用 `HTTPStatus` 查它的名字。

哪里卡住了，就回去看一看：

- 字典和列表：第 3、4 章
- JSON：实战 5 的「四、换成 json 试试」
- 编码和 `encoding='utf-8'` ：实战 5 的「五、常见坑」

到这里，「获取」这一步就算过关了：网页取回来了，也知道怎么判断取得对不对。可取回来的是一大段 HTML，书名、价格都埋在里面，该怎么把它们找出来呢？下一章，咱们先学会看懂 HTML，再用浏览器的开发者工具，找到数据藏在哪儿。
