"""将 MkDocs 页面与 100 个旧网址统一发布为 learn-py.org 跳转入口，保留教程源文件。"""

from html import escape
import json
from pathlib import Path, PurePosixPath


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
    "practice1": "talk-to-program",
    "practice2": "ledger-v1",
    "practice3": "debugging",
    "practice4": "ledger-rewrite",
    "practice5": "files-csv-json",
    "practice6": "learn-a-module",
    "crawler1": "crawler-intro",
    "crawler2": "http-request",
    "crawler3": "html-and-devtools",
    "crawler4": "beautifulsoup-basics",
    "crawler5": "extract-list",
    "crawler6": "pagination-and-politeness",
    "crawler7": "json-api",
    "crawler8": "save-data",
    "crawler9": "bookstore-project",
    "crawler10": "local-requests",
    "crawler11": "session-and-cookies",
    "crawler12": "dynamic-and-concurrency",
    "data1": "what-is-analysis",
    "data2": "first-dataframe",
    "data3": "selecting-data",
    "data4": "descriptive-stats",
    "data5": "data-cleaning",
    "data6": "groupby-and-pivot",
    "data7": "merge-and-concat",
    "data8": "charts",
    "data9": "ledger-analysis",
    "data10": "bookstore-report",
}

TUTORIAL_CHAPTERS = {
    "01-basics/00-why-python.md": "python0",
    "01-basics/00b-code-specification.md": "python17",
    "01-basics/01-hello-world.md": "python1",
    "01-basics/02-data-types-and-variables.md": "python2",
    "01-basics/02b-practice-1-talk-to-program.md": "practice1",
    "01-basics/03-list-and-tuple.md": "python3",
    "01-basics/04-dict-and-set.md": "python4",
    "01-basics/05-conditions-and-loops.md": "python5",
    "01-basics/05b-practice-2-ledger-v1.md": "practice2",
    "01-basics/06-functions.md": "python6",
    "01-basics/06b-practice-3-debugging.md": "practice3",
    "01-basics/07-iteration.md": "python7",
    "01-basics/08-oop.md": "python8",
    "01-basics/08b-practice-4-ledger-rewrite.md": "practice4",
    "01-basics/09-modules.md": "python9",
    "01-basics/09b-practice-5-files-csv-json.md": "practice5",
    "01-basics/09c-practice-6-learn-a-module.md": "practice6",
    "02-advanced/10-magic-methods.md": "python10",
    "02-advanced/11-enum.md": "python11",
    "02-advanced/12-metaclass.md": "python12",
    "02-advanced/13-threading.md": "python13",
    "02-advanced/14-regex.md": "python14",
    "02-advanced/15-closure.md": "python15",
    "02-advanced/16-decorator.md": "python16",
    "02-advanced/17-type-hints.md": "python17",
    "02-advanced/18-pathlib.md": "python18",
    "02-advanced/19-exception-handling.md": "python19",
    "02-advanced/20-dataclass.md": "python20",
    "02-advanced/21-context-manager.md": "python21",
    "02-advanced/22-async.md": "python22",
    "03-engineering/23-pyproject-uv.md": "python23",
    "03-engineering/24-ruff.md": "python24",
    "03-engineering/25-pytest.md": "python25",
    "03-engineering/26-logging.md": "python26",
    "03-engineering/27-pypi.md": "python27",
    "03-engineering/28-whats-next.md": "python28",
    "04-crawler/01-crawler-intro.md": "crawler1",
    "04-crawler/02-http-request.md": "crawler2",
    "04-crawler/03-html-and-devtools.md": "crawler3",
    "04-crawler/04-beautifulsoup-basics.md": "crawler4",
    "04-crawler/05-extract-list.md": "crawler5",
    "04-crawler/06-pagination-and-politeness.md": "crawler6",
    "04-crawler/07-json-api.md": "crawler7",
    "04-crawler/08-save-data.md": "crawler8",
    "04-crawler/09-bookstore-project.md": "crawler9",
    "04-crawler/10-local-requests.md": "crawler10",
    "04-crawler/11-session-and-cookies.md": "crawler11",
    "04-crawler/12-dynamic-and-concurrency.md": "crawler12",
    "05-data-analysis/01-what-is-analysis.md": "data1",
    "05-data-analysis/02-first-dataframe.md": "data2",
    "05-data-analysis/03-selecting-data.md": "data3",
    "05-data-analysis/04-descriptive-stats.md": "data4",
    "05-data-analysis/05-data-cleaning.md": "data5",
    "05-data-analysis/06-groupby-and-pivot.md": "data6",
    "05-data-analysis/07-merge-and-concat.md": "data7",
    "05-data-analysis/08-charts.md": "data8",
    "05-data-analysis/09-ledger-analysis.md": "data9",
    "05-data-analysis/10-bookstore-report.md": "data10",
}

# 旧站 GitHub Pages 历史网址（除 index.md 外共 99 个子页），与正文目录解耦以保住外链跳转。
LEGACY_URIS = (
    "PythonBasis/python0/WhyStudyPython.md",
    "PythonBasis/python1/IDE.md",
    "PythonBasis/python1/Installation.md",
    "PythonBasis/python1/Introduction.md",
    "PythonBasis/python1/Preface.md",
    "PythonBasis/python1/The_first_procedure.md",
    "PythonBasis/python2/Grammar.md",
    "PythonBasis/python2/Preface.md",
    "PythonBasis/python2/StringCoding.md",
    "PythonBasis/python2/Type_conversion.md",
    "PythonBasis/python2/Type_of_data.md",
    "PythonBasis/python2/Variable.md",
    "PythonBasis/python2/print.md",
    "PythonBasis/python3/List.md",
    "PythonBasis/python3/Preface.md",
    "PythonBasis/python3/tuple.md",
    "PythonBasis/python4/Dict.md",
    "PythonBasis/python4/Preface.md",
    "PythonBasis/python4/Set.md",
    "PythonBasis/python5/Cycle.md",
    "PythonBasis/python5/Example.md",
    "PythonBasis/python5/If.md",
    "PythonBasis/python5/Preface.md",
    "PythonBasis/python6/1.md",
    "PythonBasis/python6/2.md",
    "PythonBasis/python6/3.md",
    "PythonBasis/python6/4.md",
    "PythonBasis/python6/5.md",
    "PythonBasis/python6/Preface.md",
    "PythonBasis/python7/1.md",
    "PythonBasis/python7/2.md",
    "PythonBasis/python7/3.md",
    "PythonBasis/python7/4.md",
    "PythonBasis/python7/5.md",
    "PythonBasis/python7/Preface.md",
    "PythonBasis/python8/1.md",
    "PythonBasis/python8/2.md",
    "PythonBasis/python8/3.md",
    "PythonBasis/python8/4.md",
    "PythonBasis/python8/5.md",
    "PythonBasis/python8/6.md",
    "PythonBasis/python8/7.md",
    "PythonBasis/python8/8.md",
    "PythonBasis/python8/9.md",
    "PythonBasis/python8/Preface.md",
    "PythonBasis/python9/1.md",
    "PythonBasis/python9/2.md",
    "PythonBasis/python9/3.md",
    "PythonBasis/python9/4.md",
    "PythonBasis/python9/5.md",
    "PythonBasis/python9/Preface.md",
    "PythonBasis/python10/1.md",
    "PythonBasis/python10/2.md",
    "PythonBasis/python10/3.md",
    "PythonBasis/python10/4.md",
    "PythonBasis/python10/5.md",
    "PythonBasis/python10/6.md",
    "PythonBasis/python10/Preface.md",
    "PythonBasis/python11/1.md",
    "PythonBasis/python11/2.md",
    "PythonBasis/python11/3.md",
    "PythonBasis/python11/4.md",
    "PythonBasis/python11/Preface.md",
    "PythonBasis/python12/1.md",
    "PythonBasis/python12/2.md",
    "PythonBasis/python12/3.md",
    "PythonBasis/python12/4.md",
    "PythonBasis/python12/5.md",
    "PythonBasis/python12/Preface.md",
    "PythonBasis/python13/1.md",
    "PythonBasis/python13/2.md",
    "PythonBasis/python13/3.md",
    "PythonBasis/python13/Preface.md",
    "PythonBasis/python14/1.md",
    "PythonBasis/python14/2.md",
    "PythonBasis/python14/3.md",
    "PythonBasis/python14/4.md",
    "PythonBasis/python14/5.md",
    "PythonBasis/python14/6.md",
    "PythonBasis/python14/Preface.md",
    "PythonBasis/python14/常用的正则表达式.md",
    "PythonBasis/python15/1.md",
    "PythonBasis/python16/1.md",
    "PythonBasis/python17/1.md",
    "PythonBasis/python18/1.md",
    "PythonBasis/python19/1.md",
    "PythonBasis/python20/1.md",
    "PythonBasis/python21/1.md",
    "PythonBasis/python22/1.md",
    "PythonBasis/python23/1.md",
    "PythonBasis/python24/1.md",
    "PythonBasis/python25/1.md",
    "PythonBasis/python26/1.md",
    "PythonBasis/python27/1.md",
    "PythonBasis/python28/1.md",
    "codeSpecification/codeSpecification_Preface.md",
    "codeSpecification/codeSpecification_first.md",
    "codeSpecification/codeSpecification_second.md",
    "codeSpecification/codeSpecification_third.md",
)


def target_url(src_uri):
    """未知目录直接阻止构建，避免新增内容被错误导向首页。"""
    if src_uri == "index.md":
        return "https://learn-py.org/"
    if src_uri in TUTORIAL_CHAPTERS:
        chapter = TUTORIAL_CHAPTERS[src_uri]
        return f"https://learn-py.org/lessons/{chapter}/{LESSONS[chapter]}/read/"
    parts = PurePosixPath(src_uri).parts
    if len(parts) == 2 and parts[0] == "codeSpecification":
        chapter = "python17"
    elif len(parts) == 3 and parts[0] == "PythonBasis" and parts[1] in LESSONS:
        chapter = parts[1]
    else:
        raise ValueError(f"旧站页面尚未配置跳转目标：{src_uri}")
    return f"https://learn-py.org/lessons/{chapter}/{LESSONS[chapter]}/read/"


def render_redirect_html(url, title="小白学 Python"):
    target = escape(url, quote=True)
    script_target = json.dumps(url).replace("<", "\\u003c")
    safe_title = escape(title or "小白学 Python")
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
  <title>{safe_title} — 已迁移至小白学 Python</title>
</head>
<body>
  <main>
    <h1>正在打开小白学 Python…</h1>
    <p>若未自动进入，请<a href="{target}">继续阅读教程</a>。</p>
  </main>
</body>
</html>
'''


def on_page_markdown(markdown, *, page, **kwargs):
    # 搜索索引也只保留迁移提示，不再发布一份重复的教程正文。
    return f"本页已迁移，请前往 [小白学 Python]({target_url(page.file.src_uri)})。"


def on_post_page(output, *, page, **kwargs):
    return render_redirect_html(target_url(page.file.src_uri), page.title)


def on_post_build(*, config, **kwargs):
    site_dir = Path(config["site_dir"])
    for uri in LEGACY_URIS:
        dest_dir = site_dir / PurePosixPath(uri).with_suffix("")
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / "index.html").write_text(
            render_redirect_html(target_url(uri)),
            encoding="utf-8",
        )
