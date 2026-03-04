"""
工具函数模块

提供一系列实用的辅助函数。

函数列表：
    - show: 安全查看可迭代对象内容
    - see: 查看对象的可访问属性和方法
    - every: 扁平化任意嵌套的可迭代对象
    - r_step: 可迭代对象分组生成器
    - check: 全局命名冲突检查
    - bases: 查看类的继承树
    - line: 生成终端宽度分隔线
    - count_chars: 统计文件字符数
    - time_data: 获取当前时间
    - doc: 打印模块文档
"""

import os
import time
import shutil
import builtins
import functools
from pathlib import Path
from typing import Callable, Any, Iterable, Generator, Set

from .decorators import now, OPEN

__all__ = [
    "show",
    "see",
    "every",
    "r_step",
    "check",
    "bases",
    "line",
    "count_chars",
    "time_data",
    "doc",
]

try:
    import inspect
except ImportError:
    inspect = None

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def show(ite: Iterable, end_at: int = 1) -> None:
    """
    查看可迭代对象的内容

    安全地查看可迭代对象（包括无限生成器）的内容，避免无限循环。
    通过 end_at 参数控制输出长度，特别适用于调试无限生成器或大型数据集。

    学习要点：
        - 可迭代对象的处理
        - 参数控制行为

    参数:
        ite: Iterable - 要查看的可迭代对象
        end_at: int - 控制输出长度的参数，默认值为 1
            - 0: 输出所有元素
            - n>0: 最多输出 10**n 个元素后停止

    返回:
        None - 无返回值，直接输出到控制台
    """
    if end_at != 0:
        count: int = 10**end_at
        for i in ite:
            print(i, end=",")
            count -= 1
            if count <= 0:
                print("\n")
                return
    else:
        for i in ite:
            print(i, end=",")
        else:
            print("\n")


def see(obj: Any, simple: int = 1, translate_doc: bool = False):
    """
    查看对象的可访问属性和方法

    通过反射机制检查类或实例对象的所有可访问属性和方法，
    包括继承的成员。特别适用于调试和探索未知对象的结构。

    学习要点：
        - 反射机制（getattr, dir）
        - inspect 模块的使用
        - 可调用对象判断

    参数:
        obj: Any - 要检查的类或实例对象
        simple: int - 控制是否显示特殊方法
            - 1: 跳过特殊方法（默认）
            - 0: 显示所有方法，包括特殊方法
        translate_doc: bool - 控制是否翻译文档字符串
            - False: 显示原始文档字符串（默认）
            - True: 翻译文档字符串为中文

    返回:
        None - 无返回值，直接输出到控制台
    """
    from .trans import trans

    translator = trans if translate_doc else None

    attributes: list[str] = dir(obj)
    for attr_name in attributes:
        if simple and attr_name.startswith("__") and attr_name.endswith("__"):
            continue
        try:
            attr_value: Any = getattr(obj, attr_name)
            if attr_name == "__doc__":
                if attr_value and translate_doc:
                    translated_doc = translator.translate(attr_value)
                    print(f"- 属性 {attr_name} = {translated_doc}\n")
                else:
                    print(f"- 属性 {attr_name} = {attr_value}\n")
            elif callable(attr_value):
                try:
                    sig = inspect.signature(attr_value)
                    params = str(sig)
                except (ValueError, TypeError):
                    params = "[无法获取参数]"

                doc = attr_value.__doc__
                if doc and translate_doc:
                    translated_doc = translator.translate(doc)
                    print(f"- 方法 {attr_name}{params}: {translated_doc}\n")
                else:
                    print(f"- 方法 {attr_name}{params}: {doc}\n")
            else:
                attr_type = type(attr_value)
                type_name = attr_type.__name__

                doc = None
                show_doc = False

                if hasattr(attr_value, "__doc__"):
                    doc = attr_value.__doc__
                    if doc and doc != attr_type.__doc__:
                        show_doc = True

                if show_doc:
                    if translate_doc:
                        translated_doc = translator.translate(doc)
                        print(
                            f"- 属性 {attr_name} = {attr_value} :" f"{translated_doc}\n"
                        )
                    else:
                        print(f"- 属性 {attr_name} = {attr_value} :{doc}\n")
                else:
                    print(f"- 属性 {attr_name} = {attr_value} (类型: {type_name})\n")
        except Exception as e:
            print(f"- {attr_name}: [访问错误: {e}]")


def every(its: Iterable[Any]) -> Any:
    """
    扁平化任意嵌套的可迭代对象生成器

    递归遍历输入的可迭代对象，将所有嵌套的元素扁平化为单个序列返回。
    特别处理字符串类型，将其视为原子元素而非可迭代对象。

    学习要点：
        - 递归生成器
        - yield from 语法
        - 类型检查

    参数:
        its: Iterable[Any] - 任意嵌套的可迭代对象

    返回:
        Any - 生成器，产生扁平化后的元素序列
    """
    for i in its:
        if isinstance(i, Iterable):
            if isinstance(i, str):
                yield i
            else:
                yield from every(i)
        else:
            yield i


def r_step(ite: Iterable[Any], step: int) -> Generator[list[Any], None, None]:
    """
    可迭代对象分组生成器

    将一个可迭代对象按照指定的步长进行分组，返回一个生成器，每次生成一个长度为step的列表。
    如果可迭代对象的长度不是step的整数倍，最后一次生成的列表长度会小于step。

    学习要点：
        - 生成器的使用
        - for-else 语法

    参数:
        ite: Iterable[Any] - 要分组的可迭代对象
        step: int - 每个分组的长度

    返回:
        Generator[list[Any], None, None] - 生成器，每次生成一个长度为step的列表
    """
    crt = []
    for item in ite:
        crt.append(item)
        if len(crt) == step:
            yield crt
            crt = []
    else:
        if crt:
            yield crt


def check(*args: str, letters="abcdefghijklmnopqrstuvwxyz"):
    """
    全局命名冲突检查

    检查给定的名称是否与调用者模块的全局变量或内置函数名称冲突。

    学习要点：
        - inspect 获取调用栈
        - 集合运算

    参数:
        *args: str - 要检查的名称列表

    返回:
        set[str] - 可用的名称集合
    """
    caller_globals = inspect.currentframe().f_back.f_globals

    check_names = set(args)
    if letters:
        check_names.update(set(letters))

    conflict_sources = set(caller_globals.keys()) | set(dir(builtins))

    conflict_names = check_names & conflict_sources
    available_names = check_names - conflict_sources

    print(" - 重复:", conflict_names, "\n", "- 可用:", available_names)

    return available_names


def line(char: str = "=") -> str:
    """
    打印一个填满终端宽度的分隔线字符串。

    学习要点：
        - shutil.get_terminal_size 获取终端尺寸

    Args:
        char: 用于构成分隔线的字符，默认为 '='。

    Returns:
        str: 分隔线字符串
    """
    terminal_width = shutil.get_terminal_size().columns
    print("\n" + char * terminal_width+"\n")
    return "\n" + char * terminal_width+"\n"

def count_chars(
    path: Path = None,
    extension: str = ".py",
    recursive: bool = True,
    print_result: bool = True,
) -> dict:
    """
    统计路径下指定扩展名文件的字符数

    学习要点：
        - pathlib 路径操作
        - glob 模式匹配

    Args:
        path: 要统计的目录路径，默认为当前工作目录
        extension: 文件扩展名，默认为".py"
        recursive: 是否递归搜索子目录，默认为True
        print_result: 是否打印结果，默认为True

    Returns:
        dict: 包含统计结果的字典
    """
    if path is None:
        path = Path()
    if not extension.startswith("."):
        extension = "." + extension

    files_info = []
    total_chars = 0

    pattern = f"**/*{extension}" if recursive else f"*{extension}"

    for file in path.glob(pattern):
        if file.is_file():
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    chars = len(content)
                    files_info.append(
                        {"name": str(file.relative_to(path)), "chars": chars}
                    )
                    total_chars += chars
            except (IOError, UnicodeDecodeError) as e:
                print(f"无法读取文件: {file} - {e}")
                continue

    result = {
        "total_chars": total_chars,
        "file_count": len(files_info),
        "files": files_info,
    }

    if print_result:
        print("\n文件详情:")
        for file_info in result["files"]:
            print(f"  {file_info['name']}: {file_info['chars']} 字符")
        print(f"\n统计路径: {path.resolve()}")
        print(f"文件总数: {result['file_count']}")
        print(f"总字符数: {result['total_chars']}")

    return result


def bases(obj: Any) -> None:
    """
    格式化打印对象的继承树结构。

    学习要点：
        - 递归打印树结构
        - __bases__ 和 __mro__ 属性

    参数:
        obj: 任意对象（类或实例）

    返回:
        None
    """

    def _print_tree(
        cls: type,
        visited: Set[type] = None,
        prefix: str = "",
        is_last: bool = True,
        ref_count: dict = None,
    ) -> None:
        if visited is None:
            visited = set()
        if ref_count is None:
            ref_count = {}

        ref_count[cls] = ref_count.get(cls, 0) + 1

        connector = "└── " if is_last else "├── "
        star_mark = " (*)" if ref_count[cls] > 1 else ""
        print(f"{prefix}{connector}{cls.__module__}.{cls.__name__}{star_mark}")

        if cls in visited:
            return

        visited.add(cls)

        bases_list = cls.__bases__

        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, base in enumerate(bases_list):
            is_last_base = i == len(bases_list) - 1
            _print_tree(base, visited, new_prefix, is_last_base, ref_count)

    cls = obj if isinstance(obj, type) else type(obj)

    print(f"继承树 for {cls.__module__}.{cls.__name__}")
    print("* 代表重复项")
    print("=" * 60)

    _print_tree(cls)

    print("\nMRO (方法解析顺序):")
    for base_class in cls.__mro__:
        print(f"{base_class.__module__}.{base_class.__name__}")


@now
def time_data():
    """
    时间数据函数

    获取并打印当前时间，返回格式化的时间字符串。
    格式为：年-月-日 时:分:秒

    该函数使用 @now 装饰器，在模块导入时会立即执行（受 OPEN 全局变量控制）。

    返回:
        str - 格式化的时间字符串
    """
    rs = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(rs)
    print("\n")
    return rs


@now
def doc():
    """
    打印模块文档字符串

    打印当前模块的 __doc__ 属性，用于查看模块的文档说明。

    该函数使用 @now 装饰器，在模块导入时会立即执行（受 OPEN 全局变量控制）。

    返回:
        str - 模块的文档字符串
    """
    print(__doc__)
    return __doc__
