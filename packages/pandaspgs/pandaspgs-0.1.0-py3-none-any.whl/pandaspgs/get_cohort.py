from pandaspgs.client import get_cohort
from pandaspgs.cohort import Cohort


def get_cohorts(cohort_symbol: str = None, cached: bool= True, mode: str = 'Fat') -> Cohort:
    """
    Get Cohort data from the server.

    Args:
        cohort_symbol: Short name of a cohort
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A Cohort object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_cohort import get_cohorts

    ch = get_cohorts(cohort_symbol='ABCFS')
    ```
    """
    if cohort_symbol is None:
        return Cohort(get_cohort('https://www.pgscatalog.org/rest/cohort/all', cached=cached), mode)
    by_id = None
    if cohort_symbol is not None:
        by_id = get_cohort('https://www.pgscatalog.org/rest/cohort/%s' % cohort_symbol, cached=cached)
    return Cohort(by_id, mode)
