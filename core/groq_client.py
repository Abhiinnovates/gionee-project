from groq import Groq
from core.config import settings

# Initialize the Groq client
groq_client = Groq(api_key=settings.GROQ_API_KEY)


def generate_quiz_from_llm(system_prompt: str, user_prompt: str) -> str:
    """Sends prompts to Groq and returns the raw JSON string."""
    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=settings.MODEL_NAME,
        temperature=0.3,  # Low temperature keeps the JSON formatting strict
        response_format={"type": "json_object"},  # Forces Groq to return valid JSON
    )
    return response.choices[0].message.content
