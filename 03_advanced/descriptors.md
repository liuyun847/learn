# 描述符 ⭐⭐⭐高级

> 精细控制属性访问的核心机制

---

## 描述符协议

实现了 `__get__`、`__set__`、`__delete__` 中至少一个的类。

```python
class Descriptor:
    def __get__(self, instance, owner):
        """拦截属性访问"""
        pass

    def __set__(self, instance, value):
        """拦截属性赋值"""
        pass

    def __delete__(self, instance):
        """拦截属性删除"""
        pass

    def __set_name__(self, owner, name):
        """Python 3.6+：设置属性名"""
        pass
```

---

## 数据描述符与非数据描述符

| 类型 | 实现方法 | 优先级 |
|------|---------|--------|
| 数据描述符 | `__get__` + `__set__` | 最高 |
| 非数据描述符 | 仅 `__get__` | 低于实例字典 |

---

## 属性查找顺序

```python
# 访问 obj.attr 时：
1. __getattribute__
2. 数据描述符.__get__
3. obj.__dict__['attr']
4. 非数据描述符.__get__
5. 类.__dict__['attr']
6. 父类.__dict__['attr']
7. __getattr__
```

---

## 基本示例

### 只读属性

```python
class ReadOnly:
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        raise AttributeError("只读属性")

class A:
    x = ReadOnly(10)

a = A()
a.x      # 10
a.x = 20 # AttributeError
```

### 类型检查

```python
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} 应为 {self.expected_type}")
        instance.__dict__[self.name] = value

class Person:
    name = Typed('name', str)
    age = Typed('age', int)

p = Person()
p.name = "Alice"  # OK
p.name = 100      # TypeError
```

---

## __set_name__

Python 3.6+ 新增，自动获取属性名。

```python
class Descriptor:
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)

class A:
    x = Descriptor()  # 自动设置 name='x', private_name='_x'
```

---

## property 的实现原理

`property` 本身是一个描述符类。

```python
class Property:
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("只读属性")
        self.fset(instance, value)

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self
```

---

## 类方法和静态方法的实现

### 函数作为描述符

```python
class Function:
    def __get__(self, instance, owner):
        if instance is None:
            return self  # 通过类访问，返回函数
        return Method(self, instance)  # 通过实例访问，返回绑定方法
```

### ClassMethod

```python
class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return lambda *args, **kwargs: self.func(owner, *args, **kwargs)
```

### StaticMethod

```python
class StaticMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func
```

---

## 延迟计算属性

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        instance.__dict__[self.name] = value  # 缓存到实例
        return value

class A:
    @LazyProperty
    def expensive(self):
        print("计算中...")
        return sum(range(1000000))

a = A()
a.expensive  # 打印 "计算中..."
a.expensive  # 直接返回缓存值
```

---

## 描述符 vs __getattribute__

| 特点 | 描述符 | __getattribute__ |
|------|--------|------------------|
| 粒度 | 特定属性 | 所有属性 |
| 复用性 | 可在多个类中复用 | 每个类单独实现 |
| 继承 | 自动继承 | 需要调用 super() |
| 复杂度 | 较低 | 较高 |
