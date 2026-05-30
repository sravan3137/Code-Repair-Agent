import json

from agent.llm_client import call_llm

from agent.memory import AgentMemory

from agent.prompts import SYSTEM_PROMPT

from agent.tool_executor import execute_tool

from utils.logger import log_step, clear_logs

from utils.security import is_safe_code


# -----------------------------------------
# Autonomous repository debugging agent loop.
# Implements iterative ReAct tool orchestration.
# -----------------------------------------

class DebuggingAgent:

    def __init__(self, require_approval=True):

        self.memory = AgentMemory()
        self.require_approval = require_approval

        self.memory.add(
            "system",
            SYSTEM_PROMPT
        )


    # -----------------------------------------
    # Execute iterative repository repair workflow.
    # Continue until repository becomes valid.
    # -----------------------------------------

    def run(
        self,
        initial_logs,
        repo_path,
        max_iterations=40
    ):

        # Clear previous trace at start
        clear_logs()

        self.memory.add(
            "user",
            f"""
Repository Path:
{repo_path}

Failure Logs:
{initial_logs}
"""
        )

        iteration = 0


        # -----------------------------------------
        # Execute ReAct reasoning loop continuously.
        # Alternate reasoning and deterministic tools.
        # -----------------------------------------

        while iteration < max_iterations:

            iteration += 1

            print(
                f"\n===== ITERATION {iteration} ====="
            )

            response = call_llm(
                self.memory.get_messages()
            )

            # -----------------------------------------
            # Parse structured LLM JSON response safely.
            # Handle chatty LLMs by finding the JSON block.
            # -----------------------------------------

            try:
                # Find first { and last }
                start_index = response.find("{")
                end_index = response.rfind("}")
                
                if start_index == -1 or end_index == -1:
                    raise ValueError("No JSON object found in response")

                json_string = response[start_index : end_index + 1]
                parsed_response = json.loads(json_string)

            except Exception as e:
                print(f"Invalid JSON response: {e}")
                print(f"RAW LLM RESPONSE: {response}") # added
                log_step(iteration, "Invalid JSON", "error", observation=response)
                break

            action = parsed_response.get("action")
            thought = parsed_response.get("thought", "")


            # -----------------------------------------
            # Handle final successful agent responses.
            # Stop iterative debugging execution loop.
            # -----------------------------------------

            if action == "final_answer":

                print(
                    parsed_response["message"]
                )
                
                log_step(iteration, thought, "final_answer", observation=parsed_response["message"])

                break


            # -----------------------------------------
            # Execute deterministic repository tool calls.
            # Store results back into memory.
            # -----------------------------------------

            elif action == "tool_call":

                tool_name = (
                    parsed_response["tool_name"]
                )

                arguments = (
                    parsed_response["arguments"]
                )

                # --- SECURITY CHECK: Token Scanning ---
                if "new_code" in arguments:
                    is_safe, reason = is_safe_code(arguments["new_code"])
                    if not is_safe:
                        print(f"SECURITY ALERT: {reason}")
                        log_step(iteration, thought, action, tool_name, arguments, observation=f"BLOCKED: {reason}")
                        break

                # --- SECURITY CHECK: Manual Approval ---
                if self.require_approval and tool_name in ["apply_symbol_patch", "apply_file_patch", "validate_dummy_repository"]:
                    print(f"\n{'='*60}")
                    print(f"SECURITY APPROVAL REQUIRED")
                    print(f"{'='*60}")
                    print(f"Tool: {tool_name}")
                    
                    target = arguments.get("symbol_id") or arguments.get("file_path") or "Repository"
                    print(f"Target: {target}")

                    if "new_code" in arguments:
                        print("\nPROPOSED CODE CHANGES:")
                        print("-" * 40)
                        print(arguments["new_code"])
                        print("-" * 40)
                    
                    if "new_imports" in arguments and arguments["new_imports"]:
                        print(f"Adding Import: {arguments['new_imports']}")

                    if "new_fields" in arguments and arguments["new_fields"]:
                        print(f"Adding Field: {arguments['new_fields']}")

                    choice = input("\nApprove this action? (y/n): ").lower()
                    if choice != 'y':
                        print("Execution aborted by user.")
                        log_step(iteration, thought, action, tool_name, arguments, observation="Aborted by user")
                        break
                    print(f"{'='*60}\n")

                tool_result = execute_tool(
                    tool_name,
                    arguments
                )

                # Record the full execution step in audit log
                log_step(
                    iteration=iteration,
                    thought=thought,
                    action="tool_call",
                    tool_name=tool_name,
                    arguments=arguments,
                    observation=tool_result
                )

                print(f"Tool executed: {tool_name}")

                self.memory.add(
                    "assistant",
                    response
                )

                self.memory.add(
                    "user",
                    json.dumps(tool_result)
                )

            else:
                received_action = parsed_response.get("action", "MISSING")
                print(f"Error: Unknown agent action received: '{received_action}'")
                print(f"FULL PARSED JSON: {json.dumps(parsed_response, indent=2)}") # added
                
                # Log the entire response so we can debug what the LLM sent
                log_step(
                    iteration, 
                    thought, 
                    "error_unknown_action", 
                    observation={
                        "received_action": received_action,
                        "full_response": parsed_response
                    }
                )
                break
