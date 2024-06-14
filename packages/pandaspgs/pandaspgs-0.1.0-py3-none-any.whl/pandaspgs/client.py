import requests
import json
import progressbar
from typing import List, Dict
from requests.adapters import HTTPAdapter
from cachetools import TTLCache

fields = ['Score', 'Publication', 'Trait', 'Trait_category', 'Performance', 'Cohort', 'Sample_set', 'Release',
          'Ancestry_category']
fields_and_all = ['All', 'Score', 'Publication', 'Trait', 'Trait_category', 'Performance', 'Cohort', 'Sample_set',
                  'Release', 'Ancestry_category']
publication_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
score_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
trait_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
trait_category_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
performance_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
cohort_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
sample_set_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
release_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)
ancestry_category_cache = TTLCache(maxsize=1024*1024, ttl=60 * 60 * 24)


def get_ancestry_category(url: str, cached=True) -> List[Dict]:
    raw_dict = get_data(url, cache_impl=ancestry_category_cache, cached=cached)[0]
    dict_list = []
    for key in raw_dict:
        raw_dict[key]['symbols'] = key
        dict_list.append(raw_dict[key])
    return dict_list


def get_publication(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=publication_cache, cached=cached)


def get_score(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=score_cache, cached=cached)


def get_trait(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=trait_cache, cached=cached)


def get_trait_category(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=trait_category_cache, cached=cached)


def get_performance(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=performance_cache, cached=cached)


def get_cohort(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=cohort_cache, cached=cached)


def get_sample_set(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=sample_set_cache, cached=cached)


def get_release(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=release_cache, cached=cached)


def clear_cache(field: str = 'All') -> None:
    """
    Clear some or all of the cache.

    Args:
        field: It can be one of the following: 'All', 'Score', 'Publication', 'Trait', 'Trait_category', 'Performance', 'Cohort', 'Sample_set', 'Release', 'Ancestry_category'

    Returns:
        None

    ```Python
    from pandaspgs.get_publication import get_publications
    from pandaspgs.client import clear_cache

    # Clear all caches.
    clear_cache('All')
    pub = get_publications()
    # Clear the cache used by get_publications()
    clear_cache('Publication')
    pub = get_publications()
    ```

    """
    if field not in fields_and_all:
        raise Exception('The field must one of %s' % str(fields_and_all))
    if field == 'All':
        for s in fields:
            eval(s.lower() + '_cache.clear()')
    else:
        eval(field.lower() + '_cache.clear()')


def get_data(url: str, cache_impl=None, cached=True) -> List[Dict]:
    with requests.Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=5))
        if url in cache_impl and cached:
            r = cache_impl[url]
        else:
            r = s.get(url)
        if r.status_code == 200:
            if len(json.loads(r.text)) == 0:
                return []
            cache_impl[url] = r
            parsed_data = json.loads(r.text)
            if parsed_data.get('results') is not None:
                results_list = parsed_data.get('results')
                if parsed_data.get('next') is not None:
                    bar = progressbar.ProgressBar(max_value=parsed_data.get('count')).start()
                    progress = 50
                    bar.update(progress)
                    next_url = parsed_data.get('next')
                    while next_url is not None:
                        if next_url in cache_impl and cached:
                            r = cache_impl[next_url]
                        else:
                            r = s.get(next_url)
                            if r.status_code == 200:
                                cache_impl[next_url] = r
                            elif r.status_code == 404:
                                return []
                            else:
                                raise Exception('The request for %s failed: response code was %d, content was \n%s' % (next_url, r.status_code, r.text))
                        parsed_data = json.loads(r.text)
                        results_list.extend(parsed_data.get('results'))
                        progress = progress + parsed_data.get('size')
                        bar.update(progress)
                        next_url = parsed_data.get('next')
                    bar.finish()
                return results_list
            else:
                return [parsed_data]
        elif r.status_code == 404:
            return []
        else:
            raise Exception('The request for %s failed: response code was %d, content was \n%s' % (url, r.status_code, r.text))


def ask_yes_no_question(question: str) -> str:
    yes_no_answer = ""
    while yes_no_answer != "YES" and yes_no_answer != "NO":
        yes_no_answer = input(question).upper()
    return yes_no_answer
