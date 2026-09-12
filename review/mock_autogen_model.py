class MockReviewEngine:
    @staticmethod
    def review(context: str, draft_answer: str):
        if "30 years warranty" in draft_answer.lower():
            return {
                "approved": False,
                "final_answer": context,
                "reason": "Unsupported claim detected."
            }

        return {
            "approved": True,
            "final_answer": draft_answer,
            "reason": "Answer grounded in retrieved context."
        }