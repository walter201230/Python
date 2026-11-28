# 实战 5：文件、csv 与 json

# 前言

前面学了模块，知道了怎么用 `import` ，把别人写好的工具拿来用。有了这个本事，就可以回头解决记账本的一个老问题了。

记账本一路写到 v3，能记、能算、能汇总，输错了也不怕。可它一直有个老毛病：程序一关，记的账就全没了。每次打开，都得从头记起。

这一章，咱们就来治好它：把账存进文件，下次打开还在。

要做到这一点，得用上两个 Python 自带的模块：`csv` 和 `json` 。那要不要先把这两个模块从头到尾背一遍呢？不用。第 9 章说过，模块不用一个一个地背，知道它能干什么，用的时候再查就行。这一章就是这么做的：带着「把账存起来」这个需求，边用边查。

先给各位童鞋打个预防针：文件读写一开始会有点绕，打开方式、编码、换行，每一样都可能出岔子。出了错也别着急，按实战 3 的办法，先看报错的最后一行，再找行号，大多数问题都能自己解决。

**学这一章之前**，需要先学完 [实战 4](08b-practice-4-ledger-rewrite.md) 的记账本 v3，以及 [第 9 章](09-modules.md) 的 `import` 和「几个常用的标准库」里的 json。

# 目录

这一章会学到：

- 一、程序一关，账就没了——变量只活在程序运行的时候
- 二、先学会读写一个文件——`open()` 、`with` 和 `encoding`
- 三、账本存成 csv——一行一笔账，表格软件也能打开
- 四、换成 json 试试——存进去是什么类型，读出来还是什么类型
- 五、常见坑
- 六、自己查一次文档——csv 文件为什么要写 `newline=''`
- 七、记账本 v4——给 `Ledger` 加上 `save()` 和 `load()`
- 八、小结与回看

学完这一章，你的记账本会把每一笔账存进文件，下次打开程序，接着上次的账往下记。

# 一、程序一关，账就没了

程序一关，账为什么就没了呢？先回顾一下实战 4 的记账本 v3：记账的时候，账都存在 `book.entries` 这个列表里。

问题就出在这儿。列表、字典这些变量，都放在电脑的**内存**里。内存有个特点：速度快，可程序一结束，里面的东西就全清空了。所以每次运行记账本，`book.entries` 都是从一个空列表开始。

那怎样才能让账留下来呢？得把它存进**文件**。文件放在硬盘上，程序关了、电脑关了，它都还在。下次打开程序，再把文件里的账读回来就行。

所以这一章要做两件事：

1. **存**：程序结束之前，把账写进文件。
2. **读**：程序开始的时候，把文件里的账读回来。

不过，在网页里运行代码，有一点要先说清楚：网页里的 Python 碰不到你电脑上的硬盘。这一章的代码在网页里写出的文件，存在浏览器临时准备的一块地方，刷新页面就没了。所以，想亲眼看到「关掉程序，下次打开账还在」，要把代码存成 `.py` 文件，在自己电脑上运行。运行以后，文件会出现在你运行程序时所在的文件夹里。

存也好，读也好，都得先学会怎么读写文件。咱们就从最简单的文本文件开始。

# 二、先学会读写一个文件

咱们先写一个文件，再把它读出来，看看都要用到哪些写法：

```python
with open('ledger.txt', 'w', encoding='utf-8') as f:
    f.write('奶茶 12.5\n')
    f.write('午饭 25\n')

with open('ledger.txt', encoding='utf-8') as f:
    print(f.read())
```

输出的结果：

```
奶茶 12.5
午饭 25

```

这几行代码里，新东西不少，咱们一样一样来看：

- `open('ledger.txt', 'w', encoding='utf-8')` ：打开一个叫 `ledger.txt` 的文件。第二个参数是打开方式，`'w'` 是写（write）：文件不存在就新建一个，**已经存在就清空了重写**。不写这个参数，就是 `'r'` 读（read）。
- `encoding='utf-8'` ：用哪种编码来存文字。有中文的时候一定要写上，不然换一台电脑读，可能就是一堆乱码，甚至直接报错。第五节「常见坑」会细说。
- `with ... as f:` ：打开文件，给它起个名字叫 `f` 。缩进里的代码执行完，Python 会自动把文件关掉。`with` 是怎么做到的，第 21 章会讲；现在先记住这个写法：**读写文件，都用 `with`** 。
- `f.write()` ：把一段文字写进文件。它不会自动换行，要换行得自己加 `\n` 。
- `f.read()` ：把整个文件读成一个字符串。

细心的童鞋会发现，输出的最后多了一个空行。这是因为文件最后有一个 `\n` ，`print()` 打印完，自己又换了一次行。

`f.read()` 是一下子读出整个文件。要是想一行一行地处理呢？文件也可以一行一行地读，用 `for` 遍历它就行：

```python
with open('ledger.txt', 'w', encoding='utf-8') as f:
    f.write('奶茶 12.5\n')
    f.write('午饭 25\n')

with open('ledger.txt', encoding='utf-8') as f:
    for line in f:
        print(line.strip())
```

输出的结果：

```
奶茶 12.5
午饭 25
```

这里为什么要先 `strip()` 一下呢？因为读出来的每一行，末尾都带着换行符 `\n` ，所以先用 `strip()` 把它去掉。

前面说过，用 `'w'` 打开，已经存在的文件会被清空了重写。那要是想在文件后面接着写呢？这时候就用 `'a'` ，也就是追加（append）：

```python
with open('ledger.txt', 'w', encoding='utf-8') as f:
    f.write('奶茶 12.5\n')

with open('ledger.txt', 'a', encoding='utf-8') as f:
    f.write('午饭 25\n')

with open('ledger.txt', encoding='utf-8') as f:
    print(f.read())
```

输出的结果：

```
奶茶 12.5
午饭 25

```

可以看到，第二次打开用的是 `'a'` ，午饭接在了奶茶后面，先写的那一笔没有被冲掉。

这样一来，文本文件就能存账了。可是读回来以后，`奶茶 12.5` 只是一整行字符串，名称和金额还得自己拆开。要是再加上类别，就更麻烦了。

那么，有没有现成的格式，专门用来存这种一条一条的数据呢？有，csv 和 json 就是最常用的两种。下一节先来看 csv。

# 三、账本存成 csv

先说 csv。它是一种很常见的表格格式：一行一条记录，每一项用逗号隔开。Excel、WPS 这些表格软件都能直接打开它。

那怎么把账写成 csv 呢？Python 自带一个 `csv` 模块。咱们的每一笔账正好是一个字典，所以用 `csv.DictWriter` 来写最方便：

```python
import csv

entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
]
with open('ledger.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['item', 'category', 'cost'])
    writer.writeheader()
    writer.writerows(entries)

with open('ledger.csv', encoding='utf-8') as f:
    print(f.read())
```

输出的结果：

```
item,category,cost
奶茶,餐饮,12.5
地铁,交通,4

```

对照输出，看看写文件的那几行各干了什么：

- `fieldnames` 告诉它有哪几列，按什么顺序排。
- `writeheader()` 先写第一行，也就是表头。
- `writerows(entries)` 把每一笔账写成一行。

另外，这回 `open()` 里多了一个 `newline=''` 。它是干什么的，先不急，照着写就行，第六节查文档的时候再细说。

写进去了，还得能读回来。读用的是 `csv.DictReader` ，每一行会变回一个字典：

```python
import csv

entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
]
with open('ledger.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['item', 'category', 'cost'])
    writer.writeheader()
    writer.writerows(entries)

with open('ledger.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        print(row)
```

输出的结果：

```
{'item': '奶茶', 'category': '餐饮', 'cost': '12.5'}
{'item': '地铁', 'category': '交通', 'cost': '4'}
```

是不是发现什么不对？存进去的时候，`cost` 是数字 `12.5` ，读回来却变成了字符串 `'12.5'` 。

这是为什么呢？因为 csv 文件里存的全是文字，它可不记得哪一列原来是数字。这和实战 1 的 `input()` 是一回事：读进来的都是字符串，要当数字用，就得自己转换。所以下面读的时候，顺手把每一笔的金额转成数字：

```python
import csv

entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
]
with open('ledger.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['item', 'category', 'cost'])
    writer.writeheader()
    writer.writerows(entries)

loaded = []
with open('ledger.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        row['cost'] = float(row['cost'])
        loaded.append(row)
print(loaded)
print(sum([entry['cost'] for entry in loaded]))
```

输出的结果：

```
[{'item': '奶茶', 'category': '餐饮', 'cost': 12.5}, {'item': '地铁', 'category': '交通', 'cost': 4.0}]
16.5
```

转换以后，金额又变回了数字，合计也能算出来了。

csv 还有一点要注意：要把 csv 文件拿给 Excel 打开的话，把 `encoding='utf-8'` 换成 `encoding='utf-8-sig'` 。不然 Excel 可能认不出这是 UTF-8 编码，中文就显示成了乱码。

到这里，账已经能存成 csv，再读回来了。只是读回来的数字还得自己转换，多少有点麻烦。下一节换成 json，看看能不能省掉这一步。在那之前，先做一道练习：用 `csv.DictReader` 读一个文件，把金额加起来。

# 四、换成 json 试试

json 并不陌生，第 9 章就见过：`json.dumps()` 把字典、列表变成 JSON 字符串，`json.loads()` 再把它变回来。

那存文件用什么呢？用的是另一对：`json.dump()` 和 `json.load()` 。和上面那一对比，名字少了一个 `s` ，它们直接对文件读写：

```python
import json

entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
]
with open('ledger.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

with open('ledger.json', encoding='utf-8') as f:
    print(f.read())
```

输出的结果：

```
[
  {
    "item": "奶茶",
    "category": "餐饮",
    "cost": 12.5
  },
  {
    "item": "地铁",
    "category": "交通",
    "cost": 4
  }
]
```

`json.dump()` 里，除了要存的账和文件 `f` ，还多写了两个参数：

- `ensure_ascii=False` ：中文原样写进去。不加的话，中文会变成 `\u5976\u8336` 这样的编码，第五节「常见坑」里会看到。
- `indent=2` ：每一层缩进两个空格，人看起来方便。

存好了，再用 `json.load()` 读回来，看看读出来的是什么：

```python
import json

entries = [
    {'item': '奶茶', 'category': '餐饮', 'cost': 12.5},
    {'item': '地铁', 'category': '交通', 'cost': 4},
]
with open('ledger.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

with open('ledger.json', encoding='utf-8') as f:
    loaded = json.load(f)
print(loaded)
print(sum([entry['cost'] for entry in loaded]))
```

输出的结果：

```
[{'item': '奶茶', 'category': '餐饮', 'cost': 12.5}, {'item': '地铁', 'category': '交通', 'cost': 4}]
16.5
```

和 csv 比一比：这回 `cost` 读回来还是数字，不用再转换了。因为 json 记得每一项是什么类型：数字、字符串、列表、字典，存进去是什么，读出来还是什么。

两种格式都能存账，那 csv 和 json 该选哪个呢？放在一起比一比：

| | csv | json |
|---|---|---|
| 样子 | 表格，一行一笔 | 和 Python 的列表、字典很像 |
| 读回来 | 全是字符串，要自己转换 | 类型原样还原 |
| 谁来看 | 表格软件直接打开 | 主要给程序读 |
| 适合 | 导出给人看，放进表格里算 | 程序自己存数据，下次再读 |

所以，记账本 v4 自己存账，用 json；想把账导出给 Excel 看，就用 csv。

格式选好了，先做一道练习：把一个字典存进 json 文件，再把它读回来。

# 五、常见坑

文件读写的写法都学了，可真动起手来，还有几个坑等着。有的会报错，有的一声不吭就把账弄丢了，咱们一个一个来看。

## 1、用 'w' 打开，原来的账全没了

```python
with open('ledger.txt', 'w', encoding='utf-8') as f:
    f.write('奶茶 12.5\n')
    f.write('午饭 25\n')

with open('ledger.txt', 'w', encoding='utf-8') as f:
    f.write('地铁 4\n')

with open('ledger.txt', encoding='utf-8') as f:
    print(f.read())
```

输出的结果：

```
地铁 4

```

前两笔账哪儿去了？

因为用 `'w'` 打开文件时，会先把里面的内容**清空**。第二次用 `'w'` 打开，奶茶和午饭就这么没了，而且程序一声不吭。

那该怎么办呢？有两个办法。一是想在后面接着写，就用 `'a'` 。二是像记账本 v4 那样：先把整本账读出来，在内存里加好，再整本写回去。

## 2、读一个不存在的文件

<!-- skip-ci -->
```python
with open('no-such-ledger.json', encoding='utf-8') as f:
    print(f.read())
```

在网页里运行，报错信息的最后一行是：

```
FileNotFoundError: [Errno 44] No such file or directory: 'no-such-ledger.json'
```

要是在自己电脑上运行，中括号里会是 `[Errno 2]` ，后面的意思一样：没有这个文件。

这个错，记账本也会碰上。因为第一次运行记账本的时候，账本文件还没有，直接读就会报这个错。所以读之前，要先看看文件在不在。怎么看呢？`os` 是 Python 自带的模块，里面的 `os.path.exists()` 就是干这个的：

```python
import os

with open('ledger.txt', 'w', encoding='utf-8') as f:
    f.write('奶茶 12.5\n')

print(os.path.exists('ledger.txt'))
print(os.path.exists('no-such-ledger.json'))
```

输出的结果：

```
True
False
```

`ledger.txt` 刚刚写过，所以是 `True` ；`no-such-ledger.json` 不存在，所以是 `False` 。

顺便说一句，第 18 章还会讲一种更现代的写法 `pathlib` ，现在先用 `os.path.exists()` 就行。

## 3、json 里的中文变成了一串编码

```python
import json

entries = [{'item': '奶茶', 'category': '餐饮', 'cost': 12.5}]
print(json.dumps(entries))
print(json.dumps(entries, ensure_ascii=False))
```

输出的结果：

```
[{"item": "\u5976\u8336", "category": "\u9910\u996e", "cost": 12.5}]
[{"item": "奶茶", "category": "餐饮", "cost": 12.5}]
```

为什么会这样呢？因为 `json.dumps()` 和 `json.dump()` 默认会把中文转成 `\u5976` 这样的编码。程序读回来没问题，可人打开文件就看不懂了。所以存中文的时候，记得加上 `ensure_ascii=False` 。

## 4、忘了写 encoding

这一章的代码，每次 `open()` 都写了 `encoding` 。要是忘了写，会怎么样呢？

不写 `encoding` ，Python 就用电脑的默认编码。在中文版 Windows 上，Python 3.15 之前的版本默认用的往往是 GBK，而不是 UTF-8。

这会带来什么结果呢？在 Mac 上写的文件，拿到 Windows 上读，会报 `UnicodeDecodeError` ，或者读出一堆乱码；反过来也一样。可惜这个坑在网页里试不出来，因为网页里的 Python 默认就是 UTF-8。

所以最省事的办法，就是**每次 `open()` 都写上 `encoding='utf-8'`** 。

坑都看完了，先做一道练习：往文件后面再记一笔账，别把前面的冲掉。

# 六、自己查一次文档

第三节写 csv 文件的时候，`open()` 里多了一个 `newline=''` ，当时说先照着写。现在咱们自己去查：它到底是干什么的？

打开官方文档里 csv 模块的那一页，找到 [csv.writer()](https://docs.python.org/zh-cn/3/library/csv.html#csv.writer) 的说明，里面有一句：如果 csvfile 是一个文件对象，则打开它时应使用 `newline=''` 。

可为什么要这样写呢？这句话后面跟着一个 `[1]` ，这是脚注。点一下它，页面会跳到最下面的「备注」，那里写着原因，一共两条：

- 不写 `newline=''` ，引号字段里包含的换行符就没法被正确解析。
- 写入的时候，在使用 `\r\n` 换行的平台上，会额外多加一个 `\r` 。

第二条里说的「使用 `\r\n` 换行的平台」，其实就是 Windows。多出来的 `\r` ，会让 Excel 打开文件时，每两行账之间都夹着一个空行。这种问题在 Mac 上根本看不出来，换到 Windows 上才冒出来，所以不查文档还真不好找。

脚注最后还说：指定 `newline=''` 始终是安全的做法，因为 csv 模块会自己处理换行。

所以结论很简单：**用 csv 模块读写文件，`open()` 里都加上 `newline=''`** 。

查都查到这儿了，不妨顺着同一页，再看看 [csv.DictWriter](https://docs.python.org/zh-cn/3/library/csv.html#csv.DictWriter) 的说明，会发现一句：和 `DictReader` 不一样，`DictWriter` 的 `fieldnames` 参数不能省略。这也解释了第三节为什么要先告诉它有哪几列。

要是说明读着费劲，也可以先看例子。文档里每个函数后面，几乎都跟着「一个简短的用法示例」。看不懂说明的时候，先把示例复制下来跑一跑，往往比读说明更快明白。

回头看看，这回查文档的收获，是一个不查就很难发现的坑。所以以后用一个新模块，不妨先把它的文档页从头到尾扫一遍，尤其留意「备注」「注意」这类地方，坑往往就藏在那里。

文件读写的本事都齐了，下一节就把它们用到记账本上。

# 七、记账本 v4

现在回到这一章开头的那个老毛病：程序一关，账就没了。第四节比过，记账本自己存账，用 json 最合适。所以咱们给实战 4 的 `Ledger` 加两个方法：`save()` 把整本账存成 json 文件，`load()` 再把它读回来。

```python
import json


class Ledger:
    """记账本：记下每一笔账，可以存进文件，下次再读回来。"""

    def __init__(self):
        self.entries = []

    def add(self, item, category, cost):
        """记一笔账。"""
        self.entries.append({'item': item, 'category': category, 'cost': cost})

    def total(self):
        """返回所有账的合计。"""
        return sum([entry['cost'] for entry in self.entries])

    def save(self, path):
        """把整本账存成 json 文件。"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def load(self, path):
        """从 json 文件读回整本账。"""
        with open(path, encoding='utf-8') as f:
            self.entries = json.load(f)


book = Ledger()
book.add('奶茶', '餐饮', 12.5)
book.add('午饭', '餐饮', 25)
book.save('my_ledger.json')

# 假装程序关掉了，又重新打开：新建一本空账，再从文件里读
again = Ledger()
print(len(again.entries))
again.load('my_ledger.json')
print(len(again.entries))
print(f'合计：{again.total():.2f} 元')
```

输出的结果：

```
0
2
合计：37.50 元
```

对照输出看一看。`again` 是一本新账，一开始什么都没有，所以先打印出 0。`load()` 以后，存进去的两笔账都回来了，就变成了 2。

有的童鞋可能会担心：`save()` 用 `'w'` 打开文件，第五节不是刚说过，它会把原来的内容清空吗？没错，它每次都是整本重写。可是 `self.entries` 里本来就是完整的账，整本写一遍，文件就和内存里的一模一样，所以不会出现第五节那种「后写的把先写的冲掉」的问题。

`save()` 和 `load()` 都试过了，再把它们放进记账的主程序。思路是这样的：开始的时候，有账本文件就先读出来；记完了，再存回去。

<!-- skip-ci -->
```python
import os

PATH = 'my_ledger.json'
book = Ledger()
if os.path.exists(PATH):
    book.load(PATH)
    print(f'读到了以前的 {len(book.entries)} 笔账')

while True:
    item = input('买了什么：').strip()
    if item == '完':
        break
    category = input('类别：').strip()
    book.add(item, category, read_cost())

book.save(PATH)
print(f'一共 {len(book.entries)} 笔，合计 {book.total():.2f} 元，已经存好了')
```

这段主程序里用到的 `read_cost()` ，和实战 3 的一样，这里就不重复写了。另外，文件名写成了大写的 `PATH` ，这是一个习惯：全大写的变量，表示它是一个「定下来就不改」的设置。

第一节说过，网页里写出的文件，刷新页面就没了。所以想亲眼看看效果，要把 `read_cost()` 、`Ledger` 和上面的主程序放进同一个 `ledger.py` ，在自己电脑上运行。第一次运行，记两笔：

```
买了什么：奶茶
类别：餐饮
花了多少钱：12.5
买了什么：午饭
类别：餐饮
花了多少钱：25
买了什么：完
一共 2 笔，合计 37.50 元，已经存好了
```

然后把程序关掉，再运行一次，这回记一笔：

```
读到了以前的 2 笔账
买了什么：地铁
类别：交通
花了多少钱：4
买了什么：完
一共 3 笔，合计 41.50 元，已经存好了
```

看第一行：第二次一打开，就读到了上次的两笔账，接着往下记。再看看程序旁边多出来的 `my_ledger.json` ，用记事本就能打开，里面是一笔一笔的账。

记账本终于有了记性。

最后做一道练习：给 `Ledger` 补上 `load()` ，让它在文件不存在的时候什么都不做，也不报错。

# 八、小结与回看

这一章，咱们带着「把账存起来」这个需求，学了文件、csv 和 json，记账本终于能把账存下来了。回头梳理一下，学到了这几件事：

- 变量在内存里，程序一结束就没了；要留下来，就存进文件。
- 读写文件用 `with open(路径, 打开方式, encoding='utf-8') as f:` 。`'r'` 读，`'w'` 清空重写，`'a'` 在后面追加。
- csv 一行一条记录，表格软件能直接打开。用 `DictWriter` 、`DictReader` 读写字典；读回来全是字符串，数字要自己转换。要给 Excel 打开，编码用 `'utf-8-sig'` 。
- json 能原样还原数字、字符串、列表、字典。`json.dump()` 存，`json.load()` 读；有中文时加上 `ensure_ascii=False` 。
- 读文件之前，用 `os.path.exists()` 看看文件在不在。
- 用 csv 模块时，`open()` 里加上 `newline=''` ，这是从文档的脚注里查到的。
- 网页里写出的文件，刷新页面就没了；想真正存下来，要在自己电脑上运行。

哪里卡住了，就回去看一看：

- `import` 和 json 的 `dumps()` 、`loads()` ：第 9 章
- 读进来的都是字符串：实战 1 的「二、12 加 30，怎么等于 1230？」
- `Ledger` 类和 `self` ：实战 4 的「四、v3：写成一个类」

回头看看，从实战 1 只会记一笔的 v0，到现在有记性的 v4，记账本已经是一个真正能天天用的小程序了。这一路用到的，全是前面学过的东西：变量、列表、字典、循环、函数、类、模块。把学过的东西用起来，它们才真正变成了你的。

不过，现在的账还缺一样东西：日期。光知道一共花了多少，却不知道是哪天花的，就没法看这个月、这一周各花了多少。所以下一章，咱们自学一个新模块 `datetime` ，给每一笔账加上日期。
