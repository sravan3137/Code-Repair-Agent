import javalang

from utils.ast_utils import (
    build_symbol_id,
    extract_method_calls
)

from utils.constants import (
    FORWARD_EDGES_FILE,
    REVERSE_EDGES_FILE,
    SYMBOL_TABLE_FILE,
    SYMBOL_TO_FILE_FILE
)

from utils.graph_utils import (
    load_json,
    save_json
)

from utils.parser_utils import parse_java_file


# -----------------------------------------
# Incrementally update modified repository symbols.
# Avoid rebuilding complete repository graph.
# -----------------------------------------

def update_repository_graph(modified_symbols=None, modified_files=None):

    if modified_symbols is None:
        modified_symbols = []

    if modified_files is None:
        modified_files = set()
    else:
        modified_files = set(modified_files)

    symbol_table = load_json(
        SYMBOL_TABLE_FILE
    )

    forward_edges = load_json(
        FORWARD_EDGES_FILE
    )

    reverse_edges = load_json(
        REVERSE_EDGES_FILE
    )

    symbol_to_file = load_json(
        SYMBOL_TO_FILE_FILE
    )


    # -----------------------------------------
    # Locate modified source files carefully.
    # Modified symbols determine reparsing scope.
    # -----------------------------------------

    for symbol_id in modified_symbols:

        if symbol_id in symbol_to_file:

            modified_files.add(
                symbol_to_file[symbol_id]
            )


    # -----------------------------------------
    # Remove stale graph nodes completely.
    # Delete outdated repository relationships safely.
    # -----------------------------------------

    stale_symbols = []

    for symbol_id, file_path in (
        symbol_to_file.items()
    ):

        if file_path in modified_files:

            stale_symbols.append(symbol_id)

    for stale_symbol in stale_symbols:

        symbol_table.pop(stale_symbol, None)

        forward_edges.pop(stale_symbol, None)

        reverse_edges.pop(stale_symbol, None)

        symbol_to_file.pop(stale_symbol, None)


    # -----------------------------------------
    # Remove incoming stale dependency references.
    # Clean repository graph consistency carefully.
    # -----------------------------------------

    for node in forward_edges:

        forward_edges[node] = [
            neighbor
            for neighbor in forward_edges[node]
            if neighbor not in stale_symbols
        ]

    for node in reverse_edges:

        reverse_edges[node] = [
            neighbor
            for neighbor in reverse_edges[node]
            if neighbor not in stale_symbols
        ]


    # -----------------------------------------
    # Reparse modified files incrementally now.
    # Rebuild affected repository graph sections.
    # -----------------------------------------

    method_lookup = {}

    for file_path in modified_files:

        tree, code = parse_java_file(file_path)

        package_name = ""

        if tree.package:
            package_name = tree.package.name

        for _, class_node in tree.filter(
            javalang.tree.ClassDeclaration
        ):

            class_name = class_node.name

            for method in class_node.methods + class_node.constructors:

                symbol_id = build_symbol_id(
                    package_name,
                    class_name,
                    method
                )

                symbol_table[symbol_id] = {

                    "id": symbol_id,

                    "file_path": file_path,

                    "callers": [],

                    "callees": []
                }

                symbol_to_file[symbol_id] = file_path

                method_lookup[
                    method.name
                ] = symbol_id


    # -----------------------------------------
    # Recompute dependency graph edges incrementally.
    # Update affected callers and callees.
    # -----------------------------------------

    for file_path in modified_files:

        tree, code = parse_java_file(file_path)

        package_name = ""

        if tree.package:
            package_name = tree.package.name

        for _, class_node in tree.filter(
            javalang.tree.ClassDeclaration
        ):

            class_name = class_node.name

            for method in class_node.methods + class_node.constructors:

                caller_id = build_symbol_id(
                    package_name,
                    class_name,
                    method
                )

                forward_edges[caller_id] = []

                calls = extract_method_calls(method)

                for call_name in calls:

                    if call_name in method_lookup:

                        callee_id = (
                            method_lookup[call_name]
                        )

                        forward_edges[
                            caller_id
                        ].append(callee_id)

                        if callee_id not in reverse_edges:
                            reverse_edges[callee_id] = []

                        reverse_edges[
                            callee_id
                        ].append(caller_id)


    # -----------------------------------------
    # Persist incrementally updated graph structures.
    # Repository graph remains fully synchronized.
    # -----------------------------------------

    save_json(
        SYMBOL_TABLE_FILE,
        symbol_table
    )

    save_json(
        FORWARD_EDGES_FILE,
        forward_edges
    )

    save_json(
        REVERSE_EDGES_FILE,
        reverse_edges
    )

    save_json(
        SYMBOL_TO_FILE_FILE,
        symbol_to_file
    )

    return {
        "updated_symbols": modified_symbols
    }
