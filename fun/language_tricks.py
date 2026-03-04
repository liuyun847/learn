"""
好玩代码集合模块 (For Fun Only)

⚠️ 警告：此模块中的代码仅为娱乐和探索 Python 语言特性而编写，
不建议在生产环境或实际项目中使用！

本模块包含各种利用 Python 魔法方法、元编程技巧和语言特性
实现的有趣但非实用的功能，旨在展示 Python 的灵活性和趣味性。

内容概览：
    - find 利用 __call__ 和 __repr__ 判断数字奇偶性
    - Point 使用魔法方法模拟 C 语言指针语法
    - print_flow 打字机效果的文字输出
    - init 文件初始化模板工具
    - import_ 动态导入模块工具
    - glb 元编程：在调用者模块中动态创建全局变量
    - as_obj 类装饰器，使类定义时直接返回实例

使用建议：
    - 仅供学习 Python 语言特性参考
    - 不要在正式代码中模仿这些写法
    - 理解原理即可，不要复制到生产环境

作者注：
    写这些代码的目的是探索 Python 的边界，展示语言的趣味性。
    真正的 Pythonic 代码应该清晰、简洁、可读性强。
"""

__all__ = [
    "find",
    "Point",
    "print_flow",
    "init",
    "import_",
    "glb",
    "as_obj",
]

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import *
from typing import Any, TypeVar, overload, Callable
import time
import inspect
import importlib


T = TypeVar("T")


@overload
def as_obj(cls: type[T]) -> T: ...


@overload
def as_obj(*args: Any, **kwargs: Any) -> Callable[[type[T]], T]: ...


def as_obj(*args: Any, **kwargs: Any) -> T | Callable[[type[T]], T]:
    """
    类装饰器，使被装饰的类在定义时直接返回实例而非类本身。

    支持两种使用方式：
        1. 无参数调用: @as_obj
           - 直接使用类作为参数，返回无参构造的实例
        2. 带参数调用: @as_obj(arg1, arg2, kwarg1=value1)
           - 将参数传递给类的 __init__ 方法构造实例

    Args:
        *args: 位置参数。如果是无括号调用，第一个参数是被装饰的类；
               如果是带括号调用，这些参数会传给类的 __init__
        **kwargs: 关键字参数，会传给类的 __init__

    Returns:
        无括号调用时直接返回实例；带括号调用时返回装饰器函数

    Example:
        >>> @as_obj
        ... class A:
        ...     pass
        >>> type(A)  # A 现在是实例，不是类
        <class '__main__.A'>

        >>> @as_obj(1, 2, name="test")
        ... class B:
        ...     def __init__(self, x, y, name: str):
        ...         self.x = x
        ...         self.y = y
        ...         self.name = name
        >>> B.x, B.y, B.name
        (1, 2, 'test')
    """
    # 情况1：无括号调用 @as_obj（直接传入类作为唯一参数）
    if len(args) == 1 and isinstance(args[0], type) and not kwargs:
        # 直接实例化并返回，不维护任何内部状态
        return args[0]()

    # 情况2：带参数调用 @as_obj(...)
    # 返回一个装饰器函数，该函数接收类并用给定参数实例化
    def decorator(cls: type[T]) -> T:
        """内部装饰器函数，负责用收集的参数实例化类。"""
        return cls(*args, **kwargs)

    return decorator


# 判断奇偶数 利用 Python 的魔术方法 __call__ 和 __repr__ 来判断数字的奇偶性


class _C:
    """
    一个特殊的类，用于构造可递归调用的对象。

    核心原理：
    - 实例被调用时（使用 ()），返回类本身
    - 类被调用时，创建新的实例
    - 因此，奇数次调用返回实例，偶数次调用返回类
    """

    def __call__(self):
        """
        使实例可被调用。

        当实例被调用时（如 C()()），返回 type(self) 即类本身，
        而不是创建新实例。

        Returns:
            type: 类 C 本身
        """
        return type(self)

    def __repr__(self):
        """
        定义实例的字符串表示。

        返回类名 'C'，用于构造调用链字符串。

        Returns:
            str: 类名 'C'
        """
        return str(type(self).__name__)


def find(i: int) -> None:
    """
    判断数字 i 的奇偶性。

    原理：构造一个长度为 i 的调用链 C()()()...，
    - 如果 i 是奇数，最终结果是 C 的实例
    - 如果 i 是偶数，最终结果是 C 类本身

    Args:
        i: 要判断奇偶性的非负整数

    Example:
        >>> find(3)  # 奇数
        奇数
        >>> find(4)  # 偶数
        偶数
    """
    # 构造调用链字符串，如 i=3 时：'C()()()'
    call = repr(_C()) + "()" * i

    # 执行调用链，获取最终结果
    w = eval(call)

    # 判断结果类型：
    # - 实例表示奇数（因为奇数次调用返回实例）
    # - 类表示偶数（因为偶数次调用返回类）
    if isinstance(w, _C):
        print("奇数")
    else:
        print("偶数")


class Point:
    """
    模拟指针效果的类，通过魔法方法实现特殊语法。

    使用方式:
        point = Point()
        point *= 'data'    # 存储数据
        value = ... * point  # 获取数据（看起来像解引用）
    """

    def __init__(self) -> None:
        """初始化 Point 实例，_data 存储实际数据。"""
        self._data: Any = None

    def __imul__(self, value: Any) -> "Point":
        """
        实现赋值乘运算 (point *= value)。

        参数:
            value: 要存储的任意数据

        返回:
            self: 返回实例自身以支持链式操作
        """
        self._data = value
        return self

    def __rmul__(self, other: Any) -> Any:
        """
        实现右乘运算 (other * point)。

        当左侧操作数（如 Ellipsis ...）没有实现 __mul__ 或返回 NotImplemented 时，
        Python 会调用此方法。

        参数:
            other: 左侧操作数（通常是 ... Ellipsis）

        返回:
            存储在 _data 中的数据
        """
        return self._data

    def __repr__(self) -> str:
        """返回对象的官方字符串表示。"""
        return f"Point(data={self._data!r})"


def print_flow(*args: object, **kwargs: object) -> None:
    """
    实现文字流式输出效果，类似于打字机效果

    该函数会逐个字符地打印文本，并在非空白字符之间添加短暂的延迟，
    创造出流畅的输出效果，增强用户体验。还会在前后添加边框线。

    参数:
        *args: 要打印的参数，可以是任意类型，会被转换为字符串。
            如果未传入任何参数，则打印函数自身的文档字符串。
        **kwargs:
            sep: 分隔符，默认为空格
            end: 结束符，默认为换行符
            time_step: 字符间的延迟时间（秒），默认为0.02秒

    异常:
        ValueError: 如果传入了flush或file关键字参数

    返回:
        None

    示例:
        >>> print_flow("Hello", "World")
        Hello World
        >>> print_flow()  # 打印自身文档字符串
    """
    # 检查是否传入了不支持的关键字参数
    if ("flush" in kwargs) or ("file" in kwargs):
        raise ValueError("flush and file are not supported")

    # 如果没有传入参数，打印自己的文档字符串
    if not args:
        args = (print_flow.__doc__,)

    # 获取关键字参数，设置默认值
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", line())
    time_step = kwargs.get("time_step", 0.02)

    # 将所有参数转换为字符串 拼接所有参数和结束符
    all_arg = sep.join((str(i) for i in args)) + end

    # 逐个字符打印
    for i in all_arg:
        # 打印单个字符，立即刷新缓冲区
        print(i, end="", flush=True)
        # 仅在非空白字符时添加延迟
        if i.strip():
            time.sleep(time_step)


def import_(*names: str, globals_dict: dict | None = None) -> None:
    """动态导入模块并注入到指定全局命名空间。

    基于 importlib 实现运行时动态导入，支持批量导入指定模块或
    一次性导入所有标准库模块（通过 inspect 自动定位调用者命名空间）。

    Args:
        *names: 模块名字符串序列。特殊值 "*" 表示导入全部标准库模块
            （自动排除下划线开头及 antigravity、this 等非实用模块）。
        globals_dict: 目标全局命名空间字典。为 None 时自动通过调用栈
            获取调用者的 globals()。

    Returns:
        None: 模块通过副作用注入到 globals_dict，函数本身无返回值。

    Note:
        导入异常被捕获并打印，不中断批量导入流程。

    Examples:
        >>> import_("os", "sys")
        >>> import_("*")
        >>> import_("json", globals_dict=custom_globals)
    """

    # 自动检测目标命名空间：通过调用栈获取调用者的全局作用域
    if globals_dict is None:
        inspect = importlib.import_module("inspect")
        current_frame = inspect.currentframe()
        if current_frame is not None and current_frame.f_back is not None:
            caller_globals = current_frame.f_back.f_globals
        else:
            # 回退方案：若无法获取调用者帧，使用当前模块的全局命名空间
            caller_globals = globals()
        globals_dict = caller_globals

    if "*" in names:
        # 批量导入所有标准库模块
        sys = importlib.import_module("sys")
        all_modules: list[str] = list(sys.stdlib_module_names)
        skip_modules = {"antigravity", "this"}  # 跳过非实用模块
        for mod_name in all_modules:
            if mod_name in skip_modules or mod_name.startswith("_"):
                # 跳过私有模块
                continue
            try:
                module = importlib.import_module(mod_name)
                globals_dict[mod_name] = module
            except Exception as e:
                print(f"- 导入模块 {mod_name} 失败: {e}")
    else:
        # 逐个导入指定模块
        for name in names:
            try:
                module = importlib.import_module(name)
                globals_dict[name] = module
            except Exception as e:
                print(f"- 导入模块 {name} 失败: {e}")


def init(sure: str | int = 0, mods: str = "") -> None:
    """将调用者文件初始化为标准 Python 脚本模板。

    该函数通过 inspect 获取调用者的文件路径，并将其内容
    覆盖写入一个包含文档字符串和导入和 main 函数的标准模板。

    Args:
        sure: 安全确认参数，必须为字符串 "make sure" 才会执行初始化。
            默认为 0，用于防止意外调用。
        mods: 用空格分隔的模块名字符串，会自动生成 import 语句。
            例如: "os sys pathlib" 会生成:
                import os
                import sys
                import pathlib

    Returns:
        None

    Note:
        此操作会覆盖原文件内容，请谨慎使用。
        调用方式: init("make sure", "os sys json")
    """
    if sure != "make sure":
        return

    # 处理模块导入字符串
    imports = ""
    if mods.strip():
        module_list = [m.strip() for m in mods.split() if m.strip()]
        imports = "\n".join(f"import {m}" for m in module_list)
        imports += "\n"

    # 获取调用者的文件路径
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename

    with open(caller_file, "w", encoding="utf-8") as f:
        f.write(
            f'''{imports}
"""
doc
"""


def main():
    ...


if __name__ == "__main__":
    main()
'''
        )


def glb(name: str, value: Any = 0) -> bool:
    """
    在调用者模块的全局命名空间中创建变量。

    该函数通过 inspect 模块获取调用者的帧，从而在调用者模块（而非本模块）中
    动态创建全局变量。这是一种元编程技术，用于在运行时动态注入全局变量。

    参数:
        name: 变量名称，将作为全局变量的标识符
        value: 变量的初始值，默认为 0

    返回:
        bool: 如果变量创建成功返回 True，如果变量已存在则返回 False

    注意:
        - 这违反了封装原则，可能导致代码难以追踪和调试，请谨慎使用
        - 仅在特殊场景（如框架初始化、配置注入、动态代码生成）中使用
        - 不会覆盖已存在的变量，确保安全性


    实现原理:
        使用 inspect.currentframe().f_back 获取调用者的执行帧，
        通过 f_globals 访问调用者的全局命名空间，从而在该空间中创建变量。
    """
    # 获取调用者帧的全局命名空间
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals

    if name not in caller_globals:
        caller_globals[name] = value
        return True
    return False


if __name__ == "__main__":
    line()

    # 创建一个包含 0-9 的元组，用于测试
    n = tuple(range(10))

    # 测试：对 0-9 的每个数字判断奇偶性
    for i in n:
        find(i)

    line()

    # 测试指针效果
    point = Point()
    point *= "data"  # 像指针赋值: *ptr = 'data'
    get = ... * point  # 像解引用: *ptr
    print(f"存储的数据: {get}")

    line()

    print_flow()

    line()

    import_("*")
    print(globals().keys())
