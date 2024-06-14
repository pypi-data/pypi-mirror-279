from typing import List, Dict
from pandaspgs.client import get_score
from pandas import DataFrame, json_normalize, set_option, Series, concat
from pandaspgs.score import Score


def get_scores(pgs_id: str = None, pgp_id: str = None, pmid: int = None, trait_id: str = None, cached: bool = True,
               mode: str = 'Fat') -> Score:
    """
    Get Score data from the server.

    Args:
        pgs_id: Polygenic Score ID
        pgp_id: PGS Catalog Publication ID (PGP)
        pmid: PubMed ID (without the prefix "PMID:")
        trait_id: Ontology ID (e.g. from EFO, HP or MONDO) with the format "EFO_XXXX"
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A Score object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_score import get_scores

    ch = get_scores(pgs_id='PGS000001')
    ```
    """
    if pgs_id is None and pgp_id is None and pmid is None and trait_id is None:
        return Score(get_score('https://www.pgscatalog.org/rest/score/all', cached=cached), mode)
    by_pgs_id = None
    by_other = None
    if pgs_id is not None:
        by_pgs_id = get_score('https://www.pgscatalog.org/rest/score/%s' % pgs_id, cached=cached)
    if pgp_id is not None or pmid is not None or trait_id is not None:
        query_str = []
        if pgp_id is not None:
            query_str.append('pgp_id=%s' % pgp_id)
        if pmid is not None:
            query_str.append('pmid=%d' % pmid)
        if trait_id is not None:
            query_str.append('trait_id=%s' % trait_id)
        by_other = get_score('https://www.pgscatalog.org/rest/score/search?%s' % '&'.join(query_str))
    if pgs_id is None:
        return Score(by_other, mode)
    if pgp_id is None and pmid is None and trait_id is None:
        return Score(by_pgs_id, mode)
    other_set = set()
    pgs_id_dict = {}
    for single in by_pgs_id:
        pgs_id_dict[single['id']] = single
    pgs_id_set = pgs_id_dict.keys()
    for single in by_other:
        other_set.add(single['id'])
    intersection = pgs_id_set & other_set
    result = []
    for id in intersection:
        result.append(pgs_id_dict[id])
    return Score(result, mode)


