# THIS FILE HAS BEEN GENERATED AUTOMATICALLY BY capnpy
# do not edit by hand
# generated on 2024-06-17 03:45
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
__capnpy_id__ = 0x83b3c14c3c8dd083
__capnpy_version__ = '0.10.1'
__capnproto_version__ = '0.5.3.1'
# schema compiled with --no-version-check, skipping the call to _check_version
from capnpy.schema import CodeGeneratorRequest as _CodeGeneratorRequest
from capnpy.annotate import Options as _Options
from capnpy.reflection import ReflectionData as _ReflectionData
class _rust_ReflectionData(_ReflectionData):
    request = _CodeGeneratorRequest.from_buffer(_Segment(b"\x00\x00\x00\x00\x00\x00\x02\x00\x05\x00\x00\x00g\x01\x00\x00\x8d\x01\x00\x00\x1f\x00\x00\x00\x10\x00\x00\x00\x05\x00\x06\x00N\x96\xe1N,\xf2\xfe\xab-\x00\x00\x00\x05\x00 \x00\x83\xd0\x8d<L\xc1\xb3\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00\xa2\x01\x00\x00\xb1\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xac\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x03E\xd1l8\xee\xab-\x00\x00\x00\x05\x00\x01\x00\x83\xd0\x8d<L\xc1\xb3\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x9d\x00\x00\x00\xd2\x01\x00\x00\xb9\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd0f\x01\x10mL\xfe\xc2-\x00\x00\x00\x05\x00\xfc\x00\x83\xd0\x8d<L\xc1\xb3\x83\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa5\x00\x00\x00\x92\x01\x00\x00\xbd\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb8\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x83\xd0\x8d<L\xc1\xb3\x83'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa9\x00\x00\x00j\x01\x00\x00\xbd\x00\x00\x007\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/rust.capnp:option\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/rust.capnp:parentModule\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/rust.capnp:name\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00/github/workspace/podping_schemas/rust.capnp\x00\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x01\x00\xd0f\x01\x10mL\xfe\xc2\x11\x00\x00\x00*\x00\x00\x00d\x03E\xd1l8\xee\xab\r\x00\x00\x00j\x00\x00\x00N\x96\xe1N,\xf2\xfe\xab\r\x00\x00\x00:\x00\x00\x00name\x00\x00\x00\x00parentModule\x00\x00\x00\x00option\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\x83\xd0\x8d<L\xc1\xb3\x83\x05\x00\x00\x00j\x01\x00\x00\x19\x00\x00\x00\x07\x00\x00\x00/github/workspace/podping_schemas/rust.capnp\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00"), 8, 0, 2)
    default_options = _Options.from_buffer(_Segment(b'\x02\x00\x02\x00\x02\x00\x03\x00'), 0, 1, 0)
    pyx = False
_reflection_data = _rust_ReflectionData()

#### FORWARD DECLARATIONS ####

class option(object):
    __capnpy_id__ = 0xabfef22c4ee1964e
    targets_file = False
    targets_const = False
    targets_enum = False
    targets_enumerant = False
    targets_struct = False
    targets_field = True
    targets_union = False
    targets_group = False
    targets_interface = False
    targets_method = False
    targets_param = False
    targets_annotation = False
class parentModule(object):
    __capnpy_id__ = 0xabee386cd1450364
    targets_file = True
    targets_const = False
    targets_enum = False
    targets_enumerant = False
    targets_struct = False
    targets_field = False
    targets_union = False
    targets_group = False
    targets_interface = False
    targets_method = False
    targets_param = False
    targets_annotation = False
class name(object):
    __capnpy_id__ = 0xc2fe4c6d100166d0
    targets_file = False
    targets_const = False
    targets_enum = True
    targets_enumerant = True
    targets_struct = True
    targets_field = True
    targets_union = True
    targets_group = True
    targets_interface = False
    targets_method = False
    targets_param = False
    targets_annotation = False

#### DEFINITIONS ####


_extend_module_maybe(globals(), modname=__name__)