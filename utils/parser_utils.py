import os
import javalang


# -----------------------------------------
# Parse Java source code into AST.
# Return both AST and source code.
# -----------------------------------------

def parse_java_file(file_path):

    with open(file_path, "r") as file:
        code = file.read()

    tree = javalang.parse.parse(code)

    return tree, code


# -----------------------------------------
# Recursively collect Java source files.
# Ignore non-Java files completely.
# -----------------------------------------

def get_java_files(repo_path):

    java_files = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".java"):

                java_files.append(
                    os.path.join(root, file)
                )

    return java_files