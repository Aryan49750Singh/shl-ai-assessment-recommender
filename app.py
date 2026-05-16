from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from recommender import recommend_assessments
from llm_engine import generate_reply

app = FastAPI(
    title="SHL AI Assessment Recommendation Agent",
    version="1.0.0"
)


# -----------------------------
# REQUEST MODELS
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# BLOCKED TOPICS
# -----------------------------

BLOCKED_KEYWORDS = {
    "salary",
    "legal",
    "politics",
    "ignore previous instructions",
    "bypass",
    "hack"
}


# -----------------------------
# HELPERS
# -----------------------------

def extract_full_conversation(messages):

    return "\n".join(
        f"{msg.role}: {msg.content}"
        for msg in messages
    ).lower()


def should_refuse(text):

    return any(
        keyword in text
        for keyword in BLOCKED_KEYWORDS
    )


def needs_clarification(text):

    text = text.lower()

    vague_phrases = {
        "need assessment",
        "need an assessment",
        "need test",
        "need tests"
    }

    strong_signals = {
        "developer",
        "engineer",
        "java",
        "python",
        "sales",
        "manager",
        "communication",
        "stakeholder",
        "analyst",
        "backend",
        "frontend",
        "cloud",
        "sql",
        "react",
        "node"
    }

    has_strong_signal = any(
        signal in text
        for signal in strong_signals
    )

    if has_strong_signal:
        return False

    vague_match = any(
        phrase in text
        for phrase in vague_phrases
    )

    short_query = len(text.split()) < 3

    return vague_match or short_query


# -----------------------------
# ROOT ENDPOINT
# -----------------------------

@app.get("/")
def root():

    return {
        "message": "SHL AI Agent Running"
    }


# -----------------------------
# HEALTH ENDPOINT
# -----------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# -----------------------------
# CHAT ENDPOINT
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        if not request.messages:

            return {
                "reply": "No messages provided.",
                "recommendations": [],
                "end_of_conversation": False
            }

        conversation = extract_full_conversation(
            request.messages
        )

        # -----------------------------
        # REFUSAL
        # -----------------------------

        if should_refuse(conversation):

            return {
                "reply": (
                    "I can only help with "
                    "SHL assessment recommendations."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # -----------------------------
        # CLARIFICATION
        # -----------------------------

        if needs_clarification(conversation):

            return {
                "reply": (
                    "Please share more details "
                    "about the role, required skills, "
                    "experience level, or assessment needs."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # -----------------------------
        # RECOMMENDATIONS
        # -----------------------------

        recommendations = recommend_assessments(
            conversation,
            top_k=5
        )

        reply = generate_reply(
            conversation,
            len(recommendations)
        )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    except Exception as e:

        print("CHAT ERROR:", str(e))

        return {
            "reply": "Internal server error.",
            "recommendations": [],
            "end_of_conversation": False
        }