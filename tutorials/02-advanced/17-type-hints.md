学完前面的章节，相信各位已经能写出像模像样的 Python 代码了。函数、类、闭包、装饰器，一路下来都不是事儿。可是啊，写代码这件事，自己写得爽是一回事，给别人看，或者半年后自己再回来看，就是另一回事了。

来，我们看一段「水哥」上周刚交接给童鞋的代码：

```python
def calc(x, y, op):
    if op == 'add':
        return x + y
    elif op == 'sub':
        return x - y
```

童鞋看着这个 `calc` 一脸懵：`x` 和 `y` 到底是数字还是字符串？`op` 还能传啥？返回的是啥类型？只能跑去翻调用方的代码，或者直接喊「水哥，这函数到底咋用啊」。

这种场景，是不是特别熟悉？Python 是动态语言，变量不需要声明类型，写起来确实痛快，可一旦项目大起来、人多起来，就特别容易翻车。

各位再想想，这种「类型不明」的代码会带来什么后果：

- 调用方传错类型，自己写代码时还没发觉，等部署上线、用户点了某个按钮才崩溃
- IDE 没法给你精准的代码补全——它都不知道你这个变量是啥，怎么提示有哪些方法可以用？
- 重构时心里没底——把这个函数的参数改了，到底会影响到哪些地方？只能全文搜索，搜完还要一行行肉眼看
- 团队协作里反复打断别人——每次你想用一个不熟的函数都要去问作者「这个参数是啥意思」

为了解决这个问题，从 Python 3.5 开始，官方就引入了「类型注解」（Type Hints）这套机制。再到 3.9、3.10、3.12，一路演变到现在，已经非常好用了。可惜的是，市面上很多老教程都没怎么讲，导致很多童鞋写了好几年 Python 还是 `def f(x, y)` 啥都不写。

各位想想，假如有这么一个场景：「水哥」周末临时请假，把手头的项目交接给童鞋。代码里有几十个函数，每个函数都长成 `def process(data, config, cb)` 这副样子。童鞋打开一个文件就懵了——`data` 是字典还是列表？`config` 是对象还是路径？`cb` 是函数还是字符串？每一处都得跑去问，要么就翻一遍调用栈。这一个周末，怕是整个人都得搭进去。

而如果一开始函数签名是 `def process(data: dict[str, int], config: Path, cb: Callable[[str], None])`，童鞋一眼就明白了，连问都不用问。这就是类型注解最直接的价值。

那今天这篇，就专门聊聊类型注解，让各位写出来的代码更清晰、更专业。



## 最简单的注解

我们先把上面那段 `calc` 改造一下。假设它就是处理两个整数的加减：

```python
def calc(x: int, y: int, op: str) -> int:
    if op == 'add':
        return x + y
    elif op == 'sub':
        return x - y
    return 0


print(calc(3, 5, 'add'))
print(calc(10, 4, 'sub'))
```

输出结果：

```
8
6
```

是不是发现，现在这个函数一眼就能看明白：`x` 和 `y` 是 `int`，`op` 是 `str`，返回值也是 `int`。就算没有任何注释，光看签名就够了。

注解的语法很简单，记住两点：

- 参数后面用 `: 类型` 标注
- 返回值用 `-> 类型` 标注

记住这个比例：「参数加冒号，返回加箭头」。语法上跟原来的写法 100% 兼容，没注解的旧代码不需要改一行字符就能跟有注解的新代码混着跑。

那么有童鞋可能会问：「我能不能只标参数，不标返回值？或者只标返回值，不标参数？」

完全可以，类型注解是「想标哪里标哪里」的，不强制全标。比如：

```python
def double(x: int):
    return x * 2


def greet(name) -> str:
    return f'你好，{name}'


print(double(3))
print(greet('两点水'))
```

输出结果：

```
6
你好，两点水
```

但是从「契约清晰」的角度，建议**要么全标，要么干脆都不标**。半标半不标看着特别割裂，读代码的人会怀疑「漏标的那个是忘了，还是故意的？」

这里有个非常重要的点，各位一定要记住：**Python 解释器并不会强制检查这些类型**。它只是个「说明」，给人看，给工具（IDE、静态检查器）看。

不信我们试试，故意传错类型：

```python
def calc(x: int, y: int) -> int:
    return x + y


print(calc('两点水', '做鸭事业部'))
```

输出结果：

```
两点水做鸭事业部
```

看，明明标了 `int`，传字符串照样能跑，因为字符串本身也支持 `+`，Python 啥都没拦。所以类型注解不是「类型强制」，更像是写给同事看的「契约」。

那有人就要问了：「既然不强制，那加它干啥？」

好问题，答案是：

- IDE（PyCharm、VSCode）能根据注解给你**精准的代码补全和报错提示**
- 静态检查工具（比如 mypy、pyright）能在**代码运行前**就揪出类型错误
- 同事（包括未来的自己）读代码时**省下大把猜测时间**

就这三条，已经足够让我们认真对待它了。



还有一个很多童鞋会困惑的点：「带默认值的参数怎么注解？」很简单，注解写在前面，等号默认值跟在后面：

```python
def punch(name: str, dept: str = '做鸭事业部') -> None:
    print(f'{name}（{dept}）打卡成功')


punch('两点水')
punch('三点水', '做鹅事业部')
```

输出结果：

```
两点水（做鸭事业部）打卡成功
三点水（做鹅事业部）打卡成功
```

格式是 `参数名: 类型 = 默认值`，三个部分依次排好就行。

那 `*args`、`**kwargs` 这种可变参数呢？也能注解，写的是「单个元素」的类型，不是整个 tuple/dict 的类型：

```python
def sum_all(*nums: int) -> int:
    return sum(nums)


def make_user(**fields: str) -> dict[str, str]:
    return fields


print(sum_all(1, 2, 3, 4, 5))
print(make_user(name='两点水', dept='做鸭事业部'))
```

输出结果：

```
15
{'name': '两点水', 'dept': '做鸭事业部'}
```

`*nums: int` 的意思是「`nums` 这个 tuple 里的每个元素都是 int」，不是「`nums` 本身是 int」；`**fields: str` 同理，是说每个 value 都是 str。这点初学时很容易搞错，记一下。



## 常用的几个基础类型

类型注解里能写的类型，基本都是 Python 内置的那些：

| 类型      | 含义                  |
| --------- | --------------------- |
| `int`     | 整数                  |
| `float`   | 浮点数                |
| `str`     | 字符串                |
| `bool`    | 布尔值                |
| `list`    | 列表                  |
| `dict`    | 字典                  |
| `tuple`   | 元组                  |
| `set`     | 集合                  |
| `bytes`   | 字节串                |
| `None`    | 空值（用作返回类型）  |

来个综合例子，给「做鸭事业部」写一个员工档案函数：

```python
def make_profile(name: str, age: int, salary: float, is_active: bool) -> str:
    return f'{name}（{age} 岁，工资 {salary}，在职：{is_active}）'


print(make_profile('两点水', 28, 12000.5, True))
```

输出结果：

```
两点水（28 岁，工资 12000.5，在职：True）
```

各位试一下，把上面这段代码贴到 PyCharm 或者 VSCode 里。当你调用 `make_profile(` 的时候，IDE 会立刻弹出参数提示——「第一个参数 name 是 str，第二个参数 age 是 int……」。要是没有注解，IDE 就只能干瘪地告诉你「这里要四个参数」，啥类型完全靠你脑子记。

是不是发现，注解写一下，开发体验立马上一个台阶？

是不是发现，记这一张表就够大部分场景用了？基础类型本身没什么花哨的，关键是用得「准」——是 `int` 就写 `int`，是 `str` 就写 `str`，别图省事写个 `object` 或者 `Any` 把一切都吃掉。

这里多说几句 `bool` 的注解。Python 里 `bool` 其实是 `int` 的子类（`True == 1`、`False == 0`），所以一个标了 `int` 的参数，传 `True` 进去类型检查器是不报错的。但反过来，标 `bool` 的参数你传个 `1`，检查器就会拦下来。这点平时知道一下就行，写注解还是按「真实意图」来写：开关用 `bool`，数字用 `int`。

再说一个跟 `int` 相关的小坑：Python 的 `int` 是「无限精度」的，没有 `int32`、`int64` 之分，所以注解里也只有一个 `int`。习惯了 C/Java 的童鞋一开始会找「int 32 在哪」，那是没有的——大胆放心地用 `int` 就好。

来看一个实际写「员工档案」时常见的混合签名：

```python
def make_employee(
    name: str,
    age: int,
    height: float,
    is_intern: bool,
    skills: list,
    address: dict,
) -> str:
    return f'{name} / {age} 岁 / {height}m / 实习：{is_intern} / 技能：{skills} / 地址：{address}'


print(make_employee(
    '两点水', 28, 1.75, False,
    ['Python', 'Django'],
    {'city': '深圳', 'street': '科技园'},
))
```

输出结果：

```
两点水 / 28 岁 / 1.75m / 实习：False / 技能：['Python', 'Django'] / 地址：{'city': '深圳', 'street': '科技园'}
```

现在这个签名读起来已经清晰多了，但是仔细看，`skills: list` 和 `address: dict` 这两个还不够好——「列表里装的啥？字典的键值都是啥类型？」我们不知道。这就要靠下一节讲的「容器类型」来进一步细化。

如果一个函数没有返回值（也就是返回 `None`），返回类型写 `None` 就好：

```python
def greet(name: str) -> None:
    print(f'你好，{name}')


greet('两点水')
```

输出结果：

```
你好，两点水
```

注意啊，这里的 `-> None` 不是说「不写返回值」，而是「明确告诉别人这个函数没有有意义的返回值」。这俩在阅读体验上差很多。

那么各位再想一个场景。「做鸭事业部」的上班打卡函数（前面装饰器章节里见过的那个），加上注解之后是这样：

```python
import time


def punch(name: str, dept: str) -> None:
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(f'{today}：昵称：{name}  部门：{dept} 上班打卡成功')


punch('两点水', '做鸭事业部')
```

输出结果（日期会随当前时间变）：

```
2026-04-28：昵称：两点水  部门：做鸭事业部 上班打卡成功
```

各位看，仅仅在签名里加了 `name: str, dept: str` 和 `-> None`，整个函数的「使用契约」就完全交代清楚了——传字符串进去，不会得到任何返回值，行为是打印。换成读者视角，是不是省心多了？



## 函数可能返回 None 怎么办

来设想一个真实的场景。「做鸭事业部」的员工库是个字典，我们写一个根据昵称查工号的函数：

```python
employees = {'两点水': '001', '三点水': '002'}


def find_id(name: str) -> str:
    return employees.get(name)


print(find_id('两点水'))
print(find_id('四点水'))
```

输出结果：

```
001
None
```

看出来问题了吗？我们标的返回类型是 `str`，可实际上当这个员工不存在时，`dict.get()` 返回的是 `None`，不是 `str`。注解和实际行为对不上了。

这种「要么返回 X，要么返回 None」的情况非常常见，老一辈的写法是用 `typing` 模块里的 `Optional`：

```python
from typing import Optional


employees = {'两点水': '001', '三点水': '002'}


def find_id(name: str) -> Optional[str]:
    return employees.get(name)


print(find_id('两点水'))
print(find_id('四点水'))
```

`Optional[str]` 等价于「这个值要么是 `str`，要么是 `None`」。

可是啊，每次都要从 `typing` 导入这个 `Optional`，写多了真的烦。到了 Python 3.10，官方推出了一个更简洁的写法（PEP 604），直接用竖线 `|` 连起来：

```python
employees = {'两点水': '001', '三点水': '002'}


def find_id(name: str) -> str | None:
    return employees.get(name)


print(find_id('两点水'))
print(find_id('四点水'))
```

输出结果：

```
001
None
```

`str | None` 读起来是不是更直白？「字符串或者空值」，跟英语里的 or 一个意思。

这里要重点强调一句：返回类型标 `str | None`，**不是说调用方就能直接当 str 用了**——你必须在使用前判断一下到底是哪种情况。看这段：

<!-- skip-ci -->
```python
def find_id(name: str) -> str | None:
    db = {'两点水': '001'}
    return db.get(name)


emp_id = find_id('四点水')
print(emp_id.upper())
```

上面这段 IDE 会立刻给 `emp_id.upper()` 飘红，因为 `emp_id` 可能是 `None`，`None` 没有 `upper` 方法。正确写法是先判断：

```python
def find_id(name: str) -> str | None:
    db = {'两点水': '001'}
    return db.get(name)


emp_id = find_id('两点水')
if emp_id is not None:
    print(emp_id.upper())
else:
    print('员工不存在')
```

输出结果：

```
001
```

走过这个 `if` 分支之后，类型检查器会「自动收窄」——它知道 `if emp_id is not None:` 内部 `emp_id` 一定是 `str`，于是 `.upper()` 就不报错了。这种聪明劲儿叫「Type Narrowing（类型收窄）」，是现代类型检查器最有用的能力之一。

而且这个 `|` 不止能用来表示 None，可以连接任意多个类型：

```python
def to_int(value: int | str | float) -> int:
    return int(value)


print(to_int(3))
print(to_int('5'))
print(to_int(7.8))
```

输出结果：

```
3
5
7
```

`int | str | float` 表示「这个参数可以是 int、str、float 三者之一」，行话叫「联合类型」（Union Type）。

> Python 3.10+ 才支持 `X | Y` 这种写法。如果项目还在用 3.9 或更早版本，只能用 `from typing import Union; Union[X, Y]`。但说实话，2026 年了，能升就升吧。

总结一下：

- 老写法：`Optional[str]`、`Union[int, str]` —— 需要 `from typing import ...`
- 新写法：`str | None`、`int | str` —— 不用 import，直接写

新代码统一推荐新写法。

顺便提一个小细节。函数有了 `X | None` 的返回类型之后，**调用方就被「提醒」要处理 None 的情况**。比如：

```python
employees = {'两点水': '001', '三点水': '002'}


def find_id(name: str) -> str | None:
    return employees.get(name)


emp_id = find_id('四点水')
if emp_id is None:
    print('员工不存在')
else:
    print(f'工号：{emp_id}')
```

输出结果：

```
员工不存在
```

如果不写 `| None`，调用方很容易忘记判空，直接拿返回值去做字符串拼接、查询数据库，运行到一半才崩。注解+静态检查器的组合，能在你忘记判空的瞬间就提醒你。



## 容器类型怎么注解

光说一个 `list` 还不够。看下面这个函数：

```python
def total_salary(salaries: list) -> float:
    return sum(salaries)


print(total_salary([10000, 12000, 8000]))
```

输出结果：

```
30000
```

这里标了 `list`，但是「列表里到底装的是啥」没说清楚。是 int？是 float？是 str？读代码的人还是要猜。

老写法又来了，从 `typing` 导入 `List`、`Dict`、`Tuple` 这些大写开头的版本：

```python
from typing import List


def total_salary(salaries: List[float]) -> float:
    return sum(salaries)


print(total_salary([10000, 12000, 8000]))
```

`List[float]` 表示「装着 float 的列表」，方括号里写的是元素类型。

到了 Python 3.9（PEP 585），官方说：「这玩意儿大家天天用，还要 import 真的很烦，咱们直接让 `list` 自己支持下标行不行？」于是新写法就来了：

```python
def total_salary(salaries: list[float]) -> float:
    return sum(salaries)


print(total_salary([10000, 12000, 8000]))
```

输出结果：

```
30000
```

注意看，这里直接用小写的 `list[float]`，不用 import 任何东西。其他容器也一样：

```python
def group_by_dept(staff: dict[str, list[str]]) -> int:
    return len(staff)


data = {
    '做鸭事业部': ['两点水', '三点水'],
    '做鹅事业部': ['四点水'],
}
print(group_by_dept(data))
```

输出结果：

```
2
```

`dict[str, list[str]]` 表示「键是 str、值是 str 列表的字典」，这种嵌套写起来也很直观。

说到这里，多说一句关于「`list` 还是 `Sequence`」的选择。`list[int]` 写起来很自然，但其实有时候我们的函数并不真的需要一个 list，只要「能被遍历、能用下标访问」就行——这种情况下用 `Sequence` 更宽松：

```python
from collections.abc import Sequence


def first_and_last(items: Sequence[int]) -> tuple[int, int]:
    return items[0], items[-1]


print(first_and_last([1, 2, 3]))
print(first_and_last((10, 20, 30)))
```

输出结果：

```
(1, 3)
(10, 30)
```

`Sequence[int]` 接受 list、tuple、字符串……只要是「有顺序的容器」就行。同样的还有 `Iterable[X]`（只要能遍历就行，连生成器也接受）、`Mapping[K, V]`（能像字典一样取值就行）。这些抽象类型在写库的时候特别有用，能让函数接受更广泛的输入。日常写业务代码倒不用太纠结，直接 `list[int]` 也完全 OK。

`tuple` 稍微特殊一点。如果是固定长度的元组，每个位置类型都要写出来：

```python
def parse_point(p: tuple[int, int]) -> int:
    x, y = p
    return x + y


print(parse_point((3, 5)))
```

输出结果：

```
8
```

如果是不定长但元素同类型的元组（比较少见），用 `...`：

```python
def join_names(names: tuple[str, ...]) -> str:
    return '、'.join(names)


print(join_names(('两点水', '三点水', '四点水')))
```

输出结果：

```
两点水、三点水、四点水
```

`set` 跟 `list` 类似：

```python
def unique_count(tags: set[str]) -> int:
    return len(tags)


print(unique_count({'Python', 'Java', 'Python'}))
```

输出结果：

```
2
```

记住一句话：**3.9 以后，所有内置容器都能直接当类型用，不用从 `typing` 里 import 大写版了**。

再多看几个稍微复杂的容器嵌套例子。比如有这么一个数据结构，记录每个员工每天打卡的次数：

```python
punches: dict[str, dict[str, int]] = {
    '两点水': {'2026-04-26': 2, '2026-04-27': 1},
    '三点水': {'2026-04-26': 1, '2026-04-27': 2},
}


def total_punches(data: dict[str, dict[str, int]], name: str) -> int:
    return sum(data.get(name, {}).values())


print(total_punches(punches, '两点水'))
print(total_punches(punches, '三点水'))
print(total_punches(punches, '四点水'))
```

输出结果：

```
3
3
0
```

`dict[str, dict[str, int]]` 这种嵌套，刚开始读会有点累，但是只要拆开来看——「外层的键是 `str`（员工昵称），值是一个 `dict[str, int]`（日期到次数的映射）」，逻辑就很清楚了。后面我们会讲到，这种嵌套类型如果出现多次，可以用类型别名简化。

来个综合一点的例子，巩固一下。「做鸭事业部」要做一个员工统计函数，输入是一组员工记录，输出每个部门的人数：

```python
def count_by_dept(records: list[dict[str, str]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for r in records:
        dept = r['dept']
        result[dept] = result.get(dept, 0) + 1
    return result


data = [
    {'name': '两点水', 'dept': '做鸭事业部'},
    {'name': '三点水', 'dept': '做鸭事业部'},
    {'name': '四点水', 'dept': '做鹅事业部'},
]
print(count_by_dept(data))
```

输出结果：

```
{'做鸭事业部': 2, '做鹅事业部': 1}
```

整个函数的输入输出，光看签名 `list[dict[str, str]] -> dict[str, int]` 就一清二楚——「传一组『字段名到字段值』的字典进来，得到一个『部门到人数』的字典」。是不是很爽？

这里还藏了一个小细节，函数体里 `result: dict[str, int] = {}` 也加了注解，目的就是告诉 IDE「我后面 result 里要装的是 str → int」，否则 IDE 看到 `result = {}` 只能猜「这是个空字典，啥都能塞」，写错了也不会提示。



## 变量也能加注解

不光函数参数和返回值，普通的变量声明也能加注解。语法跟参数一样：

```python
name: str = '两点水'
age: int = 28
salary: float = 12000.5
tags: list[str] = ['Python', '后端']

print(name, age, salary, tags)
```

输出结果：

```
两点水 28 12000.5 ['Python', '后端']
```

那么有童鞋就要问了：「变量赋值的时候，类型不是一眼就能看出来吗？我直接 `name = '水哥'` 不就完了？还加注解干啥？」

主要有两种场景特别需要：

第一种，**初始值还推断不出最终类型**。比如初始化一个空列表，你想告诉别人「这是一个装字符串的列表」：

```python
employees: list[str] = []
employees.append('两点水')
employees.append('三点水')
print(employees)
```

输出结果：

```
['两点水', '三点水']
```

如果不写注解，IDE 看到 `employees = []` 只能猜「这是一个 list，元素类型未知」，后面你 append 啥它都不报错。加了 `list[str]` 之后，要是不小心 `employees.append(123)`，IDE 立马给你飘红。

来一个非常贴近实际的小场景。我们要写一个登录积分系统的初始化代码——「水哥」每天登录会累积一些积分，但是初始时还没积分：

```python
points: int = 0
visited_pages: list[str] = []
last_login: str | None = None


points += 5
visited_pages.append('首页')
last_login = '2026-04-28'

print(points, visited_pages, last_login)
```

输出结果：

```
5 ['首页'] 2026-04-28
```

注意看 `last_login: str | None = None` 这行——初始是 `None`，但是变量类型是 `str | None`。这种「先声明可以为空，运行时再赋具体值」的写法在长流程里特别常见。要是不写注解，IDE 看到 `last_login = None`，可能就把它的类型推断成 `None` 了，后面你赋值字符串它倒不报错，但语义上就不那么明确了。

类似的还有空字典、空集合：

```python
scores: dict[str, int] = {}
scores['两点水'] = 95
scores['三点水'] = 88
print(scores)


unique_tags: set[str] = set()
unique_tags.add('Python')
unique_tags.add('后端')
unique_tags.add('Python')
print(unique_tags)
```

输出结果：

```
{'两点水': 95, '三点水': 88}
{'Python', '后端'}
```

第二种，**只声明不赋值**。比如类的属性：

```python
class Employee:
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


emp = Employee('两点水', 28)
print(emp.name, emp.age)
```

输出结果：

```
两点水 28
```

类体里直接 `name: str` 就声明了一个类型为 `str` 的属性，连默认值都不用给。这种写法在 dataclass 里更常见，后面会讲。

也可以在类体里直接给默认值，效果跟变量声明差不多：

```python
class Counter:
    count: int = 0
    name: str = '默认计数器'

    def incr(self) -> None:
        self.count += 1


c = Counter()
c.incr()
c.incr()
print(c.name, c.count)
```

输出结果：

```
默认计数器 2
```

注意啊，这种「类体里给默认值」的写法，本质上是「类属性」（所有实例共享）。如果默认值是不可变的（int、str、tuple 这些），用起来跟「实例属性默认值」差别不大；可如果默认值是 list、dict 这种**可变对象**，就特别容易踩坑——所有实例会共享同一个列表。所以一般 list、dict 这种字段，咱们还是放到 `__init__` 里初始化，或者干脆用 dataclass 的 `field(default_factory=list)`，这点后面再细聊。



## Callable 和 Any——两个特殊角色

写了几个函数注解后，迟早会遇到一个问题：「我这个函数的参数是另一个函数，咋注解？」

学过装饰器的童鞋应该有印象，函数本身也是对象，是可以传来传去的。这种「可以被调用的东西」，类型叫 `Callable`，从 `collections.abc` 里来：

```python
from collections.abc import Callable


def apply(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)


print(apply(lambda a, b: a + b, 3, 5))
print(apply(lambda a, b: a * b, 3, 5))
```

输出结果：

```
8
15
```

`Callable[[int, int], int]` 怎么读？方括号里第一个列表是「参数类型列表」，第二个是「返回类型」。所以这个意思是：「一个接收两个 int、返回 int 的函数」。

> 在 Python 3.9 以前，`Callable` 也是从 `typing` 里 import 的。3.9+ 推荐从 `collections.abc` 导入。

学过装饰器的童鞋应该会想到，装饰器的本质就是「接收一个函数，返回一个函数」，那么装饰器的类型注解也能用 `Callable` 写出来：

```python
from collections.abc import Callable


def with_log(func: Callable[[int, int], int]) -> Callable[[int, int], int]:
    def wrapper(x: int, y: int) -> int:
        print(f'调用 {func.__name__}({x}, {y})')
        return func(x, y)
    return wrapper


@with_log
def add(x: int, y: int) -> int:
    return x + y


print(add(3, 5))
```

输出结果：

```
调用 add(3, 5)
8
```

这个 `with_log` 装饰器的签名是不是一目了然——「我吃一个『接收两个 int、返回 int』的函数，然后吐出来一个一模一样形状的函数」。当然，要写出能装饰任意函数的通用装饰器，光靠 `Callable` 还不够，得用 `ParamSpec`、`TypeVar` 这些更进阶的工具，那就属于另一个话题了，这里先不展开。

那么还有一个角色叫 `Any`，意思是「啥类型都行，别检查」。它在你**真的不在乎类型**的时候用：

```python
from typing import Any


def log(value: Any) -> None:
    print(f'记录：{value}')


log('两点水')
log(123)
log([1, 2, 3])
```

输出结果：

```
记录：两点水
记录：123
记录：[1, 2, 3]
```

`Any` 听起来很方便，但请慎用。一旦标了 `Any`，类型检查器就当没看见这个值，等于把注解的好处全扔了。能写具体类型，绝不用 `Any`。

那么各位可能会问：「啥时候用 `Any` 呢？」一般是这两种情况：

- 你在写一个真正通用的工具函数，确实不知道传进来是什么类型（比如 `print` 这种）
- 你在跟一个没注解的旧库交互，连作者都说不清类型，硬标会更乱

除此之外，**优先选具体类型，再次选联合类型，再次选 `object` / `Sequence` 这种宽松抽象类型，最后才考虑 `Any`**。这是写注解的优先级顺序，记一下。

举个例子，假设我们要写一个「把任意输入序列化成字符串」的函数，第一反应可能是：

```python
from typing import Any


def to_str(x: Any) -> str:
    return str(x)


print(to_str(123))
print(to_str([1, 2, 3]))
print(to_str({'name': '两点水'}))
```

输出结果：

```
123
[1, 2, 3]
{'name': '两点水'}
```

但是仔细想想，这个 `x` 真的是「啥都行」吗？不是。`str(x)` 内部其实只调用 `x.__str__()`，所以更准确的描述是「任何能 `str()` 的对象」。Python 中所有对象都有 `__str__`（继承自 `object`），所以这里其实标 `object` 比 `Any` 更准确：

```python
def to_str(x: object) -> str:
    return str(x)


print(to_str(123))
print(to_str([1, 2, 3]))
print(to_str({'name': '两点水'}))
```

输出结果：

```
123
[1, 2, 3]
{'name': '两点水'}
```

效果一样，但是注解的「自带文档」效果好得多。看到 `x: Any`，读者会想「难道还能传函数、类、生成器？」；看到 `x: object`，读者立刻就明白「随便给个对象都能用」。这种细节的考究，会让你的代码读起来很专业。

顺便提一个跟 `Any` 经常被搞混的类型——`object`。`object` 是所有类型的父类，注解写 `object` 意味着「随便传，但你拿到之后只能用所有对象都有的方法（比如 `str()`）」。它跟 `Any` 长得像，行为很不一样：

```python
def show(x: object) -> None:
    print(str(x))


show('两点水')
show(123)
show([1, 2, 3])
```

输出结果：

```
两点水
123
[1, 2, 3]
```

如果你给 `x` 标 `object`，然后函数体里写 `x.upper()`，类型检查器会报错——因为「`object` 没有 `upper` 方法」。换成 `Any` 就不会报。所以如果想「让函数能接受任意类型，但又强制使用前要先判断/转换」，标 `object` 比标 `Any` 更安全。



## 类型起得太长？给它起个别名

来看一个略复杂的场景。「做鸭事业部」要给所有员工建一个档案库，每个员工的档案是「姓名 + 标签列表」，整个库是「部门名 → 员工档案列表」的映射。注解写出来是这样：

```python
def add_employee(
    db: dict[str, list[tuple[str, list[str]]]],
    dept: str,
    profile: tuple[str, list[str]],
) -> None:
    db.setdefault(dept, []).append(profile)


db: dict[str, list[tuple[str, list[str]]]] = {}
add_employee(db, '做鸭事业部', ('两点水', ['Python', '后端']))
add_employee(db, '做鸭事业部', ('三点水', ['前端']))
print(db)
```

输出结果：

```
{'做鸭事业部': [('两点水', ['Python', '后端']), ('三点水', ['前端'])]}
```

是不是发现 `dict[str, list[tuple[str, list[str]]]]` 这一长串读起来真的很累？而且每次写到这个类型都得复制一遍，万一哪里少打个方括号，bug 就埋下了。

这时候就该「类型别名」上场了。从 Python 3.12 开始，有了一个全新的 `type` 关键字（PEP 695），可以这么写：

<!-- skip-ci -->
```python
type Profile = tuple[str, list[str]]
type EmployeeDB = dict[str, list[Profile]]


def add_employee(db: EmployeeDB, dept: str, profile: Profile) -> None:
    db.setdefault(dept, []).append(profile)


db: EmployeeDB = {}
add_employee(db, '做鸭事业部', ('两点水', ['Python', '后端']))
add_employee(db, '做鸭事业部', ('三点水', ['前端']))
print(db)
```

> Python 3.12+ 才支持 `type Alias = ...` 这种语法。

这样一来，`Profile` 和 `EmployeeDB` 这两个名字一眼就能看懂含义，而且只要类型定义集中在一个地方，要改也方便。

实际跑一下（在 3.12+ 上）：

```python
Profile = tuple[str, list[str]]
EmployeeDB = dict[str, list[Profile]]


def add_employee(db: EmployeeDB, dept: str, profile: Profile) -> None:
    db.setdefault(dept, []).append(profile)


db: EmployeeDB = {}
add_employee(db, '做鸭事业部', ('两点水', ['Python', '后端']))
add_employee(db, '做鸭事业部', ('三点水', ['前端']))
print(db)
```

输出结果：

```
{'做鸭事业部': [('两点水', ['Python', '后端']), ('三点水', ['前端'])]}
```

注意了，上面这段代码其实是「等号右边赋值的写法」——直接把类型当作普通变量赋值。这种写法在所有支持类型注解的版本都能跑，运行时表现就是定义一个普通变量。但严格来说，类型检查器并不一定把它视为「类型别名」。

如果项目跑在 3.10、3.11 上，又想要明确告诉检查器「这是别名」，可以用 `TypeAlias`：

```python
from typing import TypeAlias


Profile: TypeAlias = tuple[str, list[str]]
EmployeeDB: TypeAlias = dict[str, list[Profile]]


def add_employee(db: EmployeeDB, dept: str, profile: Profile) -> None:
    db.setdefault(dept, []).append(profile)


db: EmployeeDB = {}
add_employee(db, '做鸭事业部', ('两点水', ['Python']))
print(db)
```

输出结果：

```
{'做鸭事业部': [('两点水', ['Python'])]}
```

简单总结一下：

- Python 3.12+：直接 `type Alias = ...`，最干净
- Python 3.10/3.11：用 `Alias: TypeAlias = ...`
- 普通赋值 `Alias = ...`：能跑，但语义上不如前两种明确

类型别名还有一个特别实用的场景：**给业务概念起名字**。比如下面这段：

```python
UserId = int
ProductId = int


def get_user(uid: UserId) -> str:
    return f'用户 {uid}'


def get_product(pid: ProductId) -> str:
    return f'商品 {pid}'


print(get_user(1001))
print(get_product(2002))
```

输出结果：

```
用户 1001
商品 2002
```

`UserId` 和 `ProductId` 底下都是 `int`，但是名字不一样。代码读起来 `def get_user(uid: UserId)` 比 `def get_user(uid: int)` 信息量大得多——一眼就能看出「这个 int 不是随便一个数字，是用户 ID」。

来看一段反面教材，「做鸭事业部」原本的代码是这样的：

```python
def transfer(from_id: int, to_id: int, product_id: int, amount: int) -> bool:
    print(f'从用户 {from_id} 给用户 {to_id} 转 {amount} 个商品 {product_id}')
    return True


transfer(1001, 2002, 3003, 5)
```

输出结果：

```
从用户 1001 给用户 2002 转 5 个商品 3003
```

四个参数全是 `int`，调用的时候顺序写错一个，就完蛋了——可能商品 ID 当成用户 ID，金额当成商品 ID，连报错都不会有，因为类型对得上。改成有名字的别名后，调用时虽然语法上不强制，但是 IDE 提示会变成 `from_id: UserId, to_id: UserId, product_id: ProductId, amount: int`，写错的概率就低多了。

要进一步防止「把商品 ID 当用户 ID 传错」这种 bug，还可以用 `NewType`：

```python
from typing import NewType


UserId = NewType('UserId', int)
ProductId = NewType('ProductId', int)


def get_user(uid: UserId) -> str:
    return f'用户 {uid}'


print(get_user(UserId(1001)))
```

输出结果：

```
用户 1001
```

`NewType` 在运行时其实就是个透传函数，但在类型检查器眼里 `UserId` 和 `int` 是两种不同的类型——传普通 `int` 进去会被报错。这就把「业务概念」实实在在地变成了「类型」。这个特性在大型项目里特别有用，但小项目用 `type Alias` 就够了。



## 类的属性怎么注解

前面写了一个 `Employee`，类的属性注解我们顺便聊深一点。

最朴素的写法是这样：

```python
class Employee:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary


emp = Employee('两点水', 28, 12000.5)
print(emp.name)
```

输出结果：

```
两点水
```

读这个 `Employee` 类，单看 `__init__` 我们不知道每个属性是啥类型。改造一下：

```python
class Employee:
    def __init__(self, name: str, age: int, salary: float) -> None:
        self.name = name
        self.age = age
        self.salary = salary


emp = Employee('两点水', 28, 12000.5)
print(emp.name, emp.age, emp.salary)
```

输出结果：

```
两点水 28 12000.5
```

参数注解上去之后，IDE 一般就能把 `self.name` 推断为 `str` 了。如果想再明确一些，把属性也单独声明在类体里：

```python
class Employee:
    name: str
    age: int
    salary: float

    def __init__(self, name: str, age: int, salary: float) -> None:
        self.name = name
        self.age = age
        self.salary = salary


emp = Employee('两点水', 28, 12000.5)
print(emp.name, emp.age, emp.salary)
```

输出结果：

```
两点水 28 12000.5
```

类体顶部三行是「类级注解」，这是给类型检查器和工具看的。它跟 `__init__` 里的 `self.xxx = xxx` 配合，让整个类的「属性蓝图」一目了然。

那么「在类体里直接 `name: str`」和「`__init__` 里 `self.name = name`」是不是必须配对呢？严格说不是必须，但是配对最稳妥——光在类体里声明而不在 `__init__` 里赋值，访问时会报 `AttributeError`；光在 `__init__` 里赋值而不在类体里声明，类型检查器对类的「属性蓝图」就没那么清楚。

实例方法的注解也按同样规则来，`self` 不用注解，其他参数和返回值正常写：

```python
class Wallet:
    balance: float

    def __init__(self, initial: float = 0) -> None:
        self.balance = initial

    def deposit(self, amount: float) -> float:
        self.balance += amount
        return self.balance

    def can_afford(self, price: float) -> bool:
        return self.balance >= price


w = Wallet(100.0)
print(w.deposit(50.5))
print(w.can_afford(120))
print(w.can_afford(160))
```

输出结果：

```
150.5
True
False
```

签名读起来很顺畅吧？`deposit` 「接收 float、返回 float」，`can_afford` 「接收 float、返回 bool」，意图都一目了然。

那么各位想想，写过几个这种「一堆属性 + 一个 `__init__` 全是赋值」的类之后，是不是会觉得很烦？每个属性都要写两遍（类体里一次、`__init__` 里又一次）。

是的，这就是 `dataclass` 想要解决的问题。它能让你只写类体那段类型声明，`__init__` 自动帮你生成。这部分留到 `python20` 专门讲，这里先卖个关子。



## Protocol——类型注解版的 duck typing

学 Python 久了的童鞋肯定听过一句话：「If it walks like a duck and quacks like a duck, it's a duck.」——鸭子类型。Python 的核心精神之一，就是「我不管你是不是 Duck 类的实例，只要你会 `quack()`，我就当你是鸭」。

可是问题来了：在类型注解里怎么表达这个意思？总不能写 `def feed(d: Duck)` 然后强制大家都继承 `Duck` 吧，那就违背鸭子类型的初衷了。

Python 3.8 引入了 `Protocol`（PEP 544），专门解决这个事。它的意思是：**只要这个对象有我要的方法、属性，就算我没继承它，也算它符合这个协议**。

来看个例子。「做鸭事业部」养了好多种动物，我们想写一个通用的「让它们叫一声」的函数：

```python
from typing import Protocol


class Quacker(Protocol):
    def quack(self) -> str:
        ...


class Duck:
    def quack(self) -> str:
        return '嘎嘎嘎'


class Dog:
    def quack(self) -> str:
        return '汪汪汪（其实我不是鸭）'


def let_it_quack(animal: Quacker) -> None:
    print(animal.quack())


let_it_quack(Duck())
let_it_quack(Dog())
```

输出结果：

```
嘎嘎嘎
汪汪汪（其实我不是鸭）
```

各位看，`Duck` 和 `Dog` 都没有继承 `Quacker`，但是它们都有 `quack` 方法，所以传给 `let_it_quack` 都没问题——这就是「结构化子类型」。如果传一个没有 `quack` 方法的对象进去，类型检查器会立刻报错。

`Protocol` 的好处是：你不用提前规划好继承关系，只要「形状」对得上就行。这是写库、写框架时非常好用的工具。

再看一个更贴近实际的场景。假如我们要写一个「打印任意东西的尺寸」的工具函数，按 duck typing 的思路，「只要这东西能 `len()`，我就当它有尺寸」：

```python
from typing import Protocol


class Sized(Protocol):
    def __len__(self) -> int:
        ...


def show_size(obj: Sized) -> None:
    print(f'尺寸是 {len(obj)}')


show_size('两点水')
show_size([1, 2, 3, 4])
show_size({'a': 1, 'b': 2})
```

输出结果：

```
尺寸是 3
尺寸是 4
尺寸是 2
```

`str`、`list`、`dict` 都没继承我们定义的 `Sized`，但是它们都实现了 `__len__`，所以全都符合协议。这种「不靠继承、靠形状」的多态，写起来又灵活又类型安全。

`Protocol` 不止能描述「方法」，也能描述「属性」。比如「我需要一个有 `name` 属性的对象」：

```python
from typing import Protocol


class HasName(Protocol):
    name: str


class Employee:
    def __init__(self, name: str, dept: str) -> None:
        self.name = name
        self.dept = dept


class Pet:
    def __init__(self, name: str, kind: str) -> None:
        self.name = name
        self.kind = kind


def shout_name(obj: HasName) -> None:
    print(f'你好，{obj.name}！')


shout_name(Employee('两点水', '做鸭事业部'))
shout_name(Pet('小黄', '鸭子'))
```

输出结果：

```
你好，两点水！
你好，小黄！
```

`Employee` 和 `Pet` 八竿子打不着，但是它们都有 `name` 属性，所以都能传给 `shout_name`。

这种写法在写库、写中间层的时候特别好用——你不用强迫调用方继承你定义的基类，他们的现有类型只要「形状对得上」就能直接接进来，可拓展性极强。

这里只是浅尝辄止，`Protocol` 还有 `runtime_checkable`、属性协议等等更深的用法，留给善于思考的各位自己探索。



## 写完注解，怎么真的检查类型

聊到这里，各位应该会问一个问题：「我注解都写了，可是 Python 解释器又不强制，那要怎么真的发现类型错误啊？」

答案是：用静态类型检查器。常见的两个：

- `mypy`：老牌，社区生态最成熟
- `pyright`：微软出的，速度快，VSCode 里 Pylance 的核心就是它

随便挑一个就行。安装：

```
pip install mypy
```

假设我们写了这么一个文件 `bad.py`：

```
def add(x: int, y: int) -> int:
    return x + y


print(add('两点水', 3))
```

跑 `python bad.py`，能跑出来（虽然结果是 `水哥水哥水哥`），但是跑 `mypy bad.py`：

```
bad.py:5: error: Argument 1 to "add" has incompatible type "str"; expected "int"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

再换一种典型错误，比如忘记处理 `None`：

```
def find_id(name: str) -> str | None:
    db = {'两点水': '001'}
    return db.get(name)


emp_id = find_id('四点水')
print(emp_id.upper())
```

直接跑 `python` 会报 `AttributeError: 'NoneType' object has no attribute 'upper'`，等于线上挂了；而 `mypy` 在写完代码就提醒：

```
bad.py:7: error: Item "None" of "str | None" has no attribute "upper"  [union-attr]
```

各位看，这种「忘了判 None」的错，mypy 简直是降维打击——你脑子里没想到的边界情况，它机器扫一遍就给你揪出来。

看，运行时混过去的错误，mypy 在「写完代码、还没运行」时就给抓出来了。这就是类型注解最大的意义所在。

实际项目里，一般会把 mypy 或者 pyright 配进 CI，跟单元测试一起跑，就能在合并代码前拦住一大批低级错误。

那么各位可能又会问：「IDE（PyCharm、VSCode）已经能根据注解给我飘红了，我还需要单独跑 mypy 吗？」

答案是：**最好还是跑**。原因有几个：

- IDE 飘红只在你打开那个文件时才看得到。整个项目里没人打开过的旧文件，类型错误可能藏好几年
- 不同人电脑上的 IDE 配置可能不一样，有人飘红、有人不飘
- CI 里跑 mypy 是「客观的、强制的」，没过就拦下来，没法装作没看见

所以推荐的做法是：**写代码时靠 IDE 即时反馈，提交代码前由 mypy/pyright 把关**。两条防线一起上，类型错误才能真的被治住。

最后再交代一个常见疑问：「老项目里一堆没注解的代码，跑 mypy 会不会满屏报错？」会，所以对老项目，一般是「逐步引入」——

- 先在 `mypy.ini` 或者 `pyproject.toml` 里把检查级别调宽松（`--ignore-missing-imports`、不强制返回类型注解等等）
- 新写的代码全部带注解，老代码遇到改动时顺手补
- 几个迭代下来，覆盖率慢慢爬上来，再逐步收紧规则

千万别一上来就开 `--strict`，那基本等于「我要重写整个项目」，谁都顶不住。一步步来才是稳的。



## 一些常见疑问

写到最后再统一回答几个童鞋反复问的问题：

**Q1：注解会不会让 Python 变慢？**

几乎不会。注解在解释器层面只是「读取一下、存到 `__annotations__` 里」，运行时不做任何检查。除非函数被调用得极其频繁、且参数注解极其复杂，否则你测都测不出来差别。安心写就好。

**Q2：注解和 docstring 冲突吗？**

不冲突，是互补关系。注解负责「类型」，docstring 负责「业务含义、行为约束、示例」。两者一起上才是完整的：

```python
def punch(name: str, dept: str = '做鸭事业部') -> None:
    """记录员工上班打卡。

    Args:
        name: 员工昵称，比如 '两点水'
        dept: 部门名称，默认是 '做鸭事业部'

    打卡只记录到内存，不写数据库。
    """
    print(f'{name}（{dept}）打卡成功')


punch('两点水')
```

输出结果：

```
两点水（做鸭事业部）打卡成功
```

**Q3：每一行都要写注解吗？**

不必。优先级从高到低是：

1. **公共函数/类**（要给别人调用的）：尽量都加，这是接口契约
2. **复杂的业务函数**（参数多、嵌套层级深的）：加，方便后期维护
3. **简单的一次性脚本**：随意，不加也无所谓

像 `for i in range(10): print(i)` 这种 `i` 显然是 `int` 的循环变量，没必要硬塞个 `i: int`。注解的价值是「消除歧义」，没歧义的地方加了反而显得啰嗦。

**Q4：第三方库没注解怎么办？**

很多老库可能没写注解，那就只能：

- 看库的 `py.typed` 标记是否存在（存在表示作者承诺了类型支持）
- 没有的话，用 `typeshed` 社区维护的存根包（package 名一般是 `types-xxx`）
- 实在没有，就在调用处用变量注解「补救」一下：`result: list[str] = some_legacy_lib.get_data()`

主流的现代库（FastAPI、httpx、Pydantic、SQLAlchemy 2.x 等等）都已经全面拥抱类型注解，新选库时多看一眼这点准没错。



## 小结

类型注解这玩意儿，乍一看是给 Python 加负担，写惯了之后会发现真香。最后再总结三点：

- **注解只是给人和工具看的**，Python 解释器不强制；想真的检查类型，跑 mypy 或 pyright
- **拥抱新写法**：`X | None` 代替 `Optional[X]`，`list[int]` 代替 `List[int]`，少一份 import 多一份清爽
- **从签名开始写起**：函数参数和返回值是性价比最高的注解位置；变量注解、类属性注解按需补；遇到长得离谱的类型，就用类型别名命名

慢慢把注解习惯养起来，你写出来的代码会一天比一天专业。

最后留一个小思考给善于思考的各位：本文里我们见到了 `int | None`、`list[int]`、`Callable[[int, int], int]`、`Protocol`、类型别名…… 那么如果想写一个「接收任意类型 T，返回同样类型 T 的列表」的函数（比如「把任意元素包成单元素列表」），该怎么写呢？

提示一下：这就要用到「泛型」（Generics）了，关键字是 `TypeVar` 或者 Python 3.12+ 的新泛型语法（`def wrap[T](x: T) -> list[T]: ...`）。这部分内容比较进阶，不过等你写过几个工具函数、几个小框架之后，你自然就会想去查它了。慢工出细活，咱们慢慢来。

再多举几个学完本章后可以继续深挖的方向：

- `Literal['get', 'post']`：限定字符串只能是有限几个值，写 API 客户端时特别好用
- `TypedDict`：给字典里每个键都标具体类型，比 `dict[str, Any]` 强多了
- `Final`：声明「这个变量赋值后不准改」
- `@override`（Python 3.12+）：明确标记「我是在覆盖父类方法」
- `Self` 类型（Python 3.11+）：在类里写「返回我自己」更优雅
- 泛型类、泛型函数、`ParamSpec`：写工具库的标配

这些都是类型注解大家族里的成员，不用一次学完，遇到再学是最高效的。

类型注解这件事，最重要的不是「学全」，而是「用起来」。从今天开始，每写一个新函数都顺手把签名补上，一个月之后再回头看，你会发现自己写代码的「肌肉记忆」已经完全变了——这就够了。



## 注解写上了，输入就一定正确吗

前面已经说明类型注解的用途。现在自己验证一下它和运行时检查的区别：

```python
def add_minutes(first: int, second: int) -> int:
    return first + second


print(add_minutes(5, 10))
print(add_minutes('5', '10'))
```

输出：

```text
15
510
```

第二次传的是字符串，解释器仍然执行字符串拼接。注解能帮助人和静态检查工具理解意图，但不会自动替我们把文本转换成整数，或替我们拒绝不符合业务要求的输入。

自己为这个函数补一行文档字符串，说明分钟数的单位，再决定负数是否允许。类型是整数，只回答了一部分问题；是不是非负数、有没有上限、空记录怎么处理，还需要把约定写清楚并验证。

阅读时可以先看命名和函数接口，再按需要查阅高级注解，不必为了一个小函数先掌握所有类型工具。
