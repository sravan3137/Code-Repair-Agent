import json
import datetime
import os

LOG_FILE = "logs/repair_trace.json"

def log_step(iteration, thought, action, tool_name=None, arguments=None, observation=None):
    """
    Records a complete step in the autonomous repair process.
    """
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "iteration": iteration,
        "thought": thought,
        "action": action,
        "tool": tool_name,
        "arguments": arguments,
        "observation": observation
    }
    
    # Read existing logs or start new list
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
            
    logs.append(entry)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def clear_logs():
    """Reset the log file at the start of a session."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
