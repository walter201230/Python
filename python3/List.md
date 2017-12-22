# 一、List（列表） #

Python 内置的一种数据类型是列表：list。 list 是一种有序的集合，可以随时添加和删除其中的元素。

## 1、创建 List（列表） ##

创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可,且列表的数据项不需要具有相同的类型

```python
list1=['两点水','twowter','liangdianshui',123]
```

## 2、访问 List（列表）中的值 ##

使用下标索引来访问列表中的值，同样你也可以使用方括号的形式截取字符

```python
list1=['两点水','twowter','liangdianshui',123]
# 通过索引来访问列表
print(list1[2])
# 通过方括号的形式来截取列表中的数据
print(list1[0:2])
```

输出的结果：

![访问 List（列表）中的值](http://upload-images.jianshu.io/upload_images/2136918-ab562ada6ba08848?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 3、更新 List（列表） ##

可以通过索引对列表的数据项进行修改或更新，也可以使用 append() 方法来添加列表项。

```python
list1=['两点水','twowter','liangdianshui',123]
print(list1)
# 通过索引对列表的数据项进行修改或更新
list1[2]=456
print(list1)
# 使用 append() 方法来添加列表项
list1.append('hello');
print(list1)
```

输出的结果：

![更新 List（列表）](http://upload-images.jianshu.io/upload_images/2136918-96de950da2563ac6?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 4、删除 List（列表） ##

使用 del 语句来删除列表的的元素

```python
list1=['两点水','twowter','liangdianshui',123]
print(list1)
# 使用 del 语句来删除列表的的元素
del list1[3]
print(list1)
```

输出的结果:

![删除 List（列表）](http://upload-images.jianshu.io/upload_images/2136918-e761bf56f583089f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 5、List（列表）运算符 ##

列表对 + 和 * 的操作符与字符串相似。+ 号用于组合列表，* 号用于重复列表。

|Python 表达式|结果|描述|
|-----------|-----|-----|
|len([1, 2, 3])|3|计算元素个数|
|[1, 2, 3] + [4, 5, 6]|	[1, 2, 3, 4, 5, 6]|	组合|
|['Hi!'] * 4|['Hi!', 'Hi!', 'Hi!', 'Hi!']|复制|
|3 in [1, 2, 3]|True|元素是否存在于列表中|
|for x in [1, 2, 3]: print x,|1 2 3|迭代|

## 6、List （列表）函数&方法 ##

|函数&方法|描述|
|----|----|
|cmp(list1, list2)|比较两个列表的元素|
|len(list)|列表元素个数|
|max(list)|返回列表元素最大值|
|min(list)|返回列表元素最小值|
|list(seq)|将元组转换为列表|
|list.append(obj)|在列表末尾添加新的对象|
|list.count(obj)|统计某个元素在列表中出现的次数|
|list.extend(seq)|在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）|
|list.index(obj)|从列表中找出某个值第一个匹配项的索引位置|
|list.insert(index, obj)|将对象插入列表|
|list.pop(obj=list[-1])|移除列表中的一个元素（默认最后一个元素），并且返回该元素的值|
|list.reverse()|反向列表中元素|
|list.sort([func])|对原列表进行排序|


## 7、实例 ##


最后通过一个例子来熟悉了解 List 的操作

例子：

```python
#-*-coding:utf-8-*-
#-----------------------list的使用----------------------------------

# 1.一个产品，需要列出产品的用户，这时候就可以使用一个 list 来表示
user=['liangdianshui','twowater','两点水']
print('1.产品用户')
print(user)

# 2.如果需要统计有多少个用户，这时候 len() 函数可以获的 list 里元素的个数
len(user)
print('\n2.统计有多少个用户')
print(len(user))

# 3.此时，如果需要知道具体的用户呢？可以用过索引来访问 list 中每一个位置的元素，索引是0从开始的
print('\n3.查看具体的用户')
print(user[0]+','+user[1]+','+user[2])

# 4.突然来了一个新的用户，这时我们需要在原有的 list 末尾加一个用户
user.append('茵茵')
print('\n4.在末尾添加新用户')
print(user)

# 5.又新增了一个用户，可是这个用户是 VIP 级别的学生，需要放在第一位，可以通过 insert 方法插入到指定的位置
# 注意：插入数据的时候注意是否越界，索引不能超过 len(user)-1
user.insert(0,'VIP用户')
print('\n5.指定位置添加用户')
print(user)

# 6.突然发现之前弄错了，“茵茵”就是'VIP用户'，因此，需要删除“茵茵”；pop() 删除 list 末尾的元素
user.pop()
print('\n6.删除末尾用户')
print(user)

# 7.过了一段时间，用户“liangdianshui”不玩这个产品，删除了账号
# 因此需要要删除指定位置的元素，用pop(i)方法，其中i是索引位置
user.pop(1)
print('\n7.删除指定位置的list元素')
print(user)

# 8.用户“两点水”想修改自己的昵称了
user[2]='三点水'
print('\n8.把某个元素替换成别的元素')
print(user)

# 9.单单保存用户昵称好像不够好，最好把账号也放进去
# 这里账号是整数类型，跟昵称的字符串类型不同，不过 list 里面的元素的数据类型是可以不同的
# 而且 list 元素也可以是另一个 list
newUser=[['VIP用户',11111],['twowater',22222],['三点水',33333]]
print('\n9.不同元素类型的list数据')
print(newUser)

```

![list的使用](http://upload-images.jianshu.io/upload_images/2136918-65d31cae9f8bb34d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
