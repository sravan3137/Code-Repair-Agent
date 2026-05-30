# -----------------------------------------
# Tool to provide the final repair summary.
# Calling this tool signals the end of the agent loop.
# -----------------------------------------

def final_answer(message):
    return {
        "status": "success",
        "message": message,
        "is_final": True
    }
