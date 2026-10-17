"""将旧 MkDocs 页面发布为 learn-py.org 跳转入口，保留教程源文件。"""

from html import escape
from pathlib import PurePosixPath


LESSONS = {
    "python0": "why-python",
    "python1": "intro-and-hello-world",
    "python2": "data-types-and-variables",
    "python3": "list-and-tuple",
    "python4": "dict-and-set",
    "python5": "conditions-and-loops",
    "python6": "functions",
    "python7": "iteration",
    "python8": "oop",
    "python9": "modules",
    "python10": "magic-methods",
    "python11": "enum",
    "python12": "metaclass",
    "python13": "threading",
    "python14": "regex",
    "python15": "closure",
    "python16": "decorator",
    "python17": "readable-code",
    "python18": "pathlib",
    "python19": "exception-handling",
    "python20": "dataclass",
    "python21": "context-manager",
    "python22": "async",
    "python23": "pyproject-uv",
    "python24": "ruff",
    "python25": "pytest",
    "python26": "logging",
    "python27": "pypi",
    "python28": "whats-next",
}


def target_url(src_uri):
    """未知目录直接阻止构建，避免新增内容被错误导向首页。"""
    if src_uri == "index.md":
        return "https://learn-py.org/"
    parts = PurePosixPath(src_uri).parts
    if len(parts) == 2 and parts[0] == "codeSpecification":
        chapter = "python17"
    elif len(parts) == 3 and parts[0] == "PythonBasis" and parts[1] in LESSONS:
        chapter = parts[1]
    else:
        raise ValueError(f"旧站页面尚未配置跳转目标：{src_uri}")
    return f"https://learn-py.org/lessons/{chapter}/{LESSONS[chapter]}/read/"


def on_page_markdown(markdown, *, page, **kwargs):
    # 搜索索引也只保留迁移提示，不再发布一份重复的教程正文。
    return f"本页已迁移，请前往 [小白学 Python]({target_url(page.file.src_uri)})。"


def on_post_page(output, *, page, **kwargs):
    target = escape(target_url(page.file.src_uri), quote=True)
    title = escape(page.title or "小白学 Python")
    # 0 秒 meta refresh 无需 JavaScript；canonical 与手动链接使用同一目标。
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>{title} — 已迁移至小白学 Python</title>
</head>
<body>
  <main>
    <h1>教程已迁移</h1>
    <p>正在前往小白学 Python。若未自动跳转，请<a href="{target}">点击这里继续阅读</a>。</p>
  </main>
</body>
</html>
'''
