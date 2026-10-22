# ruff：一个工具替掉 black + flake8 + isort + pyupgrade

各位还记不记得 2022 年那会儿，开一个 Python 新项目，光「保证代码风格统一」这件事就要装一堆东西：

- `black`：自动格式化代码，管缩进、换行、引号
- `flake8`：检查语法错误、未使用变量、命名不规范
- `isort`：把 `import` 语句按字母顺序、按分组重新排列
- `pyupgrade`：把老语法升级到新版本，比如 `Dict[str, int]` 改成 `dict[str, int]`
- `pydocstyle`：检查 docstring 写得规不规范
- `bandit`：扫一扫有没有安全漏洞

六个工具，六份配置文件，六套规则，每个工具自己装一遍，CI 上每个跑一遍，commit 之前每个调一遍。水哥当年配一个新项目的 lint 流水线，光研究这些工具怎么互相不打架就能花掉半天。

「不能合并一下吗？」当年很多童鞋都问过这个问题。

合不了。这些工具互相独立，技术栈也不一样：`black` 用 `Python` 写，`flake8` 用 `Python` 写但内核是 `pycodestyle`，`isort` 自己是个独立项目。要把它们捏到一起，意味着要重新实现一遍。

直到 2022 年底，Astral 公司——就是上一章那个写 `uv` 的 Astral——丢出来一个叫 `ruff` 的东西。这家公司有个特点：用 `Rust` 重写 Python 工具链，并且**比原版快 10 到 100 倍**。

`ruff` 一上来就把 `flake8`、`isort`、`pyupgrade`、`pydocstyle`、`bandit` 这些工具的规则一口气全实现了，后来又补上了 `format` 子命令，把 `black` 的功能也吃掉了。一个二进制文件，一份配置，一套命令。

到 2024 年，`ruff` 已经是 Python 社区的事实标准，`Pandas`、`FastAPI`、`Pydantic`、`Hugging Face Transformers`、`Apache Airflow` 都换了过去。到 2026 年的今天，各位开新项目，几乎不会再有人推荐用 `flake8 + black + isort` 这套老组合了。

这一章就来讲讲 `ruff` 怎么用。学完之后，各位应该能：

1. 在新项目里五分钟内配好 `ruff`
2. 看懂别人 `pyproject.toml` 里那一坨 `[tool.ruff]` 配置
3. 把 `ruff` 接进 `pre-commit`、`CI`、编辑器
4. 把老项目从 `black + flake8 + isort` 平滑迁移过来


## 老办法到底烦在哪

先回忆一下老办法是怎么个用法。一个比较「正经」的项目，根目录下通常会出现这些配置：

```
my-project/
├── pyproject.toml         # 部分工具的配置
├── setup.cfg              # flake8 必须放这里（或单独的 .flake8）
├── .flake8                # flake8 配置（可选）
├── .isort.cfg             # isort 配置（可选）
├── .pre-commit-config.yaml
└── ...
```

每个工具有自己偏好的配置文件位置：

- `black` 看 `pyproject.toml` 的 `[tool.black]`
- `flake8` 死活不支持 `pyproject.toml`，只能用 `.flake8` 或 `setup.cfg`
- `isort` 可以放 `pyproject.toml`、`.isort.cfg`、`setup.cfg`，看心情
- `pyupgrade` 没配置文件，全靠命令行参数

这就埋了第一个坑——**配置散落各处**，新人接手项目，光找配置文件就要找半天。

第二个坑是**工具之间会打架**。最经典的就是 `black` 和 `flake8` 冲突。`black` 默认行宽 88 字符，`flake8` 默认行宽 79 字符（PEP 8 推荐值）。两个不调一致，`black` 格式化完，`flake8` 就报 `E501 line too long`。怎么办？要么改 `flake8`，要么改 `black`，要么两边都加 `# noqa` 注释。

`isort` 和 `black` 也会打架。`isort` 默认按某种风格排 `import`，`black` 不一定接受，要给 `isort` 加上 `--profile black` 才能一致。

第三个坑是**慢**。这个慢不是「人感觉慢」，是真的慢——一个中型项目，跑 `flake8 .` 几秒到几十秒；跑 `black .` 几秒到十几秒；跑 `isort .` 也要几秒。CI 上串起来跑一遍，几十秒就没了。本地保存文件时想跑一遍 lint，慢到没法接进编辑器。

这就是 2022 年之前 Python 工程化的真实情况。各位老司机看到这里应该能共鸣。


## ruff 是个啥

`ruff` 是 Astral 公司开源的 Python 代码检查 + 格式化工具。两个关键属性：

1. **用 Rust 写的**。Python 工具用 Python 写，速度天花板就在那里。换成 Rust，速度能上一两个数量级。
2. **一个工具替掉一堆**。`flake8`、`black`、`isort`、`pyupgrade`、`pydocstyle`、`bandit`、`pylint` 的部分规则、`autoflake`，全部内置。

看一下 `ruff` 官方公布的速度对比。在 `CPython` 项目（约 25 万行代码）上跑：

| 工具 | 耗时 |
|---|---|
| `flake8` | 12 秒左右 |
| `pylint` | 几分钟 |
| `ruff check` | 0.4 秒左右 |

各位读到这里可能怀疑：「真的有这么快吗，会不会是数据造假？」水哥亲自在自己电脑上跑过，结论是**真的就是这么快**。一个一千文件的项目，`ruff check .` 经常一秒之内出结果，肉眼看不到「跑」的过程。

`ruff format` 也类似。一个中等大小的项目，`black` 跑十几秒，`ruff format` 一秒不到。

这速度有什么用？两点重要：

1. **保存文件时实时跑 lint** 成为可能。编辑器里每次 `Ctrl+S`，`ruff` 后台跑一遍，几乎感觉不到延迟。
2. **CI 时间短**。从前 lint 阶段要 30 秒，现在 1 秒就过了。

「那它支持多少规则？」有童鞋想知道这个。截至 2026 年，`ruff` 已经实现了 800 多条规则，覆盖了 `flake8` 主线 + 几十个 `flake8-*` 插件 + `isort` + `pyupgrade` + `pydocstyle` + `pylint` 的一部分 + `bandit` 的一部分。换句话说，几乎所有主流 Python lint 工具的能力，`ruff` 都吃下来了。


## 安装

老规矩，推荐用 `uv` 装：

```bash
uv add --dev ruff
```

「`--dev` 是啥意思？」上一章讲过，意思是「装到开发依赖组」，发布生产环境时不会带上。`ruff` 是开发工具，只在开发和 CI 时用，所以放 `--dev` 最合适。

如果项目还没用 `uv`，用 `pip` 装也行：

```bash
pip install ruff
```

或者用 `pipx` 装成全局命令：

```bash
pipx install ruff
```

装完之后，验证一下：

```bash
ruff --version
```

输出类似：

```
ruff 0.8.0
```

具体版本号会变，2026 年的 `ruff` 应该已经到 0.9 或者 1.0 之后了。

「为什么版本号都还没到 1.0？」有细心的童鞋会问。`ruff` 的作者一直在小步迭代，规则集还在持续扩充，所以版本号一直保持在 0.x。但稳定性其实早就生产级别了，社区里大量项目在用，没什么大问题。


## 第一次跑

进项目目录，跑一下：

```bash
ruff check .
```

这条命令会扫描当前目录下所有 `.py` 文件，按默认规则检查。各位第一次跑大概率会看到一堆告警：

```
foo.py:3:1: F401 [*] `os` imported but unused
foo.py:8:5: E731 Do not assign a `lambda` expression, use a `def`
bar.py:12:80: E501 Line too long (95 > 79)
```

格式很清晰：`文件名:行:列: 规则号 描述`。规则号前面如果带个 `[*]`，说明这条规则可以**自动修复**。

要让 `ruff` 自动修，加 `--fix`：

```bash
ruff check --fix .
```

跑完之后，`os imported but unused` 这种问题，`ruff` 直接把那行 `import os` 删掉了。各位再跑一次 `ruff check .`，告警少了一大半。

格式化代码用另一个子命令：

```bash
ruff format .
```

这条命令的行为基本和 `black .` 一样——把整个项目的代码风格统一到一致的缩进、引号、换行规则。各位之前如果用过 `black`，这一步零学习成本。

把这两条命令加在一起，就是日常 commit 之前的标准流程：

```bash
ruff check --fix . && ruff format .
```

先 lint 再 format，齐活。


## 配置：pyproject.toml

`ruff` 的配置全部塞进 `pyproject.toml`，没有别的文件。配置长这样：

```toml
[tool.ruff]
# 行宽，跟 black 默认一致
line-length = 88

# 目标 Python 版本，影响某些规则的判断
target-version = "py312"

# 排除哪些目录
exclude = [
    ".git",
    ".venv",
    "build",
    "dist",
    "__pycache__",
    "migrations",
]

[tool.ruff.lint]
# 启用哪些规则集
select = ["E", "F", "I", "UP", "B", "SIM"]

# 忽略哪些具体规则
ignore = ["E501"]

[tool.ruff.format]
# 引号风格：双引号优先（black 风格）
quote-style = "double"
# 缩进风格：空格
indent-style = "space"
```

各位看着这一坨可能有点懵，下面挨个拆开讲。

### line-length

行宽。默认 88，跟 `black` 一致。喜欢 100 也行：

```toml
line-length = 100
```

### target-version

目标 Python 版本。这个值影响一些规则的判断。比如 `target-version = "py312"`，`ruff` 知道 `dict[str, int]` 这种语法你能用，会建议把老代码里的 `Dict[str, int]` 改过来。如果你写 `target-version = "py38"`，`ruff` 就不会做这种建议（因为 3.8 不支持）。

合法值：`py38`、`py39`、`py310`、`py311`、`py312`、`py313`、`py314`。

### exclude

不扫描哪些目录。`.git`、`.venv`、`build`、`dist` 这些 `ruff` 默认就会排除，但是 `migrations`（Django 项目自动生成的迁移文件）这种，需要自己加。

### select

最重要的字段——**启用哪些规则集**。`ruff` 用「字母前缀」给规则分组：

- `E`：`pycodestyle` 错误（PEP 8 风格规则）
- `W`：`pycodestyle` 警告
- `F`：`pyflakes`（未使用变量、未定义引用等）
- `I`：`isort`（import 排序）
- `UP`：`pyupgrade`（语法升级建议）
- `B`：`flake8-bugbear`（常见 bug 模式）
- `SIM`：`flake8-simplify`（简化代码建议）
- `N`：`pep8-naming`（命名规范）
- `D`：`pydocstyle`（docstring 规范）
- `S`：`flake8-bandit`（安全检查）
- `ANN`：`flake8-annotations`（类型注解）
- `C4`：`flake8-comprehensions`（推导式优化）
- `RET`：`flake8-return`（return 语句规范）
- `ARG`：`flake8-unused-arguments`（未使用参数）

每个前缀下面还有具体规则，比如 `E501` 是「行太长」、`F401` 是「import 但没用」。

新项目第一次配，推荐这一套：

```toml
select = ["E", "F", "I", "UP", "B", "SIM"]
```

`E + F` 是基本款（PEP 8 + pyflakes），`I` 管 import 排序，`UP` 把老语法升级到新版本，`B` 抓常见 bug，`SIM` 给一些简化建议。这六组覆盖了 80% 的需求，又不会噪声太大。

如果项目对代码质量要求高，再加上 `N`（命名规范）、`C4`（推导式）、`RET`（return）、`ARG`（未用参数）。

如果还要加 docstring 检查（`D`），各位要做好心理准备——`pydocstyle` 的规则很严格，老项目一开就是几百条告警。建议从 `select = ["D"]` + `ignore = ["D100", "D101", "D102", ...]` 一条条试，别一上来就全开。

### ignore

忽略某些具体规则。比如 `E501`（行太长），有些项目觉得 88 字符不够用，就加进 `ignore`：

```toml
ignore = ["E501"]
```

或者忽略整个组：

```toml
ignore = ["D"]
```

### per-file-ignores

按文件忽略规则。`__init__.py` 经常有未使用的 import（其实是用来重导出的），不想被告警，可以这样：

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101", "ANN"]
```

`tests/*` 里允许用 `assert`（`S101`），不要求每个测试函数都写类型注解（`ANN`）。

### isort 子配置

`I` 规则集（isort 替代）有自己的子配置，放 `[tool.ruff.lint.isort]`：

```toml
[tool.ruff.lint.isort]
# 把这些当成「第一方」包，跟其他第三方分开排
known-first-party = ["my_project"]

# import 块的分组顺序
section-order = [
    "future",
    "standard-library",
    "third-party",
    "first-party",
    "local-folder",
]
```

`known-first-party` 这个配置很常用——告诉 `ruff`「`my_project` 是我自己的包」，`ruff` 就会把它的 `import` 放到独立的一组，不跟第三方包混在一起。


## 完整配置示例

放一份生产可用的 `pyproject.toml` 配置，各位可以直接抄回去改：

```toml
[tool.ruff]
line-length = 88
target-version = "py312"
exclude = [
    ".git",
    ".venv",
    "build",
    "dist",
    "__pycache__",
    "migrations",
    "*.ipynb",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "SIM", # flake8-simplify
    "C4",  # flake8-comprehensions
    "N",   # pep8-naming
    "RET", # flake8-return
]
ignore = [
    "E501",  # 行太长，交给 formatter 处理
    "B008",  # 函数默认参数里调用函数，FastAPI 的 Depends 用法
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

抄这份过去，改一下 `target-version` 和 `known-first-party`，基本就能用。


## 常用规则集一览

把上面提到的规则集整理成一张对照表，方便各位查：

| 前缀 | 来源工具 | 管什么 |
|---|---|---|
| `E` | `pycodestyle` | PEP 8 风格错误（缩进、空格） |
| `W` | `pycodestyle` | PEP 8 风格警告 |
| `F` | `pyflakes` | 未使用变量、未定义引用、import 错 |
| `I` | `isort` | import 排序与分组 |
| `UP` | `pyupgrade` | 老语法升级到新版本 |
| `B` | `flake8-bugbear` | 常见 bug 模式 |
| `SIM` | `flake8-simplify` | 代码简化建议 |
| `N` | `pep8-naming` | 命名规范（驼峰、下划线） |
| `D` | `pydocstyle` | docstring 规范 |
| `S` | `flake8-bandit` | 安全漏洞检查 |
| `ANN` | `flake8-annotations` | 类型注解检查 |
| `C4` | `flake8-comprehensions` | 推导式优化 |
| `RET` | `flake8-return` | return 语句风格 |
| `ARG` | `flake8-unused-arguments` | 未使用参数 |
| `PT` | `flake8-pytest-style` | pytest 风格 |
| `PL` | `pylint` | pylint 部分规则 |
| `RUF` | `ruff` | ruff 自家原创规则 |

完整清单官方文档里有，叫「Rules」页面，规则号、说明、是否能自动修都列得清清楚楚。各位用到哪条规则不懂，搜一下规则号就行。


## 自动修复实战

`ruff check --fix .` 能修哪些东西？挑几个常见的看看。

### F401：未使用的 import

```python
import os
import sys

print(sys.version)
```

`ruff check --fix` 之后：

```python
import sys

print(sys.version)
```

`os` 没用上，直接删掉。

### E711：和 None 比较应该用 is

<!-- skip-ci -->
```python
if x == None:
    print("x 是 None")
```

修复后：

<!-- skip-ci -->
```python
if x is None:
    print("x 是 None")
```

为什么要改？因为 `==` 会触发 `__eq__` 方法，有些类的 `__eq__` 实现得稀奇古怪（比如 `numpy` 数组），跟 `None` 比较会出意想不到的结果。`is None` 是身份比较，永远只看「是不是同一个对象」，绝对安全。

### C408：不必要的 list/dict/tuple 调用

```python
empty = list()
d = dict()
t = tuple()
```

修复后：

```python
empty = []
d = {}
t = ()
```

`list()` 和 `[]` 等价，但是 `list()` 要去全局名字空间里查 `list` 这个名字、再调用，慢一点。直接写字面量更快也更短。

### UP006：用新版类型注解

```python
from typing import List, Dict

def foo(x: List[int]) -> Dict[str, int]:
    pass
```

修复后（`target-version = "py39"` 以上）：

```python
def foo(x: list[int]) -> dict[str, int]:
    pass
```

Python 3.9+ 已经支持直接用 `list[int]` 写类型注解，不用再从 `typing` 里 import 了。`ruff` 自动帮各位升级。

### UP008：用 super() 不要带参数

<!-- skip-ci -->
```python
class Foo(Bar):
    def __init__(self):
        super(Foo, self).__init__()
```

修复后：

<!-- skip-ci -->
```python
class Foo(Bar):
    def __init__(self):
        super().__init__()
```

Python 3 里 `super()` 不传参数就够了，老 Python 2 风格的 `super(Foo, self)` 是历史包袱。

### SIM108：能用三元表达式不要用 if-else

<!-- skip-ci -->
```python
if x > 0:
    y = "positive"
else:
    y = "non-positive"
```

`ruff` 会建议（这条不是自动修，因为牵涉可读性，需要人判断）：

<!-- skip-ci -->
```python
y = "positive" if x > 0 else "non-positive"
```

### I001：import 排序

<!-- skip-ci -->
```python
import sys
from my_project import utils
import os
import requests
```

修复后：

<!-- skip-ci -->
```python
import os
import sys

import requests

from my_project import utils
```

`ruff` 把 import 按「标准库 → 第三方 → 第一方」分成三组，每组之间空一行，组内按字母序排。这等同于跑了一遍 `isort`。

### 不安全修复

有些修复 `ruff` 不会默认做，因为可能改变行为。比如把 `dict()` 改成 `{}`——99% 情况下等价，但是如果你的代码里 `dict` 这个名字被覆盖了，行为就变了。这种修复叫「unsafe fix」，要加 `--unsafe-fixes` 才会做：

```bash
ruff check --fix --unsafe-fixes .
```

各位如果心里没底，先 `ruff check --fix .` 跑安全的，再用 `--unsafe-fixes` 单独跑一遍并 review 改动。


## ruff format：black 替代品

`ruff format .` 干的事跟 `black .` 几乎一样：

- 行宽默认 88
- 字符串默认双引号
- 缩进 4 空格
- 函数参数过长自动换行
- 字典、列表、`set` 字面量按一致风格排版

格式化前：

```python
def foo(a,b,c, d ):
    return  {  'name':a,'age':b,'list':[1,2,3]  }
```

`ruff format .` 之后：

```python
def foo(a, b, c, d):
    return {"name": a, "age": b, "list": [1, 2, 3]}
```

跟 `black` 输出几乎完全一致。Astral 在文档里明确写过「`ruff format` 与 `black` 99.9% 兼容」，各位从 `black` 迁过来不用担心代码风格突变。

少量差异确实存在，主要在边缘情况（极长行、特殊魔法注释等），跑一遍 `ruff format`，git diff 一看就知道。

`ruff format` 也支持 `--check` 模式，只检查不改：

```bash
ruff format --check .
```

如果有文件需要格式化，命令返回非零 exit code，CI 上可以拿来卡住「忘了 format 就提交」的 PR。


## 集成 pre-commit

`pre-commit` 是一个 git hook 框架，让各位在 `git commit` 时自动跑一些检查。装一下：

```bash
uv add --dev pre-commit
pre-commit install
```

然后在项目根目录建 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

这一段配置干了两件事：

1. `ruff` hook：跑 `ruff check --fix`，自动修能修的
2. `ruff-format` hook：跑 `ruff format`

每次 `git commit`，`pre-commit` 会自动跑这两个 hook，跑通才让 commit。

「`rev: v0.8.0` 怎么填？」`pre-commit` 上有命令自动填最新版：

```bash
pre-commit autoupdate
```

跑一下，`.pre-commit-config.yaml` 里的版本号就更新到最新了。建议各位每隔几个月跑一次。

第一次装好 `pre-commit`，可以手动跑一遍：

```bash
pre-commit run --all-files
```

把项目里所有文件都过一遍，把历史欠债一次性清干净。

「为什么不直接用 `ruff` 自己的 hook？」有童鞋会问。`ruff` 没有自己的 git hook 机制，要靠 `pre-commit` 这种通用框架。`pre-commit` 是 Python 圈里通用方案，除了 `ruff` 还能挂别的 hook（比如 `mypy`、`prettier`），统一管理。


## 集成 GitHub Actions CI

`ruff` 在 CI 上的用法非常简单。新建 `.github/workflows/lint.yml`：

```yaml
name: Lint

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Install ruff
        run: uv tool install ruff

      - name: Run ruff check
        run: ruff check --output-format=github .

      - name: Run ruff format check
        run: ruff format --check .
```

`--output-format=github` 这个选项很重要——它把告警输出成 GitHub Actions 能识别的格式，PR 页面上会直接在出问题的代码行上显示一个小标记，鼠标悬停就能看到具体规则和说明。比纯文本日志好用得多。

也有官方做的 action，更省事：

```yaml
- name: Run ruff
  uses: astral-sh/ruff-action@v3
```

这个 action 自动装 `ruff` 并跑 `ruff check`，一行搞定。各位有兴趣可以去 GitHub 搜 `astral-sh/ruff-action` 看文档。

CI 时间方面，`ruff` 这部分通常 5 秒以内跑完（包括环境准备），比从前 `flake8 + black + isort` 那一套快太多。

「能在 PR 上自动修复并提交回来吗？」可以，但是要小心处理权限和分叉 PR。一般做法是：CI 上只检查不修，由开发者自己在本地修完再推。要做自动修复 PR，得用专门的 bot 账号 + GitHub App，超出本章范围。


## 集成编辑器

代码风格工具最后一公里——编辑器集成。装好之后，每次保存文件，编辑器自动跑 `ruff`，问题立刻显示在出错的行上。这种体验和 CI、`pre-commit` 是不可替代的：CI 是兜底，编辑器是日常。

### VS Code

装这个插件：[Ruff (charliermarsh.ruff)](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

装完之后，`settings.json` 里加几行：

```json
{
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    }
}
```

效果：

- 保存文件时自动跑 `ruff format`
- 自动应用所有能自动修的 lint 修复
- 自动整理 import

写代码的时候，每次 `Ctrl+S`，`ruff` 在背后跑一遍，代码自动整齐。

### PyCharm

PyCharm 有官方支持的 `Ruff` 插件，去 `Settings → Plugins` 搜「Ruff」装上。

装完之后：

- `Settings → Tools → Ruff`：勾上「Use ruff format」、「Run ruff on save」
- `Settings → Editor → Code Style → Python`：行宽改成 88，跟 `ruff` 一致

PyCharm 的好处是检查在编辑时实时显示，不用等保存。问题代码会有黄色波浪线，鼠标悬停看具体规则。

### Neovim / Vim

通过 `nvim-lspconfig` + `mason.nvim` 装 `ruff` 的 LSP server：

```lua
require("lspconfig").ruff.setup({})
```

或者直接用 `null-ls` / `none-ls` 的 `ruff` 集成。具体用哪种取决于各位的 Neovim 配置框架。


## 从 black + flake8 + isort 迁移

老项目要换过来，怎么办？步骤：

### 第一步：装 ruff

```bash
uv add --dev ruff
```

### 第二步：写 ruff 配置

参考前面的「完整配置示例」，写一份 `[tool.ruff]` 进 `pyproject.toml`。`line-length`、`target-version` 等关键参数对齐原来 `black` 的配置。

### 第三步：跑一遍看看差异

```bash
ruff check .
ruff format --check .
```

`ruff check .` 看 lint 告警，`ruff format --check .` 看格式化差异。

`ruff format` 跟 `black` 99.9% 兼容，但还是会有少量文件被改。各位先 `ruff format .` 跑一遍，git diff 看一下，确认改动可接受再提交。

### 第四步：删掉老工具

```bash
uv remove --dev black flake8 isort pyupgrade
```

如果项目还在用 `pip` + `requirements-dev.txt`，从那里删。

### 第五步：删配置

`.flake8` 删掉，`setup.cfg` 里的 `[flake8]` 段删掉，`pyproject.toml` 里的 `[tool.black]`、`[tool.isort]` 段删掉。

### 第六步：更新 pre-commit 和 CI

`.pre-commit-config.yaml` 里把 `black`、`flake8`、`isort` 的 hook 删掉，换成 `ruff` 的。CI 同理。

### 第七步：通知团队

发一条消息给团队：「项目从 X 月 X 日起切换到 ruff，请大家拉最新代码、跑 `pre-commit install` 重装 hook」。一般这个步骤不会有什么问题，因为 `ruff format` 和 `black` 兼容，原来 `black` 格式化过的代码 `ruff` 不会再大改。


## ruff vs black + flake8 + isort 对照表

最后放一张对照表，方便各位心里有个底：

| 维度 | 老组合 | ruff |
|---|---|---|
| 工具数量 | 至少 3 个（black + flake8 + isort），加 pyupgrade、pydocstyle 更多 | 1 个 |
| 配置位置 | 散落在 `pyproject.toml`、`.flake8`、`setup.cfg` 等 | 全部在 `pyproject.toml` |
| 速度 | 几秒到几十秒 | 通常 1 秒以内 |
| 规则数量 | 各家加起来约 500 条 | 800+ 条 |
| 自动修复 | 部分支持（black、isort、pyupgrade 自动；flake8 不修） | 大部分规则支持 |
| 实现语言 | Python | Rust |
| 二进制依赖 | 安装 Python 包 | 单二进制（也能 pip 装） |
| 编辑器实时 lint | 慢，体验差 | 快，体验丝滑 |
| pyproject.toml 支持 | 部分（flake8 不支持） | 完全支持 |


## ruff 自家规则：RUF 系列

`ruff` 除了搬运别家规则，也自己原创了一些规则，前缀是 `RUF`。挑几个常见的看看。

### RUF001/RUF002/RUF003：模糊字符

代码里出现「看着是英文字母但其实是希腊字母、全角字符」这种字符，会触发 `RUF001`。比如：

<!-- skip-ci -->
```python
result = data["nаme"]  # 这里的 а 是西里尔字母 а，不是英文 a
```

肉眼几乎看不出来，但是程序跑起来会找不到键报 `KeyError`。`ruff` 能识别出这种字符并告警，避免各位调试到怀疑人生。

### RUF005：用解包代替 list 拼接

<!-- skip-ci -->
```python
new_list = [1, 2, 3] + list(other)
```

`ruff` 建议改成：

<!-- skip-ci -->
```python
new_list = [1, 2, 3, *other]
```

解包语法更快、更短，还能直接拼任何可迭代对象，不用先转成 list。

### RUF013：隐式 Optional 类型

<!-- skip-ci -->
```python
def greet(name: str = None):
    print(f"Hello, {name}")
```

这个写法很常见，但其实有问题——`name` 默认是 `None`，但类型注解写的是 `str`，前后不一致。`ruff` 会建议改成：

<!-- skip-ci -->
```python
def greet(name: str | None = None):
    print(f"Hello, {name}")
```

老 Python 写法是 `Optional[str]`，新版 Python（3.10+）直接用 `str | None` 更清爽。

### RUF100：未使用的 noqa

```python
x = 1  # noqa: F401
```

如果这一行其实没有任何 lint 告警，那个 `# noqa` 就是垃圾。`ruff` 会专门把这种「过期 noqa」标出来，提醒各位删掉。

这条规则非常实用——老项目迁移到 `ruff` 之后，原来给 `flake8` 加的 `# noqa` 大部分会过时，靠 `RUF100` 一扫一个准。


## 一个常见坑：和 mypy 的关系

很多童鞋会问：「`ruff` 能替代 `mypy` 吗？」

**不能。**

`ruff` 是 lint + formatter，做的是「代码风格、常见错误模式」检查。`mypy` 是**类型检查器**，做的是「这个变量传给那个函数，类型对不对」这种全局类型推导。两者是不同维度的工具，互补使用。

正确的姿势：

- 用 `ruff` 管风格、import、明显 bug、语法升级
- 用 `mypy` 或者 `pyright` 管类型

CI 上两个都跑：

```yaml
- run: ruff check .
- run: ruff format --check .
- run: mypy .
```

`ruff` 倒是有几条规则（前缀 `ANN`）会做粗浅的类型注解检查，比如「这个函数没有写 return 类型」。但是它**不会**真正去推导类型一致性，复杂的类型问题还是要靠 `mypy`。


## 一个进阶玩法：分目录用不同规则

大项目经常会有「核心代码严格管，脚本目录放松点」的需求。`ruff` 0.5 之后支持**子目录覆盖配置**，写法是 `[tool.ruff.lint.per-file-ignores]` 加 glob 模式。前面提过简单用法，下面看更复杂的：

```toml
[tool.ruff.lint.per-file-ignores]
# 测试文件允许 assert，允许长一点
"tests/**/*.py" = ["S101", "ANN", "D"]

# 一次性脚本，规则放最松
"scripts/*.py" = ["ALL"]

# 文档示例代码，允许 print
"docs/examples/*.py" = ["T20"]

# 迁移文件不动它
"**/migrations/*.py" = ["E", "F", "I", "UP", "B"]
```

`"ALL"` 是个特殊值，意思是「所有规则都忽略」。各位看到 `scripts/*.py` 那条，意思是脚本目录里 `ruff` 啥都不管，怎么写都行。

### 嵌套配置

如果你的项目是 monorepo，多个子项目共存，每个子项目想要自己的 `ruff` 配置，可以在子目录里放一个独立的 `pyproject.toml` 或 `ruff.toml`：

```
mono/
├── pyproject.toml          # 根配置
├── service-a/
│   ├── pyproject.toml      # service-a 自己的配置（可选）
│   └── ...
└── service-b/
    ├── ruff.toml           # service-b 自己的配置
    └── ...
```

`ruff` 在扫描每个文件时，会向上查找最近的配置文件。各子项目互不干扰。


## 一个进阶玩法：noqa 注释

有些时候你确实想让 `ruff` 闭嘴。比如某行代码里 `eval()` 用得有充分理由，但 `S307`（`flake8-bandit`）会告警。这时候可以加 `# noqa` 注释：

<!-- skip-ci -->
```python
result = eval(user_input)  # noqa: S307
```

`# noqa: S307` 表示「这行代码忽略 S307 这条规则」。多条规则用逗号隔开：

<!-- skip-ci -->
```python
result = eval(user_input)  # noqa: S307, S102
```

裸的 `# noqa`（不指定规则号）也行，但是不推荐——会把这行所有规则都忽略，相当于关大灯。指定规则号最精准。

各位写 `# noqa` 之前最好先想想：是这个规则不合理，还是代码本身就该改？大多数时候是后者。


## 几个易踩的坑

最后讲几个迁移到 `ruff` 之后老司机也会踩的坑，各位提前知道少走弯路。

### 坑 1：select 写错前缀，规则不生效

`select = ["E1"]` 不会启用 `pycodestyle E1xx` 这一组，**只会启用 E1 这一条**（如果有的话）。要启用 E1xx 整组，要写 `select = ["E1"]` 或者更宽的 `select = ["E"]`。

具体规则：

- `"E"`：启用所有 E 开头的规则（E1xx、E2xx、E5xx...）
- `"E1"`：启用所有 E1xx 开头的规则
- `"E101"`：只启用 E101 这一条

各位记不住的话，先用粗粒度 `["E", "F", "I"]` 这种，能跑就行。

### 坑 2：select 和 ignore 同时写

```toml
select = ["E"]
ignore = ["E501"]
```

这样配的意思是「启用 E 全组，但 E501 这条不要」。这是合法的，**ignore 优先级高**。各位经常会看到这种「开一组+排除一两条」的写法，是标准用法。

### 坑 3：ruff format 不读 [tool.ruff.lint] 的配置

`[tool.ruff.lint]` 管 lint，`[tool.ruff.format]` 管 format，**两者完全独立**。最常见的踩坑是：在 `[tool.ruff.lint]` 里设了 `quote-style = "double"`，结果 `ruff format` 还是按默认风格跑，因为 `quote-style` 应该写在 `[tool.ruff.format]` 里。

```toml
# 错误位置
[tool.ruff.lint]
quote-style = "double"  # 这里写了没用

# 正确位置
[tool.ruff.format]
quote-style = "double"
```

### 坑 4：preview 规则

`ruff` 还有一批正在开发的「preview」规则，默认不启用。要打开：

```toml
[tool.ruff.lint]
preview = true
```

或者命令行 `ruff check --preview`。preview 规则的好处是抢先用上新东西，坏处是规则号、行为可能在版本之间变。生产项目稳着来，**不建议默认开 preview**。

### 坑 5：忘了升级 pre-commit hook 版本

各位 `.pre-commit-config.yaml` 里的 `rev: v0.8.0` 是写死的，`ruff` 升了新版本不会自动同步。半年之后老 `ruff` 跑不出新规则，团队成员之间 `ruff` 版本不一致也会出问题。

建议：每个月或每个季度跑一次 `pre-commit autoupdate`，把 hook 版本统一升一下。CI 也跟着升。


## 小结

各位走完这一章，应该已经能：

1. 装 `ruff`：`uv add --dev ruff`
2. 跑 `ruff`：`ruff check --fix .` 和 `ruff format .`
3. 配 `ruff`：`pyproject.toml` 里写 `[tool.ruff.lint] select = ["E", "F", "I", "UP", "B", "SIM"]`
4. 接 `pre-commit`：写 `.pre-commit-config.yaml`，加 `ruff-pre-commit` 仓库
5. 接 `CI`：GitHub Actions 用 `astral-sh/ruff-action@v3`
6. 接编辑器：VS Code 装 `charliermarsh.ruff` 插件，配置保存时自动 format

这套工作流配好之后，新项目从零到「能自动检查、能自动修复、能 CI 兜底、能编辑器实时反馈」只需要十分钟。代码风格的事，交给 `ruff` 就行，各位省下来的精力可以用来写真正的业务代码。

下一章我们看 `pytest`——怎么写好 Python 项目的测试。`uv` 管依赖、`ruff` 管风格、`pytest` 管测试，这三件套配齐，2026 年的 Python 工程化就齐活了。



## 每次先处理一条看得懂的检查结果

代码检查工具输出一串规则号时，先选一条能解释的问题，不要急着把所有规则都打开。用综合练习的目录做一次只读检查：

```bash
ruff check .
ruff format --check .
```

前一条检查已启用规则，后一条检查格式是否需要调整。实际输出取决于版本、配置和当前文件内容，不要求和某张历史截图完全相同。

如果发现未使用的导入，先找到它，确认确实没用，再在自己的练习文件中改掉。把规则号、原因和改动记下来，重新运行检查。遇到不认识的规则，到 [Ruff 规则说明](https://docs.astral.sh/ruff/rules/) 查它检查什么、是否存在适用边界。

接着故意把统计函数的加法写错，再检查一次。你会发现，风格检查并不负责判断「总学习时间应该是多少」。运行测试仍然必要。反过来，测试通过也不能说明代码一定清楚易读，这两种检查各自有用。

先在自己的练习目录里操作。自动修改前看清工具报告的原因，修改后再运行测试，确认程序的结果没有改变。
