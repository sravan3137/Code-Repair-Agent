import re
import javalang
from utils.parser_utils import parse_java_file
from utils.ast_utils import build_symbol_id

# ---------------------------------------------------------
# Extract candidate repository symbols and tags from logs.
# Uses JIT AST parsing to handle Methods, Fields, and Imports.
# ---------------------------------------------------------

def extract_failure_context(raw_error_logs):
    
    candidate_targets = set()
    
    # Standard Java error patterns (Compilation/Runtime)
    patterns = [
        r"at ([\w.]+)\.([\w<>]+)\([\w.]+\.java:(\d+)\)", # Runtime
        r"([a-zA-Z0-9_/.]+\.java):(\d+):"               # Compilation
    ]

    matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, raw_error_logs):
            groups = match.groups()
            if len(groups) == 3: # Runtime
                matches.append({"file": None, "line": int(groups[2]), "hint": groups[0]}) 
            else: # Compilation
                matches.append({"file": groups[0], "line": int(groups[1]), "hint": None})

    if not matches:
        return {"status": "success", "candidate_symbols": []}

    for match in matches:
        target_file = match["file"]
        target_line = match["line"]
        
        # We need a proper path to the file. For now, we search repositories/
        # In a real system, we'd use a more robust path resolver.
        actual_path = None
        if target_file:
            for root, _, files in os.walk("repositories"):
                if target_file in files:
                    actual_path = os.path.join(root, target_file)
                    break
        
        if not actual_path:
            continue

        try:
            tree, code = parse_java_file(actual_path)
            package_name = tree.package.name if tree.package else ""
            
            # 1. Check Imports
            import_start = 1
            import_end = 1
            if tree.imports:
                import_start = tree.imports[0].position.line
                import_end = tree.imports[-1].position.line
                if import_start <= target_line <= import_end + 1:
                    candidate_targets.add(f"{actual_path}:<import>")
                    continue

            for _, node in tree.filter(javalang.tree.ClassDeclaration):
                class_name = node.name
                
                # 2. Check Class Header/Signature
                if node.position and node.position.line == target_line:
                    candidate_targets.add(f"{package_name}.{class_name}:<class>")
                    continue

                # 3. Check Fields
                for field in node.fields:
                    if field.position and field.position.line == target_line:
                        var_name = field.declarators[0].name
                        candidate_targets.add(f"{package_name}.{class_name}.<field>({var_name})")
                        break

                # 4. Check Methods/Constructors
                for method in node.methods + node.constructors:
                    if method.position:
                        # Estimate method end (very primitive, but works for JIT localization)
                        # A better way is to find the next sibling's start line
                        start = method.position.line
                        # We'll assume the line belongs to the method if it's within a reasonable block
                        # The agent will retrieve the source anyway to verify.
                        if start <= target_line <= start + 100: # Heuristic
                            symbol_id = build_symbol_id(package_name, class_name, method)
                            candidate_targets.add(symbol_id)
                            break

        except Exception as e:
            print(f"Error parsing {target_file}: {e}")

    return {
        "status": "success",
        "candidate_symbols": list(candidate_targets),
        "message": f"Localized {len(candidate_targets)} targets."
    }

import os # Needed for path walking