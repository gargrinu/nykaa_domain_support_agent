from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str

class AddDocumentRequest(BaseModel):
    document_name: str
    content: str

class AddDocumentResponse(BaseModel):
    message: str