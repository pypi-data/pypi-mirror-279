from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (of_array, choose)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf)
from ..fable_modules.fable_library.types import (to_string, Array)
from ..fable_modules.fable_library.util import (int32_to_string, equals)
from ..fable_modules.thoth_json_core.decode import (one_of, map, int_1, float_1, string, object, IOptionalGetter, IGetters)
from ..fable_modules.thoth_json_core.types import (Decoder_1, Json)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string as to_string_1
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.uri import URIModule_toString
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoderDisambiguatingDescription, Comment_ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_ontology_annotation_context import context_jsonvalue
from .context.rocrate.property_value_context import context_jsonvalue as context_jsonvalue_1
from .decode import Decode_resizeArray
from .encode import (try_include, try_include_seq, default_spaces)
from .string_table import (encode_string, decode_string)

AnnotationValue_decoder: Decoder_1[str] = one_of(of_array([map(int32_to_string, int_1), map(to_string, float_1), string]))

def OntologyAnnotation_encoder(oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1112(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1113(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1114(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1115(comment: Comment, oa: Any=oa) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("annotationValue", _arrow1112, oa.Name), try_include("termSource", _arrow1113, oa.TermSourceREF), try_include("termAccession", _arrow1114, oa.TermAccessionNumber), try_include_seq("comments", _arrow1115, oa.Comments)])))


def _arrow1120(get: IGetters) -> OntologyAnnotation:
    def _arrow1116(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("annotationValue", AnnotationValue_decoder)

    def _arrow1117(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("termSource", string)

    def _arrow1118(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("termAccession", string)

    def _arrow1119(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return OntologyAnnotation.create(_arrow1116(), _arrow1117(), _arrow1118(), _arrow1119())


OntologyAnnotation_decoder: Decoder_1[OntologyAnnotation] = object(_arrow1120)

def OntologyAnnotation_compressedEncoder(string_table: Any, oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1122(s: str, string_table: Any=string_table, oa: Any=oa) -> Json:
        return encode_string(string_table, s)

    def _arrow1123(s_1: str, string_table: Any=string_table, oa: Any=oa) -> Json:
        return encode_string(string_table, s_1)

    def _arrow1124(s_2: str, string_table: Any=string_table, oa: Any=oa) -> Json:
        return encode_string(string_table, s_2)

    def _arrow1125(comment: Comment, string_table: Any=string_table, oa: Any=oa) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("a", _arrow1122, oa.Name), try_include("ts", _arrow1123, oa.TermSourceREF), try_include("ta", _arrow1124, oa.TermAccessionNumber), try_include_seq("comments", _arrow1125, oa.Comments)])))


def OntologyAnnotation_compressedDecoder(string_table: Array[str]) -> Decoder_1[OntologyAnnotation]:
    def _arrow1130(get: IGetters, string_table: Any=string_table) -> OntologyAnnotation:
        def _arrow1126(__unit: None=None) -> str | None:
            arg_1: Decoder_1[str] = decode_string(string_table)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("a", arg_1)

        def _arrow1127(__unit: None=None) -> str | None:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("ts", arg_3)

        def _arrow1128(__unit: None=None) -> str | None:
            arg_5: Decoder_1[str] = decode_string(string_table)
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("ta", arg_5)

        def _arrow1129(__unit: None=None) -> Array[Comment] | None:
            arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("comments", arg_7)

        return OntologyAnnotation(_arrow1126(), _arrow1127(), _arrow1128(), _arrow1129())

    return object(_arrow1130)


def OntologyAnnotation_ROCrate_genID(o: OntologyAnnotation) -> str:
    match_value: str | None = o.TermAccessionNumber
    if match_value is None:
        match_value_1: str | None = o.TermSourceREF
        if match_value_1 is None:
            match_value_2: str | None = o.Name
            if match_value_2 is None:
                return "#DummyOntologyAnnotation"

            else: 
                return "#UserTerm_" + replace(match_value_2, " ", "_")


        else: 
            return "#" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def OntologyAnnotation_ROCrate_encoderDefinedTerm(oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1131(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1132(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1133(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1134(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, OntologyAnnotation_ROCrate_genID(oa))), ("@type", Json(0, "OntologyAnnotation")), try_include("annotationValue", _arrow1131, oa.Name), try_include("termSource", _arrow1132, oa.TermSourceREF), try_include("termAccession", _arrow1133, oa.TermAccessionNumber), try_include_seq("comments", _arrow1134, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1139(get: IGetters) -> OntologyAnnotation:
    def _arrow1135(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("annotationValue", AnnotationValue_decoder)

    def _arrow1136(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("termSource", string)

    def _arrow1137(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("termAccession", string)

    def _arrow1138(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return OntologyAnnotation.create(_arrow1135(), _arrow1136(), _arrow1137(), _arrow1138())


OntologyAnnotation_ROCrate_decoderDefinedTerm: Decoder_1[OntologyAnnotation] = object(_arrow1139)

def OntologyAnnotation_ROCrate_encoderPropertyValue(oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1140(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1141(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1142(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, OntologyAnnotation_ROCrate_genID(oa))), ("@type", Json(0, "PropertyValue")), try_include("category", _arrow1140, oa.Name), try_include("categoryCode", _arrow1141, oa.TermAccessionNumber), try_include_seq("comments", _arrow1142, oa.Comments), ("@context", context_jsonvalue_1)])))


def _arrow1146(get: IGetters) -> OntologyAnnotation:
    def _arrow1143(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("category", string)

    def _arrow1144(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("categoryCode", string)

    def _arrow1145(__unit: None=None) -> Array[Comment] | None:
        arg_5: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("comments", arg_5)

    return OntologyAnnotation.create(_arrow1143(), None, _arrow1144(), _arrow1145())


OntologyAnnotation_ROCrate_decoderPropertyValue: Decoder_1[OntologyAnnotation] = object(_arrow1146)

OntologyAnnotation_ISAJson_encoder: Callable[[OntologyAnnotation], Json] = OntologyAnnotation_encoder

OntologyAnnotation_ISAJson_decoder: Decoder_1[OntologyAnnotation] = OntologyAnnotation_decoder

def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow1147(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: Json = OntologyAnnotation_encoder(obj)
        return to_string_1(default_spaces(spaces), value)

    return _arrow1147


def ARCtrl_OntologyAnnotation__OntologyAnnotation_ToJsonString_71136F3F(this: OntologyAnnotation, spaces: int | None=None) -> str:
    return ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_ROCrate_decoderDefinedTerm, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow1148(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: Json = OntologyAnnotation_ROCrate_encoderDefinedTerm(obj)
        return to_string_1(default_spaces(spaces), value)

    return _arrow1148


def ARCtrl_OntologyAnnotation__OntologyAnnotation_ToROCrateJsonString_71136F3F(this: OntologyAnnotation, spaces: int | None=None) -> str:
    return ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow1149(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: Json = OntologyAnnotation_ISAJson_encoder(obj)
        return to_string_1(default_spaces(spaces), value)

    return _arrow1149


def ARCtrl_OntologyAnnotation__OntologyAnnotation_ToISAJsonString_71136F3F(this: OntologyAnnotation, spaces: int | None=None) -> str:
    return ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["AnnotationValue_decoder", "OntologyAnnotation_encoder", "OntologyAnnotation_decoder", "OntologyAnnotation_compressedEncoder", "OntologyAnnotation_compressedDecoder", "OntologyAnnotation_ROCrate_genID", "OntologyAnnotation_ROCrate_encoderDefinedTerm", "OntologyAnnotation_ROCrate_decoderDefinedTerm", "OntologyAnnotation_ROCrate_encoderPropertyValue", "OntologyAnnotation_ROCrate_decoderPropertyValue", "OntologyAnnotation_ISAJson_encoder", "OntologyAnnotation_ISAJson_decoder", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_ToJsonString_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_ToROCrateJsonString_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_ToISAJsonString_71136F3F"]

