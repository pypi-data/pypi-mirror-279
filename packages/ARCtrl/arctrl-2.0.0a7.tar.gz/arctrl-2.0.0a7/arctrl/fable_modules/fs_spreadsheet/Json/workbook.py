from __future__ import annotations
from typing import Any
from ...fable_library.seq import map
from ...fable_library.util import (to_enumerable, IEnumerable_1)
from ...thoth_json_core.decode import (object, seq as seq_1, IRequiredGetter, IGetters)
from ...thoth_json_core.encode import seq
from ...thoth_json_core.types import (Json, Decoder_1)
from ..fs_workbook import FsWorkbook
from ..fs_worksheet import FsWorksheet
from .worksheet import (encode as encode_1, decode as decode_1)

def encode(wb: FsWorkbook) -> Json:
    def mapping(sheet: FsWorksheet, wb: Any=wb) -> Json:
        return encode_1(sheet)

    return Json(5, to_enumerable([("sheets", seq(map(mapping, wb.GetWorksheets())))]))


def _arrow246(builder: IGetters) -> FsWorkbook:
    wb: FsWorkbook = FsWorkbook()
    ws: IEnumerable_1[FsWorksheet]
    arg_1: Decoder_1[IEnumerable_1[FsWorksheet]] = seq_1(decode_1)
    object_arg: IRequiredGetter = builder.Required
    ws = object_arg.Field("sheets", arg_1)
    wb.AddWorksheets(ws)
    return wb


decode: Decoder_1[FsWorkbook] = object(_arrow246)

__all__ = ["encode", "decode"]

