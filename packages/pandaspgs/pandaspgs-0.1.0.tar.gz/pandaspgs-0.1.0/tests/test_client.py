from pandaspgs.client import get_data, get_publication, clear_cache, get_ancestry_category
from cachetools import TTLCache

cache = TTLCache(maxsize=1024, ttl=60)


def test_get_data():

    r1 = get_data('https://www.pgscatalog.org/rest/publication/search?pgs_id=PGS000001', cache_impl=cache)
    assert len(r1) == 1
    r2 = get_data('https://www.pgscatalog.org/rest/publication/PGP000001', cache_impl=cache)
    assert len(r2) == 1
    r3 = get_data('https://www.pgscatalog.org/rest/publication/all', cache_impl=cache)
    r3 = get_data('https://www.pgscatalog.org/rest/publication/all', cache_impl=cache)
    assert len(r3) == 455
    r4 = get_data('https://www.pgscatalog.org/rest/publication/all', cache_impl=cache, cached=False)
    assert len(r3) == 455


def test_get_publication():
    r1 = get_publication('https://www.pgscatalog.org/rest/publication/search?pgs_id=PGS000001')
    assert len(r1) == 1
    r2 = get_publication('https://www.pgscatalog.org/rest/publication/PGP000001')
    assert len(r2) == 1
    r3 = get_publication('https://www.pgscatalog.org/rest/publication/all')
    r3 = get_publication('https://www.pgscatalog.org/rest/publication/all')
    clear_cache('Publication')
    r3 = get_publication('https://www.pgscatalog.org/rest/publication/all')
    assert len(r3) == 455
    r4 = get_publication('https://www.pgscatalog.org/rest/publication/all', cached=False)
    assert len(r3) == 455


def test_get_ancestry_category():
    cat = get_ancestry_category('https://www.pgscatalog.org/rest/ancestry_categories')
    assert cat[0]['symbol'] == 'AFR'
