from agent.agent_loop import DebuggingAgent

from tools.create_repository_graph import (
    create_repository_graph
)

from tools.validate_dummy_repository import (
    validate_dummy_repository
)


# -----------------------------------------
# Configure repository path for debugging.
# Dummy repository contains intentional errors.
# -----------------------------------------

REPO_PATH = "repositories/complex_repo"


# -----------------------------------------
# Build initial repository graph structures.
# Graph powers dependency-aware retrieval system.
# -----------------------------------------

create_repository_graph(REPO_PATH)


# -----------------------------------------
# Validate repository before agent execution.
# Capture compilation and runtime failures.
# -----------------------------------------

validation_result = validate_dummy_repository(
    REPO_PATH
)

print(validation_result)


# -----------------------------------------
# Launch autonomous debugging agent conditionally.
# Agent starts only when validation fails.
# -----------------------------------------
 
if not validation_result["success"]:

    agent = DebuggingAgent()

    agent.run(
        initial_logs=validation_result["logs"],
        repo_path=REPO_PATH,
        max_iterations=40
    )

else:

    print("Repository already valid.")