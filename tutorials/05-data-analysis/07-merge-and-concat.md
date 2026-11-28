# 数据分析第 7 章：把几张表拼起来

# 前言

前面几章，每次分析的都只是一张表。可真实的数据，常常是分散在好几张表里的。

两点书店的数据就是这样，分成了两张表。`books.csv` 是书目，记着每本书的书名、作者、类别、价格。`book_reviews.csv` 是读者的评分，一条评分占一行，只记了是给哪个编号的书、打了几分、哪天打的。

那么，要是想知道「哪一类书评分最高」呢？这时候两张表缺一不可：评分在一张表里，类别却在另一张表里。所以，得先把它们**合并**起来。

这一章就来学两种合并的办法：一种是按某一列「对上号」，左右拼起来；另一种是把几张一样的表，上下接起来。

**学这一章之前**，需要先学完 [数据分析课第 6 章](06-groupby-and-pivot.md) 。

# 目录

这一章会学到：

- 一、两张表怎么对上号——认识「键」
- 二、左右拼起来——`merge()`
- 三、对不上号的行去哪儿了——`how` 参数
- 四、上下接起来——`pd.concat()`
- 五、常见坑
- 六、自己查一次文档——用 `indicator` 看清每一行从哪儿来
- 七、小结与回看

学完这一章，数据分散在几张表里也不用怕了：你能先把它们拼成一张，再接着用前面学的本事去分析。

# 一、两张表怎么对上号

两张表要合并，首先得知道它们靠什么连在一起。咱们先看看评分表里都记了些什么：

```python
import pandas as pd

reviews = pd.read_csv('book_reviews.csv')
print(reviews.shape)
print(reviews.head(3))
```

输出的结果：

```
(834, 4)
   review_id  book_id  score        date
0          1      111      4  2025-01-01
1          2       49      2  2025-01-02
2          3      106      4  2025-01-02
```

可以看到，评分表一共有 834 条评分。每一条里，和书有关的只有一个 `book_id` ，也就是书的编号。比如第一条评分，是给 111 号书的，打了 4 分。那 111 号书叫什么、是什么类别呢？这张表里可就没有了。

书名和类别，都记在书目表里。再从书目表里挑三列出来看看：

```python
import pandas as pd

books = pd.read_csv('books.csv')
print(books[['id', 'title', 'category']].head(3))
```

输出的结果：

```
   id               title category
0   1      轻松玩转自动化     编程
1   2  小账本里的通货膨胀     经济
2   3            早起养花     生活
```

两边对比一下就会发现：书目表里的 `id` ，就是评分表里的 `book_id` 。两张表就是靠这个编号对上号的。评分表说「111 号书打了 4 分」，那就去书目表里找 `id` 是 111 的那一行，一看就知道是哪本书了。

像这样用来对号的列，叫做**键**（key）。它就像身份证号一样，一个编号只对应一本书。

看到这里，很多童鞋可能会问：「为什么不在评分表里直接写上书名呢？」因为一本书有好几条评分，要是书名、作者、类别、价格每条都写一遍，就太浪费了；而且万一哪本书改了价格，还得把它所有的评分都改一遍。所以，数据常常分成几张表，各管各的，再用键连在一起。等到要分析的时候，再把它们合并起来。

那么，具体怎么合并呢？下一节就来动手。

# 二、左右拼起来

按键把两张表左右拼起来，用的是 `merge()` 。不过，这两张表里键的列名不一样：评分表里叫 `book_id` ，书目表里叫 `id` 。所以要分别告诉它：`left_on` 写左边那张表的列名，`right_on` 写右边那张表的列名：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
merged = reviews.merge(books, left_on='book_id', right_on='id')
print(merged.shape)
print(merged[['review_id', 'book_id', 'title', 'category', 'score']].head(3))
```

输出的结果：

```
(834, 14)
   review_id  book_id           title category  score
0          1      111  小账本里的保险     经济      4
1          2       49      月亮的冒险     童书      2
2          3      106    一个人的厨房     生活      4
```

读这行合并的代码，先要分清谁在左、谁在右。`reviews.merge(books, ...)` 里，`reviews` 在左，`books` 在右。合并的时候，每一条评分都会拿着自己的 `book_id` ，去书目表里找到 `id` 一样的那一行，再把那一行拼到自己的右边。

再看输出的第一行。拼完以后还是 834 行，因为仍然是每条评分占一行；列却变成了 14 列，也就是评分表的 4 列，加上书目表的 10 列。这样一来，每条评分旁边，就都有了书名和类别。

有了类别，前言里那个问题「哪一类书评分最高」，就能回答了。用的还是第 6 章的老本事，按类别分组：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
merged = reviews.merge(books, left_on='book_id', right_on='id')
print(merged.groupby('category')['score'].agg(['count', 'mean']).round(2).sort_values('mean', ascending=False))
```

输出的结果：

```
          count  mean
category             
设计        107  3.83
编程        107  3.68
小说        100  3.59
童书         88  3.50
经济        106  3.50
科普        108  3.38
历史        100  3.36
生活        118  3.25
```

从结果看，设计类的书评分最高，平均 3.83 分；生活类收到的评分最多，平均分却是最低的。

所以说，合并只是一个开头。表拼好了以后，筛选、分组、排序，前几章学的本事都能接着用。

不过，这回每一条评分都对上了号，拼完一行也没少。要是有的行对不上号，又会怎么样呢？下一节就来看看。在那之前，先做一道练习：给评分配上书名。

# 三、对不上号的行去哪儿了

上一节是从评分出发，给每条评分配上书。这回换个方向，从书出发：每本书收到了几条评分，平均几分？做法是先在评分表里按书分组，算出条数和平均分，再拼回书目表：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
stats = reviews.groupby('book_id')['score'].agg(['count', 'mean']).reset_index()
table = books.merge(stats, left_on='id', right_on='book_id')
print(len(books), len(table))
```

输出的结果：

```
120 109
```

奇怪，书目表有 120 本书，拼完却只剩 109 本。少了的 11 本，到哪儿去了？

原来，它们是还没有人打过分的书。评分表里没有它们的编号，自然就对不上号。而 `merge()` 默认只留下**两边都对得上**的行，对不上的，就直接扔掉了。

那想把书一本不少地留着，该怎么办呢？加上 `how='left'` 就行。它的意思是：左边表的行全部保留，右边对不上的地方，就填上 `NaN` ：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
stats = reviews.groupby('book_id')['score'].agg(['count', 'mean']).reset_index()
table = books.merge(stats, left_on='id', right_on='book_id', how='left')
print(len(table))
print(table[['id', 'title', 'count', 'mean']].head(4).round(2))
```

输出的结果：

```
120
   id               title  count  mean
0   1      轻松玩转自动化   13.0  4.69
1   2  小账本里的通货膨胀    3.0  3.67
2   3            早起养花    NaN   NaN
3   4            书院笔记    7.0  5.00
```

这回 120 本都在了。比如 3 号书《早起养花》，没人打过分，所以它的 `count` 和 `mean` 都是 `NaN` 。

细心的童鞋会发现，条数本来应该是整数，`count` 却变成了 `13.0` 这样的小数。这是因为这一列里混进了 `NaN` 。`NaN` 在 pandas 里算是一个小数，整数列里混进了它，整列就都变成了小数。

其实 `how` 一共有四种写法，可以对照这张表来看：

| `how=` | 留下哪些行 |
|---|---|
| `'inner'` | 两边都对得上的，默认就是这个 |
| `'left'` | 左边的全部，右边对不上的填 `NaN` |
| `'right'` | 右边的全部，左边对不上的填 `NaN` |
| `'outer'` | 两边的全部，谁对不上谁填 `NaN` |

这么多种，该选哪一种呢？合并之前，先想清楚一件事：对不上号的行，你还要不要？要分析「每本书」，就用 `'left'` ，一本都不能少；只关心「有评分的书」，用默认的 `'inner'` 就行。

先做一道练习，用 `how='left'` 数一数：有几本书还没人打分？

# 四、上下接起来

前面学的 `merge()` ，是把两张表左右拼起来。还有一种情况也很常见：几张表的列都一样，要把它们上下接起来。比如书店又进了两本新书，要把它们接在书目的后面：

```python
import pandas as pd

books = pd.read_csv('books.csv')
new_books = pd.DataFrame([
    {'id': 121, 'title': '给数据画张像', 'category': '编程', 'price': 66.0},
    {'id': 122, 'title': '窗台上的四季', 'category': '生活', 'price': 39.5},
])
all_books = pd.concat([books, new_books], ignore_index=True)
print(len(books), len(all_books))
print(all_books[['id', 'title', 'price', 'rating']].tail(3))
```

输出的结果：

```
120 122
      id         title  price  rating
119  120  蒲公英的冒险   37.7     4.0
120  121  给数据画张像   66.0     NaN
121  122  窗台上的四季   39.5     NaN
```

这段代码里有三处新写法，咱们一个一个来看：

- `pd.DataFrame(字典的列表)` 可以直接造一张表：列表里的每个字典是一行，字典的键就是列名。
- `pd.concat([表1, 表2])` 把列表里的几张表，按列名对齐，上下接起来。
- `ignore_index=True` 让行号重新从 0 一直排到底。不写的话，新书的行号还是它们自己的 0 和 1，就和原来的 0、1 重复了。

再看输出：新书只写了四列，没写评分、库存这些列，所以接起来以后，这些地方都是 `NaN` 。

那什么时候会用到上下接呢？其实数据常常是一份一份来的：每个月一个账单文件，爬虫每抓一页存一份。把它们一份一份读进来，放进一个列表，最后 `pd.concat()` 一下，就是完整的一张表了。

# 五、常见坑

合并的写法并不难，可真用起来，有几个地方很容易出岔子。下面这三个坑，咱们一个一个来看。

## 1、键的类型不一样

有时候，一张表里的编号是数字，另一张表里的却是文字，比如从网页上抓下来的数据。看上去都是 111，合并的时候却会报错。下面就故意造一个这样的情况：

<!-- skip-ci -->
```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
reviews['book_id'] = reviews['book_id'].astype(str)
merged = reviews.merge(books, left_on='book_id', right_on='id')
```

运行以后，报错信息的最后一行是：

```
ValueError: You are trying to merge on object and int64 columns for key 'book_id'. If you wish to proceed you should use pd.concat
```

代码里故意用 `astype(str)` ，把评分表的编号变成了文字。可数字 111 和文字 `'111'` ，在 Python 里是不相等的，所以 pandas 干脆不让你合并。

有意思的是，报错的后半句建议用 `pd.concat` 。可这个建议其实并不对路：咱们要的是对上号、左右拼，而不是上下接。所以，报错信息里的建议，也要自己判断一下适不适用。

那正确的改法是什么呢？把两边的类型统一起来就行，比如 `reviews['book_id'].astype(int)` 。为了不踩这个坑，合并之前，先用 `dtypes` 看一眼两边的键是不是同一个类型。

## 2、两张表有同名的列

再看一种情况。下面这段代码，先按书算出平均分，把列名改成 `id` 和 `rating` ，再拼回书目表，最后打印拼好的表都有哪些列：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
stats = reviews.groupby('book_id')['score'].mean().round(1).reset_index()
stats.columns = ['id', 'rating']
table = books.merge(stats, on='id')
print(list(table.columns))
```

输出的结果：

```
['id', 'title', 'author', 'category', 'price', 'rating_x', 'reviews', 'stock', 'pages', 'year', 'rating_y']
```

先说说代码里的两处新写法：

- `stats.columns = [...]` 是给表的列重新起名字。
- 两边键的列名一样时，用 `on='id'` 一个参数就够了。

再来看问题出在哪儿。书目表里本来就有 `rating` ，自己算的评分也叫 `rating` 。两列重名了，pandas 只好给它们加上后缀：左边的叫 `rating_x` ，右边的叫 `rating_y` 。可是过一阵子再看，谁还记得 x 是哪个、y 是哪个？

所以，合并之前，最好给要拼进来的列起个不重名、又看得懂的名字，比如 `avg_score` 。另外，`merge()` 也有个 `suffixes` 参数，可以自己定后缀。

## 3、合并以后，行变多了

最后这个坑最不容易发现，因为它不报错。下面分别用书目表和合并后的表，把书的价格加起来：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
merged = reviews.merge(books, left_on='book_id', right_on='id')
print(round(books['price'].sum(), 1))
print(round(merged['price'].sum(), 1))
```

输出的结果：

```
6981.4
49730.7
```

用书目表算，把书店里每种书各买一本，要 6981.4 元。可用合并后的表一算，却变成了将近五万元。这是怎么回事呢？

原因在于，合并以后的表是**每条评分一行**。比如 1 号书有 13 条评分，它的价格就在表里出现了 13 次。拿这张表去算和书有关的合计，同一本书就被多算了好多遍。

像这样，一本书对应好几条评分，叫做「一对多」。所以合并以后，表的每一行代表什么，心里要有数：这张表一行是一条评分，就只适合算和评分有关的数；要算和书有关的，就回到书目表去算。

坑看完了，先做一道练习：把两张表合并起来，看看编程书一共收到了几条评分，平均几分。

# 六、自己查一次文档

第三节用 `how='left'` ，把没有评分的书也留了下来。那么，这 11 本到底是哪几本呢？一个办法是去找 `count` 是 `NaN` 的行。不过，`merge()` 会不会有更直接的办法，能告诉我们每一行是怎么来的？

这种事，去文档里查一查最靠谱：[DataFrame.merge](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.DataFrame.merge.html) 。

打开以后看参数列表，`how` 、`on` 、`left_on` 、`right_on` 、`suffixes` 这些都见过了。再往下，有一个 `indicator` 。它的说明是：设成 `True` ，结果里就会多出一列 `_merge` ，记下每一行的来历。这一列的值有三种：

- `both` ：两边都有，对上号了。
- `left_only` ：只在左边的表里有。
- `right_only` ：只在右边的表里有。

查到了，就动手试一试：

```python
import pandas as pd

books = pd.read_csv('books.csv')
reviews = pd.read_csv('book_reviews.csv')
stats = reviews.groupby('book_id')['score'].agg(['count', 'mean']).reset_index()
table = books.merge(stats, left_on='id', right_on='book_id', how='left', indicator=True)
print(table['_merge'].value_counts())
print(table[table['_merge'] == 'left_only'][['id', 'title', 'rating']])
```

输出的结果：

```
_merge
both          109
left_only      11
right_only      0
Name: count, dtype: int64
      id           title  rating
2      3        早起养花     NaN
21    22  轻松学网页开发     NaN
22    23      光影的秘密     NaN
41    42      月亮找朋友     NaN
45    46      看懂经济学     NaN
56    57      小熊找朋友     NaN
60    61      旧城的钟声     NaN
75    76        长街旧影     NaN
113  114      版式的力量     NaN
114  115      气候的故事     NaN
117  118      光里的秘密     NaN
```

输出分成两部分。前一部分数的是每种来历各有几行：109 本对上了号，11 本只在书目表里。后一部分把这 11 本挑了出来，一看，书目表里它们的 `rating` 也正好是空的。也就是说，两张表说的是同一件事，彼此对得上，心里就踏实了。

所以，`indicator` 特别适合在合并以后做检查：有多少行没对上号，又是哪几行。合并前后多看一眼，很多错误就能早早发现。

另外，文档里还有一个参数 `validate` ，可以让 pandas 检查键是不是「一对一」「一对多」。暂时用不上的时候，知道有这么个东西就行。

# 七、小结与回看

这一章，咱们为了回答「哪一类书评分最高」，学会了把几张表拼成一张。回头梳理一下，学到了这几件事：

- 几张表靠**键**对上号，键就像身份证号。数据常常分开存，要分析的时候再合并。
- `左表.merge(右表, left_on=..., right_on=...)` 按键把两张表左右拼起来；键的列名一样时，用 `on=` 就行。
- `how` 决定对不上号的行怎么办：`'inner'` 只留对得上的，`'left'` 留下左边的全部，另外还有 `'right'` 和 `'outer'` 。
- `pd.concat([表1, 表2], ignore_index=True)` 把列一样的几张表上下接起来；`pd.DataFrame(字典的列表)` 可以直接造一张表。
- 常见的坑有三个：键的类型不一样；两张表有同名的列，会被加上 `_x` 、`_y` ；一对多合并以后行变多，和「一」那边有关的数会被重复计算。
- 查文档学会了用 `indicator=True` ，看清每一行是两边都有，还是只在一边。

哪里卡住了，就回去看一看：

- 列表和字典：第 3 章、第 4 章
- 分组汇总：数据分析课第 6 章

到这里，咱们看结果，看的一直都是一行行的数字。下一章换个看法，把这些数画成图：表格里要一行一行比较的东西，画成图，一眼就能看出来。
