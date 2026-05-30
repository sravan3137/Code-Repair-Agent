from collections import deque

from utils.constants import (
    FORWARD_EDGES_FILE,
    REVERSE_EDGES_FILE
)

from utils.graph_utils import load_json


# -----------------------------------------
# Traverse repository dependency graph safely.
# Supports BFS traversal with depth limits.
# -----------------------------------------

def traverse_dependency_graph(
    symbol_id,
    direction="outgoing",
    depth=1
):

    forward_edges = load_json(
        FORWARD_EDGES_FILE
    )

    reverse_edges = load_json(
        REVERSE_EDGES_FILE
    )


    # -----------------------------------------
    # Track visited graph nodes carefully.
    # Prevent infinite graph traversal loops.
    # -----------------------------------------

    visited = set()

    traversal_result = []

    queue = deque()

    queue.append((symbol_id, 0))

    visited.add(symbol_id)


    # -----------------------------------------
    # Perform BFS traversal over graph.
    # Retrieve neighboring dependency symbols.
    # -----------------------------------------

    while queue:

        current_node, current_depth = (
            queue.popleft()
        )

        if current_depth >= depth:
            continue

        neighbors = []

        if direction == "outgoing":
 
            neighbors = forward_edges.get(
                current_node,
                []
            )

        elif direction == "incoming":

            neighbors = reverse_edges.get(
                current_node,
                []
            )

        elif direction == "both":

            neighbors.extend(
                forward_edges.get(current_node, [])
            )

            neighbors.extend(
                reverse_edges.get(current_node, [])
            )


        # -----------------------------------------
        # Visit neighboring dependency nodes safely.
        # Track traversal depth for propagation.
        # -----------------------------------------

        for neighbor in neighbors:

            if neighbor not in visited:

                visited.add(neighbor)

                traversal_result.append(neighbor)

                queue.append(
                    (neighbor, current_depth + 1)
                )

    return traversal_result