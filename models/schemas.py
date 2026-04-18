from pydantic import BaseModel, Field
from typing import List


# 1. Schema for a single Question
class Question(BaseModel):
    id: int = Field(..., description="A unique identifier for the question")
    question_text: str = Field(..., description="The actual quiz question")
    options: List[str] = Field(
        ...,
        min_length=2,
        description="List of possible answers. Must contain at least 2 options.",
    )
    correct_answer: str = Field(..., description="The exact text of the correct option")
    explanation: str = Field(
        ..., description="A brief explanation of why this answer is correct"
    )


# 2. Schema for the entire Quiz (This is what the LLM will return)
class QuizResponse(BaseModel):
    topic: str = Field(..., description="The topic of the quiz")
    difficulty: str = Field(
        ..., description="The difficulty level (e.g., Beginner, Intermediate, Advanced)"
    )
    questions: List[Question] = Field(..., description="A list of generated questions")


# 3. Schema for what the user sends TO your API
class QuizRequest(BaseModel):
    topic: str = Field(..., example="Python basics")
    difficulty: str = Field("Beginner", example="Beginner")
    num_questions: int = Field(
        3, ge=1, le=10, description="Number of questions to generate (1-10)"
    )
