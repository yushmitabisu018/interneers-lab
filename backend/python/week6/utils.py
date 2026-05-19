import json


def clean_and_parse_json(text):
    #Clean LLM output and parse JSON with robust error handling.
    
    try:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        
        parsed = json.loads(cleaned)
        
        if isinstance(parsed, dict):
            return [parsed]
        elif isinstance(parsed, list):
            return parsed
        else:
            return []
            
    except json.JSONDecodeError as e:
        return []
    except Exception as e:
        return []
