"""
工具集合包

该包提供了一系列实用工具函数和类，旨在简化日常编程任务。

模块列表：
    - decorators: 装饰器集合（log, catch, now, reg, Dec, abc_def）
    - utils: 工具函数（show, see, every, r_step, check, bases, line, count_chars）
    - trans: 翻译模块（Trans类）
    - mission: 工具类（Mission, Catch, TestFile, Create, Frange）

使用方式：
    from tools import log, catch, trans, Mission
    # 或
    from tools.decorators import log
    from tools.utils import show, see
"""

from .decorators import (
    log,
    catch,
    now,
    reg,
    Dec,
    abc_def,
    OPEN,
    set_OPEN,
)

from .utils import (
    show,
    see,
    every,
    r_step,
    check,
    bases,
    line,
    count_chars,
    time_data,
    doc,
)

from .trans import (
    Trans,
    trans,
)

from .mission import (
    Catch,
    TestFile,
    Mission,
    Create,
    Frange,
    crt,
    r,
)

__all__ = [
    # 装饰器
    "log",
    "catch",
    "now",
    "reg",
    "Dec",
    "abc_def",
    # 工具类
    "Trans",
    "Create",
    "Frange",
    "Catch",
    "TestFile",
    "Mission",
    # 辅助函数
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
    "set_OPEN",
    # 实例对象
    "trans",
    "crt",
    "r",
    # 全局变量
    "OPEN",
]
