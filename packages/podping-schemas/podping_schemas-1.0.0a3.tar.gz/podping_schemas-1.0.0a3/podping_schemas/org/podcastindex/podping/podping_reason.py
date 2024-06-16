# THIS FILE HAS BEEN GENERATED AUTOMATICALLY BY capnpy
# do not edit by hand
# generated on 2024-06-16 03:37
# cython: language_level=2

from capnpy import ptr as _ptr
from capnpy.struct_ import Struct as _Struct
from capnpy.struct_ import check_tag as _check_tag
from capnpy.struct_ import undefined as _undefined
from capnpy.enum import enum as _enum, fill_enum as _fill_enum
from capnpy.enum import BaseEnum as _BaseEnum
from capnpy.type import Types as _Types
from capnpy.segment.segment import Segment as _Segment
from capnpy.segment.segment import MultiSegment as _MultiSegment
from capnpy.segment.builder import SegmentBuilder as _SegmentBuilder
from capnpy.list import List as _List
from capnpy.list import PrimitiveItemType as _PrimitiveItemType
from capnpy.list import BoolItemType as _BoolItemType
from capnpy.list import TextItemType as _TextItemType
from capnpy.list import TextUnicodeItemType as _TextUnicodeItemType
from capnpy.list import StructItemType as _StructItemType
from capnpy.list import EnumItemType as _EnumItemType
from capnpy.list import VoidItemType as _VoidItemType
from capnpy.list import ListItemType as _ListItemType
from capnpy.anypointer import AnyPointer as _AnyPointer
from capnpy.util import text_bytes_repr as _text_bytes_repr
from capnpy.util import text_unicode_repr as _text_unicode_repr
from capnpy.util import data_repr as _data_repr
from capnpy.util import float32_repr as _float32_repr
from capnpy.util import float64_repr as _float64_repr
from capnpy.util import extend_module_maybe as _extend_module_maybe
from capnpy.util import check_version as _check_version
from capnpy.util import encode_maybe as _encode_maybe
__capnpy_id__ = 0x9accdfe4a45164eb
__capnpy_version__ = '0.10.1'
__capnproto_version__ = '0.5.3.1'
# schema compiled with --no-version-check, skipping the call to _check_version
from capnpy.schema import CodeGeneratorRequest as _CodeGeneratorRequest
from capnpy.annotate import Options as _Options
from capnpy.reflection import ReflectionData as _ReflectionData
class _podping_reason_ReflectionData(_ReflectionData):
    request = _CodeGeneratorRequest.from_buffer(_Segment(b'\x00\x00\x00\x00\x00\x00\x02\x00\x05\x00\x00\x00\xb7\x00\x00\x00\x01\x01\x00\x00\x1f\x00\x00\x00\x08\x00\x00\x00\x05\x00\x06\x00\x89\xbc\xec\xac\xdf\x1f\x9a\xd9P\x00\x00\x00\x02\x00\x00\x00\xebdQ\xa4\xe4\xdf\xcc\x9a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x00\x00\x00\xf2\x02\x00\x00m\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00i\x00\x00\x00O\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xebdQ\xa4\xe4\xdf\xcc\x9aJ\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00}\x00\x00\x00\x82\x02\x00\x00\xa1\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_reason.capnp:PodpingReason\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x0c\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00update\x00\x00live\x00\x00\x00\x00liveEnd\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_reason.capnp\x00\x04\x00\x00\x00\x01\x00\x01\x00\x89\xbc\xec\xac\xdf\x1f\x9a\xd9\x01\x00\x00\x00r\x00\x00\x00PodpingReason\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\xebdQ\xa4\xe4\xdf\xcc\x9a\x05\x00\x00\x00\x82\x02\x00\x00)\x00\x00\x00\x07\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_reason.capnp\x00\x00\x00\x00\x00\x01\x00\x01\x00'), 8, 0, 2)
    default_options = _Options.from_buffer(_Segment(b'\x02\x00\x02\x00\x02\x00\x03\x00'), 0, 1, 0)
    pyx = False
_reflection_data = _podping_reason_ReflectionData()

#### FORWARD DECLARATIONS ####

class PodpingReason(_BaseEnum):
    __capnpy_id__ = 15679880098183167113
    __members__ = ('update', 'live', 'liveEnd',)
    @staticmethod
    def _new(x):
        return PodpingReason(x)
_fill_enum(PodpingReason)
_PodpingReason_list_item_type = _EnumItemType(PodpingReason)


#### DEFINITIONS ####


_extend_module_maybe(globals(), modname=__name__)