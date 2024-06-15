import os
import typing as t

from ctdk.types import UndefinedType, Undefined

_T = t.TypeVar("_T")


class EnvValue:
    def __init__(self, x: str):
        self.x = x

    def get_value(self) -> str:
        return self.x

    def __str__(self):
        return self.x


def _env_get(key: str, default: _T = Undefined, upper_fmt: bool = True) -> t.Union[EnvValue, _T, UndefinedType]:
    """
    获取环境变量的值，并可以选择是否进行格式化处理。

    :param key: 环境变量的名称。
    :param default: 如果环境变量未设置时返回的默认值。
    :param upper_fmt: 是否将键名转换为大写并替换破折号为下划线。
    :return: 环境变量的值或者默认值。
    """
    if upper_fmt:
        key = key.upper().replace("-", "_")
    if key in os.environ:
        return EnvValue(os.environ[key])
    return default


def pick(*values: _T) -> t.Union[_T, UndefinedType]:
    """
    从参数中选择第一个不是 Undefined 的值。

    :param values: 需要选择的值。
    :return: 第一个非 Undefined 的值，如果都是 Undefined 则返回 Undefined。
    """
    for v in values:
        if v is not Undefined:
            return v
    return Undefined


P = pick
ENV = _env_get

is_prod = os.environ.get("CT_PROD", "false").lower() in {"true", "t", "yes", "y", "1"}
is_debug = debug_mode = not is_prod
