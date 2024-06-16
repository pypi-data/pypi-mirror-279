# THIS FILE HAS BEEN GENERATED AUTOMATICALLY BY capnpy
# do not edit by hand
# generated on 2024-06-16 03:36
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
__capnpy_id__ = 0xedda8f1fc8b626fe
__capnpy_version__ = '0.10.1'
__capnproto_version__ = '0.5.3.1'
# schema compiled with --no-version-check, skipping the call to _check_version
from capnpy.schema import CodeGeneratorRequest as _CodeGeneratorRequest
from capnpy.annotate import Options as _Options
from capnpy.reflection import ReflectionData as _ReflectionData
class _podping_medium_ReflectionData(_ReflectionData):
    request = _CodeGeneratorRequest.from_buffer(_Segment(b'\x00\x00\x00\x00\x00\x00\x02\x00\x05\x00\x00\x00\xb7\x00\x00\x00\xd5\x01\x00\x00\x1f\x00\x00\x00\x08\x00\x00\x00\x05\x00\x06\x00\x80\xa2v\xa5u\x16\xe8\xaaP\x00\x00\x00\x02\x00\x00\x00\xfe&\xb6\xc8\x1f\x8f\xda\xed\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x00\x00\x00\xf2\x02\x00\x00m\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00i\x00\x00\x00o\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe&\xb6\xc8\x1f\x8f\xda\xedJ\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Q\x01\x00\x00\x82\x02\x00\x00u\x01\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_medium.capnp:PodpingMedium\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00<\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\xad\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xa5\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x9d\x00\x00\x00J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x91\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x89\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x81\x00\x00\x00:\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00y\x00\x00\x00*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00q\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00i\x00\x00\x00R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00e\x00\x00\x00Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00a\x00\x00\x00Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00]\x00\x00\x00b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\x00\x00\x00Y\x00\x00\x00*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00Q\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00mixed\x00\x00\x00podcast\x00podcastL\x00\x00\x00\x00\x00\x00\x00\x00music\x00\x00\x00musicL\x00\x00video\x00\x00\x00videoL\x00\x00film\x00\x00\x00\x00filmL\x00\x00\x00audiobook\x00\x00\x00\x00\x00\x00\x00audiobookL\x00\x00\x00\x00\x00\x00newsletter\x00\x00\x00\x00\x00\x00newsletterL\x00\x00\x00\x00\x00blog\x00\x00\x00\x00blogL\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_medium.capnp\x00\x04\x00\x00\x00\x01\x00\x01\x00\x80\xa2v\xa5u\x16\xe8\xaa\x01\x00\x00\x00r\x00\x00\x00PodpingMedium\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\xfe&\xb6\xc8\x1f\x8f\xda\xed\x05\x00\x00\x00\x82\x02\x00\x00)\x00\x00\x00\x07\x00\x00\x00/github/workspace/podping_schemas/org/podcastindex/podping/podping_medium.capnp\x00\x00\x00\x00\x00\x01\x00\x01\x00'), 8, 0, 2)
    default_options = _Options.from_buffer(_Segment(b'\x02\x00\x02\x00\x02\x00\x03\x00'), 0, 1, 0)
    pyx = True
_reflection_data = _podping_medium_ReflectionData()

#### FORWARD DECLARATIONS ####

cdef class PodpingMedium(_BaseEnum):
    __capnpy_id__ = 12315117875587621504
    __members__ = ('mixed', 'podcast', 'podcastL', 'music', 'musicL', 'video', 'videoL', 'film', 'filmL', 'audiobook', 'audiobookL', 'newsletter', 'newsletterL', 'blog', 'blogL',)
    @staticmethod
    cdef _new(long x, __prebuilt=(PodpingMedium(0), PodpingMedium(1), PodpingMedium(2), PodpingMedium(3), PodpingMedium(4), PodpingMedium(5), PodpingMedium(6), PodpingMedium(7), PodpingMedium(8), PodpingMedium(9), PodpingMedium(10), PodpingMedium(11), PodpingMedium(12), PodpingMedium(13), PodpingMedium(14),)):
        try:
            return __prebuilt[x]
        except IndexError:
            return PodpingMedium(x)
    @staticmethod
    def _new_hack(long x, __prebuilt=(PodpingMedium(0), PodpingMedium(1), PodpingMedium(2), PodpingMedium(3), PodpingMedium(4), PodpingMedium(5), PodpingMedium(6), PodpingMedium(7), PodpingMedium(8), PodpingMedium(9), PodpingMedium(10), PodpingMedium(11), PodpingMedium(12), PodpingMedium(13), PodpingMedium(14),)):
        try:
            return __prebuilt[x]
        except IndexError:
            return PodpingMedium(x)
_fill_enum(PodpingMedium)
_PodpingMedium_list_item_type = _EnumItemType(PodpingMedium)


#### DEFINITIONS ####


_extend_module_maybe(globals(), modname=__name__)