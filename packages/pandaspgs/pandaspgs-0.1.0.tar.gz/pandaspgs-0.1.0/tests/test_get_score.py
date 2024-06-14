
from pandaspgs import get_scores
from pandaspgs import clear_cache


def test_get_scores():
    filter_by_id = get_scores(pgs_id='PGS000001')
    assert len(filter_by_id) == 1
    filter_by_pgp_id = get_scores(pgp_id='PGP000001')
    assert len(filter_by_pgp_id) == 3
    filter_by_pmid = get_scores(pmid=25855707)
    assert len(filter_by_pmid) == 3
    filter_by_trait_id = get_scores(trait_id='EFO_1000649')
    assert len(filter_by_trait_id) == 6
    filter_by_all = get_scores(pgs_id='PGS000002', pgp_id='PGP000001', pmid=25855707, trait_id='EFO_1000649')
    assert len(filter_by_all) == 1
    filter_by_id = get_scores()
    assert len(filter_by_id) == 4650
    assert len(filter_by_id ^ filter_by_id[0]) == 4649
    assert len(filter_by_id[range(2)]) == 2
    assert len(filter_by_id[1:3]) == 2
    assert len(filter_by_id['PGS000001']) == 1
    assert len(filter_by_id[0] + filter_by_id[1]) == 2
    assert len(filter_by_id - filter_by_id[1]) == 4649
    assert len(filter_by_id[0] & filter_by_id) == 1
    assert len(filter_by_id | filter_by_id[0]) == 4650
    assert len(filter_by_id[0:506] | filter_by_id[506]) == 507

