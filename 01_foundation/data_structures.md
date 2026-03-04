# 数据结构 ⭐入门

> 列表、元组、字典、集合 - Python 核心数据容器

---

## 列表 (list)

可变的有序序列。

### 基本操作

```python
# 索引访问
l[0]      # 第一个元素
l[-1]     # 最后一个元素
l[1:3]    # 切片 [1, 3)

# 添加元素
l.append(x)       # 末尾添加
l.extend(iter)    # 扩展可迭代对象
l.insert(i, x)    # 在索引 i 处插入

# 删除元素
l.remove(x)       # 删除第一个匹配项
l.pop([i])        # 弹出索引 i（默认末尾）

# 排序
l.sort()          # 原地排序
l.reverse()       # 原地反转
```

### 推导式

```python
# 列表推导式
[i**2 for i in range(10)]

# 带条件
[i for i in range(10) if i % 2 == 0]

# 嵌套
[[j for j in range(3)] for i in range(3)]
```

---

## 元组 (tuple)

不可变的有序序列。

```python
# 创建
t = (1, 2, 3)
t = 1, 2, 3        # 可省略括号

# 打包与解包
a = 1, 2, 3        # 打包
x, y, z = a        # 解包

# 单元素元组
t = (1,)           # 注意逗号
```

---

## 字典 (dict)

键值对映射。

### 基本操作

```python
# 访问
d.keys()           # 所有键
d.values()         # 所有值
d.items()          # 所有键值对

# 安全访问
d.get(k, default)  # 获取，不存在返回默认值
d.setdefault(k, v) # 获取，不存在则设置

# 修改
d.update(d2)       # 合并字典
d.pop(k)           # 删除并返回
```

### 初始化

```python
# 从键列表创建
d = dict.fromkeys([1, 2, 3], 0)
# {1: 0, 2: 0, 3: 0}
```

### 推导式

```python
{k: v for k, v in pairs}
{k: v**2 for k, v in d.items()}
```

---

## 集合 (set)

无序不重复元素集。

### 基本操作

```python
s.add(x)           # 添加元素
s.remove(x)        # 删除（不存在报错）
s.discard(x)       # 删除（不存在不报错）
```

### 集合运算

| 运算 | 说明 | 示例 |
|------|------|------|
| `&` | 交集 | `a & b` |
| `\|` | 并集 | `a \| b` |
| `-` | 差集 | `a - b` |
| `^` | 对称差集 | `a ^ b` |

### 推导式

```python
{i for i in range(10) if i % 2}
```

---

## 生成器表达式

```python
# 圆括号生成生成器对象，惰性求值
(i**2 for i in range(10))

# 对比列表推导式
[i**2 for i in range(10)]  # 立即生成列表
```

---

## 字符串方法

```python
split()      # 按指定字符分割为列表
join()       # 用指定字符串连接列表元素
replace()    # 替换子串
strip()      # 移除首尾空白字符
```

---

## 序列工具函数

| 函数 | 说明 |
|------|------|
| `sorted(iter, key=func)` | 排序，可多规则 |
| `filter(func, iter)` | 过滤 |
| `map(func, iter)` | 逐个运算 |
| `zip(*iters)` | 逐个重组 |
| `enumerate(iter)` | 返回索引和值 |
| `iter(obj)` | 转换为迭代器 |
