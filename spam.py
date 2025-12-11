from google import genai
from google.genai import types

# Initialize Gemini client once (reuse for all calls)
client = genai.Client(api_key="AIzaSyBQS1-hhhOqzv8JhYTSxJkO3DZAqaNP0zA")  # or use env var

def is_financial_spam_sms(sms_text: str) -> bool:
    """
    Uses Google Gemini to classify an SMS as financial spam or not.

    Returns:
        True  -> financial spam
        False -> not financial spam (legit or other type of message)
    """

    prompt = f"""
You are a strict SMS classifier.

Task:
Given the SMS text below, respond with EXACTLY ONE WORD:
- "SPAM" if it is a financial scam/spam (e.g., fake bank alerts, fake prize, phishing, money transfer scams, fake investment offers, etc.)
- "NOT_SPAM" if it is not financial spam.

SMS:
\"\"\"{sms_text}\"\"\"
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",  # you can also use gemini-1.5-pro
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,  # deterministic, good for classification
            max_output_tokens=5,
        ),
    )

    # Get full text from the response
    reply = response.text.strip().upper()

   
    if reply in ("SPAM", "SP"):
      return True
    elif reply in ("NOT_SPAM", "NOT"):
      return False
    return False


print("WELCOME TO DERA’A")
print("Type a message to analyze.")
print("Type EXIT to quit.\n")

while True:
    msg = input("Enter message: ")
    if msg.lower() == "exit":
        print("Goodbye.")
        break

    is_spam = is_financial_spam_sms(msg)

    # Convert True/False → SPAM / NOT_SPAM
    result = "SPAM" if is_spam else "NOT_SPAM"

    print("Result:", result)
    print("-" * 40)
