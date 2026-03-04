"""
工具函数示例

展示 tools.utils 模块中各种工具函数的使用方法。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import show, see, every, r_step, check, bases, line, count_chars


def demo_show():
    """演示 show() - 安全查看可迭代对象"""
    line()
    print("【show() 示例】")

    print("1. 查看有限列表:")
    show([1, 2, 3, 4, 5])

    print("2. 查看无限生成器 (end_at=1, 最多显示10个):")
    def infinite_counter():
        n = 0
        while True:
            yield n
            n += 1

    show(infinite_counter(), end_at=1)

    print("3. 查看无限生成器 (end_at=2, 最多显示100个):")
    show(infinite_counter(), end_at=2)


def demo_see():
    """演示 see() - 查看对象属性和方法"""
    line()
    print("【see() 示例】")

    print("1. 查看字符串对象的方法:")
    see("hello", simple=1)

    print("2. 查看自定义类:")
    class MyClass:
        """我的类"""
        def __init__(self):
            self.value = 42

        def method(self):
            """我的方法"""
            pass

    see(MyClass(), simple=1)


def demo_every():
    """演示 every() - 扁平化嵌套可迭代对象"""
    line()
    print("【every() 示例】")

    nested = [1, [2, 3], [[4, 5], 6], [[[7]]]]
    print(f"原始嵌套结构: {nested}")
    flattened = list(every(nested))
    print(f"扁平化结果: {flattened}")

    print("\n注意: 字符串被视为原子元素，不会被拆分:")
    mixed = ["hello", [1, 2], ["world"]]
    print(f"原始: {mixed}")
    print(f"结果: {list(every(mixed))}")


def demo_r_step():
    """演示 r_step() - 可迭代对象分组"""
    line()
    print("【r_step() 示例】")

    data = list(range(10))
    print(f"原始数据: {data}")

    print("\n按步长3分组:")
    for group in r_step(data, 3):
        print(f"  {group}")

    print("\n按步长4分组:")
    for group in r_step(data, 4):
        print(f"  {group}")


def demo_check():
    """演示 check() - 全局命名冲突检查"""
    line()
    print("【check() 示例】")

    print("检查变量名 'data', 'result', 'x', 'y' 是否与内置或全局冲突:")
    available = check("data", "result", "x", "y", letters="")
    print(f"可用名称: {available}")


def demo_bases():
    """演示 bases() - 查看类继承树"""
    line()
    print("【bases() 示例】")

    class A:
        pass

    class B(A):
        pass

    class C(B):
        pass

    print("查看类 C 的继承树:")
    bases(C)


def demo_count_chars():
    """演示 count_chars() - 统计文件字符数"""
    line()
    print("【count_chars() 示例】")

    print("统计当前示例目录下的 Python 文件字符数:")
    result = count_chars(
        path=Path(__file__).parent,
        extension=".py",
        recursive=False
    )


if __name__ == "__main__":
    demo_show()
    demo_see()
    demo_every()
    demo_r_step()
    demo_check()
    demo_bases()
    demo_count_chars()
    line()
