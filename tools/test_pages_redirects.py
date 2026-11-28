"""跳转映射的回归检查，不访问网络。"""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest

from pages_redirects import (
    LEGACY_URIS,
    on_page_markdown,
    on_post_build,
    on_post_page,
    target_url,
)


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class RedirectTests(unittest.TestCase):
    def test_home_and_chapters(self):
        for source, target in {
            "index.md": "https://learn-py.org/",
            "PythonBasis/python2/Type_of_data.md": "https://learn-py.org/lessons/python2/data-types-and-variables/read/",
            "PythonBasis/python28/1.md": "https://learn-py.org/lessons/python28/whats-next/read/",
            "codeSpecification/codeSpecification_second.md": "https://learn-py.org/lessons/python17/readable-code/read/",
            "01-basics/02-data-types-and-variables.md": "https://learn-py.org/lessons/python2/data-types-and-variables/read/",
            "04-crawler/01-crawler-intro.md": "https://learn-py.org/lessons/crawler1/crawler-intro/read/",
            "05-data-analysis/10-bookstore-report.md": "https://learn-py.org/lessons/data10/bookstore-report/read/",
        }.items():
            with self.subTest(source=source):
                self.assertEqual(target_url(source), target)

    def test_every_tutorial_and_legacy_uri_has_a_target(self):
        tutorials = Path(__file__).resolve().parents[1] / "tutorials"
        sources = [p.relative_to(tutorials).as_posix() for p in tutorials.rglob("*.md")]
        self.assertEqual(len(sources), 59)  # index.md + 58 篇教程
        self.assertEqual(len(LEGACY_URIS), 99)
        for uri in [*sources, *LEGACY_URIS]:
            with self.subTest(source=uri):
                url = target_url(uri)
                if uri != "index.md":
                    self.assertTrue(url.startswith("https://learn-py.org/lessons/"))
                    self.assertTrue(url.endswith("/read/"))

    def test_unmapped_sources_fail_closed(self):
        for source in ["", "new-page.md", "PythonBasis/python29/1.md", "../index.md"]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                target_url(source)

    def test_html_refresh_and_manual_fallback(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri="index.md"), title="<script>bad()</script>")
        html = on_post_page("原教程正文", page=page)
        parser = Tags()
        parser.feed(html)
        self.assertIn(("meta", {"http-equiv": "refresh", "content": "0; url=https://learn-py.org/"}), parser.tags)
        self.assertIn(("link", {"rel": "canonical", "href": "https://learn-py.org/"}), parser.tags)
        self.assertIn(("a", {"href": "https://learn-py.org/"}), parser.tags)
        self.assertEqual([attrs for tag, attrs in parser.tags if tag == "script"], [{}])
        self.assertIn('&lt;script&gt;bad()&lt;/script&gt;', html)
        self.assertNotIn("原教程正文", html)

    def test_early_replace_preserves_all_targets_and_legacy_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            on_post_build(config={"site_dir": tmp})
            for uri in LEGACY_URIS:
                out = Path(tmp) / Path(uri).with_suffix("") / "index.html"
                with self.subTest(source=uri):
                    self.assertTrue(out.exists())
                    html = out.read_text(encoding="utf-8")
                    script = re.search(r'<script>window\.location\.replace\((.*?)\);</script>', html)
                    self.assertIsNotNone(script)
                    self.assertEqual(json.loads(script.group(1)), target_url(uri))
                    self.assertLess(script.start(), html.index('<body>'))
                    self.assertLess(html.index('background: #020617'), script.start())
                    self.assertIn('content="0; url=' + target_url(uri) + '"', html)
                    self.assertLess(len(html.encode()), 2048)

    def test_search_content_is_migration_notice(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri="index.md"))
        markdown = on_page_markdown("原教程正文", page=page)
        self.assertIn("https://learn-py.org/", markdown)
        self.assertNotIn("原教程正文", markdown)


if __name__ == "__main__":
    unittest.main()
