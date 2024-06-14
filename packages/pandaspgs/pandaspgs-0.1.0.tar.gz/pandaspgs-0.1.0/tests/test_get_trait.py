from pandaspgs.get_trait import get_trait_categories
from pandaspgs.get_trait import get_traits
import pytest


def test_get_trait_categories():
    categories = get_trait_categories(mode='Thin')
    categories
    categories = get_trait_categories()
    categories
    assert len(categories) == 17
    assert len(categories[1:3]) == 2
    assert len(categories[range(2)]) == 2
    assert len(categories ^ categories[0]) == 16
    assert len(categories[0] + categories[1]) == 2
    assert len(categories - categories[1]) == 16
    assert len(categories & categories[1]) == 1
    assert len(categories[0] | categories[1]) == 2


def test_get_traits():
    filter_get_trait = get_traits(trait_id='EFO_0000305', mode='Thin')
    filter_get_trait
    filter_get_trait = get_traits(trait_id='EFO_0000305')
    filter_get_trait
    assert len(filter_get_trait) == 1
    assert filter_get_trait.traits.size == 4 * 1
    assert filter_get_trait.trait_categories.size == 2 * 1
    assert filter_get_trait.trait_synonyms.size == 2 * 9
    assert filter_get_trait.associated_pgs_ids.size == 2 * 103
    assert filter_get_trait.child_associated_pgs_ids.size == 2 * 17
    assert filter_get_trait.trait_mapped_terms.size == 2 * 8
    filter_get_trait_a = get_traits(trait_id='EFO_0001645')
    assert len(filter_get_trait_a) == 1
    filter_get_trait_b = get_traits(term='Alzheimer')
    assert len(filter_get_trait_b) == 4
    filter_get_trait_c = get_traits(term='Neurological disorder')
    assert len(filter_get_trait_c) == 102
    filter_get_trait_d = get_traits(trait_id="EFO_0005782", term='Neurological disorder')
    assert len(filter_get_trait_d) == 1
    filter_get_trait_e = get_traits()
    assert len(filter_get_trait_e) == 1180
    filter_get_trait_f = get_traits(term='Alzheimer', exact=False)
    assert len(filter_get_trait_f) == 4
    filter_get_trait_g = get_traits(trait_id="EFO_0005782", term='Neurological disorder', exact=False)
    assert len(filter_get_trait_g) == 1
    assert filter_get_trait[0] == filter_get_trait
    assert filter_get_trait['EFO_0000305'] == filter_get_trait
    assert len(filter_get_trait_c[1:3]) == 2
    assert len(filter_get_trait_c[range(2)]) == 2
    assert filter_get_trait[0] == filter_get_trait['EFO_0000305']
    assert len(filter_get_trait_c ^ filter_get_trait_c[0]) == len(filter_get_trait_c[1:102])
    assert len(filter_get_trait_a + filter_get_trait_c) == 103
    assert len(filter_get_trait_c - filter_get_trait_c[0]) == 101
    assert len(filter_get_trait_c & filter_get_trait_c[0]) == 1
    assert len(filter_get_trait_c | filter_get_trait_a) == 103
    with pytest.raises(Exception):
        get_traits(trait_id='EFO_0000305', exact=False)
