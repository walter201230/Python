# 爬虫第 6 章：翻页与礼貌地爬

# 前言

上一章，咱们已经能把一页的 20 本书整整齐齐地取出来了。可是两点书店一共有 6 页，真实的网站更是动辄几十页、几百页。要是一页一页地手动去改网址，那就不叫爬虫了。

所以这一章，咱们要让爬虫自己**翻页**。办法有两种：一种是顺着页面上的「下一页」链接往下走，另一种是看出网址的规律，直接把每一页的地址拼出来。

能自己翻页了，请求也就跟着多了起来。这时候，第 1 章立下的规矩就要真正用起来了：每取一页，都要停一停。网站暂时出错了，就等一会儿再试，但别没完没了地试。循环要有出口，不能一直跑下去。

这些听上去都是小事，可真实的爬虫，很多就是栽在这些小事上：要么把网站拖垮了，要么被网站封掉了，要么半夜跑出一个死循环。所以写爬虫，慢一点不要紧，稳才是第一位的。

**学这一章之前**，需要先学完 [爬虫课第 5 章](05-extract-list.md) ，会用 `parse_list()` 把一页书取成列表，会用 `urljoin()` 补全链接。另外，还要熟悉基础课第 5 章的 `while` 循环和 `break` 。

# 目录

这一章会学到：

- 一、顺着「下一页」往下翻——`while` 循环加出口
- 二、看出网址规律，直接拼——先知道一共几页
- 三、出错了怎么办——超时、重试和放弃
- 四、常见坑
- 五、自己查一次文档——怎么确认真的停了 0.2 秒
- 六、小结与回看

学完这一章，你的爬虫能把整个书店的 120 本书一页不落地取下来，而且取得稳、取得有礼貌。

# 一、顺着「下一页」往下翻

先说第一种办法：顺着「下一页」往下翻。两点书店每一页的底部，都有一个「下一页」的链接，只有最后一页没有。这个链接在 HTML 里长什么样呢？取回第 2 页，把底部的翻页栏打印出来看看：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get('https://learn-py.org/lab/bookstore/page/2/').text, 'html.parser')
print(soup.select_one('nav.pager'))
```

输出的结果：

```
<nav class="pager"><a class="prev" href="https://learn-py.org/lab/bookstore/page/1/">上一页</a><span class="current">2 / 6</span><a class="next" href="https://learn-py.org/lab/bookstore/page/3/">下一页</a></nav>
```

可以看到，翻页栏里有「上一页」，有当前是第几页，最后是一个 `class` 为 `next` 的链接。这个 `a.next` ，就是下一页的链接。

有了它，翻页的思路就清楚了：

1. 取回当前页，把书取出来。
2. 找 `a.next` 。找到了，就补全地址，作为下一轮要取的网页。找不到，说明已经到了最后一页，就停下来。

把这个思路写成代码，从首页开始一页一页往下取，顺便数一数一共取到了几本书：

<!-- skip-ci -->
```python
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = 'https://learn-py.org/lab/bookstore/'
count = 0
while url:
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    count = count + len(soup.select('article.book-card'))
    print(url, count)
    next_link = soup.select_one('a.next')
    url = urljoin(url, next_link['href']) if next_link else None
    time.sleep(0.2)
print(f'一共 {count} 本书')
```

输出的结果：

```
https://learn-py.org/lab/bookstore/ 20
https://learn-py.org/lab/bookstore/page/2/ 40
https://learn-py.org/lab/bookstore/page/3/ 60
https://learn-py.org/lab/bookstore/page/4/ 80
https://learn-py.org/lab/bookstore/page/5/ 100
https://learn-py.org/lab/bookstore/page/6/ 120
一共 120 本书
```

6 页都取到了，一共 120 本书。那么，这个循环是怎么知道该停下来的呢？关键在 `while url:` ，和循环里找 `next_link` 的那两行：

- `while url:` 的意思是：只要 `url` 不是 `None` ，就接着取。
- 每取完一页，就去找 `a.next` 。找到了，`url` 就换成下一页的地址；找不到，`url` 就变成 `None` 。
- 到了第 6 页，找不到 `a.next` ，`url` 变成了 `None` ，循环自然就停了。

这种写法还有一个好处：不用事先知道一共有几页。网站以后加了新的一页，也照样能取到。

下面先做一道练习：从第 4 页开始，顺着「下一页」一直翻到最后。

# 二、看出网址规律，直接拼

顺着「下一页」翻，是第一种办法。再来看第二种办法：直接拼网址。仔细看看上一节输出里的那几个地址，会发现两点书店的网址很有规律：第 n 页就是 `https://learn-py.org/lab/bookstore/page/n/` 。既然这样，只要知道一共有几页，用 `for` 循环把每一页的地址拼出来就行了。

那一共有几页，怎么知道呢？其实页面上就写着：标题是「全部图书 · 第 1 页，共 6 页」。把它取出来：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get('https://learn-py.org/lab/bookstore/').text, 'html.parser')
heading = soup.select_one('main h2').get_text()
print(heading)
total = int(heading.split('共 ')[1].split(' 页')[0])
print(total)
```

输出的结果：

```
全部图书 · 第 1 页，共 6 页
6
```

`total` 那一行看着有点长，其实只做了一件事：用 `split()` 把「共 」和「 页」中间的数字切出来，再转成整数。具体来说，先按「共 」切开，取后面那一半，也就是「6 页」。再按「 页」切开，取前面那一半，就只剩下「6」了。

总页数有了，接下来就用它来拼地址：从第 1 页一直拼到第 `total` 页，把每一页都取一遍。下面的代码，先像上面那样读出 `total` ，再接一个循环：

<!-- skip-ci -->
```python
import time

import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get('https://learn-py.org/lab/bookstore/').text, 'html.parser')
heading = soup.select_one('main h2').get_text()
total = int(heading.split('共 ')[1].split(' 页')[0])

count = 0
for n in range(1, total + 1):
    url = f'https://learn-py.org/lab/bookstore/page/{n}/'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    count = count + len(soup.select('article.book-card'))
    time.sleep(0.2)
print(f'一共 {count} 本书')
```

输出的结果：

```
一共 120 本书
```

这里要留意 `range(1, total + 1)` 里的 `+ 1` 。`range()` 不包括右边那个数，要是写成 `range(1, total)` ，就只取到第 5 页，最后一页漏掉了。另外，这里没有直接写 6，而是用从页面上读出来的 `total` 。这样哪天书店多了一页，代码也不用改。

到这里，两种翻页的办法都会了，取到的也都是 120 本书。那么问题来了：两种办法，该怎么选呢？对比一下：

| 办法 | 好处 | 要留意的 |
|---|---|---|
| 顺着「下一页」 | 不用知道总页数，不用猜网址 | 「下一页」的选择器要找对，循环要有出口 |
| 直接拼网址 | 写起来简单，想取第几页就取第几页 | 要先看出规律、知道总页数；网址规则一变就失效 |

简单地说：网址的规律很明显，总页数也能拿到，就直接拼。规律看不出来，或者页数会变，就顺着「下一页」走。

下面先做一道练习，用直接拼网址的办法，数一数整个书店有几本书缺货。

# 三、出错了怎么办

两种翻页的办法，都要一口气发出好几个请求。请求一多，总会遇到出错的时候。那么，出了错该怎么办？是不是再试一次就行？先别急，出错其实分两种：

- **再试也没用的**：`404` 网页不存在、`403` 不让看。这是网址本身有问题，试一百遍也一样，应该放弃，记下来回头再查。
- **等一会儿可能就好的**：`503` 网站暂时忙不过来、`500` 网站内部出了点问题、`429` 你请求得太快了。等一等再试，常常就成功了。

所以重试的规矩是：**只对后一种重试，每次多等一会儿，最多试几次，试不成就放弃**。

规矩有了，怎么写成代码呢？这里有个小麻烦：网站出错，可不是想遇到就能遇到的。为了看清重试的过程，咱们先用一个假的 `get` 函数来代替真的请求，让它依次返回 503、503、200：

```python
import time


def fetch_status(get, url, retries=3):
    """请求 url，遇到 429 或 5 开头的状态码就等一会儿再试，最多试 retries 次。"""
    for attempt in range(1, retries + 1):
        status = get(url)
        print(f'第 {attempt} 次：{status}')
        if status == 200:
            return status
        if status != 429 and status < 500:
            return status
        time.sleep(0.2 * attempt)
    return status


answers = iter([503, 503, 200])


def fake_get(url):
    return next(answers)


print(fetch_status(fake_get, 'https://learn-py.org/lab/bookstore/'))
```

输出的结果：

```
第 1 次：503
第 2 次：503
第 3 次：200
200
```

前两次都是 503，等一等再试，第 3 次就成功了。这段代码里，有几处值得说一说：

- `get` 是一个参数，调用的时候，把 `fake_get` 这个函数传了进去。函数也能当参数传来传去，基础课第 15、16 章讲闭包和装饰器时会细说。
- `iter()` 把列表变成一个迭代器，每次调用 `next()` ，就取出下一个值。这是基础课第 7 章的内容。
- `time.sleep(0.2 * attempt)` ：第 1 次失败等 0.2 秒，第 2 次等 0.4 秒。越往后等得越久，好给网站喘口气。
- `for attempt in range(1, retries + 1)` 限定了最多试几次，所以不会没完没了地试下去。
- 状态码是 404 这类时，直接 `return` ，不再重试。

用假的函数把过程看清楚了，换成真的 `requests` ，思路也是一样的。下面分别取一个存在的第 3 页，和一个不存在的第 9 页：

<!-- skip-ci -->
```python
import time

import requests


def fetch(url, retries=3):
    """取回网页，成功返回响应；不能重试的错误或者试了几次都不行，返回 None。"""
    for attempt in range(1, retries + 1):
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response
        if response.status_code != 429 and response.status_code < 500:
            print(f'{url} 返回 {response.status_code}，不再重试')
            return None
        time.sleep(0.2 * attempt)
    print(f'{url} 试了 {retries} 次都没成功')
    return None


print(fetch('https://learn-py.org/lab/bookstore/page/3/').status_code)
print(fetch('https://learn-py.org/lab/bookstore/page/9/'))
```

输出的结果：

```
200
https://learn-py.org/lab/bookstore/page/9/ 返回 404，不再重试
None
```

第 3 页取到了，状态码是 200。第 9 页不存在，返回了 404，所以没有重试，直接放弃了。

和假的版本比，这里多了一个 `timeout=10` 。它的意思是：10 秒内网站还没回应，就别等了。为什么要加它呢？因为真实的网站偶尔会卡住不动，不设 `timeout` ，程序可能就一直傻等下去。超时以后，`requests` 会抛出一个异常。要接住它、换个办法处理，得用基础课第 19 章的 `try` / `except` 。

最后还要提醒一句。这里两处等待都只用了零点几秒，是因为网页里每次运行最多 5 秒。在自己电脑上抓真实的网站，重试前至少要等几秒，次数也别超过三五次。

下面先做一道练习，自己补全一个会重试的函数。

# 四、常见坑

翻页和重试都会了。不过这两样东西要是写错了，后果往往不只是报个错，而是没完没了地请求别人的网站。所以下面这几个坑，一定要留意。

## 1、翻页的循环没有出口

先看下面这段翻页的代码：

<!-- skip-ci -->
```python
url = 'https://learn-py.org/lab/bookstore/'
while url:
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    next_link = soup.select_one('a.nxt')
    url = urljoin(url, next_link['href'])
```

这段代码把选择器写错了一个字母：`a.next` 写成了 `a.nxt` 。这样一来，就找不到下一页了，`next_link` 是 `None` ，下一行就会报错。不过报错还算好的，至少程序停了下来。更糟的是另一种情况：要是网站的最后一页，「下一页」链接指向的是它自己，循环就永远停不下来。

所以，稳妥的做法是给循环再加一道保险，比如最多只翻 50 页：

<!-- skip-ci -->
```python
max_pages = 50
pages = 0
while url and pages < max_pages:
    pages = pages + 1
    ...
```

这样不管出了什么怪事，翻到第 50 页，循环也一定会停下来。为什么要这么小心呢？因为在网页里，死循环最多跑 5 秒就会被停掉。可是在自己电脑上，它会一直跑下去，一直请求别人的网站。

## 2、`time.sleep()` 放错了位置

下面这段代码，本来想每取一页就停 0.2 秒：

<!-- skip-ci -->
```python
for n in range(1, 7):
    requests.get(f'https://learn-py.org/lab/bookstore/page/{n}/')
time.sleep(0.2)
```

问题出在缩进上。`time.sleep()` 没有缩进，跑到了循环外面。结果 6 个请求一口气发完，最后才停了 0.2 秒，等于没停。所以，停顿一定要放在**循环里面**，每取完一页就停一次。

## 3、重试没有上限

再看一段重试的代码：

<!-- skip-ci -->
```python
while response.status_code != 200:
    response = requests.get(url)
```

网站要是一直出错，这个循环就会一直请求下去，而且一点间隔都没有。这正是网站最怕的那种爬虫。所以，重试一定要有次数上限，每次之间也要等一等。

## 4、不管什么错误都重试

第三节说过，出错分两种。`404` 是网页不存在，重试一百次也不会出来。`403` 是不让你看，一直重试，只会让网站更警惕。所以，只对 `429` 和 5 开头的状态码重试。其他的直接放弃，把网址记下来，回头再查原因。

# 五、自己查一次文档

这一章的代码里，每取一页都写了停 0.2 秒。可是，真的停了吗？要是想量一量两次请求之间到底隔了多久，该用什么呢？

`time.sleep()` 来自 Python 自带的 `time` 模块，这个模块里有好几个跟时间有关的函数，答案多半就在里面。去官方文档里找一找：[time 模块](https://docs.python.org/zh-cn/3/library/time.html) 。

先看咱们一直在用的 [time.sleep()](https://docs.python.org/zh-cn/3/library/time.html#time.sleep) 。点开会发现，它的第一句说明还是英文：Suspend execution of the calling thread for the given number of seconds. The argument may be a non-integer to indicate a more precise sleep time.

中文文档有的地方还没翻译完。遇到英文别慌，一句一句地看，意思是：暂停当前线程给定的秒数，参数可以不是整数，用来表示更精确的时间。所以 `time.sleep(0.2)` 写成小数，完全没问题。后面的中文说明还提醒了一句：实际暂停的时间，可能会比要求的长一点。

不过 `sleep()` 只管停，不管量。要量时间，得在文档里接着往下找，找到 [time.monotonic()](https://docs.python.org/zh-cn/3/library/time.html#time.monotonic) 。文档说，它返回一个单调时钟的值。「单调」是什么意思呢？就是这个时钟不能倒退。文档还说，它的返回值本身没有意义，只有两次调用之间的差值才是有效的。

只有差值有意义，这正合咱们的用处：每次请求完记下时间，和上一次的一减，就是两次请求之间的间隔。连取几页试一试：

<!-- skip-ci -->
```python
import time

import requests

last = None
for n in range(1, 4):
    requests.get(f'https://learn-py.org/lab/bookstore/page/{n}/')
    now = time.monotonic()
    if last is not None:
        print(f'和上一次请求隔了 {now - last:.1f} 秒')
    last = now
    time.sleep(0.2)
```

输出的结果：

```
和上一次请求隔了 0.2 秒
和上一次请求隔了 0.2 秒
```

量出来，两次请求之间确实隔了 0.2 秒左右。要是网速慢，请求本身也要花时间，量出来还会再多一点。

有的童鞋可能会问：「为什么不用 `time.time()` ？」因为 `time.time()` 是电脑上的「现在几点」，电脑校时的时候，它可能会往回调。而 `monotonic()` 只往前走，用来量间隔更可靠。文档里的这类细节，平时可能用不上。可要是真遇到「明明停了，怎么算出来是负数」这种怪事，就能想起来去查一查。

# 六、小结与回看

这一章，咱们的爬虫学会了自己翻页，把整个书店都取了下来，还学会了稳稳当当地请求。回头梳理一下，学到了这几件事：

- 顺着「下一页」翻：取回当前页，找 `a.next` ，用 `urljoin()` 补全，找不到就停。`while url:` 让循环在最后一页自然结束。
- 直接拼网址：先从页面上读出总页数，再用 `for` 循环拼出每一页的地址。
- 每取一页，就 `time.sleep()` 一下，停顿要放在循环里面。网页里只停零点几秒，在本地抓真实的网站，至少停 1 秒。
- 出错分两种：`404` 、`403` 这类不重试。`429` 和 5 开头的，等一会儿再试，每次多等一些，而且有次数上限。
- `requests.get(url, timeout=10)` 不让程序无限地等下去。
- 循环要有出口，最好再加一道「最多翻几页」的保险。
- 量时间间隔用 `time.monotonic()` ，只有两次调用的差值才有意义。

哪里卡住了，就回去看一看：

- `while` 、`for` 、`break` ：第 5 章
- 迭代器和 `next()` ：第 7 章
- `parse_list()` 和 `urljoin()` ：爬虫课第 5 章

现在，整个书店都能取下来了。不过，各位童鞋有没有在开发者工具里留意过：网页上的数据，有时候并不是写在 HTML 里的，而是网页打开以后，再从另一个地址要过来的。这样的数据，光取 HTML 是取不到的。下一章，咱们就去找这些藏在背后的数据接口。
