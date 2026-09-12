import os

# Disable CrewAI Telemetry:
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

from llms.mock_llm import MockLLM

from tools.rag_lookup import rag_lookup
from tools.check_order_status import check_order_status

from schemas.response_schema import validate_crew_response

# Mock LLM:
mock_llm = MockLLM()

# Tools:
@tool("Policy Lookup Tool")
def policy_lookup_tool(query: str) -> str:
    """
    Retrieve policy information from the Nykaa knowledge base.
    """
    return rag_lookup(query)


@tool("Order Status Lookup Tool")
def order_status_lookup_tool(record_id: str) -> dict:
    """
    Retrieve order status and escalation details.
    """
    return check_order_status(record_id)

# Agents:
retrieval_agent = Agent(
    role="Retrieval Agent",
    goal="Retrieve accurate policy information from the knowledge base.",
    backstory="Expert at searching Nykaa customer support policies.",
    tools=[policy_lookup_tool],
    llm=mock_llm,
    verbose=True
)

lookup_agent = Agent(
    role="Lookup Agent",
    goal="Retrieve customer order information using record IDs.",
    backstory="Specialist in order tracking and escalation analysis.",
    tools=[order_status_lookup_tool],
    llm=mock_llm,
    verbose=True
)

response_composer = Agent(
    role="Response Composer",
    goal=("Combine outputs from all agents into a final response."),
    backstory="Experienced support agent responsible for creating clear customer responses.",
    llm=mock_llm,
    verbose=True
)

"""
Least Autonomy Control:
The order_status_lookup_tool is intentionally wired only to the Lookup Agent.
Retrieval Agent and Response Composer cannot directly access customer order data.
"""

# Tasks:
policy_task = Task(
    description=(
        """
        Use the Policy Lookup Tool to answer the following query:
        What is the warranty on electronics?
        """
    ),
    expected_output="Grounded answer generated from the policy documents.",
    agent=retrieval_agent
)

lookup_task = Task(
    description=(
        """
        Use the Order Status Lookup Tool to retrieve order details for the following:
        Record ID: ORD0019
        """
    ),
    expected_output="Order details including status, order value, escalation score and recommendation.",
    agent=lookup_agent
)

compose_task = Task(
    description=(
        """
        Review the outputs from the Retrieval Agent and Lookup Agent.
        Create one final support response.
        """
    ),
    expected_output="Final customer-support response.",
    agent=response_composer
)

# Crew:
nykaa_support_crew = Crew(
    agents=[
        retrieval_agent,
        lookup_agent,
        response_composer
    ],
    tasks=[
        policy_task,
        lookup_task,
        compose_task
    ],
    process=Process.sequential,
    verbose=True
)

# Main Execution:
if __name__ == "__main__":

    result = nykaa_support_crew.kickoff()

    validated_response = validate_crew_response(
        answer=str(result),
        source="knowledge_base",
        grounded=True,
        escalation_recommended=False
    )

    print(validated_response)

