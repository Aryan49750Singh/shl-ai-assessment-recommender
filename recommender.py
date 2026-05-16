# import json
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('all-MiniLM-L6-v2')


# # -----------------------------
# # LOAD CATALOG
# # -----------------------------

# with open("catalog.json", "r", encoding="utf-8") as f:
#     catalog = json.load(f)

# print("Catalog loaded")


# # -----------------------------
# # LOAD MODEL
# # -----------------------------

# print("Loading embedding model...")

# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )

# print("Embedding model loaded")


# # -----------------------------
# # PREPARE TEXTS
# # -----------------------------

# texts = []

# for item in catalog:

#     text = f"""
#     Name: {item.get('name', '')}
#     Category: {item.get('category', '')}
#     Test Type: {item.get('test_type', '')}
#     Skills: {' '.join(item.get('skills', []))}
#     """

#     texts.append(text)


# # -----------------------------
# # CREATE EMBEDDINGS
# # -----------------------------

# print("Creating embeddings...")

# embeddings = model.encode(texts)

# embeddings = np.array(
#     embeddings,
#     dtype=np.float32
# )

# print("Embeddings ready")


# # -----------------------------
# # CREATE FAISS INDEX
# # -----------------------------

# dimension = embeddings.shape[1]

# index = faiss.IndexFlatL2(dimension)

# index.add(embeddings)

# print("FAISS index ready")


# # -----------------------------
# # SEARCH FUNCTION
# # -----------------------------

# def search_assessments(query, top_k=10):

#     query_embedding = model.encode([query])

#     query_embedding = np.array(
#         query_embedding,
#         dtype=np.float32
#     )

#     distances, indices = index.search(
#         query_embedding,
#         top_k
#     )

#     results = []

#     for idx in indices[0]:

#         item = catalog[idx]

#         results.append({
#             "name": item.get("name", ""),
#             "url": item.get("url", ""),
#             "category": item.get("category", "General"),
#             "test_type": item.get("test_type", "Unknown"),
#             "skills": item.get("skills", [])
#         })

#     return results

# import json
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer


# # -----------------------------
# # LOAD CATALOG
# # -----------------------------

# with open("catalog.json", "r", encoding="utf-8") as f:
#     catalog = json.load(f)

# print("Catalog loaded")


# # -----------------------------
# # LOAD MODEL
# # -----------------------------

# print("Loading embedding model...")

# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )

# print("Embedding model loaded")


# # -----------------------------
# # PREPARE TEXTS
# # -----------------------------

# texts = []

# for item in catalog:

#     text = f"""
#     Name: {item.get('name', '')}
#     Category: {item.get('category', '')}
#     Test Type: {item.get('test_type', '')}
#     Skills: {' '.join(item.get('skills', []))}
#     """

#     texts.append(text)


# # -----------------------------
# # CREATE EMBEDDINGS
# # -----------------------------

# print("Creating embeddings...")

# embeddings = model.encode(
#     texts,
#     convert_to_numpy=True
# ).astype("float32")

# print("Embeddings ready")


# # -----------------------------
# # CREATE FAISS INDEX
# # -----------------------------

# dimension = embeddings.shape[1]

# index = faiss.IndexFlatL2(dimension)

# index.add(embeddings)

# print("FAISS index ready")


# # -----------------------------
# # RECOMMEND FUNCTION
# # -----------------------------

# def recommend_assessments(query, top_k=5):

#     query_embedding = model.encode(
#         [query],
#         convert_to_numpy=True
#     ).astype("float32")

#     distances, indices = index.search(
#         query_embedding,
#         top_k
#     )

#     results = []

#     for idx in indices[0]:

#         item = catalog[idx]

#         results.append({
#             "name": item.get("name", ""),
#             "url": item.get("url", ""),
#             "category": item.get("category", "General"),
#             "test_type": item.get("test_type", "Unknown"),
#             "skills": item.get("skills", [])
#         })

#     return results

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
# PREPARE SEARCH TEXTS
# -----------------------------

texts = []

for item in catalog:

    combined_text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {' '.join(item.get('skills', []))}
    {item.get('category', '')}
    {item.get('test_type', '')}
    """

    texts.append(combined_text)


# -----------------------------
# CREATE TF-IDF VECTORS
# -----------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

text_vectors = vectorizer.fit_transform(texts)

print("Retriever ready")


# -----------------------------
# RECOMMEND FUNCTION
# -----------------------------

def recommend_assessments(query, top_k=5):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        text_vectors
    )

    scores = similarities[0]

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    seen_urls = set()

    for idx in ranked_indices:

        item = catalog[idx]

        url = item.get("url", "")

        # Avoid duplicates
        if url in seen_urls:
            continue

        seen_urls.add(url)

        results.append({
            "name": item.get("name", ""),
            "url": url,
            "category": item.get("category", "General"),
            "test_type": item.get("test_type", "Unknown"),
            "skills": item.get("skills", [])
        })

    return results