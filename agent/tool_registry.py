from tools.apply_symbol_patch import (
    apply_symbol_patch
)

from tools.apply_file_patch import (
    apply_file_patch
)

from tools.extract_failure_context import (
    extract_failure_context
)

from tools.locate_symbol import (
    locate_symbol
)

from tools.retrieve_symbol_source import (
    retrieve_symbol_source
)

from tools.traverse_dependency_graph import (
    traverse_dependency_graph
)

from tools.update_repository_graph import (
    update_repository_graph
)

from tools.validate_dummy_repository import (
    validate_dummy_repository
)

from tools.final_answer import (
    final_answer
)


# -----------------------------------------
# Register all deterministic repository tools.
# Agent accesses tools using this registry.
# -----------------------------------------

TOOLS = {

    "extract_failure_context": (
        extract_failure_context
    ),

    "locate_symbol": (
        locate_symbol
    ),

    "traverse_dependency_graph": (
        traverse_dependency_graph
    ),

    "retrieve_symbol_source": (
        retrieve_symbol_source
    ),

    "apply_symbol_patch": (
        apply_symbol_patch
    ),

    "apply_file_patch": (
        apply_file_patch
    ),

    "update_repository_graph": (
        update_repository_graph
    ),

    "validate_dummy_repository": (
        validate_dummy_repository
    ),

    "final_answer": (
        final_answer
    )
}
