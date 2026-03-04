# 元编程 ⭐⭐⭐高级

> 元类、动态属性、代码生成 - Python 的黑魔法

---

## type() 函数

### 查看类型

```python
type(obj)      # 返回对象的类
type(type)     # <class 'type'>，type 是自己的实例
```

### 动态创建类

```python
# class A:
#     x = 1
A = type('A', (), {'x': 1})

# class B(A):
#     y = 2
B = type('B', (A,), {'y': 2})
```

---

## 元类

元类是创建类的类。

```python
class Meta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        """创建类时调用"""
        print(f"创建类: {name}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __init__(cls, name, bases, namespace, **kwargs):
        """初始化类时调用"""
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        """实例化时调用"""
        return super().__call__(*args, **kwargs)

class A(metaclass=Meta):
    x = 1
# 打印: 创建类: A
```

### 常见用途

| 用途 | 说明 |
|------|------|
| 单例模式 | 控制实例化 |
| 注册机制 | 自动注册子类 |
| 接口检查 | 验证方法实现 |
| 属性转换 | 自动处理属性 |

### 单例示例

```python
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class A(metaclass=Singleton):
    pass

a1 = A()
a2 = A()
a1 is a2  # True
```

---

## __init_subclass__

在父类中定义子类初始化行为。

```python
class PluginBase:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PluginBase.registry.append(cls)

class PluginA(PluginBase):
    pass

class PluginB(PluginBase):
    pass

PluginBase.registry  # [PluginA, PluginB]
```

---

## 动态属性

### __getattr__ 与 __setattr__

```python
class Dynamic:
    def __getattr__(self, name):
        """访问不存在的属性时调用"""
        return f"动态创建: {name}"

    def __setattr__(self, name, value):
        """设置属性时调用"""
        self.__dict__[name] = value
```

### __getattribute__

拦截所有属性访问。

```python
class A:
    def __getattribute__(self, name):
        """注意：容易导致无限递归"""
        # 错误：return self.name
        # 正确：
        return object.__getattribute__(self, name)
```

---

## 动态导入

```python
import importlib

# 方式1
module = importlib.import_module('os.path')

# 方式2：通过字符串导入
module = __import__('os.path')
```

---

## 在调用者命名空间创建变量

```python
import inspect

def create_global(name, value):
    """在调用者的全局命名空间创建变量"""
    frame = inspect.currentframe().f_back
    frame.f_globals[name] = value

def test():
    create_global('x', 100)
    print(x)  # 100
```

---

## exec 与 eval

```python
# 执行代码字符串
exec("x = 1 + 2")
print(x)  # 3

# 计算表达式
result = eval("1 + 2 * 3")  # 7

# 带命名空间
namespace = {}
exec("y = 10", namespace)
print(namespace['y'])  # 10
```

---

## 类装饰器

```python
def add_method(cls):
    def new_method(self):
        return "新增方法"
    cls.new_method = new_method
    return cls

@add_method
class A:
    pass

A().new_method()  # "新增方法"
```

### 替换类

```python
def replace_class(cls):
    class NewClass:
        def __init__(self, *args, **kwargs):
            self.original = cls(*args, **kwargs)

        def extra(self):
            return "额外功能"
    return NewClass
```

---

## 注意事项

> ⚠️ 元编程强大但危险：
> - 增加代码复杂度
> - 难以调试
> - 可能影响性能
> - 优先考虑装饰器、继承等简单方案
