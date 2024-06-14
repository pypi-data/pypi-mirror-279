from pandaspgs.client import get_ancestry_category
from pandaspgs.ancestry_category import AncestryCategory


def get_ancestry_categories(cached: bool = True, mode: str = 'Fat') -> AncestryCategory:
    """
    Get AncestryCategory data from the server.

    Args:
        cached: Whether or not to try to get data from the cache.
        mode: Fat or Thin. Specifies the mode of the returned object.

    Returns:
        A AncestryCategory object. Attributes of type DataFrame have hierarchical dependencies.

    ```Python
    from pandaspgs.get_ancestry_category import get_ancestry_categories

    ch = get_ancestry_categories()
    ```
    """
    return AncestryCategory(get_ancestry_category('https://www.pgscatalog.org/rest/ancestry_categories/',
                                                  cached=cached), mode)


