from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.util import equals
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ...fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.iproperty_value import IPropertyValue_1
from ...Core.Process.value import Value
from ..context.rocrate.property_value_context import context_jsonvalue
from ..encode import try_include
from ..ontology_annotation import AnnotationValue_decoder

_T = TypeVar("_T")

def gen_id(p: IPropertyValue_1[Any]) -> str:
    match_value: OntologyAnnotation | None = p.GetCategory()
    if match_value is None:
        return ("#Empty" + p.GetAdditionalType()) + ""

    else: 
        t: OntologyAnnotation = match_value
        return ((((((("" + p.GetAdditionalType()) + "/") + str(t)) + "") + str(p.GetValue())) + "") + str(p.GetUnit())) + ""



def encoder(pv: IPropertyValue_1[Any]) -> Json:
    pattern_input: tuple[str | None, str | None]
    match_value: OntologyAnnotation | None = pv.GetCategory()
    if match_value is None:
        pattern_input = (None, None)

    else: 
        oa: OntologyAnnotation = match_value
        pattern_input = (oa.Name, oa.TermAccessionNumber)

    pattern_input_1: tuple[Json | None, Json | None]
    match_value_1: Value | None = pv.GetValue()
    if match_value_1 is None:
        pattern_input_1 = (None, None)

    else: 
        v: Value = match_value_1
        if v.tag == 1:
            pattern_input_1 = (Json(7, int(v.fields[0]+0x100000000 if v.fields[0] < 0 else v.fields[0])), None)

        elif v.tag == 2:
            pattern_input_1 = (Json(2, v.fields[0]), None)

        elif v.tag == 0:
            oa_1: OntologyAnnotation = v.fields[0]
            def _arrow1301(value_3: str, pv: Any=pv) -> Json:
                return Json(0, value_3)

            def _arrow1302(value_5: str, pv: Any=pv) -> Json:
                return Json(0, value_5)

            pattern_input_1 = (map(_arrow1301, oa_1.Name), map(_arrow1302, oa_1.TermAccessionNumber))

        else: 
            pattern_input_1 = (Json(0, v.fields[0]), None)


    pattern_input_2: tuple[str | None, str | None]
    match_value_2: OntologyAnnotation | None = pv.GetUnit()
    if match_value_2 is None:
        pattern_input_2 = (None, None)

    else: 
        oa_2: OntologyAnnotation = match_value_2
        pattern_input_2 = (oa_2.Name, oa_2.TermAccessionNumber)

    def chooser(tupled_arg: tuple[str, Json], pv: Any=pv) -> tuple[str, Json] | None:
        v_1: Json = tupled_arg[1]
        if equals(v_1, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v_1)


    def _arrow1303(value_11: str, pv: Any=pv) -> Json:
        return Json(0, value_11)

    def _arrow1304(value_13: str, pv: Any=pv) -> Json:
        return Json(0, value_13)

    def _arrow1305(x: Json, pv: Any=pv) -> Json:
        return x

    def _arrow1306(x_1: Json, pv: Any=pv) -> Json:
        return x_1

    def _arrow1307(value_15: str, pv: Any=pv) -> Json:
        return Json(0, value_15)

    def _arrow1308(value_17: str, pv: Any=pv) -> Json:
        return Json(0, value_17)

    return Json(5, choose(chooser, of_array([("@id", Json(0, gen_id(pv))), ("@type", Json(0, "PropertyValue")), ("additionalType", Json(0, pv.GetAdditionalType())), try_include("category", _arrow1303, pattern_input[0]), try_include("categoryCode", _arrow1304, pattern_input[1]), try_include("value", _arrow1305, pattern_input_1[0]), try_include("valueCode", _arrow1306, pattern_input_1[1]), try_include("unit", _arrow1307, pattern_input_2[0]), try_include("unitCode", _arrow1308, pattern_input_2[1]), ("@context", context_jsonvalue)])))


def decoder(create: Callable[[OntologyAnnotation | None, Value | None, OntologyAnnotation | None], _T]) -> Decoder_1[_T]:
    def _arrow1311(get: IGetters, create: Any=create) -> _T:
        category: OntologyAnnotation | None
        name: str | None
        object_arg: IOptionalGetter = get.Optional
        name = object_arg.Field("category", string)
        code: str | None
        object_arg_1: IOptionalGetter = get.Optional
        code = object_arg_1.Field("categoryCode", string)
        (pattern_matching_result, code_1) = (None, None)
        if name is None:
            if code is not None:
                if code == "":
                    pattern_matching_result = 0

                else: 
                    pattern_matching_result = 2
                    code_1 = code


            else: 
                pattern_matching_result = 0


        elif code is not None:
            if code == "":
                pattern_matching_result = 1

            else: 
                pattern_matching_result = 2
                code_1 = code


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            category = None

        elif pattern_matching_result == 1:
            try: 
                category = OntologyAnnotation.create(name)

            except Exception as err:
                raise Exception(((("Error while decoding category (name:" + str(name)) + "): ") + str(err)) + "")


        elif pattern_matching_result == 2:
            try: 
                category = OntologyAnnotation.from_term_annotation(code_1, name)

            except Exception as err_1:
                raise Exception(((((("Error while decoding category (name:" + str(name)) + ", code:") + code_1) + "): ") + str(err_1)) + "")


        unit: OntologyAnnotation | None
        name_1: str | None
        object_arg_2: IOptionalGetter = get.Optional
        name_1 = object_arg_2.Field("unit", string)
        code_2: str | None
        object_arg_3: IOptionalGetter = get.Optional
        code_2 = object_arg_3.Field("unitCode", string)
        (pattern_matching_result_1, code_3) = (None, None)
        if name_1 is None:
            if code_2 is not None:
                if code_2 == "":
                    pattern_matching_result_1 = 0

                else: 
                    pattern_matching_result_1 = 2
                    code_3 = code_2


            else: 
                pattern_matching_result_1 = 0


        elif code_2 is not None:
            if code_2 == "":
                pattern_matching_result_1 = 1

            else: 
                pattern_matching_result_1 = 2
                code_3 = code_2


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            unit = None

        elif pattern_matching_result_1 == 1:
            try: 
                unit = OntologyAnnotation.create(name_1)

            except Exception as err_2:
                raise Exception(((("Error while decoding unit (name:" + str(name_1)) + "): ") + str(err_2)) + "")


        elif pattern_matching_result_1 == 2:
            try: 
                unit = OntologyAnnotation.from_term_annotation(code_3, name_1)

            except Exception as err_3:
                raise Exception(((((("Error while decoding unit (name:" + str(name_1)) + ", code:") + code_3) + "): ") + str(err_3)) + "")


        def _arrow1309(__unit: None=None) -> Value | None:
            value: str | None
            object_arg_4: IOptionalGetter = get.Optional
            value = object_arg_4.Field("value", AnnotationValue_decoder)
            code_4: str | None
            object_arg_5: IOptionalGetter = get.Optional
            code_4 = object_arg_5.Field("valueCode", string)
            if (code_4 is None) if (value is None) else False:
                return None

            else: 
                try: 
                    return Value.from_options(value, None, code_4)

                except Exception as err_4:
                    raise Exception(((((("Error while decoding value " + str(value)) + ",") + str(code_4)) + ": ") + str(err_4)) + "")



        return create(category, _arrow1309(), unit)

    return object(_arrow1311)


__all__ = ["gen_id", "encoder", "decoder"]

