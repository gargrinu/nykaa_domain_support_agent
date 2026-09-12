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

import asyncio
from review.autogen_review import run_review

# Case 1: Approval
context = "Electronics products may carry manufacturer warranties ranging from 6 months to 2 years."

draft_answer = "Electronics products may carry manufacturer warranties ranging from 6 months to 2 years."

verdict = asyncio.run(run_review(context, draft_answer))

print(verdict.model_dump())

# Case 2: Revision
context = "Electronics products may carry manufacturer warranties ranging from 6 months to 2 years."

draft_answer = "Electronics products come with a 30 years warranty."

verdict = asyncio.run(run_review(context, draft_answer))

print(verdict.model_dump())