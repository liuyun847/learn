# 面向对象编程 ⭐⭐进阶

> 类、继承、多态、封装 - Python OOP 核心概念

---

## 类定义

```python
class A:
    class_attr = "类属性"  # 所有实例共享

    def __init__(self, x):
        self.x = x  # 实例属性，每个实例独立

    def method(self):
        return self.x
```

### 查看属性

```python
obj.__dict__  # 查看实例属性
dir(obj)      # 查看所有属性（包括继承）
```

---

## 继承

```python
class B(A):
    def __init__(self, x, y):
        super().__init__(x)  # 调用父类方法
        self.y = y
```

### 多继承与 MRO

```python
class C(A, B):
    pass

C.__mro__  # 方法解析顺序
```

### 钻石继承

```python
class A:
    def __init__(self):
        print("A")

class B1(A):
    def __init__(self):
        A.__init__(self)  # 直接调用会导致重复
        print("B1")

class B2(A):
    def __init__(self):
        A.__init__(self)
        print("B2")

class C(B1, B2):
    def __init__(self):
        B1.__init__(self)
        B2.__init__(self)  # A 被调用两次！

# 解决方案：使用 super()
class B1(A):
    def __init__(self):
        super().__init__()
        print("B1")
```

---

## 多态

同一操作对不同对象执行不同行为。

```python
class Dog:
    def speak(self):
        return "汪"

class Cat:
    def speak(self):
        return "喵"

def animal_sound(animal):
    return animal.speak()  # 统一接口

animal_sound(Dog())  # "汪"
animal_sound(Cat())  # "喵"
```

---

## 私有变量

```python
class A:
    def __init__(self):
        self.__private = 1  # 私有变量
        self._internal = 2  # 约定内部使用

    def __private_method(self):
        pass

# 实际存储为 _A__private
obj._A__private  # 可以访问但不推荐
```

---

## __slots__

限制可添加的属性，减少内存占用。

```python
class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3  # AttributeError
```

---

## Mixin 模式

水平组合，功能注入。

```python
class LogMixin:
    def log(self, msg):
        print(f"[LOG] {msg}")

class SerializableMixin:
    def to_dict(self):
        return self.__dict__

class User(LogMixin, SerializableMixin):
    def __init__(self, name):
        self.name = name

u = User("Alice")
u.log("created")     # 来自 LogMixin
u.to_dict()          # 来自 SerializableMixin
```

---

## 重写与禁用

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"  # 重写

class C(A):
    method = None   # 禁用方法

C().method()  # TypeError
```

---

## 类型检查

```python
type(obj)          # 返回对象的类
isinstance(obj, A) # 检查是否为 A 的实例（考虑继承）
issubclass(B, A)   # 检查是否为 A 的子类
```
