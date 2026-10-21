"""检查联合核验能发现失效跳转，同时允许没有旧网址的新课。"""

import unittest

from check_course_targets import target_errors


class CourseTargetTests(unittest.TestCase):
    def test_existing_targets(self):
        self.assertEqual(target_errors({"python1": "intro"}, {("python1", "intro")}), [])

    def test_missing_or_renamed_target(self):
        self.assertEqual(
            target_errors({"python1": "intro"}, {("python1", "renamed")}),
            ["跳转目标不存在：python1/intro"],
        )

    def test_new_course_does_not_need_a_legacy_url(self):
        self.assertEqual(
            target_errors({"python1": "intro"}, {("python1", "intro"), ("python29", "new")}),
            [],
        )


if __name__ == "__main__":
    unittest.main()
