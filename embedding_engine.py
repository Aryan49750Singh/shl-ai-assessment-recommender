import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# -----------------------------
# LOAD CATALOG
# -----------------------------

with open("detailed_catalog.json", "r", encoding="utf-8") as f:

    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")


# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded")


# -----------------------------
# PREPARE TEXTS
# -----------------------------

texts = []

for item in catalog:

    combined_text = f"""
    Name: {item['name']}
    Description: {item['description']}
    """

    texts.append(combined_text)

print("Prepared texts")


# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------

embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

print("Embeddings created")


# -----------------------------
# CREATE FAISS INDEX
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS index created")


# -----------------------------
# SEARCH FUNCTION
# -----------------------------

def search_assessments(query, top_k=5):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:

        results.append(catalog[idx])

    return results


# -----------------------------
# TEST QUERY
# -----------------------------

query = "Java developer with communication skills"

results = search_assessments(query)

print("\nTop Results:\n")

for result in results:

    print(result["name"])
    print(result["url"])
    print("-" * 50)