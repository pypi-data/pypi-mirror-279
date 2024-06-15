from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class CommandLineInterfaceVersion(_message.Message):
    __slots__ = ("version", "download_url", "os", "arch", "generation")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    version: str
    download_url: str
    os: str
    arch: str
    generation: int
    def __init__(
        self,
        version: _Optional[str] = ...,
        download_url: _Optional[str] = ...,
        os: _Optional[str] = ...,
        arch: _Optional[str] = ...,
        generation: _Optional[int] = ...,
    ) -> None: ...

class GetVersionsRequest(_message.Message):
    __slots__ = ("os", "arch")
    OS_FIELD_NUMBER: _ClassVar[int]
    ARCH_FIELD_NUMBER: _ClassVar[int]
    os: str
    arch: str
    def __init__(self, os: _Optional[str] = ..., arch: _Optional[str] = ...) -> None: ...

class GetVersionsResponse(_message.Message):
    __slots__ = ("versions", "latest", "nightly", "minimum")
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    LATEST_FIELD_NUMBER: _ClassVar[int]
    NIGHTLY_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedCompositeFieldContainer[CommandLineInterfaceVersion]
    latest: CommandLineInterfaceVersion
    nightly: CommandLineInterfaceVersion
    minimum: str
    def __init__(
        self,
        versions: _Optional[_Iterable[_Union[CommandLineInterfaceVersion, _Mapping]]] = ...,
        latest: _Optional[_Union[CommandLineInterfaceVersion, _Mapping]] = ...,
        nightly: _Optional[_Union[CommandLineInterfaceVersion, _Mapping]] = ...,
        minimum: _Optional[str] = ...,
    ) -> None: ...
