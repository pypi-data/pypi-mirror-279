from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (map, FSharpList, is_empty, head, tail, try_find_index, of_array, singleton)
from ...fable_modules.fable_library.option import map as map_1
from ...fable_modules.fable_library.seq import (to_list, delay, append, singleton as singleton_1, empty)
from ...fable_modules.fable_library.string_ import (to_fail, printf)
from ...fable_modules.fable_library.types import to_string
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...Core.Helper.regex import (ActivePatterns__007CUnitColumnHeader_007C__007C, ActivePatterns__007CTANColumnHeader_007C__007C, ActivePatterns__007CTSRColumnHeader_007C__007C, try_parse_parameter_column_header, try_parse_factor_column_header, try_parse_characteristic_column_header, try_parse_component_column_header, ActivePatterns__007CInputColumnHeader_007C__007C, ActivePatterns__007COutputColumnHeader_007C__007C, ActivePatterns__007CComment_007C__007C)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_header import (CompositeHeader, IOType)
from .composite_cell import (term_from_fs_cells, unitized_from_fs_cells, data_from_fs_cells, free_text_from_fs_cells)

def ActivePattern_mergeIDInfo(id_space1: str, local_id1: str, id_space2: str, local_id2: str) -> dict[str, Any]:
    if id_space1 != id_space2:
        to_fail(printf("TermSourceRef %s and %s do not match"))(id_space1)(id_space2)

    if local_id1 != local_id2:
        to_fail(printf("LocalID %s and %s do not match"))(local_id1)(local_id2)

    return {
        "TermAccessionNumber": ((("" + id_space1) + ":") + local_id1) + "",
        "TermSourceRef": id_space1
    }


def ActivePattern__007CTerm_007C__007C(category_parser: Callable[[str], str | None], f: Callable[[OntologyAnnotation], CompositeHeader], cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def _007CAC_007C__007C(s: str, category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> str | None:
        return category_parser(s)

    def mapping(c: FsCell, category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, name) = (None, None)
    if not is_empty(cell_values):
        active_pattern_result: str | None = _007CAC_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0
                name = active_pattern_result

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow907(cells_1: FSharpList[FsCell], category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> CompositeCell:
            return term_from_fs_cells(None, None, cells_1)

        return (f(OntologyAnnotation.create(name)), _arrow907)

    elif pattern_matching_result == 1:
        (pattern_matching_result_1, name_1, term1, term2) = (None, None, None, None)
        if not is_empty(cell_values):
            active_pattern_result_1: str | None = _007CAC_007C__007C(head(cell_values))
            if active_pattern_result_1 is not None:
                if not is_empty(tail(cell_values)):
                    active_pattern_result_2: dict[str, Any] | None = ActivePatterns__007CTSRColumnHeader_007C__007C(head(tail(cell_values)))
                    if active_pattern_result_2 is not None:
                        if not is_empty(tail(tail(cell_values))):
                            active_pattern_result_3: dict[str, Any] | None = ActivePatterns__007CTANColumnHeader_007C__007C(head(tail(tail(cell_values))))
                            if active_pattern_result_3 is not None:
                                if is_empty(tail(tail(tail(cell_values)))):
                                    pattern_matching_result_1 = 0
                                    name_1 = active_pattern_result_1
                                    term1 = active_pattern_result_2
                                    term2 = active_pattern_result_3

                                else: 
                                    pattern_matching_result_1 = 1


                            else: 
                                pattern_matching_result_1 = 1


                        else: 
                            pattern_matching_result_1 = 1


                    else: 
                        pattern_matching_result_1 = 1


                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            term: dict[str, Any] = ActivePattern_mergeIDInfo(term1["IDSpace"], term1["LocalID"], term2["IDSpace"], term2["LocalID"])
            def _arrow908(cells_2: FSharpList[FsCell], category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> CompositeCell:
                return term_from_fs_cells(1, 2, cells_2)

            return (f(OntologyAnnotation.create(name_1, term["TermSourceRef"], term["TermAccessionNumber"])), _arrow908)

        elif pattern_matching_result_1 == 1:
            (pattern_matching_result_2, name_2, term1_1, term2_1) = (None, None, None, None)
            if not is_empty(cell_values):
                active_pattern_result_4: str | None = _007CAC_007C__007C(head(cell_values))
                if active_pattern_result_4 is not None:
                    if not is_empty(tail(cell_values)):
                        active_pattern_result_5: dict[str, Any] | None = ActivePatterns__007CTANColumnHeader_007C__007C(head(tail(cell_values)))
                        if active_pattern_result_5 is not None:
                            if not is_empty(tail(tail(cell_values))):
                                active_pattern_result_6: dict[str, Any] | None = ActivePatterns__007CTSRColumnHeader_007C__007C(head(tail(tail(cell_values))))
                                if active_pattern_result_6 is not None:
                                    if is_empty(tail(tail(tail(cell_values)))):
                                        pattern_matching_result_2 = 0
                                        name_2 = active_pattern_result_4
                                        term1_1 = active_pattern_result_6
                                        term2_1 = active_pattern_result_5

                                    else: 
                                        pattern_matching_result_2 = 1


                                else: 
                                    pattern_matching_result_2 = 1


                            else: 
                                pattern_matching_result_2 = 1


                        else: 
                            pattern_matching_result_2 = 1


                    else: 
                        pattern_matching_result_2 = 1


                else: 
                    pattern_matching_result_2 = 1


            else: 
                pattern_matching_result_2 = 1

            if pattern_matching_result_2 == 0:
                term_1: dict[str, Any] = ActivePattern_mergeIDInfo(term1_1["IDSpace"], term1_1["LocalID"], term2_1["IDSpace"], term2_1["LocalID"])
                def _arrow909(cells_3: FSharpList[FsCell], category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> CompositeCell:
                    return term_from_fs_cells(2, 1, cells_3)

                return (f(OntologyAnnotation.create(name_2, term_1["TermSourceRef"], term_1["TermAccessionNumber"])), _arrow909)

            elif pattern_matching_result_2 == 1:
                (pattern_matching_result_3, name_3, term1_2, term2_2) = (None, None, None, None)
                if not is_empty(cell_values):
                    active_pattern_result_7: str | None = _007CAC_007C__007C(head(cell_values))
                    if active_pattern_result_7 is not None:
                        if not is_empty(tail(cell_values)):
                            if ActivePatterns__007CUnitColumnHeader_007C__007C(head(tail(cell_values))) is not None:
                                if not is_empty(tail(tail(cell_values))):
                                    active_pattern_result_9: dict[str, Any] | None = ActivePatterns__007CTSRColumnHeader_007C__007C(head(tail(tail(cell_values))))
                                    if active_pattern_result_9 is not None:
                                        if not is_empty(tail(tail(tail(cell_values)))):
                                            active_pattern_result_10: dict[str, Any] | None = ActivePatterns__007CTANColumnHeader_007C__007C(head(tail(tail(tail(cell_values)))))
                                            if active_pattern_result_10 is not None:
                                                if is_empty(tail(tail(tail(tail(cell_values))))):
                                                    pattern_matching_result_3 = 0
                                                    name_3 = active_pattern_result_7
                                                    term1_2 = active_pattern_result_9
                                                    term2_2 = active_pattern_result_10

                                                else: 
                                                    pattern_matching_result_3 = 1


                                            else: 
                                                pattern_matching_result_3 = 1


                                        else: 
                                            pattern_matching_result_3 = 1


                                    else: 
                                        pattern_matching_result_3 = 1


                                else: 
                                    pattern_matching_result_3 = 1


                            else: 
                                pattern_matching_result_3 = 1


                        else: 
                            pattern_matching_result_3 = 1


                    else: 
                        pattern_matching_result_3 = 1


                else: 
                    pattern_matching_result_3 = 1

                if pattern_matching_result_3 == 0:
                    term_2: dict[str, Any] = ActivePattern_mergeIDInfo(term1_2["IDSpace"], term1_2["LocalID"], term2_2["IDSpace"], term2_2["LocalID"])
                    def _arrow910(cells_4: FSharpList[FsCell], category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> CompositeCell:
                        return unitized_from_fs_cells(1, 2, 3, cells_4)

                    return (f(OntologyAnnotation.create(name_3, term_2["TermSourceRef"], term_2["TermAccessionNumber"])), _arrow910)

                elif pattern_matching_result_3 == 1:
                    (pattern_matching_result_4, name_4, term1_3, term2_3) = (None, None, None, None)
                    if not is_empty(cell_values):
                        active_pattern_result_11: str | None = _007CAC_007C__007C(head(cell_values))
                        if active_pattern_result_11 is not None:
                            if not is_empty(tail(cell_values)):
                                if ActivePatterns__007CUnitColumnHeader_007C__007C(head(tail(cell_values))) is not None:
                                    if not is_empty(tail(tail(cell_values))):
                                        active_pattern_result_13: dict[str, Any] | None = ActivePatterns__007CTANColumnHeader_007C__007C(head(tail(tail(cell_values))))
                                        if active_pattern_result_13 is not None:
                                            if not is_empty(tail(tail(tail(cell_values)))):
                                                active_pattern_result_14: dict[str, Any] | None = ActivePatterns__007CTSRColumnHeader_007C__007C(head(tail(tail(tail(cell_values)))))
                                                if active_pattern_result_14 is not None:
                                                    if is_empty(tail(tail(tail(tail(cell_values))))):
                                                        pattern_matching_result_4 = 0
                                                        name_4 = active_pattern_result_11
                                                        term1_3 = active_pattern_result_14
                                                        term2_3 = active_pattern_result_13

                                                    else: 
                                                        pattern_matching_result_4 = 1


                                                else: 
                                                    pattern_matching_result_4 = 1


                                            else: 
                                                pattern_matching_result_4 = 1


                                        else: 
                                            pattern_matching_result_4 = 1


                                    else: 
                                        pattern_matching_result_4 = 1


                                else: 
                                    pattern_matching_result_4 = 1


                            else: 
                                pattern_matching_result_4 = 1


                        else: 
                            pattern_matching_result_4 = 1


                    else: 
                        pattern_matching_result_4 = 1

                    if pattern_matching_result_4 == 0:
                        term_3: dict[str, Any] = ActivePattern_mergeIDInfo(term1_3["IDSpace"], term1_3["LocalID"], term2_3["IDSpace"], term2_3["LocalID"])
                        def _arrow911(cells_5: FSharpList[FsCell], category_parser: Any=category_parser, f: Any=f, cells: Any=cells) -> CompositeCell:
                            return unitized_from_fs_cells(1, 3, 2, cells_5)

                        return (f(OntologyAnnotation.create(name_4, term_3["TermSourceRef"], term_3["TermAccessionNumber"])), _arrow911)

                    elif pattern_matching_result_4 == 1:
                        return None







def ActivePattern__007CParameter_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def _arrow912(input: str, cells: Any=cells) -> str | None:
        return try_parse_parameter_column_header(input)

    def _arrow913(Item: OntologyAnnotation, cells: Any=cells) -> CompositeHeader:
        return CompositeHeader(3, Item)

    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C(_arrow912, _arrow913, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CFactor_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def _arrow914(input: str, cells: Any=cells) -> str | None:
        return try_parse_factor_column_header(input)

    def _arrow915(Item: OntologyAnnotation, cells: Any=cells) -> CompositeHeader:
        return CompositeHeader(2, Item)

    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C(_arrow914, _arrow915, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CCharacteristic_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def _arrow916(input: str, cells: Any=cells) -> str | None:
        return try_parse_characteristic_column_header(input)

    def _arrow917(Item: OntologyAnnotation, cells: Any=cells) -> CompositeHeader:
        return CompositeHeader(1, Item)

    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C(_arrow916, _arrow917, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CComponent_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def _arrow918(input: str, cells: Any=cells) -> str | None:
        return try_parse_component_column_header(input)

    def _arrow919(Item: OntologyAnnotation, cells: Any=cells) -> CompositeHeader:
        return CompositeHeader(0, Item)

    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C(_arrow918, _arrow919, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CInput_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, cols, io_type) = (None, None, None)
    if not is_empty(cell_values):
        active_pattern_result: str | None = ActivePatterns__007CInputColumnHeader_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            pattern_matching_result = 0
            cols = tail(cell_values)
            io_type = active_pattern_result

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        match_value: IOType = IOType.of_string(io_type)
        if match_value.tag == 2:
            def mapping_1(y: int, cells: Any=cells) -> int:
                return 1 + y

            def predicate(s: str, cells: Any=cells) -> bool:
                return s.find("Data Format") == 0

            format: int | None = map_1(mapping_1, try_find_index(predicate, cols))
            def mapping_2(y_1: int, cells: Any=cells) -> int:
                return 1 + y_1

            def predicate_1(s_1: str, cells: Any=cells) -> bool:
                return s_1.find("Data Selector Format") == 0

            selector_format: int | None = map_1(mapping_2, try_find_index(predicate_1, cols))
            def _arrow920(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
                return data_from_fs_cells(format, selector_format, cells_1)

            return (CompositeHeader(11, IOType(2)), _arrow920)

        else: 
            def _arrow921(cells_2: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
                return free_text_from_fs_cells(cells_2)

            return (CompositeHeader(11, match_value), _arrow921)


    elif pattern_matching_result == 1:
        return None



def ActivePattern__007COutput_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, cols, io_type) = (None, None, None)
    if not is_empty(cell_values):
        active_pattern_result: str | None = ActivePatterns__007COutputColumnHeader_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            pattern_matching_result = 0
            cols = tail(cell_values)
            io_type = active_pattern_result

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        match_value: IOType = IOType.of_string(io_type)
        if match_value.tag == 2:
            def mapping_1(y: int, cells: Any=cells) -> int:
                return 1 + y

            def predicate(s: str, cells: Any=cells) -> bool:
                return s.find("Data Format") == 0

            format: int | None = map_1(mapping_1, try_find_index(predicate, cols))
            def mapping_2(y_1: int, cells: Any=cells) -> int:
                return 1 + y_1

            def predicate_1(s_1: str, cells: Any=cells) -> bool:
                return s_1.find("Data Selector Format") == 0

            selector_format: int | None = map_1(mapping_2, try_find_index(predicate_1, cols))
            def _arrow922(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
                return data_from_fs_cells(format, selector_format, cells_1)

            return (CompositeHeader(12, IOType(2)), _arrow922)

        else: 
            def _arrow923(cells_2: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
                return free_text_from_fs_cells(cells_2)

            return (CompositeHeader(12, match_value), _arrow923)


    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CComment_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, key) = (None, None)
    if not is_empty(cell_values):
        active_pattern_result: str | None = ActivePatterns__007CComment_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0
                key = active_pattern_result

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow924(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_1)

        return (CompositeHeader(14, key), _arrow924)

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CProtocolType_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def parser(s: str, cells: Any=cells) -> str | None:
        if s == "Protocol Type":
            return s

        else: 
            return None


    def header(_arg: OntologyAnnotation, cells: Any=cells) -> CompositeHeader:
        return CompositeHeader(4)

    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C(parser, header, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CProtocolHeader_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        if head(cell_values) == "Protocol REF":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 6


        elif head(cell_values) == "Protocol Description":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 1

            else: 
                pattern_matching_result = 6


        elif head(cell_values) == "Protocol Uri":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 2

            else: 
                pattern_matching_result = 6


        elif head(cell_values) == "Protocol Version":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 3

            else: 
                pattern_matching_result = 6


        elif head(cell_values) == "Performer":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 4

            else: 
                pattern_matching_result = 6


        elif head(cell_values) == "Date":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 5

            else: 
                pattern_matching_result = 6


        else: 
            pattern_matching_result = 6


    else: 
        pattern_matching_result = 6

    if pattern_matching_result == 0:
        def _arrow925(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_1)

        return (CompositeHeader(8), _arrow925)

    elif pattern_matching_result == 1:
        def _arrow926(cells_2: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_2)

        return (CompositeHeader(5), _arrow926)

    elif pattern_matching_result == 2:
        def _arrow927(cells_3: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_3)

        return (CompositeHeader(6), _arrow927)

    elif pattern_matching_result == 3:
        def _arrow928(cells_4: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_4)

        return (CompositeHeader(7), _arrow928)

    elif pattern_matching_result == 4:
        def _arrow929(cells_5: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_5)

        return (CompositeHeader(9), _arrow929)

    elif pattern_matching_result == 5:
        def _arrow930(cells_6: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_6)

        return (CompositeHeader(10), _arrow930)

    elif pattern_matching_result == 6:
        return None



def ActivePattern__007CFreeText_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, text) = (None, None)
    if not is_empty(cell_values):
        if is_empty(tail(cell_values)):
            pattern_matching_result = 0
            text = head(cell_values)

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow931(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_1)

        return (CompositeHeader(13, text), _arrow931)

    elif pattern_matching_result == 1:
        return None



def from_fs_cells(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]]:
    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CParameter_007C__007C(cells)
    if active_pattern_result is not None:
        p: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return p

    else: 
        active_pattern_result_1: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CFactor_007C__007C(cells)
        if active_pattern_result_1 is not None:
            f: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_1
            return f

        else: 
            active_pattern_result_2: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CCharacteristic_007C__007C(cells)
            if active_pattern_result_2 is not None:
                c: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_2
                return c

            else: 
                active_pattern_result_3: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CComponent_007C__007C(cells)
                if active_pattern_result_3 is not None:
                    c_1: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_3
                    return c_1

                else: 
                    active_pattern_result_4: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CInput_007C__007C(cells)
                    if active_pattern_result_4 is not None:
                        i: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_4
                        return i

                    else: 
                        active_pattern_result_5: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007COutput_007C__007C(cells)
                        if active_pattern_result_5 is not None:
                            o: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_5
                            return o

                        else: 
                            active_pattern_result_6: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CProtocolType_007C__007C(cells)
                            if active_pattern_result_6 is not None:
                                pt: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_6
                                return pt

                            else: 
                                active_pattern_result_7: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CProtocolHeader_007C__007C(cells)
                                if active_pattern_result_7 is not None:
                                    ph: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_7
                                    return ph

                                else: 
                                    active_pattern_result_8: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CComment_007C__007C(cells)
                                    if active_pattern_result_8 is not None:
                                        c_2: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_8
                                        return c_2

                                    else: 
                                        active_pattern_result_9: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CFreeText_007C__007C(cells)
                                        if active_pattern_result_9 is not None:
                                            ft: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_9
                                            return ft

                                        else: 
                                            return to_fail(printf("Could not parse header group %O"))(cells)












def to_fs_cells(has_unit: bool, header: CompositeHeader) -> FSharpList[FsCell]:
    if header.IsDataColumn:
        return of_array([FsCell(to_string(header)), FsCell("Data Format"), FsCell("Data Selector Format")])

    elif header.IsSingleColumn:
        return singleton(FsCell(to_string(header)))

    elif header.IsTermColumn:
        def _arrow935(__unit: None=None, has_unit: Any=has_unit, header: Any=header) -> IEnumerable_1[FsCell]:
            def _arrow934(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow933(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow932(__unit: None=None) -> IEnumerable_1[FsCell]:
                        return singleton_1(FsCell(("Term Accession Number (" + header.GetColumnAccessionShort) + ")"))

                    return append(singleton_1(FsCell(("Term Source REF (" + header.GetColumnAccessionShort) + ")")), delay(_arrow932))

                return append(singleton_1(FsCell("Unit")) if has_unit else empty(), delay(_arrow933))

            return append(singleton_1(FsCell(to_string(header))), delay(_arrow934))

        return to_list(delay(_arrow935))

    else: 
        return to_fail(printf("header %O is neither single nor term column"))(header)



__all__ = ["ActivePattern_mergeIDInfo", "ActivePattern__007CTerm_007C__007C", "ActivePattern__007CParameter_007C__007C", "ActivePattern__007CFactor_007C__007C", "ActivePattern__007CCharacteristic_007C__007C", "ActivePattern__007CComponent_007C__007C", "ActivePattern__007CInput_007C__007C", "ActivePattern__007COutput_007C__007C", "ActivePattern__007CComment_007C__007C", "ActivePattern__007CProtocolType_007C__007C", "ActivePattern__007CProtocolHeader_007C__007C", "ActivePattern__007CFreeText_007C__007C", "from_fs_cells", "to_fs_cells"]

