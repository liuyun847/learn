"""癫疯之作"""

from random import choice
import sys
from typing import Any
import subprocess


class Goto(type):
    def __new__(
        cls: type,
        name: str,
        bases: tuple[type] | None = None,
        attrs: dict[Any, Any] | None = None,
    ) -> type | None:

        bases: tuple[type] = bases or (Exception,)
        attrs: dict[Any, Any] = attrs or {}
        goto = super().__new__(cls, name, bases, attrs)
        goto.__str__ = lambda self: self.__class__.__name__ + "!"
        return goto


def get_chr_num() -> int:
    with open(__file__, "r", encoding="utf-8") as f:
        return len(f.read())


def main() -> None:

    for _ in range(1+int(str(get_chr_num())[-1])):

        try:
            raise choice(
                [
                    goto_0 := Goto("goto_0"),
                    Goto1 := Goto("Goto1"),
                    Goto2 := Goto("Goto2"),
                    Goto3 := Goto("Goto3"),
                ]
            )
        except goto_0:
            subprocess.Popen([sys.executable, __file__])
            sys.exit(0)
        except Goto1 as e:
            print(e)
        except Goto2 as e:
            print(e)
        except Goto3 as e:
            print(e)
        finally:
            print("?")


if __name__ == "__main__":
    main()
