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
            print('thread {}, @number: {}'.format(self.name, i))
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
            print('thread {}, @number: {}'.format(self.name, i))
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

```python
lock = threading.Lock()
```

在线程中获取锁

```python
lock.acquire()
```

使用完成后，我们肯定需要释放锁

```python
lock.release()
```

当然为了支持在同一线程中多次请求同一资源，Python 提供了可重入锁（RLock）。RLock 内部维护着一个 Lock 和一个 counter 变量，counter 记录了 acquire 的次数，从而使得资源可以被多次 require。直到一个线程所有的 acquire 都被 release，其他的线程才能获得资源。

那么怎么创建重入锁呢？也是一句代码的事情：

```python
r_lock = threading.RLock()
```

## 4、Condition 条件变量 ##

实用锁可以达到线程同步，但是在更复杂的环境，需要针对锁进行一些条件判断。

Python 提供了 Condition 对象。

**使用 Condition 对象可以在某些事件触发或者达到特定的条件后才处理数据，Condition 除了具有 Lock 对象的 acquire 方法和 release 方法外，还提供了 wait 和 notify 方法。**

线程首先 acquire 一个条件变量锁。如果条件不足，则该线程 wait，如果满足就执行线程，甚至可以 notify 其他线程。其他处于 wait 状态的线程接到通知后会重新判断条件。

其中条件变量可以看成不同的线程先后 acquire 获得锁，如果不满足条件，可以理解为被扔到一个（ Lock 或 RLock ）的 waiting 池。直到其他线程 notify 之后再重新判断条件。不断的重复这一过程，从而解决复杂的同步问题。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-14-Condition.png)

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

isRead = True


def write(q):
    # 写数据进程
    for value in ['两点水', '三点水', '四点水']:
        print('写进 Queue 的值为：{0}'.format(value))
        q.put(value)


def read(q):
    # 读取数据进程
    while isRead:
        value = q.get(True)
        print('从 Queue 读取的值为：{0}'.format(value))


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

使用 Event 的 `set()` 方法可以设置 Event 对象内部的信号标志为真。Event 对象提供了 `isSe()` 方法来判断其内部信号标志的状态。当使用 event 对象的 `set()` 方法后，`isSet()` 方法返回真

* 清除信号

使用 Event 对象的 `clear()` 方法可以清除 Event 对象内部的信号标志，即将其设为假，当使用 Event 的 clear 方法后，isSet() 方法返回假

*  等待

Event 对象 wait 的方法只有在内部信号为真的时候才会很快的执行并完成返回。当 Event 对象的内部信号标志位假时，则 wait 方法一直等待到其为真时才返回。

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
        if event.isSet():
            event.clear()
            event.wait()
            print(self.getName())
        else:
            print(self.getName())
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

默认情况下，主线程退出之后，即使子线程没有 join。那么主线程结束后，子线程也依然会继续执行。如果希望主线程退出后，其子线程也退出而不再执行，则需要设置子线程为后台线程。Python 提供了 `setDeamon` 方法。


