from typing import List
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from connector import request_to_model, save_embedding_to_search


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageHistory(BaseModel):
    role: str
    content: str

class UserMessage(BaseModel):
    messages: List[MessageHistory]
    chat_id: int = -1
    username: str = "ABC"
    top_p: float = 1
    temperature: float = 0
    max_tokens: int = 4000
    model: str = "gpt-35-turbo-16k"
    proposal_model: int = 1

class LegalArticle(BaseModel):
    id: str = str(uuid4())
    Protestor: str
    Solicitation_Number: str
    Outcome: str
    Filed_Date: str
    Due_Date: str
    Case_Type: str
    Agency: str
    File_Number: str
    GAO_Attorney: str
    Recommendation: str
    Executive_Action_Recommendation: str
    GAO_Contacts: str
    Decision: str
    Published_Date: str
    Publicly_Released_Date: str
    Decision_Date: str


@app.get('/api/')
def get_func():
    return {'text': 'hello world'}, 200

@app.get('/')
def get_func():
    return {'health': 'okay'}, 200

@app.post('/api/messages', status_code=200)
def submit_message(input: UserMessage):
    """
    Send message to the model to get AI response
    """
    response = request_to_model(input)
    return {
        "id": response.id,
        "model": response.model,
        "created": response.created,
        "object": response.object,
        # "history_metadata": history_metadata,
        "choices": [{
            "messages": [{
                "role": "assistant",
                "content": response.choices[0].message.content
            }]
        }]
    }

@app.post('/api/create-embeddings', status_code=200)
def create_legal_embeddings(article: LegalArticle):
    """
    Create legal articles embeddings and save to search
    """
    index_name = 'legal-custom-index'
    save_embedding_to_search(article, index_name)
    return {"response": "Data inserted successfully", "success": True}, 200
