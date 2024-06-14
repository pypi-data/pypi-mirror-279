import os
import sys
import re

import requests
from pandas import DataFrame, read_table, Series
from requests.adapters import HTTPAdapter

from pandaspgs import get_scores, AncestryCategory, Cohort, PerformanceMetric, Publication, Release, SampleSet, Score, \
    Trait, TraitCategory

s = requests.Session()
s.mount('https://', HTTPAdapter(max_retries=5))
home_path = os.path.expanduser('~') + os.sep + 'pandaspgs_home'


def write_csv(path: str,
              o: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> None:
    """
    Create a directory and write the attributes of pandasPGS objects to the corresponding CSV files.

    Args:
        path: The directory that needs to be created.
        o: pandasPGS object.

    Returns:
        None

    ```Python
    from pandaspgs import *
    import os
    home_path = os.path.expanduser('~') + os.sep + 'pandaspgs_home'
    ancestry = get_ancestry_categories()
    write_csv(home_path + os.sep + 'ancestry', ancestry)
    ```

    """
    os.mkdir(path)
    if type(o) is AncestryCategory and o.mode == 'Fat':
        o.ancestry_categories.to_csv(path_or_buf=path + os.sep + 'ancestry_categories.csv', index=False, mode='x')
        o.categories.to_csv(path_or_buf=path + os.sep + 'categories.csv', index=False, mode='x')
    elif type(o) is Cohort and o.mode == 'Fat':
        o.cohorts.to_csv(path_or_buf=path + os.sep + 'cohorts.csv', index=False, mode='x')
        o.associated_pgs_ids.to_csv(path_or_buf=path + os.sep + 'associated_pgs_ids.csv', index=False, mode='x')
    elif type(o) is PerformanceMetric and o.mode == 'Fat':
        o.performance_metrics.to_csv(path_or_buf=path + os.sep + 'performance_metrics.csv', index=False, mode='x')
        o.samples.to_csv(path_or_buf=path + os.sep + 'samples.csv', index=False, mode='x')
        o.cohorts.to_csv(path_or_buf=path + os.sep + 'cohorts.csv', index=False, mode='x')
        o.effect_sizes.to_csv(path_or_buf=path + os.sep + 'effect_sizes.csv', index=False, mode='x')
        o.class_acc.to_csv(path_or_buf=path + os.sep + 'class_acc.csv', index=False, mode='x')
        o.othermetrics.to_csv(path_or_buf=path + os.sep + 'othermetrics.csv', index=False, mode='x')
    elif type(o) is Publication and o.mode == 'Fat':
        o.publications.to_csv(path_or_buf=path + os.sep + 'publications.csv', index=False, mode='x')
        o.associated_pgs_ids.to_csv(path_or_buf=path + os.sep + 'associated_pgs_ids.csv', index=False, mode='x')
    elif type(o) is Release and o.mode == 'Fat':
        o.releases.to_csv(path_or_buf=path + os.sep + 'releases.csv', index=False, mode='x')
        o.released_performance_ids.to_csv(path_or_buf=path + os.sep + 'released_performance_ids.csv', index=False,
                                          mode='x')
        o.released_publication_ids.to_csv(path_or_buf=path + os.sep + 'released_publication_ids.csv', index=False,
                                          mode='x')
        o.released_score_ids.to_csv(path_or_buf=path + os.sep + 'released_score_ids.csv', index=False, mode='x')
        o.released_new_trait_ids.to_csv(path_or_buf=path + os.sep + 'released_new_trait_ids.csv', index=False, mode='x')
    elif type(o) is SampleSet and o.mode == 'Fat':
        o.sample_sets.to_csv(path_or_buf=path + os.sep + 'sample_sets.csv', index=False, mode='x')
        o.samples.to_csv(path_or_buf=path + os.sep + 'samples.csv', index=False, mode='x')
        o.cohorts.to_csv(path_or_buf=path + os.sep + 'cohorts.csv', index=False, mode='x')
    elif type(o) is Score and o.mode == 'Fat':
        o.scores.to_csv(path_or_buf=path + os.sep + 'scores.csv', index=False, mode='x')
        o.samples_variants.to_csv(path_or_buf=path + os.sep + 'samples_variants.csv', index=False, mode='x')
        o.samples_variants_cohorts.to_csv(path_or_buf=path + os.sep + 'samples_variants_cohorts.csv', index=False,
                                          mode='x')
        o.trait_efo.to_csv(path_or_buf=path + os.sep + 'trait_efo.csv', index=False, mode='x')
        o.samples_training.to_csv(path_or_buf=path + os.sep + 'samples_training.csv', index=False, mode='x')
        o.samples_training_cohorts.to_csv(path_or_buf=path + os.sep + 'samples_training_cohorts.csv', index=False,
                                          mode='x')
        o.ancestry_distribution.to_csv(path_or_buf=path + os.sep + 'ancestry_distribution.csv', index=False, mode='x')
    elif type(o) is Trait and o.mode == 'Fat':
        o.traits.to_csv(path_or_buf=path + os.sep + 'traits.csv', index=False, mode='x')
        o.trait_categories.to_csv(path_or_buf=path + os.sep + 'trait_categories.csv', index=False, mode='x')
        o.trait_synonyms.to_csv(path_or_buf=path + os.sep + 'trait_synonyms.csv', index=False, mode='x')
        o.trait_mapped_terms.to_csv(path_or_buf=path + os.sep + 'trait_mapped_terms.csv', index=False, mode='x')
        o.associated_pgs_ids.to_csv(path_or_buf=path + os.sep + 'associated_pgs_ids.csv', index=False, mode='x')
        o.child_associated_pgs_ids.to_csv(path_or_buf=path + os.sep + 'child_associated_pgs_ids.csv', index=False,
                                          mode='x')
    elif type(o) is TraitCategory and o.mode == 'Fat':
        o.efotraits.to_csv(path_or_buf=path + os.sep + 'efotraits.csv', index=False, mode='x')
        o.trait_categories.to_csv(path_or_buf=path + os.sep + 'trait_categories.csv', index=False, mode='x')
    else:
        raise Exception(
            "Failed to convert to CSV files. "
            "Please check whether the type of the input object is supported by pandasPGS, "
            "and check whether the mode attribute of the input object is 'Fat'.")


def write_xlsx(path: str,
                o: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> None:
    """
    Create a directory and write the attributes of pandasPGS objects to the corresponding EXCEL files.

    Args:
        path: The directory that needs to be created.
        o: pandasPGS object.

    Returns:
        None

    ```Python
    from pandaspgs import *
    import os
    home_path = os.path.expanduser('~') + os.sep + 'pandaspgs_home'
    ancestry = get_ancestry_categories()
    write_xlsx(home_path + os.sep + 'ancestry', ancestry)
    ```

    """
    os.mkdir(path)
    if type(o) is AncestryCategory and o.mode == 'Fat':
        o.ancestry_categories.to_excel(path + os.sep + 'ancestry_categories.xlsx', index=False)
        o.categories.to_excel(path + os.sep + 'categories.xlsx', index=False)
    elif type(o) is Cohort and o.mode == 'Fat':
        o.cohorts.to_excel(path + os.sep + 'cohorts.xlsx', index=False)
        o.associated_pgs_ids.to_excel(path + os.sep + 'associated_pgs_ids.xlsx', index=False)
    elif type(o) is PerformanceMetric and o.mode == 'Fat':
        o.performance_metrics.to_excel(path + os.sep + 'performance_metrics.xlsx', index=False)
        o.samples.to_excel(path + os.sep + 'samples.xlsx', index=False)
        o.cohorts.to_excel(path + os.sep + 'cohorts.xlsx', index=False)
        o.effect_sizes.to_excel(path + os.sep + 'effect_sizes.xlsx', index=False)
        o.class_acc.to_excel(path + os.sep + 'class_acc.xlsx', index=False)
        o.othermetrics.to_excel(path + os.sep + 'othermetrics.xlsx', index=False)
    elif type(o) is Publication and o.mode == 'Fat':
        o.publications.to_excel(path + os.sep + 'publications.xlsx', index=False)
        o.associated_pgs_ids.to_excel(path + os.sep + 'associated_pgs_ids.xlsx', index=False)
    elif type(o) is Release and o.mode == 'Fat':
        o.releases.to_excel(path + os.sep + 'releases.xlsx', index=False)
        o.released_performance_ids.to_excel(path + os.sep + 'released_performance_ids.xlsx', index=False)
        o.released_publication_ids.to_excel(path + os.sep + 'released_publication_ids.xlsx', index=False)
        o.released_score_ids.to_excel(path + os.sep + 'released_score_ids.xlsx', index=False)
        o.released_new_trait_ids.to_excel(path + os.sep + 'released_new_trait_ids.xlsx', index=False)
    elif type(o) is SampleSet and o.mode == 'Fat':
        o.sample_sets.to_excel(path + os.sep + 'sample_sets.xlsx', index=False)
        o.samples.to_excel(path + os.sep + 'samples.xlsx', index=False)
        o.cohorts.to_excel(path + os.sep + 'cohorts.xlsx', index=False)
    elif type(o) is Score and o.mode == 'Fat':
        o.scores.to_excel(path + os.sep + 'scores.xlsx', index=False)
        o.samples_variants.to_excel(path + os.sep + 'samples_variants.xlsx', index=False)
        o.samples_variants_cohorts.to_excel(path + os.sep + 'samples_variants_cohorts.xlsx', index=False)
        o.trait_efo.to_excel(path + os.sep + 'trait_efo.xlsx', index=False)
        o.samples_training.to_excel(path + os.sep + 'samples_training.xlsx', index=False)
        o.samples_training_cohorts.to_excel(path + os.sep + 'samples_training_cohorts.xlsx', index=False)
        o.ancestry_distribution.to_excel(path + os.sep + 'ancestry_distribution.xlsx', index=False)
    elif type(o) is Trait and o.mode == 'Fat':
        o.traits.to_excel(path + os.sep + 'traits.xlsx', index=False)
        o.trait_categories.to_excel(path + os.sep + 'trait_categories.xlsx', index=False)
        o.trait_synonyms.to_excel(path + os.sep + 'trait_synonyms.xlsx', index=False)
        o.trait_mapped_terms.to_excel(path + os.sep + 'trait_mapped_terms.xlsx', index=False)
        o.associated_pgs_ids.to_excel(path + os.sep + 'associated_pgs_ids.xlsx', index=False)
        o.child_associated_pgs_ids.to_excel(path + os.sep + 'child_associated_pgs_ids.xlsx', index=False)
    elif type(o) is TraitCategory and o.mode == 'Fat':
        o.efotraits.to_excel(path + os.sep + 'efotraits.xlsx', index=False)
        o.trait_categories.to_excel(path + os.sep + 'trait_categories.xlsx', index=False)
    else:
        raise Exception(
            "Failed to convert to EXCEL files. "
            "Please check whether the type of the input object is supported by pandasPGS, "
            "and check whether the mode attribute of the input object is 'Fat'.")


def read_scoring_file(pgs_id: str = None, grch: str = 'GRCh37') -> DataFrame:
    """
    Download a scoring file and convert it to a DataFrame. The directory of the downloaded file is $HOME/pandaspgs_home.

    Args:
        pgs_id: Polygenic Score ID.
        grch: GRCh37 or GRCh38.

    Returns:
        A DataFrame.

    ```Python
    from pandaspgs import read_scoring_file

    df = read_scoring_file(pgs_id='PGS000737')
    ```
    """
    if pgs_id is None:
        raise Exception("pgs_id can't be None.")
    raw_score_data = get_scores(pgs_id=pgs_id).raw_data
    if len(raw_score_data) != 1:
        raise Exception("Unable to find the link to download. Please check the pgs_id.")
    url = raw_score_data[0]['ftp_harmonized_scoring_files'][grch]['positions']
    match_obj = re.match('.*/(.*)', url)
    file_name = match_obj.group(1)
    os.makedirs(home_path, exist_ok=True)

    with s.get(url, timeout=60, stream=True) as r:
        online_size = r.headers.get('content-length', 0)
        local_size = 0
        if os.path.exists(home_path + os.sep + file_name):
            local_size = os.path.getsize(home_path + os.sep + file_name)
        if local_size > 0 and (int(online_size) == local_size):
            sys.stdout.write('[SKIP]: %s has been downloaded in %s\n' % (file_name, home_path))
        else:
            r.raise_for_status()
            with open(home_path + os.sep + file_name, 'wb') as f:
                i = 0
                for chunk in r.iter_content(chunk_size=1024):
                    i += 1024
                    sys.stdout.write('%s downloading: %.2f MB\r' % (file_name, i / 1024 / 1024))
                    f.write(chunk)
            sys.stdout.write('%s(%.2f MB) has been downloaded in %s\n' % (file_name, i / 1024 / 1024, home_path))

    df = read_table(home_path + os.sep + file_name, comment='#', compression='gzip')
    return df


def genotype_weighted_score(s: Series) -> DataFrame:
    genotype = [s['effect_allele'] + '/' + s['effect_allele'], s['effect_allele'] + '/' + s['other_allele'],
                s['other_allele'] + '/' + s['other_allele']]
    weighted_score = [2 * s['effect_weight'], 1 * s['effect_weight'], 0 * s['effect_weight']]
    data = {s['rsID'] + "_genotype": genotype, s['rsID'] + "_weighted_score": weighted_score}
    return DataFrame(data=data)
