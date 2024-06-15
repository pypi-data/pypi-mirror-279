import collections
import logging
import typing as t

import pydantic as pyd

from ctdk.utils import EnvValue
from ctdk.types import ConfigValueType, Undefined, UndefinedType, NoneType

BaseConfigType = t.TypeVar('BaseConfigType', bound='BaseConfig')


class TypeConverter:
    """类型转换器类，用于注册和执行类型转换方法。"""

    __default_converters__: t.Dict[t.Tuple[t.Type, t.Type], t.Callable[[t.Any], t.Any]] = {}

    def __init__(self):
        """初始化方法，设置默认配置和客户自定义转换器。"""
        self.setting: t.Dict[str, bool] = {
            "convert_number_to_str": True,
            "calculate_model_matching": False,
            "env_value_first": False,
        }
        self.customer_converters: t.Dict[t.Tuple[t.Type, t.Type], t.Callable[[t.Any], t.Any]] = {}

    def set(self, **kwargs: bool):
        """更新转换器的配置设置。"""
        self.setting.update(kwargs)

    @staticmethod
    def gen_converter_key(from_type: t.Type, to_type: t.Type) -> t.Tuple[t.Type, t.Type]:
        if from_type is None:
            from_type = type(None)
        elif from_type is Undefined:
            from_type = UndefinedType
        elif from_type == '*':
            from_type = t.Any
        return from_type, to_type

    @classmethod
    def add_default_converter(
        cls,
        from_type: t.Type,
        to_type: t.Type,
    ) -> t.Callable[[t.Callable[[t.Any], t.Any]], t.Callable[[t.Any], t.Any]]:
        """
        注册默认类型转换方法。

        :param from_type: 源类型
        :param to_type: 目标类型
        :return: 装饰器函数
        """

        def decorator(func: t.Callable[[t.Any], t.Any]) -> t.Callable[[t.Any], t.Any]:
            cls.__default_converters__[cls.gen_converter_key(from_type, to_type)] = func
            return func

        return decorator

    def add_converter(
        self,
        from_type: t.Type,
        to_type: t.Type,
    ) -> t.Callable[[t.Callable[[t.Any], t.Any]], t.Callable[[t.Any], t.Any]]:
        """
        注册类型转换方法。

        :param from_type: 源类型
        :param to_type: 目标类型
        :return: 装饰器函数
        """

        def decorator(func: t.Callable[[t.Any], t.Any]) -> t.Callable[[t.Any], t.Any]:
            self.customer_converters[self.gen_converter_key(from_type, to_type)] = func
            return func

        return decorator

    def convert(self, obj: ConfigValueType, tp: t.Optional[t.Type]) -> t.Any:
        """
        根据注册的类型转换方法，将对象转换为目标类型。
        如果没有注册的方法，使用 pydantic.TypeAdapter 进行转换。

        :param obj: 需要转换的对象
        :param tp: 期望的目标类型
        :return: 转换后的对象
        :raises TypeError: 如果转换失败
        """
        from_type = type(obj)

        # 处理 Union 类型
        if t.get_origin(tp) is t.Union:
            for subtype in t.get_args(tp):
                if subtype is NoneType and obj in [None, Undefined]:
                    return None
                try:
                    return self.convert(obj, subtype)
                except (TypeError, ValueError):
                    continue

        # 处理 List 类型
        if t.get_origin(tp) is list and isinstance(obj, collections.Iterable):
            elem_type = t.get_args(tp)[0]
            return [self.convert(elem, elem_type) for elem in obj]

        # 处理 Dict 类型
        if t.get_origin(tp) is dict and isinstance(obj, collections.Mapping):
            key_type, value_type = t.get_args(tp)
            return {self.convert(k, key_type): self.convert(v, value_type) for k, v in obj.items()}

        # 处理 Set 类型
        if t.get_origin(tp) is set and isinstance(obj, collections.Iterable):
            elem_type = t.get_args(tp)[0]
            return {self.convert(elem, elem_type) for elem in obj}

        # 处理 Tuple 类型
        if t.get_origin(tp) is tuple and isinstance(obj, collections.Iterable):
            elem_types = t.get_args(tp)
            if len(elem_types) == 2 and elem_types[1] is Ellipsis:  # Tuple[T, ...] 形式
                return tuple(self.convert(elem, elem_types[0]) for elem in obj)
            else:
                return tuple(self.convert(elem, elem_type) for elem, elem_type in zip(obj, elem_types))

        # 尝试精确匹配转换
        for key in [(from_type, tp), (t.Any, tp)]:
            if key in self.customer_converters:
                try:
                    return self.customer_converters[key](obj)
                except (TypeError, ValueError) as e:
                    logging.debug(f"Conversion failed for {from_type} to {tp} using custom converter: {e}")

            if key in self.__default_converters__:
                func = self.__default_converters__[key]
                if self.setting.get(func.__name__):
                    try:
                        return func(obj)
                    except (TypeError, ValueError) as e:
                        logging.debug(f"Conversion failed for {from_type} to {tp} using default converter: {e}")

        # 使用 pydantic TypeAdapter 作为备用转换器
        try:
            return pyd.TypeAdapter(tp).validate_python(obj)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Cannot convert obj={obj} to {tp}. Please add a custom converter using `add_converter({type(obj).__name__}, {tp})`"
            ) from e

    def is_instance_of_type(self, value: t.Any, type_annotation: t.Type) -> bool:
        """
        检查值是否是给定类型的实例。

        :param value: 要检查的值
        :param type_annotation: 类型注解
        :return: 如果是给定类型的实例，则为True；否则为False
        """
        if t.get_origin(type_annotation) is t.Union:
            return any(self.is_instance_of_type(value, arg) for arg in t.get_args(type_annotation))

        # 处理普通类型
        return isinstance(value, type_annotation)

    @staticmethod
    def ordinal_scores():
        score = 0

        def get_score(*args, **kwargs) -> int:  # noqa: F841
            nonlocal score
            score -= 1
            return score

        return get_score

    def matching_score(self, model: t.Type[pyd.BaseModel], obj: t.Mapping[str, t.Any]) -> int:
        """
        计算给定对象与模型的匹配度得分。

        :param model: Pydantic模型
        :param obj: 待匹配的对象
        :return: 匹配度得分
        """
        if not (isinstance(model, type) and issubclass(model, pyd.BaseModel) and isinstance(obj, dict)):
            return 0
        score = 0
        for k, v in obj.items():
            if k in model.model_fields:
                field_info = model.model_fields[k]
                expected_type = field_info.annotation

                # 增加权重评分
                score += 1

                # 处理嵌套模型
                if isinstance(expected_type, type) and issubclass(expected_type, pyd.BaseModel) and isinstance(v, dict):
                    score += self.matching_score(expected_type, v)
                elif self.is_instance_of_type(v, expected_type):
                    # 精确类型匹配增加更多的分数
                    score += 2
                elif t.get_origin(expected_type) is t.Union:
                    # 处理 Union 类型
                    for subtype in t.get_args(expected_type):
                        if subtype is NoneType:
                            continue
                        if self.is_instance_of_type(v, subtype):
                            score += 2
                            break
                else:
                    # 处理不精确匹配
                    try:
                        self.convert(v, expected_type)
                        score += 1
                    except (TypeError, ValueError):
                        continue
        return score

    def gen_model(self, model: t.Type[BaseConfigType], config: t.Mapping[str, t.Any]) -> BaseConfigType:
        matching_score_func = self.matching_score if self.setting.get("calculate_model_matching") else self.ordinal_scores()

        def handle_union(_field_info, _value):
            subtypes = t.get_args(_field_info.annotation)
            res = []
            for subtype in subtypes:
                if isinstance(subtype, type) and issubclass(subtype, pyd.BaseModel) and isinstance(_value, dict):
                    try:
                        res.append((matching_score_func(subtype, _value), self.gen_model(subtype, _value)))
                    except (TypeError, ValueError):
                        continue
                else:
                    try:
                        res.append((matching_score_func(subtype, _value), self.convert(_value, subtype)))
                    except (TypeError, ValueError):
                        continue
            if res:
                return sorted(res, key=lambda x: x[0])[-1][-1]
            return self.convert(_value, _field_info.annotation)

        config_dict = {}
        if not (isinstance(model, type) and issubclass(model, pyd.BaseModel)):
            raise TypeError(f"{model=} must be a subclass of pydantic.BaseModel")
        if not isinstance(config, t.Mapping):
            raise TypeError(f"{config=} must be of type typing.Mapping")

        for k, field_info in model.model_fields.items():
            if self.setting.get("env_value_first") and isinstance(field_info.default, EnvValue):
                value = field_info.default
            else:
                value = config.get(k, field_info.default)
            if isinstance(value, EnvValue):
                value = value.get_value()
            expected_type = field_info.annotation
            if t.get_origin(field_info.annotation) is t.Union:
                config_dict[k] = handle_union(field_info, value)
            else:
                if isinstance(expected_type, type) and issubclass(expected_type, pyd.BaseModel) and isinstance(value, dict):
                    config_dict[k] = self.gen_model(expected_type, value)
                else:
                    config_dict[k] = self.convert(value, field_info.annotation)
        return model(**config_dict)


@TypeConverter.add_default_converter(int, str)
@TypeConverter.add_default_converter(float, str)
def convert_number_to_str(obj: t.Union[int, float]) -> str:
    """将数字转换为字符串。"""
    return str(obj)
