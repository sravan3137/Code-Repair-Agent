# -----------------------------------------
# Store graph file locations.
# These files persist repository metadata.
# -----------------------------------------

GRAPH_DIR = "graph_data"


# -----------------------------------------
# Symbol table stores canonical symbol IDs.
# Forward edges store outgoing calls.
# -----------------------------------------

SYMBOL_TABLE_FILE = f"{GRAPH_DIR}/symbol_table.json"

FORWARD_EDGES_FILE = f"{GRAPH_DIR}/forward_edges.json"


# -----------------------------------------
# Reverse edges store incoming calls.
# Symbol-to-file maps symbols to files.
# -----------------------------------------

REVERSE_EDGES_FILE = f"{GRAPH_DIR}/reverse_edges.json"

SYMBOL_TO_FILE_FILE = f"{GRAPH_DIR}/symbol_to_file.json"

