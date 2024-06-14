from pandaspgs.client import get_trait_category, get_trait
from pandaspgs.trait import Trait
from pandaspgs.trait_category import TraitCategory


def get_trait_categories(cached: bool = True, mode: str = 'Fat') -> TraitCategory:
    """
    Get TraitCategory data from the server.

    Args:
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A TraitCategory object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_trait_category import get_trait_categories

    ch = get_trait_categories()
    ```
    """
    return TraitCategory(get_trait_category('https://www.pgscatalog.org/rest/trait_category/all', cached), mode)


def get_traits(trait_id: str = None, term: str = None, exact: bool = None, cached: bool = True, mode: str = 'Fat') -> Trait:
    """
    Get Trait data from the server.

    Args:
        trait_id: Ontology ID (e.g. from EFO, HP or MONDO) with the format "EFO_XXXX"
        term: Trait ID, trait name, trait category, trait synonym or external mapped terms/IDs
        exact: Flag to search only the exact term or not
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A Trait object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_trait import get_traits

    ch = get_traits(trait_id='EFO_0000305')
    ```
    """
    if exact is not None:
        if exact:
            num = "1"
        else:
            num = "0"

    if trait_id is None and term is None and exact is None:
        return Trait(
            get_trait('https://www.pgscatalog.org/rest/trait/all?include_child_associated_pgs_ids=1', cached=cached),
            mode)
    elif term is None and exact is not None:
        raise Exception("exact is available only if term is not None")
    elif trait_id is not None:
        by_other = get_trait('https://www.pgscatalog.org/rest/trait/%s?include_children=0' % trait_id, cached=cached)
        if term is None:
            return Trait(by_other, mode)
        else:
            if exact is not None:
                by_pgs_id = get_trait(
                    "https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s&exact=%s" % (term, num),
                    cached=cached)
            else:
                by_pgs_id = get_trait("https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s" % term,
                                      cached=cached)
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
        return Trait(result, mode)
    else:
        if exact is not None:
            return Trait(get_trait(
                "https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s&exact=%s" % (term, num),
                cached=cached), mode)
        else:
            return Trait(get_trait("https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s" % term,
                                   cached=cached), mode)


def get_child_traits(trait_id: str = None, cached: bool =True, mode: str = 'Fat') -> Trait:
    """
    Get children Trait data of the specified Trait ID from the server.

    Args:
        trait_id: Ontology ID (e.g. from EFO, HP or MONDO) with the format "EFO_XXXX"
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A Trait object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_child_trait import get_child_traits

    ch = get_child_traits(trait_id='EFO_0000305')
    ```
    """
    return Trait(get_trait('https://www.pgscatalog.org/rest/trait/%s?include_children=1' % trait_id, cached=cached),
                 mode)



