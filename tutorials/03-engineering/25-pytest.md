# pytest：30 秒跑完 100 个用例的测试框架

各位写代码的时候，是不是经常被这种问题烦到——

「这个函数我刚才改了一行，会不会把别的地方搞挂？」

「老板让加个新功能，可这一坨代码我都不敢动，万一改坏了线上炸了怎么办？」

「同事给我提了个 PR，看起来没毛病，可我心里没底。」

这种「不敢动代码」的恐惧，老司机都懂。水哥当年第一次维护一个三千行的老项目，每改一行都心惊胆战，因为没有测试，谁也不知道改完会不会出事。最后只能小心翼翼地手动点几个页面、构造几个请求看看，跑十分钟才敢提交。效率低得感人。

「我代码改一改没事吧？」这个问题的答案永远是——**跑一下测试才知道**。

那写测试要多麻烦呢？很多童鞋一听「写测试」就头疼，觉得是给自己加活儿。其实在 Python 圈，有一个工具能让各位 30 秒跑完 100 个测试用例，写一个测试只要三行代码——它就是 `pytest`。

`pytest` 是 Python 圈测试的事实标准。`Django`、`FastAPI`、`Pandas`、`NumPy`、`SQLAlchemy`、`Pydantic`、`Requests`、`httpx`、几乎你能叫出名字的 Python 项目都用它来跑测试。GitHub 上 12k+ 的 stars，PyPI 上每月几亿次下载量。

这一章咱们把 `pytest` 从零讲到能上手。学完之后，各位应该能：

1. 写出第一个 `pytest` 测试，跑起来看到绿色的 PASS
2. 看懂别人项目里 `tests/` 目录在干啥
3. 用 `fixture`、参数化、`tmp_path`、`monkeypatch` 这些核心工具把测试写得又简洁又强壮
4. 给自己的项目接上覆盖率，知道哪行代码还没被测到
5. 把测试接进 `CI`，提交 PR 自动跑

走起。



## 第一个测试

各位先来感受一下 `pytest` 有多简单。建一个新目录：

```bash
mkdir test-demo
cd test-demo
uv init
uv add --dev pytest
```

写一个最普通的 Python 文件 `mymath.py`：

```python
def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b
```

然后写一个测试文件 `test_mymath.py`：

<!-- skip-ci -->
```python
from mymath import add, divide


def test_add():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_divide():
    assert divide(10, 2) == 5
```

注意三个细节——文件名以 `test_` 开头、函数名以 `test_` 开头、断言用 Python 内置的 `assert` 关键字。就这么简单。

跑一下：

```bash
uv run pytest
```

输出大概长这样：

```
============================= test session starts ==============================
platform darwin -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/walter/test-demo
collected 3 items

test_mymath.py ...                                                       [100%]

============================== 3 passed in 0.01s ===============================
```

三个绿点 `...` 代表三个测试全部通过。0.01 秒跑完。

是不是比预想中简单？

各位再故意把 `add` 函数改坏，比如改成 `return a + b + 1`，再跑一次：

```
test_mymath.py FF.                                                       [100%]

=================================== FAILURES ===================================
___________________________________ test_add ___________________________________

    def test_add():
>       assert add(2, 3) == 5
E       assert 6 == 5
E        +  where 6 = add(2, 3)

test_mymath.py:4: AssertionError
```

`pytest` 直接告诉你：第几行的断言炸了、左边是 `6`、右边是 `5`、`6` 是怎么来的（`add(2, 3)` 算出来的）。一目了然。这就是 `pytest` 的「assert 重写」黑科技——后面会专门讲。



## pytest vs unittest——为什么选 pytest

各位可能会问：「Python 不是自带 `unittest` 标准库吗？为什么还要装 `pytest`？」

好问题。咱们对比一下同一个测试，两种写法的区别。

`unittest` 写法：

<!-- skip-ci -->
```python
import unittest


class TestMyMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)


if __name__ == "__main__":
    unittest.main()
```

`pytest` 写法：

<!-- skip-ci -->
```python
def test_add():
    assert add(2, 3) == 5


def test_divide():
    assert divide(10, 2) == 5
```

差别在哪？

1. **不需要继承 `TestCase`**。`pytest` 用普通函数就行，少写一层类
2. **不需要记一堆断言方法名**。`unittest` 有 `assertEqual`、`assertNotEqual`、`assertTrue`、`assertFalse`、`assertIn`、`assertIsInstance`、`assertGreater`、`assertRaises`…… 几十个方法都得记。`pytest` 只用一个 `assert` 就完事
3. **不需要写 `__main__`**。直接 `pytest` 命令一跑就完了

`unittest` 风格其实是从 Java 的 `JUnit` 抄过来的，「类 + 方法」这一套是 OOP 思维。Python 这种动态语言用普通函数就能搞定的事，没必要搞这么重。所以 2010 年后，Python 圈逐步全面倒向 `pytest`。

那 `unittest` 还能用吗？能。`pytest` 是**向后兼容** `unittest` 的，你写的 `unittest` 测试用例，`pytest` 直接也能跑。所以老项目从 `unittest` 迁过来很丝滑——一行代码不改，把跑测试的命令从 `python -m unittest` 换成 `pytest` 就行。新项目则建议直接全用 `pytest` 风格。

各位记一句话：**Python 圈如果现在还有人推荐用 `unittest` 写新项目，要么是十年前的资料，要么是没跟上时代**。直接 `pytest`。



## assert 重写——pytest 最神奇的地方

刚才咱们看到，`pytest` 的失败信息特别详细：

```
>       assert add(2, 3) == 5
E       assert 6 == 5
E        +  where 6 = add(2, 3)
```

按理说 `assert` 这个东西很「弱」——它失败的时候只能抛 `AssertionError`，啥提示都没有。Python 内置的 `assert` 出错时是这样的：

<!-- skip-ci -->
```python
>>> x = 6
>>> assert x == 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

只告诉你「断言失败了」，至于左边右边各是啥，不知道。

那 `pytest` 怎么搞出来这么多信息的？

答案是「assert 重写」（assertion rewriting）。`pytest` 在加载测试文件之前，会先把代码里的 `assert` 语句**重写**一遍——把简单的 `assert a == b` 改写成「先把 `a` 和 `b` 算出来存好，断言失败时再把它们打印出来」。这套机制不需要各位写任何额外代码，开箱即用。

复杂一点的断言也照样有详细信息：

```python
def test_list_equal():
    a = [1, 2, 3, 4, 5]
    b = [1, 2, 3, 4, 6]
    assert a == b
```

跑一下，`pytest` 会输出：

```
>       assert a == b
E       assert [1, 2, 3, 4, 5] == [1, 2, 3, 4, 6]
E         At index 4 diff: 5 != 6
```

它甚至会告诉你「在第 4 个位置，5 跟 6 不一样」。字典、字符串、集合都有类似的「智能 diff」。

各位有没有觉得「这个比 `unittest.TestCase.assertEqual` 都要友好」？没错——很多年前 `unittest` 系列工具喜欢用 `assertEqual` 之类的方法，就是因为「裸 `assert` 信息太少」。`pytest` 用元编程把这个问题彻底解决了。

所以 `pytest` 圈推荐的写法只有一句话——**所有断言都用 `assert`，一律不用 `assertXXX`**。

咱们看看几种常见的断言：

<!-- skip-ci -->
```python
# 相等
assert x == 5
assert name == "两点水"

# 不等
assert x != 0

# 包含
assert "Python" in "I love Python"
assert 3 in [1, 2, 3]

# 真假
assert is_valid is True
assert result is None

# 数值大小
assert age >= 18
assert 0 < score < 100

# 类型
assert isinstance(x, int)
```

要点就是「写普通 Python 表达式」。能用 `==` 就用 `==`，能用 `in` 就用 `in`，不用记任何专属断言函数。这就是各位写 `pytest` 测试时最舒服的地方。



## 测试发现——pytest 怎么找到你的测试

各位刚才有没有注意到一件事？我们写 `pytest` 命令时**没指定要跑哪个文件**，但它自动找到了 `test_mymath.py`。这是怎么做到的？

`pytest` 有一套默认的「测试发现」（test discovery）规则。它会从当前目录开始，递归扫描所有目录，找符合下面这些规则的东西：

1. **测试文件**：`test_*.py` 或 `*_test.py`
2. **测试类**：以 `Test` 开头的类（且没有 `__init__` 方法）
3. **测试函数**：以 `test_` 开头的函数或方法

举几个例子：

```
my-project/
├── src/
│   └── mymath.py
└── tests/
    ├── test_mymath.py        # 自动发现 ✓
    ├── test_helper.py        # 自动发现 ✓
    ├── helper_test.py        # 自动发现 ✓
    └── notes.py              # 不识别 ✗
```

测试文件里：

```python
def test_add():           # 自动发现 ✓
    pass


def helper():             # 不识别 ✗
    pass


class TestUser:           # 自动发现 ✓
    def test_create(self):    # 自动发现 ✓
        pass

    def helper(self):     # 不识别 ✗
        pass


class UserTest:           # 不识别 ✗（不是 Test 开头）
    pass
```

各位写测试的时候，约定俗成的目录结构是这样：

```
my-project/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
└── tests/
    ├── test_core.py
    └── test_utils.py
```

源码放在 `src/` 下，测试放在 `tests/` 下，**测试文件名跟被测文件一一对应**。`core.py` 对应 `test_core.py`，`utils.py` 对应 `test_utils.py`。这样新人接手项目，看到 `core.py` 想知道它的测试在哪，一眼就能找到。

那 `pytest` 命令怎么用？常用几种姿势：

```bash
# 跑所有测试
pytest

# 只跑某个文件
pytest tests/test_core.py

# 只跑某个测试函数
pytest tests/test_core.py::test_add

# 只跑某个类的某个方法
pytest tests/test_core.py::TestUser::test_create

# 按关键字过滤（函数名包含某个词）
pytest -k "add"
pytest -k "add or divide"
pytest -k "not slow"

# 显示更详细的输出
pytest -v

# 第一个失败就停
pytest -x

# 显示 print 输出（默认 pytest 会捕获）
pytest -s
```

`-v` 会把每个测试的名字列出来，绿勾代表通过：

```
test_mymath.py::test_add PASSED
test_mymath.py::test_add_negative PASSED
test_mymath.py::test_divide PASSED
```

`-x` 在 debug 时特别有用——一堆测试全挂了，与其全跑完再看，不如第一个挂就停下来分析。

`-s` 让 `print` 直接输出到终端，方便临时打日志看变量值。



## fixture——测试界的依赖注入

各位写测试写多了，会发现一个问题：**很多测试都需要一些「准备工作」**。

比如：

- 测试数据库相关功能时，每个测试都要先建一个临时数据库连接
- 测试 API 时，每个测试都要先启动一个 HTTP 客户端
- 测试文件操作时，每个测试都要先准备一个临时目录

如果按「最朴素」的写法：

```python
def test_user_create():
    db = create_test_db()
    db.connect()
    try:
        user = User(name="walter")
        db.save(user)
        assert db.get_user("walter").name == "walter"
    finally:
        db.close()


def test_user_delete():
    db = create_test_db()
    db.connect()
    try:
        user = User(name="walter")
        db.save(user)
        db.delete_user("walter")
        assert db.get_user("walter") is None
    finally:
        db.close()
```

每个测试都要重复「建库 → 连接 → finally 关闭」这一坨。很丑。

`pytest` 的解决办法叫 `fixture`。它把「准备工作」抽成一个带 `@pytest.fixture` 装饰器的函数：

<!-- skip-ci -->
```python
import pytest


@pytest.fixture
def db():
    """提供一个干净的测试数据库连接。"""
    conn = create_test_db()
    conn.connect()
    yield conn         # 把 conn 交给测试函数
    conn.close()       # 测试结束后再清理


def test_user_create(db):
    user = User(name="walter")
    db.save(user)
    assert db.get_user("walter").name == "walter"


def test_user_delete(db):
    user = User(name="walter")
    db.save(user)
    db.delete_user("walter")
    assert db.get_user("walter") is None
```

各位看出门道了吗？

1. 写一个 `db` fixture，里面 `yield` 出去一个连接对象
2. 测试函数把 `db` **写成参数**，`pytest` 自动把 fixture 算出来的值传进来
3. 测试结束后，`yield` 后面的清理代码自动跑

是不是有点像 Spring/Django 里的「依赖注入」？各位要啥东西，写个参数名 `pytest` 就帮你准备好。**测试函数只关心「我要测什么」，不关心「怎么准备数据」**——关注点完全分离。

那 fixture 还能怎么写？最常见的几种写法：

**只准备、不清理**：直接 `return`，省掉 `yield`。

<!-- skip-ci -->
```python
@pytest.fixture
def sample_user():
    return User(name="walter", age=28)


def test_greet(sample_user):
    assert greet(sample_user) == "Hello, walter!"
```

**fixture 之间可以互相依赖**。比如 `db` 依赖 `config`：

<!-- skip-ci -->
```python
@pytest.fixture
def config():
    return {"host": "localhost", "port": 5432}


@pytest.fixture
def db(config):                         # 注意这里也写参数
    conn = connect(config["host"], config["port"])
    yield conn
    conn.close()


def test_query(db):
    assert db.ping() is True
```

`pytest` 会自己把整个依赖链解算出来，先跑 `config`，再用 `config` 的结果调 `db`，最后把 `db` 喂给测试。



## fixture scope——什么时候建、什么时候销毁

各位再看一个实际问题——

「我有一个 fixture 是建数据库连接，建一次要 1 秒。我有 100 个测试都用它。每个测试都重新建一次的话，光建连接就要 100 秒。能不能只建一次，所有测试共用？」

`pytest` 的答案是 fixture 的 `scope` 参数。它有四档：

- `function`（默认）：每个测试函数跑前建、跑后销毁
- `class`：每个测试类跑前建、跑完销毁
- `module`：每个测试文件（模块）跑前建、跑完销毁
- `session`：整个 `pytest` 启动到结束只建一次

举个例子，把数据库连接设成 `session` 级别：

<!-- skip-ci -->
```python
@pytest.fixture(scope="session")
def db():
    conn = create_test_db()
    conn.connect()
    yield conn
    conn.close()
```

这样不管你跑多少测试，`conn` 只建一次、关一次。

那啥时候用啥 scope？给各位一个经验法则——

- **要保证测试之间彼此独立**（每个测试都从干净状态开始）：用 `function`
- **建一次代价很高**（连数据库、启容器、加载大模型）：用 `module` 或 `session`，但要注意每个测试结束后**手动清理状态**

举个混合用法：

<!-- skip-ci -->
```python
@pytest.fixture(scope="session")
def db_connection():
    """整个 session 共用一个连接，建一次就够。"""
    conn = connect_to_db()
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def db(db_connection):
    """每个测试用一个干净的事务，跑完回滚。"""
    txn = db_connection.begin_transaction()
    yield txn
    txn.rollback()


def test_create_user(db):
    db.execute("INSERT INTO users ...")
    # 测试结束后事务自动回滚，下一个测试看到的还是干净的库
```

「连接共享、事务隔离」是数据库测试里特别常见的模式。`session` 级别的连接保证速度，`function` 级别的事务保证隔离。



## 内置 fixture——pytest 自带的几个救命神器

各位先别急着自己写 fixture，`pytest` 自己已经备好了几十个常用的。说几个最最常用的。

### tmp_path——临时目录

写测试经常要操作文件——读啥、写啥、删啥。直接在硬盘上随便建文件吧，跑完测试满地是垃圾；用 `tempfile` 自己管理吧，又得写一堆 `setup/teardown`。

`pytest` 的 `tmp_path` fixture 直接给你一个临时目录，跑完测试自动清理。

```python
def test_write_and_read(tmp_path):
    file = tmp_path / "hello.txt"
    file.write_text("两点水", encoding="utf-8")

    assert file.exists()
    assert file.read_text(encoding="utf-8") == "两点水"
```

`tmp_path` 是一个 `pathlib.Path` 对象，直接 `/` 拼路径。各位回想一下 python18 讲过的 `pathlib`，这里完美闭环。

每个测试拿到的 `tmp_path` 都是不同的目录，互不干扰。`pytest` 默认会保留最近 3 次跑测试的临时目录在 `/tmp/pytest-of-<user>/` 下，如果一个测试挂了，各位可以去那里翻翻看里面的文件长啥样，方便 debug。

### monkeypatch——临时改环境

测试时经常要「修改一些全局状态」——改环境变量、替换某个函数、改某个对象的属性。改完测试结束之后还得改回去，不然影响下一个测试。

`monkeypatch` fixture 就是干这个的。它能临时改东西，测试结束自动还原。

```python
def test_with_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    assert get_api_key() == "test-key-123"
    # 测试结束后 API_KEY 自动还原


def test_replace_function(monkeypatch):
    def fake_get_time():
        return 1700000000
    monkeypatch.setattr("mymodule.time.time", fake_get_time)
    # 测试结束后 time.time 自动还原


def test_chdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    # 当前目录临时切到 tmp_path，测试结束自动切回去
```

常用方法：

- `monkeypatch.setenv(name, value)`：设环境变量
- `monkeypatch.delenv(name)`：删环境变量
- `monkeypatch.setattr(target, value)`：替换某个对象的属性
- `monkeypatch.delattr(target)`：删某个属性
- `monkeypatch.chdir(path)`：切当前目录

各位测试有外部依赖的代码时，`monkeypatch` 是首选——不用真去连数据库、不用真发 HTTP 请求，直接 fake 掉一个返回值就行。

### capsys——抓 stdout/stderr

测试一段会 `print` 的代码，怎么验证它打印对了？`capsys` 就是干这个的。

```python
def greet(name):
    print(f"Hello, {name}!")


def test_greet(capsys):
    greet("walter")
    captured = capsys.readouterr()
    assert captured.out == "Hello, walter!\n"
    assert captured.err == ""
```

`capsys.readouterr()` 返回一个对象，`.out` 是 stdout、`.err` 是 stderr。读完之后 buffer 会被清空，再次调用就是新的输出。

类似的 fixture 还有：

- `capfd`：抓文件描述符级别的输出（包括 C 扩展、子进程的输出）
- `caplog`：抓 `logging` 模块的输出

`capsys` 测「函数有没有正确 print」最方便。



## 参数化——同一个测试跑多组数据

各位写测试时是不是经常这样：

```python
def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -2) == -3


def test_add_zero():
    assert add(0, 0) == 0


def test_add_mixed():
    assert add(-5, 10) == 5
```

测一个加法，写四个函数，函数体几乎一模一样，只是数据不同。重复啊重复。

`pytest` 的参数化（`@pytest.mark.parametrize`）能把它压成一个：

<!-- skip-ci -->
```python
import pytest


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, -2, -3),
    (0, 0, 0),
    (-5, 10, 5),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

跑出来 `pytest` 会把它当成 4 个独立测试：

```
test_mymath.py::test_add[2-3-5] PASSED
test_mymath.py::test_add[-1--2--3] PASSED
test_mymath.py::test_add[0-0-0] PASSED
test_mymath.py::test_add[-5-10-5] PASSED
```

挂了哪一组、过了哪一组，一目了然。

参数化的语法两个要点：

1. 第一个参数是字符串，写**测试函数要接收的参数名**，多个用逗号分隔
2. 第二个参数是列表，每一项是一组测试数据（参数顺序跟第一个字符串对应）

每组数据还能起个名字，方便看输出：

<!-- skip-ci -->
```python
@pytest.mark.parametrize("a, b, expected", [
    pytest.param(2, 3, 5, id="正数相加"),
    pytest.param(-1, -2, -3, id="负数相加"),
    pytest.param(0, 0, 0, id="零相加"),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

跑起来：

```
test_mymath.py::test_add[正数相加] PASSED
test_mymath.py::test_add[负数相加] PASSED
test_mymath.py::test_add[零相加] PASSED
```

各位用中文给 case 起名也完全没问题，看起来更直观。

参数化还能堆——多个 `@pytest.mark.parametrize` 叠加，会自动算笛卡尔积：

<!-- skip-ci -->
```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_combo(x, y):
    print(x, y)
```

跑出来一共 `3 × 2 = 6` 个用例：`(1,10) (1,20) (2,10) (2,20) (3,10) (3,20)`。

参数化是 `pytest` 最杀手锏的功能之一，**能用参数化就尽量用，别复制粘贴写一堆相似的测试**。



## 异常断言——测「会不会抛错」

写代码时，咱们经常希望某个函数在错误输入下「**应该**」抛异常。比如除以 0、空字符串、负数年龄。

那怎么测「这个函数应该抛 `ValueError`」呢？光写 `try/except` 不行——测试函数没出错也算通过，可逻辑上没抛异常恰恰是 bug。

`pytest` 提供了 `pytest.raises` 上下文管理器：

<!-- skip-ci -->
```python
import pytest


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

`with pytest.raises(ValueError):` 块里面的代码**必须抛 `ValueError`**，不抛或抛别的异常都算测试失败。

如果各位还想顺便检查异常的内容（比如错误信息）：

```python
def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="除数不能为 0"):
        divide(10, 0)
```

`match` 参数是一个正则表达式，匹配异常的字符串表示。

或者拿到异常对象本身做更精细的断言：

```python
def test_divide_by_zero_detail():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "除数" in str(exc_info.value)
    assert exc_info.type is ValueError
```

`exc_info.value` 就是抛出来的那个异常对象，可以像普通对象一样访问它的属性。

各位写测试时，「正常路径」+「异常路径」都要覆盖。一个函数只测正常输入是不够的——边界条件、错误输入、空值这些「能否优雅地抛异常」也很重要。



## 跳过和标记——挑着跑测试

写测试时，各位经常会遇到这种场景：

- 这个测试只在 Linux 上能跑，Windows 上没法跑
- 这个测试只对 Python 3.11+ 有效
- 这个测试很慢（要十几秒），平时不想跑，CI 才跑
- 这个测试还在写，先标个「待办」

`pytest` 的解法是「mark」（标记）系统。

### skip——直接跳过

<!-- skip-ci -->
```python
import pytest


@pytest.mark.skip(reason="这个还没实现完")
def test_new_feature():
    assert do_something() == "expected"
```

跑起来 `pytest` 会显示一个 `s`：

```
test_demo.py s                                                           [100%]
================== 1 skipped in 0.01s ==================
```

测试不会执行，也不会算失败。

### skipif——条件跳过

<!-- skip-ci -->
```python
import sys


@pytest.mark.skipif(sys.platform == "win32", reason="Windows 上不支持")
def test_unix_specific():
    assert "/usr/bin" in PATH


@pytest.mark.skipif(sys.version_info < (3, 11), reason="需要 Python 3.11+")
def test_exception_group():
    pass
```

第一个参数是表达式，为 `True` 就跳过。

### xfail——预期失败

有些测试目前过不了，但又不想完全跳过。比如某个 bug 还没修，想让测试存在着提醒大家。

<!-- skip-ci -->
```python
@pytest.mark.xfail(reason="bug #42 还没修")
def test_buggy_feature():
    assert buggy_function() == "expected"
```

`xfail` 的逻辑是「我预期它会挂」：

- 如果挂了：算 PASS（符合预期）
- 如果意外通过了：算 XPASS（提醒你 bug 可能修好了）

### 自定义 marker——给测试分类

各位有时候想给测试分类。比如「慢测试」「需要数据库的测试」「网络测试」。

<!-- skip-ci -->
```python
@pytest.mark.slow
def test_big_data():
    process_one_million_rows()


@pytest.mark.db
def test_query_user():
    pass


@pytest.mark.network
def test_fetch_api():
    pass
```

然后命令行用 `-m` 挑着跑：

```bash
# 只跑慢测试
pytest -m slow

# 跑除了慢测试以外的
pytest -m "not slow"

# 跑慢测试或网络测试
pytest -m "slow or network"
```

自定义 marker 用之前要先在配置里登记一下，不然 `pytest` 会警告。在 `pyproject.toml` 里：

```toml
[tool.pytest.ini_options]
markers = [
    "slow: 慢测试（耗时 > 1 秒）",
    "db: 需要数据库的测试",
    "network: 需要网络的测试",
]
```

这样写好处有两个——一是消除警告，二是新人来看 `pyproject.toml` 就知道项目里都有哪些测试分类。



## 覆盖率——哪些代码还没被测到

各位项目里写了一堆测试，跑起来全绿，开心。可是真的「测全了」吗？

「覆盖率」（coverage）这个概念就是用来回答这个问题的——**到底有多少代码在测试中被执行过**。100 行代码，测试只跑到了 60 行，覆盖率就是 60%。剩下那 40 行可能藏着 bug。

Python 圈测覆盖率的工具是 `coverage`，跟 `pytest` 配套用一般装 `pytest-cov` 这个插件，更简洁。

```bash
uv add --dev pytest-cov
```

跑：

```bash
# 跑测试 + 输出覆盖率报告
pytest --cov=src

# 也可以指定包名
pytest --cov=mypackage

# 输出更详细的「哪几行没测到」
pytest --cov=src --cov-report=term-missing
```

输出大概长这样：

```
---------- coverage: platform darwin, python 3.13.1 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
src/mymath.py        12      2    83%   15-16
src/utils.py          8      0   100%
-----------------------------------------------
TOTAL                20      2    90%
```

看 `Missing` 那列——`mymath.py` 的第 15、16 行没被测到。各位拉过去看一下，很可能就是某个边界条件没覆盖到。

要更直观，生成 HTML 报告：

```bash
pytest --cov=src --cov-report=html
```

会在 `htmlcov/` 目录下生成网页报告。打开 `htmlcov/index.html`，每个文件点进去能看到**哪一行被测了（绿色）、哪一行没测（红色）**，特别直观。

`pytest-cov` 还能写到 `pyproject.toml` 里设默认参数：

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing"
```

这样以后跑 `pytest` 就自动带覆盖率报告。

那覆盖率多少算合格？社区的「常识值」是这样的——

- **80% 以上**：基本及格线
- **90% 以上**：项目质量比较高
- **100%**：理想，但通常代价很高（要测各种「不可能发生」的分支）

水哥的建议是——**别死追 100%**。强追覆盖率会逼出来一堆「为了凑数而写的测试」，反而拖累项目。重点是关键业务路径、复杂逻辑、边界条件这些地方测全。覆盖率工具是用来「找漏」的，不是用来「打分」的。

各位不用一上来就给老项目设 90% 的硬指标。从 50% 起步、每个 PR 守住「不下降」这条底线，长期下来项目就会越来越健壮。



## conftest.py——共享 fixture

各位写测试越写越多，会发现一个问题——**好几个测试文件都要用同一个 fixture**。

比如 `test_user.py`、`test_order.py`、`test_product.py` 都要一个 `db` fixture。难道每个文件都要写一遍？

不用。`pytest` 有一个特殊的文件叫 `conftest.py`，**放在 `conftest.py` 里的 fixture 自动可被同目录及子目录下的所有测试使用**——不需要 import。

举个例子：

```
tests/
├── conftest.py            # 共享 fixture 在这里
├── test_user.py
├── test_order.py
└── api/
    ├── conftest.py        # 子目录还能再加一份
    └── test_endpoints.py
```

`tests/conftest.py`：

<!-- skip-ci -->
```python
import pytest


@pytest.fixture
def db():
    conn = create_test_db()
    yield conn
    conn.close()


@pytest.fixture
def sample_user(db):
    user = User(name="walter", age=28)
    db.save(user)
    return user
```

`tests/test_user.py`：

```python
def test_get_user(db, sample_user):
    # 直接用，不用 import
    assert db.get_user(sample_user.id).name == "walter"
```

`tests/test_order.py`：

```python
def test_create_order(db, sample_user):
    # 一样可以直接用
    order = Order(user=sample_user, amount=100)
    db.save(order)
    assert order.id is not None
```

`tests/api/conftest.py` 还可以再补一份只对 `api/` 子目录生效的 fixture：

<!-- skip-ci -->
```python
import pytest


@pytest.fixture
def http_client():
    from httpx import Client
    with Client(base_url="http://localhost:8000") as c:
        yield c
```

`pytest` 会从测试文件所在目录开始往上查找所有 `conftest.py`，把里面的 fixture 都收集起来。所以**外层的 fixture 内层能用，反过来不行**。

各位项目里搞清楚这个规则，测试代码会非常清爽——共享逻辑全在 `conftest.py`，每个测试文件只关注自己的事。



## pyproject.toml 里配置 pytest

`pytest` 默认零配置就能用，但项目大了之后，几个常用配置写到 `pyproject.toml` 里能省很多事。

```toml
[tool.pytest.ini_options]
# 测试文件去哪找
testpaths = ["tests"]

# 默认参数（每次跑 pytest 都自动加上）
addopts = [
    "-v",                          # 详细输出
    "--strict-markers",            # 用了未登记的 marker 报错
    "--cov=src",                   # 跑覆盖率
    "--cov-report=term-missing",   # 显示未覆盖的行
]

# 自定义 marker 登记
markers = [
    "slow: 慢测试",
    "db: 需要数据库的测试",
    "network: 需要网络的测试",
]

# 最低 Python 版本
minversion = "8.0"
```

老项目里如果是 `setup.cfg` 或 `pytest.ini`，迁移到 `pyproject.toml` 也很顺利——把 `[pytest]` 段改成 `[tool.pytest.ini_options]` 就行。`pytest 8.x` 之后 `pyproject.toml` 的支持已经非常成熟，新项目直接用它。



## 一个完整小实战——给 Wallet 类写测试

各位还记得 python17 讲类型注解时，咱们写过一个 `Wallet` 类吗？这次咱们把它写完整、再给它写一套像样的测试。

先看 `wallet.py`（升级版，多加了几个方法、加了简单的 IO 持久化）：

```python
from __future__ import annotations
import json
from pathlib import Path


class InsufficientFundsError(Exception):
    """余额不足时抛出。"""


class Wallet:
    """一个简单的钱包。"""

    def __init__(self, initial: float = 0) -> None:
        if initial < 0:
            raise ValueError("初始余额不能为负数")
        self.balance: float = initial

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("存入金额必须大于 0")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("取出金额必须大于 0")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"余额不足：当前 {self.balance}，想取 {amount}"
            )
        self.balance -= amount
        return self.balance

    def can_afford(self, price: float) -> bool:
        return self.balance >= price

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps({"balance": self.balance}),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> Wallet:
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(initial=data["balance"])
```

各位看一眼这个类，有几个测试点：

1. 初始化：负数初始余额应该抛 `ValueError`
2. `deposit`：金额 ≤ 0 应抛 `ValueError`；正常存入后余额加上
3. `withdraw`：金额 ≤ 0 抛 `ValueError`；超额抛 `InsufficientFundsError`；正常取出后余额减去
4. `can_afford`：低于、等于、高于余额三种情况
5. `save` / `load`：写到文件再读回来，余额一致

接下来写测试 `test_wallet.py`：

<!-- skip-ci -->
```python
import json
import pytest
from wallet import Wallet, InsufficientFundsError


# ---------- fixture ----------

@pytest.fixture
def empty_wallet() -> Wallet:
    """每个测试拿一个空钱包。"""
    return Wallet()


@pytest.fixture
def rich_wallet() -> Wallet:
    """每个测试拿一个 1000 块的钱包。"""
    return Wallet(initial=1000)


# ---------- 初始化 ----------

def test_default_balance(empty_wallet):
    assert empty_wallet.balance == 0


def test_init_with_money():
    w = Wallet(initial=500)
    assert w.balance == 500


def test_negative_initial_raises():
    with pytest.raises(ValueError, match="不能为负数"):
        Wallet(initial=-1)


# ---------- deposit ----------

@pytest.mark.parametrize("amount, expected", [
    (100, 1100),
    (0.5, 1000.5),
    (1, 1001),
])
def test_deposit(rich_wallet, amount, expected):
    assert rich_wallet.deposit(amount) == expected
    assert rich_wallet.balance == expected


@pytest.mark.parametrize("bad_amount", [0, -1, -100])
def test_deposit_invalid(empty_wallet, bad_amount):
    with pytest.raises(ValueError, match="必须大于 0"):
        empty_wallet.deposit(bad_amount)


# ---------- withdraw ----------

def test_withdraw_normal(rich_wallet):
    assert rich_wallet.withdraw(300) == 700
    assert rich_wallet.balance == 700


def test_withdraw_too_much(rich_wallet):
    with pytest.raises(InsufficientFundsError) as exc_info:
        rich_wallet.withdraw(2000)
    assert "余额不足" in str(exc_info.value)


@pytest.mark.parametrize("bad_amount", [0, -1])
def test_withdraw_invalid(rich_wallet, bad_amount):
    with pytest.raises(ValueError, match="必须大于 0"):
        rich_wallet.withdraw(bad_amount)


# ---------- can_afford ----------

@pytest.mark.parametrize("price, ok", [
    (500, True),    # 低于余额
    (1000, True),   # 等于余额
    (1001, False),  # 高于余额
    (0, True),      # 0 块也买得起（边界）
])
def test_can_afford(rich_wallet, price, ok):
    assert rich_wallet.can_afford(price) is ok


# ---------- save / load 用 tmp_path ----------

def test_save_and_load_roundtrip(rich_wallet, tmp_path):
    file = tmp_path / "wallet.json"
    rich_wallet.save(file)

    assert file.exists()
    data = json.loads(file.read_text(encoding="utf-8"))
    assert data == {"balance": 1000}

    loaded = Wallet.load(file)
    assert loaded.balance == 1000


def test_save_overwrite(rich_wallet, tmp_path):
    file = tmp_path / "wallet.json"

    rich_wallet.save(file)
    rich_wallet.deposit(500)
    rich_wallet.save(file)

    loaded = Wallet.load(file)
    assert loaded.balance == 1500
```

跑一下：

```bash
uv run pytest -v
```

输出（节选）：

```
test_wallet.py::test_default_balance PASSED
test_wallet.py::test_init_with_money PASSED
test_wallet.py::test_negative_initial_raises PASSED
test_wallet.py::test_deposit[100-1100] PASSED
test_wallet.py::test_deposit[0.5-1000.5] PASSED
test_wallet.py::test_deposit[1-1001] PASSED
test_wallet.py::test_deposit_invalid[0] PASSED
test_wallet.py::test_deposit_invalid[-1] PASSED
test_wallet.py::test_deposit_invalid[-100] PASSED
test_wallet.py::test_withdraw_normal PASSED
test_wallet.py::test_withdraw_too_much PASSED
test_wallet.py::test_withdraw_invalid[0] PASSED
test_wallet.py::test_withdraw_invalid[-1] PASSED
test_wallet.py::test_can_afford[500-True] PASSED
test_wallet.py::test_can_afford[1000-True] PASSED
test_wallet.py::test_can_afford[1001-False] PASSED
test_wallet.py::test_can_afford[0-True] PASSED
test_wallet.py::test_save_and_load_roundtrip PASSED
test_wallet.py::test_save_overwrite PASSED

============================= 19 passed in 0.05s ==============================
```

各位数一下——一共 12 个测试函数，但是因为有参数化，**实际跑了 19 个用例**。19 个用例 0.05 秒跑完，覆盖了正常路径、边界条件、异常分支、文件 IO。

再加上覆盖率：

```bash
uv run pytest --cov=. --cov-report=term-missing
```

理想情况下应该达到 100%——所有方法、所有分支、所有异常路径都测到了。

这就是各位以后每写一个类、一个模块都该做的事——**功能代码 + 测试代码**像孪生兄弟一样一起出现，缺一不可。



## 几个常见踩坑

### 坑 1：测试函数互相影响

```python
counter = 0


def test_a():
    global counter
    counter += 1
    assert counter == 1


def test_b():
    global counter
    counter += 1
    assert counter == 1     # 这里挂——counter 已经是 2
```

测试之间共享了全局状态。`test_a` 先跑改了 `counter`，`test_b` 看到的就不是干净状态了。

**解决**：测试要么用 fixture 准备状态、要么测函数本身别有副作用。**不要用全局变量在测试间传东西**。

### 坑 2：测试时间太长

测试越写越多，跑一次几分钟。开发人员就懒得跑了，最后测试形同虚设。

**解决**：

- 慢的测试加 `@pytest.mark.slow`，本地不跑，CI 才跑
- fixture scope 调高（数据库连接 session 级别）
- 用 `pytest-xdist` 插件并行跑：`pytest -n auto`

### 坑 3：浮点数比较

```python
def test_divide():
    assert divide(1, 3) == 0.3333333333333333    # 浮点精度问题
```

浮点数本身就有精度误差，直接 `==` 比经常挂。

**解决**：用 `pytest.approx`：

```python
def test_divide():
    assert divide(1, 3) == pytest.approx(0.3333, rel=1e-3)
```

`approx` 表示「近似相等」，可以指定相对误差或绝对误差。

### 坑 4：fixture 之间循环依赖

<!-- skip-ci -->
```python
@pytest.fixture
def a(b):
    return b + 1


@pytest.fixture
def b(a):       # 循环依赖
    return a - 1
```

`pytest` 会直接报错：`fixture 'a' is recursive`。

**解决**：检查 fixture 依赖图，把循环打开。通常说明有一个 fixture 该被拆成两个独立的。

### 坑 5：用 `print` 调试结果看不到

各位 debug 时随手加了 `print`，跑 `pytest` 后发现啥也没看到。

**原因**：`pytest` 默认捕获所有 stdout，只在测试失败时才显示。

**解决**：加 `-s` 参数：

```bash
pytest -s
```

或者改用 `pytest --capture=no`，效果一样。



## FAQ

**Q1：测试要写在哪？跟源码一起吗？**

主流是分开放——源码 `src/`，测试 `tests/`。这样打包发布时测试代码不会被打进去。

也有项目把测试挨着源码放，比如 `mypackage/test_foo.py` 紧挨着 `mypackage/foo.py`。各有各的好。新项目水哥推荐分开。

**Q2：要不要把所有功能都测到？**

不必。**关键路径必须测、边界条件优先测、异常路径要测**；纯 getter/setter 那种琐碎的代码可以不测；私有函数大多通过测公共接口间接覆盖。

**Q3：mock 和 fixture 是一回事吗？**

不是同一个东西，但经常一起用。

- **fixture** 是「准备测试需要的东西」（连接、用户、临时目录）
- **mock** 是「假装某个对象/函数」（不真的发请求，假装返回了某个值）

`pytest` 自带 `monkeypatch`（轻量 mock）；想要更强大的 mock，用标准库的 `unittest.mock`，或第三方 `pytest-mock` 插件。

**Q4：测试代码里有重复怎么办？**

跟普通代码一样——抽函数、抽 fixture、用参数化。但**测试代码可读性优先于 DRY**。一个测试如果为了不重复写得让人看不懂，宁可让它重复点。读测试的人想一眼看清「这个测试在测啥」，不想去翻一堆 helper 函数。

**Q5：测试该跑多快？**

单元测试（不连数据库、不访问网络）应该是**秒级**——一个项目几百个单元测试，目标是几秒到十几秒跑完。集成测试可以慢一点，但建议放在单独的 marker（比如 `@pytest.mark.integration`）里，跟单元测试分开跑。



## 小结

各位走完这一章，应该已经能：

1. 写一个 `pytest` 测试：`def test_xxx(): assert ...`
2. 用 `fixture` 把准备工作抽出来，用 `scope` 控制生命周期
3. 用 `tmp_path`、`monkeypatch`、`capsys` 这些内置 fixture 搞定文件、环境、输出
4. 用 `@pytest.mark.parametrize` 把同一逻辑的多组数据合并
5. 用 `with pytest.raises(...)` 测异常路径
6. 用 `@pytest.mark.skip`、`skipif`、自定义 marker 给测试分类
7. 用 `pytest-cov` 看覆盖率，找出漏测的代码
8. 用 `conftest.py` 在多个测试文件之间共享 fixture
9. 在 `pyproject.toml` 里集中配置 `pytest`

`pytest` 的好处是**每写一行代码，心里都更踏实**——下次再改老代码，跑一下测试就知道有没有改坏。水哥当年写第一份完整测试套件的时候那种感觉，跟通了任督二脉一样：从「不敢动」变成「随便动」，因为绿色那一片测试就是你最忠诚的安全网。

回到开头那个问题——「我代码改一改没事吧？」

现在各位有答案了吗？跑一下测试就行。

下一章咱们讲讲怎么把这套东西接进 GitHub Actions——`uv` 管依赖、`ruff` 管风格、`pytest` 管测试，三件套配齐之后，提一个 PR 自动跑、自动报告、自动拒绝坏代码，2026 年的 Python 工程化才算真正闭环。



## 从需求里找测试，不从实现里抄答案

我们要统计分钟数，先列出三种情况：没有记录、普通记录、含零分钟的记录。预期值先手工算清楚，再核对函数：

```python
def total_minutes(records):
    return sum(record['minutes'] for record in records)


assert total_minutes([]) == 0
assert total_minutes([{'minutes': 15}, {'minutes': 10}]) == 25
assert total_minutes([{'minutes': 0}, {'minutes': 5}]) == 5
print('3 项检查通过')
```

输出：

```text
3 项检查通过
```

自己把函数改成「只返回第一条记录的分钟数」，看看哪一个检查失败。如果测试只准备一条记录，这个错误就可能漏过去。

综合项目的 `test_tracker.py` 还检查科目筛选、中文保存、损坏文件、无效分钟数和命令行行为。它使用标准库测试类，既能用 `python3 -m unittest -v` 运行，准备好 pytest 的项目也可以用 `python3 -m pytest -q` 发现这些测试。

文件测试使用专用测试数据，别让测试直接读写自己的正式学习记录。这里的 `assert` 演示用于验证结果，不代替程序对用户输入的正式校验；优化模式可能移除断言。

阅读 [pytest 官方断言说明](https://docs.pytest.org/en/stable/how-to/assert.html) 时，可以带着自己刚刚制造的那个失败去看提示，理解工具怎样帮助我们定位差异。
