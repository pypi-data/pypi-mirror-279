# THIS FILE HAS BEEN GENERATED AUTOMATICALLY BY capnpy
# do not edit by hand
# generated on 2024-06-17 03:43
# cython: language_level=2

from capnpy cimport ptr as _ptr
from capnpy.struct_ cimport Struct as _Struct
from capnpy.struct_ cimport check_tag as _check_tag
from capnpy.struct_ import undefined as _undefined
from capnpy.enum import enum as _enum, fill_enum as _fill_enum
from capnpy.enum cimport BaseEnum as _BaseEnum
from capnpy.type import Types as _Types
from capnpy.segment.segment cimport Segment as _Segment
from capnpy.segment.segment cimport MultiSegment as _MultiSegment
from capnpy.segment.builder cimport SegmentBuilder as _SegmentBuilder
from capnpy.list cimport List as _List
from capnpy.list cimport PrimitiveItemType as _PrimitiveItemType
from capnpy.list cimport BoolItemType as _BoolItemType
from capnpy.list cimport TextItemType as _TextItemType
from capnpy.list cimport TextUnicodeItemType as _TextUnicodeItemType
from capnpy.list cimport StructItemType as _StructItemType
from capnpy.list cimport EnumItemType as _EnumItemType
from capnpy.list cimport VoidItemType as _VoidItemType
from capnpy.list cimport ListItemType as _ListItemType
from capnpy.anypointer import AnyPointer as _AnyPointer
from capnpy.util import text_bytes_repr as _text_bytes_repr
from capnpy.util import text_unicode_repr as _text_unicode_repr
from capnpy.util import data_repr as _data_repr
from capnpy.util import float32_repr as _float32_repr
from capnpy.util import float64_repr as _float64_repr
from capnpy.util import extend_module_maybe as _extend_module_maybe
from capnpy.util import check_version as _check_version
from capnpy.util import encode_maybe as _encode_maybe
from capnpy cimport _hash
from capnpy.list cimport void_list_item_type as _void_list_item_type
from capnpy.list cimport bool_list_item_type as _bool_list_item_type
from capnpy.list cimport int8_list_item_type as _int8_list_item_type
from capnpy.list cimport uint8_list_item_type as _uint8_list_item_type
from capnpy.list cimport int16_list_item_type as _int16_list_item_type
from capnpy.list cimport uint16_list_item_type as _uint16_list_item_type
from capnpy.list cimport int32_list_item_type as _int32_list_item_type
from capnpy.list cimport uint32_list_item_type as _uint32_list_item_type
from capnpy.list cimport int64_list_item_type as _int64_list_item_type
from capnpy.list cimport uint64_list_item_type as _uint64_list_item_type
from capnpy.list cimport float32_list_item_type as _float32_list_item_type
from capnpy.list cimport float64_list_item_type as _float64_list_item_type
from capnpy.list cimport data_list_item_type as _data_list_item_type
from capnpy.list cimport text_bytes_list_item_type as _text_bytes_list_item_type
from capnpy.list cimport text_unicode_list_item_type as _text_unicode_list_item_type
__capnpy_id__ = 0x9accdfe4a45164eb
__capnpy_version__ = '0.10.1'
__capnproto_version__ = '0.5.3.1'
# schema compiled with --no-version-check, skipping the call to _check_version
import podping_schemas.rust as _rust_capnp
from capnpy.schema import CodeGeneratorRequest as _CodeGeneratorRequest
from capnpy.annotate import Options as _Options
from capnpy.reflection import ReflectionData as _ReflectionData
class _podping_reason_ReflectionData(_ReflectionData):
    request = _CodeGeneratorRequest.from_buffer(_Segment(b'\x00\x00\x00\x00\x00\x00\x02\x00\x05\x00\x00\x00g\x01\x00\x00\xed\x01\x00\x00\x1f\x00\x00\x00\x10\x00\x00\x00\x05\x00\x06\x00\x89\xbc\xec\xac\xdf\x1f\x9a\xd9P\x00\x00\x00\x02\x00\x00\x00\xebdQ\xa4\xe4\xdf\xcc\x9a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00\xf2\x02\x00\x00\xc5\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc1\x00\x00\x00O\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x83\xd0\x8d<L\xc1\xb3\x83\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd5\x00\x00\x00\xda\x00\x00\x00\xe1\x00\x00\x007\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x03E\xd1l8\xee\xab\x1b\x00\x00\x00\x05\x00\x01\x00\x83\xd0\x8d<L\xc1\xb3\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe5\x00\x00\x00B\x01\x00\x00\xf5\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xebdQ\xa4\xe4\xdf\xcc\x9aJ\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe1\x00\x00\x00\x82\x02\x00\x00\x05\x01\x00\x00\x17\x00\x00\x00\x15\x01\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_reason.capnp:PodpingReason\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x0c\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00update\x00\x00live\x00\x00\x00\x00liveEnd\x00podping_schemas/rust.capnp\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x01\x00\xd0f\x01\x10mL\xfe\xc2\x11\x00\x00\x00*\x00\x00\x00d\x03E\xd1l8\xee\xab\r\x00\x00\x00j\x00\x00\x00N\x96\xe1N,\xf2\xfe\xab\r\x00\x00\x00:\x00\x00\x00name\x00\x00\x00\x00parentModule\x00\x00\x00\x00option\x00\x00podping_schemas/rust.capnp:parentModule\x00\x00\x00\x00\x00\x01\x00\x01\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_reason.capnp\x00\x04\x00\x00\x00\x01\x00\x01\x00\x89\xbc\xec\xac\xdf\x1f\x9a\xd9\x01\x00\x00\x00r\x00\x00\x00PodpingReason\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00d\x03E\xd1l8\xee\xab\x04\x00\x00\x00\x02\x00\x01\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\xda\x00\x00\x00org::podcastindex::podping\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\xebdQ\xa4\xe4\xdf\xcc\x9a\x05\x00\x00\x00\x82\x02\x00\x00)\x00\x00\x00\x17\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_reason.capnp\x00\x04\x00\x00\x00\x01\x00\x01\x00\x83\xd0\x8d<L\xc1\xb3\x83\x01\x00\x00\x00\xe2\x00\x00\x00/podping_schemas/rust.capnp\x00\x00\x00\x00\x00'), 8, 0, 2)
    default_options = _Options.from_buffer(_Segment(b'\x02\x00\x02\x00\x02\x00\x03\x00'), 0, 1, 0)
    pyx = True
_reflection_data = _podping_reason_ReflectionData()

#### FORWARD DECLARATIONS ####

cdef class PodpingReason(_BaseEnum):
    __capnpy_id__ = 15679880098183167113
    __members__ = ('update', 'live', 'liveEnd',)
    @staticmethod
    cdef _new(long x, __prebuilt=(PodpingReason(0), PodpingReason(1), PodpingReason(2),)):
        try:
            return __prebuilt[x]
        except IndexError:
            return PodpingReason(x)
    @staticmethod
    def _new_hack(long x, __prebuilt=(PodpingReason(0), PodpingReason(1), PodpingReason(2),)):
        try:
            return __prebuilt[x]
        except IndexError:
            return PodpingReason(x)
_fill_enum(PodpingReason)
_PodpingReason_list_item_type = _EnumItemType(PodpingReason)


#### DEFINITIONS ####


_extend_module_maybe(globals(), modname=__name__)