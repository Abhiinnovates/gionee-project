from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json

# Import our custom modules
from models.schemas import QuizRequest, QuizResponse
from core.groq_client import generate_quiz_from_llm
from services.prompt_utils import get_quiz_system_prompt, get_quiz_user_prompt

app = FastAPI(title="Gionee Backend API")

# Mount the static directory so FastAPI can serve our CSS/JS files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Override the root endpoint to return our frontend UI!
@app.get("/")
def read_root():
    return FileResponse("static/index.html")


# This is the main endpoint that the frontend will call
@app.post("/api/v1/quiz", response_model=QuizResponse)
def create_quiz(request: QuizRequest):
    try:
        # 1. Build the prompts using our utilities
        system_prompt = get_quiz_system_prompt()
        user_prompt = get_quiz_user_prompt(
            topic=request.topic,
            difficulty=request.difficulty,
            num_questions=request.num_questions,
        )

        # 2. Send to Groq's LLaMA 3 model
        raw_llm_response = generate_quiz_from_llm(system_prompt, user_prompt)

        # 3. Parse the string response into an actual JSON dictionary
        quiz_data = json.loads(raw_llm_response)

        # FastAPI automatically validates this against our QuizResponse schema!
        return quiz_data

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="The AI failed to return valid JSON."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
