import chromadb
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CHROMA_DB_PATH = "./chroma_db"
TOP_K = 3

TEST_QUERIES = [
    "What is the return window for Beauty products?",
    "What are the delivery timelines?",
    "Can I cancel an order?",
    "What is the warranty on electronics?",
    "What happens if payment fails?"
]

GROUND_TRUTH = {
    "What is the return window for Beauty products?":
        {"01_return_window"},

    "What are the delivery timelines?":
        {"03_delivery_slas"},

    "Can I cancel an order?":
        {"06_order_cancellation_policy"},

    "What is the warranty on electronics?":
        {"05_warranty_terms"},

    "What happens if payment fails?":
        {"08_payment_failure_retry"}
}

# Retreive Document IDs from ChromaDB:
def retrieve_document_ids(
    query,
    collection_name,
    top_k=TOP_K
):

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = client.get_collection(collection_name)

    data = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    documents = data["documents"]
    metadatas = data["metadatas"]

    corpus = documents + [query]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        corpus
    )

    query_vector = vectors[-1]

    document_vectors = vectors[:-1]

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    ranked_indices = np.argsort(
        similarities
    )[::-1][:top_k]

    retrieved_docs = set()

    for idx in ranked_indices:
        doc_id = metadatas[idx].get("document_id")
        retrieved_docs.add(doc_id)

    return retrieved_docs

# Precision and Recall Calculation:
def calculate_metrics(
    retrieved_docs,
    relevant_docs
):

    true_positives = len(
        retrieved_docs.intersection(
            relevant_docs
        )
    )

    precision = (
        true_positives /
        len(retrieved_docs)
    ) if retrieved_docs else 0

    recall = (
        true_positives /
        len(relevant_docs)
    ) if relevant_docs else 0

    return (
        true_positives,
        precision,
        recall
    )

# Collection Evaluation:
def evaluate_collection(collection_name):

    print(f"\nCOLLECTION: {collection_name}")

    precision_scores = []
    recall_scores = []

    for query in TEST_QUERIES:

        relevant_docs = (GROUND_TRUTH[query])

        retrieved_docs = (
            retrieve_document_ids(
                query=query,
                collection_name=collection_name,
                top_k=TOP_K
            )
        )

        (
            tp,
            precision,
            recall
        ) = calculate_metrics(
            retrieved_docs,
            relevant_docs
            )

        precision_scores.append(precision)

        recall_scores.append(recall)

        print("\nRelevant Documents:")
        print(relevant_docs)

        print("\nRetrieved Documents:")
        print(retrieved_docs)

        print(f"\nPrecision = {tp}/{len(retrieved_docs)} = {precision:.2f}")
        print(f"Recall = {tp}/{len(relevant_docs)} = {recall:.2f}")

    average_precision = (sum(precision_scores)/len(precision_scores))
    average_recall = (sum(recall_scores)/len(recall_scores))

    print(f"\nAverage Precision: {average_precision:.2f}")
    print(f"Average Recall: {average_recall:.2f}")

    return (average_precision, average_recall)

# Main Execution:
if __name__ == "__main__":

    fixed_precision, fixed_recall = (
        evaluate_collection(
            "fixed_chunks"
        )
    )

    sentence_precision, sentence_recall = (
        evaluate_collection(
            "sentence_chunks"
        )
    )

    print("\n")
    print("FINAL COMPARISON")
    
    print(f"\nFixed Chunking")
    print(f"Average Precision = {fixed_precision:.2f}")
    print(f"Average Recall = {fixed_recall:.2f}")

    print(f"\nSentence Chunking")
    print(f"Average Precision = {sentence_precision:.2f}")
    print(f"Average Recall = {sentence_recall:.2f}")

    print("\nRecommendation:")

    if sentence_precision >= fixed_precision:
        print(
            "Deploy Sentence-Based Chunking. "
            "It provides more focused retrieval while maintaining recall."
        )

    else:
        print(
            "Deploy Fixed-Size Chunking. "
            "It provides better precision while maintaining recall."
        )