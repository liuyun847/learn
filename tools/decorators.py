"""
装饰器集合模块

提供多种实用的函数装饰器和类装饰器。

装饰器列表：
    - log: 函数执行日志记录
    - catch: 异常捕获与处理
    - now: 立即执行装饰器
    - reg: 函数注册装饰器
    - Dec: 可变函数装饰器类
    - abc_def: 严格抽象基类装饰器
"""

import functools
import time
from abc import ABCMeta, abstractmethod
from typing import Callable, Any, Self, TypeVar, Set

__all__ = [
    "log",
    "catch",
    "now",
    "reg",
    "Dec",
    "abc_def",
    "OPEN",
    "set_OPEN",
]

OPEN: bool = False
"""
全局控制开关，用于控制 @now 装饰器装饰的函数是否执行

该变量作为全局标志，控制被 @now 装饰的函数在模块导入时是否实际执行。
当 OPEN 为 True 时，被装饰的函数会在装饰时立即执行；
当 OPEN 为 False 时，被装饰的函数不会执行。

用途:
    - 用于控制 time_data() 和 doc() 等使用 @now 装饰器的函数
    - 在模块导入时可以通过修改此变量来控制这些函数的行为

注意:
    - 该变量需要在导入模块前设置才能生效
    - 仅影响使用 @now 装饰器的函数
"""


def log(func: Callable) -> Callable:
    """
    函数执行日志装饰器

    为被装饰的函数添加执行日志功能，包括函数名称、输入参数、返回值、
    单次执行耗时、总执行次数和总耗时（仅累加最外层调用）。
    特别适用于递归函数的性能分析，通过调用深度跟踪避免重复计算总耗时。

    学习要点：
        - nonlocal 关键字修改闭包变量
        - call_depth 跟踪递归深度避免重复计时
        - 装饰器的状态保持（count, alltime）

    参数:
        func: Callable - 要添加日志功能的函数

    返回:
        Callable - 包装后的函数，具有日志记录功能
    """
    count: int = 0
    alltime: float = 0
    call_depth: int = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        nonlocal count, alltime, call_depth
        call_depth += 1
        stt: float = time.time()
        rs: Any = func(*args, **kwargs)
        end: float = time.time()
        count += 1
        current_time: float = end - stt
        if call_depth == 1:
            alltime += current_time
        print(
            "- name=",func.__name__,
            "in=",args,kwargs,
            "return=",rs,
            "\n",
            f" spend={current_time:.6f} all={alltime:.3f}",
            "times=",count,
        )
        call_depth -= 1
        return rs

    return wrapper


def catch(func: Callable) -> Callable:
    """
    装饰器：捕获函数执行过程中的异常并打印错误信息

    学习要点：
        - 异常捕获与处理
        - 计数器的使用

    参数:
        func: Callable - 要装饰的函数

    返回:
        Callable - 包装后的函数，具有异常捕获功能
    """
    count: int = 0

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        nonlocal count
        try:
            count += 1
            return func(*args, **kwargs)
        except Exception as e:
            print(f"- 函数 {func.__name__} 在第{count}次执行时出错: {e} \n")

    return wrapper


def now(*args: Any, **kwargs: Any) -> Callable:
    """
    立即执行装饰器 - 在装饰时立即执行被装饰函数并输出结果

    该装饰器支持多种调用方式，无论哪种方式，都会在装饰时立即执行被装饰的函数
    并打印函数名及其返回值，最后将原始函数返回（不改变函数原有功能）。

    受 OPEN 全局变量控制:
        装饰器内部会检查 OPEN 变量来决定是否执行：
        - 当 OPEN = True 时，被装饰函数正常执行
        - 当 OPEN = False 时，跳过执行，仅返回原始函数

    学习要点：
        - 装饰器的多种调用方式
        - 可变参数的处理
        - 全局变量控制行为

    参数:
        *args: Any - 可变位置参数
        **kwargs: Any - 可变关键字参数

    返回:
        Callable - 返回原始的被装饰函数，不改变其原有功能
    """
    if len(args) == 1 and callable(args[0]) and not kwargs:
        func = args[0]
        if OPEN:
            print(f"- run {func.__name__}")
            func()
        return func

    def inner(func: Callable) -> Callable:
        if OPEN:
            print(f"""- run {func.__name__} with args={args},kwargs={kwargs}""")
            func(*args, **kwargs)
        return func

    return inner


def set_OPEN(open: bool) -> None:
    """
    设置全局变量 OPEN

    用于在运行时动态是否执行 @now 装饰器装饰的函数。

    参数:
        open: bool - 是否执行函数（True 表示执行，False 表示不执行）
    """
    global OPEN
    OPEN = open


class Reg:
    """
    函数注册装饰器类

    用于注册被装饰的函数，将函数名和文档字符串存储到类属性中。
    支持去重处理，确保同一函数不会被重复注册。

    学习要点：
        - 类作为装饰器
        - __call__ 方法的使用
        - __slots__ 限制属性

    类属性:
        reged: list[tuple[str, str, Callable[..., Any]]]
        - 存储已注册函数信息的列表
    """

    reged: list[tuple[str, str, Callable[..., Any]]] = []
    __slots__ = []

    def __call__(self, func: Callable) -> Callable:
        registered = {funcs for _, _, funcs in self.reged}
        if func not in registered:
            self.reged.append((func.__name__, func.__doc__, func))
        return func

    def __str__(self) -> str:
        return f"reged={self.reged}"


reg = Reg()


T = TypeVar("T", bound=type)


def abc_def(cls: T) -> T:
    """
    装饰器：将普通抽象基类转换为使用 StrictABCMeta 元类的严格抽象基类。

    学习要点：
        - 元类的使用
        - 抽象方法的检查
        - 类装饰器

    Args:
        cls: 要装饰的抽象基类

    Returns:
        使用 StrictABCMeta 元类的新类
    """

    class StrictABCMeta(ABCMeta):
        """
        严格的抽象基类元类。

        在子类定义完成时立即检查是否实现了所有抽象方法，而不是在实例化时。
        如果未实现则在类定义阶段就抛出 TypeError。
        """

        def __new__(
            mcs,
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, Any],
            **kwargs: Any,
        ) -> type:
            cls = super().__new__(mcs, name, bases, namespace, **kwargs)

            abstract_methods = getattr(cls, "__abstractmethods__", frozenset())

            if not abstract_methods:
                return cls

            parent_abstract = frozenset()
            for base in bases:
                if hasattr(base, "__abstractmethods__"):
                    parent_abstract |= base.__abstractmethods__

            new_abstract_methods = abstract_methods - parent_abstract
            if new_abstract_methods:
                return cls

            for method_name in abstract_methods:
                method = getattr(cls, method_name, None)
                if getattr(method, "__isabstractmethod__", False):
                    raise TypeError(f"类 '{name}' 未实现抽象方法 '{method_name}'")

            return cls

    namespace = dict(cls.__dict__)
    namespace.pop("__dict__", None)
    namespace.pop("__weakref__", None)

    return StrictABCMeta(cls.__name__, cls.__bases__, namespace)


class Dec:
    """可变函数装饰器类

    提供链式调用接口，支持以下功能：
    - 前置回调（before）：在函数执行前调用
    - 后置回调（after）：在函数执行后调用
    - 参数转换（change_arg）：修改传递给函数的参数
    - 异常处理（on_error）：捕获并处理函数执行过程中的异常
    - 返回值处理（change_result）：修改函数的返回值
    - finally 回调（finally_）：无论是否发生异常都会执行
    - 额外装饰器（dec）：使用其他装饰器包装函数

    学习要点：
        - 链式调用设计
        - 多种回调机制
        - functools.update_wrapper

    所有方法均支持链式调用，例如：
    @Dec
    def func():
        pass

    result = func.before(print).after(print)()
    """

    def __init__(self, func: Callable) -> None:
        self._func = func
        self._before = None
        self._before_arg = ((), {})
        self._after = None
        self._after_arg = ((), {})
        self._change = lambda x, y: (x, y)
        self._on_error = None
        self._error_arg = ((), {})
        self._change_result = None
        self._result_arg = ((), {})
        self._finally = None
        self._finally_arg = ((), {})
        functools.update_wrapper(self, func)

    def before(self, func: Callable) -> Self:
        self._before = func
        return self

    def before_arg(self, *args, **kwargs) -> Self:
        self._before_arg = (args, kwargs)
        return self

    def after(self, func: Callable) -> Self:
        self._after = func
        return self

    def after_arg(self, *args, **kwargs) -> Self:
        self._after_arg = (args, kwargs)
        return self

    def dec(self, dec: Callable) -> Self:
        self._func = dec(self._func)
        return self

    def change_arg(self, func: Callable) -> Self:
        self._change = func
        return self

    def on_error(self, func: Callable) -> Self:
        self._on_error = func
        return self

    def error_arg(self, *args, **kwargs) -> Self:
        self._error_arg = (args, kwargs)
        return self

    def change_result(self, func: Callable) -> Self:
        self._change_result = func
        return self

    def result_arg(self, *args, **kwargs) -> Self:
        self._result_arg = (args, kwargs)
        return self

    def finally_(self, func: Callable) -> Self:
        self._finally = func
        return self

    def finally_arg(self, *args, **kwargs) -> Self:
        self._finally_arg = (args, kwargs)
        return self

    def __call__(self, *args, **kwargs):
        try:
            if self._before:
                self._before(*self._before_arg[0], **self._before_arg[1])

            args, kwargs = self._change(args, kwargs)

            res = self._func(*args, **kwargs)

            if self._change_result:
                res = self._change_result(
                    res, *self._result_arg[0], **self._result_arg[1]
                )

            if self._after:
                self._after(*self._after_arg[0], **self._after_arg[1])

            return res

        except Exception as e:
            if self._on_error:
                return self._on_error(e, *self._error_arg[0], **self._error_arg[1])
            else:
                raise
        finally:
            if self._finally:
                self._finally(*self._finally_arg[0], **self._finally_arg[1])
