import javalang


# -----------------------------------------
# Build canonical symbol ID for methods.
# IDs become graph node identities.
# -----------------------------------------

def build_symbol_id(package_name, class_name, method_node):

    if isinstance(method_node, javalang.tree.ConstructorDeclaration):
        method_name = "<init>"
    else:
        method_name = method_node.name

    params = []

    for parameter in method_node.parameters:

        params.append(parameter.type.name)

    parameter_string = ",".join(params)

    prefix = f"{package_name}." if package_name else ""
    
    return (
        f"{prefix}"
        f"{class_name}."
        f"{method_name}"
        f"({parameter_string})"
    )


# -----------------------------------------
# Extract method invocation names from AST.
# Used for graph edge generation.
# -----------------------------------------

def extract_method_calls(method_node):

    method_calls = []

    for path, node in method_node:

        if isinstance(
            node,
            javalang.tree.MethodInvocation
        ):

            method_calls.append(node.member)

        elif isinstance(
            node,
            javalang.tree.ClassCreator
        ):

            method_calls.append(node.type.name)

    return method_calls