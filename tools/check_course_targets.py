"""本地联合核验旧站跳转与学习站课程；不加入独立仓库的生产构建依赖。"""

import argparse
import json
from pathlib import Path

from pages_redirects import LESSONS


def target_errors(targets, courses):
    """新课程可以没有旧网址，但每个既有跳转目标必须有课程承接。"""
    return [
        f"跳转目标不存在：{chapter}/{lesson}"
        for chapter, lesson in targets.items()
        if (chapter, lesson) not in courses
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_root", type=Path, help="学习站的 web/content/lessons 目录")
    args = parser.parse_args()
    files = sorted(args.content_root.glob("*/*/lesson.json"))
    if not files:
        parser.error("指定目录没有课程 lesson.json，无法核验")
    courses = set()
    for file in files:
        try:
            meta = json.loads(file.read_text(encoding="utf-8"))
            pair = (file.parent.parent.name, file.parent.name)
            if not isinstance(meta, dict) or (meta.get("chapter"), meta.get("id")) != pair:
                raise ValueError("chapter／id 与实际目录不一致")
            courses.add(pair)
        except (ValueError, OSError) as error:
            parser.error(f"{file}: {error}")
    errors = target_errors(LESSONS, courses)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print(f"✓ 两仓课程目标一致：{len(LESSONS)} 个旧站目标，{len(courses)} 门学习站课程")


if __name__ == "__main__":
    main()
