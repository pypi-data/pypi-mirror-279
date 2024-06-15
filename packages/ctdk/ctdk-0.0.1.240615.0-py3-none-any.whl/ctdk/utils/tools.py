import copy
import typing as t

_T = t.TypeVar("_T")


def merge_dicts(*dicts: t.Mapping[str, t.Any], overwrite: bool = False) -> t.Dict[str, t.Any]:
    """
    合并多个字典。如果键冲突，可以选择是否覆盖已有值。

    :param dicts: 需要合并的多个字典。
    :param overwrite: 是否在键冲突时覆盖已有值，默认值为 False。
    :return: 合并后的字典。
    :raises TypeError: 如果任何一个输入不是字典类型。

    使用示例：
    >>> dict1 = {'a': 1, 'b': {'x': 10}}
    >>> dict2 = {'b': {'y': 20}, 'c': 3}
    >>> merge_dicts(dict1, dict2, overwrite=True)
    {'a': 1, 'b': {'x': 10, 'y': 20}, 'c': 3}
    """

    def _merge(d1: t.Dict[str, t.Any], d2: t.Mapping[str, t.Any]) -> t.Dict[str, t.Any]:
        for key, value in d2.items():
            if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                d1[key] = _merge(d1[key], value)
            elif overwrite or key not in d1:
                d1[key] = value
        return d1

    merged_result = {}
    for dic in dicts:
        if not isinstance(dic, t.Mapping):
            raise TypeError(f"Expected dict, got {type(dic)}")
        merged_result = _merge(merged_result, copy.deepcopy(dic))

    return merged_result
