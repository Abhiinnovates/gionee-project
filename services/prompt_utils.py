import json
from models.schemas import QuizResponse


def get_quiz_system_prompt() -> str:
    """
    Generates the system prompt instructing the LLM on its role and expected output format.
    """
    # This is an enterprise trick: we pull the exact schema directly from our Pydantic model!
    schema = QuizResponse.model_json_schema()

    return f"""You are Gionee, an advanced AI study helper and expert educational tutor. 
Your primary goal is to generate high-quality, accurate, and educational multiple-choice quizzes.

CRITICAL INSTRUCTIONS:
1. You must return your response ONLY as a valid JSON object.
2. Do not include any markdown formatting (like ```json), conversational text, or greetings.
3. The questions must be challenging but fair, with clear, concise explanations for the correct answer.

The JSON MUST exactly match the following schema structure:
{json.dumps(schema, indent=2)}
"""


def get_quiz_user_prompt(topic: str, difficulty: str, num_questions: int) -> str:
    """
    Generates the specific user request.
    """
    return f"""Please generate a study quiz based on the following parameters:
- Topic: {topic}
- Difficulty Level: {difficulty}
- Total Number of Questions: {num_questions}

Ensure the 'explanation' field clearly explains why the correct answer is right and why the others might be wrong."""
