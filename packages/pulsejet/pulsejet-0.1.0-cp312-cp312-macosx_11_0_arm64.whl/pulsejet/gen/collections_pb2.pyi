import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_pb2 import RawEmbed as RawEmbed
from common_pb2 import Embed as Embed
from common_pb2 import Embeds as Embeds
from common_pb2 import OperationStatus as OperationStatus

DESCRIPTOR: _descriptor.FileDescriptor
OK: _common_pb2.OperationStatus
Error: _common_pb2.OperationStatus

class IndexType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FlatL2: _ClassVar[IndexType]
    FlatIP: _ClassVar[IndexType]
    HNSW: _ClassVar[IndexType]
    IVFFlat: _ClassVar[IndexType]
    IVFScalar: _ClassVar[IndexType]
    IVFPQ: _ClassVar[IndexType]
    OPQPQ: _ClassVar[IndexType]
FlatL2: IndexType
FlatIP: IndexType
HNSW: IndexType
IVFFlat: IndexType
IVFScalar: IndexType
IVFPQ: IndexType
OPQPQ: IndexType

class VectorParams(_message.Message):
    __slots__ = ("size", "index_type")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    size: int
    index_type: IndexType
    def __init__(self, size: _Optional[int] = ..., index_type: _Optional[_Union[IndexType, str]] = ...) -> None: ...

class OpCreateCollection(_message.Message):
    __slots__ = ("name", "vector_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    vector_config: VectorParams
    def __init__(self, name: _Optional[str] = ..., vector_config: _Optional[_Union[VectorParams, _Mapping]] = ...) -> None: ...

class OpDeleteCollection(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class OpUpdateCollection(_message.Message):
    __slots__ = ("name", "new_name", "vector_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    new_name: str
    vector_config: VectorParams
    def __init__(self, name: _Optional[str] = ..., new_name: _Optional[str] = ..., vector_config: _Optional[_Union[VectorParams, _Mapping]] = ...) -> None: ...

class OpListCollections(_message.Message):
    __slots__ = ("filter",)
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: str
    def __init__(self, filter: _Optional[str] = ...) -> None: ...

class CreateCollectionResponse(_message.Message):
    __slots__ = ("response", "status")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    response: _common_pb2.OperationStatus
    status: str
    def __init__(self, response: _Optional[_Union[_common_pb2.OperationStatus, str]] = ..., status: _Optional[str] = ...) -> None: ...

class DeleteCollectionResponse(_message.Message):
    __slots__ = ("response", "status")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    response: _common_pb2.OperationStatus
    status: str
    def __init__(self, response: _Optional[_Union[_common_pb2.OperationStatus, str]] = ..., status: _Optional[str] = ...) -> None: ...

class UpdateCollectionResponse(_message.Message):
    __slots__ = ("response", "status")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    response: _common_pb2.OperationStatus
    status: str
    def __init__(self, response: _Optional[_Union[_common_pb2.OperationStatus, str]] = ..., status: _Optional[str] = ...) -> None: ...

class ListCollectionsResponse(_message.Message):
    __slots__ = ("response", "status")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    response: _common_pb2.OperationStatus
    status: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, response: _Optional[_Union[_common_pb2.OperationStatus, str]] = ..., status: _Optional[_Iterable[str]] = ...) -> None: ...
