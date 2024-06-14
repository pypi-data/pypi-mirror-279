from pandaspgs.client import get_publication
from pandaspgs.publication import Publication


def get_publications(pgs_id: str = None, pgp_id: str = None, pmid: int = None, author: str = None, cached: bool = True,
                     mode: str = 'Fat') -> Publication:
    """
    Get Publication data from the server.

    Args:
        pgs_id: PGS Publication ID (PGP)
        pgp_id: Polygenic Score ID (PGS)
        pmid: PubMed ID (without the prefix "PMID:")
        author: Publication author (any author in the list of authors in a publication)
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A Publication object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_publication import get_publications

    ch = get_publications(pgp_id='PGP000003')
    ```
    """
    if pgs_id is None and pgp_id is None and pmid is None and author is None:
        return Publication(get_publication('https://www.pgscatalog.org/rest/publication/all', cached=cached), mode)
    by_id = None
    by_other = None
    if pgp_id is not None:
        by_id = get_publication('https://www.pgscatalog.org/rest/publication/%s' % pgp_id, cached=cached)
    if pgs_id is not None or pmid is not None or author is not None:
        query_str = []
        if pgs_id is not None:
            query_str.append('pgs_id=%s' % pgs_id)
        if pmid is not None:
            query_str.append('pmid=%d' % pmid)
        if author is not None:
            query_str.append('author=%s' % author)
        by_other = get_publication('https://www.pgscatalog.org/rest/publication/search?%s' % '&'.join(query_str))
    if pgp_id is None:
        return Publication(by_other, mode)
    if pgs_id is None and pmid is None and author is None:
        return Publication(by_id, mode)
    other_set = set()
    id_dict = {}
    for single in by_id:
        id_dict[single['id']] = single
    pgp_id_set = id_dict.keys()
    for single in by_other:
        other_set.add(single['id'])
    intersection = pgp_id_set & other_set
    result = []
    for id in intersection:
        result.append(id_dict[id])
    return Publication(result, mode)






