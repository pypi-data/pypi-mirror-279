from pandaspgs.client import get_sample_set
from pandaspgs.sample_set import SampleSet


def get_sample_sets(pss_id: str = None, pgs_id: str = None, pgp_id: str = None, pmid: int = None, cached: bool = True,
                    mode: str = 'Fat') \
        -> SampleSet:
    """
    Get SampleSet data from the server.

    Args:
        pss_id: PGS Sample Set ID (PSS)
        pgs_id: Polygenic Score ID (PGS)
        pgp_id: PGS Catalog Publication ID (PGP)
        pmid:PubMed ID (without the prefix "PMID:")
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A SampleSet object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_sample_set import get_sample_sets

    ch = get_sample_sets(pss_id='PSS000001')
    ```
    """
    if pss_id is None and pgs_id is None and pgp_id is None and pmid is None:
        return SampleSet(get_sample_set('https://www.pgscatalog.org/rest/sample_set/all', cached=cached), mode)
    by_id = None
    by_other = None
    if pss_id is not None:
        by_id = get_sample_set('https://www.pgscatalog.org/rest/sample_set/%s' % pss_id, cached=cached)
    if pgs_id is not None or pmid is not None or pgp_id is not None:
        query_str = []
        if pgs_id is not None:
            query_str.append('pgs_id=%s' % pgs_id)
        if pmid is not None:
            query_str.append('pmid=%d' % pmid)
        if pgp_id is not None:
            query_str.append('pgp_id=%s' % pgp_id)
        by_other = get_sample_set('https://www.pgscatalog.org/rest/sample_set/search?%s' % '&'.join(query_str), cached=cached)
    if pss_id is None:
        return SampleSet(by_other, mode)
    if pgs_id is None and pmid is None and pgp_id is None:
        return SampleSet(by_id, mode)
    other_set = set()
    id_dict = {}
    for single in by_id:
        id_dict[single['id']] = single
    ppm_id_set = id_dict.keys()
    for single in by_other:
        other_set.add(single['id'])
    intersection = ppm_id_set & other_set
    result = []
    for id in intersection:
        result.append(id_dict[id])
    return SampleSet(result, mode)


