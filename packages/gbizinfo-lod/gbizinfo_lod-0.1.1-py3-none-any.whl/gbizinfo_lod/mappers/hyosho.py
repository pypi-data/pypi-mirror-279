from rdflib import Literal, URIRef

from ..namespace import *
from . import _TripleMapType, bpo
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoHyoshoMapper(GbizInfoKatsudoMapper):
    """表彰情報"""

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        ss = HJ_EXT[f"{row['ID-識別値']}_{row['キー情報']}"]

        triples = GbizInfoKatsudoMapper.map_to_triples(row)
        triples.extend(
            [
                (ss, RDF.type, HJ.表彰型),
            ]
        )
        return triples


__all__ = ["GbizInfoHyoshoMapper"]
