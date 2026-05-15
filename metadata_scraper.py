import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


# -----------------------------
# LOAD EXISTING CATALOG
# -----------------------------

with open("catalog.json", "r", encoding="utf-8") as f:

    catalog = json.load(f)

print(f"Loaded {len(catalog)} assessments")


# -----------------------------
# CHROME SETUP
# -----------------------------

options = webdriver.ChromeOptions()

options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("Chrome started")


# -----------------------------
# SCRAPE DETAILS
# -----------------------------

detailed_catalog = []

for item in catalog:

    try:

        print(f"\nOpening: {item['name']}")

        driver.get(item["url"])

        time.sleep(5)

        body = driver.find_element(By.TAG_NAME, "body")

        page_text = body.text

        detailed_item = {
            "name": item["name"],
            "url": item["url"],
            "description": page_text[:4000]
        }

        detailed_catalog.append(detailed_item)

        print("Saved")

    except Exception as e:

        print("Error:", e)


# -----------------------------
# SAVE OUTPUT
# -----------------------------

with open("detailed_catalog.json", "w", encoding="utf-8") as f:

    json.dump(detailed_catalog, f, indent=4, ensure_ascii=False)

print("\nDetailed catalog saved successfully")


# -----------------------------
# CLOSE DRIVER
# -----------------------------

driver.quit()