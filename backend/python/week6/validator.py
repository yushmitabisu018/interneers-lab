from dotenv import load_dotenv
from google import genai
import os
import json
from schemas import ProductSchema

load_dotenv()
client =genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

if __name__ == "__main__":
    prompt="" \
    "Generate exact 50 products for a toy store." \
    "Return only a valid JSON array." \
    "Each product must have:" \
    "name(string)" \
    "brand(string)" \
    "price(float)" \
    "quantity(integer)" \
    ""

    response= client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={"temperature":0.7}
    )
    output=response.text
    #print(output)

    cleaned_output=output.strip()
    if(cleaned_output.startswith("```")):
        cleaned_output=cleaned_output.replace("```json","").replace("```","").strip()

    #print(cleaned_output)

    #parsing JSON
    products = []
    try:
        products= json.loads(cleaned_output)
        print("json parsed successfully")
        print(f"Total products: {len(products)}")
    except Exception as e:
        print("JSON parsing failed:", e)

    #validation with pydantic
    valid_products=[]
    invalid_products=[] 

    for i,product in enumerate(products):
        try:
            validated=ProductSchema(**product)
            valid_products.append(validated)
        except Exception as e:
            print(f"Product {i} is invalid:",e)
            invalid_products.append(product)

    print(f"\n Valid products: {len(valid_products)}")
    print(f"\n Invalid products: {len(invalid_products)}")            

