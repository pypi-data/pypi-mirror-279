import json
import logging
import typing as t
import warnings
from pathlib import Path

import pydantic as pyd
import yaml

from ctdk.utils import ENV
from ctdk.utils.tools import merge_dicts
from ctdk.types import UndefinedType, Undefined
from .type_converter import TypeConverter

_T = t.TypeVar("_T")
BaseModelType = type(pyd.BaseModel)


class ConfigLoader(t.Mapping):
    def __init__(self, path: t.Optional[str], *, strict=False):
        self.path = Path(path) if path else None
        self.strict = strict
        self.dic = {}

        if not self.path or not self.path.exists():
            if self.strict:
                raise ValueError(f"file not exists. path={path}")
            return

        loader_dic = {
            ".json": self.json_loader,
            ".yaml": self.yaml_loader,
            ".yml": self.yaml_loader,
            ".toml": self.toml_loader,
            ".env": self.env_loader,
            ".xml": self.xml_loader,
        }
        loader_func: t.Callable[[Path], dict] = loader_dic.get(self.path.suffix, self.default_loader)
        self.dic = loader_func(self.path)

    def json_loader(self, path: Path) -> dict:
        try:
            with path.open("r") as fp:
                return json.load(fp)
        except Exception as e:
            if self.strict:
                raise
            logging.warning(f"config load failed, path={path}, e={e}")
            return {}

    def yaml_loader(self, path: Path) -> dict:
        try:
            with path.open("r") as fp:
                return yaml.safe_load(fp)
        except Exception as e:
            if self.strict:
                raise
            logging.warning(f"config load failed, {path=}, {e=}")
            return {}

    def default_loader(self, path: Path) -> dict:
        msg = f"unsupported file type {path.suffix or path.name}"
        if self.strict:
            raise ValueError(msg)
        logging.warning(msg)
        return {}

    toml_loader = env_loader = xml_loader = default_loader

    def get(self, __key: str, default: _T = Undefined) -> t.Union[_T, UndefinedType]:
        return self.dic.get(__key, default)

    def __getitem__(self, __key) -> t.Any:
        return self.dic[__key]

    def __len__(self):
        return len(self.dic)

    def __iter__(self):
        return iter(self.dic)


class ConfigGetter:
    def __init__(self, name: str = None, *paths: str):
        self.paths = []
        self.name = name
        if self.name:
            self.paths.extend([
                f"./{self.name}.yaml",
                f"./{self.name}.yml",
                f"~/.ct/{self.name}.yaml",
                f"~/.ct/{self.name}.yml",
            ])

        if not paths:
            paths = [
                "./config.yaml", "./config.yml",
                "/config/config.yaml", "/config/config.yml",
            ]
        self.paths.extend(paths)
        self.dic = merge_dicts(*[ConfigLoader(path) for path in sorted(set(self.paths), key=self.paths.index)])
        if self.name:
            ct_conf_path = [
                "~/.ct/config.yaml", "~/.ct/config.yml",
            ]
            ct_conf = merge_dicts(*[ConfigLoader(path) for path in ct_conf_path]).get(self.name, {})
            self.dic = merge_dicts(self.dic, ct_conf)

    def __call__(self, key: str, default: _T = Undefined) -> t.Union[_T, UndefinedType]:
        p = self.dic
        ks = key.split(".")
        for k in ks:
            if isinstance(p, t.Mapping) and k in p:
                p = p[k]
            else:
                return default
        return p


BaseConfigType = t.TypeVar('BaseConfigType', bound='BaseConfig')


class BaseConfig(pyd.BaseModel):
    __converter__: TypeConverter = TypeConverter()
    __setting__: t.Dict[str, bool] = {"auto_init_sentry": True}
    model_config = pyd.ConfigDict(arbitrary_types_allowed=True)

    if t.TYPE_CHECKING:
        @classmethod
        def set(
            cls, *,
            convert_number_to_str: bool = True,
            auto_init_sentry: bool = True,
            calculate_model_matching: bool = False,
            env_value_first: bool = False,
        ):
            pass

    else:
        @classmethod
        def set(cls, **kwargs: bool):
            dic = {}
            for k, v in kwargs.items():
                if k in cls.__setting__:
                    cls.__setting__[k] = v
                else:
                    dic[k] = v
            cls.__converter__.set(**dic)

    @classmethod
    def add_converter(
        cls,
        from_type: t.Any,
        to_type: t.Type,
    ) -> t.Callable[[t.Callable[[t.Any], t.Any]], t.Callable[[t.Any], t.Any]]:
        """
        注册一个类型转换方法

        :param from_type: 源类型
        :param to_type: 目标类型
        :return: 装饰器函数
        """
        return cls.__converter__.add_converter(from_type, to_type)

    @classmethod
    def load(
        cls: t.Type[BaseConfigType],
        path: str = ENV("CONFIG_PATH", None), *,
        config: t.Optional[t.Mapping[str, t.Any]] = None
    ) -> BaseConfigType:
        if config is None:
            config = ConfigLoader(path)

        conf_obj = cls.__converter__.gen_model(cls, config)
        sentry_conf = getattr(conf_obj, 'sentry', None)

        if cls.__setting__["auto_init_sentry"] and sentry_conf and isinstance(sentry_conf, SentryConfig) and sentry_conf.enabled:
            try:
                import sentry_sdk  # noqa
            except ImportError:
                warnings.warn("sentry_sdk not installed, sentry disabled")
            else:
                sentry_sdk.init(sentry_conf.sentry_url, traces_sample_rate=sentry_conf.traces_sample_rate)

        return conf_obj


class SentryConfig(pyd.BaseModel):
    enabled: bool = ENV("SENTRY_ENABLED", False)
    sentry_url: pyd.AnyUrl = ENV("SENTRY_URL", 'https://956c651fad8345ef8f656aee3a38834e@o1230294.ingest.sentry.io/6376868')
    traces_sample_rate: float = ENV("SENTRY_TRACES_RATE", 1.0)
