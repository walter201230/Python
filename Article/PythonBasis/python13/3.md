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

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-14-%E5%A4%9A%E8%BF%9B%E7%A8%8B%E8%BE%93%E5%87%BA%E7%BB%93%E6%9E%9C.gif)


## 2、把进程创建成类 ##

当然我们也可以把进程创建成一个类，如下面的例子，当进程 p 调用 start() 时，自动调用 run() 方法。


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
            print("当前时间: {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1


if __name__ == '__main__':
    p = ClockProcess(3)
    p.start()

```

输出结果如下：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-14-%E5%88%9B%E5%BB%BA%E8%BF%9B%E7%A8%8B%E7%B1%BB.gif)

## 3、daemon 属性 ##

想知道 daemon 属性有什么用，看下下面两个例子吧，一个加了 daemon 属性，一个没有加，对比输出的结果：

没有加 deamon 属性的例子：

```python
# -*- coding: UTF-8 -*-
import multiprocessing
import time


def worker(interval):
    print('工作开始时间：{0}'.format(time.ctime()))
    time.sleep(interval)
    print('工作结果时间：{0}'.format(time.ctime()))


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
    print('工作开始时间：{0}'.format(time.ctime()))
    time.sleep(interval)
    print('工作结果时间：{0}'.format(time.ctime()))


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
    print('工作开始时间：{0}'.format(time.ctime()))
    time.sleep(interval)
    print('工作结果时间：{0}'.format(time.ctime()))


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
    print('进程的名称：{0} ；进程的PID: {1} '.format(name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('进程 {0} 运行了 {1} 秒'.format(name, (end - start)))


if __name__ == '__main__':
    print('主进程的 PID：{0}'.format(os.getpid()))
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
    print('写进程的PID:{0}'.format(os.getpid()))
    for value in ['两点水', '三点水', '四点水']:
        print('写进 Queue 的值为：{0}'.format(value))
        q.put(value)
        time.sleep(random.random())


def read(q):
    # 读取数据进程
    print('读进程的PID:{0}'.format(os.getpid()))
    while True:
        value = q.get(True)
        print('从 Queue 读取的值为：{0}'.format(value))


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


