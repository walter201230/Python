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

![set集合运算](http://upload-images.jianshu.io/upload_images/2136918-733b1d1071f772bd?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

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


