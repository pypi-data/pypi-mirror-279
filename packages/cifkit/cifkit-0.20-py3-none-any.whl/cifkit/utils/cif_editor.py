from cifkit.utils import cif_parser


def remove_author_loop(file_path: str) -> None:
    """
    Remove the author section from a .cif file to prevent parsing problems
    caused by a wrongly formatted author block.
    """
    (
        start_index,
        end_index,
    ) = cif_parser.get_start_end_line_indexes(
        file_path, "_publ_author_address"
    )

    with open(file_path, "r") as f:
        original_lines = f.readlines()

        # Replace the specific section in original_lines with modified_lines
        original_lines[start_index:end_index] = ["''\n", ";\n", ";\n"]

    with open(file_path, "w") as f:
        f.writelines(original_lines)
