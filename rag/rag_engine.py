import chromadb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cache
CACHE = {}
CALL_COUNTER = 0

def normalize_query(query: str):
    return query.strip().lower

# Vector DB
CHROMA_DB_PATH = "./chroma_db"
TOP_K = 3
SIMILARITY_THRESHOLD = 0.20

# Create ChromaDB Client:
client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_collection(
    "sentence_chunks"
)

# Retrieve Relevant Chunks:
def retrieve_relevant_chunks(query: str, top_k: int = TOP_K):
    records = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )
    documents = records["documents"]
    metadatas = records["metadatas"]
    all_text = documents + [query]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(all_text)
    query_vector = vectors[-1]
    document_vectors = vectors[:-1]
    similarities = cosine_similarity(query_vector, document_vectors)[0]
    ranked_indices = (similarities.argsort()[::-1])
    retrieved_chunks = []

    for index in ranked_indices[:top_k]:
        retrieved_chunks.append(
            {
                "text": documents[index],
                "metadata": metadatas[index],
                "similarity": float(similarities[index])
            }
        )

    return retrieved_chunks

# Build Prompt for LLM:
def build_prompt(
    query,
    retrieved_chunks
):

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"""
            Policy Chunk {index}
            Document: {chunk['metadata']['document_id']}
            Content: {chunk['text']}
            Similarity Score: {chunk['similarity']:.4f}
            """
        )

    context = "\n".join(context_parts)

    prompt = f"""
    You are a helpful Nykaa customer support assistant.
    Answer the customer question using ONLY the policy context provided.

    Rules:
    1. Do not make up information.
    2. Use only the retrieved context.
    3. If information is missing, say:
    "I don't know based on the available knowledge base."

    Policy Context:
    {context}

    Customer Question:
    {query}

    Answer:
    """

    return prompt

# Generate Answer from Retrieved Chunks:
def generate_answer(query, retrieved_chunks):
    if not retrieved_chunks:
        return ( "I don't know based on the available knowledge base.")

    answer = []

    for chunk in retrieved_chunks:
        answer.append(chunk["text"])

    return " ".join(answer)

# Answer with RAG:
def answer_with_rag(query, similarity_threshold=SIMILARITY_THRESHOLD):
    global CALL_COUNTER
    normalized_query = normalize_query(query)

    # Cache Hit:
    if normalize_query in CACHE:
        print("Cache Hit")
    
        return CACHE[normalize_query]

    # Cache Miss:
    CALL_COUNTER += 1
    print(f"Cache Miss | RAG Call #{CALL_COUNTER}")

    retrieved_chunks = (retrieve_relevant_chunks(query))
    top_similarity = (retrieved_chunks[0]["similarity"])

    print(f"Top Similarity: {top_similarity:.4f}")

    if top_similarity < similarity_threshold:
        return ("I don't know based on the available knowledge base.")
    else:
        answer = generate_answer(query, retrieved_chunks)

    CACHE[normalize_query] = answer

    return answer

# Threshold Calibration:
calibration_queries = [

    # In scope queries:
    "What is the return window for Beauty products?",
    "What are the delivery timelines?",
    "Can I cancel an order?",
    "What is the warranty on electronics?",
    "What happens if payment fails?",
    
    # Out of scope queries:
    "Who won the IPL in 2020?",
    "How do I bake a cake?"
]

for query in calibration_queries:
    chunks = retrieve_relevant_chunks(query)

    print(
        query,
        chunks[0]["similarity"]
    )

query = "Can I cancel an order?"

answer = answer_with_rag(query)

print("Query:", query)
print("Answer:", answer)