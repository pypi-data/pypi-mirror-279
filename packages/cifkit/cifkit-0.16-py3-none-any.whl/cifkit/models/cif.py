"""
Import statements placed bottom to avoid cluttering.
"""

# Polyhedron
from cifkit.figures import polyhedron
from cifkit.utils.unit import round_dict_values

# Parser .cif file
from cifkit.utils.cif_parser import (
    get_cif_block,
    get_loop_values,
    get_unitcell_lengths,
    get_unitcell_angles_rad,
    get_unique_site_labels,
    get_unique_elements_from_loop,
    get_formula_structure_weight_s_group,
    get_tag_from_third_line,
    parse_atom_site_occupancy_info,
    check_unique_atom_site_labels,
)

# Edit .cif file
from cifkit.preprocessors.format import (
    preprocess_label_element_loop_values,
)
from cifkit.utils.cif_editor import remove_author_loop

# Supercell generation
from cifkit.preprocessors.supercell import get_supercell_points
from cifkit.preprocessors.supercell_util import get_cell_atom_count
from cifkit.preprocessors.environment import (
    get_site_connections,
)


# Radius
from cifkit.data.radius_handler import (
    get_is_radius_data_available,
    get_radius_values_per_element,
    compute_radius_sum,
)

# Coordination number
from cifkit.preprocessors.environment_util import flat_site_connections
from cifkit.coordination.composition import (
    get_bond_counts,
    get_bond_fractions,
    compute_avg_CN,
    get_unique_CN_values,
)
from cifkit.coordination.method import compute_CN_max_gap_per_site
from cifkit.coordination.filter import (
    find_best_polyhedron,
    get_CN_connections_by_min_dist_method,
)

from cifkit.coordination.connection import (
    get_CN_connections_by_best_methods,
)

# Bond pair
from cifkit.coordination.bond_distance import (
    get_shortest_distance_per_bond_pair,
)

# Site info
from cifkit.coordination.site_distance import (
    get_shortest_distance,
    get_shortest_distance_per_site,
)
from cifkit.coordination.geometry import (
    get_polyhedron_coordinates_labels,
)

from cifkit.utils.bond_pair import (
    get_heterogenous_element_pairs,
    get_homogenous_element_pairs,
    get_all_bond_pairs,
)

from cifkit.occupacny.mixing import get_site_mixing_type


def ensure_connections(func):
    """For accessing lazy properties and methods, compute connections."""

    def wrapper(self, *args, **kwargs):
        if self.connections is None:
            self.compute_connections()
        return func(self, *args, **kwargs)

    return wrapper


class Cif:
    def __init__(self, file_path: str) -> None:
        """Initialize the Cif object with the file path."""
        self.file_path = file_path
        self.connections = (
            None  # Private attribute to store connections
        )
        self._shortest_pair_distance = None
        self._preprocess()
        self._load_data()

    def _preprocess(self):
        """Preprocess each .cif file and check any error."""
        check_unique_atom_site_labels(self.file_path)
        remove_author_loop(self.file_path)
        preprocess_label_element_loop_values(self.file_path)

    def _load_data(self):
        """Load data from the .cif file and process it."""

        self._block = get_cif_block(self.file_path)
        self._parse_cif_data()
        self._generate_supercell()

    def _parse_cif_data(self):
        """Parse the main CIF data from the block."""
        self._loop_values = get_loop_values(self._block)
        self.unitcell_lengths = get_unitcell_lengths(self._block)
        self.unitcell_angles = get_unitcell_angles_rad(self._block)
        self.site_labels = get_unique_site_labels(self._loop_values)
        self.unique_elements = get_unique_elements_from_loop(
            self._loop_values
        )
        (
            self.formula,
            self.structure,
            self.weight,
            self.space_group_number,
            self.space_group_name,
        ) = get_formula_structure_weight_s_group(self._block)
        self.composition_type = len(self.unique_elements)
        self.tag = get_tag_from_third_line(self.file_path)
        self.atom_site_info = parse_atom_site_occupancy_info(
            self.file_path
        )
        self.heterogeneous_bond_pairs = get_heterogenous_element_pairs(
            self.formula
        )
        self.homogenous_bond_pairs = get_homogenous_element_pairs(
            self.formula
        )
        self.all_bond_pairs = get_all_bond_pairs(self.formula)
        self.site_mixing_type = get_site_mixing_type(self._loop_values)
        self.is_radius_data_available = get_is_radius_data_available(
            self.unique_elements
        )

    def _generate_supercell(self):
        """Generate supercell information based on the unit cell data."""
        self.unitcell_points = get_supercell_points(self._block, 1)
        self.supercell_points = get_supercell_points(self._block, 3)
        self.unitcell_atom_count = get_cell_atom_count(
            self.unitcell_points
        )
        self.supercell_atom_count = get_cell_atom_count(
            self.supercell_points
        )

    """
    Coordination number util
    """

    def compute_connections(self, cutoff_radius=10.0):
        """Compute nearest neighbor connections per site label."""
        self.connections = get_site_connections(
            [
                self.site_labels,
                self.unitcell_lengths,
                self.unitcell_angles,
            ],
            self.unitcell_points,
            self.supercell_points,
            cutoff_radius=cutoff_radius,
        )

        # Flattened coordinations
        self._connections_flattened = flat_site_connections(
            self.connections
        )

        # Shortest distance
        self._shortest_distance = get_shortest_distance(
            self.connections
        )

        # Shortest distance per bond pair
        self._shortest_bond_pair_distance = (
            get_shortest_distance_per_bond_pair(
                self.connections_flattened
            )
        )

        # Shortest distance per site
        self._shortest_site_pair_distance = (
            get_shortest_distance_per_site(self.connections)
        )

        # Parse individual radii per element
        self._radius_values = round_dict_values(
            get_radius_values_per_element(
                self.unique_elements, self.shortest_bond_pair_distance
            )
        )
        self._radius_sum = compute_radius_sum(self.radius_values)

        # CN max gap per site
        self._CN_max_gap_per_site = compute_CN_max_gap_per_site(
            self.radius_sum, self.connections, self.site_mixing_type
        )

        # Find the best methods
        self._CN_best_methods = find_best_polyhedron(
            self.CN_max_gap_per_site, self.connections
        )

        # Get CN connections by the best methods
        self._CN_connections_by_best_methods = (
            get_CN_connections_by_best_methods(
                self.CN_best_methods, self.connections
            )
        )

        # Get CN connections by the best methods
        self._CN_connections_by_min_dist_method = (
            get_CN_connections_by_min_dist_method(
                self.CN_max_gap_per_site, self.connections
            )
        )
        # Bond counts
        self._CN_bond_count_by_min_dist_method = get_bond_counts(
            self.formula, self.CN_connections_by_min_dist_method
        )
        self._CN_bond_count_by_best_methods = get_bond_counts(
            self.formula, self.CN_connections_by_best_methods
        )
        # Bond fractions
        self._CN_bond_fractions_by_min_dist_method = (
            get_bond_fractions(self.CN_bond_count_by_min_dist_method)
        )
        self._CN_bond_fractions_by_best_methods = get_bond_fractions(
            self.CN_bond_count_by_best_methods
        )
        # Unique CN
        self._CN_unique_values_by_min_dist_method = (
            get_unique_CN_values(
                self.CN_connections_by_min_dist_method
            )
        )
        self._CN_unique_values_by_best_methods = get_unique_CN_values(
            self.CN_connections_by_best_methods
        )

        # Avg CN
        self._CN_avg_by_min_dist_method = compute_avg_CN(
            self.CN_connections_by_min_dist_method
        )

        self._CN_avg_by_best_methods = compute_avg_CN(
            self.CN_connections_by_best_methods
        )

        # Max CN
        self._CN_max_by_min_dist_method = max(
            self.CN_unique_values_by_min_dist_method
        )
        self._CN_max_by_best_methods = max(
            self.CN_unique_values_by_best_methods
        )
        # Min CN
        self._CN_min_by_min_dist_method = min(
            self.CN_unique_values_by_min_dist_method
        )
        self._CN_min_by_best_methods = min(
            self.CN_unique_values_by_best_methods
        )

    @property
    @ensure_connections
    def shortest_distance(self):
        """Property that checks if connections are computed and computes."""
        return self._shortest_distance

    @property
    @ensure_connections
    def connections_flattened(self):
        return self._connections_flattened

    @property
    @ensure_connections
    def shortest_bond_pair_distance(self):
        return self._shortest_bond_pair_distance

    @property
    @ensure_connections
    def shortest_site_pair_distance(self):
        return self._shortest_site_pair_distance

    @property
    @ensure_connections
    def radius_values(self):
        return self._radius_values

    @property
    @ensure_connections
    def radius_sum(self):
        return self._radius_sum

    @property
    @ensure_connections
    def CN_max_gap_per_site(self):
        return self._CN_max_gap_per_site

    @property
    @ensure_connections
    def CN_best_methods(self):
        return self._CN_best_methods

    @property
    @ensure_connections
    def CN_connections_by_best_methods(self):
        return self._CN_connections_by_best_methods

    @property
    @ensure_connections
    def CN_connections_by_min_dist_method(self):
        return self._CN_connections_by_min_dist_method

    """
    Compute avg, min, max, unique for best and min_dist method
    """

    # Bond counts
    @property
    @ensure_connections
    def CN_bond_count_by_min_dist_method(self):
        return self._CN_bond_count_by_min_dist_method

    @property
    @ensure_connections
    def CN_bond_count_by_best_methods(self):
        return self._CN_bond_count_by_best_methods

    # Bond fractions
    @property
    @ensure_connections
    def CN_bond_fractions_by_min_dist_method(self):
        return self._CN_bond_fractions_by_min_dist_method

    @property
    @ensure_connections
    def CN_bond_fractions_by_best_methods(self):
        return self._CN_bond_fractions_by_best_methods

    # Unique CN
    @property
    @ensure_connections
    def CN_unique_values_by_min_dist_method(self):
        return self._CN_unique_values_by_min_dist_method

    @property
    @ensure_connections
    def CN_unique_values_by_best_methods(self):
        return self._CN_unique_values_by_best_methods

    # Average CN
    @property
    @ensure_connections
    def CN_avg_by_min_dist_method(self):
        return self._CN_avg_by_min_dist_method

    @property
    @ensure_connections
    def CN_avg_by_best_methods(self):
        return self._CN_avg_by_best_methods

    @property
    @ensure_connections
    def CN_max_by_min_dist_method(self):
        return self._CN_max_by_min_dist_method

    @property
    @ensure_connections
    def CN_max_by_best_methods(self):
        return self._CN_max_by_best_methods

    @property
    @ensure_connections
    def CN_min_by_min_dist_method(self):
        return self._CN_min_by_min_dist_method

    @property
    @ensure_connections
    def CN_min_by_best_methods(self):
        return self._CN_min_by_best_methods

    @ensure_connections
    def get_polyhedron_labels_by_CN_min_dist_method(
        self, label: str
    ) -> tuple[list[list[float]], list[str]]:
        return get_polyhedron_coordinates_labels(
            self.CN_connections_by_min_dist_method, label
        )

    @ensure_connections
    def get_polyhedron_labels_by_CN_best_methods(
        self, label: str
    ) -> tuple[list[list[float]], list[str]]:
        return get_polyhedron_coordinates_labels(
            self.CN_connections_by_best_methods, label
        )

    @ensure_connections
    def plot_polyhedron(self, site_label, output_dir=None):
        coords, labels = get_polyhedron_coordinates_labels(
            self.CN_connections_by_min_dist_method, site_label
        )
        polyhedron.plot(coords, labels, self.file_path, output_dir)
