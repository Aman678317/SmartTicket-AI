import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client if API key is available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client = None
except Exception as e:
    print(f"Warning: Failed to initialize Gemini client: {e}")
    client = None

def generate_response(ticket_text: str, intent: str, retrieved_doc: dict) -> str:
    """
    Generates a response using the Gemini API.
    Falls back to a mock response if the API key is missing or call fails.
    """
    
    doc_content = retrieved_doc["content"] if retrieved_doc else "No relevant documentation found."
    
    prompt = f"""
    You are an AI support agent for a company. A user has submitted a support ticket.
    Your task is to generate a helpful, polite, and accurate response based ONLY on the retrieved knowledge article below.
    
    User Ticket: "{ticket_text}"
    Predicted Intent: {intent}
    
    Retrieved Knowledge Article:
    ---
    {doc_content}
    ---
    
    Draft a response to the user. Do not invent information that is not in the article. If the article does not answer the user's issue, politely ask them to contact support.
    """

    if client:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                )
            )
            return response.text
        except Exception as e:
            print(f"Gemini API generation failed: {e}. Falling back to mock generator.")
    
    # Mock fallback
    return _mock_generate(ticket_text, intent, doc_content)


def _mock_generate(ticket: str, intent: str, doc_content: str) -> str:
    # A simple deterministic fallback for demonstration purposes
    return (
        "*(Mock LLM Response - No API Key Found)*\n\n"
        f"Hello, based on your ticket, it looks like you need help with **{intent}**.\n\n"
        f"Here is the information from our knowledge base that should help:\n\n"
        f"{doc_content}\n\n"
        "If you need further assistance, please contact the IT Help Desk."
    )
