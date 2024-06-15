from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (replace, to_text, printf)
from ...fable_modules.fable_library.util import equals
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, list_1 as list_1_2, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string
from ...Core.comment import Comment
from ...Core.Process.process import Process
from ...Core.Process.process_input import ProcessInput
from ...Core.Process.process_output import ProcessOutput
from ...Core.Process.process_parameter_value import ProcessParameterValue
from ...Core.Process.protocol import Protocol
from ...Core.uri import URIModule_toString
from ..comment import (Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from ..context.rocrate.isa_process_context import context_jsonvalue
from ..decode import Decode_uri
from ..encode import (try_include, try_include_list_opt, default_spaces)
from ..person import (Person_ROCrate_encodeAuthorListString, Person_ROCrate_decodeAuthorListString)
from .process_input import (ProcessInput_ROCrate_encoder, ProcessInput_ROCrate_decoder, ProcessInput_ISAJson_encoder, ProcessInput_ISAJson_decoder)
from .process_output import (ProcessOutput_ROCrate_encoder, ProcessOutput_ROCrate_decoder, ProcessOutput_ISAJson_encoder, ProcessOutput_ISAJson_decoder)
from .process_parameter_value import (ProcessParameterValue_ROCrate_encoder, ProcessParameterValue_ROCrate_decoder, ProcessParameterValue_ISAJson_encoder, ProcessParameterValue_ISAJson_decoder)
from .protocol import (Protocol_ROCrate_encoder, Protocol_ROCrate_decoder, Protocol_ISAJson_encoder, Protocol_ISAJson_decoder)

def Process_ROCrate_genID(p: Process) -> str:
    match_value: str | None = p.ID
    if match_value is None:
        match_value_1: str | None = p.Name
        if match_value_1 is None:
            return "#EmptyProcess"

        else: 
            return "#Process_" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def Process_ROCrate_encoder(study_name: str | None, assay_name: str | None, oa: Process) -> Json:
    def chooser(tupled_arg: tuple[str, Json], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1533(value_2: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1534(oa_1: Protocol, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return Protocol_ROCrate_encoder(study_name, assay_name, oa.Name, oa_1)

    def _arrow1535(author_list: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return Person_ROCrate_encodeAuthorListString(author_list)

    def _arrow1536(value_4: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1537(value_6: ProcessInput, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return ProcessInput_ROCrate_encoder(value_6)

    def _arrow1538(value_7: ProcessOutput, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return ProcessOutput_ROCrate_encoder(value_7)

    def _arrow1539(comment: Comment, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Process_ROCrate_genID(oa))), ("@type", list_1_1(singleton(Json(0, "Process")))), try_include("name", _arrow1533, oa.Name), try_include("executesProtocol", _arrow1534, oa.ExecutesProtocol), try_include_list_opt("parameterValues", ProcessParameterValue_ROCrate_encoder, oa.ParameterValues), try_include("performer", _arrow1535, oa.Performer), try_include("date", _arrow1536, oa.Date), try_include_list_opt("inputs", _arrow1537, oa.Inputs), try_include_list_opt("outputs", _arrow1538, oa.Outputs), try_include_list_opt("comments", _arrow1539, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1549(get: IGetters) -> Process:
    def _arrow1540(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow1541(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow1542(__unit: None=None) -> Protocol | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("executesProtocol", Protocol_ROCrate_decoder)

    def _arrow1543(__unit: None=None) -> FSharpList[ProcessParameterValue] | None:
        arg_7: Decoder_1[FSharpList[ProcessParameterValue]] = list_1_2(ProcessParameterValue_ROCrate_decoder)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("parameterValues", arg_7)

    def _arrow1544(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("performer", Person_ROCrate_decodeAuthorListString)

    def _arrow1545(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("date", string)

    def _arrow1546(__unit: None=None) -> FSharpList[ProcessInput] | None:
        arg_13: Decoder_1[FSharpList[ProcessInput]] = list_1_2(ProcessInput_ROCrate_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("inputs", arg_13)

    def _arrow1547(__unit: None=None) -> FSharpList[ProcessOutput] | None:
        arg_15: Decoder_1[FSharpList[ProcessOutput]] = list_1_2(ProcessOutput_ROCrate_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("outputs", arg_15)

    def _arrow1548(__unit: None=None) -> FSharpList[Comment] | None:
        arg_17: Decoder_1[FSharpList[Comment]] = list_1_2(Comment_ROCrate_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("comments", arg_17)

    return Process(_arrow1540(), _arrow1541(), _arrow1542(), _arrow1543(), _arrow1544(), _arrow1545(), None, None, _arrow1546(), _arrow1547(), _arrow1548())


Process_ROCrate_decoder: Decoder_1[Process] = object(_arrow1549)

def Process_ISAJson_encoder(oa: Process) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1551(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1552(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1553(oa_1: Protocol, oa: Any=oa) -> Json:
        return Protocol_ISAJson_encoder(oa_1)

    def _arrow1554(oa_2: ProcessParameterValue, oa: Any=oa) -> Json:
        return ProcessParameterValue_ISAJson_encoder(oa_2)

    def _arrow1555(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1556(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1557(oa_3: Process, oa: Any=oa) -> Json:
        return Process_ISAJson_encoder(oa_3)

    def _arrow1558(oa_4: Process, oa: Any=oa) -> Json:
        return Process_ISAJson_encoder(oa_4)

    def _arrow1559(value_8: ProcessInput, oa: Any=oa) -> Json:
        return ProcessInput_ISAJson_encoder(value_8)

    def _arrow1560(value_9: ProcessOutput, oa: Any=oa) -> Json:
        return ProcessOutput_ISAJson_encoder(value_9)

    return Json(5, choose(chooser, of_array([try_include("@id", _arrow1551, oa.ID), try_include("name", _arrow1552, oa.Name), try_include("executesProtocol", _arrow1553, oa.ExecutesProtocol), try_include_list_opt("parameterValues", _arrow1554, oa.ParameterValues), try_include("performer", _arrow1555, oa.Performer), try_include("date", _arrow1556, oa.Date), try_include("previousProcess", _arrow1557, oa.PreviousProcess), try_include("nextProcess", _arrow1558, oa.NextProcess), try_include_list_opt("inputs", _arrow1559, oa.Inputs), try_include_list_opt("outputs", _arrow1560, oa.Outputs), try_include_list_opt("comments", Comment_ISAJson_encoder, oa.Comments)])))


def _arrow1573(__unit: None=None) -> Decoder_1[Process]:
    def decode(__unit: None=None) -> Decoder_1[Process]:
        def _arrow1572(get: IGetters) -> Process:
            def _arrow1561(__unit: None=None) -> str | None:
                object_arg: IOptionalGetter = get.Optional
                return object_arg.Field("@id", Decode_uri)

            def _arrow1562(__unit: None=None) -> str | None:
                object_arg_1: IOptionalGetter = get.Optional
                return object_arg_1.Field("name", string)

            def _arrow1563(__unit: None=None) -> Protocol | None:
                object_arg_2: IOptionalGetter = get.Optional
                return object_arg_2.Field("executesProtocol", Protocol_ISAJson_decoder)

            def _arrow1564(__unit: None=None) -> FSharpList[ProcessParameterValue] | None:
                arg_7: Decoder_1[FSharpList[ProcessParameterValue]] = list_1_2(ProcessParameterValue_ISAJson_decoder)
                object_arg_3: IOptionalGetter = get.Optional
                return object_arg_3.Field("parameterValues", arg_7)

            def _arrow1565(__unit: None=None) -> str | None:
                object_arg_4: IOptionalGetter = get.Optional
                return object_arg_4.Field("performer", string)

            def _arrow1566(__unit: None=None) -> str | None:
                object_arg_5: IOptionalGetter = get.Optional
                return object_arg_5.Field("date", string)

            def _arrow1567(__unit: None=None) -> Process | None:
                arg_13: Decoder_1[Process] = decode(None)
                object_arg_6: IOptionalGetter = get.Optional
                return object_arg_6.Field("previousProcess", arg_13)

            def _arrow1568(__unit: None=None) -> Process | None:
                arg_15: Decoder_1[Process] = decode(None)
                object_arg_7: IOptionalGetter = get.Optional
                return object_arg_7.Field("nextProcess", arg_15)

            def _arrow1569(__unit: None=None) -> FSharpList[ProcessInput] | None:
                arg_17: Decoder_1[FSharpList[ProcessInput]] = list_1_2(ProcessInput_ISAJson_decoder)
                object_arg_8: IOptionalGetter = get.Optional
                return object_arg_8.Field("inputs", arg_17)

            def _arrow1570(__unit: None=None) -> FSharpList[ProcessOutput] | None:
                arg_19: Decoder_1[FSharpList[ProcessOutput]] = list_1_2(ProcessOutput_ISAJson_decoder)
                object_arg_9: IOptionalGetter = get.Optional
                return object_arg_9.Field("outputs", arg_19)

            def _arrow1571(__unit: None=None) -> FSharpList[Comment] | None:
                arg_21: Decoder_1[FSharpList[Comment]] = list_1_2(Comment_ISAJson_decoder)
                object_arg_10: IOptionalGetter = get.Optional
                return object_arg_10.Field("comments", arg_21)

            return Process(_arrow1561(), _arrow1562(), _arrow1563(), _arrow1564(), _arrow1565(), _arrow1566(), _arrow1567(), _arrow1568(), _arrow1569(), _arrow1570(), _arrow1571())

        return object(_arrow1572)

    return decode(None)


Process_ISAJson_decoder: Decoder_1[Process] = _arrow1573()

def ARCtrl_Process_Process__Process_fromISAJsonString_Static_Z721C83C5(s: str) -> Process:
    match_value: FSharpResult_2[Process, str] = Decode_fromString(Process_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Process__Process_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Process], str]:
    def _arrow1574(f: Process, spaces: Any=spaces) -> str:
        value: Json = Process_ISAJson_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow1574


def ARCtrl_Process_Process__Process_ToISAJsonString_71136F3F(this: Process, spaces: int | None=None) -> str:
    return ARCtrl_Process_Process__Process_toISAJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Process_Process__Process_fromROCrateString_Static_Z721C83C5(s: str) -> Process:
    match_value: FSharpResult_2[Process, str] = Decode_fromString(Process_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Process__Process_toROCrateString_Static_39E0BC3F(study_name: str | None=None, assay_name: str | None=None, spaces: int | None=None) -> Callable[[Process], str]:
    def _arrow1577(f: Process, study_name: Any=study_name, assay_name: Any=assay_name, spaces: Any=spaces) -> str:
        value: Json = Process_ROCrate_encoder(study_name, assay_name, f)
        return to_string(default_spaces(spaces), value)

    return _arrow1577


def ARCtrl_Process_Process__Process_ToROCrateString_39E0BC3F(this: Process, study_name: str | None=None, assay_name: str | None=None, spaces: int | None=None) -> str:
    return ARCtrl_Process_Process__Process_toROCrateString_Static_39E0BC3F(study_name, assay_name, spaces)(this)


__all__ = ["Process_ROCrate_genID", "Process_ROCrate_encoder", "Process_ROCrate_decoder", "Process_ISAJson_encoder", "Process_ISAJson_decoder", "ARCtrl_Process_Process__Process_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_Process__Process_toISAJsonString_Static_71136F3F", "ARCtrl_Process_Process__Process_ToISAJsonString_71136F3F", "ARCtrl_Process_Process__Process_fromROCrateString_Static_Z721C83C5", "ARCtrl_Process_Process__Process_toROCrateString_Static_39E0BC3F", "ARCtrl_Process_Process__Process_ToROCrateString_39E0BC3F"]

