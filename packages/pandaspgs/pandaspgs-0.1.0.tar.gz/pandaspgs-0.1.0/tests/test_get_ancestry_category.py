from pandaspgs.get_ancestry_category import get_ancestry_categories


def test_get_ancestry_categories():
    filter_by_id = get_ancestry_categories()
    assert len(filter_by_id) == 11
    assert len(filter_by_id ^ filter_by_id[0]) == 10
    assert len(filter_by_id[range(2)]) == 2
    assert len(filter_by_id[1:3]) == 2
    assert len(filter_by_id["AFR"]) == 1
    assert len(filter_by_id[0] + filter_by_id[1]) == 2
    assert len(filter_by_id - filter_by_id[1]) == 10
    assert len(filter_by_id[0] & filter_by_id) == 1
    assert len(filter_by_id | filter_by_id[0]) == 11
    assert len(filter_by_id[0:4] | filter_by_id[4]) == 5