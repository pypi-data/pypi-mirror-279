import pytest
from pandaspgs import *
import os
import shutil
from sqlalchemy import create_engine

home_path = os.path.expanduser('~') + os.sep + 'pandaspgs_home'


def test_read_scoring_file():
    shutil.rmtree(home_path, ignore_errors=True)
    df3 = read_scoring_file(pgs_id='PGS002256')

    df1 = read_scoring_file(pgs_id='PGS000737')
    df2 = read_scoring_file(pgs_id='PGS000737', grch='GRCh38')
    shutil.rmtree(home_path, ignore_errors=True)
    assert df1.size == 3 * 14 and df2.size == 3 * 12
    with pytest.raises(Exception):
        read_scoring_file(pgs_id='PGS000xxxx')


def test_write_to_sql():
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host="localhost", db="pgs", user="root", pw="123456"))
    scores = get_scores()
    scores.scores.to_sql('scores', engine, index=False)
    scores.samples_variants.to_sql('samples_variants', engine, index=False)
    scores.samples_variants_cohorts.to_sql('samples_variants_cohorts', engine, index=False)
    scores.trait_efo.to_sql('trait_efo', engine, index=False)
    scores.samples_training.to_sql('samples_training', engine, index=False)
    scores.samples_training_cohorts.to_sql('samples_training_cohorts', engine, index=False)
    scores.ancestry_distribution.to_sql('ancestry_distribution', engine, index=False)

    cohort = get_cohorts()
    cohort.cohorts.to_sql('cohorts', engine, index=False)
    cohort.associated_pgs_ids.to_sql('associated_pgs_ids', engine, index=False)

    pp = get_performances()
    pp.performance_metrics.to_sql('performance_metrics', engine, index=False)
    pp.samples.to_sql('samples', engine, index=False)
    pp.cohorts.to_sql('cohorts', engine, index=False)
    pp.effect_sizes.to_sql('effect_sizes', engine, index=False)
    pp.class_acc.to_sql('class_acc', engine, index=False)
    pp.othermetrics.to_sql('othermetrics', engine, index=False)

    pub = get_publications()
    pub.publications.to_sql('publications', engine, index=False)
    pub.associated_pgs_ids.to_sql('associated_pgs_ids', engine, index=False)

    rel = get_releases()
    rel.releases.to_sql('releases', engine, index=False)
    rel.released_performance_ids.to_sql('released_performance_ids', engine, index=False)
    rel.released_publication_ids.to_sql('released_publication_ids', engine, index=False)
    rel.released_score_ids.to_sql('released_score_ids', engine, index=False)
    rel.released_new_trait_ids.to_sql('released_new_trait_ids', engine, index=False)

    ss = get_sample_sets()
    ss.sample_sets.to_sql('sample_sets', engine, index=False)
    ss.samples.to_sql('samples', engine, index=False)
    ss.cohorts.to_sql('cohorts', engine, index=False)

    trait = get_traits()
    trait.traits.to_sql('traits', engine, index=False)
    trait.trait_categories.to_sql('trait_categories', engine, index=False)
    trait.trait_synonyms.to_sql('trait_synonyms', engine, index=False)
    trait.trait_mapped_terms.to_sql('trait_mapped_terms', engine, index=False)
    trait.associated_pgs_ids.to_sql('associated_pgs_ids', engine, index=False)
    trait.child_associated_pgs_ids.to_sql('child_associated_pgs_ids', engine, index=False)

    trait_c = get_trait_categories()
    trait_c.efotraits.to_sql('efotraits', engine, index=False)
    trait_c.trait_categories.to_sql('trait_categories', engine, index=False)

    ancestry = get_ancestry_categories()
    ancestry.ancestry_categories.to_sql('ancestry_categories', engine, index=False)
    ancestry.categories.to_sql('categories', engine, index=False)


def test_write_csv():
    shutil.rmtree(home_path + os.sep, ignore_errors=True)
    os.makedirs(home_path, exist_ok=True)
    ancestry = get_ancestry_categories()
    write_csv(home_path + os.sep + 'ancestry', ancestry)
    assert os.path.isfile(home_path + os.sep + 'ancestry' + os.sep + 'ancestry_categories.csv')
    assert os.path.isfile(home_path + os.sep + 'ancestry' + os.sep + 'categories.csv')
    trait_c = get_trait_categories()
    write_csv(home_path + os.sep + 'trait_c', trait_c)
    assert os.path.isfile(home_path + os.sep + 'trait_c' + os.sep + 'trait_categories.csv')
    trait = get_traits()
    write_csv(home_path + os.sep + 'trait', trait)
    assert os.path.isfile(home_path + os.sep + 'trait' + os.sep + 'traits.csv')
    ss = get_sample_sets()
    write_csv(home_path + os.sep + 'ss', ss)
    assert os.path.isfile(home_path + os.sep + 'ss' + os.sep + 'sample_sets.csv')
    rel = get_releases()
    write_csv(home_path + os.sep + 'rel', rel)
    assert os.path.isfile(home_path + os.sep + 'rel' + os.sep + 'releases.csv')
    pub = get_publications()
    write_csv(home_path + os.sep + 'pub', pub)
    assert os.path.isfile(home_path + os.sep + 'pub' + os.sep + 'publications.csv')
    pp = get_performances()
    write_csv(home_path + os.sep + 'pp', pp)
    assert os.path.isfile(home_path + os.sep + 'pp' + os.sep + 'performance_metrics.csv')
    cohort = get_cohorts()
    write_csv(home_path + os.sep + 'cohort', cohort)
    assert os.path.isfile(home_path + os.sep + 'cohort' + os.sep + 'cohorts.csv')
    scores = get_scores()
    write_csv(home_path + os.sep + 'scores', scores)
    assert os.path.isfile(home_path + os.sep + 'scores' + os.sep + 'scores.csv')


def test_write_xlsx():
    shutil.rmtree(home_path + os.sep, ignore_errors=True)
    os.makedirs(home_path, exist_ok=True)
    ancestry = get_ancestry_categories()
    write_xlsx(home_path + os.sep + 'ancestry', ancestry)
    assert os.path.isfile(home_path + os.sep + 'ancestry' + os.sep + 'ancestry_categories.xlsx')
    assert os.path.isfile(home_path + os.sep + 'ancestry' + os.sep + 'categories.xlsx')
    trait_c = get_trait_categories()
    write_xlsx(home_path + os.sep + 'trait_c', trait_c)
    assert os.path.isfile(home_path + os.sep + 'trait_c' + os.sep + 'trait_categories.xlsx')
    trait = get_traits()
    write_xlsx(home_path + os.sep + 'trait', trait)
    assert os.path.isfile(home_path + os.sep + 'trait' + os.sep + 'traits.xlsx')
    ss = get_sample_sets()
    write_xlsx(home_path + os.sep + 'ss', ss)
    assert os.path.isfile(home_path + os.sep + 'ss' + os.sep + 'sample_sets.xlsx')
    rel = get_releases()
    write_xlsx(home_path + os.sep + 'rel', rel)
    assert os.path.isfile(home_path + os.sep + 'rel' + os.sep + 'releases.xlsx')
    pub = get_publications()
    write_xlsx(home_path + os.sep + 'pub', pub)
    assert os.path.isfile(home_path + os.sep + 'pub' + os.sep + 'publications.xlsx')
    pp = get_performances()
    write_xlsx(home_path + os.sep + 'pp', pp)
    assert os.path.isfile(home_path + os.sep + 'pp' + os.sep + 'performance_metrics.xlsx')
    cohort = get_cohorts()
    write_xlsx(home_path + os.sep + 'cohort', cohort)
    assert os.path.isfile(home_path + os.sep + 'cohort' + os.sep + 'cohorts.xlsx')
    scores = get_scores()
    write_xlsx(home_path + os.sep + 'scores', scores)
    assert os.path.isfile(home_path + os.sep + 'scores' + os.sep + 'scores.xlsx')
