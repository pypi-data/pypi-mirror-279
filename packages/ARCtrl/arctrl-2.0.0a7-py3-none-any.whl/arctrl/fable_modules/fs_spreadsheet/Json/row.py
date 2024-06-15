from __future__ import annotations
from typing import Any
from ...fable_library.seq import map
from ...fable_library.util import (to_enumerable, IEnumerable_1)
from ...thoth_json_core.decode import (object, IRequiredGetter, int_1, seq as seq_1, IGetters)
from ...thoth_json_core.encode import seq
from ...thoth_json_core.types import (Json, Decoder_1)
from ..Cells.fs_cell import FsCell
from ..fs_row import FsRow
from .cell import (encode as encode_1, decode as decode_1)

def encode(row: FsRow) -> Json:
    def _arrow240(__unit: None=None, row: Any=row) -> Json:
        value: int = row.Index or 0
        return Json(7, int(value+0x100000000 if value < 0 else value))

    def mapping(cell: FsCell, row: Any=row) -> Json:
        return encode_1(cell)

    return Json(5, to_enumerable([("number", _arrow240()), ("cells", seq(map(mapping, row.Cells)))]))


def _arrow242(builder: IGetters) -> tuple[int, IEnumerable_1[FsCell]]:
    n: int
    object_arg: IRequiredGetter = builder.Required
    n = object_arg.Field("number", int_1)
    def _arrow241(__unit: None=None) -> IEnumerable_1[FsCell]:
        arg_3: Decoder_1[IEnumerable_1[FsCell]] = seq_1(decode_1(n))
        object_arg_1: IRequiredGetter = builder.Required
        return object_arg_1.Field("cells", arg_3)

    return (n, _arrow241())


decode: Decoder_1[tuple[int, IEnumerable_1[FsCell]]] = object(_arrow242)

__all__ = ["encode", "decode"]

