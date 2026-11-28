# 实战 4：同一个记账本写三遍

# 前言

前面两章，咱们学了迭代和面向对象。学了新东西，先别急着往下赶，回头看看一直在写的记账本。

记账本写到 v1.1，已经能用了，输错了也不怕。可回头看看代码，各位童鞋是不是觉得它越来越长，读起来也越来越费劲？想加个新功能，得在一大段代码里来回找地方，生怕改了这里，又弄坏了那里。

有这种感觉很正常。因为程序能跑，只是第一步；写得好读、好改，才是下一步。

所以这一章不加什么大功能，咱们把**同一个记账本，换两种写法再写一遍**：先拆成几个函数，做成 v2；再写成一个类，做成 v3。功能一模一样，代码的样子却会大不相同。

这种「功能不变，只改写法」的活儿，有个专门的名字，叫**重构**。别小看它，写程序的人花在重构上的时间，一点都不比写新功能少。

一开始你可能会觉得：程序能跑不就行了，何必这么折腾？没关系，先跟着写一遍。等写完这一章，再回头看看 v1.1，你大概就不这么想了。

**学这一章之前**，需要先学完 [实战 3](06b-practice-3-debugging.md) 的记账本 v1.1，以及 [第 7 章](07-iteration.md) 的列表生成式、[第 8 章](08-oop.md) 的类、`__init__` 、实例属性和类属性。

# 目录

这一章会学到：

- 一、v1.1 越来越难改了——一大段代码挤在一起
- 二、v2：拆成几个函数——每个函数只做一件事
- 三、加个新功能试试——只加一个函数，别的都不用动
- 四、v3：写成一个类——数据和操作放在一起
- 五、三种写法比一比——什么时候用哪一种
- 六、常见坑
- 七、自己查一次文档——给自己的代码写说明书
- 八、记账本 v3
- 九、小结与回看

学完这一章，你能把一段长代码拆成函数、再写成类，也能说清楚三种写法各适合什么时候用。

# 一、v1.1 越来越难改了

要说清楚为什么要重构，先得看看现在的代码到底哪里不好。咱们回头看看实战 3 的记账本 v1.1。`read_cost()` 这个函数先放在一边，剩下的主程序是这样的：

<!-- skip-ci -->
```python
entries = []
print('输入「完」结束记账')
while True:
    item = input('买了什么：').strip()
    if item == '完':
        break
    category = input('类别：').strip()
    cost = read_cost()
    entries.append({'item': item, 'category': category, 'cost': cost})

total = 0
totals = {}
for entry in entries:
    total = total + entry['cost']
    totals[entry['category']] = totals.get(entry['category'], 0) + entry['cost']

for category, money in totals.items():
    print(f'{category}：{money:.2f} 元')
if len(entries) == 0:
    print('今天还没有记账')
else:
    print(f'一共 {len(entries)} 笔，合计 {total:.2f} 元，平均每笔 {total / len(entries):.2f} 元')
```

二十来行代码，从上到下一口气写下来。现在只有二十来行，还算凑合。可要是再加几个功能呢？比如下面这三个：

- 汇总之前，先把每一笔的明细列出来。
- 找出今天最大的一笔开销。
- 同时管两本账：自己的一本，家里的一本。

每加一个功能，都得在这一大段里找地方插进去。而且 `total` 、`totals` 、`category` 这些变量，上面在用，下面也在用。改的时候，心里难免直打鼓：这一处改了，别的地方会不会跟着出问题？

那么，问题到底出在哪儿呢？仔细看看，这一大段其实干了三件事：**读输入、记账、汇总**。三件事搅在一起，所以既难读，也难改。

既然是三件事，能不能把它们分开，各写各的呢？下一节就来试试。

# 二、v2：拆成几个函数

要把几件事分开，用什么工具呢？答案是早就学过的函数。

第 6 章学函数的时候，说的是：函数把一段代码包起来、起个名字，就可以反复用。其实函数还有一个同样重要的用处：**把一件事和别的事隔开**。

那就按上一节说的三件事，拆成三个函数。每个函数做什么、要传进去什么、交回来什么，先在这张表里列清楚：

| 函数 | 做什么 | 要传进去什么 | 交回来什么 |
|---|---|---|---|
| `read_entries()` | 一直问，直到输入「完」 | 什么都不用 | 记好的账，一个列表 |
| `totals_by_category(entries)` | 按类别汇总 | 账的列表 | 类别对应金额的字典 |
| `print_report(entries)` | 打印汇总 | 账的列表 | 什么都不交，只管打印 |

三个函数里，咱们先写汇总。它只管算，不管账是怎么来的：

```python
def totals_by_category(entries):
    totals = {}
    for entry in entries:
        category = entry['category']
        totals[category] = totals.get(category, 0) + entry['cost']
    return totals


entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
    {'item': '午饭', 'category': '餐饮', 'cost': 25},
]
print(totals_by_category(entries))
```

输出的结果：

```
{'餐饮': 37.5, '交通': 4}
```

注意最后一行：这回不用一笔一笔地输入，而是直接拿上面写好的列表来试。为什么能这样试呢？因为函数拆出来以后，每一块都能单独拿出来试。这是拆函数最大的好处之一。

汇总有了，还差一个合计。合计当然也能写个循环，一笔一笔地加，不过还有更省事的办法：Python 自带一个求和的函数 `sum()` ，配上第 7 章学的列表生成式，一行就能算出来：

```python
entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
    {'item': '午饭', 'category': '餐饮', 'cost': 25},
]
print([entry['cost'] for entry in entries])
print(sum([entry['cost'] for entry in entries]))
```

输出的结果：

```
[12.5, 4, 25]
41.5
```

对照两行输出，就能看出这一句分成了两步：

- 列表生成式先把每一笔的金额取出来，组成一个新列表，也就是第一行的 `[12.5, 4, 25]` 。
- `sum()` 再把列表里的数加起来，得到第二行的 `41.5` 。

原来要写一个 `for` 循环才能算出的合计，现在一行就够了。

汇总和合计都有了。剩下的读输入和打印汇总，下一节也包成函数，拼出完整的 v2。在那之前，先做一道练习：仿照上面的汇总函数，按类别数一数，每一类各记了几笔。

# 三、加个新功能试试

上一节写好了汇总。现在把读输入和打印汇总也包成函数，再加上实战 3 写过的 `read_cost()` ，拼在一起，记账本 v2 就是这样的：

<!-- skip-ci -->
```python
def read_cost():
    while True:
        text = input('花了多少钱：').strip()
        if text.replace('.', '', 1).isdigit():
            return float(text)
        print('请输入数字，比如 12 或 12.5')


def read_entries():
    entries = []
    print('输入「完」结束记账')
    while True:
        item = input('买了什么：').strip()
        if item == '完':
            break
        category = input('类别：').strip()
        cost = read_cost()
        entries.append({'item': item, 'category': category, 'cost': cost})
    return entries


def totals_by_category(entries):
    totals = {}
    for entry in entries:
        category = entry['category']
        totals[category] = totals.get(category, 0) + entry['cost']
    return totals


def print_report(entries):
    if len(entries) == 0:
        print('今天还没有记账')
        return
    for category, money in totals_by_category(entries).items():
        print(f'{category}：{money:.2f} 元')
    total = sum([entry['cost'] for entry in entries])
    print(f'一共 {len(entries)} 笔，合计 {total:.2f} 元，平均每笔 {total / len(entries):.2f} 元')


entries = read_entries()
print_report(entries)
```

输出的结果：

```
输入「完」结束记账
买了什么：奶茶
类别：餐饮
花了多少钱：12.5
买了什么：地铁
类别：交通
花了多少钱：4
买了什么：午饭
类别：餐饮
花了多少钱：25
买了什么：完
餐饮：37.50 元
交通：4.00 元
一共 3 笔，合计 41.50 元，平均每笔 13.83 元
```

这段代码里，有一处值得多看一眼：`print_report()` 里那个单独的 `return` 。它后面什么都没跟，作用是提前结束函数。一笔账都没有的时候，打印一句「今天还没有记账」就走，下面的汇总都不用做了。

再从整体上看一看。功能和 v1.1 一模一样，代码却分成了四块，也就是四个函数。真正的主程序，只有最后两行：

<!-- skip-ci -->
```python
entries = read_entries()
print_report(entries)
```

这两行读起来就像一本书的目录：先读账，再打印汇总。想知道某一步具体是怎么做的，再翻到对应的函数去看。

拆成这样，到底好在哪儿呢？光说不算，咱们加个新功能试试。第一节列过的三个功能，先做第一个：汇总之前，先把每一笔的明细列出来。

要是在 v1.1 里，就得在那一大段中间找地方插进去。在 v2 里呢？只要新写一个函数就行：

```python
def print_details(entries):
    number = 0
    for entry in entries:
        number = number + 1
        print(f"{number}. {entry['item']}（{entry['category']}）{entry['cost']:.2f} 元")


entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
]
print_details(entries)
```

输出的结果：

```
1. 奶茶（餐饮）12.50 元
2. 地铁（交通）4.00 元
```

和上一节一样，先拿写好的两笔账单独试一试，明细列得没问题。接着把它放进主程序，主程序就变成了三行：

<!-- skip-ci -->
```python
entries = read_entries()
print_details(entries)
print_report(entries)
```

再回头看看，原来的 `read_entries()` 、`totals_by_category()` 、`print_report()` ，一行都没动。加功能只是多加一个函数，不用担心把别的地方改坏，这就是拆函数的好处。

第一节列的第二个功能，是找出今天最大的一笔开销。下面这道练习，就用同样的办法，再给 v2 加一个函数，把它做出来。

# 四、v3：写成一个类

写到这里，v2 已经清爽多了。不过，各位童鞋有没有注意到一件事：`totals_by_category(entries)` 、`print_report(entries)` 、`print_details(entries)` ，每个函数都要把 `entries` 传进去。

为什么每次都得传呢？因为账放在函数外面，函数要用，就只能从外面递进来。可仔细想想，账（数据）和处理账的函数（操作），其实是分不开的一对。那么，能不能干脆把它们放到一起？

能。第 8 章学的类，干的就是这件事。咱们把「一本账」写成一个类：

```python
class Ledger:
    def __init__(self):
        self.entries = []

    def add(self, item, category, cost):
        self.entries.append({'item': item, 'category': category, 'cost': cost})

    def total(self):
        return sum([entry['cost'] for entry in self.entries])


book = Ledger()
book.add('奶茶', '餐饮', 12.5)
book.add('午饭', '餐饮', 25)
print(len(book.entries))
print(book.total())
```

输出的结果：

```
2
37.5
```

这个类里一共有三个方法，咱们一个一个来看：

- `__init__()` 是初始化函数，每创建一本账，就给它准备一个空列表 `self.entries` 。
- `add()` 记一笔账。以前要写 `entries.append({...})` ，现在说一句 `book.add('奶茶', '餐饮', 12.5)` 就行，用起来更像在说话：往这本账里加一笔。
- `total()` 算合计。它要的账就在 `self.entries` 里，不用再从外面传进来。

数据和操作放在一起，还有一个好处。还记得第一节想加的第三个功能吗？同时管两本账：自己的一本，家里的一本。写成类以后，就可以同时有好几本账，各记各的，互不干扰：

```python
class Ledger:
    def __init__(self):
        self.entries = []

    def add(self, item, category, cost):
        self.entries.append({'item': item, 'category': category, 'cost': cost})

    def total(self):
        return sum([entry['cost'] for entry in self.entries])


mine = Ledger()
home = Ledger()
mine.add('奶茶', '餐饮', 12.5)
home.add('买菜', '餐饮', 58)
home.add('水电费', '生活', 120)
print(f'我的账本：{mine.total():.2f} 元')
print(f'家庭账本：{home.total():.2f} 元')
```

输出的结果：

```
我的账本：12.50 元
家庭账本：178.00 元
```

两本账为什么不会混在一起呢？因为 `mine` 和 `home` 是同一个类创建出来的两个对象。第 8 章讲过，`self.entries` 是实例属性，每个对象都有自己的一份，所以两本账互不影响。

反过来想一想，要是用 v2 的写法来管两本账，就得准备两个列表，每次调用函数都得小心，别把列表传错了。写成类以后，就不用操这个心了：`mine.add()` 只会记进我的账本，不可能跑到家庭账本里去。

类写好了，先做一道练习：给 `Ledger` 再加一个方法，算出平均每笔花了多少钱。

# 五、三种写法比一比

写到这里，同一个记账本已经有了三种写法：v1.1 一整段，v2 拆成函数，v3 写成类。很多童鞋会想：「是不是越往后越好，以后都该写成类？」

还真不是。三种写法各有各的用处，放在一张表里比一比：

| 写法 | 样子 | 适合什么时候 |
|---|---|---|
| v1.1 一整段 | 从上到下一口气写完 | 几十行以内、用一次就扔的小脚本 |
| v2 拆成函数 | 每件事一个函数，主程序像目录 | 代码变长了，有几件事要分开写、分开试 |
| v3 写成类 | 数据和操作放在一起 | 一份数据配着好几个操作，还可能同时要好几份 |

光看表可能有点抽象，还是拿记账本来说：

- 只是临时算一下今天花了多少，像 v1.1 那样写完全没问题，硬拆成类反而啰嗦。
- 功能多起来以后，拆成函数，每一块都能单独试，加功能也不容易改坏别的地方。
- 要同时管好几本账，或者账本还要存进文件、再读出来，写成类最顺手。

所以重构不是为了显得「高级」，而是为了让代码配得上它要干的事。那么，怎么判断该不该重构呢？可以问自己两个问题：

1. 下次再加功能的时候，我能很快找到该改哪里吗？
2. 改了一处，我有把握别的地方不会跟着出问题吗？

只要有一个答案是「不能」，就该动手了。

动手重构的时候，还有一点很重要：**重构前后，功能要一模一样**。怎么保证呢？每改一步，就用同样的输入运行一遍，看看输出和原来是不是完全一致。一次改一点，改完就试，这和实战 3 改 bug 的道理是一样的。

道理讲完了。不过，不管是拆函数还是写成类，都有几个坑特别容易踩，下一节一个一个来看。

# 六、常见坑

下面四个坑，前三个出在写类的时候，最后一个出在拆函数的时候。写 v2、v3 的时候要是出了错，可以先对照着看看。

## 1、方法忘了写 self

<!-- skip-ci -->
```python
class Ledger:
    def __init__(self):
        self.entries = []

    def add(item, category, cost):
        self.entries.append({'item': item, 'category': category, 'cost': cost})


book = Ledger()
book.add('奶茶', '餐饮', 12.5)
```

报错信息的最后一行是：

```
TypeError: Ledger.add() takes 3 positional arguments but 4 were given
```

明明只传了 3 个参数，怎么说给了 4 个？

因为 `book.add('奶茶', '餐饮', 12.5)` 调用的时候，Python 会自动把 `book` 自己当成第一个参数传进去，再加上括号里的 3 个，一共就是 4 个。所以方法定义的第一个参数，必须留给它，也就是 `self` 。少写了 `self` ，参数就对不上了。

## 2、方法里忘了写 self.

<!-- skip-ci -->
```python
class Ledger:
    def __init__(self):
        self.entries = []

    def add(self, item, category, cost):
        entries.append({'item': item, 'category': category, 'cost': cost})


book = Ledger()
book.add('奶茶', '餐饮', 12.5)
```

报错信息的最后一行是：

```
NameError: name 'entries' is not defined. Did you mean: 'self.entries'?
```

明明 `__init__()` 里写了 `self.entries = []` ，怎么说 `entries` 没定义？

因为 `entries` 是这本账自己的属性，在方法里要写成 `self.entries` 。只写 `entries` ，Python 会去找一个叫 `entries` 的普通变量，当然找不到。好在 Python 已经猜到了你想写什么，`Did you mean` 后面给出的就是答案。

## 3、账本写成了类属性，两本账记到了一起

```python
class Ledger:
    entries = []

    def add(self, item, category, cost):
        self.entries.append({'item': item, 'category': category, 'cost': cost})


mine = Ledger()
home = Ledger()
mine.add('奶茶', '餐饮', 12.5)
home.add('买菜', '餐饮', 58)
print(len(mine.entries))
print(len(home.entries))
```

输出的结果：

```
2
2
```

我的账本只记了一笔，家庭账本也只记了一笔，怎么都变成了 2 笔？

因为 `entries = []` 写在了类里面、方法外面，成了**类属性**。第 8 章讲过，类属性是所有对象共用的一份。`mine` 和 `home` 往里面加的，其实是同一个列表。

这个坑比前两个更麻烦：它不报错，两本账就这么悄悄地混在了一起。那该怎么改呢？把它放进 `__init__()` ，写成 `self.entries = []` ，让每一本账在创建的时候，都有自己的一个列表。

## 4、函数只打印，没有返回

<!-- skip-ci -->
```python
def total_of(entries):
    total = 0
    for entry in entries:
        total = total + entry['cost']
    print(total)


entries = [{'item': '奶茶', 'cost': 12.5}, {'item': '午饭', 'cost': 25}]
total = total_of(entries)
print(f'合计：{total:.2f} 元')
```

运行一下，`37.5` 先打印了出来，接着就报错了，最后一行是：

```
TypeError: unsupported format string passed to NoneType.__format__
```

合计明明算出来了，怎么还报错？

因为函数里把合计 `print()` 了出来，看着像是「给出了结果」，可它没有 `return` 。没有 `return` 的函数，返回的是 `None` 。所以 `total` 拿到的其实是 `None` ，`None` 当然没法按 `:.2f` 显示。第 6 章「打印出来了，为什么还拿到 None」说的就是这个坑。

拆函数的时候记住：**算结果的函数用 `return` 交出结果，打印交给调用它的地方去做**。

# 七、自己查一次文档

坑都看完了，这一节换个话题，来查一次文档。

前几章，咱们一直在用 `help()` 查 Python 自带函数的说明书。那么，自己写的类，能不能也有一份说明书呢？

当然能。第 6 章讲函数的时候提过一句：函数的第一行，可以写一段「文档字符串」，用来存放函数的说明。类也一样。

咱们先给 `Ledger` 写上说明。写法很简单：用三个引号把说明括起来，放在类和方法的第一行。写好以后，再用 `help()` 看一看：

```python
class Ledger:
    """记账本：记下每一笔账，再按类别汇总。"""

    def __init__(self):
        self.entries = []

    def add(self, item, category, cost):
        """记一笔账。cost 是金额，单位是元。"""
        self.entries.append({'item': item, 'category': category, 'cost': cost})

    def total(self):
        """返回所有账的合计。"""
        return sum([entry['cost'] for entry in self.entries])


help(Ledger)
```

输出的结果：

```
Help on class Ledger in module __main__:

class Ledger(builtins.object)
 |  记账本：记下每一笔账，再按类别汇总。
 |
 |  Methods defined here:
 |
 |  __init__(self)
 |
 |  add(self, item, category, cost)
 |      记一笔账。cost 是金额，单位是元。
 |
 |  total(self)
 |      返回所有账的合计。
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables
 |
 |  __weakref__
 |      list of weak references to the object
```

是不是有点眼熟？这和 `help(input)` 、`help(str.isdigit)` 是同一个样子。原来，我们一直查的说明书，就是别人写在代码里的文档字符串。

再细看这份说明书。前半部分来自咱们自己写的代码：类的说明，还有每个方法的参数和说明。最后 `Data descriptors` 那一段，是 Python 自动给每个类加上的，现在先不用管。

那么，`help()` 是从哪儿拿到这些说明的呢？去官方文档查一查，文档字符串到底是什么：[术语表 docstring](https://docs.python.org/zh-cn/3/glossary.html#term-docstring) 。文档里说，它是出现在类、函数或模块里的第一个字符串，会被放进它们的 `__doc__` 属性里。

文档是这么说的，可到底是不是这样呢？写几行代码试一试：

```python
class Ledger:
    """记账本：记下每一笔账，再按类别汇总。"""

    def add(self, item, category, cost):
        """记一笔账。cost 是金额，单位是元。"""


print(Ledger.__doc__)
print(Ledger.add.__doc__)
```

输出的结果：

```
记账本：记下每一笔账，再按类别汇总。
记一笔账。cost 是金额，单位是元。
```

两句说明原样打印了出来，文档说得没错。`help()` 显示的说明，就是从 `__doc__` 里取出来的。

所以，写函数和类的时候，顺手在第一行写一句说明：它是做什么的，参数是什么意思。过几个月再回来看自己的代码，或者别人用你的代码时，`help()` 一下就清楚了。下一节拼出记账本 v3，咱们就照这个习惯，给里面的函数和方法写上说明。

# 八、记账本 v3

这一章要学的都学完了，现在把它们拼起来：v2 里汇总、打印这些处理账的函数，挪进 `Ledger` 类里变成方法，再给它们写上文档字符串。记账本 v3 就是这样的：

<!-- skip-ci -->
```python
def read_cost():
    """一直问金额，直到输入的是数字，返回转换好的浮点数。"""
    while True:
        text = input('花了多少钱：').strip()
        if text.replace('.', '', 1).isdigit():
            return float(text)
        print('请输入数字，比如 12 或 12.5')


class Ledger:
    """记账本：记下每一笔账，再按类别汇总。"""

    def __init__(self):
        self.entries = []

    def add(self, item, category, cost):
        """记一笔账。cost 是金额，单位是元。"""
        self.entries.append({'item': item, 'category': category, 'cost': cost})

    def total(self):
        """返回所有账的合计。"""
        return sum([entry['cost'] for entry in self.entries])

    def average(self):
        """返回平均每笔多少钱；一笔都没有时返回 0。"""
        if len(self.entries) == 0:
            return 0
        return self.total() / len(self.entries)

    def totals_by_category(self):
        """返回一个字典：类别对应这一类的合计。"""
        totals = {}
        for entry in self.entries:
            category = entry['category']
            totals[category] = totals.get(category, 0) + entry['cost']
        return totals

    def report(self):
        """打印按类别的汇总和合计。"""
        if len(self.entries) == 0:
            print('今天还没有记账')
            return
        for category, money in self.totals_by_category().items():
            print(f'{category}：{money:.2f} 元')
        print(f'一共 {len(self.entries)} 笔，合计 {self.total():.2f} 元，平均每笔 {self.average():.2f} 元')


book = Ledger()
print('输入「完」结束记账')
while True:
    item = input('买了什么：').strip()
    if item == '完':
        break
    category = input('类别：').strip()
    book.add(item, category, read_cost())
book.report()
```

输出的结果：

```
输入「完」结束记账
买了什么：奶茶
类别：餐饮
花了多少钱：12.5
买了什么：地铁
类别：交通
花了多少钱：4
买了什么：午饭
类别：餐饮
花了多少钱：25
买了什么：完
餐饮：37.50 元
交通：4.00 元
一共 3 笔，合计 41.50 元，平均每笔 13.83 元
```

拿它和第三节的 v2 对比一下：用同样的输入运行，输出一字不差。功能没变，只是写法变了，这就是重构。

这段代码里，有一个地方要特别留意，就是 `report()` 里面的几处调用：`self.total()` 、`self.average()` 、`self.totals_by_category()` 。在一个方法里调用同一本账的其他方法，前面也要加上 `self.` 。

有的童鞋可能会嘀咕：代码怎么比 v1.1 还长了？没错，是长了一些。可每一块都很短，名字也说清了它是干什么的。要加新功能，就给 `Ledger` 加一个方法；要管两本账，就再创建一个 `Ledger()` 。

不过，记账本还有一个老毛病一直没解决：程序一关，记的账就全没了。这个问题要等学完第 9 章的模块，到实战 5 再来解决，把账存进文件里。

在那之前，先来做本章最后一道题：把第三节 v2 的 `print_details()` 函数，改写成 `Ledger` 的方法。

# 九、小结与回看

这一章没加什么大功能，只是把同一个记账本换了两种写法，重新写了一遍。回头梳理一下，学到了这几件事：

- **重构**：功能不变，只改写法。每改一步，就用同样的输入跑一遍，确认输出和原来一模一样。
- **v2 拆成函数**：一件事一个函数，主程序读起来像目录。拆出来的函数可以单独拿写好的数据来试，加功能只要加一个函数。
- **v3 写成类**：账（数据）和处理账的方法（操作）放在一起，不用到处传 `entries` ，还能同时有好几本账，互不干扰。
- 三种写法没有高低之分：小脚本写成一整段就够了；代码变长了，就拆成函数；一份数据配着好几个操作，还要好几份的时候，就写成类。
- 方法的第一个参数是 `self` ；方法里用这本账自己的东西，要写 `self.` 。
- 每本账自己的数据，放进 `__init__()` 写成实例属性；写成类属性，所有对象会共用一份。
- 算结果的函数用 `return` 交出结果，别只 `print()` 。
- 给函数和类写文档字符串，`help()` 就能显示它。

哪里卡住了，就回去看一看：

- 函数、`return` 和「打印出来了，为什么还拿到 None」：第 6 章
- 列表生成式：第 7 章「三、list 生成式（列表生成式）」
- 类、`__init__` 、实例属性和类属性：第 8 章「五、类和对象」「六、初始化函数」

其实写程序有点像写文章：先写出来，再一遍一遍地改，改到别人读得懂、自己改得动。所以第一遍写得乱一点没关系，重要的是知道怎么把它改好。

不过，记账本那个「程序一关，账就没了」的老毛病，还等着解决。接下来的第 9 章讲模块。学完之后，到了实战 5，咱们就给记账本加上一个真正有用的本事：把账存进文件，下次打开还在。
