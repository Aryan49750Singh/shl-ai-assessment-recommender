import json
import re


# -----------------------------
# LOAD DETAILED CATALOG
# -----------------------------

with open("detailed_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


# -----------------------------
# SIMPLE SKILL EXTRACTION
# -----------------------------

TECH_KEYWORDS = [
    "java",
    "python",
    "sql",
    ".net",
    "mvc",
    "cloud",
    "backend",
    "frontend",
    "developer",
    "programming",
    "software",
    "coding",
    "api",
    "communication",
    "leadership",
    "problem solving",
    "analytics",
    "stakeholder"
]


# -----------------------------
# ENRICH DATA
# -----------------------------

enriched_catalog = []

for item in catalog:

    text = item["description"].lower()

    found_skills = []

    for keyword in TECH_KEYWORDS:

        if keyword in text:

            found_skills.append(keyword)

    enriched_item = {
        "name": item["name"],
        "url": item["url"],
        "description": item["description"],
        "skills": found_skills
    }

    enriched_catalog.append(enriched_item)


# -----------------------------
# SAVE
# -----------------------------

with open("enriched_catalog.json", "w", encoding="utf-8") as f:

    json.dump(enriched_catalog, f, indent=4, ensure_ascii=False)

print("Enriched catalog saved")