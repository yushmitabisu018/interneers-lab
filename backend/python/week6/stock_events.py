from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

if __name__ == "__main__":
    prompt="" \
    "Generate 10 future stock events for a toy warehouse." \
     "Return only a valid JSON array." \
     "" \
     "Each event must have:" \
     "product_name(string)" \
     "event_type(like one of: 'restock', 'sale','expiry','return')" \
     "quantity(integer)" \
     "date(string,format:YYYY-MM-DD)" \
     "" \
     "Date must be after 2026-03-30"

    response=client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents=prompt,
        config={"temperature":0.7}
    )

    output=response.text

    #cleaning output
    cleaned_output=output.strip()
    if(cleaned_output.startswith("```")):
        cleaned_output=cleaned_output.replace("```json","").replace("```","").strip()

    #parsing JSON
    events = []
    try:
        events= json.loads(cleaned_output)
        print("json parsed successfully")
        print(f"Total events: {len(events)}")
    except Exception as e:
        print("JSON parsing failed:", e)

    for i,event in enumerate(events):
        print(f"Event {i+1}:{event}")