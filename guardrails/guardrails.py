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

import re
from rag.rag_engine import retrieve_relevant_chunks

# PII Masking:
PHONE_PATTERN = r"\b\d{10}\b"

CARD_LAST4_PATTERN = (r"\b(?:card|last4|last-4)\s*[:=]?\s*(\d{4})\b")

def mask_pii(text: str):

    # Mask Phone Numbers:
    text = re.sub(
        PHONE_PATTERN,
        "[PHONE_MASKED]",
        text
    )

    # Mask Card Last 4 Digits:
    text = re.sub(
        CARD_LAST4_PATTERN,
        "card: [CARD_LAST4_MASKED]",
        text,
        flags=re.IGNORECASE
    )

    return text

# Prompt Injection Detection:
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "show hidden prompt",
    "bypass guardrails",
    "act as administrator",
    "act as admin",
    "override instructions"
]

def detect_prompt_injection(user_input: str):
    text = user_input.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in text:
            return True

    return False

# Input Guardrail:
def input_guardrail(user_input: str):
    if detect_prompt_injection(user_input):
        return {
            "allowed": False,
            "message": "Prompt injection attempt detected."
        }

    masked_input = mask_pii(user_input)

    return {
        "allowed": True,
        "masked_input": masked_input
    }

# Groundedness Check:
SIMILARITY_THRESHOLD = 0.20

def groundedness_check(query: str):
    chunks = retrieve_relevant_chunks(query=query)
    top_similarity = (chunks[0]["similarity"])

    if top_similarity < (SIMILARITY_THRESHOLD):
        return {
            "grounded": False,
            "message": "I don't know based on the available knowledge base."
        }

    return {
        "grounded": True,
        "chunks": chunks
    }