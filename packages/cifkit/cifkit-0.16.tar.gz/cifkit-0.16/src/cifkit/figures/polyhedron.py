import os
import pyvista as pv
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay


def plot(points, labels, file_path, output_dir=None):
    """
    Generate and save a 3D plot of a molecular structure.
    """
    points = np.array(points)
    plotter = pv.Plotter(off_screen=True)
    central_atom_coord = points[-1]
    central_atom_label = labels[-1]

    for point, label in zip(points, labels):
        radius = (
            0.6 if np.array_equal(point, central_atom_coord) else 0.4
        )  # Central atom larger
        sphere = pv.Sphere(radius=radius, center=point)
        plotter.add_mesh(sphere, color="#D3D3D3")  # Light grey color

    delaunay = Delaunay(points)
    hull = ConvexHull(points)

    edges = set()
    for simplex in delaunay.simplices:
        for i in range(4):
            for j in range(i + 1, 4):
                edge = tuple(sorted([simplex[i], simplex[j]]))
                edges.add(edge)

    hull_edges = set()
    for simplex in hull.simplices:
        for i in range(len(simplex)):
            for j in range(i + 1, len(simplex)):
                hull_edge = tuple(sorted([simplex[i], simplex[j]]))
                hull_edges.add(hull_edge)

    for edge in edges:
        if edge in hull_edges:
            start, end = points[edge[0]], points[edge[1]]
            cylinder = pv.Cylinder(
                center=(start + end) / 2,
                direction=end - start,
                radius=0.05,
                height=np.linalg.norm(end - start),
            )
            plotter.add_mesh(cylinder, color="grey")

    faces = []
    for simplex in hull.simplices:
        faces.append([3] + list(simplex))
    poly_data = pv.PolyData(points, faces)
    plotter.add_mesh(
        poly_data, color="aqua", opacity=0.5, show_edges=True
    )

    # Determine the output directory based on provided path
    if not output_dir:
        output_dir = os.path.join(
            os.path.dirname(file_path), "polyhedrons"
        )

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Use the filename from file_path and append the central atom label
    plot_filename = (
        os.path.basename(file_path).replace(".cif", "")
        + "_"
        + central_atom_label
        + ".png"
    )
    save_path = os.path.join(output_dir, plot_filename)

    # Save the screenshot
    plotter.screenshot(save_path)
