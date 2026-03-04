# 上下文管理器 ⭐⭐进阶

> 资源管理的优雅方式

---

## 基本用法

```python
with open('file.txt', 'r') as f:
    content = f.read()
# 自动关闭文件
```

---

## 类实现

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """进入上下文，返回绑定到 as 的对象"""
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文，处理异常"""
        self.file.close()
        # 返回 True 抑制异常，False 或 None 传播异常
        return False
```

---

## contextlib 模块

### contextmanager 装饰器

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    f = open(filename, mode)
    try:
        yield f  # __enter__ 的返回值
    finally:
        f.close()  # __exit__ 的逻辑

with managed_file('test.txt', 'w') as f:
    f.write('hello')
```

### suppress

抑制指定异常。

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove('nonexistent.txt')  # 不抛出异常
```

### redirect_stdout

重定向标准输出。

```python
from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    print('hello')

output = f.getvalue()  # 'hello\n'
```

### ExitStack

动态管理多个上下文。

```python
from contextlib import ExitStack

files = ['a.txt', 'b.txt', 'c.txt']
with ExitStack() as stack:
    handles = [stack.enter_context(open(f)) for f in files]
    # 所有文件在退出时自动关闭
```

---

## 异常处理

```python
class Catch:
    def __init__(self, suppress=False):
        self.suppress = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"捕获异常: {exc_type.__name__}: {exc_val}")
        return self.suppress

with Catch(suppress=True):
    1 / 0  # 异常被捕获并抑制
```

---

## 嵌套上下文

```python
with open('in.txt') as fin:
    with open('out.txt', 'w') as fout:
        fout.write(fin.read())

# 简化写法
with open('in.txt') as fin, open('out.txt', 'w') as fout:
    fout.write(fin.read())
```

---

## 常见应用场景

| 场景 | 说明 |
|------|------|
| 文件操作 | 自动关闭文件 |
| 数据库连接 | 自动提交/回滚 |
| 锁 | 自动释放锁 |
| 计时 | 自动记录时间 |
| 临时修改状态 | 恢复原状态 |

### 计时示例

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        print(f"耗时: {self.end - self.start:.2f}s")

with Timer():
    time.sleep(1)  # 耗时: 1.00s
```

### 临时目录

```python
import tempfile
import os

with tempfile.TemporaryDirectory() as tmpdir:
    path = os.path.join(tmpdir, 'test.txt')
    with open(path, 'w') as f:
        f.write('hello')
# 临时目录自动删除
```
