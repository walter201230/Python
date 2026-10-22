# 打包发布到 PyPI + typer：让全世界一行 pip install 用上你的工具

各位有没有过这样的瞬间——

水哥自己在本地写了一个小工具，比如「批量重命名截图文件」、「统计微信导出的聊天记录」、「自动给图片加水印」。脚本一两百行，跑起来挺顺手，自己天天用。然后某天一个朋友看见了，说：「这玩意儿挺好啊，能给我一份吗？」

水哥于是把 `tool.py` 用微信发过去。朋友收到之后，第一句话是——「这怎么用？」

「装一下 `pillow` 和 `httpx`。」

「好，装好了。」

「再装一下 `pyyaml`。」

「装好了。」

「跑一下 `python tool.py`。」

「报错了，说找不到 `requests`。」

「哦对，还要 `requests`。」

来回折腾五分钟，朋友放弃了。

各位看，这就是 Python 工具的「最后一公里」问题——代码自己能跑，可是给别人用就费劲。Node 圈一行 `npm install -g xxx`，Rust 圈一行 `cargo install xxx`，Go 圈一行 `go install xxx`，到了 Python 这边，难道就要「先装这个再装那个」吗？

当然不是。Python 也有自己的「全球应用商店」，叫 **PyPI**（Python Package Index）。把工具按照规范打包发上去，别人就能用一行 `pip install my-tool` 装上，再也不用各位手把手教了。

这一章咱们把整个流程从零跑通。学完之后，各位应该能：

1. 知道 PyPI 是什么、它跟 `pip` 是啥关系
2. 把自己的项目改造成「可发布」的标准结构
3. 用 `uv build` 一条命令把项目打成 `wheel` 和 `sdist`
4. 先在 TestPyPI 演练一遍，再正式发布到 PyPI
5. 用 `[project.scripts]` 把 Python 函数变成系统命令
6. 用 `typer` 写出比 `argparse` 优雅 10 倍的命令行工具
7. 把整套发布流程接进 GitHub Actions，打 tag 自动发版

后半段我们会用 `typer` 写一个 `todo-cli` 的命令行小工具，再把它发到 PyPI，让全世界都能 `pip install todo-cli` 装上。这个小项目把前后两块知识串起来，跑一遍就全懂了。

走起。



## PyPI 是个啥

各位平时一行 `pip install requests`，包是从哪儿下载的？答案是 PyPI。

**PyPI（Python Package Index）是 Python 官方维护的全球公共包仓库**，地址 `https://pypi.org`。截至 2026 年，上面挂着 60 多万个 Python 包，每个月被下载几百亿次。所有 Python 圈知名的包——`requests`、`numpy`、`flask`、`django`、`pandas`、`fastapi`——都住在 PyPI 上。

`pip install xxx` 这条命令的本质是——「从 PyPI 下载叫 `xxx` 的包，装到当前 Python 环境」。

PyPI 跟 GitHub 是啥关系？两者各管一摊：

- **GitHub** 是放源代码的地方，给开发者看
- **PyPI** 是放打好包的地方，给用户用 `pip` 装

一个项目通常两头都有——源码托管在 GitHub，发布版本上传到 PyPI。各位常用的 `requests`、`flask`，源码都在 GitHub，包都在 PyPI，两边版本号对得上。

PyPI 还有一个「兄弟站点」叫 **TestPyPI**，地址 `https://test.pypi.org`。它是 PyPI 的演练场——发版本之前先发到 TestPyPI 试一下，确认没问题再发正式 PyPI。两个网站各自独立，账号、密码、token 都不通用。

「为什么要有 TestPyPI？」因为 PyPI **正式版本一旦发布就不能修改、不能删除**。各位发版本的时候手抖了，把 `0.1.0` 发上去之后发现版本号写错了或者打包漏文件，没法撤回，只能再发一个 `0.1.1`，那个错版本会永远挂在 PyPI 上当历史档案。所以发正式 PyPI 之前先在 TestPyPI 演练一遍，是发版本的好习惯。

接下来我们就一步步搭一个能发到 PyPI 的项目。



## 先把项目结构搭对

各位写 Python 项目的时候，最常见的目录长这样：

```
my-tool/
├── my_tool.py
└── README.md
```

或者稍微讲究一点的：

```
my-tool/
├── my_tool/
│   ├── __init__.py
│   └── main.py
└── README.md
```

这种结构本地跑没问题，可一旦要打包发布，就会暴露一个隐藏的坑——**当前目录会被 Python 自动加进 `sys.path`**。结果跑测试的时候，导入的是「项目根目录的源码」而不是「装到环境里的包」，问题就被遮住了。

社区现在推荐的写法叫 **src layout**，长这样：

```
my-tool/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_tool/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

注意中间多了一层 `src/` 目录。这个 `src/` 不是装饰，它的作用是——**强行让源码不在项目根目录**。这样你就必须把包装到环境里才能 import，避免了上面说的坑。

「这样写麻烦吗？」一点都不麻烦。配合 `uv` 和 `pyproject.toml`，工具会自动识别 `src/` 布局，啥都不用配。

各位现在用 `uv` 起一个新项目，看看默认结构：

```bash
uv init --package my-tool
cd my-tool
ls -R
```

输出大概长这样：

```
.
├── README.md
├── pyproject.toml
└── src
    └── my_tool
        └── __init__.py
```

`uv init --package` 这一行就帮各位把 `src layout` 的骨架搭好了。注意这里加了 `--package`——不加这个参数，`uv init` 默认搭的是「应用」结构（不打包），加上才是「库/工具」结构（要打包发布）。

打开 `pyproject.toml` 看看 `uv` 给生成了什么：

```toml
[project]
name = "my-tool"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
my-tool = "my_tool:main"
```

各位看，骨架已经齐了——`[project]` 段写元数据、`[build-system]` 段写打包后端、`[project.scripts]` 段写命令行入口。下一步咱们逐个字段把它填充完整。



## pyproject.toml 必填字段拆解

要发到 PyPI，`[project]` 段里有几个字段是绕不过的——名字、版本、描述、Python 版本要求、依赖。下面挨个讲。

### name：包的全网唯一名字

`name` 就是发到 PyPI 之后，别人用 `pip install xxx` 时填的那个 `xxx`。**它在 PyPI 全网唯一**，跟域名一样，先到先得。各位起名前最好先到 `https://pypi.org/project/xxx/` 看一下有没有重名。

命名规则——只允许字母、数字、`-`、`_`、`.`，不区分大小写，不能以数字开头。社区习惯用小写加连字符，比如 `my-tool`、`todo-cli`、`http-prompt`。

注意一个细节：**包名（`name`）和导入名（`import xxx` 的 `xxx`）不一定一样**。比如 `pip install scikit-learn`，但 `import sklearn`。`pip install Pillow`，但 `import PIL`。这是因为：

- `name` 是 PyPI 上的项目名，可以带连字符
- 导入名是 Python 模块名，必须是合法 Python 标识符，不能带连字符

水哥的建议是——为了不让用户搞晕，**两个名字尽量保持一致**。比如包名叫 `my-tool`，导入名就叫 `my_tool`（连字符变下划线，Python 圈通用习惯）。

### version：版本号

`version` 是这个发布版本的版本号，写成字符串，比如 `"0.1.0"`、`"1.2.3"`、`"2.0.0a1"`。

社区强烈推荐用 **语义化版本（SemVer）**，三段数字 `主.次.补丁`：

- **主版本号**：不向后兼容的大改动（删函数、改签名）
- **次版本号**：向后兼容的新功能
- **补丁号**：向后兼容的 bug 修复

新项目从 `0.1.0` 起步，到了 1.0 之前都算「不稳定」，API 可以随便改。1.0 之后再改 API 就要小心了。

PyPI 还有一条铁规——**同一个版本号只能上传一次**。各位发了 `0.1.0` 之后想撤回重新发，对不起，办不到。必须改成 `0.1.1` 或者 `0.1.0.post1` 重新发。

### description：一句话描述

`description` 是一句话简介，会显示在 PyPI 页面顶部，搜索结果里也会带。写得稍微像样一点，别 `"Add your description here"` 这种默认值就发上去——上线之后看着尴尬。

```toml
description = "两点水的小工具，批量给图片加水印"
```

### readme：长描述

`readme` 是项目的长描述，发到 PyPI 之后会显示在项目页面正文。指向一个 Markdown 文件即可：

```toml
readme = "README.md"
```

`uv init` 已经帮各位生成了一个空的 `README.md`，把内容补上。建议至少包含——一段简介、安装命令、最小用法示例。

### authors / maintainers：作者

`authors` 写作者列表，每个作者是一个对象，至少写名字，邮箱可选：

```toml
authors = [
    { name = "两点水", email = "liangdianshui@example.com" },
]
```

### requires-python：Python 版本要求

`requires-python` 限定这个包支持哪些 Python 版本：

```toml
requires-python = ">=3.10"
```

各位不要写 `>=3.0`，那样老到不能再老的 Python 都会尝试装，结果一堆兼容问题。2026 年的合理选择是 `>=3.10` 或 `>=3.11`，3.9 已经在 EOL 边缘。

### dependencies：依赖列表

`dependencies` 是这个包运行时需要的其他包：

```toml
dependencies = [
    "httpx>=0.27",
    "typer>=0.12",
]
```

每条遵守 PEP 508 语法——`包名` + 版本约束。常用的版本约束符——

- `>=0.27`：大于等于 0.27 即可，最常用
- `~=0.27`：兼容版本，`>=0.27, <0.28`
- `==0.27.1`：固定版本，几乎不用
- `>=0.27, <1.0`：限定范围

「写不写版本号？」**强烈建议写最低版本**，比如 `httpx>=0.27`。这样别人装的时候，至少能保证 `httpx` 不会因为太老而缺函数。上限不要随便写，写死会增加用户的依赖冲突概率。

完整的最小可发布 `pyproject.toml` 大概长这样：

```toml
[project]
name = "my-tool"
version = "0.1.0"
description = "两点水的小工具"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    { name = "两点水", email = "liangdianshui@example.com" },
]
dependencies = [
    "httpx>=0.27",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

下一节讲 `[build-system]` 是个啥。



## build-backend：谁来负责打包

各位刚才的 `pyproject.toml` 末尾有这么一段：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

这两行在干啥？要解释清楚，得先理清 Python 打包的角色分工。

Python 打包过程里有两个角色——**前端**和**后端**：

- **前端（frontend）** 是用户敲的命令，比如 `pip`、`uv`、`build`
- **后端（backend）** 是真正干活的库，把源码变成 `wheel` 和 `sdist`

PEP 517 这个标准把两者拆开了，前端只负责调用，后端可以自由替换。`[build-system]` 段就是告诉前端：「我用的是哪个后端」。

社区目前主流的后端有三个——

- **`hatchling`**：来自 `Hatch` 项目，配置简单、扩展性强，**新项目首选**
- **`setuptools`**：上古时代留下来的老牌后端，几乎所有老项目都在用
- **`poetry-core`**：Poetry 项目自带的后端，跟 Poetry 工具一起用

各位还可能在野外见到 `flit-core`、`pdm-backend`、`maturin`（Rust 写的扩展用），都是同一个生态位的不同选择。

为啥推荐 `hatchling`？三个原因——

1. **配置简单**。`uv init --package` 默认就是它，啥都不用改
2. **现代化**。原生支持 `src layout`、PEP 621 元数据，没有历史包袱
3. **生态有官方背书**。`hatch` 是 PyPA（Python Packaging Authority）旗下的项目

「`setuptools` 不是更普及吗？」普及没错，但是配置又多又乱，新项目没必要自找麻烦。除非你需要 C 扩展，或者要兼容 10 年前的老代码，否则 `hatchling` 闭着眼睛选就行。

各位 `pyproject.toml` 这一段保持默认就好：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

`requires` 列出「构建这个项目时需要装哪些包」。这里的依赖跟 `[project].dependencies` 不一样——后者是「跑这个项目要的包」，前者是「打包这个项目要的包」。

下一节咱们试着把项目打包出来。



## 本地构建：uv build 一条命令出炉

各位写完代码之后，怎么把项目打成可发布的格式？一条命令——

```bash
uv build
```

跑一下，输出大概是：

```
Building source distribution...
Building wheel from source distribution...
Successfully built dist/my_tool-0.1.0.tar.gz
Successfully built dist/my_tool-0.1.0-py3-none-any.whl
```

打开 `dist/` 目录看看：

```
dist/
├── my_tool-0.1.0-py3-none-any.whl
└── my_tool-0.1.0.tar.gz
```

两个文件分别是啥？

- **`.whl` 文件（wheel）**：预编译好的二进制包。用户 `pip install` 时会优先选这个，因为不用编译，秒装
- **`.tar.gz` 文件（sdist，source distribution）**：源码包。包含整个项目源码，给那些环境特殊、需要从源码编译的用户用

文件名里有个规则——`包名-版本-Python 版本-ABI-平台`：

- `py3`：兼容所有 Python 3
- `none`：不依赖特定的 ABI
- `any`：跨平台

要是你的包包含 C 扩展，`whl` 名字就会变成 `my_tool-0.1.0-cp311-cp311-linux_x86_64.whl`，限定 CPython 3.11、Linux x86_64 上能用。每个平台都要单独打一个 `whl`。

纯 Python 项目就一个 `py3-none-any.whl`，全平台通吃，最省事。

「`uv` 没装怎么办？」用官方的 `build` 工具也行：

```bash
pip install build
python -m build
```

效果一模一样。各位看自己习惯，本章后面统一用 `uv`。

构建成功之后，**一定要先在本地装一下试试**：

```bash
uv pip install dist/my_tool-0.1.0-py3-none-any.whl
```

或者：

```bash
pip install dist/my_tool-0.1.0-py3-none-any.whl
```

装完之后跑跑你的工具，确认能用。这一步是发版本前的最后一道防线，发到 PyPI 之前如果发现问题，还能改；发上去就晚了。



## 注册 TestPyPI 账号

包打好了，下一步——发上去。先发 TestPyPI 演练，再发正式 PyPI。

TestPyPI 注册流程——

1. 打开 `https://test.pypi.org/account/register/`
2. 用邮箱注册账号，验证邮箱
3. 登录之后，进 `Account settings`
4. 开启 **两步验证（2FA）**，TestPyPI 现在强制要求 2FA。可以用 Authy、Google Authenticator、1Password 这类 TOTP App
5. 进 `API tokens` 页面，创建一个 token，scope 选 `Entire account`（第一次发包没办法限定到具体项目，因为项目还不存在）
6. 把生成的 token 复制下来，**只能看一次，关掉页面就没了**

TestPyPI 的 token 长这样：

```
pypi-AgEIcHlwaS5vcmcCJ...（一长串 base64）
```

把这个 token 保存在密码管理器里。

正式 PyPI 的注册流程一样——`https://pypi.org/account/register/`，开 2FA，建 token，存好。注意 PyPI 跟 TestPyPI 是两个独立网站，账号、token 都是分开的。

「token 怎么用？」下一节就用上了。



## 上传到 TestPyPI 演练

TestPyPI 的发布命令——

```bash
uv publish --publish-url https://test.pypi.org/legacy/ \
    --token pypi-AgEIcHlwaS5vcmcCJ...
```

或者用环境变量更安全：

```bash
export UV_PUBLISH_TOKEN=pypi-AgEIcHlwaS5vcmcCJ...
uv publish --publish-url https://test.pypi.org/legacy/
```

跑成功之后，输出大概是：

```
Uploading my_tool-0.1.0-py3-none-any.whl
Uploading my_tool-0.1.0.tar.gz
Published https://test.pypi.org/project/my-tool/0.1.0/
```

打开链接看看，自己的小工具已经躺在 TestPyPI 上了，标题、描述、版本号、README、依赖列表全都有。

下一步——**用 TestPyPI 装一下，确认能用**：

```bash
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    my-tool
```

注意这里两个 `index-url` 参数——

- `--index-url https://test.pypi.org/simple/`：从 TestPyPI 找你刚发的包
- `--extra-index-url https://pypi.org/simple/`：从正式 PyPI 找依赖（因为你的依赖比如 `httpx` 是发在正式 PyPI 上的）

不加第二个参数，TestPyPI 上的依赖会装不全（TestPyPI 只有你刚上传的，没有 `httpx`）。这是新手最常踩的坑，记一下。

装完跑你的工具，能跑通，恭喜各位，发包流程已经掌握了。



## 正式上传到 PyPI

TestPyPI 演练成功之后，正式发 PyPI 就一条命令——

```bash
export UV_PUBLISH_TOKEN=pypi-正式的-token-...
uv publish
```

`uv publish` 默认就是发到 `https://upload.pypi.org/legacy/`，也就是正式 PyPI。

发完之后，打开 `https://pypi.org/project/my-tool/`，自己的项目就在 PyPI 上了。任何人现在都能：

```bash
pip install my-tool
```

把你的工具装到自己的环境里。水哥写到这里都觉得有点小激动——这意味着你的代码已经在全球公共仓库上了，谁都能用上。

「我发包之后想下架怎么办？」PyPI 提供了一个「yank」机制——版本号会保留，但默认不再被新装机会找到。注意只是「藏起来」不是「删除」，已经装上的用户还能继续用。完全删除一个版本是不允许的，避免破坏依赖链。



## 版本号管理：手动 vs 自动

各位发完 `0.1.0`，过了一段时间想发 `0.1.1`。怎么改版本号？

**手动法**——打开 `pyproject.toml`，把 `version = "0.1.0"` 改成 `version = "0.1.1"`，然后重新 `uv build` + `uv publish`。简单直接。

但是手动法有个问题——`pyproject.toml` 和 git tag 容易对不上。比如 `pyproject.toml` 写 `0.1.1`，git tag 是 `v0.2.0`，到底哪个才算正确？这种漂移积累几个版本就乱套。

**自动法**——用 `hatch-vcs`，从 git tag 自动算版本号。改一下 `pyproject.toml`：

```toml
[project]
name = "my-tool"
dynamic = ["version"]
description = "两点水的小工具"
# ...

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"
```

注意三处变化——

1. `version = "0.1.0"` 改成 `dynamic = ["version"]`，告诉 `hatchling`「版本号不是写死的，动态算」
2. `[build-system].requires` 加上 `hatch-vcs`，引入算版本号的插件
3. 新增 `[tool.hatch.version]` 段，告诉 `hatch-vcs`「从 git 读」

之后流程变成——

```bash
git tag v0.1.1
git push --tags
uv build
uv publish
```

`uv build` 时，`hatch-vcs` 会读 git 最新的 tag `v0.1.1`，自动得出版本号 `0.1.1`，包名就是 `my_tool-0.1.1-py3-none-any.whl`。

要是你打 tag 之后又改了代码，`hatch-vcs` 还会自动加上一个 `dev` 后缀，版本号变成 `0.1.2.dev3+gabc1234`，明显告诉你「这是个开发中的版本」。

水哥的建议是——**新项目用自动法**。一开始用手动法没问题，但是到了第三、第四个版本，开发者多起来的时候，自动法能省掉很多对帐的功夫。



## README 和 LICENSE：最低限度的「正经感」

各位发到 PyPI 的项目，**必须有 README.md 和 LICENSE 文件**，这是基本的行业礼仪。

### README.md

`README.md` 在 PyPI 项目页面会被渲染成正文，是用户第一眼看到的东西。建议至少包含——

```markdown
# my-tool

两点水的小工具，批量给图片加水印。

## 安装

```bash
pip install my-tool
```

## 用法

```bash
my-tool ./photos --watermark "© 两点水"
```

## License

MIT
```

简介、安装、用法、License，四段够用了。讲究一点的项目还会加上「特性」、「示例」、「FAQ」、「贡献指南」。

### LICENSE

License 是法律文件，告诉用户「我允许你怎么用我的代码」。各位写开源项目，不写 License 等于「保留所有权利」，反而是最严的——别人不能拿来用，因为没拿到许可。

常用的 License 三选一——

- **MIT**：最宽松，「你随便用，别告我，写一句版权声明就行」
- **Apache 2.0**：跟 MIT 类似，加了一条「专利授权」条款，对企业更友好
- **GPL v3**：传染性 License，「你用了我的代码，你的代码也得开源」

社区惯例——工具/库类项目用 MIT 或 Apache 2.0，应用类项目自己拿主意。水哥的小工具一律 MIT，省事。

`pyproject.toml` 里也声明一下：

```toml
[project]
license = { file = "LICENSE" }
```

或者写 SPDX 标识（PEP 639，2024 年正式落地）：

```toml
[project]
license = "MIT"
```

后者更现代，但是有些老工具还不认，看你的容忍度。



## CI 自动发包：打 tag 就发版

每次发包都手动 `uv build` + `uv publish`，跑两三次就嫌烦。最理想的状态是——**打个 git tag，CI 自动构建并发到 PyPI**。

GitHub Actions 加一段 workflow 就能做到。在项目里建一个文件 `.github/workflows/release.yml`：

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: astral-sh/setup-uv@v3

      - run: uv build

      - uses: pypa/gh-action-pypi-publish@release/v1
```

这段配置干了什么——

1. **触发条件**：`push` 一个以 `v` 开头的 tag（比如 `v0.1.1`）就跑
2. **`permissions: id-token: write`**：给 workflow 申请 OpenID Connect 权限，下面的「可信发布」要用
3. **构建**：用 `uv build` 打包
4. **发布**：用 `pypa/gh-action-pypi-publish` 上传到 PyPI

最神奇的是——**这套流程不需要写 PyPI token**。靠的是「**可信发布（Trusted Publishers）**」机制，2023 年 PyPI 推出，2024 年成为推荐做法。

可信发布的原理是——PyPI 直接信任 GitHub Actions 的 OIDC 身份。你在 PyPI 项目设置里关联「这个 GitHub 仓库的这个 workflow 文件」之后，CI 跑起来 PyPI 就认识，不用 token 就能上传。

配置步骤——

1. 登录 PyPI，进项目页面 → `Settings` → `Publishing`
2. 添加一个「Trusted Publisher」，填 `Owner`（你的 GitHub 用户名/组织）、`Repository name`（仓库名）、`Workflow name`（`release.yml`）、`Environment`（可选）
3. 推一个 tag 试试

打 tag 的命令——

```bash
git tag v0.1.1
git push origin v0.1.1
```

GitHub Actions 跑起来，几分钟之后包就在 PyPI 上了。

「比起 token 有啥好处？」三点——

1. **不用管 token 过期**。token 默认一年过期，到点就要重建
2. **不用怕 token 泄露**。OIDC 凭证只在 workflow 跑的那一瞬间存在，没法拷出来
3. **配置在 PyPI 一边**。换 token 不用改 secrets，权限管理更清晰

水哥强烈推荐 2026 年的新项目一上来就用可信发布，比 token 干净太多。

到这里，发包到 PyPI 这部分讲完了。下一节我们换个话题——**`typer`**，写 CLI 工具的利器。



## CLI 的痛：argparse 太啰嗦

各位写过命令行工具吗？Python 标准库自带一个 `argparse`，能用，但是写起来啰嗦得要命。看一段：

<!-- skip-ci -->
```python
import argparse

parser = argparse.ArgumentParser(description="给图片加水印")
parser.add_argument("input", type=str, help="输入图片路径")
parser.add_argument("--watermark", type=str, default="© 两点水", help="水印文本")
parser.add_argument("--opacity", type=float, default=0.5, help="不透明度")
parser.add_argument("--verbose", action="store_true", help="显示详细信息")
args = parser.parse_args()

print(f"输入：{args.input}")
print(f"水印：{args.watermark}")
print(f"不透明度：{args.opacity}")
print(f"详细：{args.verbose}")
```

这段代码 9 行，但实际有用的逻辑只有 4 个变量。为啥这么啰嗦？因为 `argparse` 是 2009 年写的，那时候 Python 还没有类型注解。所有参数都得手动 `add_argument` 一遍，类型、默认值、帮助文本各填一遍，函数签名跟参数声明分两处，改起来还容易漏。

更糟的是子命令——比如 `git commit`、`git push` 这种「主命令 + 子命令」结构，`argparse` 写起来嵌套一堆 `subparsers`，看一眼就头疼。

到了 2026 年，各位有没有更好的选择？

有，叫 **`typer`**。它是 `FastAPI` 作者 Tiangolo 写的，思路跟 `FastAPI` 一脉相承——**用类型注解直接当参数声明**。同样的功能，`typer` 写出来是这样：

<!-- skip-ci -->
```python
import typer

app = typer.Typer()


@app.command()
def watermark(
    input: str,
    watermark: str = "© 两点水",
    opacity: float = 0.5,
    verbose: bool = False,
):
    print(f"输入：{input}")
    print(f"水印：{watermark}")
    print(f"不透明度：{opacity}")
    print(f"详细：{verbose}")


if __name__ == "__main__":
    app()
```

各位看看——参数直接写在函数签名里，类型注解就是参数类型，默认值就是命令行默认值，帮助文本能从 docstring 自动提取。逻辑跟 `argparse` 等价，行数少了一半，可读性高了 10 倍。

接下来咱们把 `typer` 从最简单的开始一步步讲。



## 第一个 typer

各位先装一下 `typer`：

```bash
uv add typer
```

或者：

```bash
pip install typer
```

写一个最简单的脚本 `hello.py`：

<!-- skip-ci -->
```python
import typer


def hello(name: str):
    print(f"Hi {name}")


if __name__ == "__main__":
    typer.run(hello)
```

跑一下：

```bash
python hello.py 两点水
```

输出：

```
Hi 两点水
```

各位再试试不带参数：

```bash
python hello.py
```

输出：

```
Usage: hello.py [OPTIONS] NAME
Try 'hello.py --help' for help.

Error: Missing argument 'NAME'.
```

`typer` 自动帮你做了——

- 解析命令行参数
- 类型转换（`name` 是 `str`，从命令行字符串直接拿）
- 缺参数报错
- 提示有 `--help` 命令

试试 `--help`：

```bash
python hello.py --help
```

输出：

```
Usage: hello.py [OPTIONS] NAME

Arguments:
  NAME  [required]

Options:
  --help  Show this message and exit.
```

帮助文本是 `typer` 自动生成的。各位有没有发现——你压根没写 `parser.add_argument`、没写 `--help`、没写 `Usage`，全是 `typer` 自动整出来的。这就是「**类型注解即文档**」的威力。

`typer.run(hello)` 这一行做的事情是「把 `hello` 函数变成一个命令行入口」。它适合只有一个命令的小工具。如果各位的工具有多个命令（比如 `add`、`list`、`done`），就需要下一节讲的 `Typer` app。



## 多命令 app

各位写过 `git` 没？`git commit`、`git push`、`git pull`，一个主命令带一堆子命令。这种结构在 `typer` 里叫 **多命令 app**：

<!-- skip-ci -->
```python
import typer

app = typer.Typer()


@app.command()
def add(item: str):
    """添加一项任务。"""
    print(f"添加：{item}")


@app.command()
def list():
    """列出所有任务。"""
    print("列出全部任务...")


@app.command()
def done(index: int):
    """标记任务完成。"""
    print(f"完成第 {index} 项")


if __name__ == "__main__":
    app()
```

各位看，三个步骤——

1. `app = typer.Typer()`：创建一个 app 实例
2. 用 `@app.command()` 装饰每个命令对应的函数
3. `app()` 启动

跑一下：

```bash
python todo.py add "学 typer"
python todo.py list
python todo.py done 1
```

输出：

```
添加：学 typer
列出全部任务...
完成第 1 项
```

每个 `@app.command()` 装饰的函数都会变成一个子命令，函数名就是子命令名。用户输入 `add` 时跑 `add` 函数，输入 `list` 时跑 `list` 函数。

各位试试 `--help`：

```bash
python todo.py --help
```

输出：

```
Usage: todo.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell.
  --help                Show this message and exit.

Commands:
  add   添加一项任务。
  done  标记任务完成。
  list  列出所有任务。
```

注意每个命令旁边的描述——它来自每个函数的 docstring。`typer` 直接读 docstring 生成命令帮助，docstring 写得清楚一点，CLI 文档就完整了。

子命令的帮助也有：

```bash
python todo.py add --help
```

输出：

```
Usage: todo.py add [OPTIONS] ITEM

  添加一项任务。

Arguments:
  ITEM  [required]
```

`add` 子命令的描述、参数列表全自动生成。



## 类型注解 = CLI 参数

`typer` 最神奇的地方在于——**函数参数的类型注解，就是 CLI 参数的类型**。各位写什么类型，CLI 自动转什么类型，不用写一行类型转换代码。

支持的类型——

<!-- skip-ci -->
```python
import typer
from pathlib import Path
from enum import Enum


class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"


def cmd(
    text: str,
    count: int,
    ratio: float,
    enabled: bool,
    file: Path,
    color: Color,
):
    print(f"text={text!r}")
    print(f"count={count} (类型 {type(count).__name__})")
    print(f"ratio={ratio} (类型 {type(ratio).__name__})")
    print(f"enabled={enabled}")
    print(f"file={file} (类型 {type(file).__name__})")
    print(f"color={color}")
```

跑这个命令——

```bash
python cmd.py "hi" 10 1.5 ./README.md red
```

输出：

```
text='hi'
count=10 (类型 int)
ratio=1.5 (类型 float)
enabled=False
file=README.md (类型 PosixPath)
color=Color.red
```

注意几个细节——

- `int` 类型，命令行的 `"10"` 自动变成整数
- `float` 类型，命令行的 `"1.5"` 自动变成浮点数
- `Path` 类型，自动包装成 `pathlib.Path` 对象
- `Enum` 类型，限定值只能是 `red`/`green`/`blue`，输入别的值直接报错

要是各位输错类型试试：

```bash
python cmd.py "hi" abc 1.5 ./README.md red
```

`typer` 直接拒绝：

```
Usage: cmd.py [OPTIONS] TEXT COUNT RATIO FILE COLOR
Try 'cmd.py --help' for help.

Error: Invalid value for 'COUNT': 'abc' is not a valid integer.
```

「类型即验证」——你写 `int`，`typer` 就只接受能转成 `int` 的值，转不了的连函数都进不去。这跟用 `argparse` 还得自己 `try except` 一对比，简直舒服。



## Optional 参数：默认值的魔法

各位回到刚才的例子，参数 `text: str` 是「必填」还是「可选」？是必填，因为没写默认值。

要是想让它变成可选，加一个默认值即可：

```python
def hello(name: str = "World"):
    print(f"Hi {name}")
```

这时候 `typer` 会把它从「位置参数」变成「**选项参数**」，命令行用法变成：

```bash
python hello.py            # 输出 Hi World
python hello.py --name 两点水  # 输出 Hi 两点水
```

注意——

- **没有默认值的参数 = 位置参数（Argument）**，必填，直接跟在命令后面
- **有默认值的参数 = 选项参数（Option）**，可选，要带 `--name` 前缀

这跟 Python 函数的「位置参数 vs 关键字参数」逻辑一致。各位写 Python 函数有没有默认值，决定了 CLI 是位置参数还是选项参数。

短选项也很容易加，用 `typer.Option`：

<!-- skip-ci -->
```python
import typer


def hello(
    name: str = typer.Option("World", "--name", "-n", help="谁的名字"),
):
    print(f"Hi {name}")


if __name__ == "__main__":
    typer.run(hello)
```

这时候——

```bash
python hello.py -n 两点水
python hello.py --name 两点水
```

两种写法等价。`typer.Option` 第一个参数是默认值，后面是各种命令行别名，最后 `help` 是帮助文本。



## 必选参数 vs 可选参数：一句话区分

各位老在「位置参数」和「选项参数」之间纠结，水哥给一个一句话原则——

- **「这个值非给不可」→ 位置参数**。比如 `cp 源 目标`，没源、没目标，命令没法跑
- **「这个值可以省略，省略时有个默认行为」→ 选项参数**。比如 `ls --all`，不加也能跑

写到 `typer` 函数签名里——

<!-- skip-ci -->
```python
def watermark(
    input: Path,                 # 位置参数：必填
    output: Path,                # 位置参数：必填
    text: str = "© 两点水",       # 选项参数：可选，默认水印
    opacity: float = 0.5,        # 选项参数：可选，默认 0.5
    verbose: bool = False,       # 选项参数：可选，默认 False
):
    ...
```

CLI 用法：

```bash
my-tool input.jpg output.jpg
my-tool input.jpg output.jpg --text "两点水版权所有" --opacity 0.8 --verbose
```

各位写 CLI 工具的时候，**位置参数一般 1-3 个**，多了用户记不住顺序。3 个以上的参数全用选项参数，写出来反而清楚。



## 交互式输入：prompt 和 confirm

各位写 CLI 工具的时候，常常有这种场景——「这个参数用户没传，我想问一下他」。比如删除文件之前问「确定吗？」、初始化项目时问「项目名叫啥？」。

老办法是用 `input()`。`typer` 提供了更好用的两件武器——`typer.prompt` 和 `typer.confirm`。

先看 `prompt`，它问用户一个问题然后拿到答案：

<!-- skip-ci -->
```python
import typer


def init():
    name = typer.prompt("项目名叫啥")
    author = typer.prompt("作者是谁", default="两点水")
    print(f"创建项目 {name}，作者 {author}")


if __name__ == "__main__":
    typer.run(init)
```

跑起来——

```
项目名叫啥: my-tool
作者是谁 [两点水]:
创建项目 my-tool，作者 两点水
```

`default` 参数给一个默认值，用户直接回车就用默认值。比 `input()` 漂亮一截。

`confirm` 是「问 yes/no」：

<!-- skip-ci -->
```python
import typer


def delete(path: str):
    sure = typer.confirm(f"确定要删除 {path} 吗")
    if not sure:
        print("取消")
        raise typer.Abort()
    print(f"已删除 {path}")


if __name__ == "__main__":
    typer.run(delete)
```

跑起来——

```
$ python del.py /tmp/foo
确定要删除 /tmp/foo 吗 [y/N]: y
已删除 /tmp/foo
```

`confirm` 默认是「不」（用户直接回车 = no），加 `default=True` 改成默认「是」。

`typer.Abort()` 是另一个特殊异常——「用户主动放弃」，CLI 会用一个统一的退出码（默认 1）退出，比 `typer.Exit()` 语义更清楚。



## 错误退出：typer.Exit 和 typer.Abort

各位写 CLI 工具，有些情况下要让命令以「失败」退出——文件不存在、网络挂了、用户输错值。Linux 圈的惯例是「退出码 0 = 成功，非 0 = 失败」，shell 脚本会根据这个判断要不要继续。

`typer` 提供了两种退出方式——

<!-- skip-ci -->
```python
import typer


def deploy(env: str):
    if env not in ("dev", "staging", "prod"):
        print(f"不认识的环境：{env}")
        raise typer.Exit(code=2)
    print(f"开始部署到 {env}")
```

`typer.Exit(code=N)` 直接让 CLI 退出，退出码是 N。约定俗成——

- `0`：成功
- `1`：通用失败
- `2`：用户输错参数

各位也别瞎用 `sys.exit(N)`——它绕过了 `typer` 的退出钩子，写日志、清理资源都来不及。统一用 `typer.Exit`。

另一个是 `typer.Abort()`，「用户中止」的语义。比如上面 `confirm` 用户答了 no，就 `raise typer.Abort()`。它本质上等价于 `typer.Exit(code=1)`，但语义更清楚。



## 彩色输出：echo 和 secho

各位看 `git status` 输出有没有发现——modified 文件是红的、staged 文件是绿的、提示文本是黄的。命令行工具加点颜色，可读性立刻提升。

`typer` 内置了简单的彩色输出，叫 `typer.echo` 和 `typer.secho`：

<!-- skip-ci -->
```python
import typer


def status():
    typer.echo("普通文本，跟 print 一样")
    typer.secho("成功！", fg=typer.colors.GREEN)
    typer.secho("警告！", fg=typer.colors.YELLOW)
    typer.secho("错误！", fg=typer.colors.RED, bold=True)


if __name__ == "__main__":
    typer.run(status)
```

跑起来在支持彩色的终端里——「成功！」是绿色、「警告！」是黄色、「错误！」是红色加粗。在不支持彩色的环境（比如重定向到文件），`typer` 自动去掉色码，输出还是干净的。

可选颜色——`BLACK`、`RED`、`GREEN`、`YELLOW`、`BLUE`、`MAGENTA`、`CYAN`、`WHITE`，外加 `bold=True`、`underline=True` 这些样式。

「为啥不用 `print`？」`print` 没办法自动判断终端是否支持彩色。重定向到文件的时候，色码会变成乱七八糟的 `\x1b[32m` 之类的字符，污染输出。用 `typer.secho` 自动处理这个细节。

要更花哨的输出（表格、进度条、Markdown 渲染），`typer` 可以无缝接 `rich`——`pip install "typer[all]"` 之后，它默认就用 `rich` 当后端。



## 子命令嵌套：app.add_typer

各位写大型 CLI 工具，命令多了之后想分组管理——比如 `git remote add`、`git remote rm`、`git stash push`、`git stash pop` 这种「子命令的子命令」。

`typer` 支持子 app 嵌套：

<!-- skip-ci -->
```python
import typer

app = typer.Typer()
remote_app = typer.Typer()
stash_app = typer.Typer()

app.add_typer(remote_app, name="remote", help="管理远程仓库")
app.add_typer(stash_app, name="stash", help="管理暂存区")


@remote_app.command("add")
def remote_add(name: str, url: str):
    print(f"添加远程：{name} -> {url}")


@remote_app.command("rm")
def remote_rm(name: str):
    print(f"删除远程：{name}")


@stash_app.command("push")
def stash_push():
    print("暂存当前修改")


@stash_app.command("pop")
def stash_pop():
    print("恢复最近一次暂存")


if __name__ == "__main__":
    app()
```

跑起来——

```bash
python git.py remote add origin git@github.com:walter/python.git
python git.py remote rm origin
python git.py stash push
python git.py stash pop
```

每个子 app 又可以再嵌套子 app，理论上无限层。但是各位别真嵌套三层以上，用户记不住。两层够用。



## 打包成系统命令：[project.scripts]

各位现在的 `typer` 工具，跑起来是 `python todo.py add ...`，每次都要加 `python`，不像 `git` 那样直接敲。怎么变成全局命令？

答案是 `pyproject.toml` 里的 `[project.scripts]` 段：

```toml
[project.scripts]
todo-cli = "my_tool.cli:app"
```

格式是 `命令名 = "包路径:函数名"`。这一行的意思是——

- 装这个包之后，命令行多一个叫 `todo-cli` 的命令
- 跑 `todo-cli` 时，等于跑 `my_tool/cli.py` 里的 `app` 函数

`typer.Typer()` 实例本身就是可调用的，直接当 `app` 用。

各位重装一下包：

```bash
uv pip install -e .
```

然后试试：

```bash
todo-cli --help
```

直接出帮助。再试：

```bash
todo-cli add "学 typer"
todo-cli list
```

跟之前 `python todo.py add ...` 一模一样，但是命令短了一截，体验立刻像样起来。

「`uv pip install -e .` 是啥意思？」`-e` 是 editable 模式，把包以「软链接」的方式装进去——你改源码，命令立刻生效，不用重装。开发期间一定加 `-e`，省去无数次重装。

到这里，发包 + CLI 的所有零件都齐了。下一节用一个完整的小项目把所有东西串起来。



## 实战：todo-cli 从零到发布

各位跟着水哥写一个完整的 `todo-cli` 工具，最后发到 PyPI（演练版本发到 TestPyPI）。这个工具支持三个命令——

- `todo-cli add "买菜"`：添加一项 todo
- `todo-cli list`：列出所有 todo
- `todo-cli done 1`：标记第 1 项完成

数据存在用户家目录下的 `~/.todo-cli.json`，最简单的本地存储。

### 第一步：起项目骨架

```bash
uv init --package todo-cli
cd todo-cli
uv add typer
```

`uv` 自动生成 `src/todo_cli/__init__.py`。我们再加一个文件 `src/todo_cli/cli.py`。

### 第二步：实现核心逻辑

<!-- skip-ci -->
```python
import json
from pathlib import Path

import typer

app = typer.Typer(help="两点水的小型 todo 工具")

DATA_FILE = Path.home() / ".todo-cli.json"


def load_todos() -> list[dict]:
    """读 todo 列表，文件不存在返回空 list。"""
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_todos(todos: list[dict]) -> None:
    """把 todo 列表写回文件。"""
    DATA_FILE.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@app.command()
def add(item: str):
    """添加一项 todo。"""
    todos = load_todos()
    todos.append({"item": item, "done": False})
    save_todos(todos)
    print(f"已添加：{item}")


@app.command(name="list")
def list_todos():
    """列出所有 todo。"""
    todos = load_todos()
    if not todos:
        print("还没有 todo，先 add 一个吧")
        return
    for i, t in enumerate(todos, start=1):
        mark = "[x]" if t["done"] else "[ ]"
        print(f"{i}. {mark} {t['item']}")


@app.command()
def done(index: int):
    """把第 index 项 todo 标记为完成。"""
    todos = load_todos()
    if index < 1 or index > len(todos):
        print(f"序号要在 1 到 {len(todos)} 之间")
        raise typer.Exit(code=1)
    todos[index - 1]["done"] = True
    save_todos(todos)
    print(f"已完成：{todos[index - 1]['item']}")


if __name__ == "__main__":
    app()
```

注意几个细节——

- `list` 是 Python 内置函数，不能直接当函数名，所以函数叫 `list_todos`，但是用 `@app.command(name="list")` 把它注册成 `list` 命令
- `Path.home() / ".todo-cli.json"` 用 `pathlib`，比 `os.path.join` 优雅多了（参考 `python18` 那一章）
- `typer.Exit(code=1)` 抛一个特殊异常，让 CLI 退出时返回非零退出码，方便脚本判断成败
- 文件用 `encoding="utf-8"`，windows 上中文不挂

### 第三步：配置 pyproject.toml

完整的 `pyproject.toml`：

```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "两点水写的最小 todo 命令行工具"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    { name = "两点水", email = "liangdianshui@example.com" },
]
license = { file = "LICENSE" }
dependencies = [
    "typer>=0.12",
]

[project.scripts]
todo-cli = "todo_cli.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

注意 `[project.scripts]` 那一行——发包之后，用户 `pip install todo-cli`，会自动多出一个叫 `todo-cli` 的命令。

### 第四步：本地装一下试试

```bash
uv pip install -e .
todo-cli add "写完 python27"
todo-cli add "去吃饭"
todo-cli list
todo-cli done 1
todo-cli list
```

输出大概是——

```
已添加：写完 python27
已添加：去吃饭
1. [ ] 写完 python27
2. [ ] 去吃饭
已完成：写完 python27
1. [x] 写完 python27
2. [ ] 去吃饭
```

打开 `~/.todo-cli.json` 看看：

```json
[
  {
    "item": "写完 python27",
    "done": true
  },
  {
    "item": "去吃饭",
    "done": false
  }
]
```

数据被持久化了，下次重启电脑，todo 还在。

### 第五步：补 README 和 LICENSE

`README.md`：

```markdown
# todo-cli

两点水写的最小 todo 命令行工具。

## 安装

```bash
pip install todo-cli
```

## 用法

```bash
todo-cli add "学 typer"
todo-cli list
todo-cli done 1
```

## License

MIT
```

`LICENSE` 文件直接抄一份 MIT，把年份和名字改成自己的。

### 第六步：构建并发到 TestPyPI

```bash
uv build
ls dist/
```

得到——

```
dist/
├── todo_cli-0.1.0-py3-none-any.whl
└── todo_cli-0.1.0.tar.gz
```

发 TestPyPI 演练：

```bash
export UV_PUBLISH_TOKEN=pypi-...（TestPyPI token）
uv publish --publish-url https://test.pypi.org/legacy/
```

成功之后，找一台干净的电脑（或者新建一个虚拟环境）测一下：

```bash
uv venv .test-env
source .test-env/bin/activate
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    todo-cli
todo-cli --help
```

能跑就发正式 PyPI：

```bash
export UV_PUBLISH_TOKEN=pypi-...（正式 PyPI token）
uv publish
```

打开 `https://pypi.org/project/todo-cli/`，自己的小工具上线了。水哥写到这里又有点小激动——这就是「全世界一行 `pip install todo-cli` 就能用」的感觉。

「这个名字是 PyPI 上唯一的吗？」名字起得太常见，PyPI 上很可能已经被占用，请各位实际发包时换一个独特点的名字，比如 `todo-cli-by-walter`、`my-todo-cli` 之类。

到这里，整套流程一遍走通了——从写代码、改 `pyproject.toml`、本地装、本地测、TestPyPI 演练、正式 PyPI 发布。



## 小结

一章下来，咱们把「打包发布」和「写 CLI」两件事都拿下了。回顾一下要点——

**关于 PyPI**：

1. **PyPI 是 Python 全球公共包仓库**，`pip install` 的源头
2. **TestPyPI 是演练场**，发正式版本之前先在它上面试一遍，因为 PyPI 版本不可撤回
3. **现代 Python 项目用 `src layout` + `pyproject.toml`**，所有元数据集中在一个文件
4. **`[project]` 段最低必填**：name、version、description、readme、requires-python、dependencies
5. **`[build-system]` 段写打包后端**，新项目首选 `hatchling`
6. **`uv build` 一条命令打包**，生成 `wheel`（二进制）和 `sdist`（源码）
7. **`uv publish` 一条命令上传**，靠 token 或者可信发布
8. **版本号建议自动化**——用 `hatch-vcs` 从 git tag 自动算
9. **CI 自动发包推荐用可信发布**，比 token 干净——打 tag 即发版

**关于 typer**：

10. **`typer` 用类型注解直接当 CLI 参数**，比 `argparse` 简洁 10 倍
11. **`typer.run(func)` 适合单命令工具**，`Typer()` + `@app.command()` 适合多命令工具
12. **类型即验证**——`int` 类型自动验证、`Path` 类型自动包装、`Enum` 类型自动限定值
13. **没默认值是位置参数（必填），有默认值是选项参数（可选）**
14. **`[project.scripts]` 把函数变成系统命令**，装包之后命令全局可用
15. **docstring 自动变成命令帮助文本**，写代码就是写文档

到这里，各位手里就握着一套「写工具 → 打包 → 发布 → 让全世界用上」的完整链条。下一次再想把自己的小工具分享给朋友，不用微信发 `tool.py` 了——直接说「`pip install xxx`」，潇洒。

各位接下来给自己一个小作业——把日常用的某个 Python 脚本（截图重命名也好、聊天记录统计也好），按照本章的流程改造一遍，发到 TestPyPI 上演练一次。哪怕没真发到正式 PyPI，单走完一遍流程，下次发起来就是肌肉记忆了。

走起。



## 先把本地命令的使用约定做清楚

学到打包发布时，我们先用学习时间记录工具检查一个更小的目标：别人拿到代码，能不能知道怎样调用、参数填什么、失败时发生什么。

在项目目录运行：

```bash
python3 tracker.py --help
python3 tracker.py --file practice-records.json list
python3 tracker.py --file practice-records.json total --subject Python
```

一份尚不存在的记录文件应该显示「暂无记录」，指定科目的总时长是 `0`。这两条查询不会为了显示空结果而创建数据文件。接着按最后一章添加几条记录，检查帮助、列表、统计和测试是否一致。

这个参考工具使用标准库 `argparse`，目的是把入口和核心函数分开。typer 与打包步骤可以在本地功能明确以后继续练，不需要为了验证入口先上传一个包。

给自己的工具补一段最短使用说明：需要哪个 Python、从哪个目录运行、记录保存在何处、遇到损坏数据如何报告。确认本地功能正常以后，再按本章的 TestPyPI 步骤练习打包和安装，检查别人能否照着说明使用。
