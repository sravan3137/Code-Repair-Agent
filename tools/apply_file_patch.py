from tools.update_repository_graph import update_repository_graph
from utils.security import is_safe_path
import os

# -----------------------------------------
# Apply structural source patch onto file.
# Targets: imports, package, class headers.
# -----------------------------------------

def apply_file_patch(
    file_path,
    old_code,
    new_code
):
    # --- SECURITY CHECK: Path Sandboxing ---
    if not is_safe_path(file_path, os.getcwd()):
        return {
            "success": False,
            "message": f"SECURITY: Access denied to path: {file_path}"
        }

    # -----------------------------------------
    # Read current repository source contents.
    # Replace targeted structural region.
    # -----------------------------------------

    with open(file_path, "r") as file:

        content = file.read()

    if old_code not in content:
        return {
            "success": False,
            "message": "Target old_code not found in the file."
        }

    # Basic safety: ensure we aren't replacing a massive block including method bodies
    # Structural patches should generally be small or focused on declarations.
    if "{" in old_code and "}" in old_code and old_code.count("\n") > 15:
         return {
            "success": False,
            "message": "Patch appears to include method bodies. Use apply_symbol_patch for logic changes."
        }

    updated_content = content.replace(
        old_code,
        new_code
    )


    # -----------------------------------------
    # Persist updated repository source code.
    # -----------------------------------------

    with open(file_path, "w") as file:

        file.write(updated_content)


    # -----------------------------------------
    # Sync repository graph after modification.
    # Reparses the entire file to find new symbols.
    # -----------------------------------------
    update_repository_graph(modified_files=[file_path])

    return {
        "success": True,
        "updated_file": file_path
    }
