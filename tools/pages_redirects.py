"""将旧 MkDocs 页面发布为 learn-py.org 跳转入口，保留教程源文件。"""

from html import escape
import json
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
    url = target_url(page.file.src_uri)
    target = escape(url, quote=True)
    script_target = json.dumps(url).replace("<", "\\u003c")
    title = escape(page.title or "小白学 Python")
    # 在解析正文前启动导航，replace 避免返回时又经过中转页。
    # meta refresh 为无脚本兜底；背景匹配新站默认主题，不读取另一域名的偏好。
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    html {{ background: #020617; color: #cbd5e1; color-scheme: dark; }}
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center;
      font: 16px/1.7 system-ui, sans-serif; }}
    main {{ max-width: 28rem; padding: 1.5rem; }}
    h1 {{ font-size: 1.125rem; font-weight: 500; }}
    a {{ color: #6ee7b7; text-underline-offset: .2em; }}
    a:focus-visible {{ outline: 2px solid currentColor; outline-offset: 4px; }}
  </style>
  <link rel="preconnect" href="https://learn-py.org">
  <script>window.location.replace({script_target});</script>
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <title>{title} — 已迁移至小白学 Python</title>
</head>
<body>
  <main>
    <h1>正在打开小白学 Python…</h1>
    <p>若未自动进入，请<a href="{target}">继续阅读教程</a>。</p>
  </main>
</body>
</html>
'''
