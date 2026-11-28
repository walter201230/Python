# 爬虫第 11 章：Session 与 Cookie：登录以后再抓

# 前言

各位童鞋，到目前为止，咱们每次调用 `requests.get()` ，都是一次全新的请求，网站根本不知道你上一次来过没有。可平时上网的时候，明明登录一次就够了，后面点开的每个网页，网站都还记得你是谁。这是怎么做到的呢？

靠的是 **Cookie**。它的道理并不复杂：网站发给你一小段文字，浏览器把它存起来，以后每次访问这个网站，都带上它。网站一看，就认出你来了。

所以这一章，先弄清楚 Cookie 是怎么回事，再用 `requests.Session` 在自己电脑上登录一个练习网站。登录成功以后，还要想清楚一件更重要的事：登录了，能抓什么，不能抓什么？

这一章的规矩，会比前面几章都多。为什么呢？因为登录以后看到的东西，往往就不再是公开的了。技术上做得到，不等于就应该去做。

**学这一章之前**，需要先学完 [爬虫课第 10 章](10-local-requests.md) ，在自己电脑上配好环境，装好 requests 和 beautifulsoup4。

# 目录

这一章会学到：

- 一、网站怎么记住你——Cookie
- 二、让 requests 也记住——`requests.Session`
- 三、登录一个练习网站——表单、隐藏字段和 POST
- 四、登录以后，能抓什么
- 五、常见坑
- 六、自己查一次文档——用 `http.cookies` 读懂一条 Cookie
- 七、小结与回看

学完这一章，你能看懂 Cookie，用 Session 保持登录状态，并清楚登录以后的抓取边界在哪儿。

# 一、网站怎么记住你

先回到前言里的那个问题：网站是怎么记住你的？

要知道，HTTP 本身是「健忘」的：每一次请求都是独立的，网站不会因为你刚才来过，就认出你。所以要想记住你，网站得自己想个办法。

这个办法就是 **Cookie**。整个过程分三步：

1. 你第一次访问，网站在响应头里加一行 `Set-Cookie: session=一串文字` ，意思是「请把这个记下来」。
2. 浏览器把它存起来。
3. 之后你再访问这个网站，浏览器会自动在请求头里加一行 `Cookie: session=一串文字` 。网站一看，就知道是你。

明白了这三步，登录也就好理解了：所谓登录，其实就是网站在 Cookie 里记下了「这个人已经登录了」。

道理说完了，来看一个真实的例子。在自己电脑上运行下面的代码，看看 quotes.toscrape.com 的登录页，都发回了什么 Cookie：

<!-- skip-ci -->
```python
import requests

response = requests.get('https://quotes.toscrape.com/login')
print(list(response.cookies.keys()))
print(response.headers['Set-Cookie'].split(';')[1:])
```

在自己电脑上运行，输出是：

```
['session']
[' HttpOnly', ' Path=/']
```

第一行说明，网站发来了一个叫 `session` 的 Cookie。`Set-Cookie` 里除了名字和值，后面还跟着几个属性，第二行打印的就是它们：

- `Path=/` ：这个网站的所有网址，都要带上这个 Cookie。
- `HttpOnly` ：网页里的 JavaScript 读不到它，它只在请求里发来发去，这样比较安全。

那 Cookie 的值呢？它是一长串看不懂的文字。这是网站自己的事，咱们不用去解读它，原样带回去就行。

问题来了：`requests` 会自动把它带回去吗？

# 二、让 requests 也记住

答案是：单独用 `requests.get()` ，**不会**。每次调用 `requests.get()` ，都像是新开了一个浏览器窗口，上一次拿到的 Cookie，不会带到下一次去。

那怎么让 `requests` 像浏览器一样，记住 Cookie 呢？要用 **Session**（会话）：

<!-- skip-ci -->
```python
import requests

session = requests.Session()
session.get('https://quotes.toscrape.com/login')
print(list(session.cookies.keys()))
```

在自己电脑上运行，输出是：

```
['session']
```

这回 `session.cookies` 里有了 `session` 这个 Cookie，说明它记住了。

`requests.Session()` 会创建一个会话对象，用法和 `requests` 几乎一样，也有 `session.get()` 、`session.post()` 。区别在于，它会把每次响应里的 Cookie 都存进 `session.cookies` ，下一次请求的时候，再自动带上。

除了记住 Cookie，Session 还有一个好处：对同一个网站的多次请求，它会复用同一个网络连接，比每次都重新连接要快一些。所以哪怕不用登录，要连续抓同一个网站的很多页时，用 Session 也是个好习惯。

还有一个方便的地方：请求头也可以设在 Session 上，以后它发出的每个请求，都会带着：

<!-- skip-ci -->
```python
import requests

session = requests.Session()
session.headers['User-Agent'] = 'learn-py-practice/1.0 (contact: you@example.com)'
response = session.get('https://quotes.toscrape.com/')
print(response.request.headers['User-Agent'])
```

在自己电脑上运行，输出是：

```
learn-py-practice/1.0 (contact: you@example.com)
```

上一章，每次请求都要写一遍 `headers=HEADERS` ；现在，设一次就够了。

Session 会用了，下一节就用它，真正去登录一个练习网站。

# 三、登录一个练习网站

Session 能记住 Cookie 了，现在就用它来真正登录一次。[quotes.toscrape.com](https://quotes.toscrape.com/login) 上有一个练习用的登录页。toscrape 的首页说明了：这个登录要带 CSRF 令牌，用户名和密码随便填，都能登录。CSRF 令牌是什么，下面马上就会讲到。

登录一共分三步来做。

**第一步：看清表单。** 在浏览器里打开登录页，用开发者工具看看登录表单长什么样。然后用 BeautifulSoup 把它取出来：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
page = session.get('https://quotes.toscrape.com/login')
form = BeautifulSoup(page.text, 'html.parser').select_one('form')
print(form['action'], form['method'])
for field in form.select('input'):
    print(field.get('name'), field.get('type'))
```

在自己电脑上运行，输出是：

```
/login post
csrf_token hidden
username text
password password
None submit
```

从输出里，能看出两件事：

- 表单提交到 `/login` ，方法是 `post` 。第 2 章说过，取网页用 `GET` ，提交表单用 `POST` 。
- 要填的字段有三个：`username` 、`password` ，还有一个藏起来的 `csrf_token` 。

那么，`csrf_token` 是什么呢？它是网站在登录页里埋下的一串随机文字，叫 **CSRF 令牌**。提交表单的时候，必须把它原样带回去。网站核对一致了，才相信这次提交是从它自己的登录页发出来的，而不是别的网站伪造的。所以登录的顺序是：先取登录页，从里面拿到令牌，再提交。

**第二步：提交表单。** 令牌拿到了，就和用户名、密码一起提交：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
page = session.get('https://quotes.toscrape.com/login')
token = BeautifulSoup(page.text, 'html.parser').select_one('input[name="csrf_token"]')['value']
response = session.post('https://quotes.toscrape.com/login', data={
    'csrf_token': token,
    'username': 'practice',
    'password': 'any-password',
})
print(response.url)
print([r.status_code for r in response.history])
print('Logout' in response.text)
```

在自己电脑上运行，输出是：

```
https://quotes.toscrape.com/
[302]
True
```

这段代码和输出，有三个地方要看一看：

- `session.post(网址, data=字典)` 用来提交表单，字典的键就是表单里各个字段的 `name` 。
- 提交以后，网站用 `302` 让我们跳转回首页，`requests` 自动跟了过去。`response.history` 里记着这次跳转，所以第二行打印出来的是 `[302]` 。
- 首页上出现了 `Logout` （退出登录），说明登录成功了。

**第三步：带着登录状态继续抓。** 登录成功了，接下来怎么抓呢？很简单，用同一个 `session` 接着请求，看到的就是登录以后的样子。那要是换成单独的 `requests.get()` 呢？看到的还是没登录的样子。下面把两种放在一起比一比：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
page = session.get('https://quotes.toscrape.com/login')
token = BeautifulSoup(page.text, 'html.parser').select_one('input[name="csrf_token"]')['value']
session.post('https://quotes.toscrape.com/login', data={'csrf_token': token, 'username': 'practice', 'password': 'any-password'})

logged_in = session.get('https://quotes.toscrape.com/')
anonymous = requests.get('https://quotes.toscrape.com/')
print('Logout' in logged_in.text, 'Logout' in anonymous.text)
print('Goodreads' in logged_in.text, 'Goodreads' in anonymous.text)
```

在自己电脑上运行，输出是：

```
True False
True False
```

每一行左边的结果来自 `logged_in` ，也就是用 `session` 取到的首页；右边的来自 `anonymous` ，也就是单独用 `requests.get()` 取到的首页。

第二行说明，登录以后，这个网站会在每条名言旁边多显示一个 Goodreads 链接，没登录就没有。也就是说，同一个网址，登没登录，看到的内容是不一样的。这也是为什么有的数据，非得登录以后才能取到。

登录的三步都走通了。下面先做两道练习，再接着往下看。

# 四、登录以后，能抓什么

回头看看上一节，技术上，登录其实并不难：取表单、带上令牌、提交，再用 Session 接着请求。可正因为不难，动手之前，更要先想清楚边界在哪儿。

为什么登录以后要格外小心呢？因为登录以后看到的内容，和公开的网页不一样：

- 很多是**只给你自己看**的：你的订单、你的消息、你的收藏。
- 有的是**给会员看**的：付费的文章、课程、数据。
- 有的里面有**别人的信息**：好友列表、群成员、评论者的资料。

所以，登录以后的抓取，要守住这几条：

1. **只抓自己的东西**。用自己的账号，导出自己的数据，这通常没问题。而且很多网站本身就提供了「导出数据」的功能，先找找有没有，有就用它。
2. **别人的信息不碰**。哪怕登录以后看得到，也不去批量收集别人的资料。
3. **先看网站的条款**。很多网站明确禁止用程序登录、抓取，那就别做。
4. **不共享、不硬编码账号**。别拿别人的账号去登录，也别把自己的密码写进代码里。不写进代码，那密码放哪儿？第五节会讲怎么做。
5. **付费内容不外传**。会员能看到的内容，抓下来自己学习是一回事，拿去发布、转卖，就是另一回事了。

这门课只在 toscrape 这类明确允许练习的网站上演示登录。到了真实的网站，拿不准能不能抓的时候，就别抓。

# 五、常见坑

登录这件事，步骤不算多，可每一步都有容易出错的地方。下面这几个坑，最常见。

## 1、登录用的是 session，后面又换成了 requests

<!-- skip-ci -->
```python
session.post('https://quotes.toscrape.com/login', data=form_data)
page = requests.get('https://quotes.toscrape.com/')
```

问题出在哪儿呢？登录时用的是 `session` ，Cookie 也就存在了 `session` 里；可后面取网页时，却换成了 `requests.get()` 。Cookie 没带上，网站又把你当成了没登录的人。第三节最后那个例子里，`anonymous` 就是这样取到的。所以记住：登录以后，所有的请求都要用同一个 `session` 。

## 2、没带令牌，登录失败了

要是不带 `csrf_token` ，直接提交，会怎样？网站并不会报错，而是把你送回登录页，页面上写着一行提示。在自己电脑上，把这行提示取出来看看：

<!-- skip-ci -->
```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.get('https://quotes.toscrape.com/login')
response = session.post('https://quotes.toscrape.com/login', data={'username': 'practice', 'password': 'any-password'})
print(response.url)
print(BeautifulSoup(response.text, 'html.parser').select_one('.error').get_text(strip=True))
```

在自己电脑上运行，输出是：

```
https://quotes.toscrape.com/login
Error while logging in: invalid CRSF token.
```

（网站把 CSRF 拼成了 CRSF，原文如此。）

注意看：网址还是登录页，提示说令牌不对。状态码是 200，程序也没有报错，可登录其实并没有成功。所以提交以后，一定要检查一下，登录到底成没成功，比如看看页面上有没有「Logout」。

## 3、把密码写进了代码

<!-- skip-ci -->
```python
session.post(url, data={'username': 'me', 'password': 'my-real-password'})
```

这样写，代码一分享、一上传，密码就跟着泄露了。所以真实的账号，密码不要写进代码里。那密码从哪儿来呢？可以用 Python 自带的 `getpass` ，运行的时候在终端里输入，输入的内容不会显示出来：

<!-- skip-ci -->
```python
from getpass import getpass

password = getpass('密码：')
```

还有一个办法，是把密码存在环境变量里，用 `os.environ['变量名']` 读取。这样代码里就只剩一个变量名，看不到密码了。

## 4、登录状态过一阵就没了

Cookie 是会过期的，网站也可能隔一段时间，就要求重新登录一次。所以程序跑得久了，要时不时检查一下，自己还是不是登录状态。失效了，就重新登录一次，而不是对着「请先登录」的页面，一直抓下去。

# 六、自己查一次文档

第一节里，`Set-Cookie` 是这样一行：`session=一串文字; HttpOnly; Path=/` 。当时咱们用 `split(';')` ，粗略地把它拆开看了看。那么，Python 有没有专门用来解析 Cookie 的工具呢？

有，就在 `http.cookies` 模块里。去查一下文档：[http.cookies --- HTTP 状态管理](https://docs.python.org/zh-cn/3/library/http.cookies.html) 。

文档里，有两个类正好用得上：

- [SimpleCookie](https://docs.python.org/zh-cn/3/library/http.cookies.html#http.cookies.SimpleCookie) ：装 Cookie 的容器。它的 `load()` 方法能解析一段 Cookie 文字，找到的每一个 Cookie，都会变成一个 `Morsel` 。
- [Morsel](https://docs.python.org/zh-cn/3/library/http.cookies.html#http.cookies.Morsel) ：代表一个 Cookie。它像一个字典，键是一组固定的属性：`expires` 、`path` 、`domain` 、`max-age` 、`secure` 、`httponly` 、`samesite` 等等；而它的 `value` ，就是 Cookie 的值。

光看说明还不够，拿一条 Set-Cookie 来试一试。这段代码在网页里就能运行：

```python
from http.cookies import SimpleCookie

cookie = SimpleCookie()
cookie.load('session=abc123; HttpOnly; Path=/; Max-Age=3600')
morsel = cookie['session']
print(morsel.key, morsel.value)
print(morsel['path'], morsel['max-age'], morsel['httponly'])
```

输出的结果：

```
session abc123
/ 3600 True
```

名字、值、每一个属性，都拆得清清楚楚。其中 `Max-Age=3600` 表示这个 Cookie 一小时以后就过期，正好对上第五节说的「登录状态过一阵就没了」。

文档的属性表里，还有一项 `partitioned` 。仔细看，文档注明了它是 3.14 版才加的。网页里运行的是 Python 3.12，所以用不了它。这也提醒咱们：查文档的时候，要留意这类版本说明。

最后说一句：平时用 `requests.Session` ，这些它都替你处理好了，用不着自己拆。可是遇到「为什么登录状态带不过去」这类问题的时候，把 Cookie 拆开，看看它的 `path` 、`domain` 、过期时间，往往就能找到原因。

# 七、小结与回看

这一章，咱们从「网站怎么记住你」说起，弄清楚了登录是怎么回事。回头梳理一下，学到了这几件事：

- 网站用 `Set-Cookie` 发给你一个 Cookie，浏览器以后每次请求，都在 `Cookie` 请求头里带上它，网站就认出你了。
- 单独的 `requests.get()` 不会记住 Cookie；`requests.Session()` 会，而且还能复用连接、统一设置请求头。
- 登录三步：取登录页，拿到 CSRF 令牌这类隐藏字段，再用 `session.post(网址, data=字典)` 提交。之后的请求，都用同一个 session。
- 提交以后，要检查到底登录成功没有，比如看看页面上有没有「Logout」。
- 登录以后，只抓自己的东西，别人的信息不碰，先看条款。密码不写进代码，用 `getpass` 或环境变量。
- `http.cookies.SimpleCookie` 能把一条 Cookie 拆成名字、值和各个属性。

哪里卡住了，就回去看一看：

- 请求方法 `GET` 和 `POST` ：爬虫课第 2 章
- 表单、`input` 标签和 BeautifulSoup：爬虫课第 3、4 章
- 本地环境和 User-Agent：爬虫课第 10 章

登录学会了，可还有一些网站，`requests` 怎么都搞不定。下一章是爬虫课的最后一章，就来看其中的两种情况：一种是数据要靠 JavaScript 才显示出来，网页背后又找不到好用的接口；另一种是网页太多，一页一页地抓，太慢了。
