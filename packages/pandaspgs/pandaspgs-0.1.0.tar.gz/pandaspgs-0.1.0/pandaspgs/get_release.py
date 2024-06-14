from typing import List, Dict
from pandaspgs.client import get_release
from pandaspgs.release import Release
import re


def get_releases(date: str = 'all', cached: bool = True, mode: str = 'Fat') -> Release:
    """
    Get Release data from the server.

    Args:
        date: PGS Catalog release date (format YYYY-MM-DD) or 'latest' or 'all'
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.


    Returns:
        A Release object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_release import get_releases

    ch = get_releases(date="2024-01-26")
    ```
    """
    if date == 'all':
        return Release(get_release('https://www.pgscatalog.org/rest/release/all', cached=cached), mode)
    if date == 'latest':
        return Release(get_release('https://www.pgscatalog.org/rest/release/current', cached=cached), mode)
    if date is None:
        raise Exception("Date can't be None.")
    if re.match('\\d{4}-\\d{2}-\\d{2}$', date) is None:
        raise Exception('The format of the date must be YYYY-MM-DD.')
    return Release(get_release('https://www.pgscatalog.org/rest/release/%s' % date, cached=cached), mode)



