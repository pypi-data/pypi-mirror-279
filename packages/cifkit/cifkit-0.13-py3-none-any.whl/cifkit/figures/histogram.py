"""
Histgoram for supercell size, minimum distances
"""

import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from cifkit.utils import folder, prompt


def plot_histograms(cif_ensemble, output_dir=None) -> None:
    histograms = [
        {
            "data": cif_ensemble.structure_stats,
            "settings": {
                "file_name": "structures.png",
                "title": "Structures Distribution",
                "xlabel": "Structure",
            },
        },
        {
            "data": cif_ensemble.formula_stats,
            "settings": {
                "file_name": "formula.png",
                "title": "Formulas Distribution",
                "xlabel": "Formula",
            },
        },
        {
            "data": cif_ensemble.tag_stats,
            "settings": {
                "file_name": "tag.png",
                "title": "Tags Distribution",
                "xlabel": "Tag",
            },
        },
        {
            "data": cif_ensemble.space_group_number_stats,
            "settings": {
                "file_name": "space_group_number.png",
                "title": "Space Group Numbers Distribution",
                "xlabel": "Space Group Number",
            },
        },
        {
            "data": cif_ensemble.space_group_name_stats,
            "settings": {
                "file_name": "space_group_name.png",
                "title": "Space Group Names Distribution",
                "xlabel": "Space Group Name",
            },
        },
        {
            "data": cif_ensemble.supercell_size_stats,
            "settings": {
                "file_name": "supercell_size.png",
                "title": "Supercell Sizes Distribution",
                "xlabel": "Supercell Size",
            },
        },
        {
            "data": cif_ensemble.unique_CN_values_by_min_dist_method_stat,
            "settings": {
                "file_name": "CN_by_min_dist_method.png",
                "title": "Coordination Numbers Distribution by Min Dist Method",
                "xlabel": "Coordination Number",
            },
        },
        {
            "data": cif_ensemble.unique_CN_values_by_method_methods_stat,
            "settings": {
                "file_name": "CN_by_best_methods.png",
                "title": "Coordination Numbers Distribution by Best Methods",
                "xlabel": "Coordination Number",
            },
        },
        {
            "data": cif_ensemble.min_distance_stats,
            "settings": {
                "file_name": "min_distance.png",
                "title": "Minimum Distances Distribution",
                "xlabel": "Minimum Distance",
                "key_data_type": "float",
            },
        },
        {
            "data": cif_ensemble.site_mixing_type_stats,
            "settings": {
                "file_name": "site_mixing_type.png",
                "title": "Site Mixing Distribution",
                "xlabel": "Site Mixing Type",
            },
        },
        {
            "data": cif_ensemble.unique_elements_stats,
            "settings": {
                "file_name": "elements.png",
                "title": "Unique Elements Distribution",
                "xlabel": "Element",
            },
        },
        {
            "data": cif_ensemble.composition_type_stats,
            "settings": {
                "file_name": "composition_type.png",
                "title": "Unique Composition Types Distribution",
                "xlabel": "Compositions (1: unary, 2: binary, 3: ternary, etc.)",
                "key_data_type": "string",
            },
        },
    ]

    # Make a deafult folder if the output folder is not provided=
    if not output_dir:
        output_dir = folder.make_output_folder(
            cif_ensemble.dir_path, "histograms"
        )

    for histogram in histograms:
        generate_histogram(
            histogram["data"], histogram["settings"], output_dir
        )


def generate_histogram(
    data: dict, settings: dict, output_dir: str
) -> None:
    """
    Generate a histogram from a dictionary of data and save
    it to a specified directory.
    """

    if settings.get("key_data_type") == "string":
        # Assuming all keys can be converted to integers for sorting purposes
        # Sorting is needed for for composition types, order from 1, 2, 3, etc.
        data = {
            str(key): data[key] for key in sorted(data.keys(), key=int)
        }

    if not settings.get("key_data_type") == "float":
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    keys = list(data.keys())
    values = [
        data[key] for key in keys
    ]  # Align values with keys after potential conversion

    plt.figure(figsize=(10, 6))
    plt.bar(
        keys,
        values,
        color=settings.get("color", "blue"),
        edgecolor=settings.get("edgecolor", "black"),
    )
    plt.title(settings["title"])
    plt.xlabel(settings["xlabel"])
    plt.ylabel("Count")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=settings.get("rotation", 45), ha="right")
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.tight_layout()

    # File name
    output_file_path = folder.get_file_path(
        output_dir, settings["file_name"]
    )

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(output_file_path, dpi=300)
    plt.close()
    prompt.log_save_file_message("Histograms", output_file_path)
