# 二、set #

python 的 set 和其他语言类似, 是一个无序不重复元素集, 基本功能包括关系测试和消除重复元素。

set 和 dict 类似，但是 set 不存储 value 值的。


## 1、set 的创建 ##

创建一个 set，需要提供一个 list 作为输入集合

```python
set1=set([123,456,789])
print(set1)
```

输出结果：

```
{456, 123, 789}
```

传入的参数 `[123,456,789]` 是一个 list，而显示的 `{456, 123, 789}` 只是告诉你这个 set 内部有 456, 123, 789 这 3 个元素，显示的顺序跟你参数中的 list 里的元素的顺序是不一致的，这也说明了 set 是无序的。

还有一点，我们观察到输出的结果是在大括号中的，经过之前的学习，可以知道，tuple (元组) 使用小括号，list (列表) 使用方括号, dict (字典) 使用的是大括号，dict 也是无序的，只不过 dict 保存的是 key-value 键值对值，而 set 可以理解为只保存 key 值。

> 注意这里的版本区别：Python 3.7 起，普通字典保证保持键的插入顺序；集合仍不保证插入顺序。字典保持顺序不等于自动按键排序。

回忆一下，在 dict （字典） 中创建时，有重复的 key ，会被后面的 key-value 值覆盖的，而 重复元素在 set 中自动被过滤的。


```python
set1=set([123,456,789,123,123])
print(set1)
```

输出的结果：

```
{456, 123, 789}
```

## 2、set 添加元素 ##

通过 add(key) 方法可以添加元素到 set 中，可以重复添加，但不会有效果

```python
set1=set([123,456,789])
print(set1)
set1.add(100)
print(set1)
set1.add(100)
print(set1)
```

输出结果：
```
{456, 123, 789}
{456, 123, 100, 789}
{456, 123, 100, 789}
```

## 3、set 删除元素 ##

通过 remove(key) 方法可以删除 set 中的元素

```python
set1=set([123,456,789])
print(set1)
set1.remove(456)
print(set1)
```

输出的结果：

```
{456, 123, 789}
{123, 789}
```


## 4、set 的运用 ##

因为 set 是一个无序不重复元素集，因此，两个 set 可以做数学意义上的 union(并集), intersection(交集), difference(差集) 等操作。

用文氏图理解一下三种集合运算：

- Union（并集）：两个圆全部填充，代表两个集合所有的元素合并
- Intersection（交集）：只填充两个圆重叠的中间部分，代表两个集合都有的元素
- Difference（差集）：只填充第一个圆减去与第二个圆重叠的部分，代表第一个集合中有、第二个集合中没有的元素

例子：

```python
set1=set('hello')
set2=set(['p','y','y','h','o','n'])
print(set1)
print(set2)

# 交集 (求两个 set 集合中相同的元素)
set3=set1 & set2
print('\n交集 set3:')
print(set3)
# 并集 （合并两个 set 集合的元素并去除重复的值）
set4=set1 | set2
print('\n并集 set4:')
print(set4)
# 差集
set5=set1 - set2
set6=set2 - set1
print('\n差集 set5:')
print(set5)
print('\n差集 set6:')
print( set6)


# 去除海量列表里重复元素，用 hash 来解决也行，只不过感觉在性能上不是很高，用 set 解决还是很不错的
list1 = [111,222,333,444,111,222,333,444,555,666]  
set7=set(list1)
print('\n去除列表里重复元素 set7:')
print(set7)

```

运行的结果：

```
{'h', 'l', 'e', 'o'}
{'h', 'n', 'o', 'y', 'p'}

交集 set3:
{'h', 'o'}

并集 set4:
{'h', 'p', 'n', 'e', 'o', 'y', 'l'}

差集 set5:
{'l', 'e'}

差集 set6:
{'p', 'y', 'n'}

去除列表里重复元素 set7:
{555, 333, 111, 666, 444, 222}
```


## 5、现代 set 的几个补充 ##

各位童鞋，前面讲的几条 set 用法在 Python 各个版本都能用。这里再补三个现代写法里比较常见的小知识，让你写代码的时候更顺手。

### （1）集合推导式 ###

我们之前学列表的时候，用过列表推导式，比如 `[x * x for x in range(5)]` 。其实 set 也有自己的「集合推导式」，写法几乎一样，只是把外面的方括号换成大括号：

```python
# 取 1 到 10 中所有偶数的平方
squares = {x * x for x in range(1, 11) if x % 2 == 0}
print(squares)
```

输出的结果：

```
{64, 4, 36, 100, 16}
```

是不是发现，最后的结果自动就是「无序、不重复」的，根本不需要再手动调用 `set()` 转一道。

举个更贴近业务的例子，假设水哥想从一堆订单里，提取出「不重复的下单用户」：

```python
orders = [
    {'user': '一点水', 'amount': 100},
    {'user': '两点水', 'amount': 200},
    {'user': '一点水', 'amount': 50},
    {'user': '三点水', 'amount': 300},
]

users = {order['user'] for order in orders}
print(users)
```

输出的结果（顺序可能不同）：

```
{'两点水', '一点水', '三点水'}
```

一行就搞定，比先建空 set 再 `add` 干净多了。

### （2）frozenset：不可变的 set ###

普通的 set 是可变的，可以 `add` 、 `remove` 。可是某些时候，我们想要一个「不能再改」的集合，比如把它当作 dict 的 key，或者放进另一个 set 里。

这时候就要用 `frozenset` ：

```python
fs = frozenset([1, 2, 3])
print(fs)

# 可以做集合运算
print(fs & frozenset([2, 3, 4]))

# 可以当作 dict 的 key
config = {frozenset(['admin', 'editor']): '后台权限'}
print(config[frozenset(['editor', 'admin'])])
```

输出的结果：

```
frozenset({1, 2, 3})
frozenset({2, 3})
后台权限
```

注意最后一段，`frozenset(['admin', 'editor'])` 和 `frozenset(['editor', 'admin'])` 是相等的——因为 set 本来就无序——所以两次查找命中的是同一个 key。

### （3）什么时候该用 set 而不是 list ###

最后这点不是新语法，但是很重要。我们做「成员判断」的时候，比如 `x in collection` ：

* 如果 `collection` 是 list ，复杂度是 O(n)，元素越多越慢
* 如果 `collection` 是 set （或 dict），复杂度接近 O(1) ，跟元素数量基本无关

所以，如果你的代码里有大量「这个东西在不在那一堆里」的判断，把那一堆从 list 转成 set，往往能让性能瞬间起飞：

```python
# 有 10 万个用户名，要判断某个名字在不在
names_list = [f'user_{i}' for i in range(100000)]
names_set = set(names_list)

# 这两种写法结果一样，但是后者快得多
print('user_99999' in names_list)
print('user_99999' in names_set)
```

输出的结果：

```
True
True
```

是不是发现，set 的价值不光是「去重」，更重要的是「快查」。各位以后在写代码的时候，遇到「频繁的 in 判断」，就可以考虑把那个集合换成 set。

