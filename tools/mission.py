"""
工具类模块

提供多种实用工具类。

类列表：
    - Catch: 异常捕获上下文管理器
    - TestFile: 测试文件上下文管理器
    - Mission: 任务并行执行类
    - Create: 数据结构创建工具
    - Frange: 范围生成器
"""

import os
import random
import multiprocessing
import concurrent.futures as cf
from typing import Callable, Any, Iterable, Generator, Self

__all__ = [
    "Catch",
    "TestFile",
    "Mission",
    "Create",
    "Frange",
    "crt",
    "r",
]

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


class Catch:
    """
    异常捕获上下文管理器

    用于捕获with语句块中的异常并打印错误信息，使代码更加简洁，避免重复的try-except结构。

    学习要点：
        - 上下文管理器协议
        - __enter__ 和 __exit__ 方法

    示例用法:
        # 基本用法
        with Catch():
            1 / 0

        # 指定上下文名称
        with Catch(name="除法操作"):
            result = 10 / 0

        # 控制是否抑制异常传播
        with Catch(e=False):  # 不抑制异常，异常会向上传播
            1 / 0
    """

    def __init__(self, name: str = "", e: bool = True) -> None:
        """
        初始化Catch上下文管理器

        参数:
            name: str - 上下文名称
            e: bool - 是否抑制异常传播
                - True: 异常已处理，不向上传播
                - False: 异常未处理，向上传播
        """
        self.e = e
        self.name = name

    def __enter__(self) -> None:
        if self.name:
            print(f"进入Catch上下文: {self.name}")

    def __exit__(
        self, exc_type: type | None, exc_val: Exception | None, exc_tb: object | None
    ) -> bool:
        if exc_type:
            print(f"捕获到异常{exc_type.__name__}: {exc_val}")
            return self.e
        return False


class TestFile:
    """
    测试文件上下文管理器类。

    用于创建临时测试文件，支持上下文管理器协议，退出时自动清理。

    学习要点：
        - 上下文管理器
        - 文件操作
        - 异常处理

    Attributes:
        filepath: 创建的文件路径
        size: 文件大小（KB）
        content: 填充内容字符

    Example:
        >>> with TestFile(5) as tf:  # 创建 5KB 测试文件
        ...     data = tf.read()     # 读取文件内容
        >>> # 文件自动删除
    """

    def __init__(
        self,
        size: int = 1,
        filename: str | None = None,
        content: str = "1",
    ) -> None:
        """
        初始化测试文件上下文管理器。

        Args:
            size: 文件大小，单位为 KB，默认为 1 KB。
            filename: 自定义文件名，默认为 None
            content: 填充内容字符，默认为 "1"
        """
        self.size: int = size
        self.content: str = content
        self.filepath: str = filename if filename else f"{size}kb_test.txt"

    def __enter__(self) -> "TestFile":
        size_in_bytes: int = self.size * 1024

        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(self.content * size_in_bytes)
        except IOError as e:
            raise IOError(f"无法创建测试文件 '{self.filepath}': {e}") from e

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            os.remove(self.filepath)
        except (FileNotFoundError, OSError):
            pass

    def read(self) -> str:
        """
        读取测试文件的内容。

        Returns:
            str: 文件内容
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.read()
        except IOError as e:
            raise IOError(f"无法读取测试文件 '{self.filepath}': {e}") from e


class Mission:
    """
    任务管理类，用于批量并行执行函数任务。

    基于 ProcessPoolExecutor 实现多进程并行，内置 tqdm 进度条显示。
    自动处理多进程保护，子进程中迭代会直接返回空列表避免递归。

    学习要点：
        - 多进程并行
        - 迭代器协议
        - 进程保护

    Attributes:
        _todo: 待执行的任务列表
        _res: 任务执行结果列表

    Example:
        >>> mission = Mission()
        >>> mission.add(task_func, arg1, arg2)
        >>> for result in mission:  # 迭代时自动执行并返回结果
        ...     print(result)
    """

    @staticmethod
    def _is_main_process() -> bool:
        """
        判断是否为主进程（非多进程子进程）。

        Returns:
            True 表示主进程，False 表示子进程
        """
        return multiprocessing.current_process().name == "MainProcess"

    def __init__(self, todo: list | None = None) -> None:
        self._todo: list[tuple[Callable, tuple]] = todo if todo is not None else []
        self._res: list[Any] = []

    def add(self, func: Callable, *args) -> None:
        """
        添加任务到待执行列表。

        Args:
            func: 要执行的函数
            *args: 函数的参数
        """
        self._todo.append((func, args))

    def _clear(self) -> None:
        """清空所有任务和结果（内部方法）。"""
        self._todo.clear()
        self._res.clear()

    def __iter__(self):
        if not self._res and self._todo:
            self._run()
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self._res):
            self._clear()
            raise StopIteration
        result = self._res[self._iter_index]
        self._iter_index += 1
        return result

    def _run(self, max_workers: int | None = None) -> list[Any]:
        """
        并行执行所有任务（内部方法）。

        Args:
            max_workers: 最大进程数，默认为 CPU 核心数

        Returns:
            任务执行结果列表
        """
        if not Mission._is_main_process():
            return []

        if not self._todo:
            raise RuntimeError("没有任务可执行，请先使用 add() 添加任务")

        self._res = []

        with cf.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, *args) for func, args in self._todo]
            self._res = [
                f.result() for f in tqdm(futures, total=len(futures), desc="完成任务")
            ]

        return self._res


class Create:
    """
    数据结构创建工具类

    用于快速创建各种数据结构（列表、元组、字典、集合、字符串）。
    通过属性访问方式获取不同类型的数据结构。

    学习要点：
        - __getattr__ 动态属性
        - __slots__ 限制属性
        - match-case 语法

    属性说明:
        l: list[int] - 随机整数列表
        t: tuple[int] - 元组
        d: dict[int, int] - 字典
        s: set[int] - 集合
        st: str - 大写字母字符串
    """

    __slots__ = ["l", "t", "d", "s", "st"]

    def __getattr__(self, name: str) -> Any:
        match name:
            case "l":
                return [random.randint(0, 25) for _ in range(10)]
            case "t":
                return tuple(self.l)
            case "d":
                return dict.fromkeys(self.l, 0)
            case "s":
                return set(self.l)
            case "st":
                return "".join([chr(i + 65) for i in self.l])
            case _:
                print(f"can not create '{name}'")


crt = Create()


class Frange:
    """
    范围生成器类，支持整数、浮点数和罗马数字风格的范围生成。

    学习要点：
        - __call__ 使实例可调用
        - __getattr__ 动态属性
        - 生成器 yield

    支持的功能：
    - 正整数：生成从 0 到 ct-1 的序列
    - 负整数：生成从负的 (abs(ct)-1) 到 0 的序列
    - 正浮点数：生成从 0 到 ct 的序列，步长为最小精度
    - 负浮点数：生成从负的 (abs(ct)-1) 到 0 的序列
    - 罗马数字风格：通过属性访问生成范围，如 r.xv 对应生成 0 到 14 的序列
    """

    def __call__(self, ct: int | float) -> Generator[float | int, None, None]:
        if not isinstance(ct, (int, float)):
            raise ValueError("only int and float are valid")

        is_negative = ct < 0
        ct = abs(ct)

        if isinstance(ct, int):
            yield from self._yield_int_range(ct, is_negative)
        else:
            yield from self._yield_float_range(ct, is_negative)

    def _yield_int_range(
        self, ct: int, is_negative: bool
    ) -> Generator[int, None, None]:
        if is_negative:
            for i in range(ct - 1, -1, -1):
                yield -i
        else:
            yield from range(ct)

    def _yield_float_range(
        self, ct: float, is_negative: bool
    ) -> Generator[float, None, None]:
        ct = round(ct, 4)

        cont = self._get_precision(ct)

        if cont == 0:
            yield from self._yield_int_range(int(ct), is_negative)
            return

        ct_int = int(str(ct).replace(".", ""))

        if is_negative:
            for i in range(ct_int - 1, -1, -1):
                yield -i / 10**cont
        else:
            for i in range(ct_int):
                yield i / 10**cont

    def _get_precision(self, ct: float) -> int:
        ct_str = str(ct)
        if "." not in ct_str:
            return 0

        decimal_part = ct_str.split(".")[1]

        last_non_zero_pos = -1
        for i, ch in enumerate(decimal_part):
            if ch != "0":
                last_non_zero_pos = i

        return 0 if last_non_zero_pos == -1 else last_non_zero_pos + 1

    def __getattr__(self, name: str) -> Generator[int, None, None]:
        def t(n: str) -> int:
            match n:
                case "i":
                    return 1
                case "v":
                    return 5
                case "x":
                    return 10
                case _:
                    raise ValueError(f"only i=1,v=5,x=10 are valid")

        nums = list(map(t, name))

        total = 0
        n = len(nums)
        for i in range(n):
            if i < n - 1 and nums[i] < nums[i + 1]:
                total -= nums[i]
            else:
                total += nums[i]

        yield from range(total)


r = Frange()
