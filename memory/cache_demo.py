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

from rag.rag_engine import (
    answer_with_rag,
    CACHE
)

# Clear the Cache:
CACHE.clear()

query = "What is the warranty on electronics?"

print("\nFIRST REQUEST")
print(answer_with_rag(query))

print("\nSECOND REQUEST")
print(answer_with_rag(query))