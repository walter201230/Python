"""示例运行器的命令行和工作目录回归检查。"""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from example_runner import main

RUNNER = Path(__file__).with_name("example_runner.py")


class ExampleRunnerTests(unittest.TestCase):
    def test_single_markdown_file_runs_its_examples(self):
        with tempfile.TemporaryDirectory() as folder:
            article = Path(folder) / "lesson.md"
            article.write_text("```python\nassert False\n```\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, RUNNER, article], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn(f"FAIL {article}:1", result.stdout)
            self.assertIn("总计 1 块", result.stdout)

    def test_invalid_input_paths_report_an_error(self):
        with tempfile.TemporaryDirectory() as folder:
            other_file = Path(folder) / "lesson.txt"
            other_file.touch()
            for path in (other_file, Path(folder) / "missing.md"):
                with self.subTest(path=path):
                    result = subprocess.run(
                        [sys.executable, RUNNER, path], capture_output=True, text=True
                    )
                    self.assertEqual(result.returncode, 2)
                    self.assertIn(str(path), result.stderr)

    def test_examples_do_not_write_into_caller_cwd(self):
        with tempfile.TemporaryDirectory() as caller:
            article = Path(caller) / "docs" / "a.md"
            article.parent.mkdir()
            article.write_text(
                "```python\nopen('app.log', 'w').write('x')\n```\n\n"
                "```python\nassert open('app.log').read() == 'x'\n```\n",
                encoding="utf-8",
            )
            previous = os.getcwd()
            os.chdir(caller)
            try:
                with mock.patch.object(sys, "argv", ["example_runner.py", "docs"]), \
                        contextlib.redirect_stdout(io.StringIO()) as output:
                    code = main()
            finally:
                os.chdir(previous)

            # 第二块读取第一块写出的文件：同一次运行内的示例仍共享工作目录
            self.assertEqual(code, 0, output.getvalue())
            self.assertEqual([p.name for p in Path(caller).iterdir()], ["docs"])


if __name__ == "__main__":
    unittest.main()
