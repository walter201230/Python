# 数据分析第 3 章：挑出想要的数据

# 前言

上一章，咱们把记账本这张表看清楚了：一千多行、5 列，每一列是什么类型，心里都有数了。

可是真要回答问题的时候，往往用不着整张表。比如「看病一年花了多少？」，只要医疗那几行就够了；「哪几笔花得最多？」，只要金额大的那几行；「每天的早饭吃了些什么？」，只要名称这一列里的一部分。

所以这一章，就来学怎么从一张大表里，把想要的那部分挑出来。挑法主要有三种：按列挑、按位置挑、按条件挑。为什么要专门花一章来学呢？因为这是 pandas 里用得最多的本事，后面每一章都离不开它。

**学这一章之前**，需要先学完 [数据分析课第 2 章](02-first-dataframe.md) 。

# 目录

这一章会学到：

- 一、按列挑——一列、几列，以及去掉不要的列
- 二、按位置挑——`iloc` 和 `loc`
- 三、按条件挑——一串 `True` 和 `False`
- 四、好几个条件——`&` 、`|` 、`~` 和 `isin()`
- 五、常见坑
- 六、自己查一次文档——用 `between()` 挑出一个范围
- 七、小结与回看

学完这一章，脑子里冒出一个问题，你就能把回答它所需要的那部分数据，从表里干干净净地挑出来。

# 一、按列挑

先从最简单的按列挑说起。上一章已经见过：方括号里写一个列名，就能取出一列；写一个列名的列表，就能取出好几列。不过这里面有一个容易忽略的区别，先运行下面的代码看看：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(type(ledger['item']))
print(type(ledger[['item']]))
```

输出的结果：

```
<class 'pandas.core.series.Series'>
<class 'pandas.core.frame.DataFrame'>
```

同样是 `item` 这一列，用一层方括号，得到的是 Series；用两层方括号，得到的却是 DataFrame，也就是一张只有一列的表。

为什么要分得这么清楚呢？因为两者能做的事不一样：

- Series 是一串值，可以直接 `sum()` 、`unique()` 。
- DataFrame 是一张表，打印出来带着列名，还能接着挑行、挑列。

所以，只想要一串值，就用一层方括号；想要的还是一张表，就用两层。

好几列一起取的时候，还有一个小细节：列的顺序，是按你写的顺序来的。

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(ledger[['cost', 'item', 'date']].head(3))
```

输出的结果：

```
     cost      item        date
0  2500.0      房租  2026-01-01
1   156.0  水电燃气  2026-01-01
2    13.0      早饭  2026-01-01
```

`cost` 写在最前面，打印出来它就排在了第一列。

那要是想要的列很多，不要的只有一两列呢？一个一个地写想要的列，就太麻烦了。这时候反过来，只写不要的那几列更省事，用 `drop(columns=[...])` ：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
no_payment = ledger.drop(columns=['payment'])
print(list(no_payment.columns))
print(ledger.shape)
```

输出的结果：

```
['date', 'item', 'category', 'cost']
(1354, 5)
```

先看第一行：`payment` 这一列已经去掉了。再留意第二行：`ledger` 还是 5 列。这是因为 `drop()` 不会改动原来的表，而是返回一张新表。pandas 里大部分方法都是这样，所以要保留结果，就得用一个变量把它接住，比如这里的 `no_payment` 。

# 二、按位置挑

列会挑了，那行该怎么挑呢？

最直接的办法，是按**位置**挑，也就是说「我要第几行」。这时候用 `iloc` ，方括号里写位置。和列表的下标一样，位置也是从 0 开始数的：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(ledger.iloc[0])
```

输出的结果：

```
date        2026-01-01
item              房租
category          居住
cost            2500.0
payment         银行卡
Name: 0, dtype: object
```

取出一行，得到的也是一个 Series。只不过这回，是把横着的一行竖过来放：左边是列名，右边是这一行的值。最下面的 `Name: 0` 告诉你，这是行号为 0 的那一行。

一次只取一行，不够用怎么办？可以用切片，一次取好几行。切片的规则也和列表一样，**不包括结尾**：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(ledger.iloc[9:12])
print(ledger.iloc[-2:])
```

输出的结果：

```
          date  item category  cost payment
9   2026-01-02  地铁     交通   6.5    微信
10  2026-01-02  零食     餐饮  12.5  支付宝
11  2026-01-03  午饭     餐饮  27.0  支付宝
            date  item category  cost payment
1352  2026-12-31  地铁     交通   4.0    微信
1353  2026-12-31  零食     餐饮   9.5    微信
```

`iloc[9:12]` 取的是位置 9、10、11 这三行，不包括 12。`iloc[-2:]` 取的是最后两行，因为负数是从后往前数的，这一点也和列表一样。

除了 `iloc` ，还有一个 `loc` 。它和 `iloc` 有什么不同呢？`loc` 是按行的**标签**来挑，也就是最左边那一列行号。而且它还能同时用列名挑列：逗号前面写行，逗号后面写列。

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(ledger.loc[0, 'item'])
print(ledger.loc[9:11, ['item', 'cost']])
```

输出的结果：

```
房租
    item  cost
9   地铁   6.5
10  零食  12.5
11  午饭  27.0
```

来看看这两行各取出了什么：

- `loc[0, 'item']` 是行号为 0 的那一行、`item` 那一列，正好就是一个值：房租。
- `loc[9:11, ...]` 取出了 9、10、11 这三行。注意，它**包括结尾的 11**，这一点和 `iloc` 不一样。

把两者放在一起，比一比：

| | `iloc` | `loc` |
|---|---|---|
| 按什么挑 | 位置：第几行、第几列 | 标签：行号、列名 |
| 写法 | `ledger.iloc[0]` 、`ledger.iloc[9:12]` | `ledger.loc[0, 'item']` 、`ledger.loc[9:11, ['item', 'cost']]` |
| 切片包不包括结尾 | 不包括，和列表一样 | 包括 |

看到这里，有的童鞋可能会觉得：行号和位置不都是 0、1、2 吗，两者好像也差不多？没错，眼下行号和位置是一回事，所以看起来差不多。可是下一节按条件挑完以后，行号就不再是 0、1、2 这样连着的了，到时候区别就出来了。

在那之前，先做一道练习：挑出几行几列，顺便留意一下切片的结尾包不包括。

# 三、按条件挑

前面挑行，都得先知道要的是第几行。可是大多数时候，咱们并不知道想要的是第几行，只知道它满足什么**条件**，比如「金额超过 500 元的」「类别是医疗的」。这样的行，该怎么挑出来呢？

先别急着挑，看看拿一整列去做比较，会得到什么：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
big = ledger['cost'] > 500
print(big.head())
print(big.sum())
```

输出的结果：

```
0     True
1    False
2    False
3    False
4    False
Name: cost, dtype: bool
12
```

很多童鞋可能以为，`ledger['cost'] > 500` 会得到一个 `True` 或者 `False` 。其实不是，它得到的是**一整串**：这一列的每个值，都拿去和 500 比了一次，比完的结果排成一个 Series，类型是 `bool` 。比如第 0 行是 2500 元的房租，比 500 大，所以是 `True` 。

那最后那个 12 是怎么来的呢？因为求和的时候，`True` 当成 1，`False` 当成 0，加起来就是一共有几个 `True` 。也就是说，一年里超过 500 元的花销有 12 笔。

有了这一串 `True` 和 `False` ，挑行就简单了：把它放进方括号，pandas 就只留下 `True` 的那些行。

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(ledger[ledger['cost'] > 500])
```

输出的结果：

```
            date  item category    cost payment
0     2026-01-01  房租     居住  2500.0  银行卡
116   2026-02-01  房租     居住  2500.0  银行卡
218   2026-03-01  房租     居住  2500.0  银行卡
325   2026-04-01  房租     居住  2500.0  银行卡
441   2026-05-01  房租     居住  2500.0  银行卡
555   2026-06-01  房租     居住  2500.0  银行卡
660   2026-07-01  房租     居住  2500.0  银行卡
781   2026-08-01  房租     居住  2500.0  银行卡
893   2026-09-01  房租     居住  2500.0  银行卡
1004  2026-10-01  房租     居住  2500.0  银行卡
1116  2026-11-01  房租     居住  2500.0  银行卡
1232  2026-12-01  房租     居住  2500.0  银行卡
```

原来，超过 500 元的全是每个月 1 号交的房租。

这种写法乍一看有点绕：`ledger[ ... ]` 里面又套着一个 `ledger['cost']` 。拆开来读就清楚了：里面那一层，算出一串 `True` 和 `False` ；外面那一层，按这一串来挑行。

再看看左边的行号：0、116、218……已经不再是连着的了。这是因为挑出来的行，都保留着它们在原表里的行号。上一节说的区别，这时候就出来了：同一行，用 `iloc` 和用 `loc` 来取，写法不一样。

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
rent = ledger[ledger['cost'] > 500]
print(rent.iloc[1]['date'])
print(rent.loc[116, 'date'])
```

输出的结果：

```
2026-02-01
2026-02-01
```

两行输出一样，取到的是同一行。可是在 `iloc` 眼里，它是「挑出来的第 2 行」，位置是 1；在 `loc` 眼里，它是「行号为 116 的那一行」。

比较也不只有大于、小于，`==` 等于、`!=` 不等于也一样能用。比如，看病一年花了多少钱？

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
health = ledger[ledger['category'] == '医疗']
print(health)
print(health['cost'].sum())
```

输出的结果：

```
            date  item category   cost payment
436   2026-04-29  看病     医疗  134.0  支付宝
486   2026-05-11  看病     医疗  193.0  支付宝
537   2026-05-26  看病     医疗  191.0    微信
617   2026-06-16  看病     医疗   83.5    微信
1201  2026-11-21  看病     医疗  216.5    微信
1300  2026-12-18  看病     医疗  204.0    微信
1318  2026-12-23  看病     医疗  159.5    微信
1181.5
```

这段代码分了两步：先挑出医疗的那几行，再取出金额这一列求和。结果是一年看了 7 次病，一共花了 1181.5 元。「先挑行，再取列，最后算」，这就是 pandas 里最常见的套路。

照着这个套路，先做一道练习：交通一年花了多少？做完了，再来看看条件不止一个的时候，该怎么写。

# 四、好几个条件

上一节的条件都只有一个。可有些问题，一个条件说不清楚。比如「吃饭的时候，一顿超过 50 元的有几次？」，这里就有两个条件：类别是餐饮，**并且**金额超过 50 元。

两个条件要同时满足，就用 `&` 把它们连起来。要注意，**每个条件都要用括号括起来**：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
pricey = ledger[(ledger['category'] == '餐饮') & (ledger['cost'] > 50)]
print(len(pricey))
print(pricey['item'].unique())
```

输出的结果：

```
55
['晚饭']
```

一共 55 次，而且全是晚饭。也就是说，早饭、午饭再怎么吃，也没有超过 50 元的。

「并且」有了，那「或者」呢？「或者」用 `|` 。比如，娱乐和学习加起来，一年花了多少？

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
fun_or_study = ledger[(ledger['category'] == '娱乐') | (ledger['category'] == '学习')]
print(fun_or_study['cost'].sum())
```

输出的结果：

```
4837.0
```

这样写没有问题。可是同一列要和好几个值比的时候，一个一个用 `|` 连起来，代码就太长了。这时候可以用 `isin()` ，一次就说清楚：「是不是这几个值当中的一个」。

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
fun_or_study = ledger[ledger['category'].isin(['娱乐', '学习'])]
print(fun_or_study['cost'].sum())
```

输出的结果：

```
4837.0
```

结果一样，而且读起来也更像一句话。

最后还有「不是」，用 `~` 。把它放在条件前面，就会把 `True` 和 `False` 反过来。比如，不是用微信、也不是用支付宝付的，有几笔？

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
others = ledger[~ledger['payment'].isin(['微信', '支付宝'])]
print(len(others))
print(others['payment'].unique())
```

输出的结果：

```
197
['银行卡' '现金']
```

一共 197 笔，用的是银行卡和现金。

把这几个符号放在一起，对照着看：

| 符号 | 意思 | 例子 |
|---|---|---|
| `&` | 并且，两个都满足 | `(条件1) & (条件2)` |
| `\|` | 或者，满足一个就行 | `(条件1) \| (条件2)` |
| `~` | 不是，反过来 | `~(条件)` |
| `isin()` | 是这几个值当中的一个 | `ledger['category'].isin(['娱乐', '学习'])` |

看到这里，你也许会问：Python 里明明有 `and` 、`or` 、`not` ，为什么要换成这几个符号？下一节的第一个坑，说的就是它。

# 五、常见坑

按条件挑行，写法比前面几节都要绕一些，所以坑也最多。咱们先接着上一节留下的问题说。

## 1、用了 and、or

很多童鞋会很自然地写成这样：

<!-- skip-ci -->
```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
pricey = ledger[(ledger['category'] == '餐饮') and (ledger['cost'] > 50)]
```

报错信息的最后一行是：

```
ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
```

这句报错的意思是：「一个 Series 的真假是说不清的」。为什么说不清呢？因为 `and` 要先判断左边整个是真还是假，可左边是一千多个 `True` 和 `False` ，到底该算真还是算假？Python 没法替你决定，只好报错。

`&` 就不一样了，它是**一个一个对着比**：第 0 行和第 0 行比，第 1 行和第 1 行比……得到的还是一串。所以挑行的时候，「并且」写 `&` ，「或者」写 `|` ，「不是」写 `~` 。

## 2、忘了加括号

换成了 `&` ，可要是嫌括号麻烦，把它们省掉了呢？

<!-- skip-ci -->
```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
pricey = ledger[ledger['category'] == '餐饮' & ledger['cost'] > 50]
```

报错信息的最后一行是：

```
TypeError: Cannot perform 'rand_' with a dtyped [float64] array and scalar of type [bool]
```

这条报错很难看懂，原因却很简单：在 Python 里，`&` 比 `==` 、`>` 先算。没有括号，这一行就被理解成了先算 `'餐饮' & ledger['cost']` ，也就是把文字和金额「并且」起来，这当然不行。

所以，每个条件都用括号括起来，就不会出错了。以后看到报错里有 `rand_` 、`ror_` 这样的字眼，先去数一数括号。

## 3、挑完以后还按原来的位置用 loc

<!-- skip-ci -->
```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
rent = ledger[ledger['cost'] > 500]
print(rent.loc[1])
```

报错信息的最后一行是：

```
KeyError: 1
```

这里本来想要的，是挑出来的第 2 行，结果写成了 `loc[1]` 。可 `loc` 认的是行号，而挑出来的表里，并没有行号为 1 的那一行：原表里行号为 1 的是水电燃气，早就被筛掉了。所以按位置取，要用 `iloc[1]` 。

## 4、loc 和 iloc 的切片不一样长

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(len(ledger.iloc[0:3]))
print(len(ledger.loc[0:3]))
```

输出的结果：

```
3
4
```

同样是写 `0:3` ，`iloc` 取了 3 行，因为它不包括结尾；`loc` 取了 4 行，因为它包括结尾。拿不准的时候，就 `len()` 一下，或者 `print()` 出来看一眼。

# 六、自己查一次文档

先来看一个问题：「金额在 20 到 30 元之间的有几笔？」用学过的写法，是这样的：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
middle = ledger[(ledger['cost'] >= 20) & (ledger['cost'] <= 30)]
print(len(middle))
```

输出的结果：

```
349
```

答案是算出来了，就是同一列写了两遍，有点啰嗦。这种「在某个范围之内」的需求太常见了，pandas 会不会有现成的方法呢？咱们去文档里找一找。

Series 的方法很多，一个一个看太慢。不妨按名字猜一猜：「在……之间」，英文是 between。去文档里一找，正好有一个：[Series.between](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.Series.between.html) 。

文档开头说，它返回一串布尔值，表示每个值是不是在 `left` 和 `right` 之间。它的参数有三个：

- `left` 是下限。
- `right` 是上限。
- `inclusive` 管两头包不包括，可以写 `'both'` 、`'neither'` 、`'left'` 、`'right'` 。默认是 `'both'` ，也就是两头都包括。

查到了，就动手试一试，把 `inclusive` 的几种写法比一比：

```python
import pandas as pd

ledger = pd.read_csv('ledger_2026.csv')
print(len(ledger[ledger['cost'].between(20, 30)]))
print(len(ledger[ledger['cost'].between(20, 30, inclusive='left')]))
print(len(ledger[ledger['cost'].between(20, 30, inclusive='neither')]))
```

输出的结果：

```
349
332
326
```

第一行是 349，和上面算的一样。第二行用了 `inclusive='left'` ，只包括左边的 20，不包括右边的 30，结果少了 17 笔，说明正好 30 元的有 17 笔。第三行两头都不包括，又少了 6 笔，说明正好 20 元的有 6 笔。

所以用 `between()` 之前，先想清楚：边界上的那个值，要不要算进去？文档里写的默认值，其实就是你没想清楚的时候，它替你做的决定。

# 七、小结与回看

这一章，咱们学会了从一张大表里，把回答问题需要的那部分挑出来。回头梳理一下，学到了这几件事：

- 按列挑：`ledger['列名']` 得到的是一个 Series，`ledger[['列名']]` 得到的是一张表。`drop(columns=[...])` 能去掉不要的列，它返回一张新表，原表不变。
- 按位置挑：`iloc[位置]` 、`iloc[开始:结束]` ，用法和列表一样，切片不包括结尾。
- 按标签挑：`loc[行号, 列名]` ，切片包括结尾。挑过以后，行号不再连着，这时两者的区别就出来了。
- 按条件挑：拿一整列去比较，得到一串 `True` 和 `False` ；把它放进方括号，就只留下 `True` 的行。对它 `sum()` 一下，就知道满足条件的有几个。
- 好几个条件：`&` 表示并且，`|` 表示或者，`~` 表示不是，每个条件都要用括号括起来。同一列要和好几个值比，就用 `isin()` 。
- 常见的坑：用了 `and` 、`or` ；忘了加括号；挑完以后还按原来的位置用 `loc` 。
- 查文档学会了用 `between()` 挑出一个范围，还弄清了 `inclusive` 管的是两头包不包括。

哪里卡住了，就回去看一看：

- 列表的下标和切片：第 3 章
- 布尔值和 `and` 、`or` 、`not` ：第 2 章

数据挑出来了，接下来就该好好算一算了。下一章要回答这几个问题：平均数和中位数，该信哪个？每个值出现了几次？各占了多大比例？
