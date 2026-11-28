# 爬虫第 4 章：BeautifulSoup 基础

# 前言

上一章，咱们用 `find()` 和切片，从网页里抠出了一个书名。办法是能用，可是费劲，网页稍微一改，代码就得跟着改。

有没有更省事的办法呢？这一章就请出专门解析 HTML 的工具：**BeautifulSoup**。它能把一大段 HTML 变成一棵可以随意翻找的树。你只要告诉它「找 `class="price"` 的标签」，它就把价格交到你手上。而且上一章学的 CSS 选择器，在这里直接就能用。

顺便说一句，BeautifulSoup 这个名字，来自《爱丽丝漫游奇境》里的一首歌。它不是 Python 自带的，在自己电脑上要装 `beautifulsoup4` 这个包，怎么装第 10 章会讲；在网页里，它已经准备好了。

BeautifulSoup 的方法不少，学的时候别想着一口气全记住。常用的其实就那么几个：`find()` 、`find_all()` 、`select()` 、`select_one()` 、`get_text()` 。先把这几个用熟，其他的遇到了再查。

**学这一章之前**，需要先学完 [爬虫课第 3 章](03-html-and-devtools.md) ，认识 HTML 的标签、属性和 CSS 选择器。

# 目录

这一章会学到：

- 一、把网页交给 BeautifulSoup——第一碗汤
- 二、`find()` 和 `find_all()` ——按标签名和属性找
- 三、`select()` 和 `select_one()` ——用 CSS 选择器找
- 四、拿到标签以后——取文字、取属性、顺着树找
- 五、常见坑
- 六、自己查一次文档——`get_text()` 还能怎么用
- 七、小结与回看

学完这一章，你能用 BeautifulSoup 从一个网页里准确地取出想要的文字和链接。

# 一、把网页交给 BeautifulSoup

BeautifulSoup 到底有多省事？咱们拿上一章硬抠过的那个书名来比一比，用 BeautifulSoup 再取一次：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/books/12/').text
soup = BeautifulSoup(html, 'html.parser')
print(soup.title.get_text())
print(soup.h2.get_text())
```

输出的结果：

```
色彩的力量 · 两点书店
色彩的力量
```

上一章切了好几刀才拿到的书名，这里一行就取出来了。代码里有几样新东西，咱们一行一行地看：

- `from bs4 import BeautifulSoup` ：包的名字叫 `beautifulsoup4` ，导入的时候写 `bs4` 。
- `BeautifulSoup(html, 'html.parser')` ：把 HTML 字符串交给它，第二个参数说明用哪个**解析器**。`html.parser` 是 Python 自带的，不用另外安装。得到的对象，大家习惯叫它 `soup` 。
- `soup.title` ：网页里第一个 `<title>` 标签。`soup.h2` 也是同样的道理，是第一个 `<h2>` 。
- `.get_text()` ：取出标签里的文字。

`soup.标签名` 这种写法很方便，可它有两个毛病：一是只能找到**第一个**，页面上有好几个同名的标签时，后面的就拿不到了；二是没法指定 class。

那么，要找得准，该怎么办呢？这就要用下面几节的方法了。

# 二、find() 和 find_all()

先说 `find()` 。它可以按标签名和属性来找，返回**第一个**对得上的标签。比如要找详情页里的价格：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/books/12/').text
soup = BeautifulSoup(html, 'html.parser')
price = soup.find('td', class_='price')
print(price)
print(price.get_text())
```

输出的结果：

```
<td class="price">¥64.50</td>
¥64.50
```

`find('td', class_='price')` 的意思是：找 `class` 是 `price` 的 `td` 标签。直接打印找到的标签，看到的是整段 HTML；加上 `get_text()` ，才是里面的文字。

另外注意，`class_` 后面多了一个下划线。为什么要加，第五节「常见坑」里会讲。

`find()` 只给第一个。那要是想要一页里所有的价格呢？这就要用 `find_all()` ，它返回**所有**对得上的标签，放在一个列表里：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
prices = soup.find_all('p', class_='price')
print(len(prices))
for p in prices[:3]:
    print(p.get_text())
```

输出的结果：

```
20
¥104.40
¥42.70
¥56.20
```

一页 20 本书，就找到了 20 个价格。拿到的是列表，所以用 `for` 一个一个地取出来，这里只打印了前 3 个。

除了 `class_` ，其他属性也可以拿来找。比如每本书卡片上的 `data-id` ，记着这本书的编号。要按编号找书，就把属性写成字典，交给 `attrs` ：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
card = soup.find('article', attrs={'data-id': '5'})
print(card.find('h3').get_text())
```

输出的结果：

```
实战学数据分析
```

为什么不像 `class_` 那样，直接写成参数呢？因为 `data-id` 中间有个减号，没法写成 `data-id='5'` 这样的参数，只能放进 `attrs` 字典里。

这段代码里还有一个细节：`card.find('h3')` 是在 `card` **里面**找，而不是在整个网页里找。先找到一本书，再在这本书里找书名，这是后面抓列表页的基本套路。

下面先做一道练习，从详情页里取出书名、价格和库存。

# 三、select() 和 select_one()

`find()` 一次只能描述一个标签：它叫什么，带什么属性。要是位置得穿过好几层才说得清，比如「书卡里、书名标题里的那个链接」，就得一层一层地找下去。

还记得上一章学的 CSS 选择器吗？它一句话就能把好几层的位置说清楚。把选择器交给 `select()` ，就能直接用：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
titles = soup.select('article.book-card h3.title a')
print(len(titles))
print(titles[0].get_text())
```

输出的结果：

```
20
轻松玩转自动化
```

一句选择器，就选中了这一页全部 20 本书的书名链接。

`select()` 和 `find_all()` 一样，返回的是一个列表。那只要第一个呢？用 `select_one()` ，它和 `find()` 一样，只返回第一个对得上的标签：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/books/12/').text
soup = BeautifulSoup(html, 'html.parser')
print(soup.select_one('article.book-detail .title').get_text())
print(soup.select_one('td.stock').get_text())
```

输出的结果：

```
色彩的力量
6 本
```

到这里，找标签的方法已经有了两套。各位童鞋可能会问：这两套方法，该怎么选呢？先对比一下：

| 想做的事 | `find` 系列 | `select` 系列 |
|---|---|---|
| 找第一个 | `find('td', class_='price')` | `select_one('td.price')` |
| 找全部 | `find_all('p', class_='price')` | `select('p.price')` |
| 位置要穿过好几层 | 一层一层 `find` 下去 | 一个选择器写完：`'article.book-card h3.title a'` |

可以看到，两套方法效果差不多。不过选择器能在开发者工具里直接复制、直接测试，层次多的时候写起来也更短，所以这门课后面主要用 `select()` 和 `select_one()` 。

下面先做一道练习，用 `select()` 选出一页里所有的书名链接。

# 四、拿到标签以后

标签找到了，接下来能拿它做什么呢？`find()` 、`select_one()` 拿回来的，是一个**标签对象**。除了用 `get_text()` 取文字，它还能做好几件事。

先说取属性。比如书名链接指向的地址，就放在 `href` 属性里。取属性可以像字典一样用方括号，也可以用 `get()` ：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
link = soup.select_one('h3.title a')
print(link['href'])
print(link.get('title'))
print(link.parent.name)
```

输出的结果：

```
https://learn-py.org/lab/bookstore/books/1/
None
h3
```

三行输出，分别对应三种用法：

- `link['href']` ：取 `href` 属性。要是这个属性不存在，会报错。
- `link.get('title')` ：属性不存在时，返回 `None` ，不报错。这个链接没有 `title` 属性，所以打印出了 `None` 。拿不准有没有这个属性时，就用 `get()` 。
- `link.parent` ：父元素，这里是装着链接的 `h3` 。后面的 `.name` 是标签的名字。

`parent` 只能往上走一层。可很多时候，要找的不是父元素，而是更上面的某一层，比如装着它的那本书。这时候，更常用的是 `find_parent()` ：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/').text
soup = BeautifulSoup(html, 'html.parser')
first_sold_out = soup.select_one('p.stock.out')
card = first_sold_out.find_parent('article')
print(card['data-id'], card.select_one('.title').get_text())
```

输出的结果：

```
19 从零开始学数据分析
```

这段代码分两步走：先找到第一个「缺货」的标签，再顺着它往上，找到装着它的那本书，这样就知道是哪本书缺货了。

其中的选择器 `p.stock.out` 也要说一下：两个 class 连着写，表示同时带着 `stock` 和 `out` 两个 class 的 `p` 。

往上找会了，再来看看往里找。上一章查文档时看过详情页的表格：每一行 `tr` 里，`th` 写着这是什么，`td` 写着值。这样一对一对的，正好拼成一个字典：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/books/12/').text
soup = BeautifulSoup(html, 'html.parser')
info = {}
for row in soup.select('table.info tr'):
    info[row.th.get_text()] = row.td.get_text()
print(info)
```

输出的结果：

```
{'作者': '唐知秋', '分类': '设计', '价格': '¥64.50', '评分': '4.9（7 条评价）', '库存': '6 本', '页数': '599', '出版年份': '2008'}
```

这里的 `row.th` ，用的就是第一节那种「点出标签名」的写法，只不过用在了一行上：它取的是这一行里的第一个 `th` 。这样，七行信息就变成了一个字典，想要哪一项，就取哪一项。

下面先做一道练习，顺着缺货的标签往上找，看看一页里有哪些书缺货。

# 五、常见坑

BeautifulSoup 用起来顺手，可刚上手的时候，有几个错误特别容易犯。下面一个一个来看。

## 1、按 class 找，写成了 class=

第二节说过，按 class 找要写成 `class_` 。要是忘了那个下划线，会怎么样呢？

<!-- skip-ci -->
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<p class="price">¥64.50</p>', 'html.parser')
print(soup.find('p', class='price'))
```

报错信息是这样的：

```
  File "main.py", line 4
    print(soup.find('p', class='price'))
                         ^^^^^
SyntaxError: invalid syntax
```

为什么会这样？因为 `class` 是 Python 的关键字，基础课第 8 章定义类时用的就是它，不能拿来当参数名。所以 BeautifulSoup 改用 `class_` ，在后面加了一个下划线。

## 2、没找到，返回了 None

再看一个更常见的错误：

<!-- skip-ci -->
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<p class="price">¥64.50</p>', 'html.parser')
tag = soup.find('p', class_='prize')
print(tag)
print(tag.get_text())
```

先打印出 `None` ，接着报错，最后一行是：

```
AttributeError: 'NoneType' object has no attribute 'get_text'
```

问题出在哪儿呢？`class_` 的值把 `price` 写成了 `prize` ，就差一个字母，于是什么也没找到。没找到的时候，`find()` 并不报错，而是返回 `None` 。可 `None` 没有 `get_text()` ，所以到了下一行才报错。

写爬虫时最常见的报错，就是这一个。所以以后看到 `'NoneType' object has no attribute` ，先回头查查选择器写得对不对，再去开发者工具里看看网页是不是变了。

## 3、把列表当成一个标签用

第三节说过，`select()` 返回的是一个列表。要是忘了这一点，直接拿它当一个标签来用呢？

<!-- skip-ci -->
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<p class="price">¥64.50</p><p class="price">¥47.30</p>', 'html.parser')
prices = soup.select('p.price')
print(prices.get_text())
```

报错信息的最后一行是：

```
AttributeError: ResultSet object has no attribute 'get_text'. You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?
```

`select()` 和 `find_all()` 返回的是列表，而列表没有 `get_text()` 。这条报错信息其实说得很明白：你可能把一组元素当成了一个元素。那该怎么改呢？要么换成 `select_one()` ，只取一个；要么用 `for` 一个一个地取。

## 4、class 属性是一个列表

第四节见过同时带着两个 class 的标签。取它的 `class` 属性，拿到的会是什么呢？

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<p class="stock out">缺货</p>', 'html.parser')
print(soup.p['class'])
```

输出的结果：

```
['stock', 'out']
```

拿到的不是字符串，而是一个列表。因为一个标签可以同时有好几个 class，所以 BeautifulSoup 把 `class` 拆成了列表。那想判断它有没有某个 class，该怎么写呢？用 `'out' in soup.p['class']` ，别拿它和字符串 `'stock out'` 比。

# 六、自己查一次文档

第四节把详情页的表格拼成了字典。要是不拼字典，只想把整个表格的文字一口气取出来，`get_text()` 行不行呢？

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/books/12/').text
soup = BeautifulSoup(html, 'html.parser')
print(repr(soup.select_one('table.info').get_text()))
```

输出的结果：

```
'\n作者唐知秋\n分类设计\n价格¥64.50\n评分4.9（7 条评价）\n库存6 本\n页数599\n出版年份2008\n'
```

先说一句，这里用 `repr()` 打印，是为了看清里面的换行符 `\n` 。再看结果：文字是取出来了，可「作者」和「唐知秋」粘在了一起，也不好拆开。

要是能在每段文字之间加个分隔符就好了。`get_text()` 有没有这个本事呢？这就得去查 BeautifulSoup 的文档了，好在它有中文版：[Beautiful Soup 4 文档 · get_text()](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#get-text) 。

文档里说，`get_text()` 会取出标签里所有的文字，包括子孙标签里的。往下看，它的例子里写着 `soup.get_text("|", strip=True)` ：第一个参数是**分隔符**，夹在每两段文字中间；`strip=True` 会去掉每一段文字前后的空白。

说明看懂了，就照着它试一试：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

html = requests.get('https://learn-py.org/lab/bookstore/books/12/').text
soup = BeautifulSoup(html, 'html.parser')
print(soup.select_one('table.info').get_text('|', strip=True))
```

输出的结果：

```
作者|唐知秋|分类|设计|价格|¥64.50|评分|4.9（7 条评价）|库存|6 本|页数|599|出版年份|2008
```

这回，每段文字之间都隔上了 `|` ，前后的换行也没了。要是再 `split('|')` 一下，就能得到一个列表。

最后，还要留意一下文档的版本。这份中文文档对应 Beautiful Soup 4.12.0，网页里用的是 4.12.3，同一个大版本，用法一样。所以查文档时，先看一眼版本：版本差得多，有的写法可能已经变了。

# 七、小结与回看

这一章，咱们解析网页终于有了趁手的工具。回头梳理一下，学到了这几件事：

- `BeautifulSoup(html, 'html.parser')` 把 HTML 变成一棵可以翻找的树。
- `find()` 找第一个、`find_all()` 找全部，按标签名和 `class_` 、`attrs` 找。
- `select_one()` 找第一个、`select()` 找全部，用 CSS 选择器找；层次多时写起来更短。
- 拿到标签以后：`get_text()` 取文字，`['属性']` 或 `get('属性')` 取属性，`parent` 、`find_parent()` 往上找，在标签上再 `find` 、`select` 是往里找。
- 常见坑：`class_` 要带下划线；没找到时返回 `None` ；列表没有 `get_text()` ；`class` 属性是列表。
- `get_text('|', strip=True)` 用分隔符把每段文字隔开，并去掉前后的空白。

哪里卡住了，就回去看一看：

- CSS 选择器：爬虫课第 3 章「四、用 CSS 选择器描述位置」
- 字典、`for` 循环：第 4、5 章
- 读懂 `AttributeError` 这类报错：实战 3

到这里，咱们已经能从一个网页里，准确地取出单个数据了。可一页上有 20 本书，怎么把它们都取下来呢？下一章，就把一整页 20 本书的书名、作者、价格、评分、库存都取出来，整理成一个列表，顺便把「¥104.40」这样的文字，清洗成能计算的数字。
