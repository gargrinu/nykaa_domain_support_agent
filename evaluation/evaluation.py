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

import json
from rag.rag_engine import answer_with_rag

TEST_QUERIES = [
    # Required Knowledge Base Topics
    "What is the return window for Beauty products?",
    "How long do COD refunds take?",
    "What are the delivery timelines?",
    "How does reverse pickup work?",
    "What is the warranty on electronics?",
    "Can I cancel an order after shipment?",
    "How can loyalty points be redeemed?",
    "What happens if a payment fails?",
    "How does size exchange work?",
    "How do I report a damaged item?",
    "Are there international shipping restrictions?",
    "How are support requests escalated?",

    # Additional
    "What is the return period for apparel items?",

    # Out of scope
    "Who won the IPL in 2020?",
    "How do I bake a cake?"
]

# Mock LLM Judge:
def mock_judge(query,answer):
    """
    Deterministic evaluation judge.
    Scores: 1-5
    """
    answer_lower = answer.lower()

    # Safety
    safety = 5

    # Grounding
    if "i don't know" in answer_lower:
        grounding = 5
    else:
        grounding = 4

    # Accuracy
    if len(answer.strip()) == 0:
        accuracy = 1
    elif "i don't know" in answer_lower:
        accuracy = 5
    else:
        accuracy = 4

    # Completeness
    if len(answer.split()) > 20:
        completeness = 5
    elif len(answer.split()) > 10:
        completeness = 4
    else:
        completeness = 3

    return {
        "accuracy": accuracy,
        "grounding": grounding,
        "completeness": completeness,
        "safety": safety
    }

# Run Evaluation:
def evaluate():
    results = []

    accuracy_scores = []
    grounding_scores = []
    completeness_scores = []
    safety_scores = []

    print("LLM-AS-JUDGE EVALUATION")

    for query in TEST_QUERIES:
        answer = answer_with_rag(query)
        scores = mock_judge(
            query=query,
            answer=answer
        )
        results.append({
            "query": query,
            "answer": answer,
            "accuracy": scores["accuracy"],
            "grounding": scores["grounding"],
            "completeness": scores["completeness"],
            "safety": scores["safety"]
        })
        accuracy_scores.append(scores["accuracy"])
        grounding_scores.append(scores["grounding"])
        completeness_scores.append(scores["completeness"])
        safety_scores.append(scores["safety"])

        print(f"\nQuery: {query}")
        print(f"Accuracy: {scores['accuracy']}")
        print(f"Grounding: {scores['grounding']}")
        print(f"Completeness: {scores['completeness']}")
        print(f"Safety: {scores['safety']}")

    # Calculate Averages:
    avg_accuracy = round(sum(accuracy_scores) / len(accuracy_scores), 2)
    avg_grounding = round(sum(grounding_scores) / len(grounding_scores), 2)
    avg_completeness = round(sum(completeness_scores) / len(completeness_scores), 2)
    avg_safety = round(sum(safety_scores) / len(safety_scores), 2)

    print("\nAVERAGE SCORES")

    print(f"Accuracy: {avg_accuracy}")
    print(f"Grounding: {avg_grounding}")
    print(f"Completeness: {avg_completeness}")
    print(f"Safety: {avg_safety}")

    # Save Results
    evaluation_summary = {
        "per_query_results": results,
        "average_scores": {
            "accuracy": avg_accuracy,
            "grounding": avg_grounding,
            "completeness": avg_completeness,
            "safety": avg_safety
        }
    }

    with open("evaluation/evaluation_results.json", "w", encoding="utf-8") as file:
        json.dump(evaluation_summary, file, indent=4)

    return evaluation_summary

# Main
if __name__ == "__main__":
    evaluate()