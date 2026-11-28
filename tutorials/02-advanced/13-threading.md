# 第 13 章：线程与进程

# 前言 #

学编程，谁没有为线程折腾过啊。

# 目录 #


```
草根学 Python（十三）线程和进程
│
├── 线程与进程
│
├── 多线程编程
│   ├── 1、线程的创建
│   ├── 2、线程合并（join 方法）
│   ├── 3、线程同步与互斥锁
│   ├── 4、Condition 条件变量
│   ├── 5、线程间通信
│   └── 6、后台线程
│
└── 进程
    ├── 1、类 Process
    ├── 2、把进程创建成类
    ├── 3、daemon 属性
    ├── 4、join 方法
    ├── 5、Pool
    └── 6、进程间通信
```

# 线程与进程 #

线程与进程是操作系统里面的术语，简单来讲，每一个应用程序都有一个自己的进程。

操作系统会为这些进程分配一些执行资源，例如内存空间等。

在进程中，又可以创建一些线程，他们共享这些内存空间，并由操作系统调用，以便并行计算。

我们都知道现代操作系统比如 Mac OS X，UNIX，Linux，Windows 等可以同时运行多个任务。

打个比方，你一边在用浏览器上网，一边在听敲代码，一边用 Markdown 写博客，这就是多任务，至少同时有 3 个任务正在运行。

当然还有很多任务悄悄地在后台同时运行着，只是桌面上没有显示而已。

对于操作系统来说，一个任务就是一个进程（Process），比如打开一个浏览器就是启动一个浏览器进程，打开 PyCharm 就是一个启动了一个 PtCharm 进程，打开 Markdown 就是启动了一个 Md 的进程。 

虽然现在多核 CPU 已经非常普及了。

可是由于 CPU 执行代码都是顺序执行的，这时候我们就会有疑问，单核 CPU 是怎么执行多任务的呢？

其实就是操作系统轮流让各个任务交替执行，任务 1 执行 0.01 秒，切换到任务 2 ，任务 2 执行 0.01 秒，再切换到任务 3 ，执行 0.01秒……这样反复执行下去。

表面上看，每个任务都是交替执行的，但是，由于 CPU的执行速度实在是太快了，我们肉眼和感觉上没法识别出来，就像所有任务都在同时执行一样。

真正的并行执行多任务只能在多核 CPU 上实现，但是，由于任务数量远远多于 CPU 的核心数量，所以，操作系统也会自动把很多任务轮流调度到每个核心上执行。


有些进程不仅仅只是干一件事的啊，比如浏览器，我们可以播放时视频，播放音频，看文章，编辑文章等等，其实这些都是在浏览器进程中的子任务。在一个进程内部，要同时干多件事，就需要同时运行多个“子任务”，我们把进程内的这些“子任务”称为线程（Thread）。

由于每个进程至少要干一件事，所以，一个进程至少有一个线程。

当然，一个进程也可以有多个线程，多个线程可以同时执行，多线程的执行方式和多进程是一样的，也是由操作系统在多个线程之间快速切换，让每个线程都短暂地交替运行，看起来就像同时执行一样。

那么在 Python 中我们要同时执行多个任务怎么办？

有两种解决方案：

一种是启动多个进程，每个进程虽然只有一个线程，但多个进程可以一块执行多个任务。

还有一种方法是启动一个进程，在一个进程内启动多个线程，这样，多个线程也可以一块执行多个任务。

当然还有第三种方法，就是启动多个进程，每个进程再启动多个线程，这样同时执行的任务就更多了，当然这种模型更复杂，实际很少采用。

总结一下就是，多任务的实现有3种方式：

* 多进程模式；
* 多线程模式；
* 多进程+多线程模式。

同时执行多个任务通常各个任务之间并不是没有关联的，而是需要相互通信和协调，有时，任务 1 必须暂停等待任务 2 完成后才能继续执行，有时，任务 3 和任务 4 又不能同时执行，所以，多进程和多线程的程序的复杂度要远远高于我们前面写的单进程单线程的程序。

因为复杂度高，调试困难，所以，不是迫不得已，我们也不想编写多任务。

但是，有很多时候，没有多任务还真不行。

想想在电脑上看电影，就必须由一个线程播放视频，另一个线程播放音频，否则，单线程实现的话就只能先把视频播放完再播放音频，或者先把音频播放完再播放视频，这显然是不行的。




## 先确认哪些任务可以独立完成

讨论线程与进程之前，先把任务拆清楚：每条记录的计算是否互相依赖？结果需要按输入顺序展示，还是处理完一条就展示一条？这些约定会影响写法。

下面的线程池示例用于本地 Python。浏览器里的 Python 运行环境不提供与本机相同的线程和进程能力，请在本地终端运行这一段。

```python no-run
from concurrent.futures import ThreadPoolExecutor


def double_minutes(minutes):
    return minutes * 2


with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(double_minutes, [15, 0, 10]))
print(results)
```

输出：

```text
[30, 0, 20]
```

这个 `map` 的结果按输入顺序取出，不代表任务内部也严格按这个顺序执行。自己把输入换成空列表，结果应该是 `[]`。

这个任务太小，使用线程池主要是为了观察接口，不能用它证明线程一定更快。比较性能要固定工作量、运行环境和测量方法；GIL 的讨论也要注明解释器与构建方式，不能把某一种 CPython 配置的结论套到所有 Python 环境。先学会辨认计算、等待和共享状态，再选择工具。

# 多线程编程 #

其实创建线程之后，线程并不是始终保持一个状态的，其状态大概如下：

* New 创建
* Runnable 就绪。等待调度
* Running 运行
* Blocked 阻塞。阻塞可能在 Wait Locked Sleeping
* Dead 消亡

线程有着不同的状态，也有不同的类型。大致可分为：

* 主线程
* 子线程
* 守护线程（后台线程）
* 前台线程

简单了解完这些之后，我们开始看看具体的代码使用了。

## 1、线程的创建 ##

Python 提供两个模块进行多线程的操作，分别是 `thread` 和 `threading`

前者是比较低级的模块，用于更底层的操作，一般应用级别的开发不常用。

因此，我们使用 `threading` 来举个例子：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import threading


class MyThread(threading.Thread):
    def run(self):
        for i in range(5):
            print(f'thread {self.name}, @number: {i}')
            time.sleep(1)


def main():
    print("Start main threading")

    # 创建三个线程
    threads = [MyThread() for i in range(3)]
    # 启动三个线程
    for t in threads:
        t.start()

    print("End Main threading")


if __name__ == '__main__':
    main()

```

运行结果：

```txt
Start main threading
thread Thread-1, @number: 0
thread Thread-2, @number: 0
thread Thread-3, @number: 0
End Main threading
thread Thread-2, @number: 1
thread Thread-1, @number: 1
thread Thread-3, @number: 1
thread Thread-1, @number: 2
thread Thread-3, @number: 2
thread Thread-2, @number: 2
thread Thread-2, @number: 3
thread Thread-3, @number: 3
thread Thread-1, @number: 3
thread Thread-3, @number: 4
thread Thread-2, @number: 4
thread Thread-1, @number: 4
```

注意喔，这里不同的环境输出的结果肯定是不一样的。

## 2、线程合并（join方法） ##

上面的示例打印出来的结果来看，主线程结束后，子线程还在运行。那么我们需要主线程要等待子线程运行完后，再退出，要怎么办呢？

这时候，就需要用到 `join` 方法了。

在上面的例子，新增一段代码，具体如下：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import threading


class MyThread(threading.Thread):
    def run(self):
        for i in range(5):
            print(f'thread {self.name}, @number: {i}')
            time.sleep(1)


def main():
    print("Start main threading")

    # 创建三个线程
    threads = [MyThread() for i in range(3)]
    # 启动三个线程
    for t in threads:
        t.start()

    # 一次让新创建的线程执行 join
    for t in threads:
        t.join()

    print("End Main threading")


if __name__ == '__main__':
    main()

```


从打印的结果，可以清楚看到，相比上面示例打印出来的结果，主线程是在等待子线程运行结束后才结束的。

```txt
Start main threading
thread Thread-1, @number: 0
thread Thread-2, @number: 0
thread Thread-3, @number: 0
thread Thread-1, @number: 1
thread Thread-3, @number: 1
thread Thread-2, @number: 1
thread Thread-2, @number: 2
thread Thread-1, @number: 2
thread Thread-3, @number: 2
thread Thread-2, @number: 3
thread Thread-1, @number: 3
thread Thread-3, @number: 3
thread Thread-3, @number: 4
thread Thread-2, @number: 4
thread Thread-1, @number: 4
End Main threading

```
## 3、线程同步与互斥锁 ##

使用线程加载获取数据，通常都会造成数据不同步的情况。当然，这时候我们可以给资源进行加锁，也就是访问资源的线程需要获得锁才能访问。

其中 `threading` 模块给我们提供了一个 Lock 功能。

<!-- skip-ci -->
```python
lock = threading.Lock()
```

在线程中获取锁

<!-- skip-ci -->
```python
lock.acquire()
```

使用完成后，我们肯定需要释放锁

<!-- skip-ci -->
```python
lock.release()
```

当然为了支持在同一线程中多次请求同一资源，Python 提供了可重入锁（RLock）。RLock 内部维护着一个 Lock 和一个 counter 变量，counter 记录了 acquire 的次数，从而使得资源可以被多次 require。直到一个线程所有的 acquire 都被 release，其他的线程才能获得资源。

那么怎么创建重入锁呢？也是一句代码的事情：

<!-- skip-ci -->
```python
r_lock = threading.RLock()
```

## 4、Condition 条件变量 ##

实用锁可以达到线程同步，但是在更复杂的环境，需要针对锁进行一些条件判断。

Python 提供了 Condition 对象。

**使用 Condition 对象可以在某些事件触发或者达到特定的条件后才处理数据，Condition 除了具有 Lock 对象的 acquire 方法和 release 方法外，还提供了 wait 和 notify 方法。**

线程首先 acquire 一个条件变量锁。如果条件不足，则该线程 wait，如果满足就执行线程，甚至可以 notify 其他线程。其他处于 wait 状态的线程接到通知后会重新判断条件。

其中条件变量可以看成不同的线程先后 acquire 获得锁，如果不满足条件，可以理解为被扔到一个（ Lock 或 RLock ）的 waiting 池。直到其他线程 notify 之后再重新判断条件。不断的重复这一过程，从而解决复杂的同步问题。

![Condition 条件变量](../assets/diagrams/condition-flow.svg)

该模式常用于生产者消费者模式，具体看看下面在线购物买家和卖家的示例：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import threading, time


class Consumer(threading.Thread):
    def __init__(self, cond, name):
        # 初始化
        super(Consumer, self).__init__()
        self.cond = cond
        self.name = name

    def run(self):
        # 确保先运行Seeker中的方法
        time.sleep(1)
        self.cond.acquire()
        print(self.name + ': 我这两件商品一起买，可以便宜点吗')
        self.cond.notify()
        self.cond.wait()
        print(self.name + ': 我已经提交订单了，你修改下价格')
        self.cond.notify()
        self.cond.wait()
        print(self.name + ': 收到，我支付成功了')
        self.cond.notify()
        self.cond.release()
        print(self.name + ': 等待收货')


class Producer(threading.Thread):
    def __init__(self, cond, name):
        super(Producer, self).__init__()
        self.cond = cond
        self.name = name

    def run(self):
        self.cond.acquire()
        # 释放对琐的占用，同时线程挂起在这里，直到被 notify 并重新占有琐。
        self.cond.wait()
        print(self.name + ': 可以的，你提交订单吧')
        self.cond.notify()
        self.cond.wait()
        print(self.name + ': 好了，已经修改了')
        self.cond.notify()
        self.cond.wait()
        print(self.name + ': 嗯，收款成功，马上给你发货')
        self.cond.release()
        print(self.name + ': 发货商品')


cond = threading.Condition()
consumer = Consumer(cond, '买家（两点水）')
producer = Producer(cond, '卖家（三点水）')
consumer.start()
producer.start()

```

输出的结果如下：

```txt
买家（两点水）: 我这两件商品一起买，可以便宜点吗
卖家（三点水）: 可以的，你提交订单吧
买家（两点水）: 我已经提交订单了，你修改下价格
卖家（三点水）: 好了，已经修改了
买家（两点水）: 收到，我支付成功了
买家（两点水）: 等待收货
卖家（三点水）: 嗯，收款成功，马上给你发货
卖家（三点水）: 发货商品
```

## 5、线程间通信 ##

如果程序中有多个线程，这些线程避免不了需要相互通信的。那么我们怎样在这些线程之间安全地交换信息或数据呢？

从一个线程向另一个线程发送数据最安全的方式可能就是使用 queue 库中的队列了。创建一个被多个线程共享的 `Queue` 对象，这些线程通过使用 `put()` 和 `get()` 操作来向队列中添加或者删除元素。

```python
# -*- coding: UTF-8 -*-
from queue import Queue
from threading import Thread


def write(q):
    # 写数据进程
    for value in ['两点水', '三点水', '四点水']:
        print(f'写进 Queue 的值为：{value}')
        q.put(value)
    q.put(None)  # 写完放一个结束标记


def read(q):
    # 读取数据进程
    while True:
        value = q.get(True)
        if value is None:  # 读到结束标记就退出
            break
        print(f'从 Queue 读取的值为：{value}')


if __name__ == '__main__':
    q = Queue()
    t1 = Thread(target=write, args=(q,))
    t2 = Thread(target=read, args=(q,))
    t1.start()
    t2.start()
```

输出的结果如下：

```txt
写进 Queue 的值为：两点水
写进 Queue 的值为：三点水
从 Queue 读取的值为：两点水
写进 Queue 的值为：四点水
从 Queue 读取的值为：三点水
从 Queue 读取的值为：四点水
```

Python 还提供了 Event 对象用于线程间通信，它是由线程设置的信号标志，如果信号标志位真，则其他线程等待直到信号接触。

Event 对象实现了简单的线程通信机制，它提供了设置信号，清楚信号，等待等用于实现线程间的通信。

* 设置信号

使用 Event 的 `set()` 方法可以设置 Event 对象内部的信号标志为真。Event 对象提供了 `is_set()` 方法来判断其内部信号标志的状态。当使用 event 对象的 `set()` 方法后，`is_set()` 方法返回真

* 清除信号

使用 Event 对象的 `clear()` 方法可以清除 Event 对象内部的信号标志，即将其设为假，当使用 Event 的 clear 方法后，is_set() 方法返回假

*  等待

Event 对象 wait 的方法只有在内部信号为真的时候才会很快的执行并完成返回。当 Event 对象的内部信号标志位假时，则 wait 方法一直等待到其为真时才返回。

> 旧代码里常把 `is_set()` 写成 `isSet()`，读取线程名写成 `getName()`。这两个旧名称从 Python 3.10 起已弃用，运行时会出现 DeprecationWarning，所以下面的示例使用 `is_set()` 和线程的 `name` 属性。

示例：

```python
# -*- coding: UTF-8 -*-

import threading


class mThread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)

    def run(self):
        # 使用全局Event对象
        global event
        # 判断Event对象内部信号标志
        if event.is_set():
            event.clear()
            # 加 timeout 兜底：is_set() 判断与 clear() 之间不是原子操作，
            # 两个线程可能都通过判断、都进 wait()，而只有一个 set() 来唤醒
            event.wait(timeout=1)
            print(self.name)
        else:
            print(self.name)
            # 设置Event对象内部信号标志
            event.set()

# 生成Event对象
event = threading.Event()
# 设置Event对象内部信号标志
event.set()
t1 = []
for i in range(10):
    t = mThread(str(i))
    # 生成线程列表
    t1.append(t)

for i in t1:
    # 运行线程
    i.start()

```


输出的结果如下：

```txt
1
0
3
2
5
4
7
6
9
8
```


## 6、后台线程 ##

默认情况下，主线程退出之后，即使子线程没有 join。那么主线程结束后，子线程也依然会继续执行。如果希望主线程退出后，其子线程也退出而不再执行，则需要设置子线程为后台线程。Python 提供了 `daemon` 属性，在 `start()` 之前把它设为 `True` 即可。

> 旧代码里常写成 `setDaemon(True)`，这个方法从 Python 3.10 起已弃用。

# 进程 #

Python 中的多线程其实并不是真正的多线程，如果想要充分地使用多核 CPU 的资源，在 Python 中大部分情况需要使用多进程。

Python 提供了非常好用的多进程包 multiprocessing，只需要定义一个函数，Python 会完成其他所有事情。

借助这个包，可以轻松完成从单进程到并发执行的转换。multiprocessing 支持子进程、通信和共享数据、执行不同形式的同步，提供了 Process、Queue、Pipe、Lock 等组件。


## 1、类 Process ##

创建进程的类：`Process([group [, target [, name [, args [, kwargs]]]]])`

* target 表示调用对象
* args 表示调用对象的位置参数元组
* kwargs表示调用对象的字典
* name为别名
* group实质上不使用

下面看一个创建函数并将其作为多个进程的例子：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import multiprocessing
import time


def worker(interval, name):
    print(name + '【start】')
    time.sleep(interval)
    print(name + '【end】')


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=worker, args=(2, '两点水1'))
    p2 = multiprocessing.Process(target=worker, args=(3, '两点水2'))
    p3 = multiprocessing.Process(target=worker, args=(4, '两点水3'))

    p1.start()
    p2.start()
    p3.start()

    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    print("END!!!!!!!!!!!!!!!!!")

```

输出的结果：

```
The number of CPU is:4
child   p.name:Process-3    p.id7600
child   p.name:Process-2    p.id5560
child   p.name:Process-1    p.id7716
END!!!!!!!!!!!!!!!!!
两点水 1【start】
两点水 2【start】
两点水 3【start】
两点水 1【end】
两点水 2【end】
两点水 3【end】

Process finished with exit code 0
```


## 2、把进程创建成类 ##

当然我们也可以把进程创建成一个类，如下面的例子，当进程 p 调用 start() 时，自动调用 run() 方法。


<!-- skip-ci -->
```python
# -*- coding: UTF-8 -*-

import multiprocessing
import time


class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def run(self):
        n = 5
        while n > 0:
            print(f"当前时间: {time.ctime()}")
            time.sleep(self.interval)
            n -= 1


if __name__ == '__main__':
    p = ClockProcess(3)
    p.start()

```

输出结果如下：

```
当前时间: Mon Oct  9 17:26:16 2017
当前时间: Mon Oct  9 17:26:19 2017
当前时间: Mon Oct  9 17:26:22 2017
当前时间: Mon Oct  9 17:26:25 2017
当前时间: Mon Oct  9 17:26:28 2017

Process finished with exit code 0
```

## 3、daemon 属性 ##

想知道 daemon 属性有什么用，看下下面两个例子吧，一个加了 daemon 属性，一个没有加，对比输出的结果：

没有加 deamon 属性的例子：

```python
# -*- coding: UTF-8 -*-
import multiprocessing
import time


def worker(interval):
    print(f'工作开始时间：{time.ctime()}')
    time.sleep(interval)
    print(f'工作结果时间：{time.ctime()}')


if __name__ == '__main__':
    p = multiprocessing.Process(target=worker, args=(3,))
    p.start()
    print('【EMD】')

```

输出结果：

```txt
【EMD】
工作开始时间：Mon Oct  9 17:47:06 2017
工作结果时间：Mon Oct  9 17:47:09 2017
```

在上面示例中，进程 p 添加 daemon 属性：

```python
# -*- coding: UTF-8 -*-

import multiprocessing
import time


def worker(interval):
    print(f'工作开始时间：{time.ctime()}')
    time.sleep(interval)
    print(f'工作结果时间：{time.ctime()}')


if __name__ == '__main__':
    p = multiprocessing.Process(target=worker, args=(3,))
    p.daemon = True
    p.start()
    print('【EMD】')
```

输出结果：

```txt
【EMD】
```


根据输出结果可见，如果在子进程中添加了 daemon 属性，那么当主进程结束的时候，子进程也会跟着结束。所以没有打印子进程的信息。


## 4、join 方法 ##

结合上面的例子继续，如果我们想要让子线程执行完该怎么做呢？

那么我们可以用到 join 方法，join 方法的主要作用是：阻塞当前进程，直到调用 join 方法的那个进程执行完，再继续执行当前进程。

因此看下加了 join 方法的例子：

```python
import multiprocessing
import time


def worker(interval):
    print(f'工作开始时间：{time.ctime()}')
    time.sleep(interval)
    print(f'工作结果时间：{time.ctime()}')


if __name__ == '__main__':
    p = multiprocessing.Process(target=worker, args=(3,))
    p.daemon = True
    p.start()
    p.join()
    print('【EMD】')
```

输出的结果：

```txt
工作开始时间：Tue Oct 10 11:30:08 2017
工作结果时间：Tue Oct 10 11:30:11 2017
【EMD】
```

## 5、Pool ##

如果需要很多的子进程，难道我们需要一个一个的去创建吗？

当然不用，我们可以使用进程池的方法批量创建子进程。

例子如下：

```python
# -*- coding: UTF-8 -*-

from multiprocessing import Pool
import os, time, random


def long_time_task(name):
    print(f'进程的名称：{name} ；进程的PID: {os.getpid()} ')
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print(f'进程 {name} 运行了 {end - start} 秒')


if __name__ == '__main__':
    print(f'主进程的 PID：{os.getpid()}')
    p = Pool(4)
    for i in range(6):
        p.apply_async(long_time_task, args=(i,))
    p.close()
    # 等待所有子进程结束后在关闭主进程
    p.join()
    print('【End】')
```

输出的结果如下：

```txt
主进程的 PID：7256
进程的名称：0 ；进程的PID: 1492
进程的名称：1 ；进程的PID: 12232
进程的名称：2 ；进程的PID: 4332
进程的名称：3 ；进程的PID: 11604
进程 2 运行了 0.6500370502471924 秒
进程的名称：4 ；进程的PID: 4332
进程 1 运行了 1.0830621719360352 秒
进程的名称：5 ；进程的PID: 12232
进程 5 运行了 0.029001712799072266 秒
进程 4 运行了 0.9720554351806641 秒
进程 0 运行了 2.3181326389312744 秒
进程 3 运行了 2.5331451892852783 秒
【End】
```

这里有一点需要注意： `Pool` 对象调用 `join()` 方法会等待所有子进程执行完毕，调用 `join()` 之前必须先调用 `close()` ，调用`close()` 之后就不能继续添加新的 Process 了。

请注意输出的结果，子进程 0，1，2，3是立刻执行的，而子进程 4 要等待前面某个子进程完成后才执行，这是因为 Pool 的默认大小在我的电脑上是 4，因此，最多同时执行 4 个进程。这是 Pool 有意设计的限制，并不是操作系统的限制。如果改成：

<!-- skip-ci -->
```python
p = Pool(5)
```

就可以同时跑 5 个进程。



## 6、进程间通信 ##

Process 之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。Python 的 multiprocessing 模块包装了底层的机制，提供了Queue、Pipes 等多种方式来交换数据。

以 Queue 为例，在父进程中创建两个子进程，一个往 Queue 里写数据，一个从 Queue 里读数据：

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from multiprocessing import Process, Queue
import os, time, random


def write(q):
    # 写数据进程
    print(f'写进程的PID:{os.getpid()}')
    for value in ['两点水', '三点水', '四点水']:
        print(f'写进 Queue 的值为：{value}')
        q.put(value)
        time.sleep(random.random())


def read(q):
    # 读取数据进程
    print(f'读进程的PID:{os.getpid()}')
    while True:
        value = q.get(True)
        print(f'从 Queue 读取的值为：{value}')


if __name__ == '__main__':
    # 父进程创建 Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程 pw
    pw.start()
    # 启动子进程pr
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr 进程里是死循环，无法等待其结束，只能强行终止
    pr.terminate()

```

输出的结果为：

```txt
读进程的PID:13208
写进程的PID:10864
写进 Queue 的值为：两点水
从 Queue 读取的值为：两点水
写进 Queue 的值为：三点水
从 Queue 读取的值为：三点水
写进 Queue 的值为：四点水
从 Queue 读取的值为：四点水
```
