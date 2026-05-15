from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from recommender import recommend_assessments, catalog

app = FastAPI()


# -----------------------------
# REQUEST MODELS
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# HEALTH ENDPOINT
# -----------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "assessments_loaded": len(catalog)
    }


# -----------------------------
# CHAT ENDPOINT
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # Get latest user message
        query = request.messages[-1].content

        # Get recommendations
        recommendations = recommend_assessments(query)

        return {
            "query": query,
            "reply": "I found relevant SHL assessments for your query.",
            "total_results": len(recommendations),
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    except Exception as e:

        return {
            "reply": "Something went wrong",
            "error": str(e)
        }