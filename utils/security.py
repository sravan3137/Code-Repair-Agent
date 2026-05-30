import os

DANGEROUS_JAVA_TOKENS = [
    "Runtime.getRuntime().exec",
    "ProcessBuilder",
    "System.exit",
    "Thread.stop",
    "FileOutputStream",
    "Files.write",
    "Socket",
    "ServerSocket",
    "URL.openStream"
]

def is_safe_code(code):
    """Checks if the generated code contains obvious security risks."""
    for token in DANGEROUS_JAVA_TOKENS:
        if token in code:
            return False, f"Dangerous token detected: {token}"
    return True, "Safe"

def is_safe_path(target_path, repo_root):
    """Ensures the agent doesn't write outside the repository root."""
    absolute_root = os.path.abspath(repo_root)
    absolute_target = os.path.abspath(target_path)
    return absolute_target.startswith(absolute_root)
