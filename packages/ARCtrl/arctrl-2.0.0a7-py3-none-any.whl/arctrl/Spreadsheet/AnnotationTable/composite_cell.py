from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.list import (map, FSharpList, item, of_array, singleton)
from ...fable_modules.fable_library.option import (map as map_1, default_arg)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...Core.Table.composite_cell import CompositeCell

def term_from_fs_cells(tsr_col: int | None, tan_col: int | None, cells: FSharpList[FsCell]) -> CompositeCell:
    def mapping(c: FsCell, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    def _arrow901(i: int, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return item(i, cell_values)

    tan: str | None = map_1(_arrow901, tan_col)
    def _arrow902(i_1: int, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return item(i_1, cell_values)

    tsr: str | None = map_1(_arrow902, tsr_col)
    return CompositeCell.create_term_from_string(item(0, cell_values), tsr, tan)


def unitized_from_fs_cells(unit_col: int, tsr_col: int | None, tan_col: int | None, cells: FSharpList[FsCell]) -> CompositeCell:
    def mapping(c: FsCell, unit_col: Any=unit_col, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    unit: str = item(unit_col, cell_values)
    def _arrow903(i: int, unit_col: Any=unit_col, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return item(i, cell_values)

    tan: str | None = map_1(_arrow903, tan_col)
    def _arrow904(i_1: int, unit_col: Any=unit_col, tsr_col: Any=tsr_col, tan_col: Any=tan_col, cells: Any=cells) -> str:
        return item(i_1, cell_values)

    tsr: str | None = map_1(_arrow904, tsr_col)
    return CompositeCell.create_unitized_from_string(item(0, cell_values), unit, tsr, tan)


def free_text_from_fs_cells(cells: FSharpList[FsCell]) -> CompositeCell:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    return CompositeCell.create_free_text(item(0, cell_values))


def data_from_fs_cells(format: int | None, selector_format: int | None, cells: FSharpList[FsCell]) -> CompositeCell:
    def mapping(c: FsCell, format: Any=format, selector_format: Any=selector_format, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    def _arrow905(i: int, format: Any=format, selector_format: Any=selector_format, cells: Any=cells) -> str:
        return item(i, cell_values)

    format_1: str | None = map_1(_arrow905, format)
    def _arrow906(i_1: int, format: Any=format, selector_format: Any=selector_format, cells: Any=cells) -> str:
        return item(i_1, cell_values)

    selector_format_1: str | None = map_1(_arrow906, selector_format)
    return CompositeCell.create_data_from_string(item(0, cell_values), format_1, selector_format_1)


def to_fs_cells(is_term: bool, has_unit: bool, cell: CompositeCell) -> FSharpList[FsCell]:
    if cell.tag == 0:
        if has_unit:
            return of_array([FsCell(cell.fields[0].NameText), FsCell(""), FsCell(default_arg(cell.fields[0].TermSourceREF, "")), FsCell(cell.fields[0].TermAccessionOntobeeUrl)])

        else: 
            return of_array([FsCell(cell.fields[0].NameText), FsCell(default_arg(cell.fields[0].TermSourceREF, "")), FsCell(cell.fields[0].TermAccessionOntobeeUrl)])


    elif cell.tag == 2:
        return of_array([FsCell(cell.fields[0]), FsCell(cell.fields[1].NameText), FsCell(default_arg(cell.fields[1].TermSourceREF, "")), FsCell(cell.fields[1].TermAccessionOntobeeUrl)])

    elif cell.tag == 3:
        format: FsCell = FsCell(default_arg(cell.fields[0].Format, ""))
        selector_format: FsCell = FsCell(default_arg(cell.fields[0].SelectorFormat, ""))
        return of_array([FsCell(default_arg(cell.fields[0].Name, "")), format, selector_format])

    elif has_unit:
        return of_array([FsCell(cell.fields[0]), FsCell(""), FsCell(""), FsCell("")])

    elif is_term:
        return of_array([FsCell(cell.fields[0]), FsCell(""), FsCell("")])

    else: 
        return singleton(FsCell(cell.fields[0]))



__all__ = ["term_from_fs_cells", "unitized_from_fs_cells", "free_text_from_fs_cells", "data_from_fs_cells", "to_fs_cells"]

