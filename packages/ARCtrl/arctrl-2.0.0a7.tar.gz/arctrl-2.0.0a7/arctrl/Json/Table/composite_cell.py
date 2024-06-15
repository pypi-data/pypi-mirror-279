from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (singleton, of_array, FSharpList)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_fail, printf, to_text)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import to_enumerable
from ...fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, index, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string
from ...Core.data import Data
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.composite_cell import CompositeCell
from ..encode import default_spaces
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)
from ..Process.data import (Data_encoder, Data_decoder, Data_compressedEncoder, Data_compressedDecoder)
from ..string_table import (encode_string, decode_string)
from .oatable import (encode_oa, decode_oa)

def CompositeCell_encoder(cc: CompositeCell) -> Json:
    def oa_to_json_string(oa: OntologyAnnotation, cc: Any=cc) -> Json:
        return OntologyAnnotation_encoder(oa)

    pattern_input: tuple[str, FSharpList[Json]] = (("Term", singleton(oa_to_json_string(cc.fields[0])))) if (cc.tag == 0) else ((("Unitized", of_array([Json(0, cc.fields[0]), oa_to_json_string(cc.fields[1])]))) if (cc.tag == 2) else ((("Data", singleton(Data_encoder(cc.fields[0])))) if (cc.tag == 3) else (("FreeText", singleton(Json(0, cc.fields[0]))))))
    return Json(5, to_enumerable([("celltype", Json(0, pattern_input[0])), ("values", list_1(pattern_input[1]))]))


def _arrow1587(get: IGetters) -> CompositeCell:
    match_value: str
    object_arg: IRequiredGetter = get.Required
    match_value = object_arg.Field("celltype", string)
    def _arrow1582(__unit: None=None) -> str:
        arg_3: Decoder_1[str] = index(0, string)
        object_arg_1: IRequiredGetter = get.Required
        return object_arg_1.Field("values", arg_3)

    def _arrow1583(__unit: None=None) -> OntologyAnnotation:
        arg_5: Decoder_1[OntologyAnnotation] = index(0, OntologyAnnotation_decoder)
        object_arg_2: IRequiredGetter = get.Required
        return object_arg_2.Field("values", arg_5)

    def _arrow1584(__unit: None=None) -> str:
        arg_7: Decoder_1[str] = index(0, string)
        object_arg_3: IRequiredGetter = get.Required
        return object_arg_3.Field("values", arg_7)

    def _arrow1585(__unit: None=None) -> OntologyAnnotation:
        arg_9: Decoder_1[OntologyAnnotation] = index(1, OntologyAnnotation_decoder)
        object_arg_4: IRequiredGetter = get.Required
        return object_arg_4.Field("values", arg_9)

    def _arrow1586(__unit: None=None) -> Data:
        arg_11: Decoder_1[Data] = index(0, Data_decoder)
        object_arg_5: IRequiredGetter = get.Required
        return object_arg_5.Field("values", arg_11)

    return CompositeCell(1, _arrow1582()) if (match_value == "FreeText") else (CompositeCell(0, _arrow1583()) if (match_value == "Term") else (CompositeCell(2, _arrow1584(), _arrow1585()) if (match_value == "Unitized") else (CompositeCell(3, _arrow1586()) if (match_value == "Data") else to_fail(printf("Error reading CompositeCell from json string: %A"))(match_value))))


CompositeCell_decoder: Decoder_1[CompositeCell] = object(_arrow1587)

def CompositeCell_encoderCompressed(string_table: Any, oa_table: Any, cc: CompositeCell) -> Json:
    pattern_input: tuple[str, FSharpList[Json]] = (("Term", singleton(encode_oa(oa_table, cc.fields[0])))) if (cc.tag == 0) else ((("Unitized", of_array([encode_string(string_table, cc.fields[0]), encode_oa(oa_table, cc.fields[1])]))) if (cc.tag == 2) else ((("Data", singleton(Data_compressedEncoder(string_table, cc.fields[0])))) if (cc.tag == 3) else (("FreeText", singleton(encode_string(string_table, cc.fields[0]))))))
    return Json(5, to_enumerable([("t", encode_string(string_table, pattern_input[0])), ("v", list_1(pattern_input[1]))]))


def CompositeCell_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation]) -> Decoder_1[CompositeCell]:
    def _arrow1593(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table) -> CompositeCell:
        match_value: str
        arg_1: Decoder_1[str] = decode_string(string_table)
        object_arg: IRequiredGetter = get.Required
        match_value = object_arg.Field("t", arg_1)
        def _arrow1588(__unit: None=None) -> str:
            arg_3: Decoder_1[str] = index(0, decode_string(string_table))
            object_arg_1: IRequiredGetter = get.Required
            return object_arg_1.Field("v", arg_3)

        def _arrow1589(__unit: None=None) -> OntologyAnnotation:
            arg_5: Decoder_1[OntologyAnnotation] = index(0, decode_oa(oa_table))
            object_arg_2: IRequiredGetter = get.Required
            return object_arg_2.Field("v", arg_5)

        def _arrow1590(__unit: None=None) -> str:
            arg_7: Decoder_1[str] = index(0, decode_string(string_table))
            object_arg_3: IRequiredGetter = get.Required
            return object_arg_3.Field("v", arg_7)

        def _arrow1591(__unit: None=None) -> OntologyAnnotation:
            arg_9: Decoder_1[OntologyAnnotation] = index(1, decode_oa(oa_table))
            object_arg_4: IRequiredGetter = get.Required
            return object_arg_4.Field("v", arg_9)

        def _arrow1592(__unit: None=None) -> Data:
            arg_11: Decoder_1[Data] = index(0, Data_compressedDecoder(string_table))
            object_arg_5: IRequiredGetter = get.Required
            return object_arg_5.Field("v", arg_11)

        return CompositeCell(1, _arrow1588()) if (match_value == "FreeText") else (CompositeCell(0, _arrow1589()) if (match_value == "Term") else (CompositeCell(2, _arrow1590(), _arrow1591()) if (match_value == "Unitized") else (CompositeCell(3, _arrow1592()) if (match_value == "Data") else to_fail(printf("Error reading CompositeCell from json string: %A"))(match_value))))

    return object(_arrow1593)


def ARCtrl_CompositeCell__CompositeCell_fromJsonString_Static_Z721C83C5(s: str) -> CompositeCell:
    match_value: FSharpResult_2[CompositeCell, str] = Decode_fromString(CompositeCell_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_CompositeCell__CompositeCell_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[CompositeCell], str]:
    def _arrow1594(obj: CompositeCell, spaces: Any=spaces) -> str:
        value: Json = CompositeCell_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1594


def ARCtrl_CompositeCell__CompositeCell_ToJsonString_71136F3F(this: CompositeCell, spaces: int | None=None) -> str:
    return ARCtrl_CompositeCell__CompositeCell_toJsonString_Static_71136F3F(spaces)(this)


__all__ = ["CompositeCell_encoder", "CompositeCell_decoder", "CompositeCell_encoderCompressed", "CompositeCell_decoderCompressed", "ARCtrl_CompositeCell__CompositeCell_fromJsonString_Static_Z721C83C5", "ARCtrl_CompositeCell__CompositeCell_toJsonString_Static_71136F3F", "ARCtrl_CompositeCell__CompositeCell_ToJsonString_71136F3F"]

