"""综合练习的验收用例；unittest 与 pytest 均可发现。"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tracker import load_records, main, make_record, save_records, total_minutes


class RecordTests(unittest.TestCase):
    def test_subject_is_trimmed_and_zero_is_allowed(self):
        self.assertEqual(
            make_record(" Python ", 0), {"subject": "Python", "minutes": 0}
        )

    def test_invalid_minutes(self):
        for value in [-1, True, 1.5, "15", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                make_record("Python", value)

    def test_invalid_subject(self):
        for value in ["", "  ", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                make_record(value, 15)

    def test_total_and_filter(self):
        records = [
            make_record("Python", 15),
            make_record("读书", 10),
            make_record("Python", 5),
        ]
        self.assertEqual(total_minutes(records), 30)
        self.assertEqual(total_minutes(records, "Python"), 20)
        self.assertEqual(total_minutes(records, "不存在的科目"), 0)
        self.assertEqual(total_minutes([]), 0)


class FileTests(unittest.TestCase):
    def setUp(self):
        # 验收数据留在独立临时目录，避免接触读者已有记录。
        self.folder = Path(tempfile.mkdtemp(prefix="study-tracker-test-"))
        self.path = self.folder / "records.json"

    def test_missing_file(self):
        self.assertEqual(load_records(self.path), [])

    def test_round_trip_with_chinese(self):
        records = [make_record("读书", 10)]
        save_records(self.path, records)
        self.assertEqual(load_records(self.path), records)
        self.assertIn("读书", self.path.read_text(encoding="utf-8"))

    def test_corrupt_file_is_not_overwritten(self):
        original = "{这是损坏的数据"
        self.path.write_text(original, encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            result = main(["--file", str(self.path), "add", "Python", "15"])
        self.assertEqual(result, 2)
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_invalid_schema_and_data(self):
        cases = [
            ("{}", TypeError),
            ("[{}]", ValueError),
            ('[{"subject":"Python","minutes":true}]', ValueError),
        ]
        for content, expected_error in cases:
            self.path.write_text(content, encoding="utf-8")
            with self.assertRaises(expected_error):
                load_records(self.path)

    def test_invalid_record_is_not_saved(self):
        records = [make_record("Python", 15)]
        save_records(self.path, records)
        original = self.path.read_bytes()
        with self.assertRaises(ValueError):
            save_records(self.path, [{"subject": "Python", "minutes": -1}])
        self.assertEqual(self.path.read_bytes(), original)

    def test_cli_add_list_total_and_negative_minutes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--file", str(self.path), "add", "Python", "15"]), 0)
            self.assertEqual(main(["--file", str(self.path), "list"]), 0)
            self.assertEqual(main(["--file", str(self.path), "total"]), 0)
        self.assertEqual(
            output.getvalue(),
            "已记录：Python 15 分钟\n1. Python：15 分钟\n合计：15 分钟\n",
        )
        original = self.path.read_bytes()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--file", str(self.path), "add", "Python", "-1"]), 2)
        self.assertEqual(self.path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
