# Reject Oversized Requests:
MAX_REQUEST_TOKENS = 200

def enforce_budget(user_input: str):
    """
    Simple token budget control.
    """
    token_count = len(user_input.split())

    if token_count > MAX_REQUEST_TOKENS:
        return {
            "allowed": False,
            "message":
                (
                    "Request rejected. "
                    "Token budget exceeded."
                ),
            "token_count": token_count
        }

    return {
        "allowed": True,
        "token_count": token_count
    }

oversized_prompt = ("hello " * 250)

result = enforce_budget(oversized_prompt)

print(result)