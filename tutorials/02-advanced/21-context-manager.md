# 上下文管理器：with 到底在做什么

各位先来看一段代码，猜猜哪里有坑：

```python
f = open('/tmp/two_drops_of_water.txt', 'w')
f.write('两点水的日记：今天打卡迟到了三分钟。')
f.close()
```

「这有什么问题？文件打开了、写完了、关掉了，一气呵成。」善于思考的你可能会这么说。

可是，万一 `f.write` 那一行抛了异常呢？

`close` 永远不会被执行，文件描述符就这么悬在那儿。一两次没事，可如果是个 Web 服务跑一整天，几千个请求里只要有几十个写文件失败，操作系统的 fd 就会被慢慢耗光，最后报一个看起来八竿子打不着的「Too many open files」。这种 bug，定位起来非常痛苦。

那怎么办？老办法当然是 `try/finally` ：

```python
f = open('/tmp/two_drops_of_water.txt', 'w')
try:
    f.write('两点水的日记：今天打卡迟到了三分钟。')
finally:
    f.close()
```

这样写虽然稳，但是丑。一个简单的写文件，外面要套一层 `try/finally` ，缩进就多一级。如果接下来还要打开第二个文件、第三个文件，缩进会一层一层套下去，很快就会写出「金字塔代码」。

童鞋们一定见过 Python 的另一种写法：

```python
with open('/tmp/two_drops_of_water.txt', 'w') as f:
    f.write('两点水的日记：今天打卡迟到了三分钟。')
```

短短两行，没有 `try` ，没有 `finally` ，没有手动 `close` ，但是不管 `write` 是否抛异常，文件都会被正确关闭。

这个 `with` 到底是个什么东西？为什么它能做到这么神奇的事情？这一章我们就把它从里到外讲清楚。


## with 的本质：上下文管理协议

`with` 后面跟的不是「文件」，也不是「连接」、「锁」之类的具体东西，而是一类东西，Python 给它起了个名字，叫「上下文管理器」（context manager）。

什么样的对象能算上下文管理器？只要满足两个方法：

- `__enter__(self)` ：进入 `with` 块的时候被调用，返回值会赋给 `as` 后面的变量
- `__exit__(self, exc_type, exc_val, tb)` ：离开 `with` 块的时候被调用，无论是正常离开还是异常离开

这就是「上下文管理协议」（context manager protocol）。它的全部规则就这两条，没有第三条。

我们可以拿打卡这个老朋友来手写一个最简单的上下文管理器，让各位先有个直观感受：

```python
class Punch:
    def __enter__(self):
        print('两点水进入打卡区')
        return self

    def __exit__(self, exc_type, exc_val, tb):
        print('两点水离开打卡区')


with Punch() as p:
    print('两点水正在工位摸鱼')
```

输出：

```
两点水进入打卡区
两点水正在工位摸鱼
两点水离开打卡区
```

各位看到了什么？`with Punch() as p` 这一行做了三件事：

1. 创建一个 `Punch()` 实例
2. 调用这个实例的 `__enter__()` 方法
3. 把 `__enter__()` 的返回值赋给 `p`

然后才执行 `with` 块里面的代码。等 `with` 块结束（不管是正常结束还是异常结束），就调用 `__exit__()` 。

这个流程看着是不是很眼熟？没错，它本质上就是把：

<!-- skip-ci -->
```python
p_obj = Punch()
p = p_obj.__enter__()
try:
    print('两点水正在工位摸鱼')
finally:
    p_obj.__exit__(None, None, None)
```

这一坨样板代码，藏到了 `with` 这个语法糖背后。`with` 一行顶六行，就是这么来的。


## 顺手回头看一眼 open

弄懂了协议，我们再回头看 `open()` ：

```python
with open('/tmp/two_drops_of_water.txt', 'w') as f:
    f.write('一行字。')
```

`open()` 返回的文件对象本身就实现了 `__enter__` 和 `__exit__` 。它的 `__enter__` 直接 `return self` ，所以 `f` 拿到的就是文件对象本身；它的 `__exit__` 里调用的就是 `close()` 。简简单单，但是覆盖了所有的异常路径。

各位可以自己验证一下：

```python
f = open('/tmp/two_drops_of_water.txt', 'w')
print(hasattr(f, '__enter__'))
print(hasattr(f, '__exit__'))
f.close()
```

输出：

```
True
True
```

不光是文件，标准库里的 `socket` 、`threading.Lock` 、`sqlite3.Connection` ，第三方库里的 `requests.Session` 、`open(...).fileobj` 等等，几乎所有「需要成对操作」的资源都实现了上下文管理器协议。打开/关闭、获取/释放、连接/断开，凡是这种「有借有还」的事情，扔给 `with` 去管准没错。

我们再多看一个例子，体会一下上下文管理器是怎么把「成对操作」的细节藏起来的。`threading.Lock` 这个类大家应该不陌生，多线程编程里几乎离不开它：

```python
import threading


lock = threading.Lock()

# 不用 with 的写法，需要手动 acquire 和 release
lock.acquire()
try:
    print('两点水正在临界区里搬砖')
finally:
    lock.release()

# 用 with 的写法，Python 帮我们把 acquire 和 release 都安排好了
with lock:
    print('两点水又一次进入临界区')
```

输出：

```
两点水正在临界区里搬砖
两点水又一次进入临界区
```

注意这里 `with lock:` 没有写 `as ...` 。因为锁的 `__enter__` 返回的就是它自己，对绝大多数使用场景没用——我们关心的是「锁住了」这个状态，不是返回值本身。所以 `as` 可以省。这也是大部分锁、信号量、事件之类的上下文管理器的常见写法。


## 一个稍微有用一点的例子：打卡上下文

光是 `print` 几行字太单薄了，我们让这个 `Punch` 做点正经事——记录员工的进入时间和离开时间，并把它写到「日志」里：

```python
import time


class PunchLog:
    def __init__(self, name):
        self.name = name
        self.records = []

    def __enter__(self):
        self.start = time.time()
        self.records.append(f'{self.name} 进入工位')
        return self

    def __exit__(self, exc_type, exc_val, tb):
        cost = time.time() - self.start
        self.records.append(f'{self.name} 离开工位，停留 {cost:.4f} 秒')


log = PunchLog('两点水')
with log:
    time.sleep(0.05)
    print('正在划水……')

for line in log.records:
    print(line)
```

输出大致是：

```
正在划水……
两点水 进入工位
两点水 离开工位，停留 0.0507 秒
```

注意 `__enter__` 这次没有 `return self` 也没关系，因为我们外面用的是 `with log:` ，不需要 `as` 接返回值，`log` 这个变量本身就是上下文管理器。如果改成 `with log as l:` ，那 `l` 会变成 `None` ，因为 `__enter__` 默认返回 `None` 。这是新手最容易踩的小坑：「我的 `as x` 怎么是 `None` ？」八成是 `__enter__` 忘了 `return` 。


## 同时管理多个上下文

实际项目里，经常需要同时打开两个甚至三个文件——读一个、写一个、再写一个错误日志。早期 Python 只能这么写：

```python
with open('/tmp/in.txt', 'w') as fin:
    pass

with open('/tmp/in.txt') as fin:
    with open('/tmp/out.txt', 'w') as fout:
        fout.write(fin.read())
```

两层缩进。如果再加一个 `err.log` ，就是三层。

后来 Python 允许在一个 `with` 里写多个上下文，用逗号分隔：

```python
with open('/tmp/in.txt') as fin, open('/tmp/out.txt', 'w') as fout:
    fout.write(fin.read())
```

这样比嵌套写法清爽多了。可是问题又来了——如果上下文很多，一行会变得贼长，没法折行。

Python 3.10 给出了一个新语法，叫 PEP 617 「带括号的上下文管理器」，允许把多个上下文用括号包起来：

```python
with (
    open('/tmp/in.txt') as fin,
    open('/tmp/out.txt', 'w') as fout,
):
    fout.write(fin.read())
```

注意三件事：

1. 括号里每一行后面都可以加逗号，包括最后一个，PEP 617 允许尾随逗号
2. 这个语法是 Python 3.10+ 才有的
3. 代码风格上，这是处理「同时管理 3 个以上上下文」时最推荐的写法

如果各位还在用 3.9 或者更老的版本，要么用逗号分隔的单行写法，要么后面我们会讲到 `ExitStack` 。

顺手提一个细节：多个上下文管理器是按从左到右的顺序依次 `__enter__` ，按从右到左的顺序依次 `__exit__` 。这是个非常重要的语义保证——比如「先拿锁再开文件」的代码，退出时一定是「先关文件再放锁」。我们写一个小 demo 验证一下：

```python
from contextlib import contextmanager


@contextmanager
def stage(name):
    print(f'{name} __enter__')
    try:
        yield name
    finally:
        print(f'{name} __exit__')


with stage('A') as a, stage('B') as b, stage('C') as c:
    print(f'with 块内部：{a} {b} {c}')
```

输出：

```
A __enter__
B __enter__
C __enter__
with 块内部：A B C
C __exit__
B __exit__
A __exit__
```

各位看到了，C 是最后进入的，也是第一个退出的。和函数调用栈、嵌套 `try/finally` 的语义完全一致。


## __exit__ 的三个参数：异常处理

前面有提到，`__exit__` 的签名是 `__exit__(self, exc_type, exc_val, tb)` ，但一直没解释这三个参数干嘛用。

正常情况下，`with` 块里没抛异常，这三个参数都是 `None` 。一旦出了异常，它们分别是：

- `exc_type` ：异常的类型（比如 `ZeroDivisionError`）
- `exc_val` ：异常的实例
- `tb` ：traceback 对象

更关键的是 `__exit__` 的返回值：

- 返回 `True` （或者任何「真值」）：异常被「吞掉」，不再往外抛
- 返回 `False` 、`None` 、或者根本不写 `return` ：异常继续往外抛

我们写一个能把 `ZeroDivisionError` 吞掉的上下文管理器看看：

```python
class IgnoreZeroDivision:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        if exc_type is ZeroDivisionError:
            print(f'吞掉了一个除零异常：{exc_val}')
            return True
        return False


with IgnoreZeroDivision():
    x = 1 / 0
    print('这句话不会被打印，因为上一行抛异常了')

print('但是这句话会被打印，因为异常被 __exit__ 吞掉了')
```

输出：

```
吞掉了一个除零异常：division by zero
但是这句话会被打印，因为异常被 __exit__ 吞掉了
```

如果 `with` 块里抛的是 `ZeroDivisionError` 之外的异常，比如 `ValueError` ，`__exit__` 会返回 `False` ，异常照常往外冒。

需要强调一点：吞掉异常这个能力非常强，但请务必谨慎使用。一般来说，上下文管理器的职责是「无论怎样都把资源清理掉」，而不是「假装异常没发生过」。盲目地 `return True` 可能掩盖真正的 bug 。标准库里真正会吞异常的上下文管理器寥寥无几，最常见的就是后面要讲的 `contextlib.suppress` 。

还有一个常见的错觉：「我能不能在 `__exit__` 里把异常换成另一种异常抛出来？」答案是可以，但是有讲究。直接在 `__exit__` 里 `raise` 一个新异常会把当前正在传播的异常「替换掉」，这种情况下原异常会变成新异常的 `__context__` 。我们写个例子让童鞋们看清楚：

```python
class TranslateException:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        if exc_type is not None:
            raise RuntimeError(f'我把 {exc_type.__name__} 翻译成了 RuntimeError') from exc_val


try:
    with TranslateException():
        1 / 0
except RuntimeError as e:
    print(f'外面拿到的是：{e}')
    print(f'原因是：{e.__cause__}')
```

输出：

```
外面拿到的是：我把 ZeroDivisionError 翻译成了 RuntimeError
原因是：division by zero
```

这种「翻译异常」的模式在写库的时候特别有用。比如数据库驱动里把底层各种网络错误统一翻译成 `DatabaseError` ，外层就不用关心是 socket 断了、还是 SSL 握手失败、还是协议解析出错了。`raise X from Y` 这个语法在异常处理章节里讲过，这里复习一下用法即可。


## contextlib：标准库的好朋友

写一个上下文管理器，只为了管几行代码，居然要写一个完整的类、写两个 dunder 方法，是不是有点重？

Python 标准库里有个叫 `contextlib` 的模块，专门给我们提供了一堆工具来简化这件事。最重要的就是 `@contextmanager` 这个装饰器。

各位还记得装饰器章节里提到的生成器吗？`@contextmanager` 就是把一个生成器函数变成上下文管理器。它的规则非常简单：

- `yield` 之前的代码 = `__enter__`
- `yield` 出来的值 = `__enter__` 的返回值
- `yield` 之后的代码 = `__exit__`

我们把上面那个 `PunchLog` 用 `@contextmanager` 重写一遍，对比一下：

```python
import time
from contextlib import contextmanager


@contextmanager
def punch_log(name):
    records = []
    start = time.time()
    records.append(f'{name} 进入工位')
    try:
        yield records
    finally:
        cost = time.time() - start
        records.append(f'{name} 离开工位，停留 {cost:.4f} 秒')


with punch_log('两点水') as records:
    time.sleep(0.05)
    print('继续划水……')

for line in records:
    print(line)
```

输出：

```
继续划水……
两点水 进入工位
两点水 离开工位，停留 0.0506 秒
```

是不是清爽多了？类一下子变成了一个函数，两个 dunder 方法变成了一个 `yield` 。

注意里面那个 `try/finally` 。为什么需要它？

因为 `with` 块里面可能抛异常，异常会从 `yield` 那一行重新「钻」回生成器函数里。如果不写 `try/finally` ，那异常会把后面的清理代码直接绕过去，资源就泄露了。`try/finally` 才能保证「不管 yield 抛不抛异常，finally 里的清理代码一定会执行」。

这是用 `@contextmanager` 写上下文管理器时最重要的一条铁律：**清理代码要包在 finally 里**。新手最常见的 bug 就是不写 `try/finally` ，结果异常路径下资源没释放。


## @contextmanager + 异常处理

那如果我想吞掉异常呢？用 `@contextmanager` 怎么写？

很简单，把 `yield` 包在 `try/except` 里就行：

```python
from contextlib import contextmanager


@contextmanager
def ignore_zero_division():
    try:
        yield
    except ZeroDivisionError as e:
        print(f'用 @contextmanager 吞掉了：{e}')


with ignore_zero_division():
    x = 1 / 0
    print('这一行不会执行')

print('但是这一行会')
```

输出：

```
用 @contextmanager 吞掉了：division by zero
但是这一行会
```

`except` 捕获到异常之后，函数正常返回，对应的就是 `__exit__` 返回 `True` ；如果异常没被捕获、被生成器原样抛出来，对应的就是 `__exit__` 让异常继续向上传播。`@contextmanager` 内部帮你把这两条路接好了，我们只需要按 Python 异常处理的常规思路来写就行。


## contextlib 里的几个常客

`contextlib` 不只有 `@contextmanager` ，还有几个开箱即用的小工具，用过几次之后会觉得离不开：

### closing：把没实现 with 的对象包成上下文

不是所有需要 close 的对象都实现了上下文管理器协议。最典型的就是 `urllib.request.urlopen` 在某些老版本里返回的对象，以及一些自定义的资源对象。`closing` 帮我们补上这一层：

```python
from contextlib import closing


class Connection:
    def __init__(self, name):
        self.name = name

    def close(self):
        print(f'{self.name} 已关闭')


with closing(Connection('数据库连接')) as conn:
    print(f'正在使用 {conn.name}')
```

输出：

```
正在使用 数据库连接
数据库连接 已关闭
```

`closing(obj)` 等价于一个上下文管理器，它的 `__enter__` 返回 `obj` ，它的 `__exit__` 调用 `obj.close()` 。简单粗暴。

### suppress：优雅地忽略异常

```python
from contextlib import suppress


with suppress(FileNotFoundError):
    open('/tmp/this_file_definitely_does_not_exist_12345.txt').read()

print('哪怕文件不存在，我也能继续往下走')
```

输出：

```
哪怕文件不存在，我也能继续往下走
```

`suppress` 就是上面 `IgnoreZeroDivision` 的标准库通用版。它接受任意多个异常类型，匹配上就吞掉，不匹配就往上抛。

`suppress` 比 `try: ... except SomeError: pass` 短，而且更明显地表达「我就是要忽略这个异常」的意图。但同样请谨慎使用，不要用它来掩盖真 bug 。

### redirect_stdout / redirect_stderr：临时改写标准输出

有时候我们想把某段代码的 `print` 输出抓到字符串里，或者写到文件里，又不想动它的源码：

```python
import io
from contextlib import redirect_stdout


buf = io.StringIO()
with redirect_stdout(buf):
    print('这段话不会出现在终端')
    print('而是被抓到了 buf 里')

captured = buf.getvalue()
print('我抓到了：')
print(captured)
```

输出：

```
我抓到了：
这段话不会出现在终端
而是被抓到了 buf 里

```

测试代码、或者把第三方库的日志重定向到自己的 logger 时，这两个工具特别好使。

### nullcontext：什么都不做的占位上下文

考虑这种场景：你的函数有时候需要在锁里跑，有时候不需要。怎么写得优雅一点？

```python
from contextlib import nullcontext
import threading


def do_stuff(lock=None):
    cm = lock if lock is not None else nullcontext()
    with cm:
        print('做事')


lock = threading.Lock()
do_stuff(lock)
do_stuff()
```

输出：

```
做事
做事
```

`nullcontext()` 的 `__enter__` 和 `__exit__` 啥都不做，纯粹是为了让 `with` 这一行能写得通用。你不用再去写 `if lock: with lock: ... else: ...` 这种又臭又长的分支。

`nullcontext` 还能携带一个值，假装它就是 `__enter__` 的返回结果——这在「有时候已经有现成的对象，有时候要新打开一个」的场景里非常顺手：

```python
from contextlib import nullcontext


def read_text(source):
    cm = nullcontext(source) if hasattr(source, 'read') else open(source)
    with cm as f:
        return f.read()


import io
text1 = read_text(io.StringIO('我是一个已经打开的对象'))
print(text1)

with open('/tmp/two_drops_e.txt', 'w') as f:
    f.write('我是写在磁盘上的内容')

text2 = read_text('/tmp/two_drops_e.txt')
print(text2)
```

输出：

```
我是一个已经打开的对象
我是写在磁盘上的内容
```

一个函数，既能接受字符串路径，也能接受已经打开的文件对象，写法一气呵成。这种「适配两种输入」的小套路在工程里非常常用。


## 实战：临时改环境变量

来看一个非常常见的需求：测试一段代码在某个环境变量被设置时的行为，但是又不想污染当前进程的环境。

各位会怎么写？

```python
import os
from contextlib import contextmanager


@contextmanager
def set_env(**kwargs):
    old = {}
    for k, v in kwargs.items():
        old[k] = os.environ.get(k)
        os.environ[k] = v
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


os.environ.pop('TWO_DROPS_OF_WATER', None)
print('进入前：', os.environ.get('TWO_DROPS_OF_WATER'))

with set_env(TWO_DROPS_OF_WATER='hello'):
    print('with 里：', os.environ.get('TWO_DROPS_OF_WATER'))

print('退出后：', os.environ.get('TWO_DROPS_OF_WATER'))
```

输出：

```
进入前： None
with 里： hello
退出后： None
```

各位看仔细：进入 `with` 之前，把要修改的环境变量的「原值」记下来；`with` 块里，把它们改成新值；退出的时候——不管是不是正常退出——把原值恢复回去。这就是上下文管理器最经典的用法：「临时改一下，离开时还原」。

类似的模式还能用在「临时切换工作目录」、「临时改 sys.path」、「临时调高日志级别」等场景。一旦掌握了这个套路，写起来手感非常顺。


## 临时切换工作目录

顺手再演示一个：

```python
import os
from contextlib import contextmanager


@contextmanager
def chdir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


before = os.getcwd()
with chdir('/tmp'):
    print('在 with 里：', os.getcwd())

print('退出后回到：', os.getcwd() == before)
```

输出（路径以实际为准）：

```
在 with 里： /tmp
退出后回到： True
```

补一句：Python 3.11 在标准库里加了 `contextlib.chdir` ，效果跟我们手写的这个一样，可以直接 `from contextlib import chdir` 。如果你已经在 3.11+ ，就不用自己造轮子了。


## ExitStack：动态数量的上下文

到目前为止，我们一直假设「我有 N 个上下文，N 是写代码的时候就知道的」。但是有时候 N 是运行时才知道的——比如「打开用户给的一组文件，全部用完之后再关」。

用 `with` 一行写不下，因为名字数量不定；用嵌套 `with` 写不出来，因为缩进不知道嵌几层。这种时候 `ExitStack` 就派上用场了。

```python
from contextlib import ExitStack


def make_files(paths):
    with ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in paths]
        total = sum(len(f.read()) for f in files)
        print(f'共读取 {len(files)} 个文件，{total} 字节')


with open('/tmp/two_drops_a.txt', 'w') as f:
    f.write('a' * 100)
with open('/tmp/two_drops_b.txt', 'w') as f:
    f.write('bb' * 50)
with open('/tmp/two_drops_c.txt', 'w') as f:
    f.write('ccc' * 30)

make_files(['/tmp/two_drops_a.txt', '/tmp/two_drops_b.txt', '/tmp/two_drops_c.txt'])
```

输出：

```
共读取 3 个文件，290 字节
```

`stack.enter_context(cm)` 把一个上下文管理器「压入栈」，效果就跟把它放在最外层 `with` 一样。当 `with ExitStack()` 退出的时候，栈里所有的上下文会按照「后进先出」的顺序被一一退出，跟普通嵌套 `with` 的语义完全一致。

`ExitStack` 还有一个特别好用的方法叫 `callback` ，可以注册一个普通的清理函数，不需要它是上下文管理器：

```python
from contextlib import ExitStack


def cleanup(name):
    print(f'清理 {name}')


with ExitStack() as stack:
    stack.callback(cleanup, 'A')
    stack.callback(cleanup, 'B')
    stack.callback(cleanup, 'C')
    print('正在 with 块内部')
```

输出：

```
正在 with 块内部
清理 C
清理 B
清理 A
```

清理顺序是 C → B → A ，倒着来。这跟函数局部变量析构的顺序一致，符合「先打开后关」的直觉。

`ExitStack` 还有一些更高级的用法，比如 `pop_all` 把栈转移到另一个 `ExitStack` 里，用来实现「事务性清理」——但那是进阶话题了，等各位真正遇到再去翻文档不迟。

补一个比较实用的模式：把多个文件按动态数量打开，万一中途有一个开失败，已经打开的全部要被关掉。`ExitStack` 天然就帮我们做到了这一点：

```python
from contextlib import ExitStack


def open_safely(paths):
    with ExitStack() as stack:
        files = []
        for p in paths:
            files.append(stack.enter_context(open(p)))
        return [f.name for f in files]


# 准备三个真实存在的文件
for name in ['/tmp/two_drops_x.txt', '/tmp/two_drops_y.txt', '/tmp/two_drops_z.txt']:
    with open(name, 'w') as f:
        f.write('hi')

names = open_safely(['/tmp/two_drops_x.txt', '/tmp/two_drops_y.txt', '/tmp/two_drops_z.txt'])
print(f'安全地处理了 {len(names)} 个文件')

try:
    open_safely(['/tmp/two_drops_x.txt', '/tmp/this_does_not_exist_99999.txt'])
except FileNotFoundError as e:
    print(f'第二个文件失败，但是第一个已经被自动关闭了：{e.filename}')
```

输出：

```
安全地处理了 3 个文件
第二个文件失败，但是第一个已经被自动关闭了：/tmp/this_does_not_exist_99999.txt
```

这就是 `ExitStack` 在工程里最值钱的地方：「批量打开，一旦失败统一回滚」。如果让我们手写 `try/finally` 来实现，代码会变得非常啰嗦，而且很容易漏掉某条异常路径。


## async with：异步世界的 with

最后简单提一句异步版本。Python 3.5 引入了 `async/await` 语法，3.7 之后逐渐成为主流。在 `async def` 函数里，如果要用上下文管理器，需要写成 `async with` ：

```python
# 这是一个示意，需要在 async 函数里运行
# async with httpx.AsyncClient() as client:
#     resp = await client.get('https://example.com')
```

对应的协议方法是 `__aenter__` 和 `__aexit__` ，`contextlib` 也提供了 `@asynccontextmanager` 装饰器。这部分内容会在 `async/await` 章节深入讲，这里只是让童鞋们知道有这么一回事，不要在 `async` 代码里看到 `async with` 一脸懵。


## 小实战：写一个 timer 上下文

把这一章学到的东西串起来，我们写一个小工具：进入 `with` 时记录时间，退出时打印「这段代码耗时多少毫秒」。

先用类的写法：

```python
import time


class Timer:
    def __init__(self, name='匿名代码块'):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, tb):
        cost_ms = (time.perf_counter() - self.start) * 1000
        print(f'{self.name} 耗时 {cost_ms:.2f} ms')


with Timer('两点水的睡觉时间'):
    time.sleep(0.05)
    s = sum(range(10000))
```

输出大约是：

```
两点水的睡觉时间 耗时 50.46 ms
```

再用 `@contextmanager` 重写，对比一下：

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(name='匿名代码块'):
    start = time.perf_counter()
    try:
        yield
    finally:
        cost_ms = (time.perf_counter() - start) * 1000
        print(f'{name} 耗时 {cost_ms:.2f} ms')


with timer('打卡用时'):
    time.sleep(0.03)
    sum(range(5000))
```

输出大约是：

```
打卡用时 耗时 30.21 ms
```

各位选哪个版本？我个人偏爱 `@contextmanager` 版本，更紧凑。但是当上下文管理器需要保存复杂状态、或者要被复用、或者需要继承的时候，类的写法更合适。两种写法的能力是等价的，看场合选一个就好。

再加点料——如果想让 `Timer` 既能当上下文管理器，又能当装饰器呢？这两个需求经常一起出现。`contextlib` 早就替我们想好了，`ContextDecorator` 这个基类一行代码搞定：

```python
import time
from contextlib import ContextDecorator


class Timer(ContextDecorator):
    def __init__(self, name='匿名代码块'):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, tb):
        cost_ms = (time.perf_counter() - self.start) * 1000
        print(f'{self.name} 耗时 {cost_ms:.2f} ms')


@Timer('两点水的函数')
def work():
    time.sleep(0.02)


work()
```

输出大约是：

```
两点水的函数 耗时 20.34 ms
```

而且如果有了 `ContextDecorator` ，`@contextmanager` 装饰器写出来的函数也天然能当装饰器用，不需要再做额外处理：

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(name='匿名代码块'):
    start = time.perf_counter()
    try:
        yield
    finally:
        cost_ms = (time.perf_counter() - start) * 1000
        print(f'{name} 耗时 {cost_ms:.2f} ms')


@timer('打卡函数')
def punch():
    time.sleep(0.01)


punch()
```

输出大约是：

```
打卡函数 耗时 10.32 ms
```

是不是发现 `@contextmanager` 自带了 `ContextDecorator` 的能力？所以一个函数同时是装饰器和上下文管理器，毫无违和感。这也是为什么很多日志、性能监控、tracing 库都喜欢用 `@contextmanager` 写它们的核心 API ：一份实现，两种用法。


## 一个常见的反模式

最后唠叨几句新手最容易踩的几个坑：

### 反模式一：在 with 外面访问 with 的变量

```python
with open('/tmp/two_drops_d.txt', 'w') as f:
    f.write('hi')

print(f.closed)
```

输出：

```
True
```

`f` 这个变量在 `with` 退出后**还在**，但它指向的文件对象已经被 close 了。这不是错误，但是非常具有误导性——很多新手以为 `with` 出来后 `f` 会变成 `None` 或者直接 `NameError` ，实则不会。能拿到这个变量但是它已经废了，这是 Python 上下文管理器的设计取舍。

记住：`with` 块退出后，`as` 后面的变量仍然存在于当前作用域，但里面的资源已经被释放，碰它大概率会出错。

### 反模式二：忘了 try/finally

写 `@contextmanager` 时如果不写 `try/finally` ，看起来正常路径下没问题，但是异常一来就资源泄露：

```python
from contextlib import contextmanager


@contextmanager
def bad():
    print('打开资源')
    yield
    print('关闭资源')


try:
    with bad():
        raise ValueError('故意抛个异常')
except ValueError:
    print('外层捕获到了异常')
```

输出：

```
打开资源
外层捕获到了异常
```

「关闭资源」这句话**没有被打印**，因为异常把 `yield` 之后的代码全跳过了。所以前面才那么强调，清理逻辑必须放在 `finally` 里。

### 反模式三：在 @contextmanager 函数里 yield 多次

```python
from contextlib import contextmanager


@contextmanager
def double_yield():
    print('准备')
    yield 1
    yield 2
    print('结束')


try:
    with double_yield() as v:
        print(f'拿到了 {v}')
except RuntimeError as e:
    print(f'报错了：{e}')
```

输出：

```
准备
拿到了 1
报错了：generator didn't stop
```

`@contextmanager` 装饰的生成器**只能 `yield` 一次**。yield 之前是 `__enter__` ，yield 之后是 `__exit__` 。如果 yield 了两次，Python 在第二次 yield 的时候发现「这个生成器没有按预期在 yield 之后立即结束」，就会抛 `RuntimeError` 。这是新手最容易写出来的 bug ，因为生成器函数本身是允许多次 yield 的，但是放到 `@contextmanager` 这个上下文里就只能 yield 一次。

### 反模式四：滥用 return True 吞异常

```python
class SwallowEverything:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        return True


with SwallowEverything():
    1 / 0
    raise RuntimeError('what?')

print('我居然还在执行')
```

输出：

```
我居然还在执行
```

这种「全吞」式上下文管理器是巨型反模式。它会把真正的 bug 也一起吃掉，让程序在错误状态下继续运行，调试时根本没法定位。`return True` 应该是非常窄、非常明确的「我就是要忽略这一种异常」的精确动作，而不是「让世界更安静一点」的偷懒手段。


## 一个综合的小例子：可重用的「水哥打卡审计器」

为了让前面的知识点串起来，我们写一个稍微复杂一点的例子收尾。需求是：每次员工进入工位都要记录开始时间，离开时记录结束时间，期间如果代码出了异常，要把异常类型一并记录。最后再加一个总结报告。

```python
import time
from contextlib import contextmanager


class Auditor:
    def __init__(self):
        self.events = []

    @contextmanager
    def shift(self, name):
        start = time.perf_counter()
        self.events.append({'name': name, 'phase': 'enter'})
        try:
            yield
        except Exception as e:
            self.events.append({
                'name': name,
                'phase': 'error',
                'exception': type(e).__name__,
            })
            raise
        finally:
            cost_ms = (time.perf_counter() - start) * 1000
            self.events.append({
                'name': name,
                'phase': 'leave',
                'cost_ms': round(cost_ms, 2),
            })

    def report(self):
        print(f'共记录 {len(self.events)} 条事件：')
        for e in self.events:
            print(f'  - {e}')


auditor = Auditor()

with auditor.shift('两点水'):
    time.sleep(0.01)

try:
    with auditor.shift('童鞋甲'):
        raise ValueError('代码炸了')
except ValueError:
    pass

with auditor.shift('童鞋乙'):
    time.sleep(0.005)

auditor.report()
```

输出大约是：

```
共记录 7 条事件：
  - {'name': '两点水', 'phase': 'enter'}
  - {'name': '两点水', 'phase': 'leave', 'cost_ms': 10.42}
  - {'name': '童鞋甲', 'phase': 'enter'}
  - {'name': '童鞋甲', 'phase': 'error', 'exception': 'ValueError'}
  - {'name': '童鞋甲', 'phase': 'leave', 'cost_ms': 0.16}
  - {'name': '童鞋乙', 'phase': 'enter'}
  - {'name': '童鞋乙', 'phase': 'leave', 'cost_ms': 5.21}
```

这段代码做对了几件重要的事，各位可以挨个对照一下：

1. `@contextmanager` 装饰的是**类的方法**——这完全合法，方法的 `self` 在生成器内部依然可用
2. `try/except/finally` 三件套俱全：异常路径走 `except` ，所有路径都走 `finally`
3. `except Exception as e: ...; raise` ：先记录，再原样重新抛出，不吞异常
4. 报告里能看到一次错误事件的完整生命周期：enter → error → leave

这就是上下文管理器在工程中的典型用法——一个对象、几行代码，把「时间统计、异常记录、资源清理」三件事打包到一起。在做性能监控、APM 接入、tracing 时，几乎所有库的核心 API 都长这个样。


## 小结

`with` 不是一个孤立的语法糖，它背后是「上下文管理协议」：

- `__enter__` 进入，`__exit__` 离开
- `__exit__` 收到三个异常相关参数，返回 `True` 可以吞掉异常（请慎用）
- 多个上下文可以用逗号分隔，3.10+ 还能用括号包起来，多行书写
- `contextlib.contextmanager` 让我们用一个 `yield` 替代两个 dunder 方法，但是必须用 `try/finally` 保证清理代码被执行
- `closing` 、`suppress` 、`redirect_stdout` 、`nullcontext` 这些小工具能省掉不少样板
- `ExitStack` 处理「动态数量的上下文」
- `async with` 是异步版本，思路一致，等到 `async/await` 章节再细聊

凡是有「成对操作」、「资源借还」、「临时切换」、「进入/离开」这种语义的地方，都可以用上下文管理器去封装。一旦养成这个习惯，你写出来的代码不仅短，而且对异常路径天然友好——这才是 `with` 真正值钱的地方。

下一章我们要深入到 `async/await` 的世界，去看看 Python 是怎么用一个 `async` 关键字撬动整个异步生态的。各位先把 `with` 玩熟，到时候看 `async with` 会觉得就是顺水推舟的事。



## 结果留下来，资源关起来

`with` 不只是让代码少一行 `close()`。我们用一份内存文本观察退出语句块前后，什么仍然可以使用：

```python
from io import StringIO

with StringIO('Python:15') as stream:
    content = stream.read()
print(content)
print(stream.closed)
```

输出：

```text
Python:15
True
```

文本已经读到 `content`，这个字符串仍然可用；`stream` 则已经关闭。不要因为变量名还在，就认为它代表的资源还可以继续读写。

自己试着把 `stream.read()` 放到 `with` 之后，观察关闭后的读取错误。再在语句块里故意抛出一个异常，在外面捕获后检查 `stream.closed`。对这个对象来说，退出时仍然会关闭资源。

也要记住，`with` 的行为由具体上下文管理器决定，并不保证自动撤销所有已经做过的事情。例如打开文件写了内容，后面发生异常，不会仅因为用了 `with` 就自动恢复旧文件。资源收尾、异常是否传播和数据事务是不同的问题。
