from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.util import to_enumerable
from .collections_ import (Dictionary_ofSeq, Dictionary_tryFind)

def OntobeeParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.obolibrary.org/obo/") + "") + tsr) + "_") + local_tan) + ""


def BioregistryParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://bioregistry.io/") + "") + tsr) + ":") + local_tan) + ""


def OntobeeDPBOParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "http://purl.org/nfdi4plants/ontology/dpbo/") + "") + tsr) + "_") + local_tan) + ""


def MSParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ms/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def POParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/po/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def ROParser(tsr: str, local_tan: str) -> str:
    return ((((("" + "https://www.ebi.ac.uk/ols4/ontologies/ro/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F") + "") + tsr) + "_") + local_tan) + ""


def _arrow277(tsr: str) -> Callable[[str], str]:
    def _arrow276(local_tan: str) -> str:
        return OntobeeDPBOParser(tsr, local_tan)

    return _arrow276


def _arrow279(tsr_1: str) -> Callable[[str], str]:
    def _arrow278(local_tan_1: str) -> str:
        return MSParser(tsr_1, local_tan_1)

    return _arrow278


def _arrow281(tsr_2: str) -> Callable[[str], str]:
    def _arrow280(local_tan_2: str) -> str:
        return POParser(tsr_2, local_tan_2)

    return _arrow280


def _arrow283(tsr_3: str) -> Callable[[str], str]:
    def _arrow282(local_tan_3: str) -> str:
        return ROParser(tsr_3, local_tan_3)

    return _arrow282


def _arrow285(tsr_4: str) -> Callable[[str], str]:
    def _arrow284(local_tan_4: str) -> str:
        return BioregistryParser(tsr_4, local_tan_4)

    return _arrow284


def _arrow287(tsr_5: str) -> Callable[[str], str]:
    def _arrow286(local_tan_5: str) -> str:
        return BioregistryParser(tsr_5, local_tan_5)

    return _arrow286


def _arrow289(tsr_6: str) -> Callable[[str], str]:
    def _arrow288(local_tan_6: str) -> str:
        return BioregistryParser(tsr_6, local_tan_6)

    return _arrow288


def _arrow291(tsr_7: str) -> Callable[[str], str]:
    def _arrow290(local_tan_7: str) -> str:
        return BioregistryParser(tsr_7, local_tan_7)

    return _arrow290


def _arrow293(tsr_8: str) -> Callable[[str], str]:
    def _arrow292(local_tan_8: str) -> str:
        return BioregistryParser(tsr_8, local_tan_8)

    return _arrow292


def _arrow295(tsr_9: str) -> Callable[[str], str]:
    def _arrow294(local_tan_9: str) -> str:
        return BioregistryParser(tsr_9, local_tan_9)

    return _arrow294


def _arrow297(tsr_10: str) -> Callable[[str], str]:
    def _arrow296(local_tan_10: str) -> str:
        return BioregistryParser(tsr_10, local_tan_10)

    return _arrow296


def _arrow299(tsr_11: str) -> Callable[[str], str]:
    def _arrow298(local_tan_11: str) -> str:
        return BioregistryParser(tsr_11, local_tan_11)

    return _arrow298


def _arrow301(tsr_12: str) -> Callable[[str], str]:
    def _arrow300(local_tan_12: str) -> str:
        return BioregistryParser(tsr_12, local_tan_12)

    return _arrow300


def _arrow303(tsr_13: str) -> Callable[[str], str]:
    def _arrow302(local_tan_13: str) -> str:
        return BioregistryParser(tsr_13, local_tan_13)

    return _arrow302


def _arrow305(tsr_14: str) -> Callable[[str], str]:
    def _arrow304(local_tan_14: str) -> str:
        return BioregistryParser(tsr_14, local_tan_14)

    return _arrow304


uri_parser_collection: Any = Dictionary_ofSeq(to_enumerable([("DPBO", _arrow277), ("MS", _arrow279), ("PO", _arrow281), ("RO", _arrow283), ("ENVO", _arrow285), ("CHEBI", _arrow287), ("GO", _arrow289), ("OBI", _arrow291), ("PATO", _arrow293), ("PECO", _arrow295), ("TO", _arrow297), ("UO", _arrow299), ("EFO", _arrow301), ("NCIT", _arrow303), ("OMP", _arrow305)]))

def create_oauri(tsr: str, local_tan: str) -> str:
    match_value: Callable[[str, str], str] | None = Dictionary_tryFind(tsr, uri_parser_collection)
    if match_value is None:
        return OntobeeParser(tsr, local_tan)

    else: 
        return match_value(tsr)(local_tan)



__all__ = ["OntobeeParser", "BioregistryParser", "OntobeeDPBOParser", "MSParser", "POParser", "ROParser", "uri_parser_collection", "create_oauri"]

