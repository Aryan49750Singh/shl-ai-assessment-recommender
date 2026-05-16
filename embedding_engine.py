# import json
# import numpy as np
# import faiss

# from sentence_transformers import SentenceTransformer


# # -----------------------------
# # LOAD CATALOG
# # -----------------------------

# with open("detailed_catalog.json", "r", encoding="utf-8") as f:

#     catalog = json.load(f)

# print(f"Loaded {len(catalog)} assessments")


# # -----------------------------
# # LOAD EMBEDDING MODEL
# # -----------------------------

# model = SentenceTransformer("all-MiniLM-L6-v2")

# print("Embedding model loaded")


# # -----------------------------
# # PREPARE TEXTS
# # -----------------------------

# texts = []

# for item in catalog:

#     combined_text = f"""
#     Name: {item['name']}
#     Description: {item['description']}
#     """

#     texts.append(combined_text)

# print("Prepared texts")


# # -----------------------------
# # CREATE EMBEDDINGS
# # -----------------------------

# embeddings = model.encode(texts)

# embeddings = np.array(embeddings).astype("float32")

# print("Embeddings created")


# # -----------------------------
# # CREATE FAISS INDEX
# # -----------------------------

# dimension = embeddings.shape[1]

# index = faiss.IndexFlatL2(dimension)

# index.add(embeddings)

# print("FAISS index created")


# # -----------------------------
# # SEARCH FUNCTION
# # -----------------------------

# def search_assessments(query, top_k=5):

#     query_embedding = model.encode([query])

#     query_embedding = np.array(query_embedding).astype("float32")

#     distances, indices = index.search(query_embedding, top_k)

#     results = []

#     for idx in indices[0]:

#         results.append(catalog[idx])

#     return results


# # -----------------------------
# # TEST QUERY
# # -----------------------------

# query = "Java developer with communication skills"

# results = search_assessments(query)

# print("\nTop Results:\n")

# for result in results:

#     print(result["name"])
#     print(result["url"])
#     print("-" * 50)

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# LOAD CATALOG
# -----------------------------

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")


# -----------------------------
# PREPARE TEXTS
# -----------------------------

texts = []

for item in catalog:

    combined_text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {' '.join(item.get('skills', []))}
    {item.get('category', '')}
    """

    texts.append(combined_text)


# -----------------------------
# TF-IDF VECTORIZER
# -----------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

text_vectors = vectorizer.fit_transform(texts)

print("TF-IDF vectors created")


# -----------------------------
# SEARCH FUNCTION
# -----------------------------

def search_assessments(query, top_k=5):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, text_vectors)

    scores = similarities[0]

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for idx in ranked_indices:
        item = catalog[idx]

        results.append({
            "name": item.get("name"),
            "url": item.get("url"),
            "category": item.get("category"),
            "description": item.get("description"),
            "score": float(scores[idx])
        })

    return results


# -----------------------------
# TEST
# -----------------------------

if __name__ == "__main__":

    query = "Java developer with communication skills"

    results = search_assessments(query)

    for result in results:
        print(result["name"])
        print(result["url"])
        print(result["score"])
        print("-" * 50)