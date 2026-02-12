import os
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Load environment variables from .env
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    model_id = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-lite")

    if not api_key or api_key == "your_api_key_here":
        print("Error: GOOGLE_API_KEY is not set correctly in the .env file.")
        print("Please replace 'your_api_key_here' with a valid Gemini API key.")
        return

    # 2. Read prompt.md file content
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print("Error: prompt.md file not found.")
        return

    # 3. Create google-genai Client and call Gemini
    print(f"--- Initializing Gemini Client (Model: {model_id}) ---")
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_content
        )
        
        # 4. Print response text
        print("\n--- Gemini Response ---")
        print(response.text)
        
    except Exception as e:
        print(f"An error occurred while calling Gemini API: {e}")

if __name__ == "__main__":
    main()
