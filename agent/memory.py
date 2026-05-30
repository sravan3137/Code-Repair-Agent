# -----------------------------------------
# Store conversation history for ReAct.
# Maintain complete agent reasoning context.
# -----------------------------------------

class AgentMemory:

    def __init__(self):

        self.messages = []


    # -----------------------------------------
    # Add interaction messages into memory.
    # Preserve iterative reasoning history safely.
    # -----------------------------------------

    def add(self, role, content):

        self.messages.append({
            "role": role,
            "content": content
        })


    # -----------------------------------------
    # Retrieve full conversation memory state.
    # Used before every LLM interaction.
    # -----------------------------------------

    def get_messages(self):

        return self.messages