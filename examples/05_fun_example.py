"""
语言特性示例

展示 fun.language_tricks 模块中各种有趣的 Python 语言特性演示。

⚠️ 警告：此模块中的代码仅为娱乐和探索 Python 语言特性而编写，
不建议在生产环境或实际项目中使用！
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fun.language_tricks import find, Point, print_flow, import_, as_obj, line


def demo_find():
    """演示 find() - 利用魔术方法判断奇偶"""
    line()
    print("【find() 奇偶判断示例】")
    print("原理：构造调用链 C()()()... 利用 __call__ 和 __repr__")

    for i in range(6):
        print(f"  find({i}) -> ", end="")
        find(i)


def demo_point():
    """演示 Point - 模拟 C 语言指针"""
    line()
    print("【Point 指针模拟示例】")

    point = Point()
    print(f"创建指针: {point}")

    point *= "Hello, Pointer!"
    print(f"存储数据: point *= 'Hello, Pointer!'")

    value = ... * point
    print(f"获取数据: ... * point = '{value}'")

    point *= 42
    print(f"存储新数据: point *= 42")
    print(f"获取新数据: ... * point = { ... * point}")


def demo_print_flow():
    """演示 print_flow() - 打字机效果输出"""
    line()
    print("【print_flow() 打字机效果示例】")

    print_flow("这是一段打字机效果的文字输出", time_step=0.05)


def demo_import_():
    """演示 import_() - 动态导入模块"""
    line()
    print("【import_() 动态导入示例】")

    print("1. 导入指定模块:")
    import_("os", "sys", "json")
    print(f"  已导入: os, sys, json")
    print(f"  os.name = {os.name}")
    print(f"  sys.version_info.major = {sys.version_info.major}")

    print("\n2. 导入所有标准库模块 (import_('*')):")
    print("  此操作会导入大量模块，这里仅演示概念")


def demo_as_obj():
    """演示 as_obj - 类装饰器返回实例"""
    line()
    print("【as_obj 类装饰器示例】")

    @as_obj
    class Singleton:
        """无参数调用，直接返回实例"""
        value = 42

    print(f"  type(Singleton) = {type(Singleton)}")
    print(f"  Singleton.value = {Singleton.value}")

    @as_obj(1, 2, name="test")
    class Config:
        """带参数调用，参数传给 __init__"""
        def __init__(self, x, y, name):
            self.x = x
            self.y = y
            self.name = name

    print(f"\n  type(Config) = {type(Config)}")
    print(f"  Config.x = {Config.x}, Config.y = {Config.y}, Config.name = {Config.name}")


if __name__ == "__main__":
    demo_find()
    demo_point()
    demo_print_flow()
    demo_import_()
    demo_as_obj()
    line()
