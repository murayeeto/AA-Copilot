from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def chat_with_assistant(prompt):
    """
    Query OpenAI GPT using the updated /v1/chat/completions endpoint.
    """
    try:
        # Sending a request to /v1/chat/completions
        response = client.chat.completions.create(
            model="gpt-4",  # Replace with your model ID, e.g., "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )
        # Extract and return the assistant's reply
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error in chat_with_assistant: {e}")
        return f"Error: {e}"

def get_bag_eta(destination):
    """
    Use OpenAI to get an estimated time for bag retrieval at the destination.
    """
    prompt = f"How long does it typically take to retrieve bags at {destination}? Provide a one-sentence estimate."
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Replace with your model ID, e.g., "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error in get_bag_eta: {e}")
        return f"Error: {e}"
