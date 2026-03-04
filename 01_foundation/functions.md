# 函数基础 ⭐入门

> 函数定义、参数、作用域 - 代码复用的基础

---

## 函数定义

```python
def func(args):
    """文档字符串"""
    ...
    return value
```

---

## 参数类型

### 位置参数

```python
def func(a, b, c):
    pass

func(1, 2, 3)
```

### 默认参数

```python
def func(a, b=2):
    pass

func(1)      # b 使用默认值
func(1, 3)   # b 覆盖默认值
```

### 关键字参数

```python
def func(a, b):
    pass

func(b=2, a=1)  # 顺序无关
```

### 收集参数

```python
def func(*args):       # 收集位置参数为元组
    pass

def func(**kwargs):    # 收集关键字参数为字典
    pass

def func(*args, **kwargs):  # 组合使用
    pass
```

### 解包参数

```python
def func(a, b, c):
    pass

args = [1, 2, 3]
func(*args)        # 解包列表

kwargs = {'a': 1, 'b': 2, 'c': 3}
func(**kwargs)     # 解包字典
```

---

## 作用域

### global 关键字

```python
x = 1

def func():
    global x
    x = 2  # 修改全局变量

func()
print(x)  # 2
```

### nonlocal 关键字

```python
def outer():
    x = 1
    def inner():
        nonlocal x
        x = 2  # 修改外层变量
    inner()
    return x  # 2
```

---

## 返回值

```python
def func():
    return 1, 2, 3  # 返回元组

a, b, c = func()   # 解包接收
```

---

## 闭包

函数 + 嵌套环境 = 闭包

```python
def outer(n):
    def inner(x):
        return x ** n
    return inner

square = outer(2)
cube = outer(3)

square(5)  # 25
cube(5)    # 125
```

### 闭包捕获变量

```python
# 常见陷阱
funcs = [lambda: i for i in range(3)]
[f() for f in funcs]  # [2, 2, 2]

# 解决方案：默认参数捕获
funcs = [lambda i=i: i for i in range(3)]
[f() for f in funcs]  # [0, 1, 2]
```

---

## 装饰器基础

装饰器 = 接收函数并返回函数的函数

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("前置操作")
        result = func(*args, **kwargs)
        print("后置操作")
        return result
    return wrapper

@decorator
def func():
    pass

# 等价于
func = decorator(func)
```

### 多层装饰器

```python
@decorator1
@decorator2
def func():
    pass

# 等价于
func = decorator1(decorator2(func))
```

---

## 生成器

使用 `yield` 输出并暂停。

```python
def gen(n):
    for i in range(n):
        yield i

g = gen(3)
next(g)  # 0
next(g)  # 1
next(g)  # 2
next(g)  # StopIteration
```

### yield from

```python
def gen():
    yield from [1, 2, 3]  # 委托给另一个可迭代对象
```

---

## 递归

```python
def factorial(n):
    # 停止条件
    if n <= 1:
        return 1
    # 转移分解
    return n * factorial(n - 1)
```
