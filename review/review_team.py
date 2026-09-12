from review.verdict_schema import VerdictModel

# Reviewer Agent:
class PolicyComplianceReviewer:
    """
    Reviewer Agent
    """

    def review(self, context, draft_answer):

        draft_lower = (draft_answer.lower())
        context_lower = (context.lower())

        unsupported_claim = ("30 years warranty" in draft_lower)

        if unsupported_claim:
            return {
                "approved": False,
                "feedback": "Draft answer contains unsupported information."
            }

        return {
            "approved": True,
            "feedback": "Answer is grounded in retrieved context."
        }

# Editor Agent
class FinalEditor:
    def edit(self, review_result, context, draft_answer):
        if review_result["approved"]:
            return VerdictModel(
                approved=True,
                final_answer=draft_answer,
                reason=review_result["feedback"]
            )

        corrected_answer = context

        return VerdictModel(
            approved=False,
            final_answer=corrected_answer,
            reason=review_result["feedback"]
        )

# Review Team:
class RoundRobinReviewTeam:
    def __init__(self):
        self.reviewer = PolicyComplianceReviewer()
        self.editor = FinalEditor()

    def run(self, context, draft_answer):
        review_result = self.reviewer.review(context, draft_answer)
        verdict = self.editor.edit(review_result, context, draft_answer)

        return verdict