"""
翻译模块

提供基于 Google 翻译的文本翻译功能，支持缓存。

主要组件：
    - Trans: 翻译类，支持多语言翻译和缓存功能
    - trans: Trans类的单例实例
"""

import time
import hashlib
import json
from pathlib import Path
from typing import Optional

__all__ = ["Trans", "trans"]

try:
    from translate import Translator
except ImportError:
    Translator = None

try:
    from uapi import UapiClient, UapiError
except ImportError:
    UapiClient = None
    UapiError = None

try:
    from langdetect import detect, LangDetectException
except ImportError:
    detect = None
    LangDetectException = None


class Trans:
    """
    翻译类

    使用translate库提供的翻译功能，基于 Google 翻译服务。
    配置简单，开箱即用，不需要 API 密钥。
    支持缓存功能，提高翻译效率。
    采用单例模式实现，确保所有使用都是同一个实例和缓存。

    学习要点：
        - 单例模式实现
        - 文件缓存设计
        - 多服务降级策略

    类属性:
        _instance: Trans - 单例实例
        _default_cache_dir: Path - 默认缓存目录路径
        _cache_file: str - 缓存文件名
    """

    _instance = None
    _default_cache_dir = Path(__file__).parent / "cache"
    _cache_file = "translations.json"

    def __new__(cls, cache_dir=None):
        """
        重写__new__方法，实现单例模式

        参数:
            cache_dir: str or Path - 缓存目录路径（可选）

        返回:
            Trans - 唯一的Trans实例
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, cache_dir=None):
        """
        初始化翻译器

        参数:
            cache_dir: str or Path - 缓存目录路径（可选）
        """
        if not hasattr(self, "_initialized"):
            if cache_dir:
                self.cache_dir = Path(cache_dir)
            else:
                self.cache_dir = self._default_cache_dir

            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._cache_data: dict = {}
            self._load_cache()

            self._initialized = True

    def _get_cache_key(self, text, target_lang):
        """
        生成缓存键

        参数:
            text: str - 要翻译的文本
            target_lang: str - 目标语言

        返回:
            str - 缓存键（MD5哈希值）
        """
        key = f"{text}:{target_lang}"
        return hashlib.md5(key.encode("utf-8")).hexdigest()

    def _load_cache(self):
        """
        从文件加载缓存到内存

        如果缓存文件不存在，初始化为空字典
        """
        cache_path = self.cache_dir / self._cache_file
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    self._cache_data = json.load(f)
            except Exception as e:
                print(f"- 加载缓存失败: {e}")
                self._cache_data = {}
        else:
            self._cache_data = {}

    def _save_cache(self):
        """
        将内存缓存保存到文件
        """
        cache_path = self.cache_dir / self._cache_file
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(self._cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"- 保存缓存失败: {e}")

    def _read_cache(self, cache_key):
        """
        读取缓存

        参数:
            cache_key: str - 缓存键

        返回:
            str or None - 缓存的翻译结果，不存在则返回None
        """
        if cache_key in self._cache_data:
            return self._cache_data[cache_key].get("translation")
        return None

    def _write_cache(self, cache_key, translation):
        """
        写入缓存

        参数:
            cache_key: str - 缓存键
            translation: str - 翻译结果
        """
        self._cache_data[cache_key] = {"translation": translation}
        self._save_cache()

    def _detect_language(self, text):
        """
        检测文本语言

        参数:
            text: str - 要检测语言的文本

        返回:
            str or None - 检测到的语言代码，检测失败则返回 None
        """
        if not text:
            return None

        if detect is None:
            return None

        try:
            sample_text = text[:1000]
            return detect(sample_text)
        except (LangDetectException, Exception) as e:
            print(f"- 语言检测失败: {e}")
            return None

    def _translate_text(self, text, target_lang):
        """
        翻译文本

        参数:
            text: str - 要翻译的文本
            target_lang: str - 目标语言

        返回:
            tuple[str, bool] - (翻译后的文本, 翻译是否成功)
        """
        paragraphs = text.split("\n")

        try:
            translated_paragraphs = []
            for para in paragraphs:
                if para.strip():
                    time.sleep(1)
                    translator = Translator(to_lang=target_lang)
                    translated_para = translator.translate(para)
                    translated_paragraphs.append(translated_para)
                else:
                    translated_paragraphs.append("")
            translated_text = "\n".join(translated_paragraphs)
            return translated_text, True
        except Exception as e:
            print(f"- 默认翻译服务失败: {e}")
            print("- 尝试使用 uapi 重试...")

            try:
                translated_paragraphs = []
                client = UapiClient("https://uapis.cn")
                for para in paragraphs:
                    if para.strip():
                        time.sleep(1)
                        result = client.translate.post_translate_text(
                            to_lang=target_lang, text=para
                        )
                        if isinstance(result, dict):
                            translated_para = result.get("translate", "") or str(result)
                        else:
                            translated_para = str(result)
                        translated_paragraphs.append(translated_para)
                    else:
                        translated_paragraphs.append("")
                translated_text = "\n".join(translated_paragraphs)
                return translated_text, True
            except UapiError as e2:
                print(f"- uapi 翻译服务失败: {e2}")
                return text, False
            except Exception as e3:
                print(f"- 未知错误: {e3}")
                return text, False

    def translate(self, text, target_lang="zh", use_cache=True):
        """
        翻译方法

        使用新的翻译API进行文本翻译，默认翻译为中文。
        支持缓存功能，提高翻译效率。
        支持语言检测，当输入文本语言与目标语言相同时直接返回原文。

        参数:
            text: str - 要翻译的文本
            target_lang: str - 目标语言（默认 'zh'）
            use_cache: bool - 是否使用缓存（默认 True）

        返回:
            str - 翻译后的文本，如果翻译失败则返回原文
        """
        if not text:
            return text

        detected_lang = self._detect_language(text)
        if detected_lang and detected_lang == target_lang:
            print(f"- 输入文本语言与目标语言相同 ({detected_lang})，直接返回原文")
            return text

        if use_cache:
            cache_key = self._get_cache_key(text, target_lang)
            cached_result = self._read_cache(cache_key)
            if cached_result:
                return cached_result

        result, success = self._translate_text(text, target_lang)

        if use_cache and success:
            cache_key = self._get_cache_key(text, target_lang)
            self._write_cache(cache_key, result)
            print(f"- 缓存已保存")

        return result


trans = Trans()
