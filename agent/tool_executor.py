from agent.tool_registry import TOOLS


# -----------------------------------------
# Execute deterministic repository tool calls.
# Safely handle tool execution failures.
# -----------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name not in TOOLS:

        return {
            "success": False,
            "error": "Unknown tool"
        }

    try:

        tool_function = TOOLS[tool_name]

        result = tool_function(**arguments)

        return {
            "success": True,
            "result": result
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }