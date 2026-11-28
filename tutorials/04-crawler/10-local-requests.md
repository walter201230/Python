# 爬虫第 10 章：回到自己电脑：本地环境与练习网站

# 前言

各位童鞋，前 9 章的代码都是在网页里运行的，抓的也都是本站的两点书店。在网页里运行很方便，什么都不用装。可它也有限制：只能抓 learn-py.org 上的网页，不能自己设 User-Agent，而且每次运行最多 5 秒。

所以从这一章开始，咱们回到自己电脑上。在自己电脑上，这些限制就都没有了：`requests` 能去请求任何网站，能带上自己的请求头，想跑多久就跑多久。不过，本事大了，第 1 章立下的那些规矩，也就更要紧了。

那抓什么网站来练手呢？咱们换成一个专门给初学者练手的公开网站：**toscrape**。它的首页写得明明白白，自己就是一个给人练习抓取的沙箱。抓它，既能遇到真实网站上的各种情况，又不用担心给谁添麻烦。

还要提前说一句：第一次在自己电脑上装包、配环境，难免会遇到各种报错，比如命令找不到、包装到了别的地方、网络连不上。碰到了别着急，按实战 3 的办法，先看报错的最后一行，再一步一步地排查。环境只要配好一次，以后就都顺了。

**学这一章之前**，需要先学完 [爬虫课第 9 章](09-bookstore-project.md) ，并且已经按 [基础课第 1 章](../01-basics/01-hello-world.md) 的说明，在自己电脑上装好了 Python 3.10 或更新的版本。

# 目录

这一章会学到：

- 一、准备环境——虚拟环境和 `pip install`
- 二、在自己电脑上跑书店爬虫——同样的代码，原样能跑
- 三、抓一个真实的练习网站——books.toscrape.com
- 四、说明自己是谁——User-Agent
- 五、常见坑
- 六、自己查一次文档——requests 是怎么决定编码的
- 七、小结与回看

学完这一章，你能在自己电脑上配好爬虫的环境，礼貌地抓取一个真实的网站，并处理好编码这类网页里遇不到的问题。

# 一、准备环境

在自己电脑上写爬虫，第一件事是把环境准备好。先看看电脑上的 Python 版本够不够新。打开终端（Windows 上是「命令提示符」或 PowerShell），输入：

```bash
python3 --version
```

Windows 上一般用 `python --version` 。只要看到 `Python 3.10` 或者更高的版本号，就可以了。

版本没问题，接下来给爬虫建一个单独的文件夹，在里面建一个**虚拟环境**。虚拟环境是什么呢？简单说，就是专门给这个项目准备的一套 Python 包，和电脑上别的项目互不干扰。用下面这三条命令建好它：

```bash
mkdir my-crawler
cd my-crawler
python3 -m venv .venv
```

前两条命令建好文件夹，再进到里面。最后一条 `python3 -m venv .venv` ，意思是在当前文件夹里，建一个名叫 `.venv` 的虚拟环境。建好了还不能直接用，接着还得**激活**它：

```bash
source .venv/bin/activate
```

Windows 上要换成 `.venv\Scripts\activate` 。激活以后，命令行的前面会多出 `(.venv)` 这几个字，说明现在用的，就是这个虚拟环境里的 Python 了。

虚拟环境准备好了，最后装上这门课用到的两个包：

```bash
python -m pip install requests beautifulsoup4
```

装好以后，试一试能不能导入：

```bash
python -c "import requests, bs4; print(requests.__version__, bs4.__version__)"
```

能打印出两个版本号，环境就准备好了。

这几步里，有几个地方要说明一下：

- 包的名字叫 `beautifulsoup4` ，可导入的时候要写 `bs4` ，第 4 章说过。
- 装包用的是 `python -m pip` ，而不是直接敲 `pip` 。这样能保证，包装进的就是当前这个 Python。为什么要这样，第五节「常见坑」会讲。
- 每次重新打开终端，都要先 `cd` 到这个文件夹，再激活一次虚拟环境。
- 基础课第 23 章会讲一个更新的工具 `uv` ，用它管理环境和包更省事。现在先用 Python 自带的 `venv` 和 `pip` 。

环境配好了，先拿上一章写好的书店爬虫来试一试。

# 二、在自己电脑上跑书店爬虫

在网页里写的爬虫，搬到自己电脑上，还能不能跑？试一试就知道了。

把第 9 章「六、完整的爬虫」里的那段代码，原样存成 `bookstore.py` ，放在 `my-crawler` 文件夹里。然后在激活了虚拟环境的终端里，运行它：

```bash
python bookstore.py
```

在自己电脑上运行，输出是这样的：

```
接口：取到 120 本
校验：第 1 页 20 本全部对得上
已存成 my_bookstore.csv
```

和在网页里运行的结果一模一样。再看看文件夹，里面多了一个 `my_bookstore.csv` ，用记事本或者 Excel 都能打开。这回，它是真的存在你的硬盘上了，不会刷新一下页面就没了。

可见，在网页里写的爬虫，几乎不用改，就能在自己电脑上跑。不过，有两个地方，到了自己电脑上应该改一改：

- **停顿时间**：`fetch()` 里的 `pause=0.2` 设得这么短，是因为网页里每次运行最多只有 5 秒。在自己电脑上没有这个限制，就改成 `pause=1` 或者更长。
- **说明自己是谁**：网页里改不了 User-Agent，在自己电脑上就可以带上了。怎么带，第四节就讲。

顺便说一句：`books.csv` 也可以不用自己抓，从本站的 [练习靶场](https://learn-py.org/lab/) 直接下载。以后数据分析课在自己电脑上运行时，需要的数据文件也都在那里。

自己写的爬虫，在自己电脑上能跑了。下一节，咱们就去抓一个真正的、别人的网站。

# 三、抓一个真实的练习网站

抓哪个网站呢？就是前言里提到的 toscrape。[toscrape.com](https://toscrape.com/) 是一组专门给人练习抓取的网站。它的首页说得很清楚：其中的 books.toscrape.com 是一家虚构的书店，「迫切地希望被抓取」，是初学者练习的安全场所。这一节就来抓它。

不过要先说在前面：它毕竟是别人的网站，以后可能会改版，也可能关闭。如果下面的代码跑不通了，先在浏览器里打开看看，网站还在不在、结构变没变。实在不行，就回到两点书店练习。

抓别人的网站，第一件事做什么？当然是先看看人家的规矩。

**第一步，看 robots.txt。** 到了自己电脑上，`RobotFileParser` 可以用 `read()` 自己去把 robots.txt 取回来了：

<!-- skip-ci -->
```python
from urllib.robotparser import RobotFileParser

parser = RobotFileParser('https://books.toscrape.com/robots.txt')
parser.read()
print(parser.can_fetch('*', 'https://books.toscrape.com/catalogue/page-2.html'))
```

在自己电脑上运行，输出是：

```
True
```

结果是 `True` ，可以抓。不过这里有个小细节：这个网站其实没有 robots.txt，请求它会得到 404。没有规则，`RobotFileParser` 就认为全部都可以抓，`True` 就是这么来的。

规矩看过了，接下来就可以取网页了。

**第二步，取首页看看。** 除了第一本书的价格，顺便把状态码、响应头里的 `content-type` 和 `requests` 用的编码，也都打印出来：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

response = requests.get('https://books.toscrape.com/')
print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.select_one('article.product_pod .price_color').get_text())
```

在自己电脑上运行，输出是：

```
200
text/html
ISO-8859-1
Â£51.77
```

状态码是 200，网页取到了。可是看最后一行，价格前面多了个 `Â` ！这是怎么回事？

这就是第 2 章「常见坑」里说过的乱码。网站的 `content-type` 只写了 `text/html` ，没写 `charset` ，`requests` 就按 `ISO-8859-1` 来解码。可网页其实是 UTF-8 的，这么一解码，英镑符号 `£` 就成了 `Â£` 。

那为什么在两点书店里，从来没遇到过这个问题呢？因为两点书店的响应头里写清了编码。到了真实的网站，就碰上了。

原因找到了，修起来就简单了。

**第三步，告诉 requests 正确的编码，再取数据。** 先在开发者工具里看看网页的结构：每本书是一个 `article.product_pod` ，书名完整地写在链接的 `title` 属性里，价格在 `.price_color` 里。照着这个结构来写：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

response = requests.get('https://books.toscrape.com/')
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')
for book in soup.select('article.product_pod')[:3]:
    title = book.h3.a['title']
    price = float(book.select_one('.price_color').get_text().replace('£', ''))
    print(title, price)
```

在自己电脑上运行，输出是：

```
A Light in the Attic 51.77
Tipping the Velvet 53.74
Soumission 50.1
```

可以看到，`response.encoding = 'utf-8'` 这一行一加，`£` 就正常了。再把 `£` 去掉，价格就能转成数字。

还有一个问题：书名为什么要取 `title` 属性，而不是直接取链接的文字呢？在开发者工具里看一眼就知道了：书名长的时候，链接上显示的文字是截断的，后面带着 `...` ，完整的书名只有 `title` 属性里才有。所以写选择器之前，一定要先去开发者工具里，看看网页实际的样子。

修乱码、取完整的书名，这两件事下面各有一道练习，先动手做一做。

# 四、说明自己是谁

真实的网站能抓了，可还有一件事，一直没顾上做。第 1 章说过，有礼貌的爬虫，要说明自己是谁。在网页里改不了 User-Agent，现在回到自己电脑上，终于可以做这件事了。

先看看，`requests` 默认的 User-Agent 是什么：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://books.toscrape.com/')
print(response.request.headers['User-Agent'])
```

在自己电脑上运行，输出类似这样（版本号可能不一样）：

```
python-requests/2.34.2
```

它只说了一句「我是 requests」。网站管理员看到了，也不知道是谁在抓、为什么抓，出了问题又该去找谁。

所以要带上自己的 User-Agent，写清楚是什么程序、怎么联系你。下面这段代码，就带着它连着抓了 3 页：

<!-- skip-ci -->
```python
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'learn-py-practice/1.0 (contact: you@example.com)'}
url = 'https://books.toscrape.com/catalogue/page-1.html'
total = 0
for _ in range(3):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    total = total + len(soup.select('article.product_pod'))
    print(url, total)
    next_link = soup.select_one('li.next a')
    if next_link is None:
        break
    url = urljoin(url, next_link['href'])
    time.sleep(1)
print(response.request.headers['User-Agent'])
```

在自己电脑上运行，输出是：

```
https://books.toscrape.com/catalogue/page-1.html 20
https://books.toscrape.com/catalogue/page-2.html 40
https://books.toscrape.com/catalogue/page-3.html 60
learn-py-practice/1.0 (contact: you@example.com)
```

看最后一行，发出去的 User-Agent，已经换成了咱们自己写的那一串。

这一段代码，把前面几章的规矩都用上了，咱们一条一条地看：

- `headers=HEADERS` 带上了 User-Agent。自己用的时候，记得把 `you@example.com` 换成你自己的联系方式。
- `timeout=10` ，不让程序傻等。
- `time.sleep(1)` ，在自己电脑上，每抓一页停 1 秒。
- `for _ in range(3)` ，只抓 3 页。网站一共有 50 页，练习的时候没必要全抓。变量名写成 `_` ，表示这个循环变量用不上。
- 「下一页」的链接 `page-2.html` 是相对链接，要用 `urljoin()` 补全。

最后还要说一句：User-Agent 是用来**说明身份**的，不是用来**伪装身份**的。网上常见一种做法：把 User-Agent 改成浏览器的样子，假装自己不是爬虫。这正是这门课不教的那一类做法。网站要是明确拒绝爬虫，就尊重它。

# 五、常见坑

回到自己电脑上，本事是大了，可也多了一些在网页里遇不到的麻烦。下面这几个坑，第一次在自己电脑上写爬虫时，很容易碰上。

## 1、装了包，却说找不到

明明 `pip install requests` 已经成功了，一运行代码，却报错了，最后一行是：

```
ModuleNotFoundError: No module named 'requests'
```

包明明装了，为什么还说找不到呢？多半是因为电脑上有好几个 Python，`pip` 把包装给了其中一个，运行代码的却是另一个。解决办法有这么几条：

- 先确认虚拟环境激活了，也就是命令行的前面有 `(.venv)` 。
- 装包时用 `python -m pip install` ，让「装包的」和「运行的」是同一个 Python。
- 用编辑器运行代码时，看看它选的是不是 `.venv` 里的 Python。

## 2、中文、英镑符号变成了乱码

这个坑，第三节已经遇到过了：网站没写编码，`requests` 就猜成了 `ISO-8859-1` 。所以以后看到 `Â£` 、`ä¸` 这类怪字符，先打印 `response.encoding` 看看，再在取 `text` 之前，把它设成正确的编码。正确的编码，多半是 `'utf-8'` 。

## 3、连不上网站

在自己电脑上，还可能遇到网页里遇不到的网络问题。这时候报错的最后一行，可能是下面这几种：

- `requests.exceptions.ConnectionError` ：连不上，可能是网址写错了，或者网络断了。
- `requests.exceptions.SSLError` ：加密连接出了问题，常见于公司、学校的网络。
- `requests.exceptions.ProxyError` ：电脑设置了代理，代理那边出了问题。

碰到这些报错，先别急着改代码，在浏览器里打开同一个网址试试。要是浏览器也打不开，那就是网络的问题；浏览器打得开，再看看是不是代理、证书的设置不一样。还有一点要记住：别为了让程序跑通，就去关掉证书检查之类的安全措施。

## 4、在自己电脑上「放开了抓」

在网页里，每次运行最多 5 秒，这个限制客观上让爬虫快不起来。可到了自己电脑上，程序想跑多快就跑多快，想跑多久就跑多久，没有谁拦着你。所以这时候，更要自觉：每页至少停 1 秒，先抓几页试试，确认没问题了，再慢慢扩大范围。

# 六、自己查一次文档

第三节修乱码的时候，咱们是照着做的：改一下 `response.encoding` ，问题就解决了。可是 `requests` 到底是怎么决定用哪种编码的？为什么改了 `response.encoding` ，就能修好乱码？这一回，咱们去查 requests 自己的文档。要先说明一下：它的文档是英文的，没有官方的中文版。

打开 [Quickstart 里的 Response Content](https://requests.readthedocs.io/en/latest/user/quickstart/#response-content) 这一节，一段一段地读下来，它说的是这几件事：

- `requests` 会自动给服务器发回来的内容**解码**，大多数编码都能处理好。
- 用哪种编码，是它根据**响应头**猜出来的。books.toscrape.com 的响应头里没写 `charset` ，它只能按规范里的默认值猜，就猜成了 `ISO-8859-1` 。
- 文档原话是：「You can find out what encoding Requests is using, and change it」，也就是说，用的是哪种编码可以通过 `r.encoding` 查看，也可以改。
- 改了以后，再取 `r.text` ，就会按新的编码来解码。

读到这里，第三节那个修法就说得通了：先改 `response.encoding` ，再取 `response.text` ，这个顺序不能反。

文档接着还说，HTML 和 XML 可以在正文里写明自己的编码。这种情况下，可以先从 `r.content` 里找到编码，再设置 `r.encoding` 。其实 books.toscrape.com 的网页开头，就写了 `<meta http-equiv="content-type" content="text/html; charset=UTF-8" />` ，编码写得明明白白。只是 `requests` 不看正文，只看响应头，所以还是猜错了。

英文文档读起来慢一点，不要紧。一句一句地读，碰到不认识的词就查一下，再像上面这样，用自己的话把意思说一遍。很多好用的库只有英文文档，所以这个本事，迟早用得上。

# 七、小结与回看

这一章，咱们的爬虫走出了网页，回到了自己电脑上。回头梳理一下，学到了这几件事：

- 准备环境：用 `python3 -m venv .venv` 建虚拟环境，激活以后，再用 `python -m pip install requests beautifulsoup4` 装包。
- 网页里写的爬虫，在自己电脑上几乎原样就能跑。要改的只有两处：把停顿改长，带上自己的 User-Agent。
- 抓真实网站之前，先看 robots.txt。在自己电脑上，`RobotFileParser.read()` 能直接去读。没有 robots.txt，就是没有限制。
- 网站没在响应头里写编码时，`requests` 会猜成 `ISO-8859-1` ，出现 `Â£` 这类乱码。解决办法是在取 `text` 之前，设好 `response.encoding` 。
- User-Agent 用来说明身份，写清是什么程序、怎么联系你，不用来伪装。
- 常见坑：包装错了 Python，就用 `python -m pip` ；碰到网络、代理、证书的报错，先用浏览器排查。
- requests 的文档是英文的，一句一句地读，再用自己的话复述一遍。

哪里卡住了，就回去看一看：

- 安装 Python：第 1 章
- 编码与乱码：爬虫课第 2 章「六、常见坑」
- 完整的书店爬虫：爬虫课第 9 章

在自己电脑上，`requests` 还有一个在网页里做不到的本事：记住登录状态。下一章，咱们去 toscrape 的另一个网站上，练习登录以后再抓。
