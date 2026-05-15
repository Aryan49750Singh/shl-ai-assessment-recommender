import json
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

print("Loading catalog...")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print("Loading model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

texts = []

for item in catalog:

    text = f"""
    Name: {item.get('name', '')}
    Category: {item.get('category', '')}
    Test Type: {item.get('test_type', '')}
    Skills: {' '.join(item.get('skills', []))}
    """

    texts.append(text)

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True
).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "index.faiss")

with open("metadata.pkl", "wb") as f:
    pickle.dump(catalog, f)

print("Index saved successfully")