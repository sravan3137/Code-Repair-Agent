import subprocess
# Validate repository using Java compiler.
# Execute dummy repository Main class.
# -----------------------------------------

def validate_dummy_repository(repo_path):

    try:


        # -----------------------------------------
        # Compile all Java repository source files.
        # Capture compilation failure logs safely.
        # -----------------------------------------

        compile_process = subprocess.run(
            ["javac", "*.java"],
            cwd=repo_path,
            shell=True,
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:

            return {
                "success": False,
                "logs": compile_process.stderr
            }


        # -----------------------------------------
        # Execute compiled Main repository program.
        # Capture runtime execution logs safely.
        # -----------------------------------------

        run_process = subprocess.run(
            ["java", "Main"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        return {
            "success": (
                run_process.returncode == 0
            ),
            "logs": (
                run_process.stdout +
                run_process.stderr
            )
        }

    except Exception as error:

        return {
            "success": False,
            "logs": str(error)
        }