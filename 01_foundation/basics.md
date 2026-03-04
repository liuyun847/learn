# 基础语法 ⭐入门

> 变量、运算符、控制流 - Python 编程的基石

---

## 变量与基本数据类型

```python
int     # 整数
float   # 浮点数
str     # 字符串
bool    # 布尔值
None    # 空值
```

### 类型转换

```python
int()       # 转整数
str()       # 转字符串
float()     # 转浮点数
list()      # 转列表
tuple()     # 转元组
set()       # 转集合
dict()      # 转字典
```

---

## 运算符

### 算术运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `+` | 加 | `1 + 2` → `3` |
| `-` | 减 | `3 - 1` → `2` |
| `*` | 乘 | `2 * 3` → `6` |
| `/` | 除 | `6 / 2` → `3.0` |
| `//` | 取整除 | `7 // 2` → `3` |
| `%` | 取余 | `7 % 2` → `1` |
| `**` | 幂 | `2 ** 3` → `8` |

### 比较运算符

```python
==  # 等于
!=  # 不等于
<   # 小于
<=  # 小于等于
>   # 大于
>=  # 大于等于
```

### 逻辑运算符

```python
and  # 与
or   # 或
not  # 非
```

### 赋值运算符

```python
=   # 赋值
+=  # 加赋值
-=  # 减赋值
*=  # 乘赋值
/=  # 除赋值
```

### 成员运算符

```python
in       # 在...中
not in   # 不在...中
```

### 身份运算符

```python
is       # 是同一对象
is not   # 不是同一对象
```

---

## 控制流

### 条件判断

```python
if condition:
    ...
elif condition:
    ...
else:
    ...
```

### 遍历循环

```python
for i in range(n):
    ...

for k, v in dict.items():
    ...
```

### 条件循环

```python
while condition:
    ...
```

### 循环控制

| 语句 | 说明 |
|------|------|
| `break` | 跳出循环 |
| `continue` | 跳过本次迭代 |
| `pass` | 空操作占位 |

### 循环 else 子句

```python
for i in range(10):
    if i == 20:
        break
else:
    print("循环未被 break 时执行")
```

---

## 新特性速览

### 海象运算符 (Python 3.8+)

```python
# 在表达式中赋值
if (n := len(data)) > 10:
    print(f"数据过长: {n} 个元素")
```

### 位置参数限定 (Python 3.8+)

```python
def func(a, /, b, *, c):
    """
    a: 仅位置参数
    b: 位置或关键字参数
    c: 仅关键字参数
    """
    pass
```

### 模式匹配 (Python 3.10+)

```python
match x:
    case 1 | 2:
        print('x is 1 or 2')
    case _:
        print(f'x={x} is not 1 or 2')

# 带守卫条件
match x:
    case n if isinstance(n, int):
        print(f'整数: {n}')
```

### 异常组 (Python 3.11+)

```python
try:
    ...
except* ValueError as e:
    # 捕获多个异常
    pass
```
