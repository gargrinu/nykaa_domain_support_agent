import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Session Store:
store = {}

# Get Session History:
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

# Runnable:
def crew_response(question: str):
    if "warranty" in question.lower():
        return (
            "Electronics products may carry manufacturer"
            "warranties ranging from 6 months to 2 years."
        )

    return ("Mock crew response.")

class CrewRunnable:
    def invoke(self, inputs):
        return {
            "output": crew_response(inputs["input"])
        }

# Memory-Enabled Agent:
agent_with_memory = (
    RunnableWithMessageHistory(
        CrewRunnable(),
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="output"
    )
)

# Helper Function to Ask the Agent:
def ask_agent(session_id, user_input):
    response = (
        agent_with_memory.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
    )

    return response["output"]

# Demo:
if __name__ == "__main__":
    print("\nMEMORY DEMONSTRATION")

    session_id = "customer_001"

    print("\nTurn 1")
    print(ask_agent(session_id,"My order id is ORD0019."))

    print("\nTurn 2")
    print(ask_agent(session_id,"Can you track it?"))

    print("\nStored Memory:")

    for msg in store[session_id].messages:
        print(
            type(msg).__name__,
            "-",
            msg.content
        )

    print("\nFRESH SESSION DEMONSTRATION")

    new_session = ("customer_002")
    
    print(ask_agent(new_session,"Can you track it?"))