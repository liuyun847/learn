# 生成器与迭代器 ⭐⭐进阶

> 惰性求值与数据流处理

---

## 迭代器协议

```python
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        """返回迭代器对象"""
        return self

    def __next__(self):
        """返回下一个元素"""
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value
```

---

## 生成器函数

使用 `yield` 暂停并返回值。

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(5):
    print(i)  # 5, 4, 3, 2, 1
```

### 生成器表达式

```python
(i**2 for i in range(10))  # 惰性求值
[i**2 for i in range(10)]  # 立即求值
```

---

## yield from

委托给另一个可迭代对象。

```python
def chain(*iterables):
    for it in iterables:
        yield from it

list(chain([1, 2], [3, 4]))  # [1, 2, 3, 4]
```

### 获取子生成器返回值

```python
def sub_gen():
    yield 1
    yield 2
    return "done"

def main_gen():
    result = yield from sub_gen()
    print(f"子生成器返回: {result}")

g = main_gen()
next(g)  # 1
next(g)  # 2
next(g)  # 打印 "子生成器返回: done"，然后 StopIteration
```

---

## 生成器方法

### send()

向生成器发送值。

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

g = accumulator()
next(g)        # 0，启动生成器
g.send(10)     # 10
g.send(5)      # 15
```

### throw()

向生成器抛出异常。

```python
def gen():
    try:
        yield 1
    except ValueError:
        yield "捕获异常"

g = gen()
next(g)              # 1
g.throw(ValueError)  # "捕获异常"
```

### close()

关闭生成器。

```python
g = countdown(10)
next(g)  # 10
g.close()
next(g)  # StopIteration
```

---

## 无限生成器

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
[next(fib) for _ in range(10)]  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## 管道模式

```python
def read_lines(file):
    for line in file:
        yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith('#'):
            yield line

def to_uppercase(lines):
    for line in lines:
        yield line.upper()

# 链式处理
with open('data.txt') as f:
    pipeline = to_uppercase(filter_comments(read_lines(f)))
    for line in pipeline:
        print(line)
```

---

## itertools 常用函数

```python
from itertools import *

count(10)           # 10, 11, 12, ... 无限计数
cycle('ABC')        # A, B, C, A, B, C, ... 无限循环
repeat(10, 3)       # 10, 10, 10 重复

chain([1], [2])     # 1, 2 连接
islice('ABCDEF', 2, 4)  # C, D 切片
takewhile(lambda x: x<5, count())  # 0, 1, 2, 3, 4
dropwhile(lambda x: x<5, count())  # 5, 6, 7, ...

product('AB', repeat=2)  # AA, AB, BA, BB 笛卡尔积
permutations('ABC', 2)   # AB, AC, BA, BC, CA, CB 排列
combinations('ABC', 2)   # AB, AC, BC 组合
```
