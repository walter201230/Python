# 实战 6：自学一个新模块

# 前言

各位童鞋，这是基础部分的最后一个实战章了。

前面几章，每个新东西都是教程一步一步讲给你听的。可等你真正自己写程序的时候，会发现要用的模块成百上千，不可能每一个都有人手把手地教。

所以这一章换个学法：**咱们自己学会一个没讲过的模块**。

学哪个呢？就学 Python 自带的 `datetime` 。它在第 9 章只是露了个面，演示了怎么创建一个日期。这一章，咱们要用它给记账本的每一笔账加上日期，再算出最近 7 天花了多少钱。

那又该怎么学呢？不靠背，靠这几样：先说清楚要做什么，再去官方文档里找，然后用 `dir()` 和 `help()` 看看有哪些工具，最后用几个小例子验证自己的理解。这套办法，换成任何一个模块都管用。

自学的时候，看不懂文档，或者试出来的结果和想的不一样，都是常事。碰到这种情况，别急着去搜现成的答案，先自己多试几次。因为自己试出来的东西，记得最牢。

**学这一章之前**，需要先学完 [实战 5](09b-practice-5-files-csv-json.md) 的记账本 v4，以及 [第 9 章](09-modules.md) 的「学会用一个陌生模块」和「几个常用的标准库」。

# 目录

这一章会学到：

- 一、账单缺了日期——光知道花了多少，不知道是哪天花的
- 二、自学一个模块，分四步——先列需求，再找文档
- 三、今天是几号？——`date` 、`date.today()` 和 `fromisoformat()`
- 四、7 天前是哪天？——用 `timedelta` 算日期
- 五、显示成「11月02日」——`strftime()` 和格式代码
- 六、常见坑
- 七、自己查一次文档——一周从星期几算起？
- 八、记账本 v5
- 九、小结与回看

学完这一章，你的记账本会给每一笔账记上日期，还能算出最近 7 天花了多少钱；更重要的是，你会有一套自学新模块的办法。

# 一、账单缺了日期

上一章，记账本 v4 已经能把账存进文件了。可是打开 `my_ledger.json` 看一看，每一笔账只有三样东西：

```
{
  "item": "奶茶",
  "category": "餐饮",
  "cost": 12.5
}
```

买了什么、什么类别、花了多少，唯独没有**哪天花的**。

少了日期，会有什么麻烦呢？假如账记了一个月，想知道这个星期花了多少、哪天花得最多，就没法算了。

所以这一章要给每一笔账加上日期。具体来说，要做到这几件事：

1. 记账的时候，自动记下今天的日期。
2. 日期能存进 json 文件，下次还能读回来。
3. 算出「7 天前」是哪一天。
4. 判断某一笔账是不是在最近 7 天里。
5. 显示的时候，写成「11月02日」这样好看的样子。

这些事，Python 自带的 `datetime` 模块都能做。可它到底怎么用，前面没讲过。

这回，咱们自己学。怎么学呢？下一节先说说自学一个模块的办法。

# 二、自学一个模块，分四步

其实自学一个模块的办法，第 9 章「学会用一个陌生模块」里已经用 `math.ceil` 演示过一回：先明确需求，再去文档里找，然后用正数、零和负数验证。这一章把它展开成四步：

1. **列需求**：用大白话写清楚要做什么。上一节已经列好了。
2. **找文档**：去官方文档找到这个模块的那一页，先看目录，知道它大概有哪些东西。
3. **小步试**：用 `dir()` 看看有哪些方法，用 `help()` 看说明，每个方法写两三行代码试一试。
4. **用边界验证**：拿特殊的值去试，比如月底、年底、闰年，看结果是不是和你想的一样。

第一步上一节已经做完了，接下来做第二步：找文档。`datetime` 模块的官方中文文档在这里：[datetime --- 基本日期和时间类型](https://docs.python.org/zh-cn/3/library/datetime.html) 。

这一页很长，别想着从头读到尾。先看开头的介绍和目录，能找到这几个名字：

- `date` ：日期，年、月、日。
- `time` ：一天里的时间，时、分、秒。
- `datetime` ：日期加时间。
- `timedelta` ：两个日期或时间之间的差，比如「7 天」。

四个名字里，该先看哪个呢？记账只关心哪一天，不关心几点几分，所以先盯住 `date` 。这就到了第三步，先用 `dir()` 看看它都有些什么：

```python
from datetime import date

print([name for name in dir(date) if not name.startswith('_')])
```

输出的结果：

```
['ctime', 'day', 'fromisocalendar', 'fromisoformat', 'fromordinal', 'fromtimestamp', 'isocalendar', 'isoformat', 'isoweekday', 'max', 'min', 'month', 'replace', 'resolution', 'strftime', 'timetuple', 'today', 'toordinal', 'weekday', 'year']
```

代码里那一行列表生成式，是干什么的呢？因为 `dir()` 列出来的名字里，有一大堆以下划线开头的，那是 Python 内部用的。所以这里用第 7 章的列表生成式，把它们筛掉了。

筛完还剩二十个名字。要全学吗？不用。对着上一节列的需求，挑出看着有关系的就行：

| 需求 | 看着有关系的名字 |
|---|---|
| 拿到今天的日期 | `today` |
| 存进文件、再读回来 | `isoformat` 、`fromisoformat` |
| 年、月、日 | `year` 、`month` 、`day` |
| 星期几 | `weekday` 、`isoweekday` |
| 显示成好看的样子 | `strftime` |

那「7 天前」这个需求呢？`date` 里没有看着像的名字。不过别忘了，文档目录里还有 `timedelta` ，名字里的 delta 就是「差值」的意思，应该就是它了。

清单列好了，接下来就照着它，一个一个地试。

# 三、今天是几号？

清单上的第一个需求，是拿到今天的日期，所以先试 `today` 。看看说明书怎么说：

```python
from datetime import date

help(date.today)
```

说明书的主要内容是这样的：

```
today(...) class method of datetime.date
    Current date or datetime:  same as self.__class__.fromtimestamp(time.time()).
```

说明书里的 `Current date` ，就是当前的日期。文档里写得更直白：返回当前的本地日期。到底是不是这样，试一下就知道了：

```python
from datetime import date

print(date.today())
print(type(date.today()))
```

输出的结果（第一行是你运行那天的日期）：

```
2026-11-02
<class 'datetime.date'>
```

再看第二行：拿到的不是字符串，而是一个 `date` 对象。

不过有个问题：`date.today()` 每天运行的结果都不一样，拿来做例子不方便。所以下面的例子，都用 `date(年, 月, 日)` 创建一个固定的日期。这种写法，第 9 章见过：

```python
from datetime import date

d = date(2026, 11, 2)
print(d)
print(d.year, d.month, d.day)
```

输出的结果：

```
2026-11-02
2026 11 2
```

从输出可以看到，用 `d.year` 、`d.month` 、`d.day` ，就能分别拿到年、月、日。

日期拿到了，接下来看清单上的「存进文件、再读回来」。实战 5 说过，json 只认数字、字符串、列表、字典这些东西。那日期该怎么存呢？可以先把日期变成字符串存进去，读回来的时候，再变回日期。

清单里的 `isoformat()` 和 `fromisoformat()` ，名字刚好是一对，看着就像是干这个的。先看一眼 `fromisoformat()` 的说明：

```python
from datetime import date

help(date.fromisoformat)
```

说明书的主要内容是这样的：

```
fromisoformat(...) class method of datetime.date
    str -> Construct a date from a string in ISO 8601 format.
```

开头的 `str ->` ，意思是给它一个字符串，它造出一个日期。那要什么样的字符串呢？后面写着：ISO 8601 格式。ISO 8601 是一种国际通用的日期写法，就是 `2026-11-02` 这样的「年-月-日」。

说明看懂了，就动手试一试，看日期能不能变成字符串，再变回来：

```python
from datetime import date

d = date(2026, 11, 2)
text = d.isoformat()
print(text, type(text))

back = date.fromisoformat(text)
print(back, type(back))
print(back == d)
```

输出的结果：

```
2026-11-02 <class 'str'>
2026-11-02 <class 'datetime.date'>
True
```

对照三行输出来看：

- 第一行：`isoformat()` 把日期变成了字符串 `'2026-11-02'` 。
- 第二行：`fromisoformat()` 再把它变回了日期。
- 第三行：`True` 说明，变回来的日期和原来的一模一样。

这样一来，存文件的问题就解决了。清单上接下来是「7 天前是哪一天」，下一节接着试。

# 四、7 天前是哪天？

第二节猜过，「7 天前」这个需求要靠 `timedelta` 。文档里它的样子是 `timedelta(days=0, seconds=0, ...)` ，参数一长串，咱们只用得到 `days` 。

猜一下：日期减去 `timedelta(days=7)` ，是不是就是 7 天前？试试：

```python
from datetime import date, timedelta

d = date(2026, 11, 2)
print(d - timedelta(days=7))
print(d + timedelta(days=30))
```

输出的结果：

```
2026-10-26
2026-12-02
```

猜对了。而且加 30 天的时候，它自己知道 11 月只有 30 天，算到了 12 月 2 日，不用咱们操心每个月有几天。

不过，只试一两个普通的日期，还不够放心。这就到了四步里的第四步：用边界验证。日期最容易出错的就是月底、年底和闰年，挑几个试试：

```python
from datetime import date, timedelta

print(date(2026, 3, 1) - timedelta(days=1))
print(date(2028, 3, 1) - timedelta(days=1))
print(date(2026, 12, 31) + timedelta(days=1))
```

输出的结果：

```
2026-02-28
2028-02-29
2027-01-01
```

一行一行看：2026 年不是闰年，3 月 1 日的前一天是 2 月 28 日。2028 年是闰年，前一天就是 2 月 29 日。年底再加一天，自动跨到了下一年。三个都对。

日期减去几天，得到的还是日期。那反过来，两个日期相减，得到的又是什么呢？

```python
from datetime import date

gap = date(2026, 12, 25) - date(2026, 11, 2)
print(gap)
print(type(gap))
print(gap.days)
```

输出的结果：

```
53 days, 0:00:00
<class 'datetime.timedelta'>
53
```

看第二行就知道，两个日期相减，得到的也是一个 `timedelta` 。要拿到相差几天，用它的 `.days` ，也就是第三行的 `53` 。

再看清单上的下一个需求：判断某一笔账是不是在最近 7 天里。这要用到日期的另一个本事：日期之间还能直接比大小，越晚的越大：

```python
from datetime import date, timedelta

today = date(2026, 11, 2)
week_ago = today - timedelta(days=7)
print(date(2026, 10, 30) >= week_ago)
print(date(2026, 10, 20) >= week_ago)
```

输出的结果：

```
True
False
```

代码先算出 7 天前是哪天，再拿两个日期和它比。10 月 30 日在最近 7 天里，10 月 20 日不在。这样一来，「判断某一笔账是不是在最近 7 天里」，这个需求也解决了。

日期的加减和比较都试过了，先做一道练习：读入两个日期，算出它们相差几天。

# 五、显示成「11月02日」

清单上的需求，只剩最后一个了：显示得好看一点。`2026-11-02` 这样的写法，给程序看正合适，给人看就有点生硬。想显示成「11月02日」，要用 `strftime()` 。

这个名字有点怪，拆开来看就好懂了：str 是字符串，f 是 format（格式），time 是时间，合起来就是「按格式把时间变成字符串」。

那它怎么用呢？它要一个格式字符串，里面用 `%` 开头的代码，来代表年、月、日：

```python
from datetime import date

d = date(2026, 11, 2)
print(d.strftime('%m月%d日'))
print(d.strftime('%Y年%m月%d日'))
print(d.strftime('%Y/%m/%d'))
```

输出的结果：

```
11月02日
2026年11月02日
2026/11/02
```

对照输出，就能看出规律：`%Y` 换成四位的年份，`%m` 换成两位的月份，`%d` 换成两位的日。其他的字符，比如「月」「日」和 `/` ，都原样保留。

这些代码都是从哪儿查到的？文档里有一张专门的表：[strftime() 和 strptime() 格式代码](https://docs.python.org/zh-cn/3/library/datetime.html#format-codes) 。几个最常用的是这样写的：

| 代码 | 文档里的说明 | 例子 |
|---|---|---|
| `%Y` | 十进制数表示的带世纪的年份 | 2026 |
| `%m` | 补零后，以十进制数显示的月份 | 01、02、……、12 |
| `%d` | 补零后，以十进制数显示的月份中的一天 | 01、02、……、31 |

「补零」的意思是不够两位就在前面补个 0，所以 2 日显示成 `02` 。

不用把这张表背下来。要用的时候，打开文档查一下就行。查文档这件事，本来就是写程序的日常。

下面做一道练习，把日期显示成「11月02日 星期一」的样子。星期几怎么算，第七节才会细讲，做题时卡住了，可以先看看题目的提示。

# 六、常见坑

日期的几样本事都试过了。不过日期这东西看着简单，坑可不少，下面这五个都很常见。

## 1、日期直接存进 json

<!-- skip-ci -->
```python
import json
from datetime import date

print(json.dumps({'item': '奶茶', 'date': date(2026, 11, 2)}, ensure_ascii=False))
```

报错信息的最后一行是：

```
TypeError: Object of type date is not JSON serializable
```

报错里的 `not JSON serializable` ，意思是没法变成 JSON。因为 json 只认数字、字符串、列表、字典这些，不认 `date` 对象。

所以存之前，先用 `isoformat()` 把日期变成字符串；读回来以后，再用 `date.fromisoformat()` 变回日期。这就是第三节的做法。

## 2、%m 写成了 %M

```python
from datetime import date

d = date(2026, 11, 2)
print(d.strftime('%Y-%m-%d'))
print(d.strftime('%Y-%M-%d'))
```

输出的结果：

```
2026-11-02
2026-00-02
```

月份怎么成了 `00` ？

查一下第五节说的格式代码表就明白了：小写的 `%m` 是月份，大写的 `%M` 是**分钟**。`date` 只有日期，没有时间，所以分钟就是 0。

大小写不一样，意思完全不一样，而且不报错，又是一个安安静静的 bug。拿不准的时候，就去查表。

## 3、拿字符串比日期的早晚

```python
print('2026-11-10' > '2026-11-9')
print('2026-11-10' > '2026-11-09')
```

输出的结果：

```
False
True
```

11 月 10 日明明比 9 日晚，第一行怎么是 `False` ？

因为这是在比两个字符串。字符串是一个字符一个字符地比，比到第 9 个字符，`'1'` 比 `'9'` 小，结果就定了，后面的根本不看。

那第二行为什么又对了呢？因为它把 9 日写成了补零的 `09` ，两个字符串一样长，比出来才碰巧是对的。所以别拿字符串比日期，先用 `date.fromisoformat()` 变成日期再比。

## 4、fromisoformat() 很挑格式

<!-- skip-ci -->
```python
from datetime import date

print(date.fromisoformat('2026-11-9'))
```

报错信息的最后一行是：

```
ValueError: Invalid isoformat string: '2026-11-9'
```

问题出在 9 日只写了一位。这个函数要求月和日都写满两位，写成 `2026-11-09` 才行。所以读用户输入的日期时，要提醒用户按 `2026-11-09` 这样的格式输入。

## 5、例子里用 today()，每天结果都不一样

`date.today()` 今天运行是今天的日期，明天运行就变了。写程序、做测试的时候，要是用它，今天对的结果，明天就可能不对了。

所以测试和例子里，用 `date(2026, 11, 2)` 这样的固定日期；真正记账的时候，再用 `date.today()` 。这一章的例子，就是这么做的。

坑看完了，先做一道练习：把带日期的账存成 json，再读回来，正好绕开第一个坑。

# 七、自己查一次文档

第一节列的需求都解决了，这一节再查一个新问题：想在明细里显示「星期几」，该用哪个名字？第二节挑名字的时候，有两个看着都像：`weekday` 和 `isoweekday` 。它们有什么区别呢？

老办法，先问 `help()` ：

```python
from datetime import date

help(date.weekday)
```

说明书的主要内容是这样的：

```
weekday(...) unbound datetime.date method
    Return the day of the week represented by the date.
    Monday == 0 ... Sunday == 6
```

说明的最后一行写得很清楚：星期一是 0，星期天是 6。再去文档里看看 [isoweekday()](https://docs.python.org/zh-cn/3/library/datetime.html#datetime.date.isoweekday) ，文档写着：返回一个整数代表星期几，星期一为 1，星期天为 7。

原来两个都表示星期几，只是起点不一样。文档是这么说的，咱们还得自己验证一下。拿一个知道是星期几的日期来试：2026 年 11 月 2 日是星期一。

```python
from datetime import date

d = date(2026, 11, 2)
print(d.weekday(), d.isoweekday())
```

输出的结果：

```
0 1
```

同一个星期一，一个是 0，一个是 1，和文档说的一样。

不过，查到这里还没完。再翻到第五节那张格式代码表，里面还有一个 `%w` ，文档的说明是：以十进制数显示的工作日，其中 0 表示**星期日**，6 表示星期六。

这么一来，同一个模块里，就有了三种「星期几」，三种算法。放在一起看：

| 写法 | 星期一 | 星期日 |
|---|---|---|
| `weekday()` | 0 | 6 |
| `isoweekday()` | 1 | 7 |
| `strftime('%w')` | 1 | 0 |

要是没查文档，凭感觉混着用，算出来的星期几就会对不上。这就是为什么要查文档，还要拿一个知道答案的例子来验证。

区别弄清楚了，现在动手：用 `weekday()` 配一个列表，把日期显示成「星期一」这样的中文。各位童鞋不妨先自己想一想怎么写。

想好了再往下看：

```python
from datetime import date

names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
for d in [date(2026, 11, 2), date(2026, 11, 8)]:
    print(d.strftime('%m月%d日'), names[d.weekday()])
```

输出的结果：

```
11月02日 星期一
11月08日 星期日
```

为什么选 `weekday()` 呢？因为它正好从 0 开始，可以直接当列表的下标用：星期一是 0，取到的就是列表里的第一个「星期一」。

最后再顺手解决一个问题：这一周的星期一是哪天？下一节的记账本要算「这个星期」花了多少，就用得上它。思路是这样的：`d.weekday()` 就是从星期一算起已经过了几天，往回减这么多天就行：

```python
from datetime import date, timedelta

d = date(2026, 11, 5)
monday = d - timedelta(days=d.weekday())
print(monday)
```

输出的结果：

```
2026-11-02
```

11 月 5 日这一周的星期一，正好是 11 月 2 日。查到的这些，下一节就用进记账本。

# 八、记账本 v5

这一章查到、试过的东西，现在都用进记账本里。和 v4 比，改动有三处：

- `add()` 多一个参数 `day` ，用 `isoformat()` 变成字符串再存，这样 `save()` 存 json 就不会出错。
- 新加 `total_since(start)` ：把每一笔的日期变回 `date` ，再和 `start` 比，算出这天以后的合计。
- 新加 `details()` ：列出每一笔，带上日期和星期几。

```python
import json
from datetime import date, timedelta


class Ledger:
    """记账本：每一笔账都带日期，可以存进文件，也能算最近几天花了多少。"""

    def __init__(self):
        self.entries = []

    def add(self, item, category, cost, day):
        """记一笔账。day 是 date 对象，存成 '2026-11-02' 这样的字符串。"""
        self.entries.append({'date': day.isoformat(), 'item': item, 'category': category, 'cost': cost})

    def total_since(self, start):
        """返回 start 这天（含）以后所有账的合计。"""
        total = 0
        for entry in self.entries:
            if date.fromisoformat(entry['date']) >= start:
                total = total + entry['cost']
        return total

    def details(self):
        """列出每一笔：日期、星期几、名称和金额。"""
        names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        for entry in self.entries:
            day = date.fromisoformat(entry['date'])
            print(f"{day.strftime('%m月%d日')} {names[day.weekday()]} {entry['item']} {entry['cost']:.2f} 元")

    def save(self, path):
        """把整本账存成 json 文件。"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def load(self, path):
        """从 json 文件读回整本账。"""
        with open(path, encoding='utf-8') as f:
            self.entries = json.load(f)


book = Ledger()
book.add('奶茶', '餐饮', 12.5, date(2026, 10, 20))
book.add('午饭', '餐饮', 25, date(2026, 10, 30))
book.add('地铁', '交通', 4, date(2026, 11, 2))
book.save('dated_ledger.json')

again = Ledger()
again.load('dated_ledger.json')
again.details()

today = date(2026, 11, 2)
print(f'最近 7 天：{again.total_since(today - timedelta(days=6)):.2f} 元')
print(f'这个星期：{again.total_since(today - timedelta(days=today.weekday())):.2f} 元')
```

输出的结果：

```
10月20日 星期二 奶茶 12.50 元
10月30日 星期五 午饭 25.00 元
11月02日 星期一 地铁 4.00 元
最近 7 天：29.00 元
这个星期：4.00 元
```

先看前三行：账存进文件、再读回来以后，日期都还在，星期几也算得对。

再看最后两行。「最近 7 天」为什么减的是 6 天？因为今天也算一天：10 月 27 日到 11 月 2 日，正好 7 天。10 月 20 日的奶茶不在里面，所以是 25 加 4，一共 29 元。

「这个星期」用的是上一节的办法，从星期一，也就是 11 月 2 日算起，只有地铁那一笔。

上面为了让结果固定，日期都是写死的。真正记账的时候，日期就用今天。把实战 5 主程序里记账的那一行改成：

<!-- skip-ci -->
```python
book.add(item, category, read_cost(), date.today())
```

每一笔账就自动记上了当天的日期。

最后做一道练习：自己动手，给 `Ledger` 写出 `total_since(start)` 这个方法。

# 九、小结与回看

这一章没有人手把手地教，咱们靠自己，学会了 `datetime` 里最常用的几样东西：

- `date(年, 月, 日)` 创建日期，`date.today()` 拿到今天。
- `isoformat()` 把日期变成 `'2026-11-02'` 这样的字符串，`date.fromisoformat()` 再变回来；存 json 前先变成字符串。
- 日期加减用 `timedelta(days=7)` ，月底、年底、闰年都不用自己操心。两个日期相减，用 `.days` 拿到相差几天。日期之间还可以直接比早晚。
- `strftime()` 按格式显示日期：`%Y` 年、`%m` 月、`%d` 日；大写的 `%M` 是分钟。
- `weekday()` 星期一是 0，`isoweekday()` 星期一是 1，`%w` 星期日是 0。

不过，比这些写法更重要的，是自学一个模块的四步：

1. **列需求**：用大白话写清楚要做什么。
2. **找文档**：找到模块的那一页，先看目录。
3. **小步试**：`dir()` 看有什么，`help()` 看说明，每个方法写两三行试一试。
4. **用边界验证**：月底、年底、闰年、空的、零……拿特殊的值去试，再拿一个知道答案的例子核对。

哪里卡住了，就回去看一看：

- 「学会用一个陌生模块」和「几个常用的标准库」：第 9 章
- json 的 `dump()` 、`load()` ：实战 5 的「四、换成 json 试试」
- 列表生成式：第 7 章

回头看看这六个实战章：从实战 1 一个只会问「花了多少钱」的 v0，到现在带日期、能存档、能按天汇总的 v5，记账本一点一点长大，你也一点一点地，把学过的东西变成了自己会用的东西。

往后学的模块会越来越多，大多数都没有人手把手地教。可只要会这四步，碰到哪个都不用怕：先列需求，再找文档，小步地试，用边界验证。

基础部分的实战到这里就告一段落了。接下来的第 10 章开始进入进阶内容，学的东西会更抽象一些。学的时候，不妨也像这样，时不时停下来，用新学的东西给记账本加个小功能。
