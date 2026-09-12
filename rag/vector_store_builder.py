import os
import chromadb
from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE_FOLDER = "knowledge_base"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHROMA_DB_PATH = "./chroma_db"

FIXED_CHUNK_SIZE_WORDS = 40
FIXED_CHUNK_OVERLAP_WORDS = 10

# Load Documents:
def load_documents(folder_path):

    documents = []

    for filename in sorted(os.listdir(folder_path)):

        if filename.endswith(".txt"):

            file_path = os.path.join(
                folder_path,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read().strip()

            documents.append(
                {
                    "document_id": filename.replace(
                        ".txt",
                        ""
                    ),
                    "text": text
                }
            )

    return documents

# Fized Size Chunking With Overlap:
def fixed_size_chunking(
    text,
    chunk_size_words=40,
    overlap_words=10
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size_words

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap_words

    return chunks

# Sentence Chunking:
def sentence_chunking(text):

    sentences = text.split(".")

    chunks = []

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence:
            chunks.append(
                sentence + "."
            )

    return chunks

# Create Embeddings:
embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

def create_embeddings(texts):

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    ).tolist()

    return embeddings

# Setup ChromaDB Client and Collections:
client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

fixed_collection = (
    client.get_or_create_collection(
        name="fixed_chunks"
    )
)

sentence_collection = (
    client.get_or_create_collection(
        name="sentence_chunks"
    )
)

# Index Fixed Chunks:
def index_fixed_chunks(
    collection,
    documents
):

    ids = []
    texts = []
    metadatas = []

    for document in documents:

        chunks = fixed_size_chunking(
            document["text"],
            FIXED_CHUNK_SIZE_WORDS,
            FIXED_CHUNK_OVERLAP_WORDS
        )

        for chunk_index, chunk in enumerate(chunks):

            ids.append(
                f"{document['document_id']}_fixed_{chunk_index}"
            )

            texts.append(chunk)

            metadatas.append(
                {
                    "document_id":
                        document[
                            "document_id"
                        ],
                    "chunk_type":
                        "fixed",
                    "chunk_index":
                        chunk_index
                }
            )

    embeddings = create_embeddings(
        texts
    )

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return len(texts)

# Index Sentence Chunks:
def index_sentence_chunks(
    collection,
    documents
):

    ids = []
    texts = []
    metadatas = []

    for document in documents:

        chunks = sentence_chunking(
            document["text"]
        )

        for chunk_index, chunk in enumerate(chunks):

            ids.append(
                f"{document['document_id']}_sentence_{chunk_index}"
            )

            texts.append(chunk)

            metadatas.append(
                {
                    "document_id":
                        document["document_id"],
                    "chunk_type":
                        "sentence",
                    "chunk_index":
                        chunk_index
                }
            )

    embeddings = create_embeddings(
        texts
    )

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return len(texts)

# Main Function:
def main():

    print("\nLoading Knowledge Base Documents...")

    documents = load_documents(
        KNOWLEDGE_BASE_FOLDER
    )

    print(
        f"Loaded {len(documents)} documents."
    )

    print(
        "\nIndexing Fixed-Size Chunks..."
    )

    fixed_chunk_count = (
        index_fixed_chunks(
            fixed_collection,
            documents
        )
    )

    print(
        f"Indexed {fixed_chunk_count} fixed-size chunks."
    )

    print(
        "\nIndexing Sentence-Based Chunks..."
    )

    sentence_chunk_count = (
        index_sentence_chunks(
            sentence_collection,
            documents
        )
    )

    print(
        f"Indexed {sentence_chunk_count} sentence chunks."
    )

    print("\nINDEXING SUMMARY:")

    print(
        f"Documents Loaded          : {len(documents)}"
    )

    print(
        f"Fixed Chunks Indexed      : {fixed_chunk_count}"
    )

    print(
        f"Sentence Chunks Indexed   : {sentence_chunk_count}"
    )

    print(
        f"Fixed Collection Count    : {fixed_collection.count()}"
    )

    print(
        f"Sentence Collection Count : {sentence_collection.count()}"
    )

    print(
        "\nChromaDB collections created successfully."
    )

# Main Execution:
if __name__ == "__main__":
    main()