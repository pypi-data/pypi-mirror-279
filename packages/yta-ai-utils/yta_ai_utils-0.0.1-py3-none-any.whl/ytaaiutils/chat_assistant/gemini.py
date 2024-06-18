import google.generativeai as genai
import os

def ask(prompt):
    """
    Asks Gemini AI (gemini-1.5-flash) model by using the provided prompt, waits for the response
    and returns it.
    """
    genai.configure(api_key = os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')

    chat = model.start_chat()
    response = chat.send_message(
        prompt,
    )

    return response.text