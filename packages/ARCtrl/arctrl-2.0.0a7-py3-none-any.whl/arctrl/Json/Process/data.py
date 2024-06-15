from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (choose, of_array, singleton, FSharpList)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (replace, to_text, printf)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import equals
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string
from ...Core.comment import Comment
from ...Core.data import Data
from ...Core.data_file import DataFile
from ...Core.uri import URIModule_toString
from ..comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from ..context.rocrate.isa_data_context import context_jsonvalue
from ..decode import (Decode_uri, Decode_resizeArray, Decode_objectNoAdditionalProperties)
from ..encode import (try_include, try_include_seq, default_spaces)
from ..string_table import (encode_string, decode_string)
from .data_file import (DataFile_ISAJson_encoder, DataFile_ISAJson_decoder, DataFile_ROCrate_encoder, DataFile_ROCrate_decoder)

def Data_encoder(d: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], d: Any=d) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1427(value: str, d: Any=d) -> Json:
        return Json(0, value)

    def _arrow1428(value_2: str, d: Any=d) -> Json:
        return Json(0, value_2)

    def _arrow1429(value_4: str, d: Any=d) -> Json:
        return Json(0, value_4)

    def _arrow1430(value_6: str, d: Any=d) -> Json:
        return Json(0, value_6)

    def _arrow1431(comment: Comment, d: Any=d) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("@id", _arrow1427, d.ID), try_include("name", _arrow1428, d.Name), try_include("dataType", DataFile_ISAJson_encoder, d.DataType), try_include("format", _arrow1429, d.Format), try_include("selectorFormat", _arrow1430, d.SelectorFormat), try_include_seq("comments", _arrow1431, d.Comments)])))


def _arrow1438(get: IGetters) -> Data:
    def _arrow1432(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1433(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1434(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("dataType", DataFile_ISAJson_decoder)

    def _arrow1435(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("format", string)

    def _arrow1436(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("selectorFormat", Decode_uri)

    def _arrow1437(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Data(_arrow1432(), _arrow1433(), _arrow1434(), _arrow1435(), _arrow1436(), _arrow1437())


Data_decoder: Decoder_1[Data] = object(_arrow1438)

def Data_compressedEncoder(string_table: Any, d: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, d: Any=d) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1440(s: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s)

    def _arrow1441(s_1: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s_1)

    def _arrow1442(s_2: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s_2)

    def _arrow1443(s_3: str, string_table: Any=string_table, d: Any=d) -> Json:
        return encode_string(string_table, s_3)

    def _arrow1444(comment: Comment, string_table: Any=string_table, d: Any=d) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("i", _arrow1440, d.ID), try_include("n", _arrow1441, d.Name), try_include("d", DataFile_ISAJson_encoder, d.DataType), try_include("f", _arrow1442, d.Format), try_include("s", _arrow1443, d.SelectorFormat), try_include_seq("c", _arrow1444, d.Comments)])))


def Data_compressedDecoder(string_table: Array[str]) -> Decoder_1[Data]:
    def _arrow1451(get: IGetters, string_table: Any=string_table) -> Data:
        def _arrow1445(__unit: None=None) -> str | None:
            arg_1: Decoder_1[str] = decode_string(string_table)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("i", arg_1)

        def _arrow1446(__unit: None=None) -> str | None:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("n", arg_3)

        def _arrow1447(__unit: None=None) -> DataFile | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("d", DataFile_ISAJson_decoder)

        def _arrow1448(__unit: None=None) -> str | None:
            arg_7: Decoder_1[str] = decode_string(string_table)
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("f", arg_7)

        def _arrow1449(__unit: None=None) -> str | None:
            arg_9: Decoder_1[str] = decode_string(string_table)
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("s", arg_9)

        def _arrow1450(__unit: None=None) -> Array[Comment] | None:
            arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("c", arg_11)

        return Data(_arrow1445(), _arrow1446(), _arrow1447(), _arrow1448(), _arrow1449(), _arrow1450())

    return object(_arrow1451)


def Data_ROCrate_genID(d: Data) -> str:
    match_value: str | None = d.ID
    if match_value is None:
        match_value_1: str | None = d.Name
        if match_value_1 is None:
            return "#EmptyData"

        else: 
            return replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def Data_ROCrate_encoder(oa: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1452(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1453(value_4: DataFile, oa: Any=oa) -> Json:
        return DataFile_ROCrate_encoder(value_4)

    def _arrow1454(value_5: str, oa: Any=oa) -> Json:
        return Json(0, value_5)

    def _arrow1455(value_7: str, oa: Any=oa) -> Json:
        return Json(0, value_7)

    def _arrow1456(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Data_ROCrate_genID(oa))), ("@type", list_1_1(singleton(Json(0, "Data")))), try_include("name", _arrow1452, oa.Name), try_include("type", _arrow1453, oa.DataType), try_include("encodingFormat", _arrow1454, oa.Format), try_include("usageInfo", _arrow1455, oa.SelectorFormat), try_include_seq("comments", _arrow1456, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1463(get: IGetters) -> Data:
    def _arrow1457(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1458(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1459(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("type", DataFile_ROCrate_decoder)

    def _arrow1460(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("encodingFormat", string)

    def _arrow1461(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("usageInfo", Decode_uri)

    def _arrow1462(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Data(_arrow1457(), _arrow1458(), _arrow1459(), _arrow1460(), _arrow1461(), _arrow1462())


Data_ROCrate_decoder: Decoder_1[Data] = object(_arrow1463)

def Data_ISAJson_encoder(oa: Data) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1465(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1466(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    return Json(5, choose(chooser, of_array([try_include("@id", _arrow1465, oa.ID), try_include("name", _arrow1466, oa.Name), try_include("type", DataFile_ISAJson_encoder, oa.DataType), try_include_seq("comments", Comment_ISAJson_encoder, oa.Comments)])))


Data_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "name", "type", "comments", "@type", "@context"])

def _arrow1471(get: IGetters) -> Data:
    def _arrow1467(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1468(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1469(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("type", DataFile_ISAJson_decoder)

    def _arrow1470(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ISAJson_decoder)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return Data(_arrow1467(), _arrow1468(), _arrow1469(), None, None, _arrow1470())


Data_ISAJson_decoder: Decoder_1[Data] = Decode_objectNoAdditionalProperties(Data_ISAJson_allowedFields, _arrow1471)

def ARCtrl_Data__Data_fromISAJsonString_Static_Z721C83C5(s: str) -> Data:
    match_value: FSharpResult_2[Data, str] = Decode_fromString(Data_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Data__Data_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Data], str]:
    def _arrow1472(f: Data, spaces: Any=spaces) -> str:
        value: Json = Data_ISAJson_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow1472


def ARCtrl_Data__Data_toISAJsonString_71136F3F(this: Data, spaces: int | None=None) -> str:
    return ARCtrl_Data__Data_toISAJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Data__Data_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Data:
    match_value: FSharpResult_2[Data, str] = Decode_fromString(Data_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Data__Data_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Data], str]:
    def _arrow1473(f: Data, spaces: Any=spaces) -> str:
        value: Json = Data_ROCrate_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow1473


def ARCtrl_Data__Data_toROCrateJsonString_71136F3F(this: Data, spaces: int | None=None) -> str:
    return ARCtrl_Data__Data_toROCrateJsonString_Static_71136F3F(spaces)(this)


__all__ = ["Data_encoder", "Data_decoder", "Data_compressedEncoder", "Data_compressedDecoder", "Data_ROCrate_genID", "Data_ROCrate_encoder", "Data_ROCrate_decoder", "Data_ISAJson_encoder", "Data_ISAJson_allowedFields", "Data_ISAJson_decoder", "ARCtrl_Data__Data_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Data__Data_toISAJsonString_Static_71136F3F", "ARCtrl_Data__Data_toISAJsonString_71136F3F", "ARCtrl_Data__Data_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Data__Data_toROCrateJsonString_Static_71136F3F", "ARCtrl_Data__Data_toROCrateJsonString_71136F3F"]

