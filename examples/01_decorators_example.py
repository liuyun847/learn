"""
装饰器示例

展示 tools.decorators 模块中各种装饰器的使用方法。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import log, catch, now, reg, Dec, abc_def, set_OPEN, line


def demo_log():
    """演示 @log 装饰器 - 函数执行日志记录"""
    line()
    print("【@log 装饰器示例】")

    @log
    def factorial(n: int) -> int:
        """递归计算阶乘"""
        return 1 if n <= 1 else n * factorial(n - 1)

    result = factorial(5)
    print(f"\n最终结果: {result}")


def demo_catch():
    """演示 @catch 装饰器 - 异常捕获"""
    line()
    print("【@catch 装饰器示例】")

    @catch
    def risky_divide(a: int, b: int) -> float:
        return a / b

    risky_divide(10, 2)
    risky_divide(10, 0)
    risky_divide(10, 5)


def demo_now():
    """演示 @now 装饰器 - 立即执行"""
    line()
    print("【@now 装饰器示例】")

    print("设置 OPEN=True 后，函数会在装饰时立即执行:")
    set_OPEN(True)

    @now
    def greet():
        print("  你好，我是被 @now 立即执行的函数！")

    print("\n设置 OPEN=False 后，函数不会立即执行:")
    set_OPEN(False)

    @now
    def no_run():
        print("  这条消息不会打印")

    print("  (函数未被立即执行)")

    set_OPEN(True)


def demo_reg():
    """演示 @reg 装饰器 - 函数注册"""
    line()
    print("【@reg 装饰器示例】")

    @reg
    def func_a():
        """函数A的文档"""
        pass

    @reg
    def func_b():
        """函数B的文档"""
        pass

    @reg
    def func_c():
        """函数C的文档"""
        pass

    print(f"已注册 {len(reg.reged)} 个函数:")
    for name, doc, func in reg.reged:
        print(f"  - {name}: {doc}")


def demo_dec():
    """演示 Dec 类 - 链式装饰器"""
    line()
    print("【Dec 链式装饰器示例】")

    @Dec
    def divide(a: int, b: int) -> float:
        return a / b

    print("1. 基本使用 - 前置/后置回调:")
    result = (
        divide.before(lambda: print("  开始计算..."))
        .after(lambda: print("  计算完成!"))
        (10, 2)
    )
    print(f"  结果: {result}")

    print("\n2. 参数转换:")
    result = divide.change_arg(lambda args, kwargs: ((20, 4), kwargs))(1, 1)
    print(f"  结果: {result}")

    print("\n3. 异常处理:")
    result = divide.on_error(lambda e: f"错误: {e}")(10, 0)
    print(f"  结果: {result}")

    print("\n4. 返回值处理:")
    result = divide.change_result(lambda x: f"计算结果是 {x}")(10, 5)
    print(f"  结果: {result}")


def demo_abc_def():
    """演示 @abc_def 装饰器 - 严格抽象基类"""
    line()
    print("【@abc_def 装饰器示例】")

    from abc import abstractmethod

    @abc_def
    class Animal:
        @abstractmethod
        def speak(self) -> str:
            pass

    print("定义抽象基类 Animal，包含抽象方法 speak")

    try:

        class Dog(Animal):
            pass

        Dog()
    except TypeError as e:
        print(f"未实现抽象方法时实例化: {e}")

    class Cat(Animal):
        def speak(self) -> str:
            return "喵喵喵"

    cat = Cat()
    print(f"实现抽象方法后: Cat().speak() = '{cat.speak()}'")


if __name__ == "__main__":
    demo_log()
    demo_catch()
    demo_now()
    demo_reg()
    demo_dec()
    demo_abc_def()
    line()
