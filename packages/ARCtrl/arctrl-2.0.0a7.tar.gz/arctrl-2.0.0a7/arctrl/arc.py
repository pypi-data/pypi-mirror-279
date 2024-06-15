from __future__ import annotations
from collections.abc import Callable
from typing import Any
from .fable_modules.fable_library.array_ import (choose, try_pick, exactly_one, map, filter, iterate, exists, fold, concat)
from .fable_modules.fable_library.list import FSharpList
from .fable_modules.fable_library.map import of_seq as of_seq_1
from .fable_modules.fable_library.map_util import add_to_dict
from .fable_modules.fable_library.option import (default_arg, value as value_2, map as map_2, bind)
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)
from .fable_modules.fable_library.result import FSharpResult_2
from .fable_modules.fable_library.seq import (to_array, contains, to_list, delay, append, singleton, map as map_1, try_find, find, iterate as iterate_1, empty, collect)
from .fable_modules.fable_library.set import (union_many, of_seq, FSharpSet__Contains)
from .fable_modules.fable_library.string_ import (replace, to_text, printf)
from .fable_modules.fable_library.types import Array
from .fable_modules.fable_library.util import (string_hash, IEnumerable_1, to_enumerable, safe_hash, compare_primitives)
from .fable_modules.fs_spreadsheet.Cells.fs_cells_collection import Dictionary_tryGet
from .fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from .fable_modules.thoth_json_core.types import Json
from .Contract.arc import try_isaread_contract_from_path
from .Contract.arc_assay import (ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F, ARCtrl_ArcAssay__ArcAssay_ToDeleteContract, ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49, ARCtrl_ArcAssay__ArcAssay_ToUpdateContract)
from .Contract.arc_investigation import (ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F, ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract_6FCE9E49)
from .Contract.arc_study import (ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F, ARCtrl_ArcStudy__ArcStudy_ToUpdateContract, ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49)
from .Contract.contract import (Contract, DTOType, DTO)
from .Contract.datamap import (ARCtrl_DataMap__DataMap_tryFromReadContractForAssay_Static, ARCtrl_DataMap__DataMap_tryFromReadContractForStudy_Static, ARCtrl_DataMap__DataMap_ToCreateContractForStudy_Z721C83C5, ARCtrl_DataMap__DataMap_ToUpdateContractForStudy_Z721C83C5, ARCtrl_DataMap__DataMap_ToCreateContractForAssay_Z721C83C5, ARCtrl_DataMap__DataMap_ToUpdateContractForAssay_Z721C83C5)
from .Contract.git import (Init_createInitContract_6DFDD678, gitattributes_contract, gitignore_contract, Init_createAddRemoteContract_Z721C83C5, Clone_createCloneContract_5000466F)
from .Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from .Core.Helper.identifier import (Study_fileNameFromIdentifier, Study_datamapFileNameFromIdentifier, Assay_fileNameFromIdentifier, Assay_datamapFileNameFromIdentifier)
from .Core.Table.arc_table import ArcTable
from .Core.Table.arc_tables import ArcTables
from .Core.Table.data_map import (DataMap, DataMap__set_StaticHash_Z524259A4, DataMap__get_StaticHash)
from .FileSystem.file_system import FileSystem
from .FileSystem.file_system_tree import FileSystemTree
from .FileSystem.path import (get_assay_folder_path, get_study_folder_path)
from .fable_modules.thoth_json_python.decode import Decode_fromString
from .fable_modules.thoth_json_python.encode import to_string
from .Json.arc import (decoder as decoder_1, encoder)
from .Json.encode import default_spaces
from .Spreadsheet.arc_assay import to_fs_workbook as to_fs_workbook_2
from .Spreadsheet.arc_investigation import (to_light_fs_workbook, to_fs_workbook)
from .Spreadsheet.arc_study import ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_353D0DB7
from .Spreadsheet.data_map import to_fs_workbook as to_fs_workbook_1

def ARCAux_getArcAssaysFromContracts(contracts: Array[Contract]) -> Array[ArcAssay]:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcAssay | None:
        return ARCtrl_ArcAssay__ArcAssay_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getAssayDataMapFromContracts(assay_identifier: str, contracts: Array[Contract]) -> DataMap | None:
    def chooser(c: Contract, assay_identifier: Any=assay_identifier, contracts: Any=contracts) -> DataMap | None:
        return ARCtrl_DataMap__DataMap_tryFromReadContractForAssay_Static(assay_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getArcStudiesFromContracts(contracts: Array[Contract]) -> Array[tuple[ArcStudy, FSharpList[ArcAssay]]]:
    def chooser(c: Contract, contracts: Any=contracts) -> tuple[ArcStudy, FSharpList[ArcAssay]] | None:
        return ARCtrl_ArcStudy__ArcStudy_tryFromReadContract_Static_7570923F(c)

    return choose(chooser, contracts, None)


def ARCAux_getStudyDataMapFromContracts(study_identifier: str, contracts: Array[Contract]) -> DataMap | None:
    def chooser(c: Contract, study_identifier: Any=study_identifier, contracts: Any=contracts) -> DataMap | None:
        return ARCtrl_DataMap__DataMap_tryFromReadContractForStudy_Static(study_identifier, c)

    return try_pick(chooser, contracts)


def ARCAux_getArcInvestigationFromContracts(contracts: Array[Contract]) -> ArcInvestigation:
    def chooser(c: Contract, contracts: Any=contracts) -> ArcInvestigation | None:
        return ARCtrl_ArcInvestigation__ArcInvestigation_tryFromReadContract_Static_7570923F(c)

    return exactly_one(choose(chooser, contracts, None))


def ARCAux_updateFSByISA(isa: ArcInvestigation | None, fs: FileSystem) -> FileSystem:
    pattern_input: tuple[Array[ArcStudy], Array[ArcAssay]]
    if isa is None:
        pattern_input = ([], [])

    else: 
        inv: ArcInvestigation = isa
        pattern_input = (to_array(inv.Studies), to_array(inv.Assays))

    assays_folder: FileSystemTree
    def mapping(a: ArcAssay, isa: Any=isa, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_assay_folder(a.Identifier, a.DataMap is not None)

    assays_1: Array[FileSystemTree] = map(mapping, pattern_input[1], None)
    assays_folder = FileSystemTree.create_assays_folder(assays_1)
    studies_folder: FileSystemTree
    def mapping_1(s: ArcStudy, isa: Any=isa, fs: Any=fs) -> FileSystemTree:
        return FileSystemTree.create_study_folder(s.Identifier, s.DataMap is not None)

    studies_1: Array[FileSystemTree] = map(mapping_1, pattern_input[0], None)
    studies_folder = FileSystemTree.create_studies_folder(studies_1)
    investigation: FileSystemTree = FileSystemTree.create_investigation_file()
    tree_1: FileSystem
    tree: FileSystemTree = FileSystemTree.create_root_folder([investigation, assays_folder, studies_folder])
    tree_1 = FileSystem.create(tree = tree)
    return fs.Union(tree_1)


def ARCAux_updateFSByCWL(cwl: None | None, fs: FileSystem) -> FileSystem:
    workflows: FileSystemTree = FileSystemTree.create_workflows_folder([])
    runs: FileSystemTree = FileSystemTree.create_runs_folder([])
    tree_1: FileSystem
    tree: FileSystemTree = FileSystemTree.create_root_folder([workflows, runs])
    tree_1 = FileSystem.create(tree = tree)
    return fs.Union(tree_1)


def _expr2062() -> TypeInfo:
    return class_type("ARCtrl.ARC", None, ARC)


class ARC:
    def __init__(self, isa: ArcInvestigation | None=None, cwl: None | None=None, fs: FileSystem | None=None) -> None:
        self.cwl: None | None = cwl
        self._isa: ArcInvestigation | None = isa
        self._cwl: None | None = self.cwl
        self._fs: FileSystem = ARCAux_updateFSByCWL(self.cwl, ARCAux_updateFSByISA(isa, default_arg(fs, FileSystem.create(tree = FileSystemTree(1, "", [])))))

    @property
    def ISA(self, __unit: None=None) -> ArcInvestigation | None:
        this: ARC = self
        return this._isa

    @ISA.setter
    def ISA(self, new_isa: ArcInvestigation | None=None) -> None:
        this: ARC = self
        this._isa = new_isa
        this.UpdateFileSystem()

    @property
    def CWL(self, __unit: None=None) -> None | None:
        this: ARC = self
        return this.cwl

    @property
    def FileSystem(self, __unit: None=None) -> FileSystem:
        this: ARC = self
        return this._fs

    @FileSystem.setter
    def FileSystem(self, fs: FileSystem) -> None:
        this: ARC = self
        this._fs = fs

    def RemoveAssay(self, assay_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot remove assay from null ISA value.")

        else: 
            def _arrow1998(__unit: None=None) -> bool:
                i: ArcInvestigation = match_value
                class ObjectExpr1997:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow1996(x: str, y: str) -> bool:
                            return x == y

                        return _arrow1996

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(assay_identifier, i.AssayIdentifiers, ObjectExpr1997())

            if _arrow1998():
                i_1: ArcInvestigation = match_value
                isa = i_1

            else: 
                raise Exception("ARC does not contain assay with given name")


        assay: ArcAssay = isa.GetAssay(assay_identifier)
        studies: Array[ArcStudy] = assay.StudiesRegisteredIn
        isa.RemoveAssay(assay_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        assay_folder_path: str = get_assay_folder_path(assay_identifier)
        def predicate(p: str) -> bool:
            return not (p.find(assay_folder_path) == 0)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        def _arrow2001(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow2000(__unit: None=None) -> IEnumerable_1[Contract]:
                def _arrow1999(__unit: None=None) -> IEnumerable_1[Contract]:
                    return map_1(ARCtrl_ArcStudy__ArcStudy_ToUpdateContract, studies)

                return append(singleton(ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract_6FCE9E49(isa)), delay(_arrow1999))

            return append(singleton(ARCtrl_ArcAssay__ArcAssay_ToDeleteContract(assay)), delay(_arrow2000))

        return list(to_list(delay(_arrow2001)))

    def RenameAssay(self, old_assay_identifier: str, new_assay_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot rename assay in null ISA value.")

        else: 
            def _arrow2004(__unit: None=None) -> bool:
                i: ArcInvestigation = match_value
                class ObjectExpr2003:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow2002(x: str, y: str) -> bool:
                            return x == y

                        return _arrow2002

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(old_assay_identifier, i.AssayIdentifiers, ObjectExpr2003())

            if _arrow2004():
                i_1: ArcInvestigation = match_value
                isa = i_1

            else: 
                raise Exception("ARC does not contain assay with given name")


        isa.RenameAssay(old_assay_identifier, new_assay_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_assay_folder_path: str = get_assay_folder_path(old_assay_identifier)
        new_assay_folder_path: str = get_assay_folder_path(new_assay_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_assay_folder_path, new_assay_folder_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow2006(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow2005(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton(Contract.create_rename(old_assay_folder_path, new_assay_folder_path)), delay(_arrow2005))

        return list(to_list(delay(_arrow2006)))

    def RemoveStudy(self, study_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot remove study from null ISA value.")

        else: 
            isa = match_value

        isa.RemoveStudy(study_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        study_folder_path: str = get_study_folder_path(study_identifier)
        def predicate(p: str) -> bool:
            return not (p.find(study_folder_path) == 0)

        filtered_paths: Array[str] = filter(predicate, paths)
        this.SetFilePaths(filtered_paths)
        return list(to_enumerable([Contract.create_delete(study_folder_path), ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract_6FCE9E49(isa)]))

    def RenameStudy(self, old_study_identifier: str, new_study_identifier: str) -> Array[Contract]:
        this: ARC = self
        isa: ArcInvestigation
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            raise Exception("Cannot rename study in null ISA value.")

        else: 
            def _arrow2009(__unit: None=None) -> bool:
                i: ArcInvestigation = match_value
                class ObjectExpr2008:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow2007(x: str, y: str) -> bool:
                            return x == y

                        return _arrow2007

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(old_study_identifier, i.StudyIdentifiers, ObjectExpr2008())

            if _arrow2009():
                i_1: ArcInvestigation = match_value
                isa = i_1

            else: 
                raise Exception("ARC does not contain study with given name")


        isa.RenameStudy(old_study_identifier, new_study_identifier)
        paths: Array[str] = this.FileSystem.Tree.ToFilePaths()
        old_study_folder_path: str = get_study_folder_path(old_study_identifier)
        new_study_folder_path: str = get_study_folder_path(new_study_identifier)
        def mapping(p: str) -> str:
            return replace(p, old_study_folder_path, new_study_folder_path)

        renamed_paths: Array[str] = map(mapping, paths, None)
        this.SetFilePaths(renamed_paths)
        def _arrow2011(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow2010(__unit: None=None) -> IEnumerable_1[Contract]:
                return this.GetUpdateContracts()

            return append(singleton(Contract.create_rename(old_study_folder_path, new_study_folder_path)), delay(_arrow2010))

        return list(to_list(delay(_arrow2011)))

    @staticmethod
    def from_file_paths(file_paths: Array[str]) -> ARC:
        return ARC(None, None, FileSystem.from_file_paths(file_paths))

    def SetFilePaths(self, file_paths: Array[str]) -> None:
        this: ARC = self
        tree: FileSystemTree = FileSystemTree.from_file_paths(file_paths)
        this._fs = FileSystem(tree, this._fs.History)

    def GetReadContracts(self, __unit: None=None) -> Array[Contract]:
        this: ARC = self
        return choose(try_isaread_contract_from_path, this._fs.Tree.ToFilePaths(), None)

    def SetISAFromContracts(self, contracts: Array[Contract]) -> None:
        this: ARC = self
        investigation: ArcInvestigation = ARCAux_getArcInvestigationFromContracts(contracts)
        def mapping(tuple: tuple[ArcStudy, FSharpList[ArcAssay]]) -> ArcStudy:
            return tuple[0]

        studies: Array[ArcStudy] = map(mapping, ARCAux_getArcStudiesFromContracts(contracts), None)
        assays: Array[ArcAssay] = ARCAux_getArcAssaysFromContracts(contracts)
        def action(ai: str) -> None:
            def predicate(a: ArcAssay, ai: Any=ai) -> bool:
                return a.Identifier == ai

            if not exists(predicate, assays):
                investigation.DeleteAssay(ai)


        iterate(action, investigation.AssayIdentifiers)
        def action_1(si: str) -> None:
            def predicate_1(s: ArcStudy, si: Any=si) -> bool:
                return s.Identifier == si

            if not exists(predicate_1, studies):
                investigation.DeleteStudy(si)


        iterate(action_1, investigation.StudyIdentifiers)
        def action_2(study: ArcStudy) -> None:
            def predicate_2(s_1: ArcStudy, study: Any=study) -> bool:
                return s_1.Identifier == study.Identifier

            registered_study_opt: ArcStudy | None = try_find(predicate_2, investigation.Studies)
            if registered_study_opt is None:
                investigation.AddStudy(study)

            else: 
                registered_study: ArcStudy = registered_study_opt
                registered_study.UpdateReferenceByStudyFile(study, True)

            datamap: DataMap | None = ARCAux_getAssayDataMapFromContracts(study.Identifier, contracts)
            study.DataMap = datamap
            study.StaticHash = study.GetLightHashCode() or 0

        iterate(action_2, studies)
        def action_3(assay: ArcAssay) -> None:
            def predicate_3(a_1: ArcAssay, assay: Any=assay) -> bool:
                return a_1.Identifier == assay.Identifier

            registered_assay_opt: ArcAssay | None = try_find(predicate_3, investigation.Assays)
            if registered_assay_opt is None:
                investigation.AddAssay(assay)

            else: 
                registered_assay: ArcAssay = registered_assay_opt
                registered_assay.UpdateReferenceByAssayFile(assay, True)

            def predicate_4(a_2: ArcAssay, assay: Any=assay) -> bool:
                return a_2.Identifier == assay.Identifier

            assay_1: ArcAssay = find(predicate_4, investigation.Assays)
            updated_tables: ArcTables
            array_6: Array[ArcStudy] = assay_1.StudiesRegisteredIn
            def folder(tables: ArcTables, study_1: ArcStudy, assay: Any=assay) -> ArcTables:
                return ArcTables.update_reference_tables_by_sheets(ArcTables(study_1.Tables), tables, False)

            updated_tables = fold(folder, ArcTables(assay_1.Tables), array_6)
            datamap_1: DataMap | None = ARCAux_getAssayDataMapFromContracts(assay_1.Identifier, contracts)
            assay_1.DataMap = datamap_1
            assay_1.Tables = updated_tables.Tables

        iterate(action_3, assays)
        def action_4(a_3: ArcAssay) -> None:
            a_3.StaticHash = a_3.GetLightHashCode() or 0

        iterate_1(action_4, investigation.Assays)
        def action_5(s_2: ArcStudy) -> None:
            s_2.StaticHash = s_2.GetLightHashCode() or 0

        iterate_1(action_5, investigation.Studies)
        investigation.StaticHash = investigation.GetLightHashCode() or 0
        this.ISA = investigation

    def UpdateFileSystem(self, __unit: None=None) -> None:
        this: ARC = self
        new_fs: FileSystem
        fs: FileSystem = ARCAux_updateFSByISA(this._isa, this._fs)
        new_fs = ARCAux_updateFSByCWL(this._cwl, fs)
        this._fs = new_fs

    def GetWriteContracts(self, is_light: bool | None=None) -> Array[Contract]:
        this: ARC = self
        is_light_1: bool = default_arg(is_light, True)
        workbooks: Any = dict([])
        match_value: ArcInvestigation | None = this.ISA
        if match_value is None:
            add_to_dict(workbooks, "isa.investigation.xlsx", (DTOType(2), to_light_fs_workbook(ArcInvestigation.create("MISSING_IDENTIFIER_"))))

        else: 
            inv: ArcInvestigation = match_value
            add_to_dict(workbooks, "isa.investigation.xlsx", (DTOType(2), (to_light_fs_workbook if is_light_1 else to_fs_workbook)(inv)))
            inv.StaticHash = inv.GetLightHashCode() or 0
            def action(s: ArcStudy) -> None:
                s.StaticHash = s.GetLightHashCode() or 0
                add_to_dict(workbooks, Study_fileNameFromIdentifier(s.Identifier), (DTOType(1), ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_353D0DB7(s)))
                if s.DataMap is not None:
                    dm: DataMap = value_2(s.DataMap)
                    DataMap__set_StaticHash_Z524259A4(dm, safe_hash(dm))
                    add_to_dict(workbooks, Study_datamapFileNameFromIdentifier(s.Identifier), (DTOType(3), to_fs_workbook_1(dm)))


            iterate_1(action, inv.Studies)
            def action_1(a: ArcAssay) -> None:
                a.StaticHash = a.GetLightHashCode() or 0
                add_to_dict(workbooks, Assay_fileNameFromIdentifier(a.Identifier), (DTOType(0), to_fs_workbook_2(a)))
                if a.DataMap is not None:
                    dm_1: DataMap = value_2(a.DataMap)
                    DataMap__set_StaticHash_Z524259A4(dm_1, safe_hash(dm_1))
                    add_to_dict(workbooks, Assay_datamapFileNameFromIdentifier(a.Identifier), (DTOType(3), to_fs_workbook_1(dm_1)))


            iterate_1(action_1, inv.Assays)

        def mapping(fp: str) -> Contract:
            match_value_1: tuple[DTOType, FsWorkbook] | None = Dictionary_tryGet(fp, workbooks)
            if match_value_1 is None:
                return Contract.create_create(fp, DTOType(7))

            else: 
                wb: FsWorkbook = match_value_1[1]
                dto: DTOType = match_value_1[0]
                return Contract.create_create(fp, dto, DTO(0, wb))


        return map(mapping, this._fs.Tree.ToFilePaths(True), None)

    def GetUpdateContracts(self, is_light: bool | None=None) -> Array[Contract]:
        this: ARC = self
        is_light_1: bool = default_arg(is_light, True)
        match_value: ArcInvestigation | None = this.ISA
        def _arrow2012(__unit: None=None) -> bool:
            inv: ArcInvestigation = match_value
            return inv.StaticHash == 0

        def _arrow2013(__unit: None=None) -> Array[Contract]:
            inv_1: ArcInvestigation = match_value
            return this.GetWriteContracts(is_light_1)

        def _arrow2027(__unit: None=None) -> Array[Contract]:
            inv_2: ArcInvestigation = match_value
            def _arrow2026(__unit: None=None) -> IEnumerable_1[Contract]:
                hash_1: int = inv_2.GetLightHashCode() or 0
                def _arrow2025(__unit: None=None) -> IEnumerable_1[Contract]:
                    inv_2.StaticHash = hash_1 or 0
                    def _arrow2018(s: ArcStudy) -> IEnumerable_1[Contract]:
                        hash_2: int = s.GetLightHashCode() or 0
                        def _arrow2017(__unit: None=None) -> IEnumerable_1[Contract]:
                            s.StaticHash = hash_2 or 0
                            match_value_1: DataMap | None = s.DataMap
                            (pattern_matching_result, dm_2, dm_3) = (None, None, None)
                            if match_value_1 is not None:
                                if DataMap__get_StaticHash(match_value_1) == 0:
                                    pattern_matching_result = 0
                                    dm_2 = match_value_1

                                else: 
                                    def _arrow2016(__unit: None=None) -> bool:
                                        dm_1: DataMap = match_value_1
                                        return DataMap__get_StaticHash(dm_1) != safe_hash(dm_1)

                                    if _arrow2016():
                                        pattern_matching_result = 1
                                        dm_3 = match_value_1

                                    else: 
                                        pattern_matching_result = 2



                            else: 
                                pattern_matching_result = 2

                            if pattern_matching_result == 0:
                                def _arrow2014(__unit: None=None) -> IEnumerable_1[Contract]:
                                    DataMap__set_StaticHash_Z524259A4(dm_2, safe_hash(dm_2))
                                    return empty()

                                return append(singleton(ARCtrl_DataMap__DataMap_ToCreateContractForStudy_Z721C83C5(dm_2, s.Identifier)), delay(_arrow2014))

                            elif pattern_matching_result == 1:
                                def _arrow2015(__unit: None=None) -> IEnumerable_1[Contract]:
                                    DataMap__set_StaticHash_Z524259A4(dm_3, safe_hash(dm_3))
                                    return empty()

                                return append(singleton(ARCtrl_DataMap__DataMap_ToUpdateContractForStudy_Z721C83C5(dm_3, s.Identifier)), delay(_arrow2015))

                            elif pattern_matching_result == 2:
                                return empty()


                        return append(ARCtrl_ArcStudy__ArcStudy_ToCreateContract_6FCE9E49(s, True) if (s.StaticHash == 0) else (singleton(ARCtrl_ArcStudy__ArcStudy_ToUpdateContract(s)) if (s.StaticHash != hash_2) else empty()), delay(_arrow2017))

                    def _arrow2024(__unit: None=None) -> IEnumerable_1[Contract]:
                        def _arrow2023(a: ArcAssay) -> IEnumerable_1[Contract]:
                            hash_3: int = a.GetLightHashCode() or 0
                            def _arrow2022(__unit: None=None) -> IEnumerable_1[Contract]:
                                a.StaticHash = hash_3 or 0
                                match_value_2: DataMap | None = a.DataMap
                                (pattern_matching_result_1, dm_6, dm_7) = (None, None, None)
                                if match_value_2 is not None:
                                    if DataMap__get_StaticHash(match_value_2) == 0:
                                        pattern_matching_result_1 = 0
                                        dm_6 = match_value_2

                                    else: 
                                        def _arrow2021(__unit: None=None) -> bool:
                                            dm_5: DataMap = match_value_2
                                            return DataMap__get_StaticHash(dm_5) != safe_hash(dm_5)

                                        if _arrow2021():
                                            pattern_matching_result_1 = 1
                                            dm_7 = match_value_2

                                        else: 
                                            pattern_matching_result_1 = 2



                                else: 
                                    pattern_matching_result_1 = 2

                                if pattern_matching_result_1 == 0:
                                    def _arrow2019(__unit: None=None) -> IEnumerable_1[Contract]:
                                        DataMap__set_StaticHash_Z524259A4(dm_6, safe_hash(dm_6))
                                        return empty()

                                    return append(singleton(ARCtrl_DataMap__DataMap_ToCreateContractForAssay_Z721C83C5(dm_6, a.Identifier)), delay(_arrow2019))

                                elif pattern_matching_result_1 == 1:
                                    def _arrow2020(__unit: None=None) -> IEnumerable_1[Contract]:
                                        DataMap__set_StaticHash_Z524259A4(dm_7, safe_hash(dm_7))
                                        return empty()

                                    return append(singleton(ARCtrl_DataMap__DataMap_ToUpdateContractForAssay_Z721C83C5(dm_7, a.Identifier)), delay(_arrow2020))

                                elif pattern_matching_result_1 == 2:
                                    return empty()


                            return append(ARCtrl_ArcAssay__ArcAssay_ToCreateContract_6FCE9E49(a, True) if (a.StaticHash == 0) else (singleton(ARCtrl_ArcAssay__ArcAssay_ToUpdateContract(a)) if (a.StaticHash != hash_3) else empty()), delay(_arrow2022))

                        return collect(_arrow2023, inv_2.Assays)

                    return append(collect(_arrow2018, inv_2.Studies), delay(_arrow2024))

                return append(singleton(ARCtrl_ArcInvestigation__ArcInvestigation_ToUpdateContract_6FCE9E49(inv_2, is_light_1)) if (inv_2.StaticHash != hash_1) else empty(), delay(_arrow2025))

            return to_array(delay(_arrow2026))

        return (_arrow2013() if _arrow2012() else _arrow2027()) if (match_value is not None) else this.GetWriteContracts(is_light_1)

    def GetGitInitContracts(self, branch: str | None=None, repository_address: str | None=None, default_gitignore: bool | None=None) -> Array[Contract]:
        default_gitignore_1: bool = default_arg(default_gitignore, False)
        def _arrow2031(__unit: None=None) -> IEnumerable_1[Contract]:
            def _arrow2030(__unit: None=None) -> IEnumerable_1[Contract]:
                def _arrow2029(__unit: None=None) -> IEnumerable_1[Contract]:
                    def _arrow2028(__unit: None=None) -> IEnumerable_1[Contract]:
                        return singleton(Init_createAddRemoteContract_Z721C83C5(value_2(repository_address))) if (repository_address is not None) else empty()

                    return append(singleton(gitignore_contract) if default_gitignore_1 else empty(), delay(_arrow2028))

                return append(singleton(gitattributes_contract), delay(_arrow2029))

            return append(singleton(Init_createInitContract_6DFDD678(branch)), delay(_arrow2030))

        return to_array(delay(_arrow2031))

    @staticmethod
    def get_clone_contract(remote_url: str, merge: bool | None=None, branch: str | None=None, token: tuple[str, str] | None=None, nolfs: bool | None=None) -> Contract:
        return Clone_createCloneContract_5000466F(remote_url, merge, branch, token, nolfs)

    def Copy(self, __unit: None=None) -> ARC:
        this: ARC = self
        def mapping(i: ArcInvestigation) -> ArcInvestigation:
            return i.Copy()

        isa_copy: ArcInvestigation | None = map_2(mapping, this._isa)
        fs_copy: FileSystem = this._fs.Copy()
        return ARC(isa_copy, this._cwl, fs_copy)

    def GetRegisteredPayload(self, IgnoreHidden: bool | None=None) -> FileSystemTree:
        this: ARC = self
        def mapping_1(isa: ArcInvestigation) -> Array[ArcStudy]:
            return isa.Studies[:]

        def mapping(i: ArcInvestigation) -> ArcInvestigation:
            return i.Copy()

        registered_studies: Array[ArcStudy] = default_arg(map_2(mapping_1, map_2(mapping, this._isa)), [])
        def mapping_2(s: ArcStudy) -> Array[ArcAssay]:
            return s.RegisteredAssays[:]

        registered_assays: Array[ArcAssay] = concat(map(mapping_2, registered_studies, None), None)
        class ObjectExpr2032:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        def mapping_3(s_1: ArcStudy) -> Any:
            study_foldername: str = ((("" + "studies") + "/") + s_1.Identifier) + ""
            def _arrow2039(__unit: None=None, s_1: Any=s_1) -> IEnumerable_1[str]:
                def _arrow2038(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow2037(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow2036(table: ArcTable) -> IEnumerable_1[str]:
                            def _arrow2035(kv: Any) -> IEnumerable_1[str]:
                                text_value: str = kv[1].ToFreeTextCell().AsFreeText
                                def _arrow2034(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow2033(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton(((((("" + study_foldername) + "/") + "protocols") + "/") + text_value) + "")

                                    return append(singleton(((((("" + study_foldername) + "/") + "resources") + "/") + text_value) + ""), delay(_arrow2033))

                                return append(singleton(text_value), delay(_arrow2034))

                            return collect(_arrow2035, table.Values)

                        return collect(_arrow2036, s_1.Tables)

                    return append(singleton(((("" + study_foldername) + "/") + "README.md") + ""), delay(_arrow2037))

                return append(singleton(((("" + study_foldername) + "/") + "isa.study.xlsx") + ""), delay(_arrow2038))

            class ObjectExpr2040:
                @property
                def Compare(self) -> Callable[[str, str], int]:
                    return compare_primitives

            return of_seq(to_list(delay(_arrow2039)), ObjectExpr2040())

        class ObjectExpr2041:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        def mapping_4(a: ArcAssay) -> Any:
            assay_foldername: str = ((("" + "assays") + "/") + a.Identifier) + ""
            def _arrow2048(__unit: None=None, a: Any=a) -> IEnumerable_1[str]:
                def _arrow2047(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow2046(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow2045(table_1: ArcTable) -> IEnumerable_1[str]:
                            def _arrow2044(kv_1: Any) -> IEnumerable_1[str]:
                                text_value_1: str = kv_1[1].ToFreeTextCell().AsFreeText
                                def _arrow2043(__unit: None=None) -> IEnumerable_1[str]:
                                    def _arrow2042(__unit: None=None) -> IEnumerable_1[str]:
                                        return singleton(((((("" + assay_foldername) + "/") + "protocols") + "/") + text_value_1) + "")

                                    return append(singleton(((((("" + assay_foldername) + "/") + "dataset") + "/") + text_value_1) + ""), delay(_arrow2042))

                                return append(singleton(text_value_1), delay(_arrow2043))

                            return collect(_arrow2044, table_1.Values)

                        return collect(_arrow2045, a.Tables)

                    return append(singleton(((("" + assay_foldername) + "/") + "README.md") + ""), delay(_arrow2046))

                return append(singleton(((("" + assay_foldername) + "/") + "isa.assay.xlsx") + ""), delay(_arrow2047))

            class ObjectExpr2049:
                @property
                def Compare(self) -> Callable[[str, str], int]:
                    return compare_primitives

            return of_seq(to_list(delay(_arrow2048)), ObjectExpr2049())

        class ObjectExpr2050:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        class ObjectExpr2051:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        include_files: Any = union_many(to_enumerable([of_seq(to_enumerable(["isa.investigation.xlsx", "README.md"]), ObjectExpr2032()), union_many(map(mapping_3, registered_studies, None), ObjectExpr2041()), union_many(map(mapping_4, registered_assays, None), ObjectExpr2050())]), ObjectExpr2051())
        ignore_hidden: bool = default_arg(IgnoreHidden, True)
        fs_copy: FileSystem = this._fs.Copy()
        def binder(tree_1: FileSystemTree) -> FileSystemTree | None:
            if ignore_hidden:
                def _arrow2052(n_1: str, tree_1: Any=tree_1) -> bool:
                    return not (n_1.find(".") == 0)

                return FileSystemTree.filter_folders(_arrow2052)(tree_1)

            else: 
                return tree_1


        def _arrow2054(__unit: None=None) -> FileSystemTree | None:
            tree: FileSystemTree
            def predicate(p: str) -> bool:
                if True if (p.find("workflows") == 0) else (p.find("runs") == 0):
                    return True

                else: 
                    return FSharpSet__Contains(include_files, p)


            paths: Array[str] = filter(predicate, FileSystemTree.to_file_paths()(fs_copy.Tree))
            tree = FileSystemTree.from_file_paths(paths)
            def _arrow2053(n: str) -> bool:
                return not (n.find(".") == 0)

            return FileSystemTree.filter_files(_arrow2053)(tree) if ignore_hidden else tree

        return default_arg(bind(binder, _arrow2054()), FileSystemTree.from_file_paths([]))

    def GetAdditionalPayload(self, IgnoreHidden: bool | None=None) -> FileSystemTree:
        this: ARC = self
        ignore_hidden: bool = default_arg(IgnoreHidden, True)
        class ObjectExpr2055:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        registered_payload: Any = of_seq(FileSystemTree.to_file_paths()(this.GetRegisteredPayload()), ObjectExpr2055())
        def binder(tree_1: FileSystemTree) -> FileSystemTree | None:
            if ignore_hidden:
                def _arrow2056(n_1: str, tree_1: Any=tree_1) -> bool:
                    return not (n_1.find(".") == 0)

                return FileSystemTree.filter_folders(_arrow2056)(tree_1)

            else: 
                return tree_1


        def _arrow2058(__unit: None=None) -> FileSystemTree | None:
            tree: FileSystemTree
            def predicate(p: str) -> bool:
                return not FSharpSet__Contains(registered_payload, p)

            paths: Array[str] = filter(predicate, FileSystemTree.to_file_paths()(this._fs.Copy().Tree))
            tree = FileSystemTree.from_file_paths(paths)
            def _arrow2057(n: str) -> bool:
                return not (n.find(".") == 0)

            return FileSystemTree.filter_files(_arrow2057)(tree) if ignore_hidden else tree

        return default_arg(bind(binder, _arrow2058()), FileSystemTree.from_file_paths([]))

    @staticmethod
    def DefaultContracts() -> Any:
        class ObjectExpr2059:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        return of_seq_1(to_enumerable([(".gitignore", gitignore_contract), (".gitattributes", gitattributes_contract)]), ObjectExpr2059())

    @staticmethod
    def from_rocrate_json_string(s: str) -> ARC:
        def _arrow2060(__unit: None=None) -> ArcInvestigation | None:
            match_value: FSharpResult_2[ArcInvestigation | None, str] = Decode_fromString(decoder_1, s)
            if match_value.tag == 1:
                raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

            else: 
                return match_value.fields[0]


        return ARC(_arrow2060())

    @staticmethod
    def to_rocrate_json_string(spaces: int | None=None) -> Callable[[ARC], str]:
        def _arrow2061(obj: ARC) -> str:
            value: Json = encoder(value_2(obj.ISA))
            return to_string(default_spaces(spaces), value)

        return _arrow2061


ARC_reflection = _expr2062

def ARC__ctor_79978BA1(isa: ArcInvestigation | None=None, cwl: None | None=None, fs: FileSystem | None=None) -> ARC:
    return ARC(isa, cwl, fs)


__all__ = ["ARCAux_getArcAssaysFromContracts", "ARCAux_getAssayDataMapFromContracts", "ARCAux_getArcStudiesFromContracts", "ARCAux_getStudyDataMapFromContracts", "ARCAux_getArcInvestigationFromContracts", "ARCAux_updateFSByISA", "ARCAux_updateFSByCWL", "ARC_reflection"]

