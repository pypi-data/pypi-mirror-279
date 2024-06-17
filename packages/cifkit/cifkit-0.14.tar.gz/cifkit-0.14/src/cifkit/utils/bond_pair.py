from cifkit.utils import formula
from itertools import combinations


def get_heterogenous_element_pairs(
    formula_str: str,
) -> set[tuple[str, str]]:
    """
    Generate all possible unique alphabetically sorted heterogenious pairs.
    """
    elements = formula.get_unique_elements(formula_str)

    # Generate all possible pairs using combinations ensuring uniqueness
    all_pairs = set(combinations(sorted(elements), 2))

    # 'combinations' already sorts them alphabetically, see the test
    return all_pairs


def get_homogenous_element_pairs(
    formula_str: str,
) -> set[tuple[str, str]]:
    """
    Generate all possible sorted homogenous bonding pairs from a formula.
    """
    elements = formula.get_unique_elements(formula_str)
    # Sort the elements alphabetically
    elements.sort()
    homogenous_pairs = [(element, element) for element in elements]
    return set(homogenous_pairs)


def get_all_bond_pairs(formula_str: str) -> set[tuple[str, str]]:
    """
    Generate all possible sorted bond pairs from a formula.
    """
    heterogeneous_bond_pairs = get_heterogenous_element_pairs(
        formula_str
    )
    homogenous_bond_pairs = get_homogenous_element_pairs(formula_str)
    return heterogeneous_bond_pairs.union(homogenous_bond_pairs)
