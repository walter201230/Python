"""扫描 Article/**/*.md，提取 ```python 代码块逐块跑一遍。

用法：
    python tools/example_runner.py [path]

不写 path 默认扫描 Article/。
代码块前若有 <!-- skip-ci --> 注释行则跳过。
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BLOCK_RE = re.compile(
    r"(?:(<!--\s*skip-ci\s*-->)\s*\n)?```[Pp]ython\s*\n(.*?)\n```",
    re.DOTALL,
)


def extract_blocks(md_path: Path) -> list[tuple[int, str, bool]]:
    """返回 (起始行号, 代码内容, 是否 skip) 三元组列表。"""
    text = md_path.read_text(encoding="utf-8")
    blocks: list[tuple[int, str, bool]] = []
    for m in BLOCK_RE.finditer(text):
        skip = m.group(1) is not None
        line_no = text[: m.start()].count("\n") + 1
        blocks.append((line_no, m.group(2), skip))
    return blocks


def run_block(code: str, timeout: int = 30, cwd: str | None = None) -> tuple[bool, str]:
    """把 code 写到临时文件并在 cwd 下跑，返回 (成功?, stderr)。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=timeout,
            # 不给子进程继承 stdin：含 input() 的块在有 stdin 的环境里会一直等输入
            # 直到超时，在没有 stdin 的环境里立刻抛 EOFError——同一份代码两种结果，
            # CI 各版本失败数因此长期在 69~72 之间飘。钉死成 DEVNULL 让它稳定抛 EOFError。
            stdin=subprocess.DEVNULL,
            cwd=cwd,
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s"
    finally:
        Path(path).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", default=["Article"])
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    failed = 0
    total = 0
    skipped = 0

    # 示例会写 app.log、记录目录等文件：统一放进本次运行的临时目录，不落进调用者的当前目录；
    # 同一次运行内共用这个目录，前一块写出的文件后一块仍能读到。
    with tempfile.TemporaryDirectory() as workdir:
        for top in args.paths:
            root = Path(top)
            if not root.exists():
                print(f"路径不存在：{root}", file=sys.stderr)
                continue
            for md in sorted(root.rglob("*.md")):
                for line_no, code, skip in extract_blocks(md):
                    total += 1
                    if skip:
                        skipped += 1
                        continue
                    ok, err = run_block(code, args.timeout, workdir)
                    if not ok:
                        failed += 1
                        print(f"FAIL {md}:{line_no}\n  {err.strip()}\n")

    print(f"\n总计 {total} 块；跳过 {skipped}；失败 {failed}")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
