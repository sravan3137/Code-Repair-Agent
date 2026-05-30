from utils.constants import SYMBOL_TO_FILE_FILE

from utils.graph_utils import load_json


# -----------------------------------------
# Retrieve source code for target symbol.
# Symbol maps directly to source file.
# -----------------------------------------

def retrieve_symbol_source(symbol_id):

    symbol_to_file = load_json(
        SYMBOL_TO_FILE_FILE
    )

    if symbol_id not in symbol_to_file:
        return None

    file_path = symbol_to_file[symbol_id]


    # -----------------------------------------
    # Read repository source file contents.
    # Return complete source code currently.
    # -----------------------------------------

    with open(file_path, "r") as file:

        source_code = file.read()

    return {
        "symbol_id": symbol_id,
        "source_code": source_code
    }