"""跳转映射的回归检查，不访问网络。"""

from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
import unittest

from pages_redirects import on_page_markdown, on_post_page, target_url


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
        }.items():
            with self.subTest(source=source):
                self.assertEqual(target_url(source), target)

    def test_every_existing_article_has_a_target(self):
        articles = Path(__file__).resolve().parents[1] / "Article"
        sources = list(articles.rglob("*.md"))
        self.assertTrue(sources)
        for source in sources:
            uri = source.relative_to(articles).as_posix()
            with self.subTest(source=uri):
                url = target_url(uri)
                if uri != "index.md":
                    self.assertTrue(url.startswith("https://learn-py.org/lessons/"))
                    self.assertTrue(url.endswith("/read/"))

    def test_unmapped_sources_fail_closed(self):
        for source in ["", "new-page.md", "PythonBasis/python29/1.md", "../index.md"]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                target_url(source)

    def test_html_redirect_without_javascript(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri="index.md"), title="<script>bad()</script>")
        html = on_post_page("原教程正文", page=page)
        parser = Tags()
        parser.feed(html)
        self.assertIn(("meta", {"http-equiv": "refresh", "content": "0; url=https://learn-py.org/"}), parser.tags)
        self.assertIn(("link", {"rel": "canonical", "href": "https://learn-py.org/"}), parser.tags)
        self.assertIn(("a", {"href": "https://learn-py.org/"}), parser.tags)
        self.assertNotIn("script", [tag for tag, _ in parser.tags])
        self.assertNotIn("原教程正文", html)

    def test_search_content_is_migration_notice(self):
        page = SimpleNamespace(file=SimpleNamespace(src_uri="index.md"))
        markdown = on_page_markdown("原教程正文", page=page)
        self.assertIn("https://learn-py.org/", markdown)
        self.assertNotIn("原教程正文", markdown)


if __name__ == "__main__":
    unittest.main()
