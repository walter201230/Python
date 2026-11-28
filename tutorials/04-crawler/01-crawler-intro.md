# 爬虫第 1 章：爬虫能做什么、不能做什么

# 前言

学完基础语法和六个实战章，各位童鞋手里其实已经有了不少本事：会读写文件，会用字典、列表整理数据，还会自己查文档，学会一个新模块。

本事有了，可要拿来练手，还缺一样东西：数据。那么，数据从哪儿来呢？

记账本里的数据，是咱们一笔一笔敲进去的。可网上还有大量现成的数据，比如书店里每本书的价格、天气网站上每天的气温、公告栏里的每一条通知。要是一页一页地复制粘贴，几十条还行，几千条就受不了了。

这时候，就可以让程序替我们跑腿，去网页上把数据取下来。这样的程序，就叫**爬虫**。

这门课一共 12 章。前 9 章就在网页里运行，抓的是本站专门搭的一个练习靶场：一家虚构的「两点书店」。别看它是虚构的，真实网站上会遇到的结构，它基本都有：列表页、分页、详情页，还有藏在背后的数据接口。最后 3 章回到自己电脑上，去抓公开的爬虫练习站。

整门课都沿着一条主线走：**获取 → 解析 → 提取 → 存储**。也就是先把网页取回来，再看懂它的结构，接着从里面挑出想要的数据，最后存成文件。抓下来的书店数据，到数据分析课里还会接着用。

不过一开始，咱们先不急着写代码，而是弄清楚一件更要紧的事：爬虫能做什么，不能做什么。

**学这一章之前**，需要先学完基础课的第 0～9 章和实战 1～6，尤其是 [实战 5](../01-basics/09b-practice-5-files-csv-json.md) 的文件读写和 [实战 6](../01-basics/09c-practice-6-learn-a-module.md) 的自学方法。

# 目录

这一章会学到：

- 一、爬虫是什么——用 `requests` 取回第一个网页
- 二、能爬什么、不能爬什么——公开数据、个人信息和版权
- 三、robots.txt——网站写给爬虫的「告示」
- 四、做一个有礼貌的爬虫——放慢速度、只取需要的
- 五、常见坑
- 六、自己查一次文档——`robotparser` 还能告诉我们什么
- 七、小结与回看

学完这一章，你会写出第一个能取回网页的小爬虫，也知道写爬虫之前要先看哪些规矩。

# 一、爬虫是什么

打开浏览器，在地址栏里输入一个网址，按下回车，网页就出来了。

这中间其实发生了两件事。第一件，浏览器向网站**要**这个网页，网站把网页的内容**发回来**；第二件，浏览器再把这些内容画成我们看到的样子。

爬虫做的，只是前一半，也就是第一件事：向网站要网页，再把发回来的内容交给程序去处理。它不需要把网页画出来，只关心里面的文字和数据。

那么，在 Python 里怎么向网站要网页呢？最常用的工具是 `requests` 。它不是 Python 自带的，在自己电脑上要先安装，怎么装第 10 章会讲；在网页里，它已经准备好了，直接 `import` 就能用。

下面就用它取回两点书店的首页：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/')
print(response.status_code)
print(len(response.text))
print(response.text[:15])
```

输出的结果：

```
200
6621
<!doctype html>
```

代码虽然短，可用到的这几样东西，后面每一章都离不开。咱们一行一行地看：

- `requests.get(网址)` 向网站要这个网页。拿回来的结果叫**响应**（response），存在变量 `response` 里。
- `response.status_code` 是**状态码**。`200` 表示「要到了，一切正常」。
- `response.text` 是网页的内容，它是一个很长的字符串。用 `len()` 量一下，有六千多个字符。再看开头，是 `<!doctype html>` ，说明拿回来的是一个 HTML 网页。

就这么三行，第一个爬虫就写好了。

不过，在网页里运行有一个限制：**只能取本站，也就是 learn-py.org 上的网页**。为什么呢？因为浏览器出于安全考虑，不让一个网站上的代码随便去读别的网站。所以前 9 章都在两点书店里练，到了第 10 章，回到自己电脑上，才去抓别的网站。

刚才取的首页是存在的，所以状态码是 `200` 。那么，要是去取一个不存在的网页，又会怎么样呢？

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/no-such-page/')
print(response.status_code)
```

输出的结果：

```
404
```

`404` 表示「没有这个网页」。注意，程序并没有报错，而是老老实实地把状态码交给了你。也就是说，取没取到，得你自己来判断。所以拿到响应以后，第一件事就是看看状态码是不是 `200` 。状态码还有很多种，第 2 章会把它们讲透。

下面先做一道练习，自己取两个网页，看看各自的状态码。

# 二、能爬什么、不能爬什么

上一节，咱们已经取回了第一个网页。会取网页了，是不是网上看得到的东西，就都能拿呢？

当然不是。其实，爬虫能做的事，和你用浏览器能做的事是一样的：浏览器能看到的公开网页，爬虫才能取到。区别在于，爬虫快，一秒钟能要几十个网页，而且不知疲倦。正因为这样，写爬虫要比自己上网多守几条规矩。

那么，哪些能爬，哪些不能爬呢？先说**能爬的**：

- 公开的、不用登录就能看到的信息，比如商品的名称和价格、公开的新闻标题、天气预报。
- 网站明确欢迎抓取的数据，比如专门提供的数据接口、开放数据平台，还有像两点书店这样的练习靶场。

再说**不能爬，或者要特别小心的**：

- **个人信息**：手机号、住址、身份证号，以及能认出具体是谁的信息。哪怕网页上看得见，也不要去批量收集。
- **要登录才能看的内容**：登录以后看到的东西，往往只给你自己看，不代表网站允许你批量取走。
- **受版权保护的内容**：文章、图片、视频，取下来自己学习研究是一回事，拿去转载、发布又是另一回事。
- **网站的条款不允许的**：很多网站的「用户协议」「服务条款」里写了能不能用程序抓取，动手之前先看一眼。

除了这几类，还有一条最容易被忽略：**别给网站添麻烦**。为什么这么说呢？一个人用浏览器看网页，一分钟也就点几次；可一个写坏了的爬虫，一秒钟就可能请求上百次，小网站很可能就这样被拖垮了。

这些规矩，有的是法律要求，有的是行业里的共识。这门课不会讲怎么绕过网站的限制，也不会去抓个人信息。遇到拿不准的情况，就记住一句话：**别人不想让你拿的，就别拿**。

可是，每个网站的要求都不一样。那么，网站怎么告诉爬虫「哪些能拿、哪些不能拿」呢？靠的是一个叫 robots.txt 的文件，下一节就来看看它。

# 三、robots.txt

几乎每个网站的根目录下，都放着一个叫 `robots.txt` 的文件。它是专门写给爬虫看的，上面写着哪些地方可以去，哪些地方别去。

learn-py.org 也有这个文件。咱们用第一节学的 `requests.get()` 把它取回来，看看里面写了什么：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/robots.txt')
print(response.text)
```

输出的结果：

```
User-agent: *
# 练习书店的后台页不允许抓取，爬虫课第 1 章用它演示 robots 规则
Disallow: https://learn-py.org/lab/bookstore/admin/
Allow: /

Sitemap: https://learn-py.org/sitemap.xml

```

内容不多，咱们一行一行地看：

- `User-agent: *` ：下面的规则对谁有效。`*` 表示所有的爬虫。
- `#` 开头的是注释，和 Python 一样，是写给人看的。
- `Disallow: https://learn-py.org/lab/bookstore/admin/` ：这个路径下的网页，不要来抓。
- `Allow: /` ：其他的都可以抓。
- `Sitemap` ：网站地图的地址，告诉搜索引擎站里有哪些网页。

要注意的是，robots.txt 只是一种约定，不是技术上的锁。写在 `Disallow` 里的网页，你照样能用 `requests.get()` 取到，只是守规矩的爬虫不会去取。

learn-py.org 的规则只有几行，用眼睛看就够了。可规则一多，自己一行一行地对，就容易看错。好在 Python 自带了一个模块 `urllib.robotparser` ，专门帮我们判断能不能抓：

<!-- skip-ci -->
```python
import requests
from urllib.robotparser import RobotFileParser

rules = requests.get('https://learn-py.org/robots.txt').text
parser = RobotFileParser()
parser.parse(rules.splitlines())

print(parser.can_fetch('*', 'https://learn-py.org/lab/bookstore/'))
print(parser.can_fetch('*', 'https://learn-py.org/lab/bookstore/admin/'))
```

输出的结果：

```
True
False
```

这段代码先把规则取回来，再交给 `RobotFileParser` 去判断。其中有两处要说一下：

- `parser.parse()` 要的是一行一行的规则，所以先用字符串的 `splitlines()` ，把整段文字拆成一个列表，再交给它。
- `can_fetch(爬虫的名字, 网址)` 回答的是「这个爬虫能不能抓这个网址」。名字写 `'*'` ，表示按对所有爬虫都适用的规则来判断。

再看输出：书店首页可以抓，后台页不行，和咱们自己读出来的一样。

有的童鞋可能会问：为什么不让 `RobotFileParser` 自己去取规则呢？其实它还有一个 `read()` 方法，能自己去网站上取 robots.txt。不过这个方法在网页里用不了，所以这里先用 `requests` 取回来，再交给 `parse()` 。等到第 10 章回到自己电脑上，就可以直接用 `read()` 了。

下面先做一道练习，用 `RobotFileParser` 判断几个路径能不能抓。

# 四、做一个有礼貌的爬虫

robots.txt 告诉了咱们哪些网页能抓。可是，能抓的网页，是不是就可以随便抓了呢？也不是。守 robots.txt 只是第一步，一个有礼貌的爬虫，还要做到这几点：

1. **放慢速度**：每取一个网页，就停一下再取下一个。
2. **只取需要的**：要书名和价格，就别把整个网站都扒下来。
3. **出了错就停**：状态码不对，先停下来看看怎么回事，别一个劲儿地重试。
4. **说明自己是谁**：在请求里带上能联系到你的信息，网站有意见时知道找谁。这一条第 10 章回到自己电脑上再做，原因到时候再说。

先从第 1 条做起。放慢速度，用的是 Python 自带的 `time.sleep()` ：

<!-- skip-ci -->
```python
import time
import requests

for n in range(1, 4):
    url = f'https://learn-py.org/lab/bookstore/page/{n}/'
    response = requests.get(url)
    print(n, response.status_code)
    time.sleep(0.2)
```

输出的结果：

```
1 200
2 200
3 200
```

这段代码依次取了书店的第 1～3 页。每取完一页，`time.sleep(0.2)` 就让程序停 0.2 秒，再去取下一页。运行的时候能感觉到，结果是一行一行慢慢冒出来的。

有的童鞋可能会问：为什么只停 0.2 秒？因为网页里每次运行最多 5 秒，停太久就超时了。这只是为了在网页里练习，**在自己电脑上抓真实的网站，至少停 1 秒**，而且网站越小，停得越久越好。

速度放慢了，可万一中途出了错呢？接下来再加上第 3 条「出了错就停」。这回，故意在页码里混进一个不存在的第 99 页：

<!-- skip-ci -->
```python
import time
import requests

for n in [1, 2, 99, 3]:
    url = f'https://learn-py.org/lab/bookstore/page/{n}/'
    response = requests.get(url)
    if response.status_code != 200:
        print(f'第 {n} 页出错了，状态码 {response.status_code}，先停下来')
        break
    print(f'第 {n} 页取到了')
    time.sleep(0.2)
```

输出的结果：

```
第 1 页取到了
第 2 页取到了
第 99 页出错了，状态码 404，先停下来
```

书店只有 6 页，第 99 页是不存在的。程序取到第 99 页，发现状态码不是 `200` ，就用 `break` 跳出了循环，排在后面的第 3 页也不再去取了。

为什么一出错就要停呢？因为真实的网站出错，可能是网址写错了，也可能是网站嫌你请求太快，开始拒绝了。不管是哪一种，一个劲儿地接着请求，只会让情况更糟。所以先停下来，弄清楚原因再说。

放慢速度和出错就停，下面这道练习都会用到：礼貌地连抓几页，碰到出错就停下来。

# 五、常见坑

规矩和做法都讲完了。不过真动手写的时候，下面这几个坑，刚学爬虫的童鞋很容易踩到。

## 1、以为 robots.txt 能挡住爬虫

第三节说过，robots.txt 只是一份告示，不是门锁。不信可以试一试：被 `Disallow` 的后台页，`requests.get()` 照样取得到：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://learn-py.org/lab/bookstore/admin/')
print(response.status_code)
```

输出的结果：

```
200
```

状态码是 `200` ，说明网页确实取到了。可是能取到，不等于可以取，守不守规矩，全看写爬虫的人。所以在发请求之前，先用 `can_fetch()` 问一句。

## 2、规则的先后顺序

要是同一份 robots.txt 里，`Allow` 和 `Disallow` 管到了同一个网址，该听谁的呢？看下面这个例子：

```python
from urllib.robotparser import RobotFileParser

rules = """User-agent: *
Allow: /
Disallow: /admin/
"""
parser = RobotFileParser()
parser.parse(rules.splitlines())
print(parser.can_fetch('*', 'https://example.com/admin/'))
```

输出的结果：

```
True
```

奇怪，`/admin/` 明明写了 `Disallow` ，怎么结果还是 `True` ？

这是因为，Python 的 `RobotFileParser` 是**从上往下找，用第一条对得上的规则**。`Allow: /` 写在前面，它对所有网址都对得上，所以后面的 `Disallow` 就轮不到了。

可搜索引擎一般不是这么判断的，它们看的是**哪条规则写得更具体**。`/admin/` 比 `/` 更具体，所以它们会认为这个网址不能抓。

同一份规则，两种判断方法，结论却不一样。这也是为什么 learn-py.org 的 robots.txt 把 `Disallow` 写在了 `Allow` 前面：这样不管按哪种方法判断，结论都一样。那么，自己判断别人网站的规则时，遇到这种拿不准的情况怎么办？就按更严格的来。

## 3、循环里忘了停

下面这个循环，各位童鞋看出问题在哪儿了吗？

<!-- skip-ci -->
```python
for n in range(1, 101):
    requests.get(f'https://example.com/page/{n}/')
```

一百个请求一口气发出去，中间没有任何停顿。练习的时候抓自己的靶场还好，可换成真实的网站，很可能就被当成攻击，给封掉了。所以写循环抓网页，第一件事就是把 `time.sleep()` 加上。

## 4、顺手把个人信息也存了下来

第二节说过，个人信息不要去批量收集。可有时候，并不是你想去抓它，而是它自己混了进来：抓网页的时候，评论区的用户名、头像、联系方式，经常和你要的数据混在一起。这时候，用不上的那几项就别存，尤其是能认出具体是谁的信息。因为数据存得越少，出问题的机会就越少。

# 六、自己查一次文档

第四节说，有礼貌的爬虫要放慢速度。可到底隔多久才合适呢？有的网站会直接告诉你：在 robots.txt 里写上一行 `Crawl-delay: 2` ，意思是「每次请求之间请至少隔 2 秒」。

那么，`RobotFileParser` 能不能把这个数读出来呢？前面没有讲过，正好拿它来练一练查文档。按实战 6 的办法，先去官方文档里找：[urllib.robotparser](https://docs.python.org/zh-cn/3/library/urllib.robotparser.html) 。

这一页不长，`RobotFileParser` 的方法一个一个地列在那儿：有前面见过的 `read()` 、`parse()` 、`can_fetch()` ，还有一个 [crawl_delay()](https://docs.python.org/zh-cn/3/library/urllib.robotparser.html#urllib.robotparser.RobotFileParser.crawl_delay) ，看名字就和请求间隔有关。文档是这么说的：为指定的 useragent 从 robots.txt 返回 Crawl-delay 参数的值；如果这个参数不存在，就返回 `None` 。

这正是咱们要的。光看说明还不放心，拿一份写了 `Crawl-delay` 的规则试一试：

```python
from urllib.robotparser import RobotFileParser

rules = """User-agent: *
Crawl-delay: 2
Disallow: /private/
"""
parser = RobotFileParser()
parser.parse(rules.splitlines())
print(parser.crawl_delay('*'))
print(parser.can_fetch('*', 'https://example.com/books/'))
```

输出的结果：

```
2
True
```

间隔读出来了，正是 `2` 。那要是网站没写 `Crawl-delay` 呢？再用 learn-py.org 的规则试试，它就没有写这一行：

<!-- skip-ci -->
```python
import requests
from urllib.robotparser import RobotFileParser

parser = RobotFileParser()
parser.parse(requests.get('https://learn-py.org/robots.txt').text.splitlines())
print(parser.crawl_delay('*'))
```

输出的结果：

```
None
```

和文档说的一样，没有这个参数，就返回 `None` 。

两种情况都弄清楚了，就可以把它用起来：网站写了 `Crawl-delay` ，就按它说的间隔来；没写，就用自己定的默认值。

```python
from urllib.robotparser import RobotFileParser

rules = """User-agent: *
Crawl-delay: 2
"""
parser = RobotFileParser()
parser.parse(rules.splitlines())

delay = parser.crawl_delay('*')
if delay is None:
    delay = 1
print(f'每次请求之间停 {delay} 秒')
```

输出的结果：

```
每次请求之间停 2 秒
```

这里的默认值定的是 1 秒，正好是第四节说的「至少停 1 秒」。

查文档的时候，还可以顺便留意一下同一个类的其他方法。比如 `request_rate()` ，它读的是 `Request-rate` 这一行，表示「多少秒内最多请求几次」。现在用不上，知道有这么个东西就行，真遇到了再回来查。

# 七、小结与回看

这一章，咱们取回了第一个网页，不过还没正式抓数据，而是先把规矩立好了。回头梳理一下，学到了这几件事：

- 爬虫就是让程序替你向网站要网页。`requests.get(网址)` 拿回响应，`status_code` 看要到没有，`text` 是网页内容。
- 在网页里运行时，只能取 learn-py.org 上的网页；第 10 章回到自己电脑上，才去抓别的网站。
- 公开的、网站允许的数据可以抓；个人信息、要登录才能看的内容、受版权保护的内容，不去批量收集。
- 动手之前先看 robots.txt。`RobotFileParser` 的 `parse()` 读规则，`can_fetch()` 判断能不能抓，`crawl_delay()` 读请求间隔。
- `RobotFileParser` 按从上往下、第一条对得上的规则来判断，和搜索引擎不完全一样。拿不准的时候，就按更严格的来。
- 有礼貌的爬虫要做到四点：放慢速度、只取需要的、出了错就停、说明自己是谁。

哪里卡住了，就回去看一看：

- `for` 循环和 `break` ：第 5 章
- 切片：第 3 章
- 自学一个模块的四步：实战 6

robots.txt 也好，放慢速度也好，都不是技术难题，靠的是写爬虫的人自觉。规矩先立好，后面学到的本事越大，用起来才越放心。

这一章只是用 `requests.get()` 把网页取了回来，它背后到底发生了什么，还没有细说。下一章，咱们就来看看：网址由哪几部分组成，状态码都有哪些，网站发回来的除了网页，还有些什么。
