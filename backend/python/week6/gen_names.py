from dotenv import load_dotenv
from google import genai
import os
load_dotenv()

# Model: gemini-2.5-flash-lite
GEMINI_FLASH_LITE_INPUT_COST_PER_TOKEN = 0.0000005
GEMINI_FLASH_LITE_OUTPUT_COST_PER_TOKEN = 0.000001

# print("API KEY:", os.getenv("GOOGLE_API_KEY"))
client= genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))

def generate_products(temperature):
    response = client.models.generate_content(
       model="gemini-2.5-flash-lite",
       contents="Generate 5 product names for a toy store. Return only names as a numbered list.",
       config={
           "temperature": temperature
       }
    )

    print(f"\nTemperature: {temperature}\n")
    
    print("Raw Response object:\n")
    print(response)

    text_output = response.text
    print("\n Parsed text output:\n")
    print(text_output)

    usage=response.usage_metadata
    print("\nToekn usage:")
    print(f"Input tokens: {usage.prompt_token_count}")
    print(f"Output tokens: {usage.candidates_token_count}")
    print(f"Total tokens: {usage.total_token_count}")

    input_cost = usage.prompt_token_count * GEMINI_FLASH_LITE_INPUT_COST_PER_TOKEN
    output_cost=usage.candidates_token_count * GEMINI_FLASH_LITE_OUTPUT_COST_PER_TOKEN
    total_cost= input_cost + output_cost

    print("\nCost estimation:")
    print(f"Input cost: ${input_cost:.8f}")
    print(f"Output cost: ${output_cost:.8f}")
    print(f"Total cost: ${total_cost:.8f}")

if __name__ == "__main__":
    for temp in [0.0, 0.5, 1.0, 1.5]:
        generate_products(temp)
