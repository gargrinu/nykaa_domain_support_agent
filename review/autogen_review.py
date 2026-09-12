import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import StructuredMessage

from review.verdict_schema import VerdictModel
from review.mock_autogen_model import MockReviewEngine

# Reviewer Agent:
reviewer = AssistantAgent(
    name="PolicyComplianceReviewer",
    model_client=None
)

# Final Editor Agent:
editor = AssistantAgent(
    name="FinalEditor",
    model_client=None,
    output_content_type=VerdictModel
)

# Team:
team = RoundRobinGroupChat(
    participants=[
        reviewer,
        editor
    ],
    max_turns=2,
    custom_message_types=[StructuredMessage[VerdictModel]]
)

# Review Stage:
async def run_review(context, draft_answer):
    result = MockReviewEngine.review(
        context=context,
        draft_answer=draft_answer
    )

    verdict = VerdictModel(
        approved=result["approved"],
        final_answer=result["final_answer"],
        reason=result["reason"]
    )

    return verdict