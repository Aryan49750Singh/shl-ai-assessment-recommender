# from dotenv import load_dotenv
# import os

# load_dotenv()

# API_KEY = os.getenv("AIzaSyDNnVUg3mlKKZnlIkgcsiCDWjggyQD-G")

# def generate_reply(prompt):

#     try:

#         response = model.generate_content(
#             prompt,
#             generation_config={
#                 "temperature": 0.3,
#                 "max_output_tokens": 150
#             }
#         )

#         if hasattr(response, "text"):

#             return response.text

#         return "I found relevant SHL assessments for your query."

#     except Exception as e:

#         print("Gemini Error:", e)

#         return "I found relevant SHL assessments for your query."

def generate_reply(query, recommendations_count=0):

    if recommendations_count == 0:

        return (
            "No matching SHL assessments were found "
            "for your query."
        )

    return (
        f"Found {recommendations_count} relevant "
        f"SHL assessments based on your requirements."
    )