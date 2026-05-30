import json
import os


# -----------------------------------------
# Save dictionary data into JSON files.
# Create graph directory if absent.
# -----------------------------------------

def save_json(path, data):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------------------
# Load JSON graph structures from disk.
# Return empty dictionary if absent.
# -----------------------------------------

def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(path, "r") as file:
        return json.load(file)