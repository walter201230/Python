# 异步编程：async/await 让一个线程同时等一百件事

各位写过爬虫没有？随手写一段：

```python
import time


def fake_get(url):
    time.sleep(0.01)
    return f'GOT {url}'


def main():
    urls = [f'https://example.com/{i}' for i in range(5)]
    start = time.perf_counter()
    results = []
    for u in urls:
        results.append(fake_get(u))
    cost = time.perf_counter() - start
    print(f'拿到 {len(results)} 个，用了 {cost:.3f} 秒')


main()
```

输出大致是这样：

```
拿到 5 个，用了 0.05 秒
```

每个请求假装耗时 0.01 秒，5 个串起来就是 0.05 秒。如果是真实的网络请求，每个 200 毫秒，100 个串起来就是 20 秒，慢得想骂人。

「那好办，开线程嘛！」有童鞋立刻反应过来，「100 个 URL 就开 100 个线程，一起跑。」

线程当然能解决问题。但开 100 个线程是不是有点奢侈？这 100 个线程 99% 的时间都在干同一件事：等网络包回来。本质上这是个等待问题，不是个计算问题。为了「等」而开 100 个操作系统级的线程，CPU 不开心，内存也不开心。

而且线程一多，「锁」、「竞态」、「死锁」这些老朋友就会一个一个找上门。你只是想抓个网页，怎么忽然要去研究操作系统了？

Python 给了我们另一条路：`asyncio` 。它的卖点很直白——**一个线程，同时等一百件事**。各位听到这句话第一反应肯定是：「这不科学吧，单线程怎么同时做一百件事？」

这就是这一章要回答的问题。


## 直觉对比：串行 5 秒 vs 并发 1 秒

先不讲原理，先看效果。下面这段是「正经的」串行代码，三件事各等 1 秒：

<!-- skip-ci -->
```python
import time


def task(name):
    time.sleep(1)
    return f'{name} 完成'


start = time.perf_counter()
r1 = task('打卡')
r2 = task('查询')
r3 = task('上传')
cost = time.perf_counter() - start
print(r1, r2, r3)
print(f'总共 {cost:.2f} 秒')
```

跑出来：

```
打卡 完成 查询 完成 上传 完成
总共 3.01 秒
```

一秒一秒老老实实排队。这没什么好说的。

接下来换成异步版本：

<!-- skip-ci -->
```python
import asyncio
import time


async def task(name):
    await asyncio.sleep(1)
    return f'{name} 完成'


async def main():
    start = time.perf_counter()
    r1, r2, r3 = await asyncio.gather(
        task('打卡'),
        task('查询'),
        task('上传'),
    )
    cost = time.perf_counter() - start
    print(r1, r2, r3)
    print(f'总共 {cost:.2f} 秒')


asyncio.run(main())
```

跑出来：

```
打卡 完成 查询 完成 上传 完成
总共 1.00 秒
```

3 秒变 1 秒，三件事居然真的「同时」完成了。各位先别管 `async` 、 `await` 、 `gather` 这些词是什么意思，先记住一个事实：**`asyncio.sleep(1)` 在一个协程里等的时候，另一个协程可以去用 CPU 干自己的活**，三个协程的等待是重叠的，所以总时间就是最长那一个，而不是三者之和。

这就是 `asyncio` 的核心魔法。它没有偷偷开线程，也没有把 CPU 加速。它做的事很朴素：**当某个协程在等 IO 的时候，让出 CPU 给其他协程，等回来再继续**。

讲到这里，各位心里应该有了点直觉。下面我们一步一步把这套语法拆开来看。


## 第一个 async 函数：和普通函数差在哪

普通函数长这样：

```python
def hello():
    return '两点水好'


print(hello())
```

输出：

```
两点水好
```

加一个 `async` 关键字，就成了「协程函数」（coroutine function）：

```python
async def hello():
    return '两点水好'


print(hello())
```

输出：

```
<coroutine object hello at 0x...>
RuntimeWarning: coroutine 'hello' was never awaited
```

各位看出区别了吗？同样是 `print(hello())` ，普通函数返回的是字符串 `'水哥好'` ，协程函数返回的却是一个 **协程对象**——一个 `<coroutine object>` ，而不是字符串。

更要命的是，Python 还甩了一句警告：「这协程从来没被 await 过」（coroutine was never awaited）。

这是什么意思？关键的认知就在这里：

- `async def` 定义的不是一个「会立刻跑的函数」
- 调用 `async def` 定义的函数，**它根本没跑**，只是给你返回一个「待执行的任务清单」

打个比方，普通函数 `hello()` 像是「派人去执行任务，立刻拿到结果」。而协程函数 `hello()` 像是「写一张任务单递给你，至于什么时候去做、谁去做，另说」。

这张「任务单」就是协程对象。它必须被 **await** ，或者扔给事件循环去执行，里面的代码才会真正跑起来。


## await：让协程跑起来

那怎么让这张任务单真的执行？用 `await` ：

<!-- skip-ci -->
```python
import asyncio


async def hello():
    return '两点水好'


async def main():
    result = await hello()
    print(result)


asyncio.run(main())
```

输出：

```
两点水好
```

这下拿到字符串了。`await hello()` 的语义可以读成「请帮我把 `hello()` 这张任务单完成，然后把结果给我」。

但这里有个非常重要的限制：**`await` 只能写在 `async def` 函数体内部**。各位试试在普通函数里写 `await` ，Python 会告诉你 `SyntaxError: 'await' outside async function` 。

「那我想在普通脚本里调用一个 `async def` 怎么办？」这就要用到下一个角色——`asyncio.run()` 。


## asyncio.run()：进入异步世界的大门

`asyncio.run()` 是同步代码和异步代码之间的「门」。它接收一个协程对象，启动一个「事件循环」（event loop），把协程跑完，然后关掉事件循环：

<!-- skip-ci -->
```python
import asyncio


async def main():
    print('我在异步世界里')
    await asyncio.sleep(0.01)
    print('我又在异步世界里')


asyncio.run(main())
```

输出：

```
我在异步世界里
我又在异步世界里
```

这里隐含了一个非常重要的设计：**整个程序里通常只有一个事件循环，由 `asyncio.run()` 启动**。所有的协程都跑在这个循环里。各位可以这么想象：

- 同步世界 → 一条直直的路，一步接一步
- 异步世界 → 一个调度中心（事件循环），里面挂着一堆协程，谁能跑就让谁跑

`asyncio.run()` 就是从同步世界踏进异步世界的入口。一个程序只该调用一次（嵌套调用会报错）。

到此为止，各位掌握了三个基础概念：`async def` 定义协程函数、 `await` 等协程结果、 `asyncio.run()` 启动事件循环。这三个东西凑齐了，你已经能写一个最小可跑的异步程序。


## 协程对象不 await 会怎样

刚才警告里说的「coroutine was never awaited」，到底有多严重？我们来看一段非常容易踩坑的代码：

<!-- skip-ci -->
```python
import asyncio


async def punch():
    print('两点水开始打卡')
    await asyncio.sleep(0.01)
    print('两点水打卡完成')


async def main():
    punch()
    print('main 跑完了')


asyncio.run(main())
```

输出：

```
main 跑完了
RuntimeWarning: coroutine 'punch' was never awaited
```

各位有没有看出哪里不对？`punch()` 那一行根本没打印「两点水开始打卡」。`punch()` 只是创建了一个协程对象然后被丢掉了，里面的代码一行都没跑。

这是 `asyncio` 最经典的陷阱之一：**忘了 `await`** 。同步世界里，写函数名加括号就等于执行；异步世界里，写函数名加括号只是「拿到一张任务单」，不写 `await` 就等于把任务单扔垃圾桶。

正确的写法当然是：

<!-- skip-ci -->
```python
import asyncio


async def punch():
    print('两点水开始打卡')
    await asyncio.sleep(0.01)
    print('两点水打卡完成')


async def main():
    await punch()
    print('main 跑完了')


asyncio.run(main())
```

输出：

```
两点水开始打卡
两点水打卡完成
main 跑完了
```

记住这句话：**协程不 await，等于没写**。


## 一次等多个：asyncio.gather

到这里，各位会写串行的异步代码了。但是回到最开始那个例子——3 件事 1 秒搞定——这种「同时等多个」的能力是怎么实现的？答案是 `asyncio.gather` 。

先看错误的写法：

<!-- skip-ci -->
```python
import asyncio
import time


async def task(name):
    await asyncio.sleep(0.5)
    return f'{name} 完成'


async def main():
    start = time.perf_counter()
    r1 = await task('A')
    r2 = await task('B')
    r3 = await task('C')
    cost = time.perf_counter() - start
    print(r1, r2, r3)
    print(f'用了 {cost:.2f} 秒')


asyncio.run(main())
```

输出：

```
A 完成 B 完成 C 完成
用了 1.50 秒
```

「不是说异步快吗？怎么还是 1.5 秒？」

各位仔细看这段代码：`await task('A')` 写在前面，意思是「等 A 跑完，再继续」。一个 `await` 一个 `await` 串起来，本质上是串行的。`async/await` 不会自动并发。

要并发，得明确告诉事件循环「这几件事可以一起开始」。`asyncio.gather` 就是干这个的：

<!-- skip-ci -->
```python
import asyncio
import time


async def task(name):
    await asyncio.sleep(0.5)
    return f'{name} 完成'


async def main():
    start = time.perf_counter()
    r1, r2, r3 = await asyncio.gather(
        task('A'),
        task('B'),
        task('C'),
    )
    cost = time.perf_counter() - start
    print(r1, r2, r3)
    print(f'用了 {cost:.2f} 秒')


asyncio.run(main())
```

输出：

```
A 完成 B 完成 C 完成
用了 0.50 秒
```

这才是各位想要的「并发」效果。`asyncio.gather` 接收任意多个协程，把它们一起扔给事件循环，等全部完成之后再把结果按顺序打包返回。

这里有几个要点要划重点：

- `gather` 返回的是 **所有结果的列表**，顺序和你传进去的顺序一致
- 任意一个协程抛异常，默认情况下整个 `gather` 都会抛
- 传进去的可以是协程，也可以是 Task 对象（下面会讲）

`gather` 是 `asyncio` 里出现频率最高的函数之一。各位看到「同时跑多个」的需求，第一反应就该是它（或者后面要讲的 `TaskGroup`）。


## Task：把协程「派出去」

上面的 `gather` 用得很爽，但有时候我们想要更细的控制：「先把任务派出去，让它在后台跑着，我先去干别的事，需要的时候再回来收结果」。

这种「派出去」的动作，对应的概念叫 **Task** ，由 `asyncio.create_task()` 创建：

<!-- skip-ci -->
```python
import asyncio
import time


async def slow_job(name, delay):
    await asyncio.sleep(delay)
    return f'{name} 完成'


async def main():
    start = time.perf_counter()
    t1 = asyncio.create_task(slow_job('A', 0.3))
    t2 = asyncio.create_task(slow_job('B', 0.5))
    print('两个任务已经派出去了，main 还能干别的')
    await asyncio.sleep(0.1)
    print('我先打个卡')
    r1 = await t1
    r2 = await t2
    cost = time.perf_counter() - start
    print(r1, r2)
    print(f'用了 {cost:.2f} 秒')


asyncio.run(main())
```

输出：

```
两个任务已经派出去了，main 还能干别的
我先打个卡
A 完成 B 完成
用了 0.50 秒
```

各位注意时间——0.5 秒，不是 0.3 + 0.5 = 0.8 秒。原因是：`create_task` **立刻** 就把协程注册到事件循环开始跑了，不等 `await` 。`await t1` 这一行只是说「现在我要这个结果，没好就在这等一下」，等的时候 t2 也在并发地跑。

那 `create_task` 和 `gather` 区别是什么？

- `gather(coros...)` 一次性派出去再一次性收回，写法紧凑
- `create_task(coro)` 一个个派出去，可以单独 `await` ，可以 `cancel`，灵活

实战里常见的搭配：先用一堆 `create_task` 把任务派出去，最后用 `await asyncio.gather(*tasks)` 一次性收。这样既能拿到 Task 对象做精细控制，又能享受 gather 的便利。


### 小坑：协程 vs Task 直接传给 gather

`gather` 的参数既可以是协程对象，也可以是 Task 对象。看起来差不多，但有个细节：

<!-- skip-ci -->
```python
import asyncio


async def job(name):
    await asyncio.sleep(0.01)
    return name


async def main():
    coro = job('A')
    await asyncio.gather(coro, job('B'))


asyncio.run(main())
```

这里 `job('A')` 和 `job('B')` 都是协程对象，`gather` 内部会自动把它们包成 Task 再扔进事件循环。所以两种写法效果都一样。

只是要小心一点：**协程对象只能被 await 一次**。你不能拿同一个 `coro` 去 `gather` 两次：

<!-- skip-ci -->
```python
import asyncio


async def job():
    return 1


async def main():
    coro = job()
    await asyncio.gather(coro, coro)


asyncio.run(main())
```

这段会报错，提示协程被重复 await 。各位要并发跑同一个协程函数 N 次，要写 N 个调用，比如 `[job() for _ in range(N)]` 。


## asyncio.sleep vs time.sleep：阻塞坑

异步编程里有一个最最最常见的坑：**`time.sleep` 会把整个事件循环卡住**。

来看反例：

<!-- skip-ci -->
```python
import asyncio
import time


async def task(name):
    time.sleep(0.5)
    return f'{name} 完成'


async def main():
    start = time.perf_counter()
    await asyncio.gather(task('A'), task('B'), task('C'))
    cost = time.perf_counter() - start
    print(f'用了 {cost:.2f} 秒')


asyncio.run(main())
```

输出：

```
用了 1.50 秒
```

「不是 gather 吗？怎么又变 1.5 秒了？」

原因就是 `time.sleep` 。它是个 **同步阻塞** 函数，调用的时候不会释放 CPU 给事件循环。各位写了 `time.sleep(0.5)` ，等于跟操作系统说「让这个线程整体睡 0.5 秒」。整个事件循环——也就是所有协程——全都被卡死。

`asyncio.sleep(0.5)` 完全不一样。它是个协程，配合 `await` 使用的时候会告诉事件循环：「我要睡 0.5 秒，这段时间你随便调度别人」。

记住一条铁律：**在 `async` 函数里，凡是会阻塞的同步调用都要换成异步版本**。

| 同步（阻塞，禁用） | 异步（替代品） |
| --- | --- |
| `time.sleep(s)` | `await asyncio.sleep(s)` |
| `requests.get(url)` | `await httpx.AsyncClient().get(url)` |
| 标准 `open(f).read()` | `aiofiles` 库或者交给线程池 |

如果你不得不调用一个同步阻塞的库怎么办？`asyncio` 提供了一个逃生通道——`asyncio.to_thread` ，把这个调用扔到线程池里去：

<!-- skip-ci -->
```python
import asyncio
import time


def blocking_call():
    time.sleep(0.5)
    return '同步任务完成'


async def main():
    start = time.perf_counter()
    r1, r2 = await asyncio.gather(
        asyncio.to_thread(blocking_call),
        asyncio.to_thread(blocking_call),
    )
    cost = time.perf_counter() - start
    print(r1, r2)
    print(f'用了 {cost:.2f} 秒')


asyncio.run(main())
```

输出：

```
同步任务完成 同步任务完成
用了 0.50 秒
```

`asyncio.to_thread` 算是个折衷方案：让事件循环不被卡死，但还是要付线程的代价。如果有原生的 async 库可用（比如下面要讲的 `httpx`），优先用原生的。


## 超时控制：wait_for 和 timeout

写网络请求的童鞋一定有个心结：「万一对面服务器不返回，我这协程是不是要等到天荒地老？」

这就要请出 **超时** 了。`asyncio` 提供了两套写法。

**第一种：`asyncio.wait_for`** ，老牌的，写法是「把协程包一层」：

<!-- skip-ci -->
```python
import asyncio


async def slow_job():
    await asyncio.sleep(2)
    return '终于好了'


async def main():
    try:
        r = await asyncio.wait_for(slow_job(), timeout=0.5)
        print(r)
    except asyncio.TimeoutError:
        print('超时了，不等了')


asyncio.run(main())
```

输出：

```
超时了，不等了
```

`wait_for(coro, timeout=0.5)` 的意思是「给这个协程 0.5 秒，超过就取消并抛 `TimeoutError`」。

**第二种：`asyncio.timeout`**（Python 3.11+），新写法，用 `async with` 当上下文：

<!-- skip-ci -->
```python
import asyncio


async def slow_job():
    await asyncio.sleep(2)
    return '终于好了'


async def main():
    try:
        async with asyncio.timeout(0.5):
            r = await slow_job()
            print(r)
    except TimeoutError:
        print('超时了，不等了')


asyncio.run(main())
```

输出：

```
超时了，不等了
```

效果一样，但是写起来更顺手——你想给「这一段」加超时，就把这段 `async with` 包起来。要给多个 `await` 一起加超时，第二种写法尤其方便。新代码推荐用 `asyncio.timeout` 。

注意一个小变化：3.11 之后 `asyncio.TimeoutError` 直接就是内置的 `TimeoutError` 了，所以 `except TimeoutError` 也能 catch 到，不必写 `asyncio.TimeoutError` 。


## 取消：Task.cancel()

超时本质上是「自动取消」。其实手动取消也很简单：

<!-- skip-ci -->
```python
import asyncio


async def long_running():
    try:
        for i in range(10):
            print(f'还在跑 {i}')
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        print('被取消了，清理一下')
        raise


async def main():
    t = asyncio.create_task(long_running())
    await asyncio.sleep(0.12)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print('任务确实被取消了')


asyncio.run(main())
```

输出：

```
还在跑 0
还在跑 1
还在跑 2
被取消了，清理一下
任务确实被取消了
```

`Task.cancel()` 会向协程内部抛一个 `CancelledError` 。协程可以选择 catch 这个异常做清理，但 **强烈建议** 在清理完之后 `raise` 出去，让外面知道任务确实被取消了——把 `CancelledError` 默默吞掉，是另一个非常隐蔽的坑。


## TaskGroup：3.11 之后的 gather 升级版

`gather` 用着挺好，为什么 Python 3.11 又搞了个 `TaskGroup` 出来？

来看一个 `gather` 的尴尬场景。三个任务，一个抛错，另外两个该怎么办？

<!-- skip-ci -->
```python
import asyncio


async def good(name, delay):
    await asyncio.sleep(delay)
    return f'{name} ok'


async def bad():
    await asyncio.sleep(0.1)
    raise ValueError('坏了')


async def main():
    try:
        await asyncio.gather(good('A', 0.5), bad(), good('B', 0.5))
    except ValueError as e:
        print('main 捕获到', e)


asyncio.run(main())
```

输出大致是：

```
main 捕获到 坏了
```

看起来挺好。但是各位想想，A 和 B 这两个 0.5 秒的任务呢？它们其实还在 **后台默默跑着** ，gather 的默认行为是「一个失败就把异常往外抛，其他任务继续在事件循环里跑」。如果 A 里写文件、B 里发请求，它们会跑完（甚至再抛错）才停。这种「一脚走人，别人在背后干活」的行为不安全。

`TaskGroup` 解决了这个问题：

<!-- skip-ci -->
```python
import asyncio


async def good(name, delay):
    await asyncio.sleep(delay)
    return f'{name} ok'


async def bad():
    await asyncio.sleep(0.1)
    raise ValueError('坏了')


async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            t_a = tg.create_task(good('A', 0.5))
            t_bad = tg.create_task(bad())
            t_b = tg.create_task(good('B', 0.5))
    except* ValueError as eg:
        print('TaskGroup 捕获到异常组：', eg.exceptions)


asyncio.run(main())
```

输出大致是：

```
TaskGroup 捕获到异常组： (ValueError('坏了'),)
```

`TaskGroup` 的几个优点：

- **自动等待全部完成** ：`async with` 退出之前，所有 task 一定都跑完了
- **一个失败，全部取消** ：`bad` 抛错之后，A 和 B 会被立刻 `cancel` ，不会继续在后台跑
- **异常组（ExceptionGroup）** ：多个 task 同时失败的时候，所有异常会被打包成一个 `ExceptionGroup` ，用 `except*` 语法捕获

新代码里能用 `TaskGroup` 就用 `TaskGroup` ，比 `gather` 更安全、更可控。`gather` 适合场景简单、一两个任务、对取消语义要求不高的场合。

> 各位看到 `except*` 这个奇怪的语法不要慌，那是 Python 3.11 引入的 PEP 654「异常组」专用语法。简单理解就是「按类型从异常组里挑一类出来 catch」。一时用不到也没关系，知道有这么个东西就行。


## async with 和 async for

`asyncio.timeout(0.5)` 那个例子里，各位看到了 `async with` 的写法。这是「异步上下文管理器」——它的 `__enter__` 和 `__exit__` 都换成了 `async` 版本，叫 `__aenter__` 和 `__aexit__` 。

什么时候需要 `async with`？最常见的就是网络客户端：

<!-- skip-ci -->
```python
import asyncio
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://httpbin.org/get')
        print(r.status_code)


asyncio.run(main())
```

`async with` 之所以是 `async with`，是因为「关闭这个连接池」这件事本身可能涉及 IO，不能是一个普通的同步 `__exit__` 。

类似的还有「异步迭代器」——`async for` 。比如某些数据库驱动支持流式读取：

<!-- skip-ci -->
```python
import httpx
import asyncio


async def main():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', 'https://httpbin.org/stream/3') as resp:
            async for line in resp.aiter_lines():
                print('line:', line)


asyncio.run(main())
```

`async for line in resp.aiter_lines()` 的语义是：每读到一行（可能要等网络），把这一行交给我，然后继续等下一行。同步的 `for` 做不到这件事，只能 `async for` 。

各位记一下规律：

- 普通的对象、上下文 → `with` 、 `for`
- 涉及到 IO 的、协程的对象 → `async with` 、 `async for`


## 什么时候用 async，什么时候不用

讲了这么多，最后回到一个本质问题：什么场景适合 async？

`asyncio` 的强项是 **IO bound** ——程序大部分时间在等：等网络、等磁盘、等数据库、等用户输入。这种场景下「等待」是可以重叠的，async 能让一个线程同时等无数件事，效果立竿见影。

`asyncio` 的弱项是 **CPU bound** ——程序大部分时间在算：加密解密、图像处理、机器学习推理。这种场景下没有「等」可以利用，CPU 一直在干活，async 帮不上忙。一个线程也只能利用一个核，剩下七个核睡大觉。

对照表：

| 场景 | 用什么 |
| --- | --- |
| 抓 100 个 URL | `asyncio` + `httpx` |
| 同时读写一堆文件 | `asyncio` + `aiofiles` |
| 高并发 Web 服务（一台机器扛几千个连接） | `asyncio` + `FastAPI / aiohttp` |
| 视频转码、大矩阵计算 | `multiprocessing` 或 C 扩展 |
| 海量数据本地排序 | 多进程 + 分块 |
| 同时干一点 IO 一点 CPU | async 主框架 + `asyncio.to_thread` 或 `run_in_executor` |

各位可以这么记：**async 是用来「等」的，不是用来「算」的**。


## 实战：100 个 URL，串行 vs 并发

理论讲完了，是时候搞个真实的对比，让各位看看 `asyncio + httpx` 到底能比 `requests` 快多少。

先装一下 `httpx`：

```
pip install httpx
```

下面这段代码会同时跑两版：同步版用 `httpx` 的同步 client（行为和 `requests` 一样），并发版用 `httpx.AsyncClient` 加 `asyncio.gather` 。两边都打 50 个请求，比较总耗时：

<!-- skip-ci -->
```python
import asyncio
import time
import httpx

URLS = [f'https://httpbin.org/delay/1?i={i}' for i in range(50)]


def fetch_sync():
    with httpx.Client(timeout=30) as client:
        return [client.get(u).status_code for u in URLS]


async def fetch_async():
    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [client.get(u) for u in URLS]
        responses = await asyncio.gather(*tasks)
        return [r.status_code for r in responses]


def main():
    start = time.perf_counter()
    sync_codes = fetch_sync()
    sync_cost = time.perf_counter() - start
    print(f'同步 50 个：{sync_cost:.2f} 秒，全 200 = {all(c == 200 for c in sync_codes)}')

    start = time.perf_counter()
    async_codes = asyncio.run(fetch_async())
    async_cost = time.perf_counter() - start
    print(f'并发 50 个：{async_cost:.2f} 秒，全 200 = {all(c == 200 for c in async_codes)}')

    print(f'加速比：{sync_cost / async_cost:.1f} 倍')


main()
```

`httpbin.org/delay/1` 这个端点会强制等 1 秒再返回，方便我们看到差距。一次跑出来大致是这样：

```
同步 50 个：53.21 秒，全 200 = True
并发 50 个：1.62 秒，全 200 = True
加速比：32.8 倍
```

50 个请求，从 53 秒压到不到 2 秒——这就是 `asyncio + httpx` 的威力。各位可以拿这段代码改成自己关心的 URL 列表，比如批量抓博客文章、批量调内部 API 、批量 ping 服务，立马见效。

几个实战中要注意的点：

1. **要给 `httpx.AsyncClient` 设一个 `timeout`** ，否则碰到僵尸服务会一直挂着
2. **不要无脑开几千个并发** ，对方服务器扛不住会限流甚至封 IP 。一般用 `asyncio.Semaphore` 限制最大并发数：

<!-- skip-ci -->
```python
import asyncio
import httpx


async def fetch_one(client, sem, url):
    async with sem:
        r = await client.get(url)
        return r.status_code


async def fetch_many(urls, max_concurrency=10):
    sem = asyncio.Semaphore(max_concurrency)
    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [fetch_one(client, sem, u) for u in urls]
        return await asyncio.gather(*tasks)


urls = [f'https://httpbin.org/delay/1?i={i}' for i in range(100)]
codes = asyncio.run(fetch_many(urls, max_concurrency=10))
print(len(codes))
```

`Semaphore(10)` 的意思是「最多同时 10 个 task 进来」，第 11 个就要排队。这样既享受到了并发，又不会把对方打挂。

3. **错误处理** ：`gather` 默认一个失败就抛，整批数据都没了。如果你能接受「部分失败」，可以传 `return_exceptions=True` ，让 `gather` 把异常当做结果返回：

<!-- skip-ci -->
```python
import asyncio
import httpx


async def fetch(client, url):
    r = await client.get(url, timeout=5)
    r.raise_for_status()
    return r.status_code


async def main():
    urls = ['https://httpbin.org/get', 'https://httpbin.org/status/500', 'https://httpbin.org/get']
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *(fetch(client, u) for u in urls),
            return_exceptions=True,
        )
    for u, r in zip(urls, results):
        if isinstance(r, Exception):
            print(f'{u} 失败：{r}')
        else:
            print(f'{u} 成功：{r}')


asyncio.run(main())
```

这种写法在批量爬数据时特别好用——99 个成功 1 个失败也能继续跑。


## 小结

各位走到这里，应该已经对 `asyncio` 有了完整的直觉。我们简单回顾一下这条路：

- **痛点开场**：100 个网络请求串行跑慢得想骂人，多线程又重又乱
- **直觉对比**：3 件事 1 秒搞定 vs 3 秒搞定，差距来自「等」可以重叠
- **基础三件套**：`async def` 定义协程函数、 `await` 等结果、 `asyncio.run()` 进入事件循环
- **协程对象**：不 await 等于没写，这是最常见的坑
- **并发原语**：`asyncio.gather` 一次等多个、 `asyncio.create_task` 把任务派出去
- **阻塞坑**：`time.sleep` 会卡死整个事件循环，要换成 `asyncio.sleep`
- **超时和取消**：`asyncio.wait_for` 老写法、 `asyncio.timeout` 新写法、 `Task.cancel` 手动取消
- **TaskGroup**：3.11 之后的安全升级版，自动等全部、出错全取消
- **异步上下文**：`async with` 和 `async for` 是 IO 场景的标配
- **适用场景**：IO bound 才用 async，CPU bound 老老实实多进程
- **实战**：`asyncio + httpx` 抓 50 个 URL，30+ 倍加速肉眼可见

`asyncio` 的语法看起来花哨，本质上只是给「等待」加了一层调度。各位写代码时多想一句：「这一步是不是在等？」如果是，套个 `await` 试试，可能就有惊喜。

下一篇我们继续聊点别的好玩的东西。各位先把这一章的代码自己跑一遍，体会一下「单线程同时等一百件事」是个什么手感。



## 看清等待和结果，先不比较秒数

异步例子如果只看「快了几秒」，容易忽略究竟在等待什么。下面每个任务都返回一个分钟数，先关注任务的创建、等待和结果顺序：

```python
import asyncio


async def read_minutes(value):
    await asyncio.sleep(0)
    return value


async def main():
    tasks = [read_minutes(15), read_minutes(10)]
    results = await asyncio.gather(*tasks)
    print(results)


asyncio.run(main())
```

输出：

```text
[15, 10]
```

`read_minutes(15)` 产生协程对象，`gather` 等待这些工作完成，并按传入位置组织结果。不是谁先结束，谁就一定排到结果列表最前面。

自己把 `tasks` 改成空列表，结果应该是 `[]`。再增加一个 `read_minutes(0)`，应该得到 `[15, 10, 0]`。这比用一个很小的延迟去证明性能，更能核对我们是否理解结果。

本地脚本用 `asyncio.run()` 启动；交互式环境如果已有事件循环，要遵守该环境的运行方式。学习站已经适配了这个入口，因此这里可以跟随现有练习运行。异步也不自动把纯计算变成并行计算，选择它之前先确认任务是不是在等待可让出的工作。
