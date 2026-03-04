# 抽象基类 ⭐⭐⭐高级

> 定义接口规范，提前发现设计问题

---

## 基本用法

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        """子类必须实现"""
        pass

    @abstractmethod
    def move(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪"

    def move(self):
        return "跑"

# Animal()  # TypeError: 无法实例化抽象类
Dog()       # OK
```

---

## 抽象属性

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @property
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14 * self.radius ** 2
```

---

## 抽象类方法

```python
class Base(ABC):
    @classmethod
    @abstractmethod
    def from_string(cls, s):
        pass

class User(Base):
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_string(cls, s):
        return cls(s.split(':')[1])

User.from_string("name:Alice")
```

---

## 钩子方法

抽象基类可以提供默认实现。

```python
class Comparable(ABC):
    @abstractmethod
    def __lt__(self, other):
        pass

    # 提供默认实现
    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
```

---

## 严格抽象基类

在类定义阶段检查抽象方法实现。

```python
from abc import ABCMeta, abstractmethod

class StrictABCMeta(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        abstract_methods = getattr(cls, '__abstractmethods__', frozenset())
        if not abstract_methods:
            return cls

        # 获取父类的抽象方法
        parent_abstract = frozenset()
        for base in bases:
            if hasattr(base, '__abstractmethods__'):
                parent_abstract |= base.__abstractmethods__

        # 如果定义了新的抽象方法，是抽象基类
        new_abstract = abstract_methods - parent_abstract
        if new_abstract:
            return cls

        # 检查是否实现了所有继承的抽象方法
        for method_name in abstract_methods:
            method = getattr(cls, method_name, None)
            if getattr(method, '__isabstractmethod__', False):
                raise TypeError(f"类 '{name}' 未实现抽象方法 '{method_name}'")

        return cls

def abc_def(cls):
    """装饰器：应用严格抽象基类元类"""
    namespace = dict(cls.__dict__)
    namespace.pop('__dict__', None)
    namespace.pop('__weakref__', None)
    return StrictABCMeta(cls.__name__, cls.__bases__, namespace)
```

---

## 注册机制

非子类也可以注册为抽象基类的虚拟子类。

```python
class MyContainer(ABC):
    @abstractmethod
    def add(self, item):
        pass

@MyContainer.register
class MyList:
    def add(self, item):
        self.append(item)

issubclass(MyList, MyContainer)  # True
isinstance(MyList(), MyContainer)  # True
```

---

## 标准库抽象基类

```python
from collections.abc import (
    Container,    # __contains__
    Iterable,     # __iter__
    Iterator,     # __iter__, __next__
    Sequence,     # __getitem__, __len__
    MutableSequence,
    Mapping,
    MutableMapping,
    Callable,
)

# 检查是否可迭代
isinstance([1, 2, 3], Iterable)  # True

# 检查是否可调用
isinstance(lambda: None, Callable)  # True
```

---

## 设计原则

| 原则 | 说明 |
|------|------|
| 接口分离 | 定义小而专注的抽象基类 |
| 组合优于继承 | 抽象基类用于定义接口，不是代码复用 |
| 鸭子类型优先 | 不需要时不用抽象基类 |

### 示例：插件系统

```python
class PluginBase(ABC):
    @abstractmethod
    def execute(self, data):
        pass

    @classmethod
    @abstractmethod
    def name(cls):
        pass

class PluginA(PluginBase):
    @classmethod
    def name(cls):
        return "PluginA"

    def execute(self, data):
        return data.upper()

# 插件注册
PLUGINS = {}

def register_plugin(cls):
    PLUGINS[cls.name()] = cls
    return cls

@register_plugin
class PluginB(PluginBase):
    ...
```
