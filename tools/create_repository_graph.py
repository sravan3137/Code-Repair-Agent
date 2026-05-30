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

from utils.graph_utils import save_json

from utils.parser_utils import (
    get_java_files,
    parse_java_file
)


# -----------------------------------------
# Build complete repository graph structures.
# Create symbol table and graph edges.
# -----------------------------------------

def create_repository_graph(repo_path):

    symbol_table = {}

    forward_edges = {}

    reverse_edges = {}

    symbol_to_file = {}


    # -----------------------------------------
    # Traverse all Java repository files.
    # Parse files into AST trees.
    # -----------------------------------------

    java_files = get_java_files(repo_path)

    method_name_lookup = {}


    # -----------------------------------------
    # Extract repository symbols from AST.
    # Create canonical symbol identifiers.
    # -----------------------------------------

    for file_path in java_files:

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

                if method.name not in method_name_lookup:

                    method_name_lookup[
                        method.name
                    ] = []

                method_name_lookup[
                    method.name
                ].append(symbol_id)


    # -----------------------------------------
    # Build outgoing and incoming edges.
    # Traverse method invocations from AST.
    # -----------------------------------------

    for file_path in java_files:

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

                    if call_name in method_name_lookup:

                        possible_callees = (
                            method_name_lookup[call_name]
                        )

                        for callee_id in possible_callees:

                            forward_edges[
                                caller_id
                            ].append(callee_id)
                            
                            symbol_table[
                                caller_id
                            ]["callees"].append(
                                callee_id
                            )

                            if callee_id not in reverse_edges:
                                reverse_edges[callee_id] = []

                            reverse_edges[
                                callee_id
                            ].append(caller_id)
                            
                            symbol_table[
                                callee_id
                            ]["callers"].append(
                                caller_id
                            )


    # -----------------------------------------
    # Persist graph structures onto disk.
    # These become retrieval data structures.
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

    print("Repository graph created.")