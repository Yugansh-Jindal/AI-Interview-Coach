import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "openai/gpt-oss-120b"


def generate_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    json_mode: bool = False,
) -> str:

    request_data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": temperature,
        "max_completion_tokens": max_tokens,

        # Important for GPT-OSS:
        # Don't return reasoning in the response.
        "include_reasoning": False,

        # Keep reasoning low so the model has enough tokens
        # to produce the actual answer.
        "reasoning_effort": "low",
    }

    if json_mode:
        request_data["response_format"] = {
            "type": "json_object"
        }

    response = client.chat.completions.create(**request_data)

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response.")

    return content.strip()