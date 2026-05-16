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
# BLOCKED TOPICS
# -----------------------------

BLOCKED_KEYWORDS = [
    "salary",
    "legal",
    "politics",
    "ignore previous instructions",
    "bypass",
    "hack"
]


# -----------------------------
# HELPERS
# -----------------------------

def extract_full_conversation(messages):

    combined = ""

    for msg in messages:
        combined += f"{msg.role}: {msg.content}\n"

    return combined.lower()


def should_refuse(text):

    for keyword in BLOCKED_KEYWORDS:

        if keyword in text:
            return True

    return False


def needs_clarification(text):

    text = text.lower()

    vague_phrases = [
        "need assessment",
        "need an assessment",
        "need test",
        "need tests"
    ]

    # If clearly contains role/skills info,
    # do NOT clarify further
    strong_signals = [
        "developer",
        "engineer",
        "java",
        "python",
        "sales",
        "manager",
        "communication",
        "stakeholder",
        "analyst"
    ]

    has_strong_signal = any(
        signal in text for signal in strong_signals
    )

    if has_strong_signal:
        return False

    vague_match = any(
        phrase in text for phrase in vague_phrases
    )

    short_query = len(text.split()) < 3

    return vague_match or short_query


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

        conversation = extract_full_conversation(
            request.messages
        )

        latest_user_message = request.messages[-1].content

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
                    "Could you share more details "
                    "about the role, skills, seniority, "
                    "or assessment requirements?"
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

        return {
            "reply": (
                "Here are recommended SHL assessments "
                "based on your requirements."
            ),
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    except Exception as e:

        return {
            "reply": "Something went wrong",
            "recommendations": [],
            "end_of_conversation": False,
            "error": str(e)
        }