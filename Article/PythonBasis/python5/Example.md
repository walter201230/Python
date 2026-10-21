# 三、条件语句和循环语句综合实例 #

## 1、打印九九乘法表 ##

```python
# -*- coding: UTF-8 -*-

# 打印九九乘法表
for i in range(1, 10):
        for j in range(1, i+1):
            # 使用 f-string 直接在字符串前加 f，大括号里写表达式即可被求值并插入到字符串中
            print(f'{i}x{j}={i*j}\t', end='')
        print()
```

输出的结果:

```txt
1x1=1   
2x1=2   2x2=4   
3x1=3   3x2=6   3x3=9   
4x1=4   4x2=8   4x3=12  4x4=16  
5x1=5   5x2=10  5x3=15  5x4=20  5x5=25  
6x1=6   6x2=12  6x3=18  6x4=24  6x5=30  6x6=36  
7x1=7   7x2=14  7x3=21  7x4=28  7x5=35  7x6=42  7x7=49  
8x1=8   8x2=16  8x3=24  8x4=32  8x5=40  8x6=48  8x7=56  8x8=64  
9x1=9   9x2=18  9x3=27  9x4=36  9x5=45  9x6=54  9x7=63  9x8=72  9x9=81 
```


## 2、判断是否是闰年 ##

<!-- skip-ci -->
```python

# 判断是否是闰年

year = int(input("请输入一个年份: "))
if (year % 4) == 0 and (year % 100) != 0 or (year % 400) == 0:
    print(f'{year} 是闰年')
else:
     print(f'{year} 不是闰年')

```




<!-- content-completion-2026-10-22:start -->

## 补充讲解与自练

> 本节为本轮新增补充，以上原有文字、代码与例子逐字保留。

### 先把手工统计步骤写出来

我们准备统计学习时间。记录里可能有 `0`，也可能有录入错误的负数。先约定：零分钟允许保留，负数暂时跳过。那手工会怎么做？从零开始，逐条查看，只把符合要求的记录加进去。

```python
records = [15, 0, 10, -3]
total = 0
valid_count = 0
for minutes in records:
    if minutes < 0:
        continue
    total = total + minutes
    valid_count = valid_count + 1
print(total)
print(valid_count)
```

输出：

```text
25
3
```

别只看总数，沿着循环把每一步的 `minutes`、`total` 和 `valid_count` 写下来。零分钟虽然不增加合计，仍然是一条有效记录，所以有效条数是 `3`。

自己试两种边界：空列表应该得到 `0` 和 `0`；全是负数的列表也一样。如果把判断改成 `minutes <= 0`，合计可能没变，但条数会变。这说明输出中的某一个数字正确，并不等于程序完全符合需求。

这里跳过负数是这个练习的业务约定，不是所有程序都该悄悄跳过错误。学到异常处理时，我们会改成向调用方说明哪里不符合要求。

<!-- content-completion-2026-10-22:end -->
