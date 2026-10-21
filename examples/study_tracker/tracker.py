"""学习时间记录工具：用标准库完成添加、查看、统计与 JSON 保存。"""

import argparse
import json
import sys
from pathlib import Path


def make_record(subject, minutes):
    """创建一条记录；分钟数允许为零，不接受负数、布尔值或小数。"""
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("科目不能为空")
    if type(minutes) is not int or minutes < 0:
        raise ValueError("分钟数必须是非负整数")
    return {"subject": subject.strip(), "minutes": minutes}


def validate_records(data):
    """验证文件中的记录，不把损坏内容当成空记录覆盖。"""
    if not isinstance(data, list):
        raise TypeError("记录文件的最外层必须是列表")
    records = []
    for item in data:
        if not isinstance(item, dict) or set(item) != {"subject", "minutes"}:
            raise ValueError("每条记录必须包含 subject 和 minutes 两个字段")
        records.append(make_record(item["subject"], item["minutes"]))
    return records


def total_minutes(records, subject=None):
    """统计全部记录，或指定科目的记录。"""
    return sum(
        item["minutes"]
        for item in records
        if subject is None or item["subject"] == subject
    )


def load_records(path):
    """文件不存在时从空列表开始；格式损坏时让调用方处理错误。"""
    try:
        content = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    return validate_records(json.loads(content))


def save_records(path, records):
    """先检查记录再写入；同一路径保存的是完整的当前记录。"""
    validated = validate_records(records)
    content = json.dumps(validated, ensure_ascii=False, indent=2) + "\n"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="记录与统计学习分钟数")
    parser.add_argument("--file", default="study-records.json", help="JSON 记录路径")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="增加一条学习记录")
    add.add_argument("subject", help="科目名称")
    add.add_argument("minutes", type=int, help="非负整数分钟数")
    commands.add_parser("list", help="列出全部记录")
    total = commands.add_parser("total", help="统计学习时间")
    total.add_argument("--subject", help="只统计这个科目")
    args = parser.parse_args(argv)

    try:
        records = load_records(args.file)
        if args.command == "add":
            record = make_record(args.subject, args.minutes)
            records.append(record)
            save_records(args.file, records)
            print(f"已记录：{record['subject']} {record['minutes']} 分钟")
        elif args.command == "list":
            if not records:
                print("暂无记录")
            for index, record in enumerate(records, 1):
                print(f"{index}. {record['subject']}：{record['minutes']} 分钟")
        else:
            print(f"合计：{total_minutes(records, args.subject)} 分钟")
    except (OSError, TypeError, ValueError) as error:
        print(f"无法处理记录：{error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
