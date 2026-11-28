# 爬虫第 5 章：从列表页提取多条数据

# 前言

各位童鞋在上一章学会了用 BeautifulSoup，从网页里取出一个书名、一个价格。可是一个列表页上有 20 本书，咱们真正想要的，是**每一本**书的书名、作者、价格、评分和库存，整整齐齐地排成一张表。

这一章就来做这件事。要取的东西听上去很多，其实套路很简单，一句话就能说完：**先找到每本书的外壳，再在每个外壳里面取各个字段**。

不过，光把字段取出来还不够，因为取出来的都还只是文字：「¥104.40」不能直接加减，「★★★★☆」也没法算平均分。所以还要多做一步，把文字**清洗**成真正的数据：价格变成浮点数，星星变成数字，「有货」「缺货」变成 `True` 和 `False` 。

那么，最后做出来的东西是什么样子呢？各位童鞋还记得实战 2 的记账本吗？每一笔账是一个字典，很多笔账装进一个列表。这一章做出来的，正是同一个样子：每本书是一个字典，一页书是一个列表。

**学这一章之前**，需要先学完 [爬虫课第 4 章](04-beautifulsoup-basics.md) ，会用 `select()` 、`select_one()` 、`get_text()` 。另外，还要熟悉 [实战 2](../01-basics/05b-practice-2-ledger-v1.md) 里「列表里装字典」的写法。

# 目录

这一章会学到：

- 一、先找到每本书的外壳——在外壳里面取字段
- 二、把文字变成数据——价格、星级和库存
- 三、补全链接——`urljoin()`
- 四、包成一个函数——`parse_list()`
- 五、常见坑
- 六、自己查一次文档——`urljoin()` 是怎么拼网址的
- 七、小结与回看

学完这一章，你能把一整页书变成一个整整齐齐的列表，每本书的数据都能直接拿来计算。

# 一、先找到每本书的外壳

前言里说了，套路是先找外壳。那么，一本书的外壳在哪儿呢？在书店的网页里，一本书的所有信息，都装在一个 `<article class="book-card">` 里，这就是它的外壳。所以第一步，先把这一页上的 20 个外壳都找出来：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
cards = soup.select('article.book-card')
print(len(cards))
```

输出的结果：

```
20
```

正好 20 个，一本书一个外壳。外壳找齐了，接下来对每个外壳，**在它里面**取出书名、作者、价格、评分和库存，拼成一个字典，再放进列表 `books` 里：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
books = []
for card in soup.select('article.book-card'):
    books.append({
        'title': card.select_one('.title').get_text(strip=True),
        'author': card.select_one('.author').get_text(strip=True),
        'price': card.select_one('.price').get_text(strip=True),
        'rating': card.select_one('.rating').get_text(strip=True),
        'stock': card.select_one('.stock').get_text(strip=True),
    })
print(len(books))
print(books[0])
print(books[2])
```

输出的结果：

```
20
{'title': '轻松玩转自动化', 'author': '陈星河', 'price': '¥104.40', 'rating': '★★★★★', 'stock': '有货'}
{'title': '早起养花', 'author': '林子墨', 'price': '¥56.20', 'rating': '暂无评分', 'stock': '有货'}
```

这段代码里，最要紧的是循环里的 `card.select_one()` ，注意不是 `soup.select_one()` 。为什么呢？因为 `card` 是一本书的外壳，在它里面找，找到的一定是这本书自己的书名和价格，不会和别的书搞混。

有的童鞋可能会想：何必这么麻烦？分别 `select('.title')` 、`select('.price')` ，各拿到一个列表，再一个一个对上号，不也行吗？问题在于，万一哪本书少了一个字段，两个列表的长度就不一样了。从那本书开始，后面的书名和价格就全都错了位。而按外壳来取，一本书的字段永远在一起，就不会出这种事。

字段都取到了。可仔细看看输出，取出来的值全是字符串，还不能直接拿来算，下一节就来解决这个问题。

# 二、把文字变成数据

上一节拿到的全是字符串。比如价格 `'¥104.40'` ，前面还带着一个 `¥` ，既不能直接比大小，也没法算平均。要清洗的有三样：价格、评分和库存，咱们一样一样来。

先说**价格**：去掉 `¥` ，再转成浮点数。

```python
text = '¥104.40'
price = float(text.replace('¥', ''))
print(price, price * 2)
```

输出的结果：

```
104.4 208.8
```

转换以后，`price` 就是一个真正的数了，乘以 2 也没问题。

再看**评分**。评分是用星星画出来的，数一数有几颗实心的星星，就知道是几星。可有的书还没人评过，网页上写的是「暂无评分」，这样的书就用 `None` 来表示「没有这个值」：

```python
def parse_rating(text):
    if text == '暂无评分':
        return None
    return text.count('★')


print(parse_rating('★★★★☆'))
print(parse_rating('暂无评分'))
```

输出的结果：

```
4
None
```

看到这里，很多童鞋会问：「没有评分，记成 `0` 不就行了，为什么非要用 `None` ？」因为 `0` 星本身也是一个评分，而「没人评过」完全是另一回事。要是记成 `0` ，算平均分的时候，就会把没人评过的书也算进去，平均分就被白白拉低了。

最后是**库存**。网页上写的是「有货」或者「缺货」，咱们把「有货」变成 `True` ，「缺货」变成 `False` ：

```python
for text in ['有货', '缺货']:
    in_stock = text == '有货'
    print(text, in_stock)
```

输出的结果：

```
有货 True
缺货 False
```

这里有个小窍门。`text == '有货'` 本身就是一个比较，比较的结果就是 `True` 或 `False` ，直接存起来就行，不用再写 `if` 去判断。

三样清洗都会了，现在把它们合到一起，整理第一页。整理好以后，顺手算一算平均价格、平均评分和缺货的本数，看看数据是不是真的能算了：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup


def parse_rating(text):
    if text == '暂无评分':
        return None
    return text.count('★')


html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
books = []
for card in soup.select('article.book-card'):
    books.append({
        'title': card.select_one('.title').get_text(strip=True),
        'price': float(card.select_one('.price').get_text(strip=True).replace('¥', '')),
        'rating': parse_rating(card.select_one('.rating').get_text(strip=True)),
        'in_stock': card.select_one('.stock').get_text(strip=True) == '有货',
    })

rated = [book['rating'] for book in books if book['rating'] is not None]
print(books[2])
print(f'平均价格 {sum(book["price"] for book in books) / len(books):.2f} 元')
print(f'有评分的 {len(rated)} 本，平均 {sum(rated) / len(rated):.1f} 星')
print(f'缺货 {sum(1 for book in books if not book["in_stock"])} 本')
```

输出的结果：

```
{'title': '早起养花', 'price': 56.2, 'rating': None, 'in_stock': True}
平均价格 61.27 元
有评分的 19 本，平均 3.5 星
缺货 1 本
```

清洗之后，数据就能拿来算了：这一页书的平均价格是 61.27 元，有评分的 19 本平均 3.5 星，缺货的有 1 本。

代码里 `rated` 那一行，用的是 `[... for book in books if ...]` 的写法。这是基础课第 7 章学过的列表生成式，后面加上 `if` ，表示只要满足条件的，在这里就是只要有评分的书。正因为没有评分的书记的是 `None` ，才能这样把它们挑出去，平均分也就不会被拉低。

取字段和清洗都会了，先做两道练习，把这两步练熟。做完再回来，看看书名上的链接该怎么处理。

# 三、补全链接

每本书的书名上都有一个链接，前面取字段时还没管它。来看看它的 `href` ：写的是 `https://learn-py.org/lab/bookstore/books/1/` ，前面并没有 `https://learn-py.org` 。像这样只写了路径、没写网站地址的链接，叫**相对链接**。

浏览器会根据当前网页的地址，自动把它补全，可 `requests.get()` 不会。所以拿到相对链接，得先自己把它补成完整的地址。

补全链接，可以用 `urllib.parse` 里的 `urljoin()` 。先拿两个链接试一试：

```python
from urllib.parse import urljoin

page = 'https://learn-py.org/lab/bookstore/page/2/'
print(urljoin(page, 'https://learn-py.org/lab/bookstore/books/21/'))
print(urljoin(page, '../3/'))
```

输出的结果：

```
https://learn-py.org/lab/bookstore/books/21/
https://learn-py.org/lab/bookstore/page/3/
```

它的用法是 `urljoin(当前网页的地址, 链接)` 。对照输出看，两种链接的补法不一样：

- 链接以 `/` 开头，就接在域名后面。
- 链接以 `../` 开头，就像在文件夹里「往上走一层」，再接上去。比如 `../3/` ，从 `page/2/` 往上走一层，到了 `page/` ，再接上 `3/` ，就成了 `page/3/` 。

好在这些情况都不用自己去判断，统统交给 `urljoin()` 就行。下面把它用到书店的列表页上，补全前 3 本书的链接：

<!-- skip-ci -->
```python
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

page = 'https://learn-py.org/lab/bookstore/'
soup = BeautifulSoup(requests.get(page).text, 'html.parser')
for link in soup.select('article.book-card .title a')[:3]:
    print(urljoin(page, link['href']))
```

输出的结果：

```
https://learn-py.org/lab/bookstore/books/1/
https://learn-py.org/lab/bookstore/books/2/
https://learn-py.org/lab/bookstore/books/3/
```

每本书的详情页地址就都齐了。有了完整的地址，以后就能顺着链接，去取每一本书的详情页。

到这里，找外壳、取字段、清洗、补全链接，取一页书要做的事都学齐了。可这些代码还散落在好几段里，难道每取一页，都要重新抄一遍吗？下一节就把它们收拾到一起。

# 四、包成一个函数

从一页 HTML 里取出全部书的这段代码，后面每一页都要用。那该怎么办呢？实战 4 说过，要反复用的东西，就包成函数。

下面这个 `parse_list()` ，把前面三节学的都装了进去：找外壳、取字段、清洗，再补全链接。拿第 2 页来试一试：

<!-- skip-ci -->
```python
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_rating(text):
    if text == '暂无评分':
        return None
    return text.count('★')


def parse_list(html, page_url):
    """从列表页的 HTML 里取出每本书，返回一个列表，每本书是一个字典。"""
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    for card in soup.select('article.book-card'):
        link = card.select_one('.title a')
        books.append({
            'id': int(card['data-id']),
            'title': link.get_text(strip=True),
            'url': urljoin(page_url, link['href']),
            'author': card.select_one('.author').get_text(strip=True),
            'category': card.select_one('.category').get_text(strip=True),
            'price': float(card.select_one('.price').get_text(strip=True).replace('¥', '')),
            'rating': parse_rating(card.select_one('.rating').get_text(strip=True)),
            'in_stock': card.select_one('.stock').get_text(strip=True) == '有货',
        })
    return books


url = 'https://learn-py.org/lab/bookstore/page/2/'
books = parse_list(requests.get(url).text, url)
print(len(books))
print(books[0])
```

输出的结果：

```
20
{'id': 21, 'title': '小熊的梦', 'url': 'https://learn-py.org/lab/bookstore/books/21/', 'author': '陈若溪', 'category': '童书', 'price': 47.5, 'rating': 4, 'in_stock': True}
```

第 2 页的 20 本书都取出来了。注意这个函数是怎么分工的：`parse_list()` 只管从 HTML 里取数据，至于 HTML 是怎么来的，它不管。

这样分开有什么好处呢？好处是，可以直接拿一段自己写好的 HTML 来试它，不用每次都去请求网页：

```python
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_rating(text):
    if text == '暂无评分':
        return None
    return text.count('★')


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
            'rating': parse_rating(card.select_one('.rating').get_text(strip=True)),
        })
    return books


sample = """
<article class="book-card" data-id="7">
  <h3 class="title"><a href="https://learn-py.org/lab/bookstore/books/7/">测试用的书</a></h3>
  <p class="price">¥10.00</p>
  <p class="rating">暂无评分</p>
</article>
"""
print(parse_list(sample, 'https://learn-py.org/lab/bookstore/'))
```

输出的结果：

```
[{'id': 7, 'title': '测试用的书', 'url': 'https://learn-py.org/lab/bookstore/books/7/', 'price': 10.0, 'rating': None}]
```

这个小例子里的 HTML 只写了几个字段，所以函数也跟着删掉了 `author` 那几行。可以看到，用一小段 HTML 就把函数试完了，连网都不用联。

实战 4 里讲过「拆出来的函数能单独试」，这个好处在写爬虫时特别管用。为什么呢？因为网站是会改版的。网站一改版，先拿新的 HTML 片段试试解析函数，很快就能知道是哪个选择器失效了。

下面先做一道练习，自己动手写一个 `parse_list()` 。

# 五、常见坑

取一页书的办法都学完了。不过真动手写的时候，下面几个坑很容易踩到，有的连报错都没有。

## 1、在整页里找，而不是在外壳里找

先看一段代码。它想打印前 3 本书的书名，运行一下看看：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get('https://learn-py.org/lab/bookstore/').text, 'html.parser')
for card in soup.select('article.book-card')[:3]:
    print(soup.select_one('.title').get_text(strip=True))
```

输出的结果：

```
轻松玩转自动化
轻松玩转自动化
轻松玩转自动化
```

明明是三本书，打印出来却是同一个书名。问题出在哪儿呢？循环里写的是 `soup.select_one()` ，每次都是从整页的开头开始找，找到的当然总是第一本。改成 `card.select_one()` ，在每本书自己的外壳里找，就对了。这个坑最麻烦的地方在于：它不报错，结果却全错了，所以一定要留意。

## 2、有的字段时有时无

在真实的网站上，有的商品没有评分，有的没有折扣价。对应的标签不存在时，`select_one()` 找不到，就会返回 `None` 。这时候再去调用 `get_text()` ，程序就报错了。所以取之前，要先判断一下：

```python
from bs4 import BeautifulSoup

card = BeautifulSoup('<article><h3 class="title">没写价格的书</h3></article>', 'html.parser')
price_tag = card.select_one('.price')
price = float(price_tag.get_text().replace('¥', '')) if price_tag else None
print(price)
```

输出的结果：

```
None
```

这段代码的意思是：先判断标签在不在，在就取出价格，不在就记成 `None` 。这里用到的 `值 if 条件 else 另一个值` ，是把 `if` / `else` 一行写完的写法。

## 3、数字里还夹着别的字符

价格还可能写成 `¥1,299.00` ，千位上多了个逗号。这个逗号 `float()` 不认，所以除了去掉 `¥` ，还要把逗号也去掉：

```python
text = '¥1,299.00'
print(float(text.replace('¥', '').replace(',', '')))
```

输出的结果：

```
1299.0
```

所以，清洗数字之前，最好先打印几个原始的值看看，里面有什么多余的字符，就去掉什么。

## 4、拿相对链接直接去请求

第三节说过，相对链接要先补全。要是忘了这一步，直接拿它去请求，会怎么样呢？

<!-- skip-ci -->
```python
import requests

requests.get('https://learn-py.org/lab/bookstore/books/1/')
```

报错信息的最后一行是：

```
requests.exceptions.MissingSchema: Invalid URL 'https://learn-py.org/lab/bookstore/books/1/': No scheme supplied. Perhaps you meant https://https://learn-py.org/lab/bookstore/books/1/?
```

报错里的 `No scheme supplied` ，意思是没写协议，也就是地址前面少了 `https://` 这一截。所以，相对链接一定要先用 `urljoin()` 补全，再交给 `requests` 。

# 六、自己查一次文档

第三节用 `urljoin()` 补全了链接，用起来很方便。可它到底是按什么规矩拼的呢？咱们先做个小实验：同一个链接 `3/` ，当前网页的地址末尾有斜杠和没有斜杠，拼出来会一样吗？

```python
from urllib.parse import urljoin

print(urljoin('https://learn-py.org/lab/bookstore/page/2/', '3/'))
print(urljoin('https://learn-py.org/lab/bookstore/page/2', '3/'))
```

输出的结果：

```
https://learn-py.org/lab/bookstore/page/2/3/
https://learn-py.org/lab/bookstore/page/3/
```

只差了一个斜杠，结果就不一样了。这是为什么呢？光靠猜是猜不准的，去查一查文档：[urllib.parse.urljoin](https://docs.python.org/zh-cn/3/library/urllib.parse.html#urllib.parse.urljoin) 。

文档里说，它会把一个「基准地址」和另一个地址组合成一个完整的地址，还给了一个例子：`urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')` 得到 `'http://www.cwi.nl/%7Eguido/FAQ.html'` 。

看出规律了吗？在这个例子里，基准地址最后的 `Python.html` 被换成了 `FAQ.html` 。也就是说，基准地址的**最后一段**，也就是最后一个 `/` 后面的部分，会被当成「文件名」换掉。

用这条规律，回头再看上面的小实验，就说得通了：

- `.../page/2/` 末尾是斜杠，最后一段是空的，`3/` 就直接接在后面，成了 `.../page/2/3/` 。
- `.../page/2` 末尾没有斜杠，最后一段是 `2` ，被换成 `3/` ，成了 `.../page/3/` 。

文档再往下读，还有一段提醒：如果第二个地址本身就是完整的地址，比如以 `//` 或 `https://` 开头，结果就直接用它，基准地址里的域名会被换掉。试一试就知道了：

```python
from urllib.parse import urljoin

print(urljoin('https://learn-py.org/lab/bookstore/', 'https://example.com/books/'))
```

输出的结果：

```
https://example.com/books/
```

基准地址里的域名，果然被换掉了。

所以查完文档，可以记住两点。第一，拼链接时，基准地址一定要用**这个链接所在网页的真实地址**，原样照抄，别自己增减斜杠。第二，拼出来的地址，最好检查一下域名，看看还是不是你要抓的那个网站，免得顺着链接跑到别的网站上去。

# 七、小结与回看

这一章，咱们先找外壳、再取字段，然后清洗、补全链接，最后包成一个函数，把一整页书变成了一个整整齐齐的列表。回头梳理一下，学到了这几件事：

- 先用 `select()` 找到每本书的外壳，再用 `card.select_one()` 在外壳里取各个字段。按外壳来取，字段就不会错位。
- 取出来的文字要清洗：价格去掉符号，转成 `float` 。评分数星星，没有评分的用 `None` 。库存比较一下，就是 `True` 或 `False` 。
- 相对链接用 `urljoin(当前网页地址, 链接)` 补全。要注意，基准地址末尾有没有斜杠，结果是不一样的。
- 把解析写成函数 `parse_list(html, page_url)` 。它只管从 HTML 里取数据，所以可以拿一小段 HTML 单独测试。
- 常见的坑有四个：循环里写成了 `soup.select_one()` ；字段可能不存在，要先判断；数字里还夹着逗号；相对链接没补全就去请求。

哪里卡住了，就回去看一看：

- 列表里装字典：实战 2 的「三、一笔账怎么存？」
- 拆函数、单独测试：实战 4 的「二、v2：拆成几个函数」
- 列表生成式：第 7 章

现在，一页书已经能整整齐齐地取出来了。可书店一共有 6 页，难道要一页一页地手动去改地址吗？下一章，咱们就让爬虫自己顺着「下一页」一页一页往下翻，同时控制好速度，处理好出错的情况。
