from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Series(_message.Message):
    __slots__ = ("points", "label", "units")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[float]
    label: str
    units: str
    def __init__(
        self, points: _Optional[_Iterable[float]] = ..., label: _Optional[str] = ..., units: _Optional[str] = ...
    ) -> None: ...

class Chart(_message.Message):
    __slots__ = ("title", "series", "x_timestamp_ms")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    X_TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[Series]
    x_timestamp_ms: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...,
        x_timestamp_ms: _Optional[_Iterable[int]] = ...,
    ) -> None: ...
