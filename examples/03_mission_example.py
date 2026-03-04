"""
工具类示例

展示 tools.mission 模块中各种工具类的使用方法。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import Catch, TestFile, Mission, Create, Frange, crt, r, line


def _compute_square(n: int) -> int:
    """计算平方（用于 Mission 示例）"""
    return n * n


def _compute_cube(n: int) -> int:
    """计算立方（用于 Mission 示例）"""
    return n * n * n


def demo_catch():
    """演示 Catch - 异常捕获上下文管理器"""
    line()
    print("【Catch 上下文管理器示例】")

    print("1. 基本用法 - 捕获异常并抑制传播:")
    with Catch():
        result = 10 / 0
    print("  异常已被捕获，程序继续执行")

    print("\n2. 带名称的上下文:")
    with Catch(name="危险操作"):
        result = 10 / 0

    print("\n3. 不抑制异常传播 (e=False):")
    try:
        with Catch(name="测试", e=False):
            result = 10 / 0
    except ZeroDivisionError:
        print("  异常向上传播，被外层捕获")


def demo_test_file():
    """演示 TestFile - 测试文件上下文管理器"""
    line()
    print("【TestFile 上下文管理器示例】")

    print("1. 创建 1KB 测试文件:")
    with TestFile(1) as tf:
        content = tf.read()
        print(f"  文件大小: {len(content)} 字符")

    print("\n2. 创建自定义文件:")
    with TestFile(size=2, filename="custom_test.txt", content="AB") as tf:
        content = tf.read()
        print(f"  文件内容前20字符: {content[:20]}...")

    print("\n3. 文件已自动清理")


def demo_mission():
    """演示 Mission - 并行任务执行"""
    line()
    print("【Mission 并行任务示例】")

    mission = Mission()
    mission.add(_compute_square, 5)
    mission.add(_compute_square, 10)
    mission.add(_compute_cube, 3)

    print("执行并行任务:")
    for i, result in enumerate(mission):
        print(f"  任务 {i + 1} 结果: {result}")


def demo_create():
    """演示 Create / crt - 数据结构快速创建"""
    line()
    print("【Create 数据结构创建示例】")

    print(f"随机列表 (crt.l): {crt.l}")
    print(f"元组 (crt.t): {crt.t}")
    print(f"字典 (crt.d): {crt.d}")
    print(f"集合 (crt.s): {crt.s}")
    print(f"字符串 (crt.st): {crt.st}")

    print("\n每次访问都会生成新的随机数据:")
    print(f"新的列表: {crt.l}")


def demo_frange():
    """演示 Frange / r - 范围生成器"""
    line()
    print("【Frange 范围生成器示例】")

    print("1. 整数范围:")
    print(f"  r(5): {list(r(5))}")
    print(f"  r(-3): {list(r(-3))}")

    print("\n2. 浮点数范围:")
    print(f"  r(1.5): {list(r(1.5))}")
    print(f"  r(-2.3): {list(r(-2.3))}")

    print("\n3. 罗马数字风格 (i=1, v=5, x=10):")
    print(f"  r.iii: {list(r.iii)}")
    print(f"  r.v: {list(r.v)}")
    print(f"  r.x: {list(r.x)}")
    print(f"  r.iv: {list(r.iv)}")
    print(f"  r.ix: {list(r.ix)}")


if __name__ == "__main__":
    demo_catch()
    demo_test_file()
    demo_mission()
    demo_create()
    demo_frange()
    line()
