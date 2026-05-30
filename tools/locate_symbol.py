from utils.constants import SYMBOL_TABLE_FILE
from utils.graph_utils import load_json

# -----------------------------------------
# Lookup canonical symbol from hashmap.
# Provides fuzzy suggestions if ID is wrong.
# -----------------------------------------

def locate_symbol(symbol_id):

    symbol_table = load_json(
        SYMBOL_TABLE_FILE
    )

    metadata = symbol_table.get(symbol_id)
    
    if metadata:
        return {
            "status": "success",
            "symbol_metadata": metadata
        }
    
    # Fuzzy Search / Suggestion Logic
    parts = symbol_id.split(".")
    method_hint = parts[-1].split("(")[0] 
    
    suggestions = []
    for sid in symbol_table.keys():
        if sid.endswith("." + method_hint) or f".{method_hint}(" in sid:
            suggestions.append(sid)
            
    if suggestions:
        # We return SUCCESS here because we successfully generated candidates
        return {
            "status": "success",
            "message": f"Symbol '{symbol_id}' not found, but we found these potential Canonical IDs. YOU MUST PICK ONE of these for your next tool call.",
            "candidate_ids": suggestions
        }

    return {
        "status": "failure",
        "message": f"Symbol '{symbol_id}' not found and no similar methods discovered."
    }