# 装饰器 ⭐⭐进阶

> 函数装饰器的原理与应用

---

## 基本原理

装饰器是接收函数并返回函数的可调用对象。

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # 前置操作
        result = func(*args, **kwargs)
        # 后置操作
        return result
    return wrapper

@decorator
def func():
    pass

# 等价于
func = decorator(func)
```

---

## functools.wraps

保留原函数的元数据。

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

func.__name__  # 保留原函数名
func.__doc__   # 保留原文档字符串
```

---

## 带参数的装饰器

```python
def decorator(arg):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"装饰器参数: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return inner

@decorator("hello")
def func():
    pass

# 等价于
func = decorator("hello")(func)
```

---

## 类装饰器

```python
class Decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("前置操作")
        result = self.func(*args, **kwargs)
        print("后置操作")
        return result

@Decorator
def func():
    pass
```

---

## 常用装饰器模式

### 日志装饰器

```python
def log(func):
    count = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"调用 {func.__name__} 第 {count} 次")
        return func(*args, **kwargs)
    return wrapper
```

### 缓存装饰器

```python
def cache(func):
    cached = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    return wrapper
```

### 重试装饰器

```python
def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times - 1:
                        raise
                    print(f"重试 {i+1}/{times}")
        return wrapper
    return decorator
```

---

## 类方法与静态方法

```python
class A:
    @classmethod
    def class_method(cls):
        """绑定到类，首参数为类本身"""
        return cls

    @staticmethod
    def static_method():
        """不绑定实例或类，普通函数"""
        pass

    @property
    def prop(self):
        """属性访问器"""
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value
```

---

## 多层装饰器

```python
@decorator1
@decorator2
def func():
    pass

# 执行顺序：decorator1 → decorator2 → func
# 等价于
func = decorator1(decorator2(func))
```

---

## 类装饰器（装饰类）

```python
def add_method(cls):
    cls.new_method = lambda self: "新增方法"
    return cls

@add_method
class A:
    pass

A().new_method()  # "新增方法"
```
