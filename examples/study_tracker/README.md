# 学习时间记录工具

这是「学完之后做什么」补充练习的完整参考实现，连接变量、容器、循环、函数、文件、异常和测试。输入是科目与非负整数分钟数，输出是记录列表及汇总；数据保存在指定的本地 JSON 文件。只使用 Python 3.10+ 标准库，无需账号或第三方服务。

在本目录打开终端，先运行帮助，再用一份新记录练习：

```bash
python3 tracker.py --help
python3 tracker.py --file practice-records.json add Python 15
python3 tracker.py --file practice-records.json add 读书 10
python3 tracker.py --file practice-records.json add Python 5
python3 tracker.py --file practice-records.json list
python3 tracker.py --file practice-records.json total
python3 tracker.py --file practice-records.json total --subject Python
python3 -m unittest -v
```

总时长应为 30 分钟，Python 的合计为 20 分钟。继续添加会累积已有记录，不要为了对照示例而反复添加同一批数据。分钟数允许为零；负数、空科目、损坏的 JSON 和不符合字段要求的内容会报错。文件不存在时从空列表开始；已有文件损坏时保留其内容，不用空数据覆盖。

可以先不看 `tracker.py`，按下面顺序自己完成：

1. 用列表与字典写出三条记录，打印出来。
2. 用循环统计总分钟数和指定科目的分钟数。
3. 写出 `make_record(subject, minutes)` 与 `total_minutes(records, subject=None)`。
4. 用 UTF-8 与 JSON 保存、读取，再启动一次程序核对。
5. 处理无效输入和损坏文件。
6. 阅读 `test_tracker.py`，让自己的实现通过验收。已有 pytest 环境时也可运行 `python3 -m pytest -q`。

先解释每个函数的输入、输出和失败条件，再比较参考实现。测试数据位于独立系统临时目录，测试不会读取默认的学习记录。

浏览器练习页适合运行纯 Python 计算片段；浏览器里的文件属于运行时虚拟文件系统，不等于电脑磁盘文件，也不保证刷新后保留。上面的终端、参数和跨次保存练习请在本地完成。

本工具用于教学，保存时直接写入 JSON，没有事务、并发写入协调或自动备份。用练习数据完成验收，不把它当成生产数据存储程序。
