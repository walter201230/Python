# 爬虫第 12 章：动态页面与并发

# 前言

各位童鞋，这是爬虫课的最后一章了。前面学的 `requests` 加 BeautifulSoup，已经能对付大多数网站了。可总有一些情况，它们对付不了。这一章，就来看其中的两种。

第一种：页面上的数据，要靠 JavaScript 才能显示出来，网页背后又找不到好用的接口。这时候，`requests` 只能拿到一个空架子。怎么办呢？那就请一个真正的浏览器来打开网页，等 JavaScript 跑完了，再取内容。这要用到 **Playwright** 。

第二种：要抓的页面很多，一页一页地等，实在太慢了。那就一次发出好几个请求，同时等它们回来，这叫**并发**。基础课第 22 章讲过 asyncio，这一章就配上 **httpx** ，把它用起来。

这两样都是「大杀器」，可用起来是有代价的：浏览器又慢又占资源；并发一不小心，就成了给网站施压。所以这一章花在「什么时候该用、怎么用得有分寸」上的篇幅，不会比讲用法的少。

学完这一章，这门爬虫课就结束了。最后还会说说，想继续深入的话，再往后可以学些什么。

**学这一章之前**，需要先学完 [爬虫课第 11 章](11-session-and-cookies.md) 。基础课第 22 章的 [async / await](../02-advanced/22-async.md) 学过更好，没学过也没关系，这一章会先把用到的部分讲够。

# 目录

这一章会学到：

- 一、requests 拿不到的页面——数据在 JavaScript 里
- 二、让真正的浏览器来打开——Playwright
- 三、一次抓好几页——asyncio 加 httpx
- 四、再往后学什么——Scrapy 和更大的爬虫
- 五、常见坑
- 六、自己查一次文档——Semaphore 是怎么限制并发的
- 七、小结与回看

学完这一章，你能在需要的时候用浏览器自动化抓动态页面，用有节制的并发加快抓取，也知道下一步该往哪儿学。

# 一、requests 拿不到的页面

先看第一种情况。quotes.toscrape.com 有一个专门的练习页 `/js/` 。在浏览器里看，它和首页一样，有 10 条名言；可它的内容，是 JavaScript 生成的。用 `requests` 取一下，看看会怎样：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://quotes.toscrape.com/js/').text
soup = BeautifulSoup(html, 'html.parser')
print(len(soup.select('div.quote')))
print('var data' in html)
```

在自己电脑上运行，输出是：

```
0
True
```

第一行是 0，一条名言都没找到。可第二行是 `True` ，说明网页里确实有 `var data` 这几个字。这是怎么回事呢？在浏览器里「查看网页源代码」，搜一下就能看到：名言的数据，写在一段 JavaScript 里。网页打开以后，再由 JavaScript 把它们一条条画到页面上。而 `requests` 拿到的，只是网站最初发回来的那份 HTML，里面还没有画好的名言。

遇到这种页面，该怎么办呢？按这个顺序想办法：

1. **先找接口**：打开「网络」面板，看看数据是不是从某个接口来的。有接口就用第 7 章的办法，最省事。
2. **再看源代码**：数据要是像这样直接写在 `<script>` 里，有时可以把那一段文字切出来，当 JSON 解析。不过 JavaScript 不一定是标准的 JSON，切的时候很容易出错，网站一改就失效。
3. **最后才用浏览器**：前两条都走不通，就让一个真正的浏览器去打开网页，等 JavaScript 跑完，再取内容。

第三条用浏览器，是这一章新学的本事。具体怎么做，下一节就来讲。

# 二、让真正的浏览器来打开

上一节说到，实在没办法的时候，就让一个真正的浏览器去打开网页。可浏览器是给人用的，程序怎么去操作它呢？这就要靠 **Playwright** 了。它能用代码控制浏览器：打开网页、等元素出现、点按钮、填表单、取内容，就像有一个看不见的人，在替你操作浏览器。

用之前，先安装。它除了 Python 包，还要下载浏览器本身：

```bash
python -m pip install playwright
python -m playwright install chromium
```

第二条命令会下载一个 Chromium 浏览器，有一百多 MB，要等一会儿。

装好以后，就来打开上一节那个 `/js/` 页面。等名言出现了，再把网页交给 BeautifulSoup：

<!-- skip-ci -->
```python
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://quotes.toscrape.com/js/')
    page.wait_for_selector('div.quote')
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, 'html.parser')
quotes = soup.select('div.quote')
print(len(quotes))
print(quotes[0].select_one('.author').get_text())
```

在自己电脑上运行，输出是：

```
10
Albert Einstein
```

这回，10 条名言都取到了。这段代码的前半段是新东西，咱们一行一行地看：

- `sync_playwright()` 启动 Playwright，`p.chromium.launch()` 打开一个 Chromium 浏览器。默认是**无头**模式，也就是浏览器在后台运行，不弹出窗口。想看着它操作，就写成 `launch(headless=False)` 。
- `page.goto(网址)` 打开网页。`page.wait_for_selector('div.quote')` 会一直等，等到页面上出现了名言，也就是 JavaScript 跑完了，才往下走。
- `page.content()` 取出**此时**的 HTML，也就是开发者工具「元素」面板里看到的那一份，里面已经有名言了。
- 后面的部分，就是熟悉的 BeautifulSoup 了。

不过，要记住它的代价：启动一个浏览器要好几秒，还要占几百 MB 内存，比 `requests` 慢得多，也重得多。所以能用接口、能用 `requests` 的，就别用浏览器。

其实 Playwright 的本事，远不止抓数据，它还能点击、输入、截图。它的 [官方文档](https://playwright.dev/python/) 是英文的，写得很详细，需要的时候再去学。

# 三、一次抓好几页

动态页面的问题解决了，再来看第二种情况：页面太多，抓得太慢。

前面的爬虫，都是一页一页抓的：发出请求，等它回来，再发下一个。可是等待的时候，程序其实什么都没干，时间就这么白白过去了。

能不能不干等呢？这就是**并发**：同时发出好几个请求，一起等它们回来。基础课第 22 章讲的 asyncio，就是干这个的。不过 `requests` 不支持 asyncio，所以要换成一个用法和它很像的库：**httpx** 。先装上它：

```bash
python -m pip install httpx
```

并发到底能快多少？来比较一下：抓 quotes.toscrape.com 的前 5 页，一种是一页一页地抓，另一种是同时最多抓 2 页。两种都在每个请求之后停 0.5 秒：

<!-- skip-ci -->
```python
import asyncio
import time

import httpx

URLS = [f'https://quotes.toscrape.com/page/{n}/' for n in range(1, 6)]


def one_by_one():
    codes = []
    with httpx.Client(timeout=10) as client:
        for url in URLS:
            codes.append(client.get(url).status_code)
            time.sleep(0.5)
    return codes


async def together():
    limit = asyncio.Semaphore(2)

    async def get(client, url):
        async with limit:
            response = await client.get(url)
            await asyncio.sleep(0.5)
            return response.status_code

    async with httpx.AsyncClient(timeout=10) as client:
        return await asyncio.gather(*(get(client, url) for url in URLS))


start = time.monotonic()
print(one_by_one(), f'{time.monotonic() - start:.1f} 秒')
start = time.monotonic()
print(asyncio.run(together()), f'{time.monotonic() - start:.1f} 秒')
```

在自己电脑上运行，输出类似这样（时间每次不一样）：

```
[200, 200, 200, 200, 200] 4.4 秒
[200, 200, 200, 200, 200] 3.0 秒
```

同样是每次停 0.5 秒，并发的版本快了不少。一页一页抓的 `one_by_one()` ，是熟悉的写法，就不多说了。咱们把并发的部分拆开来看：

- `httpx.AsyncClient()` 是 httpx 的异步版客户端。`await client.get(url)` 发出请求以后，在等它回来的这段时间里，别的任务可以接着跑。
- `asyncio.gather(...)` 把 5 个任务一起交出去，等它们全部完成，再按原来的顺序返回结果。
- `asyncio.Semaphore(2)` 是关键。`async with limit:` 里面的代码，同一时间最多只有 2 个任务在跑，第 3 个任务，要等前面的出来了才能进去。

看到这里，可能有童鞋会问：「为什么不干脆 5 个一起抓呢？」因为**并发数，就是你同时压在网站上的请求数**。抓 5 页，倒没什么；可要是抓 5000 页时不加限制，一下子发出几千个请求，那和攻击网站就没什么两样了。所以用并发的时候，要记住这几条：

- 并发一定要配上 `Semaphore` ，限制数量。对小网站，两三个就够了。
- 每个请求之后，照样要停一停。
- 动手之前先算一算：同时 2 个，每个停 0.5 秒，相当于一秒最多 4 个请求，网站受得了吗？

并发的写法有点新，下面先做一道练习，把它练熟。

# 四、再往后学什么

写到这里，各位童鞋手里的爬虫本事，已经够用了：取网页、解析、找接口、存数据、登录、对付动态页面、有节制地并发。平时想抓点数据，这些本事就足够了。

那以后要是想写更大的爬虫呢？比如每天定时抓几万个页面，就会遇到一些新的问题：

- 抓过的网址要记下来，**别重复抓**。
- 失败的网址要**排队重试**。
- 抓下来的数据要**清洗、去重**，再存进数据库。
- 每个网站的**访问频率**，要分别控制。

这些事要是自己一件一件地写，会写出一大堆代码。这时候，可以去看看 **Scrapy** 。它是一个专门用来写爬虫的框架，上面这些事，它都有现成的办法。不过它的写法和这门课不太一样，要按它的规矩，把「怎么解析一页」「数据怎么存」分别写进不同的类里。所以不用急着学它。等你自己写过几个爬虫，开始觉得「这些事每次都要重写一遍」的时候，再去学，会更有体会。

除了工具，还有两样东西，同样值得花时间：

- **网络的基础知识**：HTTP 的更多细节、浏览器是怎么加载网页的、HTTPS 是怎么加密的。懂得越多，排查问题就越快。
- **数据的处理**：抓下来只是第一步，怎么整理、分析、画成图，正是下一门课「数据分析课」要讲的。你抓下来的 `books.csv` ，在那里还会派上用场。

最后，再把第 1 章的规矩说一遍。这一次，是说给本事更大了的你听：

- 抓之前，先看 robots.txt 和网站的条款。
- 放慢速度，限制并发，出了错就停。
- 说明自己是谁，不伪装。
- 不碰个人信息，不绕过登录和付费的限制。
- 别人不想让你拿的，就别拿。

# 五、常见坑

这一章的两样新工具，用起来都很有威力，可也都有容易踩的坑。下面这几个，最常见。

## 1、一上来就用浏览器

Playwright 什么页面都能对付，于是有的童鞋就不管三七二十一，什么网页都用它来抓。结果呢？爬虫又慢又占内存，几十个页面，就要跑上好几分钟。

所以还是那个顺序：先找接口，再试 `requests` ，都不行了，才用浏览器。就算用浏览器，也只让它做必须由它来做的那一步。比如用它登录，拿到 Cookie 以后，后面的请求再交还给 `requests` 。

## 2、没等内容出来就取

<!-- skip-ci -->
```python
page.goto('https://quotes.toscrape.com/js/')
html = page.content()
```

这两行少了什么？少了 `wait_for_selector()` 。`goto()` 一返回，就马上去取内容了。JavaScript 跑得快的时候，碰巧能取到；网络慢一点，取到的就是还没填好的页面。所以要等什么内容，就明确地等它出现。

## 3、并发不加限制

<!-- skip-ci -->
```python
await asyncio.gather(*(client.get(url) for url in urls))
```

这一句看着很简洁，可 `urls` 里要是有几千个网址，它就会同时向网站发出几千个请求。所以并发一定要用 `Semaphore` 之类的办法限制数量，再配上停顿。

## 4、调用异步函数时忘了 await

这个坑，在网页里就能试一试：

```python
import asyncio


async def fetch_page(n):
    await asyncio.sleep(0.1)
    return f'第 {n} 页'


result = fetch_page(1)
print(type(result).__name__)
result.close()
```

输出的结果：

```
coroutine
```

打印出来的类型是 `coroutine` ，可见 `result` 并不是函数里要返回的那句「第 1 页」。为什么呢？因为 `async def` 定义的函数，直接调用的时候并不会执行，只会得到一个**协程**对象。要拿到结果，得写成 `await fetch_page(1)` ，或者交给 `asyncio.gather()` 、`asyncio.run()` 。

那最后那句 `result.close()` 是干什么的？它是为了把这个没用上的协程关掉。不关的话，Python 会提醒你，有个协程从来没被等待过。所以以后看到这个提醒，十有八九，就是哪里少写了 `await` 。

# 六、自己查一次文档

第三节用 `asyncio.Semaphore(2)` ，把同时发出的请求限制在了 2 个。可它是怎么做到的呢？去查一下文档：[asyncio.Semaphore](https://docs.python.org/zh-cn/3/library/asyncio-sync.html#asyncio.Semaphore) 。

文档里是这么说的：信号量管理着一个内部计数器。每次 `acquire()` ，计数器减一；每次 `release()` ，计数器加一。计数器不会降到零以下，`acquire()` 发现它是零的时候，就一直等，直到有别的任务 `release()` 。可选的 `value` 参数，是计数器的初始值，默认是 1。

文档还给了推荐的用法：写成 `async with sem:` 。写成这样以后，进去的时候会自动 `acquire()` ，出来的时候会自动 `release()` 。

这样就清楚了。`Semaphore(2)` 一开始，计数器是 2。前两个任务进去以后，计数器变成 0；第三个任务就只能在门口等，直到前面有一个出来。

道理说通了，再动手验证一下「同时最多 2 个」是不是真的。在网页里，可以用 `asyncio.sleep()` 代替真正的请求：

```python
import asyncio

running = 0
most = 0


async def task(limit, n):
    global running, most
    async with limit:
        running = running + 1
        most = max(most, running)
        await asyncio.sleep(0.1)
        running = running - 1


async def main():
    limit = asyncio.Semaphore(2)
    await asyncio.gather(*(task(limit, n) for n in range(6)))
    print(f'6 个任务，同时最多 {most} 个在跑')


asyncio.run(main())
```

输出的结果：

```
6 个任务，同时最多 2 个在跑
```

这段代码靠两个变量来数数：`running` 记着此刻有几个任务在 `async with` 里面，`most` 记着最多的时候有几个。结果是 6 个任务，同时最多只有 2 个在跑，和文档说的一样。各位童鞋也可以把 `Semaphore(2)` 改成 `Semaphore(3)` ，再运行一次看看。

代码里还有两处，可能会让人疑惑：

- `global` 是基础课第 6 章补充一节讲过的关键字。在这里，它让函数能改外面的两个计数变量。
- 打印为什么放在 `main()` 里面？因为网页里的 `asyncio.run()` 不会把结果交回来，所以最好在异步函数里面，就把要看的东西打印出来。

`Semaphore` 弄明白了，下面还有两道练习：一道用它限制同时在跑的任务数，另一道看看其中一个任务出错时，怎样让别的任务照常完成。

# 七、小结与回看

这一章，咱们看了 `requests` 对付不了的两种情况。回头梳理一下，学到了这几件事：

- 数据要靠 JavaScript 才显示的时候：先找接口，再看源代码，最后才用浏览器。
- Playwright 能控制一个真正的浏览器：`goto()` 打开网页，`wait_for_selector()` 等内容出现，`content()` 取出 HTML，再交给 BeautifulSoup。它又慢又重，只在必要时用。
- 并发：httpx 的 `AsyncClient` 配上 `asyncio.gather()` ，就能同时发请求。但一定要用 `Semaphore` 限制并发数，而且照样要停顿。
- 异步函数直接调用，只会得到一个协程，要 `await` 它，或者交给 `gather()` 、`run()` 。
- `Semaphore` 靠一个计数器，限制同时进入的任务数，推荐写成 `async with` 。
- 更大的爬虫，可以去学 Scrapy；抓下来的数据，就交给数据分析课。

哪里卡住了，就回去看一看：

- async / await 和 `gather()` ：第 22 章
- `global` ：第 6 章的补充「函数里的变量，外面看得见吗？」
- 找接口：爬虫课第 7 章

到这里，爬虫课就全部学完了。回头看看这一路：从第 1 章的三行代码开始，咱们学了取网页、看懂 HTML、BeautifulSoup、清洗数据、翻页、找接口、存数据库、写完整的爬虫，又回到自己电脑上，抓真实的练习网站、登录、对付动态页面。

本事越大，越要记得第 1 章立下的规矩。写爬虫的人守规矩，网站才愿意把数据公开出来，大家都能受益。

接下来，可以去学数据分析课了。你抓下来的那份 `books.csv` ，正在那边等着你。
