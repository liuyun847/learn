"""
翻译功能示例

展示 tools.trans 模块中 Trans 类和 trans 实例的使用方法。

注意: 翻译功能需要网络连接，首次翻译会调用翻译API，
后续相同内容会使用缓存。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import Trans, trans, line


def demo_trans_instance():
    """演示 trans 实例 - 快速翻译"""
    line()
    print("【trans 实例快速翻译示例】")

    texts = [
        "Hello, World!",
        "Python is a great programming language.",
        "Decorators are powerful features in Python.",
    ]

    for text in texts:
        result = trans.translate(text)
        print(f"原文: {text}")
        print(f"译文: {result}\n")


def demo_trans_class():
    """演示 Trans 类 - 自定义翻译器"""
    line()
    print("【Trans 类自定义翻译器示例】")

    translator = Trans()

    print("1. 基本翻译:")
    result = translator.translate("Good morning!")
    print(f"  'Good morning!' -> '{result}'")

    print("\n2. 指定目标语言:")
    result = translator.translate("Thank you", target_lang="ja")
    print(f"  'Thank you' (日语) -> '{result}'")

    result = translator.translate("Thank you", target_lang="fr")
    print(f"  'Thank you' (法语) -> '{result}'")


def demo_cache():
    """演示缓存功能"""
    line()
    print("【翻译缓存示例】")

    print("首次翻译 (会调用API):")
    result1 = trans.translate("Cache demonstration")
    print(f"  结果: {result1}")

    print("\n再次翻译相同内容 (使用缓存):")
    result2 = trans.translate("Cache demonstration")
    print(f"  结果: {result2}")

    print("\n缓存位置: tools/cache/")


def demo_batch_translate():
    """演示批量翻译"""
    line()
    print("【批量翻译示例】")

    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "A journey of a thousand miles begins with a single step.",
        "Practice makes perfect.",
    ]

    print("翻译多个句子:")
    for i, sentence in enumerate(sentences, 1):
        result = trans.translate(sentence)
        print(f"\n{i}. {sentence}")
        print(f"   {result}")


if __name__ == "__main__":
    demo_trans_instance()
    demo_trans_class()
    demo_cache()
    demo_batch_translate()
    line()
