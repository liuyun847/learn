# 魔法方法 ⭐⭐进阶

> Python 特殊方法详解 - 自定义类的行为

---

## 创建与销毁

### __new__ 与 __init__

```python
class A:
    def __new__(cls, *args, **kwargs):
        """创建实例，在 __init__ 之前调用"""
        instance = super().__new__(cls)
        return instance

    def __init__(self, x):
        """初始化实例"""
        self.x = x

    def __del__(self):
        """析构，实例被回收时调用"""
        pass
```

---

## 运算方法

### 算术运算

| 方法 | 运算符 | 说明 |
|------|--------|------|
| `__add__` | `+` | 加法 |
| `__sub__` | `-` | 减法 |
| `__mul__` | `*` | 乘法 |
| `__truediv__` | `/` | 除法 |
| `__floordiv__` | `//` | 整除 |
| `__mod__` | `%` | 取余 |
| `__pow__` | `**` | 幂 |

### 反向运算

当左侧对象未实现对应方法时调用。

```python
__radd__      # 右侧加法
__rsub__      # 右侧减法
__rmul__      # 右侧乘法
```

### 增量运算

```python
__iadd__      # +=
__isub__      # -=
__imul__      # *=
```

---

## 属性访问

### 基本方法

```python
class A:
    def __getattribute__(self, name):
        """拦截所有属性访问（有递归风险）"""
        return super().__getattribute__(name)

    def __getattr__(self, name):
        """拦截未定义属性访问"""
        return f"属性 {name} 不存在"

    def __setattr__(self, name, value):
        """拦截属性赋值"""
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """拦截属性删除"""
        super().__delattr__(name)
```

### 避免递归

```python
def __setattr__(self, name, value):
    # 方式1：直接操作 __dict__
    self.__dict__[name] = value
    # 方式2：调用父类
    super().__setattr__(name, value)
```

---

## 索引与切片

```python
class MyList:
    def __getitem__(self, key):
        """拦截索引访问：obj[key]"""
        if isinstance(key, slice):
            # 处理切片
            start, stop, step = key.start, key.stop, key.step
        return self.data[key]

    def __setitem__(self, key, value):
        """拦截索引赋值：obj[key] = value"""
        self.data[key] = value

    def __delitem__(self, key):
        """拦截索引删除：del obj[key]"""
        del self.data[key]

    def __index__(self):
        """对象作为索引时调用"""
        return int(self.value)
```

---

## 迭代方法

```python
class MyIter:
    def __iter__(self):
        """返回迭代器（用于 for 循环）"""
        return self

    def __next__(self):
        """返回下一个元素"""
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value

    def __contains__(self, item):
        """拦截 in 操作"""
        return item in self.data
```

---

## 比较方法

```python
class A:
    def __eq__(self, other):   return self.value == other.value
    def __ne__(self, other):   return self.value != other.value
    def __lt__(self, other):   return self.value < other.value
    def __le__(self, other):   return self.value <= other.value
    def __gt__(self, other):   return self.value > other.value
    def __ge__(self, other):   return self.value >= other.value
```

---

## 字符串表示

```python
class A:
    def __str__(self):
        """str() 或 print() 时调用"""
        return "用户友好的字符串"

    def __repr__(self):
        """repr() 时调用，可代偿 __str__"""
        return "A(value=...)"
```

---

## 可调用对象

```python
class A:
    def __call__(self, *args, **kwargs):
        """使实例可调用：obj()"""
        return args
```

---

## 上下文管理器

```python
class A:
    def __enter__(self):
        """进入 with 语句时调用"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 语句时调用"""
        if exc_type:
            print(f"异常: {exc_val}")
        return True  # 抑制异常传播
```

---

## 代偿机制

当未实现某方法时，Python 会查找替代方法：

```python
# in 操作的代偿链
__contains__ → __iter__ → __getitem__

# 比较操作的代偿
__eq__ 未实现 → 使用 is 比较
__lt__ 未实现 → 抛出 TypeError
```
