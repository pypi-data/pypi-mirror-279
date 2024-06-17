from cifkit.utils import cif_parser
from cifkit.utils.error_messages import OccupancyError


def get_coord_occupancy_sum(loop_values):
    """
    Calculate sum of occupancies for each set of coordinates
    """
    num_atom_labels = cif_parser.get_unique_label_count(loop_values)
    # Check for full occupancy
    coord_occupancy_sum = {}

    for i in range(num_atom_labels):
        (
            _,
            occupancy,
            coordinates,
        ) = cif_parser.get_label_occupancy_coordinates(loop_values, i)
        occupancy_num = (
            coord_occupancy_sum.get(coordinates, 0) + occupancy
        )
        coord_occupancy_sum[coordinates] = occupancy_num

    return coord_occupancy_sum


def get_site_mixing_type(cif_loop_values) -> str:
    """
    Get file-level atomic site mixing info for a given set of CIF loop values.
    """
    is_full_occupancy = True
    coord_occupancy_sum = get_coord_occupancy_sum(cif_loop_values)

    # Now check summed occupancies
    for _, occupancy_sum in coord_occupancy_sum.items():
        if occupancy_sum != 1:
            is_full_occupancy = False

    # Check for atomic mixing
    num_atom_labels = len(cif_loop_values[0])
    is_atomic_mixing = len(coord_occupancy_sum) != num_atom_labels

    if is_atomic_mixing and not is_full_occupancy:
        return "deficiency_atomic_mixing"

    elif is_atomic_mixing and is_full_occupancy:
        return "full_occupancy_atomic_mixing"

    elif not is_atomic_mixing and not is_full_occupancy:
        return "deficiency_no_atomic_mixing"

    elif is_full_occupancy:
        return "full_occupancy"
    else:
        raise ValueError(OccupancyError.INVALID_MIXING_TYPE.value)
