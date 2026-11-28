# 爬虫第 9 章：综合项目：爬完整个书店

# 前言

各位童鞋学到这里，爬虫的四步已经全部学完了：获取、解析、提取、存储。不过前面八章，是一章学一样本事，每一样都是单独练的。这一章不学新东西，而是把这八章的本事串起来，写一个完整的书店爬虫。

那么，从哪儿下手呢？各位童鞋还记得实战 2 吗？写记账本之前，咱们没有急着写代码，而是先用大白话把要做的事拆开，再给每一步找一个学过的零件。写爬虫也是一样，而且更要这样做。因为爬虫要和别人的网站打交道，要是一上来就写一大坨代码，出了问题，连是哪一步错的都不知道。

所以这一章的节奏是这样的：先拆需求，再一个函数一个函数地写，每写完一个，就单独试一试，最后才把它们拼起来。写完以后，还要检查一下数据对不对。这一步，很多人都会忘。

这一章做出来的 `books.csv` ，就是数据分析课要用的那份数据。到时候你会亲眼看到：自己抓下来的文件，和数据分析课那边准备好的，一模一样。

**学这一章之前**，需要先学完爬虫课第 1～8 章，尤其是 [第 5 章](05-extract-list.md) 的 `parse_list()` 、[第 6 章](06-pagination-and-politeness.md) 的重试、[第 7 章](07-json-api.md) 的接口和 [第 8 章](08-save-data.md) 的 csv，这几样这一章都会用到。

# 目录

这一章会做：

- 一、先拆需求——要什么数据，从哪儿取，分几步
- 二、可靠地取——`fetch()`
- 三、取全部图书——`crawl_api()`
- 四、和网页对一对——数据校验
- 五、存成 csv——`save_csv()`
- 六、完整的爬虫——把函数拼起来
- 七、常见坑
- 八、自己查一次文档——只存一部分字段
- 九、小结与回看

做完这一章，你会有一个结构清楚、取得稳、存得对的书店爬虫，和一份可以交给数据分析课的 `books.csv` 。

# 一、先拆需求

动手写代码之前，先用一句大白话说清楚，这个爬虫到底要做什么：

**把两点书店的 120 本书，每本的编号、书名、作者、分类、价格、评分、评价数、库存、页数和出版年份，存成一个 csv 文件。**

要做的事说清楚了，下一个问题是：数据从哪儿取？前几章其实试过两条路，放在一起比一比：

| 办法 | 请求次数 | 数据 |
|---|---|---|
| 网页：6 个列表页，再加 120 个详情页 | 126 次 | 要用选择器一个个取，再清洗 |
| 接口：`page-1.json` 到 `page-6.json` | 6 次 | 全部字段都在，已经是数字和 `None` |

这么一比，差别就很明显了。第 7 章说过，有接口就先用接口：请求次数少，对网站友好，取到的数据也干净。所以这个爬虫，主力用接口。

不过，这里还有一个疑问：接口的数据，和网页上显示的一致吗？会不会漏了什么？光靠猜是不行的，这就要做**校验**：挑一页网页抓下来，和接口的数据对一对。

从哪儿取想好了，接下来把要做的事拆成几个函数。每个函数只做一件事，而且大多能在前面的章节里找到来历：

| 函数 | 做什么 | 用到哪一章 |
|---|---|---|
| `fetch(url)` | 取回一个网址，出错就重试，不行就返回 `None` | 第 6 章 |
| `crawl_api()` | 顺着 `next` 取完全部图书，返回列表 | 第 7 章 |
| `parse_list(html, url)` | 从列表页的网页里取出每本书 | 第 5 章 |
| `check(books, page_books)` | 拿网页上的书和接口的书对一对 | 新写的 |
| `save_csv(books, path)` | 存成 csv | 第 8 章 |

再把这几个函数按先后顺序排一排，画成流程：

```text
① crawl_api()：从 page-1.json 开始，顺着 next 取完 6 页
② 取第 1 页的网页，parse_list() 取出 20 本
③ check()：对一对书名和价格，不一致就停下来查
④ save_csv()：存成 csv
```

整个爬虫，就是这四步。下面就一个函数一个函数地写，每写完一个，就单独试一个。先从 `fetch(url)` 写起，因为后面所有的请求，都要经过它。

# 二、可靠地取

为什么要先写 `fetch()` 呢？因为这个爬虫里所有的请求，都要经过它。只要它够可靠，后面的函数就不用再操心「请求出错了怎么办」。

它要做到这么几件事：

- 请求成功了，就返回响应。
- 遇到 `404` 这类错误，重试也没有用，就不再重试。
- 遇到 `429` 和 5 开头的状态码，等一会儿可能就好了，所以等一会儿再试。
- 每次请求之后，都停一停。

这其实就是第 6 章的写法，只是多加了一个统一的停顿：

<!-- skip-ci -->
```python
import time

import requests


def fetch(url, retries=3, pause=0.2):
    """取回 url，成功返回响应；不能重试的错误或者试了几次都不行，返回 None。"""
    for attempt in range(1, retries + 1):
        response = requests.get(url, timeout=10)
        time.sleep(pause)
        if response.status_code == 200:
            return response
        if response.status_code != 429 and response.status_code < 500:
            print(f'跳过 {url}：{response.status_code}')
            return None
        time.sleep(pause * attempt)
    print(f'放弃 {url}：试了 {retries} 次')
    return None


print(fetch('https://learn-py.org/lab/bookstore/api/page-1.json').status_code)
print(fetch('https://learn-py.org/lab/bookstore/api/page-9.json'))
```

输出的结果：

```
200
跳过 https://learn-py.org/lab/bookstore/api/page-9.json：404
None
```

先看输出。第一个网址取到了，打印出状态码 `200` 。第二个网址 `page-9.json` ，网站返回的是 `404` ，`fetch()` 没有重试，打印一行「跳过」的提示，然后返回 `None` 。

这段代码里，还有一处值得说一说，就是 `time.sleep(pause)` 放的位置。它放在 `fetch()` 里面，以后不管在哪儿请求，都会自动停一停，不会忘。`pause` 写成了参数，停多久可以随时调：在网页里用 0.2 秒；在自己电脑上抓真实的网站，就调成 1 秒以上。

`fetch()` 写好了，也试过了。下面先做一道练习，自己动手写一遍 `fetch()` 。下一节，就用它去取全部的图书。

# 三、取全部图书

有了可靠的 `fetch()` ，取全部图书就好办了。接口的每一页数据里，都有一个 `next` ，指向下一页。所以 `crawl_api()` 要做的，就是从第一页开始，顺着 `next` 一页一页地取，直到没有下一页为止。每一页的请求，都交给上一节的 `fetch()` ：

<!-- skip-ci -->
```python
import time
from urllib.parse import urljoin

import requests


def fetch(url, retries=3, pause=0.2):
    for attempt in range(1, retries + 1):
        response = requests.get(url, timeout=10)
        time.sleep(pause)
        if response.status_code == 200:
            return response
        if response.status_code != 429 and response.status_code < 500:
            return None
        time.sleep(pause * attempt)
    return None


def crawl_api(start='https://learn-py.org/lab/bookstore/api/page-1.json', max_pages=50):
    """从第一页接口开始，顺着 next 取完全部图书。"""
    books = []
    url = start
    pages = 0
    while url and pages < max_pages:
        response = fetch(url)
        if response is None:
            break
        data = response.json()
        books.extend(data['books'])
        url = urljoin(url, data['next']) if data['next'] else None
        pages = pages + 1
    return books


books = crawl_api()
print(len(books))
print(books[-1])
```

输出的结果：

```
120
{'id': 120, 'title': '蒲公英的冒险', 'author': '白清和', 'category': '童书', 'price': 37.7, 'rating': 4, 'reviews': 1, 'stock': 28, 'pages': 426, 'year': 2021}
```

一共取到 120 本，最后一本是编号 120 的《蒲公英的冒险》，全部取完了。

这个 `crawl_api()` 和第 7 章的写法很像，不过多了两道保险：

- `fetch()` 返回 `None` ，说明这一页没取到，就停下来，不再往下取。
- `max_pages` 限定最多取 50 页。万一接口的 `next` 出了问题，程序也不会没完没了地取下去。

图书是都取到手了。可是，接口给的这些数据，真的靠得住吗？下一节就来验证一下。

# 四、和网页对一对

第一节留下了一个疑问：接口给的数据，和网页上显示的是同一回事吗？

要回答这个问题，不用把列表页全都抓一遍，抽查一页就够了。办法是这样的：抓第 1 页的网页，用第 5 章的 `parse_list()` 把书取出来，再和接口的前 20 本逐本比较。比较这件事，交给新写的 `check()` 来做：

<!-- skip-ci -->
```python
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch(url, retries=3, pause=0.2):
    for attempt in range(1, retries + 1):
        response = requests.get(url, timeout=10)
        time.sleep(pause)
        if response.status_code == 200:
            return response
        if response.status_code != 429 and response.status_code < 500:
            return None
        time.sleep(pause * attempt)
    return None


def parse_list(html, page_url):
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    for card in soup.select('article.book-card'):
        link = card.select_one('.title a')
        books.append({
            'id': int(card['data-id']),
            'title': link.get_text(strip=True),
            'url': urljoin(page_url, link['href']),
            'price': float(card.select_one('.price').get_text(strip=True).replace('¥', '')),
        })
    return books


def check(api_books, page_books):
    """拿网页上取到的书，和接口里同编号的书比较书名和价格，返回对不上的地方。"""
    by_id = {book['id']: book for book in api_books}
    problems = []
    for book in page_books:
        other = by_id.get(book['id'])
        if other is None:
            problems.append(f"{book['id']}：接口里没有这本书")
        elif other['title'] != book['title'] or other['price'] != book['price']:
            problems.append(f"{book['id']}：网页 {book['title']} {book['price']}，接口 {other['title']} {other['price']}")
    return problems


api_books = fetch('https://learn-py.org/lab/bookstore/api/page-1.json').json()['books']
page_url = 'https://learn-py.org/lab/bookstore/'
page_books = parse_list(fetch(page_url).text, page_url)
problems = check(api_books, page_books)
print(f'比较了 {len(page_books)} 本，对不上的 {len(problems)} 处')
```

输出的结果：

```
比较了 20 本，对不上的 0 处
```

20 本书，一处对不上的都没有。这说明接口里的书名和价格，和网页上显示的一致，可以放心用。

`check()` 是这一章新写的函数，里面用了两个小技巧，咱们拆开来看：

- `{book['id']: book for book in api_books}` 叫作**字典生成式**，写法和列表生成式一样，只是造出来的是一个「编号 → 书」的字典。有了它，按编号找书时，就不用一本一本地翻了。
- `by_id.get(编号)` 在字典里找不到这个编号时，会返回 `None` 。正好可以用它来发现那种「网页上有、接口里没有」的书。

这一回全都对得上。那要是对不上呢？比如网页上显示的是打折后的价格，接口里却是原价。这时候就要停下来想一想：数据分析要的是哪一个价格？想清楚了，再存。说到底，校验不是为了走个过场，而是在把数据交出去之前，先让自己信得过它。

数据校验过了，下一节就把它存成 csv。在那之前，先做一道练习，自己动手检查一下取回来的数据。

# 五、存成 csv

数据取到了，也校验过了，就剩最后一步：用 `save_csv()` 把书存进 csv 文件。

存的时候有一点要注意：列的顺序要固定下来，和数据分析课准备的 `books.csv` 保持一样。所以代码开头先用 `COLUMNS` 把列名按顺序排好，再交给 `DictWriter` ：

<!-- skip-ci -->
```python
import csv
import time
from urllib.parse import urljoin

import requests

COLUMNS = ['id', 'title', 'author', 'category', 'price', 'rating', 'reviews', 'stock', 'pages', 'year']


def crawl_api():
    books = []
    url = 'https://learn-py.org/lab/bookstore/api/page-1.json'
    while url:
        data = requests.get(url).json()
        books.extend(data['books'])
        url = urljoin(url, data['next']) if data['next'] else None
        time.sleep(0.2)
    return books


def save_csv(books, path):
    """按 COLUMNS 的顺序把书存成 csv，返回存了几本。"""
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(books)
    return len(books)


print(save_csv(crawl_api(), 'my_bookstore.csv'))
with open('my_bookstore.csv', encoding='utf-8') as f:
    mine = f.read()
with open('books.csv', encoding='utf-8') as f:
    prepared = f.read()
print(mine == prepared)
print(mine.splitlines()[0])
```

输出的结果：

```
120
True
id,title,author,category,price,rating,reviews,stock,pages,year
```

先看输出的第二行，是 `True` 。也就是说，自己抓下来的 `my_bookstore.csv` ，和数据分析课准备的 `books.csv` ，**一个字符都不差**。

这里的 `books.csv` 是从哪儿来的呢？在网页里运行时，它由网站提前放好了；在自己电脑上，可以从 [练习靶场](https://learn-py.org/lab/) 下载，也可以直接用这一章抓下来的文件。

那为什么 `DictWriter` 能直接把这些书写进去？因为接口给的每一本书，正好就是这 10 个字段，一个也不多。要是字典里多出了别的字段，它就会报错。遇到这种情况该怎么办，第八节查文档的时候再说。

到这里，需要的几个函数都写好了，也都单独试过了。下一节，就把它们拼成一个完整的爬虫。

# 六、完整的爬虫

前面几节写好的函数，现在把它们拼起来，再加一个 `main()` 按顺序调用它们，就是完整的书店爬虫。

代码有点长，先说说最后两行。它们用的是基础课第 9 章讲过的 `if __name__ == '__main__':` 。为什么要这么写呢？因为这样一来，这个文件被直接运行时，才会开始抓；被别的文件 `import` 的时候，只提供这些函数，不会一导入就去请求网站。

<!-- skip-ci -->
```python
import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START = 'https://learn-py.org/lab/bookstore/api/page-1.json'
CHECK_PAGE = 'https://learn-py.org/lab/bookstore/'
COLUMNS = ['id', 'title', 'author', 'category', 'price', 'rating', 'reviews', 'stock', 'pages', 'year']


def fetch(url, retries=3, pause=0.2):
    """取回 url，成功返回响应；不能重试的错误或者试了几次都不行，返回 None。"""
    for attempt in range(1, retries + 1):
        response = requests.get(url, timeout=10)
        time.sleep(pause)
        if response.status_code == 200:
            return response
        if response.status_code != 429 and response.status_code < 500:
            return None
        time.sleep(pause * attempt)
    return None


def crawl_api(start=START, max_pages=50):
    """顺着 next 取完全部图书。"""
    books, url, pages = [], start, 0
    while url and pages < max_pages:
        response = fetch(url)
        if response is None:
            break
        data = response.json()
        books.extend(data['books'])
        url = urljoin(url, data['next']) if data['next'] else None
        pages = pages + 1
    return books


def parse_list(html, page_url):
    """从列表页的网页里取出每本书的编号、书名和价格。"""
    soup = BeautifulSoup(html, 'html.parser')
    return [{
        'id': int(card['data-id']),
        'title': card.select_one('.title a').get_text(strip=True),
        'price': float(card.select_one('.price').get_text(strip=True).replace('¥', '')),
    } for card in soup.select('article.book-card')]


def check(api_books, page_books):
    """比较网页和接口的书名、价格，返回对不上的编号。"""
    by_id = {book['id']: book for book in api_books}
    return [book['id'] for book in page_books
            if by_id.get(book['id'], {}).get('title') != book['title']
            or by_id.get(book['id'], {}).get('price') != book['price']]


def save_csv(books, path):
    """按 COLUMNS 的顺序存成 csv。"""
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(books)


def main():
    books = crawl_api()
    print(f'接口：取到 {len(books)} 本')
    wrong = check(books, parse_list(fetch(CHECK_PAGE).text, CHECK_PAGE))
    if wrong:
        print(f'校验：这些编号对不上 {wrong}，先不存')
        return
    print('校验：第 1 页 20 本全部对得上')
    save_csv(books, 'my_bookstore.csv')
    print('已存成 my_bookstore.csv')


if __name__ == '__main__':
    main()
```

输出的结果：

```
接口：取到 120 本
校验：第 1 页 20 本全部对得上
已存成 my_bookstore.csv
```

整个程序六十来行，每个函数都不长，名字也说清了它是干什么的。这样写有什么好处呢？哪一步出了问题，就去看哪个函数。想换个网站抓，主要改的也只是 `parse_list()` 里的选择器，还有开头的那几个网址。

还要说一句：这段代码在自己电脑上，也能原样运行，前提是装好了 `requests` 和 `beautifulsoup4` 。怎么在自己电脑上把这些准备好，下一章就讲。

# 七、常见坑

爬虫写完了，也能跑通了，是不是就万事大吉了？还不够。下面这几个坑，写第一个完整爬虫的时候特别容易踩到。这一章的不少做法，其实就是为了避开它们。

## 1、一上来就抓全部

还没确认选择器对不对，就让爬虫一口气跑完几百页。结果到最后才发现，取下来的全是空的，白白请求了别人几百次。

所以写爬虫的顺序应该是这样的：先抓**一页**，打印出来，看看对不对；再抓**几页**，看看翻页对不对；最后，才放开抓全部。这一章的每一节，都是先单独试一个函数，再往下走，也是这个道理。

## 2、抓到一半出错，前面的全丢了

<!-- skip-ci -->
```python
books = []
for n in range(1, 101):
    books.extend(parse_list(fetch(url_of(n)).text, url_of(n)))
save_csv(books, 'books.csv')
```

这段代码把所有数据都攒在内存里，到最后才存。要是抓到第 80 页的时候，网络断了，或者程序报错了，会怎么样呢？前面 79 页的数据，一页都没存下来，全都没了。

所以数据多的时候，要抓一页就存一页。比如用 csv 的 `'a'` 模式往文件后面追加，或者像第 8 章那样，存进 sqlite3。这样程序重新跑的时候，还能先看看哪些已经存过了，接着往下抓。

## 3、存之前不检查

数据一存下来，就交出去了。要是里面有问题，往往要等到分析的时候才会发现。所以存之前，至少要检查这几样：

- **数量**对不对：书店有 120 本，取到的是不是 120 本。
- 有没有**重复**：编号有没有重复出现。
- **空值**多不多：哪些字段是空的，是本来就没有，还是没取到。

这几样怎么查呢？拿一个小例子试一试。下面这几本书是故意编的，里面藏了重复和空值：

```python
books = [{'id': 1, 'rating': 4.7}, {'id': 2, 'rating': None}, {'id': 2, 'rating': None}]
ids = [book['id'] for book in books]
print(len(books), len(set(ids)), sum(1 for book in books if book['rating'] is None))
```

输出的结果：

```
3 2 2
```

输出的三个数，依次是书的本数、不同编号的个数和没有评分的本数。`set()` 会去掉重复的元素，基础课第 4 章讲过。3 本书只有 2 个不同的编号，说明有重复；还有 2 本书没有评分。

## 4、代码里写死了网址和等待时间

网址、停顿的秒数、最多取几页，这些以后可能要改的值，不要散落在代码里，而是集中写在文件开头，起一个大写的名字，就像上一节的 `START` 、`COLUMNS` 那样。这样要改的时候，就不用在代码里到处找了。

# 八、自己查一次文档

第五节留下了一个问题：字典里要是多出了别的字段，`DictWriter` 会报错。这种情况什么时候会碰上呢？

比如说，数据分析只要书名、分类和价格这三列，可接口给的每本书，却有 10 个字段。直接交给 `DictWriter` ，会怎样？拿一本书来试试：

<!-- skip-ci -->
```python
import csv

books = [{'id': 1, 'title': '轻松玩转自动化', 'category': '编程', 'price': 104.4, 'stock': 55}]
with open('short.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'category', 'price'])
    writer.writeheader()
    writer.writerows(books)
```

报错信息的最后一行是：

```
ValueError: dict contains fields not in fieldnames: 'id', 'stock'
```

意思是：字典里有 `fieldnames` 没列出来的键，比如这里的 `id` 和 `stock` ，它就不干了。那怎么办？难道要先把每个字典都改一遍？

先别急着自己动手改，去查查文档，看看 `DictWriter` 有没有现成的办法：[csv.DictWriter](https://docs.python.org/zh-cn/3/library/csv.html#csv.DictWriter) 。

打开以后，先看它的签名：`DictWriter(f, fieldnames, restval='', extrasaction='raise', ...)` 。说明里讲了其中两个参数：

- `extrasaction` ：管的是字典里有 `fieldnames` 找不到的键时，该怎么办。默认是 `'raise'` ，也就是引发 `ValueError` ，刚才的报错就是这么来的；设成 `'ignore'` ，多出来的值就会被忽略掉。
- `restval` ：管的是反过来的情况。字典里**缺**了 `fieldnames` 里的某个键时，就写进这个值，默认是空字符串。

`extrasaction` 正是咱们要的。加上 `extrasaction='ignore'` ，再试一次：

```python
import csv

books = [{'id': 1, 'title': '轻松玩转自动化', 'category': '编程', 'price': 104.4, 'stock': 55}]
with open('short.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'category', 'price'], extrasaction='ignore')
    writer.writeheader()
    writer.writerows(books)

with open('short.csv', encoding='utf-8') as f:
    print(f.read())
```

输出的结果：

```
title,category,price
轻松玩转自动化,编程,104.4

```

这回没有报错。多出来的 `id` 和 `stock` 被忽略了，文件里只存了要的那三列。

最后再想一想：为什么默认是 `'raise'` ，而不是 `'ignore'` 呢？其实这个设计挺贴心。多数时候，字典里多出字段，是因为写错了键名，这时候报个错，正好能提醒你。只有在确定「就是只要一部分」的时候，才特意写上 `'ignore'` 。所以读文档的时候，留意一下参数的**默认值**，往往能看出设计者的用意。

# 九、小结与回看

这一章，咱们从拆需求开始，一个函数一个函数地写，最后拼成了一个完整的爬虫。回头梳理一下，学到了这几件事：

- 先拆需求：要什么数据、从哪儿取、分成几个函数。有接口，就先用接口。
- 每个函数只做一件事：`fetch()` 负责可靠地取，`crawl_api()` 取全部，`parse_list()` 解析网页，`check()` 校验，`save_csv()` 存储，最后由 `main()` 把它们串起来。
- 每写一个函数，就单独试一个。抓的时候也一样：先抓一页，再抓几页，最后才抓全部。
- 存之前要校验：网页和接口对一对，数量、重复、空值查一查。
- 数据多的时候，抓一页就存一页，别攒到最后才存。
- 网址、停顿、页数上限这些设置，集中写在文件开头。
- `if __name__ == '__main__':` 让文件既能直接运行，又能被别的文件导入。
- `DictWriter` 的 `extrasaction='ignore'` ，可以只存一部分字段。

哪里卡住了，就回去看一看：

- 拆需求、画流程：实战 2 的「二、先别写代码，把需求拆开」
- 拆函数：实战 4
- `__name__` ：第 9 章「三、主模块和非主模块」
- 各个函数的来历：爬虫课第 5～8 章

到这里，在网页里能学的爬虫本事，就都学完了。你抓下来的 `books.csv` ，会在数据分析课的最后一个项目里派上用场。

不过，真实世界的网站，可不都像两点书店这么规矩。所以接下来的三章，咱们回到自己电脑上：先把 Python 和这几个包装好，去抓公开的爬虫练习站；再学会登录以后怎么抓；最后看看页面要靠 JavaScript 才能显示的时候，还有想抓得更快的时候，该怎么办。
