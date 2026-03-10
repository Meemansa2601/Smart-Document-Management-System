import os
import json
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

# Load key from .env for security
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class DocumentProcessor:
    def __init__(self):
        # Initialize the unified client
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        # Using 2.0 Flash-Lite for high-speed, free-tier stability
        self.model_id = "gemini-2.0-flash-lite"

    def analyze_with_ai(self, ocr_text):
        if not ocr_text.strip():
            return {"category": "Error", "plain_language": "No text detected."}

        # Define the strict structure we want the AI to follow
        prompt = f"""
        Analyze this document text and extract details into a JSON format.
        TEXT: {ocr_text}
        
        REQUIRED JSON STRUCTURE:
        {{
            "category": "Education/Medical/Bills/Legal/Receipt",
            "plain_language": "One simple summary sentence",
            "extracted_data": {{
                "participant_name": "Name on doc",
                "event_name": "Workshop/Course name",
                "organization": "College/Company",
                "signatories": ["Names of people who signed"],
                "dates": ["Dates found"],
                "amounts": [0]
            }},
            "panic_alert": "Urgency message",
            "emotion_support": "Supportive message"
        }}
        """

        try:
            # Generate content using the new client syntax
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            # The new SDK handles JSON parsing more cleanly
            return json.loads(response.text)
            
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            return {"category": "Error", "plain_language": f"API Error: {str(e)}"}