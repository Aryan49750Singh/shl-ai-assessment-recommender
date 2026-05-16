# SHL Assessment Recommendation System

This project is an AI-powered recommendation system that suggests relevant SHL assessments based on user hiring requirements or job descriptions.

The system uses Natural Language Processing (NLP) with TF-IDF vectorization and cosine similarity to match user queries with suitable SHL assessments from the SHL product catalog.

---

## Features

- SHL assessment recommendation engine
- FastAPI backend
- NLP-based semantic matching
- Lightweight TF-IDF retrieval system
- REST API endpoints
- Clarification handling for vague queries
- Unsafe query refusal handling
- Deployment ready for Render

---

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity
- Uvicorn
- Selenium (for scraping catalog data)

---

## API Endpoints

### Health Check

GET `/health`

Response:

```json
{
  "status": "ok"
}
```

---

### Chat Recommendation Endpoint

POST `/chat`

Example Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Need python backend developer assessment"
    }
  ]
}
```

Example Response:

```json
{
  "reply": "Here are recommended SHL assessments based on your requirements.",
  "recommendations": [
    {
      "name": "Python (New)",
      "url": "https://www.shl.com/products/product-catalog/view/python-new/",
      "category": "Technical",
      "test_type": "Technical",
      "skills": [
        "python"
      ]
    }
  ],
  "end_of_conversation": true
}
```

---

## Project Structure

```bash
SHL-AI-AGENT/
│
├── app.py
├── recommender.py
├── scraper.py
├── llm_engine.py
├── catalog.json
├── requirements.txt
├── Procfile
├── runtime.txt
├── README.md
├── .env.example
└── .gitignore
```

---

## Deployment

Deployed on Render.

Live API:

https://shl-ai-assessment-recommender-6-ojie.onrender.com

Swagger Docs:

https://shl-ai-assessment-recommender-6-ojie.onrender.com/docs

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Aryan49750Singh/shl-ai-assessment-recommender.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
uvicorn app:app --reload
```

---

## Dataset

The assessment catalog was scraped from SHL Product Catalog using Selenium automation.

Total assessments scraped: 389

---

## Future Improvements

- Hybrid semantic search
- Better ranking logic
- LLM-enhanced explanations
- Skill extraction pipeline
- Conversation memory
- Frontend UI integration

---

## Author

Aryan

