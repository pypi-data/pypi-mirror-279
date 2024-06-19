from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class HealthCheckStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_CHECK_STATUS_UNSPECIFIED: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_OK: _ClassVar[HealthCheckStatus]
    HEALTH_CHECK_STATUS_FAILING: _ClassVar[HealthCheckStatus]

HEALTH_CHECK_STATUS_UNSPECIFIED: HealthCheckStatus
HEALTH_CHECK_STATUS_OK: HealthCheckStatus
HEALTH_CHECK_STATUS_FAILING: HealthCheckStatus

class HealthCheck(_message.Message):
    __slots__ = ("name", "status", "message")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: HealthCheckStatus
    message: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        status: _Optional[_Union[HealthCheckStatus, str]] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class CheckHealthRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CheckHealthResponse(_message.Message):
    __slots__ = ("checks",)
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...
