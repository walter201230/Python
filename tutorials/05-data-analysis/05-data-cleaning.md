# 数据分析第 5 章：把数据洗干净

# 前言

上一章结尾说过，这一章要换一份数据。为什么要换呢？因为前面几章用的记账本，是一份整理好的数据：每个日期都是同一种写法，每个金额都是数字，也没有空着的地方。

可真实的数据，很少有这么规矩的。手机上随手记的账，有时金额后面多打了一个「元」，有时手一抖记了两遍，有时忘了选类别，有时又多按了几个 9。这些问题要是不解决，后面算出来的数，就全都不可信了。

把数据收拾干净的过程，叫**数据清洗**。它不像画图那样好看，却是分析里最花时间、也最见功夫的一步。在第 1 章说的六个步骤里，它排在第三。

这一章要用的，是 `ledger_2026_raw.csv` ：11 月上半月的一份原始账单，一共 64 行。它在网页里已经准备好了，直接读就行。

**学这一章之前**，需要先学完 [数据分析课第 4 章](04-descriptive-stats.md) 。

# 目录

这一章会学到：

- 一、先做个体检——问题都藏在哪儿
- 二、空着的值——删掉还是补上
- 三、重复的行——`duplicated()` 和 `drop_duplicates()`
- 四、统一格式——去掉「元」，把文字变成数字和日期
- 五、明显不对的值——异常值，以及一份完整的清洗代码
- 六、常见坑
- 七、自己查一次文档——`to_datetime()` 的 `format='mixed'`
- 八、小结与回看

学完这一章，拿到一份乱糟糟的数据，你知道该从哪儿下手，一步一步把它收拾干净。

# 一、先做个体检

拿到一份乱糟糟的数据，先别急着改。就像看病要先体检一样，得先弄清楚问题都藏在哪儿。拿什么来体检呢？第 2 章学的那几招，正好派上用场。先用 `info()` 看看整体的情况：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
raw.info()
```

输出的结果：

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 64 entries, 0 to 63
Data columns (total 5 columns):
 #   Column    Non-Null Count  Dtype 
---  ------    --------------  ----- 
 0   date      64 non-null     object
 1   item      64 non-null     object
 2   category  61 non-null     object
 3   cost      62 non-null     object
 4   payment   64 non-null     object
dtypes: object(5)
memory usage: 1.3+ KB
```

一眼就能看出两个问题：

- 一共 64 行，可 `category` 只有 61 个非空值，`cost` 只有 62 个，说明这两列都有空着的地方。
- `cost` 的类型是 `object` ，不是数字。第 2 章说过，这说明金额这一列里，混进了不是数字的东西。

不过，`info()` 只告诉我们哪里有问题，却看不出问题具体长什么样。所以再用 `head(8)` 看看开头 8 行：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
print(raw.head(8))
```

输出的结果：

```
         date      item category    cost payment
0  2026-11-01      房租     居住    2500  银行卡
1  2026-11-01  水电燃气     居住   229.5  支付宝
2  2026-11-01      早饭     餐饮       8  支付宝
3  2026-11-01      午饭     餐饮  22.5元    微信
4  2026-11-01      晚饭     餐饮      27    微信
5  2026-11-02      早饭     餐饮     10   支付宝
6  2026-11-02      午饭     餐饮      29  支付宝
7  2026-11-02      晚饭      NaN      58    微信
```

仔细看，问题就出来了：

- 行号为 3 的那一行，金额写成了 `22.5元` 。
- 行号为 5 的那一行，`10` 有点歪，因为它前后多了空格。
- 行号为 7 的那一行，类别是 `NaN` ，也就是空着。

光看开头 8 行，就找出了三个问题，后面还有多少呢？一个一个地找就太慢了。所以接下来，咱们一类一类地收拾，先从空着的值开始。

# 二、空着的值

先来收拾空着的值。第一步，是弄清楚每一列各空了几个。`isna()` 能判断每个值是不是空的，得到一串 `True` 和 `False` 。和第 3 章一样，再 `sum()` 一下，就知道有几个空的：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
print(raw.isna().sum())
```

输出的结果：

```
date        0
item        0
category    3
cost        2
payment     0
dtype: int64
```

这里是对整张表用 `isna()` ，再 `sum()` ，所以每一列有几个空值，一下子全出来了：类别空了 3 个，金额空了 2 个。

光知道个数还不够，还得看看具体是哪几行。把它们挑出来：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
print(raw[raw['cost'].isna()])
print(raw[raw['category'].isna()])
```

输出的结果：

```
          date  item category cost payment
21  2026-11-06  早饭     餐饮  NaN    微信
52  2026-11-13  地铁     交通  NaN  支付宝
          date  item category cost payment
7   2026-11-02  晚饭      NaN   58    微信
31  2026-11-08  午饭      NaN   26  支付宝
55  2026-11-14  打车      NaN   29    微信
```

那这些空值该怎么处理呢？其实没有标准答案，要看缺的是什么：

- **金额空了**：比如那顿早饭，到底吃了多少钱？没法知道。瞎猜一个数，只会让结果更不准。所以这种就**删掉**。
- **类别空了**：晚饭、午饭肯定是餐饮，打车肯定是交通，这是能推断出来的。所以这种就**补上**。

先说删。删掉用 `dropna()` ，再用 `subset` 说明看哪几列：这几列有空的，才删。

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
has_cost = raw.dropna(subset=['cost'])
print(len(raw), len(has_cost))
```

输出的结果：

```
64 62
```

64 行删掉了金额空着的 2 行，剩下 62 行。

再说补。补上用 `fillna()` 。它可以填同一个值，比如 `fillna('未分类')` ；也可以拿另一列来填，同一行的值对着填进去。这里先用 `map()` 按名称查出类别，再拿查出来的结果去填：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
guess = raw['item'].map({'午饭': '餐饮', '晚饭': '餐饮', '打车': '交通'})
raw['category'] = raw['category'].fillna(guess)
print(raw.loc[[7, 31, 55]])
print(raw['category'].isna().sum())
```

输出的结果：

```
          date  item category cost payment
7   2026-11-02  晚饭     餐饮   58    微信
31  2026-11-08  午饭     餐饮   26  支付宝
55  2026-11-14  打车     交通   29    微信
0
```

这段代码有四个地方要说一下：

- `map(字典)` 会拿这一列的每个值去查字典：午饭查到餐饮，打车查到交通，查不到的就是 `NaN` 。
- `fillna(guess)` 只填空着的地方，原来有类别的，它不会动。
- `raw['category'] = ...` 是把结果放回去，替换掉原来那一列。
- `loc[[7, 31, 55]]` 方括号里是一个行号的列表，能一次挑出这三行，方便看看补得对不对。

最后输出的 0 说明，三个空着的类别都补上了。

那要是实在推断不出来呢？先做一道练习：把空着的类别都填成「未分类」。

# 三、重复的行

空值收拾好了，再来看第二类问题：重复。同一笔账要是记了两遍，总额就会多算一笔。怎么把重复的找出来呢？用 `duplicated()` ，它会找出和前面某一行**完全一样**的行：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
print(raw.duplicated().sum())
print(raw[raw.duplicated(keep=False)])
```

输出的结果：

```
2
          date  item category  cost payment
29  2026-11-08  早饭     餐饮    15  支付宝
30  2026-11-08  早饭     餐饮    15  支付宝
38  2026-11-10  午饭     餐饮  21元    微信
39  2026-11-10  午饭     餐饮  21元    微信
```

第一行输出说，有 2 行是重复的。可下面为什么列出了 4 行呢？因为默认情况下，`duplicated()` 只把第二次出现的那一行标成 `True` ，第一次出现的不算；而第二次打印的时候，加上了 `keep=False` ，重复的几行就全都标了出来，方便对照着看。

再看看这几行：同一天、同一种饭、同样的金额、同样的付款方式，还挨在一起，八成是记重了。要去掉它们，就用 `drop_duplicates()` ，每组只留第一行：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
no_dup = raw.drop_duplicates()
print(len(raw), len(no_dup))
```

输出的结果：

```
64 62
```

64 行去掉了 2 行，剩下 62 行。

不过，删之前要先想一想：一模一样的两行，**一定**是记重了吗？要是那天真的买了两杯一样的奶茶呢？账本里没有「时间」这一列，光凭这几列，是分不出来的。

这份账单里，挨在一起的重复行，我们判断为记重了。可要是换一份数据，就得重新判断。所以说，清洗数据不只是敲代码，每删一行、每补一个值，都是在做一个判断。最好把这些判断记下来，这样别人看你的结果时，也知道你是怎么处理的。

# 四、统一格式

空值和重复都处理了，还剩下体检时发现的另一类问题：格式不统一。先说金额，再说日期。

## 1、金额：去掉空格和「元」

要去掉空格和「元」，字符串有 `strip()` 、`replace()` 这些方法，实战 1、实战 3 都用过。可问题是，`raw['cost']` 是一整列，怎么对每个值都用一遍呢？

办法是在列后面加上 `.str` ，这样就能对整列用字符串的方法了：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
cost = raw['cost'].str.strip().str.replace('元', '')
print(raw['cost'].head(6).tolist())
print(cost.head(6).tolist())
```

输出的结果：

```
['2500', '229.5', '8', '22.5元', '27', ' 10 ']
['2500', '229.5', '8', '22.5', '27', '10']
```

对比一下前后两行：

- `str.strip()` 去掉了每个值前后的空格，` 10 ` 变成了 `10` 。
- `str.replace('元', '')` 把「元」换成空字符串，也就是去掉了它，`22.5元` 变成了 `22.5` 。

不过仔细看会发现，它们都还带着引号，说明还是字符串。所以还要再用 `astype(float)` ，把整列变成小数：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
raw['cost'] = raw['cost'].str.strip().str.replace('元', '').astype(float)
print(raw['cost'].dtype)
print(raw['cost'].head(6).tolist())
```

输出的结果：

```
float64
[2500.0, 229.5, 8.0, 22.5, 27.0, 10.0]
```

类型变成了 `float64` ，这下就可以加减、求平均了。那空着的金额呢？`.str` 的方法会跳过它，转换以后，它还是空值 `NaN` 。

## 2、日期：统一写法，变成真正的日期

金额收拾好了，再来看日期。日期有什么问题呢？先找找有没有用斜杠写的：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
print(raw[raw['date'].str.contains('/')])
```

输出的结果：

```
          date  item category cost payment
11  2026/11/03  地铁     交通    3  银行卡
42  2026/11/11  早饭     餐饮  -15  银行卡
```

果然，有两行的日期是用斜杠隔开的。这里用到的 `str.contains()` ，会判断每个值里有没有某个字符串，和 `in` 的意思一样。

写法不一样，又有什么要紧的呢？要知道，日期还是文字的时候，`2026/11/03` 和 `2026-11-03` 是两个不同的值。按日期汇总，同一天就会被分成两天。所以要先把斜杠换成短横线，再用 `pd.to_datetime()` 把它变成**真正的日期**：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
raw['date'] = pd.to_datetime(raw['date'].str.replace('/', '-'))
print(raw['date'].dtype)
print(raw['date'].head(3))
```

输出的结果：

```
datetime64[ns]
0   2026-11-01
1   2026-11-01
2   2026-11-01
Name: date, dtype: datetime64[ns]
```

类型变成了 `datetime64[ns]` ，这是 pandas 的日期类型。看上去和原来差不多，可它现在知道这是哪年哪月哪天了。这有什么用呢？在日期列后面加上 `.dt` ，就能取出年、月、日，甚至是星期几：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
raw['date'] = pd.to_datetime(raw['date'].str.replace('/', '-'))
print(raw['date'].dt.month.head(3).tolist())
print(raw['date'].dt.day.head(3).tolist())
print(raw['date'].dt.dayofweek.head(3).tolist())
```

输出的结果：

```
[11, 11, 11]
[1, 1, 1]
[6, 6, 6]
```

三行输出依次是：

- `dt.month` 是月。
- `dt.day` 是日。
- `dt.dayofweek` 是星期几：0 是星期一，6 是星期日。2026 年 11 月 1 日，正好是星期日。

可以看出来，文字有 `.str` ，日期有 `.dt` ，两者是一个道理：对整列的每个值，做同一件事。下一章按月汇总一整年的账，用的就是 `dt.month` 。

格式统一好了，先做一道练习：数一数，这份账单一共记了几天。

# 五、明显不对的值

空值、重复、格式，这三类问题都处理了。还有没有别的问题呢？格式统一以后，金额变成了数字，这下就能用 `describe()` 来看看了：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
raw['cost'] = raw['cost'].str.strip().str.replace('元', '').astype(float)
print(raw['cost'].describe())
```

输出的结果：

```
count      62.000000
mean      236.241935
std      1299.762269
min       -15.000000
25%        12.875000
50%        22.250000
75%        33.625000
max      9999.000000
Name: cost, dtype: float64
```

第 2 章说过，`describe()` 是用来发现问题的。这里就有两个问题：最大值是 9999，最小值是 -15。到底是哪几笔呢？把它们挑出来看看：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
raw['cost'] = raw['cost'].str.strip().str.replace('元', '').astype(float)
print(raw[(raw['cost'] > 3000) | (raw['cost'] <= 0)])
```

输出的结果：

```
          date  item category    cost payment
34  2026-11-09  午饭     餐饮  9999.0  支付宝
42  2026/11/11  早饭     餐饮   -15.0  银行卡
```

一顿午饭 9999 元，多半是手滑多按了几个 9；早饭 -15 元，也许是退款，也许是记错了。像这种明显不合常理的值，就叫**异常值**。

那异常值该怎么处理呢？还是要看情况。能问到记账的人，最好问清楚，再改正过来；问不到，又明显不对，就删掉。这份账单里，房租 2500 元是最大的正常花销，所以我们定一个规则：金额要大于 0，并且不超过 3000 元。

到这里，每一类问题都有了处理办法。把前面几节的步骤串起来，就是一份完整的清洗代码：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')

# 1. 去掉重复的行，删掉金额空着的行
ledger = raw.drop_duplicates().dropna(subset=['cost']).copy()
# 2. 按名称补上空着的类别
guess = ledger['item'].map({'午饭': '餐饮', '晚饭': '餐饮', '打车': '交通'})
ledger['category'] = ledger['category'].fillna(guess)
# 3. 统一金额和日期的格式
ledger['cost'] = ledger['cost'].str.strip().str.replace('元', '').astype(float)
ledger['date'] = pd.to_datetime(ledger['date'].str.replace('/', '-'))
# 4. 去掉异常值
ledger = ledger[(ledger['cost'] > 0) & (ledger['cost'] <= 3000)]

ledger.info()
print(ledger['cost'].sum())
```

输出的结果：

```
<class 'pandas.core.frame.DataFrame'>
Index: 58 entries, 0 to 63
Data columns (total 5 columns):
 #   Column    Non-Null Count  Dtype         
---  ------    --------------  -----         
 0   date      58 non-null     datetime64[ns]
 1   item      58 non-null     object        
 2   category  58 non-null     object        
 3   cost      58 non-null     float64       
 4   payment   58 non-null     object        
dtypes: datetime64[ns](1), float64(1), object(3)
memory usage: 2.0+ KB
4627.0
```

清洗完了，最后再做一次体检：58 行，每一列都没有空值，日期是日期，金额是数字。原来的 64 行里，去掉了 2 行重复、2 行没有金额、2 行异常值。

细心的童鞋可能发现了，第 1 步那一行代码的最后，多了一个 `.copy()` 。为什么要加它呢？下一节的第 3 个坑会讲。在那之前，先做一道练习：照着这份清洗代码，把洗干净的账单按类别汇总一下。

# 六、常见坑

清洗数据的步骤多，先后顺序、参数怎么写，一不小心就会出错。下面这四个坑，都是刚学清洗时最容易碰到的。

## 1、先转类型，后去单位

要是不先去掉「元」，直接转成小数，会怎么样呢？

<!-- skip-ci -->
```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
cost = raw['cost'].astype(float)
```

报错信息的最后一行是：

```
ValueError: could not convert string to float: '22.5元'
```

`22.5元` 不是一个数，`float()` 不认识它，只好报错。好在报错信息把出问题的那个值也告诉了你，照着它去找就行。所以顺序很重要：先用 `.str` 的方法收拾干净，再转类型。

## 2、dropna() 删多了

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
print(len(raw.dropna()))
print(len(raw.dropna(subset=['cost'])))
```

输出的结果：

```
59
62
```

两种写法，剩下的行数不一样。为什么呢？因为 `dropna()` 不写 `subset` 的话，只要一行里**任何一列**有空值，整行就会被删掉。那 3 行只是缺了类别，金额是好好的，本来能补上，结果也被一起删了。

所以删数据之前，先想清楚：是哪一列的空值要处理？然后用 `subset` 写明白。

## 3、改了挑出来的表

这就是上一节留下的问题：为什么要加 `.copy()` ？先看看不加会怎么样：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
meals = raw[raw['category'] == '餐饮']
meals['cost'] = meals['cost'].str.strip()
```

代码没有报错，可输出区会出现一段警告，最后几行是：

```
See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  meals['cost'] = meals['cost'].str.strip()
```

警告的开头写着 `SettingWithCopyWarning` 。它的意思是：你正在一份「从别的表里挑出来的数据」上改东西。这一改，会不会影响到原来的 `raw` 呢？pandas 也说不准，所以提醒你一下。

解决办法很简单：挑出来以后，马上 `.copy()` 一份。这就等于明明白白地告诉 pandas：这是一张新表，改它不关原表的事。

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
meals = raw[raw['category'] == '餐饮'].copy()
meals['cost'] = meals['cost'].str.strip()
print(len(meals))
```

输出的结果：

```
47
```

这回就没有警告了。所以挑出一部分以后，要是接着要改它的列，记得加上 `.copy()` 。上一节那份完整的清洗代码里，第 1 步就是这么做的。

## 4、清洗完不检查

清洗代码写完了，也跑通了，并不代表数据就洗干净了。所以最后一定要再体检一次：

- `info()` 看空值和类型。
- `describe()` 看最大值和最小值。
- `duplicated().sum()` 看还有没有重复。

上一节最后的 `info()` ，就是在做这件事。

# 七、自己查一次文档

第四节先把斜杠换成了短横线，才交给 `pd.to_datetime()` 。那要是不换，直接转，会怎么样呢？试一下：

<!-- skip-ci -->
```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
dates = pd.to_datetime(raw['date'])
```

报错信息的最后几行是：

```
ValueError: time data "2026/11/03" doesn't match format "%Y-%m-%d", at position 3. You might want to try:
    - passing `format` if your strings have a consistent format;
    - passing `format='ISO8601'` if your strings are all ISO8601 but not necessarily in exactly the same format;
    - passing `format='mixed'`, and the format will be inferred for each element individually. You might want to use `dayfirst` alongside this.
```

报错有好几行，咱们一行一行地看。

第一行说的是：`2026/11/03` 和格式 `%Y-%m-%d` 对不上。为什么会对不上呢？因为 pandas 看了前面的日期，以为都是「年-月-日」的写法，碰到斜杠，就认不出来了。

后面三行，是 pandas 给的建议。其中第三条说：可以传 `format='mixed'` ，每个值的格式单独推断；还提醒最好和 `dayfirst` 一起用。

这两个参数是什么意思呢？报错信息没有细说，那就去看文档：[pandas.to_datetime](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.to_datetime.html) 。

找到 `format` 参数。平时它写的是一个格式字符串，比如 `"%d/%m/%Y"` ；还可以写成 `"mixed"` ，为每个值单独推断格式。紧接着还有一句：这样做有风险，你大概应该和 `dayfirst` 一起用。

「有风险」先放一放，先试试它管不管用：

```python
import pandas as pd

raw = pd.read_csv('ledger_2026_raw.csv')
dates = pd.to_datetime(raw['date'], format='mixed')
print(raw['date'].nunique())
print(dates.nunique())
```

输出的结果：

```
17
15
```

管用。还是文字的时候，`2026/11/03` 和 `2026-11-03` 算两种，所以一共 17 种；变成日期以后，它们就是同一天了，正好 15 天。

那文档说的「有风险」，指的又是什么呢？看下面这个例子：

```python
import pandas as pd

s = pd.Series(['2026-11-03', '03/04/2026'])
print(pd.to_datetime(s, format='mixed').tolist())
print(pd.to_datetime(s, format='mixed', dayfirst=True).tolist())
```

输出的结果：

```
[Timestamp('2026-11-03 00:00:00'), Timestamp('2026-03-04 00:00:00')]
[Timestamp('2026-11-03 00:00:00'), Timestamp('2026-04-03 00:00:00')]
```

问题出在 `03/04/2026` 上：它到底是 3 月 4 日，还是 4 月 3 日？美国人习惯月在前，很多别的地方习惯日在前，光看这几个数字，是分不出来的。pandas 默认按月在前来理解；加上 `dayfirst=True` ，才会按日在前。要命的是，猜错了也不会报错，日期就这么悄悄地错了。

这就是文档说的风险。所以，能自己把写法统一的，就像第四节那样，先统一，再转换，这样心里最有数；写法实在太多、统一不过来的，再用 `format='mixed'` ，并且要想清楚日和月谁在前。

从这次也能看出来：报错信息里的建议，是查文档最好的入口。它不光告诉你哪里错了，还告诉你该去看哪个参数。

# 八、小结与回看

这一章，咱们把一份乱糟糟的账单，一步一步收拾干净了。回头梳理一下，学到了这几件事：

- 先体检：`info()` 看空值和类型，`head()` 看实际的样子；`isna().sum()` 能数出每一列有几个空值。
- 空值：推断不出来的，用 `dropna(subset=[...])` 删掉；推断得出来的，用 `fillna()` 补上，再配合 `map(字典)` 按另一列查出要填的值。
- 重复：`duplicated()` 能找出来，加上 `keep=False` 会全部标出；`drop_duplicates()` 能去掉。删之前要想清楚，是不是真的记重了。
- 格式：`.str` 能对整列用字符串的方法，比如 `strip()` 、`replace()` 、`contains()` ；`astype(float)` 能变成数字；`pd.to_datetime()` 能变成日期，再用 `.dt.month` 、`.dt.day` 、`.dt.dayofweek` 取出月、日、星期几。
- 异常值：先用 `describe()` 看最大值和最小值，再挑出来看，最后定一个规则去掉。
- 常见的坑：先转类型、后去单位；`dropna()` 删多了；改挑出来的表，要先 `.copy()` ；洗完以后，再体检一次。
- 查文档弄懂了 `format='mixed'` 和 `dayfirst` ：每个值单独推断日期格式，很方便，但有猜错的风险。

哪里卡住了，就回去看一看：

- 字符串的 `strip()` ：实战 1 的「五、常见坑」；`replace()` ：实战 3 的「四、输错了，别崩」
- 字典：第 4 章

最后还想说一句：每一个删除、补全的决定，都会影响最后的结论。所以清洗代码最好像第五节那样，写成完整的一段，每一步都加上注释，这样别人一看，就知道你做了哪些判断。

数据洗干净了，就可以放心地算了。下一章，咱们回到干净的记账本，学 pandas 里最有用的一招：分组汇总。每个月花了多少？每个类别每个月花了多少？一行代码就能算出来。
