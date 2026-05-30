import re
import os
from utils.constants import SYMBOL_TO_FILE_FILE
from utils.graph_utils import load_json
from tools.update_repository_graph import update_repository_graph
from utils.security import is_safe_code, is_safe_path

# -----------------------------------------
# Apply generated source patch onto symbol.
# Replace old code with new code.
# -----------------------------------------

def apply_symbol_patch(
    symbol_id,
    old_code,
    new_code,
    new_imports=None,
    new_fields=None
):

    # 1. Resolve file path from Symbol ID or Table
    is_tagged = ":" in symbol_id or "<" in symbol_id
    
    if ":" in symbol_id:
        # Format: repositories/path/to/file.java:<tag>
        file_path, tag = symbol_id.split(":")
    else:
        symbol_to_file = load_json(SYMBOL_TO_FILE_FILE)
        if symbol_id not in symbol_to_file:
            return {
                "success": False,
                "message": f"Symbol missing: {symbol_id}"
            }
        file_path = symbol_to_file[symbol_id]

    # --- SECURITY CHECK: Path Sandboxing ---
    if not is_safe_path(file_path, os.getcwd()):
        return {
            "success": False,
            "message": f"SECURITY: Access denied to path: {file_path}"
        }

    # 2. Extract context and validate patch scope
    if not is_tagged:
        symbol_parts = symbol_id.split('(')[0].split('.')
        method_name = symbol_parts[-1]
        expected_name = symbol_parts[-2] if method_name == "<init>" else method_name

        if expected_name not in old_code:
            return {
                "success": False,
                "message": f"old_code must contain the method name '{expected_name}'. Replacing the entire file is not allowed."
            }
        
        # Check for package/import declarations using regex
        if re.search(r'^package\s+', old_code, re.MULTILINE) or re.search(r'^import\s+', old_code, re.MULTILINE):
            return {
                "success": False,
                "message": "old_code should only represent the target method block, not the entire file containing package/import."
            }

    # -----------------------------------------
    # Read current repository source contents.
    # Replace targeted source code region.
    # -----------------------------------------

    with open(file_path, "r") as file:

        content = file.read()

    if old_code not in content:
        return {
            "success": False,
            "message": "Target old_code not found in the file. Ensure the provided snippet matches the source exactly."
        }

    updated_content = content.replace(
        old_code,
        new_code
    )

    if new_imports:
        if new_imports not in updated_content:
            if "package " in updated_content:
                lines = updated_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("package "):
                        lines.insert(i + 1, "\n" + new_imports)
                        break
                updated_content = "\n".join(lines)
            else:
                updated_content = new_imports + "\n\n" + updated_content

    if new_fields:
        if new_fields not in updated_content:
            target_class = symbol_parts[-2]
            class_pattern = r"(class\s+" + target_class + r"\b[^\{]*\{)"
            match = re.search(class_pattern, updated_content)
            if match:
                insert_pos = match.end()
                updated_content = updated_content[:insert_pos] + "\n    " + new_fields + "\n" + updated_content[insert_pos:]

    # -----------------------------------------
    # Persist updated repository source code.
    # Write modified file back safely.
    # -----------------------------------------

    with open(file_path, "w") as file:

        file.write(updated_content)

    # -----------------------------------------
    # Sync repository graph after modification.
    # Handles method renames or signature changes.
    # -----------------------------------------
    update_repository_graph([symbol_id])

    return {
        "success": True,
        "updated_file": file_path
    }