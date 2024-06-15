from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import map as map_2
from ...fable_modules.fable_library.list import (map, FSharpList, item, of_array, singleton as singleton_1)
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (to_array, delay, map as map_1, exists, to_list, append, singleton, empty)
from ...fable_modules.fable_library.types import (to_string, Array)
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.fs_address import FsAddress__get_RowNumber
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress__get_LastAddress
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_base import FsRangeBase__get_RangeAddress
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_column import CompositeColumn
from ...Core.Table.composite_header import (IOType, CompositeHeader)
from .composite_cell import to_fs_cells as to_fs_cells_1
from .composite_header import (from_fs_cells, to_fs_cells)

def fix_deprecated_ioheader(col: FsColumn) -> FsColumn:
    match_value: IOType = IOType.of_string(col.Item(1).ValueAsString())
    if match_value.tag == 4:
        return col

    elif match_value.tag == 0:
        col.Item(1).SetValueAs(to_string(CompositeHeader(11, IOType(0))))
        return col

    else: 
        col.Item(1).SetValueAs(to_string(CompositeHeader(12, match_value)))
        return col



def from_fs_columns(columns: FSharpList[FsColumn]) -> CompositeColumn:
    def mapping(c: FsColumn, columns: Any=columns) -> FsCell:
        return c.Item(1)

    pattern_input: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = from_fs_cells(map(mapping, columns))
    l: int = FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(item(0, columns)))) or 0
    def _arrow937(__unit: None=None, columns: Any=columns) -> IEnumerable_1[CompositeCell]:
        def _arrow936(i: int) -> CompositeCell:
            def mapping_1(c_1: FsColumn) -> FsCell:
                return c_1.Item(i)

            return pattern_input[1](map(mapping_1, columns))

        return map_1(_arrow936, range_big_int(2, 1, l))

    cells_1: Array[CompositeCell] = to_array(delay(_arrow937))
    return CompositeColumn.create(pattern_input[0], cells_1)


def to_fs_columns(column: CompositeColumn) -> FSharpList[FSharpList[FsCell]]:
    def predicate(c: CompositeCell, column: Any=column) -> bool:
        return c.is_unitized

    has_unit: bool = exists(predicate, column.Cells)
    is_term: bool = column.Header.IsTermColumn
    is_data: bool = column.Header.IsDataColumn
    header: FSharpList[FsCell] = to_fs_cells(has_unit, column.Header)
    def mapping(cell: CompositeCell, column: Any=column) -> FSharpList[FsCell]:
        return to_fs_cells_1(is_term, has_unit, cell)

    cells: Array[FSharpList[FsCell]] = map_2(mapping, column.Cells, None)
    if has_unit:
        def _arrow943(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow942(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow941(i: int) -> FsCell:
                    return item(0, cells[i])

                return map_1(_arrow941, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(0, header)), delay(_arrow942))

        def _arrow946(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow945(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow944(i_1: int) -> FsCell:
                    return item(1, cells[i_1])

                return map_1(_arrow944, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(1, header)), delay(_arrow945))

        def _arrow949(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow948(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow947(i_2: int) -> FsCell:
                    return item(2, cells[i_2])

                return map_1(_arrow947, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(2, header)), delay(_arrow948))

        def _arrow952(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow951(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow950(i_3: int) -> FsCell:
                    return item(3, cells[i_3])

                return map_1(_arrow950, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(3, header)), delay(_arrow951))

        return of_array([to_list(delay(_arrow943)), to_list(delay(_arrow946)), to_list(delay(_arrow949)), to_list(delay(_arrow952))])

    elif is_term:
        def _arrow958(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow957(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow956(i_4: int) -> FsCell:
                    return item(0, cells[i_4])

                return map_1(_arrow956, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(0, header)), delay(_arrow957))

        def _arrow961(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow960(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow959(i_5: int) -> FsCell:
                    return item(1, cells[i_5])

                return map_1(_arrow959, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(1, header)), delay(_arrow960))

        def _arrow964(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow963(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow962(i_6: int) -> FsCell:
                    return item(2, cells[i_6])

                return map_1(_arrow962, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(2, header)), delay(_arrow963))

        return of_array([to_list(delay(_arrow958)), to_list(delay(_arrow961)), to_list(delay(_arrow964))])

    elif is_data:
        def predicate_1(c_1: CompositeCell, column: Any=column) -> bool:
            return c_1.AsData.Format is not None

        has_format: bool = exists(predicate_1, column.Cells)
        def predicate_2(c_2: CompositeCell, column: Any=column) -> bool:
            return c_2.AsData.SelectorFormat is not None

        has_selector_format: bool = exists(predicate_2, column.Cells)
        def _arrow976(__unit: None=None, column: Any=column) -> IEnumerable_1[FSharpList[FsCell]]:
            def _arrow967(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow966(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow965(i_7: int) -> FsCell:
                        return item(0, cells[i_7])

                    return map_1(_arrow965, range_big_int(0, 1, len(column.Cells) - 1))

                return append(singleton(item(0, header)), delay(_arrow966))

            def _arrow975(__unit: None=None) -> IEnumerable_1[FSharpList[FsCell]]:
                def _arrow970(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow969(__unit: None=None) -> IEnumerable_1[FsCell]:
                        def _arrow968(i_8: int) -> FsCell:
                            return item(1, cells[i_8])

                        return map_1(_arrow968, range_big_int(0, 1, len(column.Cells) - 1))

                    return append(singleton(item(1, header)), delay(_arrow969))

                def _arrow974(__unit: None=None) -> IEnumerable_1[FSharpList[FsCell]]:
                    def _arrow973(__unit: None=None) -> IEnumerable_1[FsCell]:
                        def _arrow972(__unit: None=None) -> IEnumerable_1[FsCell]:
                            def _arrow971(i_9: int) -> FsCell:
                                return item(2, cells[i_9])

                            return map_1(_arrow971, range_big_int(0, 1, len(column.Cells) - 1))

                        return append(singleton(item(2, header)), delay(_arrow972))

                    return singleton(to_list(delay(_arrow973))) if has_selector_format else empty()

                return append(singleton(to_list(delay(_arrow970))) if has_format else empty(), delay(_arrow974))

            return append(singleton(to_list(delay(_arrow967))), delay(_arrow975))

        return to_list(delay(_arrow976))

    else: 
        def _arrow979(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow978(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow977(i_10: int) -> FsCell:
                    return item(0, cells[i_10])

                return map_1(_arrow977, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(0, header)), delay(_arrow978))

        return singleton_1(to_list(delay(_arrow979)))



__all__ = ["fix_deprecated_ioheader", "from_fs_columns", "to_fs_columns"]

