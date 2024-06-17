import numpy as np
from scipy.spatial import ConvexHull
from cifkit.coordination.geometry import compute_polyhedron_metrics


def find_best_polyhedron(max_gaps_per_label, connections):
    """
    Find the best polyhedron for each label based on the minimum
    distance between the reference atom to the avg. position of
    connected atoms.
    """
    best_polyhedrons = {}

    for label, CN_data_per_method in max_gaps_per_label.items():
        # Initialize variables to track the best polyhedron
        min_distance_to_center = float("inf")
        best_polyhedron_metrics = None
        best_method_used = None

        # Loop through each method
        for method, CN_data in CN_data_per_method.items():
            connection_data = connections[label][: CN_data["CN"]]
            polyhedron_points = []

            # Extract the necessary data from connections
            if len(connection_data) > 3:
                for connection in connection_data:
                    polyhedron_points.append(connection[3])
            else:
                continue

            # Only if there are 4 or more points in the polyhedron
            try:
                polyhedron_points.append(connection_data[0][2])
                hull = ConvexHull(polyhedron_points)
                # Add the last point
                polyhedron_metrics = compute_polyhedron_metrics(
                    polyhedron_points, hull
                )
                # Check if the polyhedron has the lowest distance to center.
                if (
                    polyhedron_metrics[
                        "distance_from_avg_point_to_center"
                    ]
                    < min_distance_to_center
                ):
                    min_distance_to_center = polyhedron_metrics[
                        "distance_from_avg_point_to_center"
                    ]
                    best_polyhedron_metrics = polyhedron_metrics
                    best_method_used = method  # Record the method that produced these metrics

            except Exception as e:
                print(
                    f"\nError in determining polyhedron for {label}: {str(e)}\n"
                )
                continue

        if best_polyhedron_metrics:
            best_polyhedron_metrics[
                "method_used"
            ] = best_method_used  # Add method information to the metrics
            best_polyhedrons[label] = best_polyhedron_metrics

    return best_polyhedrons


def get_CN_connections_by_min_dist_method(
    max_gaps_per_label, connections
):
    CN_by_shortest_dist = {}
    for label, methods_info in max_gaps_per_label.items():
        # Access the 'dist_by_shortest_dist' method and get the 'CN' value
        CN_by_shortest_dist[label] = methods_info[
            "dist_by_shortest_dist"
        ]["CN"]

    CN_connections: dict = {}
    # Iterate through each label and number of connections
    for label, CN_value in CN_by_shortest_dist.items():
        if label in connections:
            CN_connections[label] = connections[label][:CN_value]

    return CN_connections
