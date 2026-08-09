import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


MODEL_NAME = "llama-3.3-70b-versatile"


def generate_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 512,
) -> str:
    """
    Generate a response using the configured Groq model.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()