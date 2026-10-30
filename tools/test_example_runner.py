"""示例运行器的回归检查：示例写出的文件不能落进调用者的当前目录。"""

import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

from example_runner import main


class ExampleRunnerTests(unittest.TestCase):
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
