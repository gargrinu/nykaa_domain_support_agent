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

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)

from schemas.api_schema import (
    AskRequest,
    AskResponse,
    AddDocumentRequest,
    AddDocumentResponse
)

from guardrails.guardrails import input_guardrail
from rag.rag_engine import answer_with_rag
from memory.crew_memory import chat
from logging.structured_logger import log_request
from governance.runtime_budget import enforce_budget

app = FastAPI()

#HTTP Endpoints:
@app.post("/ask",response_model=AskResponse)
async def ask_question(request: AskRequest):
    # Runtime Budget Check:
    budget_check = enforce_budget(request.query)

    if not budget_check["allowed"]:
        return AskResponse(answer=budget_check["message"])

    # Input Guardrails:
    guardrail_result = (input_guardrail(request.query))

    if not guardrail_result["allowed"]:
        return AskResponse(answer=guardrail_result["message"])

    # RAG/Crew Processing:
    answer = answer_with_rag(guardrail_result["masked_input"])

    # Structured Logging:
    log_request(request_text=request.query,response_text=answer)

    # Response:
    return AskResponse(answer=answer)

@app.post("/add-document",response_model=AddDocumentResponse)
async def add_document(request:AddDocumentRequest):
    path = (f"knowledge_base/{request.document_name}")

    with open(path,"w",encoding="utf-8") as file:
        file.write(request.content)

    return AddDocumentResponse(message="Document added successfully.")

# Websocket Endpoint:
@app.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    session_id = (str(id(websocket)))

    try:
        while True:
            query = (await websocket.receive_text())
            response = chat(session_id,query)
            await websocket.send_text(response)

    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")