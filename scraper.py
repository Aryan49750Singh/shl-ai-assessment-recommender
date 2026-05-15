import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# -----------------------------
# CHROME OPTIONS
# -----------------------------

options = Options()

options.add_argument("--start-maximized")


# -----------------------------
# START DRIVER
# -----------------------------

driver = webdriver.Chrome(options=options)

driver.get(
    "https://www.shl.com/solutions/products/product-catalog/"
)

time.sleep(5)

print("Website opened")


# -----------------------------
# STORAGE
# -----------------------------

catalog = []

seen = set()


# -----------------------------
# SCRAPE CURRENT PAGE
# -----------------------------

def scrape_current_page():

    links = driver.find_elements(By.TAG_NAME, "a")

    count_before = len(catalog)

    for link in links:

        try:

            url = link.get_attribute("href")

            text = link.text.strip()

            if not url:
                continue

            if "/products/product-catalog/view/" not in url:
                continue

            if text == "":
                continue

            if url in seen:
                continue

            seen.add(url)

            # -----------------------------
            # SMART METADATA
            # -----------------------------

            lower_text = text.lower()

            category = "General"
            test_type = "Unknown"
            skills = []

            # TECHNICAL
            tech_keywords = [
                "java", "python", "sql", "react",
                "node", "cloud", "aws", "docker",
                "kubernetes", "programming",
                "data science", "selenium",
                "linux", "javascript"
            ]

            # PERSONALITY
            personality_keywords = [
                "opq", "personality",
                "motivation", "behavior"
            ]

            # COGNITIVE
            cognitive_keywords = [
                "verify", "reasoning",
                "numerical", "deductive",
                "inductive"
            ]

            # COMMUNICATION
            communication_keywords = [
                "communication",
                "spoken",
                "english",
                "writing"
            ]

            # -----------------------------
            # CATEGORY DETECTION
            # -----------------------------

            for keyword in tech_keywords:

                if keyword in lower_text:

                    category = "Technical"

                    test_type = "Technical"

                    skills.append(keyword)

            for keyword in personality_keywords:

                if keyword in lower_text:

                    category = "Personality"

                    test_type = "Personality"

            for keyword in cognitive_keywords:

                if keyword in lower_text:

                    category = "Cognitive"

                    test_type = "Cognitive"

            for keyword in communication_keywords:

                if keyword in lower_text:

                    category = "Communication"

                    test_type = "Communication"

            # -----------------------------
            # SAVE
            # -----------------------------

            catalog.append({
                "name": text,
                "url": url,
                "category": category,
                "test_type": test_type,
                "skills": skills
            })

            print(text)

        except Exception as e:

            print("Error:", e)

    count_after = len(catalog)

    print(f"Added {count_after - count_before} items")


# -----------------------------
# LOOP THROUGH PAGES
# -----------------------------

MAX_PAGES = 32

for page in range(MAX_PAGES):

    print(f"\nScraping page {page + 1}")

    scrape_current_page()

    try:

        next_buttons = driver.find_elements(
            By.LINK_TEXT,
            "Next"
        )

        if len(next_buttons) == 0:

            print("No next button found")
            break

        next_button = next_buttons[-1]

        driver.execute_script(
            "arguments[0].click();",
            next_button
        )

        time.sleep(5)

    except Exception as e:

        print("Pagination finished")
        print(e)
        break


# -----------------------------
# SAVE JSON
# -----------------------------

with open("catalog.json", "w", encoding="utf-8") as f:

    json.dump(
        catalog,
        f,
        indent=4,
        ensure_ascii=False
    )


print(f"\nFINAL TOTAL: {len(catalog)} assessments")

driver.quit()