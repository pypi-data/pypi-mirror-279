import datetime
import typing as t

from pydantic_core import PydanticUndefined as Undefined

UndefinedType = type(Undefined)
BaseType = t.Union[str, int, float, bool, None, datetime.date, datetime.datetime]
ContainerType = t.Union[
    t.Dict[str, t.Union[BaseType, 'ContainerType']],
    t.List[t.Union[BaseType, 'ContainerType']]
]
ConfigValueType = t.Union[BaseType, ContainerType]
NoneType = type(None)
