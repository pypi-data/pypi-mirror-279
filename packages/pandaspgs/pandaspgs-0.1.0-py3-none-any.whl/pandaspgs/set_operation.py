from pandaspgs import Cohort
from pandaspgs.ancestry_category import AncestryCategory
from pandaspgs.performance import PerformanceMetric
from pandaspgs.publication import Publication
from pandaspgs.release import Release
from pandaspgs.sample_set import SampleSet
from pandaspgs.score import Score
from pandaspgs.trait import Trait
from pandaspgs.trait_category import TraitCategory


def bind(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory:
    """
    Binds together PGS objects of the same object. Note that bind() preserves duplicates whereas union() does not.

    Args:
        a: An object of the pandasPGS custom class.
        b: An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import bind


    a = get_cohorts(cohort_symbol='100-plus')
    b = get_cohorts(cohort_symbol='23andMe')
    c = bind(a,b)
    ```

    """
    return a + b


def intersect(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory:
    """
    Returns the data common to both A and B, with no repetitions

    Args:
        a: An object of the pandasPGS custom class.
        b:An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import intersect


    a = get_cohorts(cohort_symbol='100-plus')
    b = get_cohorts(cohort_symbol='23andMe')
    c = intersect(a,b)
    ```

    """
    return a & b


def set_diff(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory:
    """
    returns the data in A that is not in B, with no repetitions

    Args:
        a: An object of the pandasPGS custom class.
        b:An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import set_diff


    a = get_cohorts(cohort_symbol='23andMe')
    b = get_cohorts(cohort_symbol='23andMe')
    c = set_diff(a,b)
    ```

    """
    return a - b


def set_xor(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory:
    """
    returns the data of A and B that are not in their intersection (the symmetric difference), with no repetitions

    Args:
        a: An object of the pandasPGS custom class.
        b:An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import set_xor


    a = get_cohorts(cohort_symbol='100-plus')
    b = get_cohorts(cohort_symbol='23andMe')
    c = set_xor(a,b)
    ```

    """
    return a ^ b


def union(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory:
    """
    returns the combined data from A and B with no repetitions

    Args:
        a: An object of the pandasPGS custom class.
        b:An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import union


    a = get_cohorts(cohort_symbol='100-plus')
    b = get_cohorts(cohort_symbol='23andMe')
    c = union(a,b)
    ```

    """
    return a | b


def set_equal(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> bool:
    """
    Check if the raw data of a and b are equal

    Args:
        a: An object of the pandasPGS custom class.
        b:An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import set_equal


    a = get_cohorts(cohort_symbol='100-plus')
    b = get_cohorts(cohort_symbol='23andMe')
    c = set_equal(a,b)
    ```

    """
    return a == b
